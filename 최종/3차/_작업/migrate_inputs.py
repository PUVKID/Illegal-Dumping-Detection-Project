"""Move reusable inputs; verify identity before removing obsolete experiment trees."""
import hashlib,json,os,shutil
from pathlib import Path

BASE=Path('/root/환경 PBL')
ROOT=BASE/'trash_round3'
ROOT.mkdir(exist_ok=True)
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'pretrained').mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=BASE/'trash_new_dataset_experiment/verified_trash_v1'
freeze={str(p.relative_to(old)):sha(p) for split in ('val','test') for folder in ('images','labels') for p in sorted((old/folder/split).glob('*')) if p.is_file()}
pairs=[(BASE/'trash_new_dataset_experiment/TACO',ROOT/'data/taco'),(old,ROOT/'data/reference'),(BASE/'trash_round2/external',ROOT/'data/salsa'),(BASE/'Test Video',ROOT/'videos')]
for source,dest in pairs:
    assert source.is_relative_to(BASE) and dest.is_relative_to(ROOT)
    if dest.exists():raise RuntimeError(f'Target already exists: {dest}')
    source.rename(dest)
ref=ROOT/'data/reference'
assert all(sha(ref/name)==digest for name,digest in freeze.items())
(ROOT/'reference_holdout_sha256.json').write_text(json.dumps(freeze,indent=2))
manifest=json.loads((ref/'manifest.json').read_text())
for item in manifest:
    item['source']=str(ROOT/'data/taco/data'/item['source'].split('/TACO/data/',1)[1])
    item['image']=str(ref/'images'/item['split']/Path(item['image']).name)
    assert Path(item['source']).is_file() and Path(item['image']).is_file()
(ROOT/'base_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(ROOT/'sources').mkdir(exist_ok=True)
for name in ('annotations.json','annotations_unofficial.json'):
    p=ROOT/'data/taco/data'/name
    if p.exists():shutil.copy2(p,ROOT/'sources'/('TACO_'+name))
person=BASE/'trash_detector_app/yolov8n.pt'
if person.is_file():person.rename(ROOT/'pretrained/yolov8n.pt')
print(json.dumps({'moved':len(pairs),'manifest_images':len(manifest),'held_out_files':len(freeze),'holdout_unchanged':True,'videos':len(list((ROOT/'videos').glob('*.mp4')))},ensure_ascii=False))
