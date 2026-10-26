"""Conservative stationary-object event candidates, not legal determinations."""
import math, csv, time, subprocess
from pathlib import Path
from backend import APP, ROOT, update, probe, allowed_video, save, read

def iou(a,b):
    x1=max(a[0],b[0]); y1=max(a[1],b[1]); x2=min(a[2],b[2]); y2=min(a[3],b[3])
    area=max(0,x2-x1)*max(0,y2-y1)
    return area/max(1,(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-area)

def near(a,b):
    # Person feet near the object's center, in screen coordinates.
    x=(a[0]+a[2])/2; y=(a[1]+a[3])/2
    px=(b[0]+b[2])/2; py=b[3]
    return math.hypot(x-px,y-py) < max(60,(b[3]-b[1])*.65)

class Events:
    def __init__(self, abandon=20, leave=5, baseline=10, gap=2):
        self.tracks=[]; self.events=[]; self.abandon=abandon; self.leave=leave
        self.baseline=baseline; self.gap=gap; self.next_id=1

    def step(self, t, boxes, people):
        available={i for i,tr in enumerate(self.tracks) if tr['baseline'] or t-tr['last']<=self.gap}
        visible=[]
        for box in boxes:
            scores=[(iou(box,self.tracks[i]['box']),i) for i in available]
            best=max(scores,default=(0,-1))
            if best[0]>.25:
                idx=best[1]; available.remove(idx); tr=self.tracks[idx]
                # Reset dwell when the object moves away from its stationary anchor.
                if iou(box,tr['anchor'])<.55:
                    tr['stationary']=t; tr['anchor']=box[:]
                tr.update(box=box[:],last=t,hits=tr['hits']+1)
            else:
                tr={'id':self.next_id,'box':box[:],'anchor':box[:],'first':t,'last':t,
                    'stationary':t,'hits':1,'baseline':False,'person_last':None,'emitted':False}
                self.next_id+=1; self.tracks.append(tr)
            # Baseline requires persistent stationary observations in the initial interval.
            if t<=self.baseline and tr['hits']>=3 and t-tr['stationary']>=min(2,self.baseline/2):
                tr['baseline']=True
            if any(near(box,p) for p in people): tr['person_last']=t
            if (not tr['baseline'] and not tr['emitted'] and tr['hits']>=3
                and t>self.baseline and t-tr['stationary']>=self.abandon
                and tr['person_last'] is not None and t-tr['person_last']>=self.leave):
                tr['emitted']=True
                self.events.append({'track_id':tr['id'],'time_sec':round(t,3),
                                    'first_seen_sec':round(tr['first'],3),
                                    'reason':'새 정지 물체 지속 + 주변 사람 이탈 (투기 의심 후보)'})
            visible.append(tr)
        return visible

def detect(job, path, model, seconds=120, abandon=20, leave=5, conf=.25,
           baseline=10, roi=None, device=0, **_):
    import cv2
    import imageio_ffmpeg
    from PIL import Image, ImageDraw, ImageFont
    from ultralytics import YOLO
    p=allowed_video(path); meta=probe(str(p))
    weights=Path(model).resolve()
    if not any(weights.is_relative_to(r.resolve()) for r in [ROOT/'runs']) or not weights.is_file() or weights.suffix!='.pt':
        raise ValueError('학습된 best.pt를 선택하세요.')
    seconds=float(seconds); abandon=float(abandon); leave=float(leave); conf=float(conf); baseline=float(baseline)
    if not(0<=seconds<=86400 and 1<=abandon<=600 and 0<=leave<=120 and .01<=conf<=1 and 0<=baseline<=60):
        raise ValueError('탐지 설정 범위 오류')
    if roi is not None:
        if len(roi)<3 or any(len(v)!=2 or not all(isinstance(x,(int,float)) and math.isfinite(x) and 0<=x<=1 for x in v) for v in roi):
            raise ValueError('구역은 0~1 좌표의 다각형이어야 합니다.')
    from inference import predict
    selection=read(APP/'selected_model.json',{})
    policy=selection.get('policy','full') if selection.get('weights')==str(weights) else 'full'
    ensemble=selection.get('ensemble',[str(weights)]) if selection.get('weights')==str(weights) else [str(weights)]
    trash=[YOLO(p) for p in ensemble]; person=YOLO(str(APP/'yolov8n.pt') if (APP/'yolov8n.pt').exists() else 'yolov8n.pt')
    if any(len(m.names)!=1 or m.names[0]!='trash' for m in trash): raise ValueError('1-class trash 학습 모델이 아닙니다.')
    out=APP/'results'/job; out.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(p)); w=meta['width']; h=meta['height']; fps=meta['fps']
    total=meta['frames'] if seconds==0 else min(meta['frames'],int(seconds*fps))
    if total<=0: raise ValueError('처리할 프레임이 없습니다.')
    raw=out/'annotated.avi'; writer=cv2.VideoWriter(str(raw),cv2.VideoWriter_fourcc(*'MJPG'),fps,(w,h))
    if not writer.isOpened(): cap.release(); raise ValueError('결과 영상 인코더를 열 수 없습니다.')
    engine=Events(abandon,leave,baseline,max(2,2/fps)); n=0
    font=ImageFont.truetype(str(APP/'fonts/NanumGothic-Bold.ttf'),max(18,round(w/80)))
    import numpy as np
    polygon=None if roi is None else np.array([[x*w,y*h] for x,y in roi],dtype=np.int32)
    update(job,stage='영상 탐지',progress=0)
    try:
        with (out/'frames.csv').open('w',newline='',encoding='utf-8-sig') as f:
            csvout=csv.writer(f); csvout.writerow(['frame','time_sec','people','trash','new_candidates'])
            while n<total:
                ok,frame=cap.read()
                if not ok: raise ValueError(f'{n}/{total} 프레임에서 영상 디코딩이 중단됐습니다. 결과를 완료 처리하지 않습니다.')
                t=n/fps
                persons=person.predict(frame,classes=[0],conf=.25,imgsz=960,device=device,verbose=False)[0].boxes.xyxy.cpu().tolist()
                prediction=predict(trash,frame,policy=policy,conf=conf,device=device)
                boxes=prediction['bboxes'].tolist()
                if polygon is not None:
                    boxes=[b for b in boxes if cv2.pointPolygonTest(polygon,((b[0]+b[2])/2,b[3]),False)>=0]
                    cv2.polylines(frame,[polygon],True,(255,180,0),2)
                visible=engine.step(t,boxes,persons)
                for b in persons:
                    x1,y1,x2,y2=map(int,b); cv2.rectangle(frame,(x1,y1),(x2,y2),(60,200,70),2)
                captions=[]
                for tr in visible:
                    x1,y1,x2,y2=map(int,tr['box'])
                    color=(0,220,255) if tr['baseline'] else ((30,30,240) if tr['emitted'] else (255,140,40))
                    cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
                    label=f"#{tr['id']} "+('기존 물체' if tr['baseline'] else '투기 의심' if tr['emitted'] else '쓰레기')
                    captions.append(((x1,max(0,y1-30)),label,tuple(reversed(color))))
                pil=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));draw=ImageDraw.Draw(pil)
                for xy,label,color in captions:draw.text(xy,label,font=font,fill=color,stroke_width=1,stroke_fill=(15,25,35))
                draw.text((20,16),f'{t:.1f}초 | 의심 장면 {len(engine.events)}건',font=font,fill='white',stroke_width=1,stroke_fill=(15,25,35))
                frame=cv2.cvtColor(np.asarray(pil),cv2.COLOR_RGB2BGR)
                writer.write(frame); csvout.writerow([n,round(t,3),len(persons),len(visible),len(engine.events)]); n+=1
                if n%10==0: update(job,progress=round(n/total*90,1),frame=n,total=total)
    finally: cap.release(); writer.release()
    update(job,stage='브라우저용 MP4 변환',progress=93)
    result=out/'result.mp4'
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-i',str(raw),'-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(result)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    raw.unlink()
    summary={'video':str(p),'model':str(weights),'ensemble':ensemble,'frames':n,'events':engine.events,'settings':{'policy':policy,'conf':conf,'abandon':abandon,'leave':leave,'baseline':baseline,'roi':roi},
             'note':'투기 의심 후보입니다. 사람이 물체를 버리는 동작이나 위법 여부를 확정하지 않습니다. 가림·이동·작은 물체에서 누락/오탐 가능.'}
    save(out/'summary.json',summary)
    update(job,result=str(result),csv=str(out/'frames.csv'),summary=str(out/'summary.json'),events=engine.events,progress=100)
