import sys,json,zipfile,requests,cv2,numpy as np
from pathlib import Path
sys.path.insert(0,'/root/환경 PBL/trash_round3/app')
from data_pipeline import ROOT,RemoteZipFile,zip_member,save
p=ROOT/'sources/pLitter_annotations.zip'
if not p.exists():
    r=requests.get('https://zenodo.org/api/records/8288500/files/annotations.zip/content',timeout=120);r.raise_for_status();p.write_bytes(r.content)
z=zipfile.ZipFile(p);name=next(n for n in z.namelist() if n.endswith('10_class_splits/annotations_all.json'));a=json.loads(z.read(name))
ids={x['image_id'] for x in a['annotations'] if x['category_id']!=4}
url='https://zenodo.org/api/records/8288500/files/images.zip/content';size=13728630001
remote=zipfile.ZipFile(RemoteZipFile(url,size));members={m.filename:m for m in remote.infolist()}
selected=None
for i in a['images']:
    if i['id'] not in ids:continue
    found=[m for n,m in members.items() if n.endswith(i.get('path','').removeprefix('/datasets/'))]
    if not found:found=[m for n,m in members.items() if Path(n).name==i['file_name']]
    if len(found)==1:selected=(i,found[0]);break
assert selected is not None
i,member=selected;raw=zip_member(url,size,member);im=cv2.imdecode(np.frombuffer(raw,np.uint8),cv2.IMREAD_COLOR)
assert im.shape[:2]==(i['height'],i['width'])
result={'archive_members':len(members),'metadata_images':len(a['images']),'sample_id':i['id'],'decoded_shape':list(im.shape),'CRC':'passed','range_extraction':'passed','archive_bytes':size,'full_zip_downloaded':False}
save(ROOT/'external_archive_check.json',result);print(result)
