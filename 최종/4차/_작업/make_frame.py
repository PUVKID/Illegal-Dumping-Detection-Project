import base64,json,subprocess
from pathlib import Path
code=r'''
import sys,json,io,base64,cv2,pathlib
from ultralytics import YOLO
from PIL import Image,ImageDraw,ImageFont,ImageFilter
r=pathlib.Path('/root/환경 PBL/trash_round3');sys.path.insert(0,str(r/'app'))
from inference import predict
s=json.loads((r/'app/selected_model.json').read_text())
v=sorted((r/'videos').glob('*.mp4'))[0];cap=cv2.VideoCapture(str(v));ok,frame=cap.read();cap.release();assert ok
pred=predict([YOLO(w) for w in s['ensemble']],frame,policy=s['policy'],conf=s['conf'],device=0)
person=YOLO(str(r/'pretrained/yolov8n.pt')).predict(frame,classes=[0],conf=.25,imgsz=960,device=0,verbose=False)[0].boxes.xyxy.cpu().tolist()
im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));draw=ImageDraw.Draw(im)
font=ImageFont.truetype(str(r/'app/fonts/NanumGothic-Bold.ttf'),26)
for b in person:
 x1,y1,x2,y2=map(int,b);crop=(max(0,x1),max(0,y1),min(im.width,x2),min(im.height,y1+int((y2-y1)*.4)))
 if crop[2]>crop[0] and crop[3]>crop[1]:im.paste(im.crop(crop).filter(ImageFilter.GaussianBlur(18)),crop)
draw=ImageDraw.Draw(im)
for b in person:draw.rectangle(list(map(int,b)),outline='#20B35A',width=4)
for b,c in zip(pred['bboxes'].tolist(),pred['conf'].tolist()):
 x1,y1,x2,y2=map(int,b);draw.rectangle((x1,y1,x2,y2),outline='#1882DF',width=4);draw.text((x1,max(4,y1-32)),f'쓰레기 {c:.2f}',font=font,fill='#1882DF',stroke_width=1,stroke_fill='white')
draw.rectangle((8,8,1220,54),fill='white');draw.text((18,15),'최종 앙상블 · 단일 프레임 기능 확인 · 투기 사건 판정 결과 아님',font=font,fill='#243448')
out=io.BytesIO();im.save(out,format='PNG')
print(json.dumps({'video':v.name,'time_sec':0,'trash':len(pred['bboxes']),'people':len(person),'test_metrics_recomputed':False,'image_base64':base64.b64encode(out.getvalue()).decode()}))
'''
p=subprocess.run(['docker','exec','-i','2026-2','python','-'],input=code.encode(),capture_output=True,check=True)
result=json.loads(p.stdout.decode().splitlines()[-1]);raw=result.pop('image_base64')
here=Path(__file__).resolve().parent/'자료'
(here/'최종모델_CCTV_프레임.png').write_bytes(base64.b64decode(raw))
(here/'프레임_확인.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
