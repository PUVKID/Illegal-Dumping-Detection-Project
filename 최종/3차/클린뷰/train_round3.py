"""New architectures, dataset expansion, focused refinement, validation-only selection."""
import csv,json,time,gc
from pathlib import Path
from data_pipeline import ROOT,FULL,prepare,verify_holdout,save,sha

def run(job,**_):
    from backend import update,APP
    from ultralytics import YOLO
    from inference import evaluate
    import torch
    notify=lambda **k:update(job,**k)
    report=prepare(notify)
    configs=[
        {'name':'yolo26x_mix','base':'yolo26x.pt','data':'mix','epochs':180,'patience':40,'batch':2,'imgsz':1536,'lr0':.001,'mosaic':.5,'scale':.4},
        {'name':'yolo26x_focus','base':'yolo26x_mix','data':'focus','epochs':60,'patience':20,'batch':2,'imgsz':1536,'lr0':.00012,'mosaic':.1,'scale':.2},
        {'name':'yolo26l_p2_mix','base':'yolo26l.pt','data':'mix','epochs':180,'patience':40,'batch':2,'imgsz':1536,'lr0':.001,'mosaic':.5,'scale':.4},
        {'name':'yolo26l_p2_focus','base':'yolo26l_p2_mix','data':'focus','epochs':60,'patience':20,'batch':2,'imgsz':1536,'lr0':.00012,'mosaic':.1,'scale':.2},
    ]
    plan=ROOT/'experiment_plan.json'
    if not plan.exists():save(plan,{'created':time.time(),'phases':configs,'data':report,'target':'precision >=.90 and recall >=.90 at IoU=.50','selection':'validation only; maximize min(P,R), F1, then AP50','test':'same photo identities and labels, original resolution; one final evaluation after selection','further_training_after_final_test':False})
    history=[];candidates=[]
    for index,cfg in enumerate(configs):
        dest=ROOT/'runs'/cfg['name'];marker=dest/'phase_complete.json';last=dest/'weights/last.pt'
        if marker.exists():
            info=json.loads(marker.read_text());history.append(info);candidates.append((cfg['name'],Path(info['best'])));continue
        notify(stage=cfg['name']+' 학습',candidate=index+1,candidates=len(configs),epoch=0,epochs=cfg['epochs'],progress=round(5+index*20,1))
        pretrained=ROOT/'pretrained'/cfg['base']
        if cfg['base'].endswith('.pt') and not pretrained.exists():
            YOLO(cfg['base']);downloaded=APP/cfg['base']
            if downloaded.exists():downloaded.rename(pretrained)
        attempts=[cfg['batch'],1] if cfg['batch']>1 else [1]
        for attempt,batch in enumerate(attempts):
            if last.exists():
                ckpt=torch.load(last,map_location='cpu',weights_only=False)
                if int(ckpt.get('epoch',-1))<0:
                    # The phase had completed and weights were stripped before its marker was written.
                    if (dest/'results.csv').exists() and (dest/'weights/best.pt').exists():break
                    raise RuntimeError('Stripped checkpoint without phase results')
                del ckpt
                model=YOLO(str(last));resume=True
            elif cfg['base'].endswith('.pt'):
                if 'p2' in cfg['name']:model=YOLO('yolo26l-p2.yaml').load(str(pretrained))
                else:model=YOLO(str(pretrained))
                resume=False
            else:model=YOLO(str(ROOT/'runs'/cfg['base']/'weights/best.pt'));resume=False
            def epoch_end(t):
                notify(stage=cfg['name']+' 학습',epoch=t.epoch+1,epochs=cfg['epochs'],progress=round(5+index*20+(t.epoch+1)/cfg['epochs']*20,1),metrics={k:float(v) for k,v in t.metrics.items()})
            model.add_callback('on_fit_epoch_end',epoch_end)
            try:
                if resume:model.train(resume=True,device=0,batch=batch,workers=4)
                else:model.train(data=str(ROOT/f'data_{cfg["data"]}.yaml'),project=str(ROOT/'runs'),name=cfg['name'],exist_ok=True,
                                 epochs=cfg['epochs'],patience=cfg['patience'],batch=batch,imgsz=cfg['imgsz'],lr0=cfg['lr0'],
                                 mosaic=cfg['mosaic'],scale=cfg['scale'],device=0,workers=4,amp=True,cache=False,
                                 seed=20261013,optimizer='AdamW',cos_lr=True,lrf=.05,close_mosaic=min(15,cfg['epochs']//3),
                                 warmup_epochs=4 if cfg['data']=='mix' else 1,fliplr=.5,degrees=5,translate=.1,
                                 plots=True,save=True)
                del model;gc.collect();torch.cuda.empty_cache();break
            except (torch.cuda.OutOfMemoryError,RuntimeError) as e:
                if 'out of memory' not in str(e).lower() or attempt+1==len(attempts):raise
                del model;gc.collect();torch.cuda.empty_cache()
                notify(stage='GPU 메모리 조정 · batch 1로 계속',memory_adjustment=True)
        best=dest/'weights/best.pt';assert best.is_file()
        epochs=len(list(csv.DictReader((dest/'results.csv').open())))
        info={'name':cfg['name'],'epochs':epochs,'best':str(best),'sha256':sha(best)}
        save(marker,info);history.append(info);candidates.append((cfg['name'],best))
        notify(completed_candidates=history,epoch=epochs)
        verify_holdout()
    validation=[]
    for name,weights in candidates:
        for policy in ('full','tiles2','tiles3'):
            out=ROOT/'evaluation'/f'val_{name}_{policy}'
            cached=out/'metrics.json'
            if cached.exists():result=json.loads(cached.read_text())
            else:result=evaluate([str(weights)],'val',policy,out,notify=notify)
            result['candidate']=name;validation.append(result);save(ROOT/'validation_comparison.json',validation)
    # Complementary architectures may recover different small objects. Still selected only on val.
    focused=[str(ROOT/'runs/yolo26x_focus/weights/best.pt'),str(ROOT/'runs/yolo26l_p2_focus/weights/best.pt')]
    for policy in ('full','tiles3'):
        out=ROOT/'evaluation'/f'val_ensemble_{policy}'
        cached=out/'metrics.json'
        result=json.loads(cached.read_text()) if cached.exists() else evaluate(focused,'val',policy,out,notify=notify)
        result['candidate']='ensemble';validation.append(result);save(ROOT/'validation_comparison.json',validation)
    chosen=max(validation,key=lambda r:(min(r['operating']['precision'],r['operating']['recall']),r['operating']['f1'],r['metrics']['metrics/mAP50(B)']))
    save(ROOT/'selection.json',chosen);notify(stage='선택 완료 · 최종 고정 테스트 평가',progress=94,selection=chosen)
    verify_holdout()
    cached=ROOT/'evaluation/test_final/metrics.json'
    # A completed saved test is reused after a packaging crash, never used to retune the selection.
    if cached.exists():
        test=json.loads(cached.read_text());assert test['weights']==chosen['weights'] and test['policy']==chosen['policy']
    else:test=evaluate(chosen['weights'],'test',chosen['policy'],cached.parent,threshold=chosen['operating']['threshold'],notify=notify)
    verify_holdout();target=test['operating']['precision']>=.9 and test['operating']['recall']>=.9
    final={'selected':chosen,'test':test,'history':history,'data':report,'target_met':target,'holdout_identity_unchanged':True,
           'best_sha256':{p:sha(Path(p)) for p in chosen['weights']},'finished':time.time(),'further_training':False}
    save(ROOT/'final.json',final)
    save(APP/'selected_model.json',{'weights':chosen['weights'][0],'ensemble':chosen['weights'],'policy':chosen['policy'],
                                  'conf':chosen['operating']['threshold'],'test':test,'target_met':target})
    notify(model=chosen['weights'][0],test_metrics=test['metrics'],operating_metrics=test['operating'],target_met=target,
           progress=100,stage='학습·평가 완료',epoch=history[-1]['epochs'],completed_candidates=history)

if __name__=='__main__':
    from backend import start
    print(json.dumps(start('improve',{}),ensure_ascii=False))
