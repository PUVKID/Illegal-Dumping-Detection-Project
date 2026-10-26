"""Identical full-image / overlapping-tile inference for evaluation and the app."""
import numpy as np
import torch
from torchvision.ops import nms

def predict(models, image, policy='full', conf=.001, device=0, imgsz=1536):
    if not isinstance(models,(list,tuple)):models=[models]
    h,w=image.shape[:2];regions=[(0,0,w,h)]
    if policy in ('tiles2','tiles3'):
        steps=2 if policy=='tiles2' else 3;fraction=.6 if steps==2 else .4
        tw=round(w*fraction);th=round(h*fraction)
        regions += [(int(x),int(y),tw,th) for y in np.linspace(0,h-th,steps) for x in np.linspace(0,w-tw,steps)]
    elif policy!='full':raise ValueError('Unknown inference policy')
    boxes=[];scores=[]
    for model in models:
        for x,y,rw,rh in regions:
            result=model.predict(image[y:y+rh,x:x+rw],conf=conf,iou=.5,imgsz=imgsz if (rw,rh)==(w,h) else 1280,
                                 device=device,verbose=False,max_det=300)[0]
            b=result.boxes.xyxy.detach().cpu();c=result.boxes.conf.detach().cpu()
            if b.numel():
                keep=torch.ones(len(b),dtype=torch.bool)
                if (rw,rh)!=(w,h):
                    if x>0:keep &= b[:,0]>3
                    if y>0:keep &= b[:,1]>3
                    if x+rw<w:keep &= b[:,2]<rw-3
                    if y+rh<h:keep &= b[:,3]<rh-3
                b=b[keep];c=c[keep]
                b[:,[0,2]]+=x;b[:,[1,3]]+=y
                boxes.append(b);scores.append(c)
    if not boxes:return {'bboxes':torch.zeros((0,4)),'conf':torch.zeros(0),'cls':torch.zeros(0)}
    b=torch.cat(boxes);c=torch.cat(scores)
    keep=nms(b,c,.5)[:300]
    return {'bboxes':b[keep],'conf':c[keep],'cls':torch.zeros(len(keep))}

def operating_metrics(stats, threshold):
    chosen=stats['conf']>=threshold
    tp=int(stats['tp'][chosen,0].sum());fp=int(chosen.sum())-tp
    fn=len(stats['target_cls'])-tp
    p=tp/max(1,tp+fp);r=tp/max(1,tp+fn)
    return {'threshold':float(threshold),'precision':p,'recall':r,'f1':2*p*r/max(p+r,1e-12),'tp':tp,'fp':fp,'fn':fn,'iou':.5}

def choose_threshold(stats):
    # Validation only. Choose both precision and recall together, not one alone.
    candidates=[operating_metrics(stats,t) for t in np.arange(.05,.851,.01)]
    return max(candidates,key=lambda x:(min(x['precision'],x['recall']),x['f1']))

def evaluate(weights, split, policy, out, threshold=None, notify=lambda **k:None):
    import cv2,json
    from pathlib import Path
    from ultralytics import YOLO
    from ultralytics.models.yolo.detect import DetectionValidator
    from ultralytics.utils.metrics import ConfusionMatrix
    from data_pipeline import FULL as ORIGINAL
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    weights=[str(weights)] if isinstance(weights,(str,Path)) else list(weights)
    model=[YOLO(p) for p in weights];v=DetectionValidator(save_dir=out,args={'plots':True})
    v.metrics.names={0:'trash'}
    cm=ConfusionMatrix(names={0:'trash'})
    records=[]
    thresholds=[float(threshold)] if threshold is not None else list(np.round(np.arange(.01,.951,.01),2))
    counts={float(t):[0,0,0] for t in thresholds}
    paths=sorted((ORIGINAL/'images'/split).glob('*.jpg'))
    if len(paths)!=150:raise ValueError('Expected frozen 150-image split')
    for n,p in enumerate(paths):
        im=cv2.imread(str(p));H,W=im.shape[:2]
        label=ORIGINAL/'labels'/split/p.with_suffix('.txt').name
        rows=np.array([list(map(float,s.split())) for s in label.read_text().splitlines() if s.strip()],dtype=np.float32).reshape(-1,5)
        gt=np.zeros((len(rows),4),dtype=np.float32)
        if len(rows):
            gt[:,0]=(rows[:,1]-rows[:,3]/2)*W;gt[:,2]=(rows[:,1]+rows[:,3]/2)*W
            gt[:,1]=(rows[:,2]-rows[:,4]/2)*H;gt[:,3]=(rows[:,2]+rows[:,4]/2)*H
        batch={'bboxes':torch.from_numpy(gt),'cls':torch.zeros(len(rows))}
        pred=predict(model,im,policy=policy)
        # Rematch at each operating threshold: low-confidence detections must not
        # consume a ground-truth match from an accepted detection.
        for t in thresholds:
            accepted=pred['conf']>=t
            filtered={k:v[accepted] for k,v in pred.items()}
            tp=int(v._process_batch(filtered,batch)['tp'][:,0].sum())
            counts[t][0]+=tp;counts[t][1]+=int(accepted.sum())-tp;counts[t][2]+=len(rows)-tp
        stat={**v._process_batch(pred,batch),'target_cls':batch['cls'].numpy(),'target_img':np.unique(batch['cls'].numpy()),'conf':pred['conf'].numpy(),'pred_cls':pred['cls'].numpy(),'im_name':p.name}
        v.metrics.update_stats(stat)
        if threshold is not None:cm.process_batch(pred,batch,conf=threshold,iou_thres=.5)
        records.append({'image':p.name,'boxes':pred['bboxes'].tolist(),'conf':pred['conf'].tolist(),'truth':gt.tolist()})
        if n%10==0:notify(stage=f'{split} 평가 · {policy} · {n+1}/{len(paths)}')
    stats=v.metrics.process(save_dir=out,plot=True)
    operating=[]
    for t,(tp,fp,fn) in counts.items():
        p=tp/max(1,tp+fp);r=tp/max(1,tp+fn)
        operating.append({'threshold':float(t),'precision':p,'recall':r,'f1':2*p*r/max(p+r,1e-12),'tp':tp,'fp':fp,'fn':fn,'iou':.5})
    op=max(operating,key=lambda x:(min(x['precision'],x['recall']),x['f1']))
    (out/'operating_thresholds.json').write_text(json.dumps(operating,indent=2))
    result={'split':split,'images':len(paths),'weights':weights,'policy':policy,'imgsz':1536,'operating':op,'metrics':{k:float(x) for k,x in v.metrics.results_dict.items()},'threshold_source':'validation only','evaluator':'Ultralytics IoU matching and AP; original-resolution full-image coordinates; NMS IoU=.5; max_det=300'}
    (out/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    (out/'predictions.json').write_text(json.dumps(records))
    np.savez_compressed(out/'stats.npz',**stats)
    if threshold is not None:cm.plot(save_dir=out,normalize=False);cm.plot(save_dir=out,normalize=True)
    del model
    torch.cuda.empty_cache()
    return result
