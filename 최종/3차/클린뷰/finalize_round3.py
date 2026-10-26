"""Windows incremental archive; no second copy of the original 7 GB project."""
import argparse,hashlib,json,os,shutil,subprocess,tarfile,tempfile,time
from pathlib import Path
SOURCE=Path(__file__).resolve().parent
DESKTOP=SOURCE.parents[1]
DEST=DESKTOP/'3차'
REMOTE='/root/환경 PBL/trash_round3/app'
ROOT='/root/환경 PBL/trash_round3'
JOB='20261013_060956_6d373b'
FLAGS=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0

def docker(*args):
    p=subprocess.run(['docker',*args],capture_output=True,creationflags=FLAGS)
    if p.returncode:raise RuntimeError(p.stderr.decode('utf-8',errors='replace'))
    return p.stdout

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while chunk:=f.read(1024*1024):h.update(chunk)
    return h.hexdigest()

def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')

class Archive:
    def __init__(self):
        self.sizes={};self.hashes={};self.records=[]
        for parent in (DEST,):
            if parent.exists():
                for p in parent.rglob('*'):
                    if p.is_file() and '_작업' not in p.parts:self.sizes.setdefault(p.stat().st_size,[]).append(p)
    def put(self,temp,dest,relative,expected=None):
        dest.parent.mkdir(parents=True,exist_ok=True)
        digest=sha(temp)
        if expected and expected!=digest:raise ValueError('Archive hash mismatch: '+relative)
        if dest.exists() and sha(dest)==digest:
            temp.unlink();method='unchanged'
        else:
            identical=None
            for p in self.sizes.get(temp.stat().st_size,[]):
                if p==dest or not p.exists():continue
                if str(p) not in self.hashes:self.hashes[str(p)]=sha(p)
                old=self.hashes[str(p)]
                if old==digest:identical=p;break
            if identical:
                # Link via temporary sibling, then replace only this managed archive file.
                link=dest.with_name(dest.name+'.linktmp')
                if link.exists():link.unlink()
                try:os.link(identical,link);os.replace(link,dest);temp.unlink();method='hardlink'
                except OSError:
                    if link.exists():link.unlink()
                    os.replace(temp,dest);method='copy'
            else:os.replace(temp,dest);method='copy'
            self.sizes.setdefault(dest.stat().st_size,[]).append(dest);self.hashes[str(dest)]=digest
        self.records.append({'file':relative,'bytes':dest.stat().st_size,'sha256':digest,'method':method})
    def local(self,source,dest):
        if source.resolve()==dest.resolve():
            for p in source.rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts:
                    self.records.append({'file':str(p.relative_to(DEST)),'bytes':p.stat().st_size,'sha256':sha(p),'method':'canonical'})
            return
        for p in source.rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts:continue
            target=dest/p.relative_to(source)
            target.parent.mkdir(parents=True,exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as f:temp=Path(f.name)
            shutil.copyfile(p,temp);self.put(temp,target,str(target.relative_to(DEST)))
    def remote(self,root,dest,subdirs=None,exclude=()):
        # Serialize regular files only; links refer to existing original data and are recorded.
        code="""import sys,tarfile,json
from pathlib import Path
r=Path(sys.argv[1]); sub=json.loads(sys.argv[2]); exclude=json.loads(sys.argv[3])
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as t:
 for p in sorted(r.rglob('*')):
  rel=p.relative_to(r)
  if '__pycache__' in rel.parts or any(x in rel.parts for x in exclude):continue
  if sub and rel.parts[0] not in sub:continue
  if p.is_file() or p.is_symlink():t.add(p,arcname=str(rel),recursive=False)
"""
        p=subprocess.Popen(['docker','exec','2026-2','python','-c',code,root,json.dumps(subdirs),json.dumps(exclude)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=FLAGS)
        count=0;links=[]
        with tarfile.open(fileobj=p.stdout,mode='r|') as tar:
            for member in tar:
                target=(dest/member.name).resolve()
                if not target.is_relative_to(dest.resolve()):raise ValueError('Unsafe archive path')
                if member.issym() or member.islnk():links.append({'path':member.name,'source':member.linkname,'hardlink':member.islnk()});continue
                if not member.isfile():continue
                target.parent.mkdir(parents=True,exist_ok=True)
                with tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as f:
                    temp=Path(f.name);shutil.copyfileobj(tar.extractfile(member),f)
                if temp.stat().st_size!=member.size:raise ValueError('Incomplete copy')
                self.put(temp,target,str(target.relative_to(DEST)))
                count+=1
                if count%500==0:print(f'{root}: verified {count} files',flush=True)
        error=p.stderr.read().decode('utf-8',errors='replace')
        if p.wait()!=0:raise RuntimeError(error)
        if links:
            for link in links:
                src=Path(link['source'])
                if dest==DEST/'데이터':
                    relative=str(src).removeprefix(ROOT+'/data/') if str(src).startswith(ROOT+'/data/') else str(src) if link.get('hardlink') and not src.is_absolute() else None
                    if relative is None:continue
                    target=dest/link['path'];original=(dest/relative).resolve()
                    assert original.is_relative_to(dest.resolve())
                    if original.is_file() and not target.exists():
                        target.parent.mkdir(parents=True,exist_ok=True);os.link(original,target)
            write(dest/'원본_연결.json',links)
        print(f'{root}: {count} files saved',flush=True)

def main():
    args=argparse.ArgumentParser();args.add_argument('--prepare',action='store_true');a=args.parse_args()
    assert DEST.resolve()==SOURCE.parent.resolve() and DEST.name=='3차'
    DEST.mkdir(exist_ok=True)
    state=json.loads(docker('exec','2026-2','cat',REMOTE+'/state/jobs/'+JOB+'.json'))
    if not a.prepare:
        if state.get('state')!='complete' or not state.get('test_metrics'):raise RuntimeError('Training/test not complete')
        for name in ('make_report.py','data_pipeline.py'):
            docker('cp',str(SOURCE/name),'2026-2:'+REMOTE+'/'+name)
        docker('cp',str(SOURCE/'fonts'),'2026-2:'+REMOTE+'/')
        print(docker('exec','2026-2','python',REMOTE+'/make_report.py').decode('utf-8'),flush=True)
    archive=Archive();archive.local(SOURCE,DEST/'클린뷰')
    for folder,target in [('data','데이터'),('sources','출처'),('videos','테스트영상'),('pretrained','사전학습가중치')]:
        archive.remote(ROOT+'/'+folder,DEST/target)
    if not a.prepare:
        archive.remote(ROOT+'/runs',DEST/'실험기록')
        archive.remote(ROOT+'/evaluation',DEST/'평가원자료')
    archive.remote(REMOTE,DEST/'실행기록',subdirs=['state','results','uploads','selected_model.json'])
    # Small top-level configuration/manifest files are retained once in this round.
    names=json.loads(docker('exec','2026-2','python','-c',"import json;from pathlib import Path;print(json.dumps([p.name for p in Path('/root/환경 PBL/trash_round3').iterdir() if p.is_file()]))"))
    for name in names:
        target=DEST/'실험설정'/name;target.parent.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as f:temp=Path(f.name)
        temp.write_bytes(docker('exec','2026-2','cat',ROOT+'/'+name));archive.put(temp,target,str(target.relative_to(DEST)))
    result={'job':JOB,'state':state['state'],'final':not a.prepare,'archive':str(DEST),'files':len(archive.records),'bytes':sum(r['bytes'] for r in archive.records),'records':archive.records,'created':time.time()}
    if not a.prepare:
        final=json.loads(docker('exec','2026-2','cat',ROOT+'/final.json'))
        model_hashes={}
        for weights,expected in final['best_sha256'].items():
            assert weights.startswith(ROOT+'/runs/')
            local=DEST/'실험기록'/weights.removeprefix(ROOT+'/runs/')
            assert sha(local)==expected,'Final weights mismatch'
            model_hashes[weights]=sha(local)
        assert final['test']['metrics']==state['test_metrics'],'Metrics mismatch'
        archive.remote(ROOT+'/report',DEST/'보고서')
        report=DEST/'보고서'
        result.update(model_sha256=model_hashes,test=final['test'],target_met=final['target_met'],files=len(archive.records),bytes=sum(r['bytes'] for r in archive.records))
        write(DEST/'완료.json',result);write(report/'보관검증.json',{k:v for k,v in result.items() if k!='records'})
    else:write(DEST/'준비자료_검증.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','test')},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
