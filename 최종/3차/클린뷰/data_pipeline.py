"""Round 3: fixed photo identities, original-resolution inputs, new labelled data."""
import json,hashlib,random,io,struct,zlib,time,os
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import cv2,numpy as np,requests,yaml,zipfile

ROOT=Path('/root/환경 PBL/trash_round3')
REF=ROOT/'data/reference'
FULL=ROOT/'data/full'
SEED=20261013

def save(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2));tmp.replace(p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def phash(im):
    d=cv2.dct(cv2.resize(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),(32,32)).astype(np.float32))[:8,:8].ravel()[1:]
    return d>np.median(d)
def verify_holdout():
    frozen=json.loads((ROOT/'reference_holdout_sha256.json').read_text())
    assert all(sha(REF/name)==value for name,value in frozen.items()),'Held-out reference changed'
    if (ROOT/'original_holdout_sha256.json').exists():
        originals=json.loads((ROOT/'original_holdout_sha256.json').read_text())
        assert all(sha(ROOT/name)==value for name,value in originals.items()),'Original held-out input changed'

class RemoteZipFile:
    """Read the central directory through HTTP Range; do not download the 13GB zip."""
    def __init__(self,url,size):self.url=url;self.size=size;self.pos=0
    def seekable(self):return True
    def tell(self):return self.pos
    def seek(self,offset,whence=0):
        self.pos=offset if whence==0 else self.pos+offset if whence==1 else self.size+offset
        return self.pos
    def read(self,n=-1):
        n=self.size-self.pos if n<0 else min(n,self.size-self.pos)
        if n<=0:return b''
        data=range_bytes(self.url,self.pos,self.pos+n-1);self.pos+=len(data);return data

def range_bytes(url,start,end):
    r=requests.get(url,headers={'Range':f'bytes={start}-{end}'},timeout=(20,70),stream=True)
    try:
        if r.status_code!=206:raise RuntimeError('Server did not honor HTTP Range')
        if not r.headers.get('Content-Range','').startswith(f'bytes {start}-'):raise RuntimeError('Wrong byte range')
        data=r.content
        if len(data)!=end-start+1:raise RuntimeError('Incomplete byte range')
        return data
    finally:r.close()

def zip_member(url,size,info):
    b=range_bytes(url,info.header_offset,min(size-1,info.header_offset+info.compress_size+4095))
    if b[:4]!=b'PK\x03\x04':raise RuntimeError('Invalid ZIP local header')
    name_len,extra_len=struct.unpack_from('<HH',b,26);offset=30+name_len+extra_len
    payload=b[offset:offset+info.compress_size]
    if len(payload)!=info.compress_size:payload=range_bytes(url,info.header_offset+offset,info.header_offset+offset+info.compress_size-1)
    data=zlib.decompress(payload,-15) if info.compress_type==8 else payload if info.compress_type==0 else None
    if data is None or zlib.crc32(data)&0xffffffff!=info.CRC:raise RuntimeError('ZIP CRC mismatch')
    return data

def label_rows(p):
    return [list(map(float,s.split())) for s in p.read_text().splitlines() if s.strip()]

def prepare(notify=lambda **k:None):
    marker=ROOT/'data_report.json'
    if marker.exists():verify_holdout();return json.loads(marker.read_text())
    verify_holdout();(ROOT/'sources').mkdir(exist_ok=True)
    manifests=json.loads((ROOT/'base_manifest.json').read_text())
    train=[];hashes=[];image_records=[];originals={}
    # Symbolic images and hardlinked labels reuse the originals without duplicating pixels.
    for item in manifests:
        split=item['split'];src=Path(item['source']);oldim=Path(item['image'])
        out=FULL/'images'/split/oldim.name;out.parent.mkdir(parents=True,exist_ok=True)
        if not out.exists():out.symlink_to(src)
        label=FULL/'labels'/split/oldim.with_suffix('.txt').name;label.parent.mkdir(parents=True,exist_ok=True)
        if not label.exists():label.hardlink_to(REF/'labels'/split/label.name)
        im=cv2.imread(str(src));assert im is not None
        hashes.append(phash(im))
        if split=='train':train.append(str(out))
        else:originals[str(src.relative_to(ROOT))]=sha(src)
        image_records.append({'image':str(out),'source':str(src),'split':split,'original_sha256':sha(src)})
    save(ROOT/'original_holdout_sha256.json',originals)
    save(ROOT/'sources/original_resolution_manifest.json',image_records)
    for p in sorted((ROOT/'data/salsa/images/train').glob('*')):
        if p.suffix.lower() not in ('.jpg','.jpeg','.png'):continue
        im=cv2.imread(str(p));assert im is not None;hashes.append(phash(im));train.append(str(p))
    hashes=np.array(hashes)
    external=[];rejected=[];errors=[]
    dest=ROOT/'data/additional';(dest/'images/train').mkdir(parents=True,exist_ok=True);(dest/'labels/train').mkdir(parents=True,exist_ok=True)
    def commit(info,p,h,boxes,source,url,license):
        nonlocal hashes
        if h is None:return False
        if np.count_nonzero(hashes!=h,axis=1).min()<=6:
            rejected.append({'source':source,'image':info,'reason':'pHash near duplicate'});p.unlink(missing_ok=True);return False
        lines=[]
        W,H=info['width'],info['height']
        for x,y,w,hb in boxes:
            x1=max(0.,float(x));y1=max(0.,float(y));x2=min(float(W),float(x+w));y2=min(float(H),float(y+hb))
            if x2<=x1 or y2<=y1:continue
            lines.append(f'0 {(x1+x2)/2/W:.8f} {(y1+y2)/2/H:.8f} {(x2-x1)/W:.8f} {(y2-y1)/H:.8f}')
        if not lines:
            p.unlink(missing_ok=True);return False
        (dest/'labels/train'/p.with_suffix('.txt').name).write_text('\n'.join(lines)+'\n')
        hashes=np.vstack([hashes,h]);train.append(str(p));external.append({'source':source,'image':str(p),'url':url,'license':license,'sha256':sha(p),'boxes':len(lines)})
        return True
    def decode_save(data,p,info):
        im=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
        if im is None:raise ValueError('Cannot decode image')
        if im.shape[:2]!=(info['height'],info['width']):raise ValueError('Annotation/image dimensions differ')
        h=phash(im);scale=min(1,2048/max(im.shape[:2]))
        if scale<1:im=cv2.resize(im,None,fx=scale,fy=scale,interpolation=cv2.INTER_AREA)
        if not cv2.imwrite(str(p),im,[cv2.IMWRITE_JPEG_QUALITY,95]):raise IOError(str(p))
        return h
    # Additional TACO photographs, excluding URL identities from all original splits.
    notify(stage='추가 TACO 라벨·이미지 수집')
    ap=ROOT/'sources/TACO_unofficial.json'
    if not ap.exists():r=requests.get('https://raw.githubusercontent.com/pedropro/TACO/master/data/annotations_unofficial.json',timeout=60);r.raise_for_status();save(ap,r.json())
    ann=json.loads(ap.read_text());byid=defaultdict(list)
    for a in ann['annotations']:byid[a['image_id']].append(a['bbox'])
    original_ann=json.loads((ROOT/'data/taco/data/annotations.json').read_text())
    urls={i.get('flickr_url') for i in original_ann['images']}
    candidates=[i for i in ann['images'] if i.get('flickr_url') and i['flickr_url'] not in urls and byid[i['id']]]
    random.Random(SEED).shuffle(candidates)
    def fetch_taco(i):
        p=dest/'images/train'/f'unofficial_{i["id"]}.jpg'
        try:
            for retry in range(3):
                try:r=requests.get(i['flickr_url'],timeout=(15,40));r.raise_for_status();h=decode_save(r.content,p,i);return i,p,h,None
                except Exception:
                    if retry==2:raise
                    time.sleep(retry+1)
        except Exception as e:return i,p,None,str(e)
    taco_added=0
    with ThreadPoolExecutor(max_workers=8) as pool:
        # Consume in stable shuffled order; only paths/signatures remain in memory.
        for n,(i,p,h,error) in enumerate(pool.map(fetch_taco,candidates)):
            if error:errors.append({'source':'TACO unofficial','id':i['id'],'error':error});continue
            if commit(i,p,h,byid[i['id']],'TACO unofficial',i['flickr_url'],i.get('license')):taco_added+=1
            if n%100==0:notify(stage=f'추가 TACO 수집 · {n+1}/{len(candidates)}',additional_taco=taco_added)
    # pLitterStreet: manually annotated outdoor litter; retain object labels, exclude trash-bin category.
    notify(stage='도로변 쓰레기 데이터 수집 · pLitterStreet')
    zp=ROOT/'sources/pLitter_annotations.zip'
    if not zp.exists():
        r=requests.get('https://zenodo.org/api/records/8288500/files/annotations.zip/content',timeout=(20,120));r.raise_for_status();zp.write_bytes(r.content)
    z=zipfile.ZipFile(zp);name=next(n for n in z.namelist() if n.endswith('10_class_splits/annotations_all.json'))
    street=json.loads(z.read(name));save(ROOT/'sources/pLitter_annotations.json',street)
    byid=defaultdict(list)
    for a in street['annotations']:
        if a['category_id']!=4:byid[a['image_id']].append(a['bbox'])
    infos=[i for i in street['images'] if byid[i['id']]];random.Random(SEED).shuffle(infos)
    url='https://zenodo.org/api/records/8288500/files/images.zip/content';size=13728630001
    remote=zipfile.ZipFile(RemoteZipFile(url,size));members=defaultdict(list)
    for m in remote.infolist():
        if not m.is_dir():members[Path(m.filename).name].append(m)
    choices=[]
    for i in infos:
        found=members.get(i['file_name'],[])
        exact=[m for m in found if m.filename.endswith(i.get('path','').removeprefix('/datasets/'))]
        if len(exact)==1:choices.append((i,exact[0]))
        elif len(found)==1:choices.append((i,found[0]))
        if len(choices)>=2000:break
    if len(choices)<500:raise RuntimeError('pLitter archive/image mapping incomplete')
    def fetch_street(pair):
        i,m=pair;p=dest/'images/train'/f'plitter_{i["id"]}.jpg'
        try:
            for retry in range(3):
                try:h=decode_save(zip_member(url,size,m),p,i);return i,p,h,None
                except Exception:
                    if retry==2:raise
                    time.sleep(retry+1)
        except Exception as e:return i,p,None,str(e)
    street_added=0
    with ThreadPoolExecutor(max_workers=8) as pool:
        for n,(i,p,h,error) in enumerate(pool.map(fetch_street,choices)):
            if error:errors.append({'source':'pLitterStreet','id':i['id'],'error':error});continue
            if commit(i,p,h,byid[i['id']],'pLitterStreet',url,'CC BY 4.0'):street_added+=1
            if n%100==0:notify(stage=f'pLitterStreet 수집 · {n+1}/{len(choices)}',additional_street=street_added)
    save(ROOT/'sources/additional_manifest.json',external);save(ROOT/'sources/excluded.json',rejected);save(ROOT/'sources/download_errors.json',errors)
    save(ROOT/'sources/attribution.json',{'TACO':'https://github.com/pedropro/TACO','TACO_unofficial':'https://github.com/pedropro/TACO/blob/master/data/annotations_unofficial.json','pLitterStreet':'https://zenodo.org/records/8288500','pLitterStreet_license':'CC BY 4.0','SALSA':'https://github.com/alinacherkas/salsa','license_note':'TACO per-image license fields are recorded as declared, including unknown; no blanket license claim.'})
    if taco_added<1000 or street_added<500:raise RuntimeError(f'Insufficient additional data: TACO={taco_added}, street={street_added}; inspect download_errors.json')
    notify(stage='작은 물체 중심 확대 데이터 생성')
    zoom=ROOT/'data/zoom';(zoom/'images/train').mkdir(parents=True,exist_ok=True);(zoom/'labels/train').mkdir(parents=True,exist_ok=True)
    zooms=[];rng=random.Random(SEED)
    # Adaptive object-centered crops from training photographs only.
    for n,path in enumerate(list(train)):
        p=Path(path);label=Path(str(p).replace('/images/','/labels/')).with_suffix('.txt')
        rows=label_rows(label)
        im=cv2.imread(str(p));H,W=im.shape[:2]
        small=sorted([r for r in rows if r[3]*W*r[4]*H*(1280/max(H,W))**2<48**2],key=lambda r:r[3]*r[4])
        for k,r in enumerate(small[:2 if n<1200 else 1]):
            _,cx,cy,bw,bh=r
            side=int(min(max(H,W),max(320,min(bw*W,bh*H)*12,max(bw*W,bh*H)*2.5)))
            cw=min(W,side);ch=min(H,side)
            ox=int(max(0,min(W-cw,cx*W-cw*(.5+rng.uniform(-.2,.2)))))
            oy=int(max(0,min(H-ch,cy*H-ch*(.5+rng.uniform(-.2,.2)))))
            lines=[]
            for _,x,y,ww,hh in rows:
                x1=max(0,(x-ww/2)*W-ox);y1=max(0,(y-hh/2)*H-oy);x2=min(cw,(x+ww/2)*W-ox);y2=min(ch,(y+hh/2)*H-oy)
                if x2-x1>=1 and y2-y1>=1:lines.append(f'0 {(x1+x2)/2/cw:.8f} {(y1+y2)/2/ch:.8f} {(x2-x1)/cw:.8f} {(y2-y1)/ch:.8f}')
            out=zoom/'images/train'/f'{p.stem}_zoom{k}.jpg'
            cv2.imwrite(str(out),im[oy:oy+ch,ox:ox+cw],[cv2.IMWRITE_JPEG_QUALITY,95])
            (zoom/'labels/train'/out.with_suffix('.txt').name).write_text('\n'.join(lines)+'\n')
            zooms.append(str(out))
        if n%200==0:notify(stage=f'작은 물체 확대 · {n+1}/{len(train)}',zoom_images=len(zooms))
    train+=zooms
    # Keep an original-resolution holdout and its unchanged old reference bytes.
    verify_holdout()
    (ROOT/'train_mix.txt').write_text('\n'.join(train)+'\n')
    focus=[p for p in train if 'plitter_' not in Path(p).name]
    (ROOT/'train_focus.txt').write_text('\n'.join(focus)+'\n')
    for name in ('mix','focus'):
        (ROOT/f'data_{name}.yaml').write_text(yaml.safe_dump({'path':str(ROOT),'train':str(ROOT/f'train_{name}.txt'),'val':str(FULL/'images/val'),'test':str(FULL/'images/test'),'names':{0:'trash'}},allow_unicode=True))
    report={'original_train':1200,'salsa_train':1243,'additional_taco':taco_added,'additional_street':street_added,'zoom_images':len(zooms),'train_mix':len(train),'train_focus':len(focus),'val':150,'test':150,'held_out_photo_identity_unchanged':True,'old_reference_bytes_unchanged':True,'evaluation_protocol':'Same held-out photographs and labels, restored original resolution; validation chooses model, tiles and operating threshold. Do not directly compare pixel preprocessing to round 2.','download_failures':len(errors),'duplicates_excluded':len(rejected),'seed':SEED}
    save(marker,report);return report

if __name__=='__main__':print(prepare(lambda **k:print(k,flush=True)))
