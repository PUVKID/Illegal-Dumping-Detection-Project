"""학습 시간을 제한하고 검증에서 모델·추론을 선택한 뒤 고정 테스트를 평가합니다."""
import collections
import json
import math
import time
from pathlib import Path

from prepare_dataset import (ROOT, WORK, TRAINING, ARCHIVE, SEED, DownloadBudget,
                             atomic_json, freeze, load, local, portable, prepare,
                             sha256_file, validate_yolo, verify_records, verify_history)

EVALUATOR = 'single-class confidence-greedy IoU; 101-point interpolated AP; v2'


def iou(left,right):
    intersection=max(0,min(left[2],right[2])-max(left[0],right[0]))*max(0,min(left[3],right[3])-max(left[1],right[1]))
    union=max(0,left[2]-left[0])*max(0,left[3]-left[1])+max(0,right[2]-right[0])*max(0,right[3]-right[1])-intersection
    return intersection/union if union else 0.0


def match_predictions(predictions,targets,threshold):
    matched=[False]*len(predictions)
    used=set()
    for index in sorted(range(len(predictions)),key=lambda i:predictions[i][4],reverse=True):
        overlap,identity=max(((iou(predictions[index],box),j) for j,box in enumerate(targets) if j not in used),default=(0,-1))
        if overlap>=threshold:
            matched[index]=True
            used.add(identity)
    return matched


def operating(tp,fp,total,threshold):
    precision=tp/(tp+fp) if tp+fp else 0.0
    recall=tp/total if total else 0.0
    return {'precision':precision,'recall':recall,'f1':2*precision*recall/(precision+recall) if precision+recall else 0.0,
            'threshold':float(threshold),'tp':int(tp),'fp':int(fp),'fn':int(total-tp),'iou':.5}


def average_precision(rows,total,column):
    if not total:return 0.0
    ordered=sorted(rows,key=lambda r:r[0],reverse=True)
    points=[]
    tp=0
    for index,(_,matches) in enumerate(ordered):
        tp+=int(matches[column])
        points.append((tp/total,tp/(index+1)))
    return sum(max((p for r,p in points if r>=step/100),default=0.0) for step in range(101))/101


def summarize(rows,total,threshold=None):
    ordered=sorted(rows,key=lambda r:r[0],reverse=True)
    if threshold is None:
        choices=[]
        tp=0
        for index,(score,matches) in enumerate(ordered):
            tp+=int(matches[0])
            if index+1==len(ordered) or ordered[index+1][0]!=score:
                choices.append(operating(tp,index+1-tp,total,score))
        selected=max(choices,key=lambda r:(min(r['precision'],r['recall']),r['f1']),default=operating(0,0,total,1.0))
    else:
        selected_rows=[matches for score,matches in ordered if score>=threshold]
        tp=sum(m[0] for m in selected_rows)
        selected=operating(tp,len(selected_rows)-tp,total,threshold)
    return {'operating':selected,'metrics':{'AP50':average_precision(rows,total,0),
            'AP50_95':sum(average_precision(rows,total,i) for i in range(10))/10},'evaluator':EVALUATOR}


def choose_candidate(results):
    if not results:raise ValueError('검증 후보가 없습니다.')
    def score(row):
        primary=row['operating']
        secondary=row.get('plastopol',{}).get('operating',{'precision':0.,'recall':0.})
        return (min(primary['precision'],primary['recall']),primary['f1'],
                min(secondary['precision'],secondary['recall']),row['metrics']['AP50'])
    # 기존 모델을 첫 항목으로 전달합니다. 모든 기준이 같으면 기존 선택을 유지합니다.
    return max(results,key=score)


def target_met(result):
    return result['operating']['precision']>=.9 and result['operating']['recall']>=.9


def remaining_seconds(elapsed,hours):
    if not math.isfinite(elapsed) or elapsed<0 or hours*3600-elapsed<=0:
        raise ValueError('후보의 누적 학습 시간 예산이 끝났거나 잘못됐습니다.')
    return hours*3600-elapsed


def enforce_epoch_cap(trainer,maximum):
    if trainer.epoch+1>=maximum:trainer.stop=True


def tile_boxes(width,height,grid=3):
    if width<=0 or height<=0 or grid not in (1,2,3):raise ValueError('허용하지 않는 타일 크기입니다.')
    def axis(length):
        side=min(length,math.ceil(length/(grid-.2*(grid-1))))
        return [(round((length-side)*i/(grid-1)) if grid>1 else 0,side) for i in range(grid)]
    return [(x,y,x+w,y+h) for y,h in axis(height) for x,w in axis(width)]


def shift_predictions(predictions,rectangle):
    left,top,_,_=rectangle
    return [[row[0]+left,row[1]+top,row[2]+left,row[3]+top,row[4]] for row in predictions]


def nms(rows,overlap=.5,maximum=1000):
    import torch
    from torchvision.ops import nms as torch_nms
    if not rows:return []
    tensor=torch.tensor(rows,dtype=torch.float32)
    chosen=torch_nms(tensor[:,:4],tensor[:,4],overlap)[:maximum]
    return tensor[chosen].tolist()


def resume_decision(directory,contract,allow_resume=False):
    directory=Path(directory)
    path=directory/'run_contract.json'
    if path.exists() and load(path)!=contract:raise ValueError('checkpoint 원본·데이터·코드·학습 계약이 다릅니다.')
    if (directory/'phase_complete.json').exists():
        if not path.exists():raise ValueError('완료 학습의 원래 계약이 없습니다.')
        best=directory/'weights/best.pt'
        if not best.exists() or sha256_file(best)!=load(directory/'phase_complete.json')['best_sha256']:
            raise ValueError('완료 학습 가중치가 보존 해시와 다릅니다.')
        return 'complete'
    if (directory/'weights/last.pt').exists():
        if not path.exists() or not allow_resume:raise ValueError('중단 checkpoint는 동일 계약과 명시적 재개가 필요합니다.')
        return 'resume'
    return 'new'


def ground_truth(row):
    labels=validate_yolo(local(row['label']).read_text(encoding='utf-8'))
    width,height=row['width'],row['height']
    return [[(x-w/2)*width,(y-h/2)*height,(x+w/2)*width,(y+h/2)*height] for _,x,y,w,h in labels]


def size_class(box):
    area=(box[2]-box[0])*(box[3]-box[1])
    return 'small' if area<32**2 else 'medium' if area<96**2 else 'large'


def image_counts(predictions,targets,threshold):
    chosen=sorted((r for r in predictions if r[4]>=threshold),key=lambda r:r[4],reverse=True)
    used=set()
    sizes={s:{'tp':0,'fp':0,'fn':0} for s in ('small','medium','large')}
    tp=0
    for row in chosen:
        overlap,index=max(((iou(row,target),i) for i,target in enumerate(targets) if i not in used),default=(0,-1))
        if overlap>=.5:
            used.add(index)
            sizes[size_class(targets[index])]['tp']+=1
            tp+=1
        else:sizes[size_class(row)]['fp']+=1
    for index,target in enumerate(targets):
        if index not in used:sizes[size_class(target)]['fn']+=1
    return {'tp':tp,'fp':len(chosen)-tp,'fn':len(targets)-tp,'sizes':sizes,
            'negative_images':int(not targets),'negative_fp':len(chosen) if not targets else 0}


def wait_gpu(config,notify):
    import torch
    if not torch.cuda.is_available():raise ValueError('CUDA GPU가 없습니다. CPU로 장기 학습을 우회하지 않습니다.')
    deadline=time.monotonic()+config['gpu_wait_seconds']
    while True:
        free,total=torch.cuda.mem_get_info(0)
        notify(stage='다른 GPU 작업을 보존하며 여유 VRAM 확인',gpu_free_mib=free//(1024**2),gpu_total_mib=total//(1024**2))
        if free>=config['gpu_minimum_free_mib']*1024**2:return
        if time.monotonic()>=deadline:raise ValueError('다른 GPU 작업 때문에 필요한 여유 VRAM을 확보하지 못했습니다.')
        time.sleep(15)


def evaluate(weights,records,out,policy,notify,config,threshold=None):
    from PIL import Image
    from ultralytics import YOLO
    import torch
    out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    verify_records(records)
    contract={'weights':{str(p):sha256_file(local(p)) for p in weights},
              'images':{r['id']:[r['sha256'],r['label_sha256']] for r in records},
              'policy':policy,'imgsz':config['evaluation_imgsz'],'conf_floor':config['evaluation_conf_floor'],
              'nms_iou':config['evaluation_nms_iou'],'max_det':config['evaluation_max_det'],
              'threshold':threshold,'evaluator':EVALUATOR}
    freeze(out/'contract.json',contract)
    if (out/'metrics.json').exists():return load(out/'metrics.json')
    wait_gpu(config,notify)
    models=[YOLO(str(local(p))) for p in weights]
    if any(list(model.names.values())!=['trash'] for model in models):raise ValueError('단일 trash 클래스 모델이 아닙니다.')
    scored=[]
    total=0
    per_image=[]
    budget=DownloadBudget(WORK/'sources')
    for index,row in enumerate(records):
        cached=out/'predictions'/(row['id']+'.json')
        if cached.exists():predictions=load(cached)
        else:
            predictions=[]
            with Image.open(local(row['image'])) as image:
                for model in models:
                    result=model.predict(image,imgsz=config['evaluation_imgsz'],conf=config['evaluation_conf_floor'],
                                         iou=config['evaluation_nms_iou'],max_det=config['evaluation_max_det'],device=0,verbose=False)[0]
                    predictions+=result.boxes.data[:,:5].detach().cpu().tolist()
                    if policy=='full_grid3':
                        for rectangle in tile_boxes(*image.size,3):
                            tile=image.crop(rectangle)
                            result=model.predict(tile,imgsz=config['evaluation_imgsz'],conf=config['evaluation_conf_floor'],
                                                 iou=config['evaluation_nms_iou'],max_det=config['evaluation_max_det'],device=0,verbose=False)[0]
                            predictions+=shift_predictions(result.boxes.data[:,:5].detach().cpu().tolist(),rectangle)
            predictions=nms(predictions,config['evaluation_nms_iou'],config['evaluation_max_det'])
            budget.space(1024*1024)
            atomic_json(cached,predictions)
        targets=ground_truth(row)
        total+=len(targets)
        matches=[match_predictions(predictions,targets,.5+.05*i) for i in range(10)]
        scored.extend((p[4],[matches[k][j] for k in range(10)]) for j,p in enumerate(predictions))
        per_image.append((row,predictions,targets))
        if index%10==0:notify(stage='고정 검증·평가 '+out.name,evaluated=index+1,evaluation_images=len(records),policy=policy)
    result=summarize(scored,total,threshold)
    breakdown=collections.defaultdict(lambda:{'tp':0,'fp':0,'fn':0})
    negatives=negative_fp=0
    for row,predictions,targets in per_image:
        scale=config['evaluation_imgsz']/max(row['width'],row['height'])
        scaled_predictions=[[x*scale for x in p[:4]]+[p[4]] for p in predictions]
        scaled_targets=[[x*scale for x in p] for p in targets]
        counts=image_counts(scaled_predictions,scaled_targets,result['operating']['threshold'])
        negatives+=counts['negative_images'];negative_fp+=counts['negative_fp']
        for size,values in counts['sizes'].items():
            for key,value in values.items():breakdown[size][key]+=value
    sizes={s:operating(v['tp'],v['fp'],v['tp']+v['fn'],result['operating']['threshold']) for s,v in breakdown.items()}
    result.update(weights=list(map(str,weights)),policy=policy,imgsz=config['evaluation_imgsz'],images=len(records),
                  weights_sha256=contract['weights'],
                  sizes=sizes,size_definition='bbox area after aspect-preserving 1280 scale; not official COCO APs',
                  negative_images=negatives,negative_false_positives=negative_fp,
                  false_positives_per_negative_image=negative_fp/negatives if negatives else None)
    atomic_json(out/'metrics.json',result)
    del models
    torch.cuda.empty_cache()
    return result


def train_candidate(recipe,manifest,config,notify,resume):
    import torch
    import ultralytics
    from ultralytics import YOLO
    directory=TRAINING/'runs'/recipe['name']
    initial=ARCHIVE/recipe['initial']
    contract={'manifest_sha256':sha256_file(TRAINING/'data_manifest.json'),'initial':portable(initial),
              'initial_sha256':sha256_file(initial),'pipeline_sha256':sha256_file(__file__),
              'preparation_sha256':sha256_file(ROOT/'prepare_dataset.py'),'config_sha256':sha256_file(ROOT/'configs/training.json'),
              'recipe':recipe,'hours':config['candidate_hours'],'seed':SEED,'torch':torch.__version__,
              'ultralytics':ultralytics.__version__,'normalization':manifest['contract']['normalization']}
    mode=resume_decision(directory,contract,resume)
    directory.mkdir(parents=True,exist_ok=True)
    freeze(directory/'run_contract.json',contract)
    best=directory/'weights/best.pt'
    if mode=='complete':return best
    wait_gpu(config,notify)
    budget=DownloadBudget(WORK/'sources')
    budget.space(config['checkpoint_reserve_bytes'])
    elapsed_path=directory/'elapsed.json'
    elapsed=load(elapsed_path).get('used_seconds',0.) if elapsed_path.exists() else 0.
    remaining=remaining_seconds(elapsed,config['candidate_hours'])
    model=YOLO(str(directory/'weights/last.pt' if mode=='resume' else initial))
    start=time.monotonic()
    last_notice=start
    in_epoch=False
    actual_epochs=0
    def batch_end(trainer):
        nonlocal last_notice,in_epoch
        in_epoch=True
        now=time.monotonic()
        if now-last_notice>=30:
            used=elapsed+now-start
            budget.space(config['checkpoint_reserve_bytes'])
            atomic_json(elapsed_path,{'used_seconds':used,'limit_seconds':config['candidate_hours']*3600})
            notify(stage='학습 '+recipe['name'],epoch=trainer.epoch+1,epochs=recipe['epochs'],training_seconds=used)
            last_notice=now
    def before_validation(trainer):
        budget.space(config['checkpoint_reserve_bytes'])
        enforce_epoch_cap(trainer,recipe['epochs'])
    def epoch_end(trainer):
        nonlocal in_epoch,actual_epochs
        # final_eval은 같은 callback을 다시 호출하므로 학습 batch가 있었던 epoch만 집계합니다.
        if not in_epoch:return
        actual_epochs=trainer.epoch+1
        in_epoch=False
        metrics={str(k):float(v) for k,v in trainer.metrics.items()}
        notify(stage='학습 '+recipe['name'],epoch=actual_epochs,epochs=recipe['epochs'],metrics=metrics,
               precision=metrics.get('metrics/precision(B)'),recall=metrics.get('metrics/recall(B)'),map50=metrics.get('metrics/mAP50(B)'))
    model.add_callback('on_train_batch_end',batch_end)
    model.add_callback('on_train_epoch_end',before_validation)
    model.add_callback('on_fit_epoch_end',epoch_end)
    notify(stage='checkpoint 재개' if mode=='resume' else '새 후보 학습',candidate=recipe['name'],remaining_training_seconds=remaining)
    try:
        if mode=='resume':
            checkpoint=torch.load(directory/'weights/last.pt',map_location='cpu',weights_only=False)
            if int(checkpoint.get('epoch',-1))<0:
                raise ValueError('완료 표식 없는 정리된 checkpoint입니다. 자동 재학습하지 않습니다.')
            del checkpoint
            model.train(resume=True,device=0,time=remaining/3600)
        else:
            model.train(data=str(TRAINING/'dataset.yaml'),project=str(TRAINING/'runs'),name=recipe['name'],exist_ok=True,
                        epochs=recipe['epochs'],patience=recipe['patience'],time=remaining/3600,imgsz=recipe['imgsz'],
                        batch=recipe['batch'],device=0,workers=4,cache=False,amp=True,seed=SEED,
                        optimizer='AdamW',lr0=recipe['lr0'],lrf=.05,cos_lr=True,warmup_epochs=2,
                        mosaic=.35,close_mosaic=8,scale=.35,translate=.1,fliplr=.5,degrees=5,
                        plots=False,save=True,deterministic=True)
    finally:
        atomic_json(elapsed_path,{'used_seconds':elapsed+time.monotonic()-start,'limit_seconds':config['candidate_hours']*3600})
    if not best.exists():raise ValueError('학습 완료 가중치가 없습니다.')
    atomic_json(directory/'phase_complete.json',{'best_sha256':sha256_file(best),'actual_epochs':actual_epochs,'completed':time.time()})
    del model
    torch.cuda.empty_cache()
    return best


def publish(final):
    selected=final['selected']
    for path,expected in selected['weights_sha256'].items():
        if sha256_file(local(path))!=expected:raise ValueError('선택 가중치가 최종 평가 계약과 다릅니다.')
    atomic_json(WORK/'selected_model.json',{'weights':selected['weights'][0],'ensemble':selected['weights'],
                'policy':selected['policy'],'imgsz':selected['imgsz'],'conf':selected['operating']['threshold'],
                'source':selected['name'],'target_met':final['target_met'],'test':final['tests']['historical_taco']})


def run(job,notify=lambda **kw:None,resume=False):
    if type(resume) is not bool:raise ValueError('재개는 명시적 bool이어야 합니다.')
    status={'job':job,'epoch':0,'epochs':60}
    def progress(**values):
        status.update(values,updated=time.time())
        atomic_json(TRAINING/'status.json',status)
        notify(**values)
    config=load(ROOT/'configs/training.json')
    verify_models()
    manifest=prepare(notify=progress)
    experiment={'manifest_sha256':sha256_file(TRAINING/'data_manifest.json'),'config_sha256':sha256_file(ROOT/'configs/training.json'),
                'pipeline_sha256':sha256_file(__file__),'preparation_sha256':sha256_file(ROOT/'prepare_dataset.py'),
                'protected_sources_sha256':sha256_file(ROOT/'configs/protected_sources.json')}
    freeze(TRAINING/'experiment_contract.json',experiment)
    if (TRAINING/'final.json').exists():
        final=load(TRAINING/'final.json')
        progress(stage='완료 결과·고정 계약 재사용',target_met=final['target_met'])
        publish(final)
        return final
    baseline=load(PREVIOUS_FINAL())['selected']['weights']
    weights=[('baseline',[portable(local(p)) for p in baseline])]
    for recipe in config['candidates']:
        weights.append((recipe['name'],[portable(train_candidate(recipe,manifest,config,progress,resume))]))
    verify_records(manifest['records'])
    verify_history(manifest)
    validation=[r for r in manifest['records'] if r['split']=='historical_val']
    plast_val=[r for r in manifest['records'] if r['split']=='val']
    comparison=[]
    for name,models in weights:
        for policy in config['validation_policies']:
            result=evaluate(models,validation,TRAINING/'evaluation'/name/policy/'taco_val',policy,progress,config)
            result['plastopol']=evaluate(models,plast_val,TRAINING/'evaluation'/name/policy/'plast_val',policy,progress,config,
                                        threshold=result['operating']['threshold'])
            result['name']=name+'_'+policy
            result['threshold_source']='TACO validation only; PlastOPol is secondary model/policy comparison'
            comparison.append(result)
            atomic_json(TRAINING/'validation_comparison.json',comparison)
    selected=choose_candidate(comparison)
    freeze(TRAINING/'selection.json',selected)
    freeze(TRAINING/'test_contract.json',{'experiment':experiment,'selected':selected,
           'protocol':'freeze model, tiles and threshold before tests; no test tuning; per-image prediction cache'})
    tests={}
    for split,name in [('historical_test','historical_taco'),('test','new_plastopol'),('external_test','source_heldout_uav')]:
        records=[r for r in manifest['records'] if r['split']==split]
        tests[name]=evaluate(selected['weights'],records,TRAINING/'evaluation/tests'/name,selected['policy'],progress,config,
                             threshold=selected['operating']['threshold'])
        atomic_json(TRAINING/'test_progress.json',tests)
    primary=tests['historical_taco']
    final={'selected':selected,'tests':tests,'test':primary,'target_met':target_met(primary),
           'target_definition':'P>=.90 and R>=.90 on previously evaluated historical TACO150 at IoU.5',
           'all_test_targets_met':all(target_met(result) for result in tests.values()),
           'limits':manifest['limits']+['custom AP is not official COCO API AP; JPEG normalization differs from round5',
                     'training budget: two candidates at most 6 hours each; download, preparation, evaluation are additional'],
           'manifest_sha256':experiment['manifest_sha256'],'counts':manifest['counts'],'finished':time.time()}
    atomic_json(TRAINING/'final.json',final)
    publish(final)
    progress(stage='학습·비교·고정 테스트 완료',target_met=final['target_met'],precision=primary['operating']['precision'],
             recall=primary['operating']['recall'],map50=primary['metrics']['AP50'])
    return final


def PREVIOUS_FINAL():
    return ROOT.parent/'5차/work/training/final.json'


def verify_models():
    for row in load(ROOT/'configs/protected_sources.json')['files']:
        if sha256_file(local(row['path']))!=row['sha256']:
            raise ValueError('보존 모델·이전 소스 해시가 다릅니다: '+row['path'])
