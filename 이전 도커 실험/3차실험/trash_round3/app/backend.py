"""Docker worker. All paths are rooted in the existing PBL directory."""
import os, sys, json, time, uuid, subprocess, traceback, math, hashlib, random
from pathlib import Path

BASE = Path(os.environ.get('TRASH_BASE', '/root/환경 PBL'))
ROOT = BASE / 'trash_round3'
APP = ROOT / 'app'
STATE = APP / 'state'
JOBS = STATE / 'jobs'
VIDEO_EXT = {'.mp4', '.avi', '.mov', '.mkv', '.m4v'}
for p in [APP, STATE, JOBS, APP / 'uploads', APP / 'results']:
    p.mkdir(parents=True, exist_ok=True)

def save(path, value):
    tmp = path.with_suffix('.'+uuid.uuid4().hex+'.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)

def read(path, default=None):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError): return default

def update(job, **kw):
    import fcntl
    p = JOBS / f'{job}.json'
    with (JOBS / f'{job}.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = read(p, {})
        data.update(kw, updated=time.time())
        save(p, data)

def status():
    jobs=[read(p,{}) for p in JOBS.glob('*.json')]
    for j in jobs:
        if j.get('state') in ['running','queued'] and j.get('pid'):
            proc=Path('/proc')/str(j['pid'])
            if not proc.exists() or (proc/'stat').read_text().split()[2]=='Z':
                j.update(state='failed',error='작업 프로세스가 종료되었습니다. 로그를 확인하세요.')
                save(JOBS/(j['id']+'.json'),j)
    selected=read(APP/'selected_model.json',{})
    models=[selected['weights']] if selected.get('weights') else []
    return {'jobs':sorted(jobs,key=lambda j:j.get('created',0),reverse=True),'models':models,
            'dataset':read(ROOT/'data_report.json',{}),'selection':selected,'container':'2026-2','base':str(ROOT)}

def videos():
    return [{'path':str(p), 'name':p.name, 'bytes':p.stat().st_size}
            for root in [ROOT / 'videos', APP / 'uploads']
            for p in sorted(root.rglob('*')) if p.is_file() and p.suffix.lower() in VIDEO_EXT]

def allowed_video(s):
    p=Path(s).resolve()
    if not any(p.is_relative_to(r.resolve()) for r in [ROOT/'videos',APP/'uploads']):
        raise ValueError('허용된 영상 폴더가 아닙니다.')
    if not p.is_file() or p.suffix.lower() not in VIDEO_EXT: raise ValueError('영상 파일이 없습니다.')
    return p

def probe(s):
    import cv2
    p=allowed_video(s)
    if p.stat().st_size == 0: raise ValueError('0바이트 파일입니다. 원본 영상을 다시 복사하세요.')
    c=cv2.VideoCapture(str(p))
    try:
        ok, frame=c.read()
        fps=c.get(cv2.CAP_PROP_FPS); count=c.get(cv2.CAP_PROP_FRAME_COUNT)
        if not ok or frame is None: raise ValueError('첫 프레임을 읽을 수 없습니다. 복사 완료 여부와 코덱/파일 손상을 확인하세요.')
        if not math.isfinite(fps) or fps <= 0: raise ValueError('유효한 FPS가 없습니다. 영상을 재인코딩하세요.')
        key=hashlib.sha256(str(p).encode()).hexdigest()[:20]
        thumbnail=APP/'results'/f'preview_{key}.jpg'
        cv2.imwrite(str(thumbnail), frame)
        return {'width':frame.shape[1], 'height':frame.shape[0], 'fps':fps,
                'seconds':count/fps, 'frames':int(count), 'bytes':p.stat().st_size,
                'preview':str(thumbnail)}
    finally: c.release()


def start(kind, params):
    if kind == 'improve' and (ROOT/'experiment_plan.json').exists():
        raise ValueError('이미 시작한 3차 실험입니다. 중복 학습 대신 현재 작업을 확인하세요.')
    import fcntl
    if kind not in ['improve','detect']: raise ValueError('지원하지 않는 작업')
    with (STATE/'start.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if any(j.get('state') in ['queued','running'] for j in status()['jobs']):
            raise ValueError('진행 중인 작업이 있습니다. 완료 후 실행하세요.')
        job=time.strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:6]
        save(JOBS/(job+'.json'),{'id':job,'kind':kind,'params':params,'state':'queued','created':time.time()})
        with (JOBS/(job+'.log')).open('w') as log:
            p=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),'worker',job],
                               stdout=log,stderr=subprocess.STDOUT,cwd=str(APP),start_new_session=True)
        update(job,pid=p.pid)
        return {'job':job}

def worker(job):
    j=read(JOBS/(job+'.json'))
    update(job,state='running',pid=os.getpid())
    try:
        if j['kind']=='improve':
            from train_round3 import run
            run(job,**j['params'])
        elif j['kind']=='detect':
            from detector import detect
            detect(job,**j['params'])
        else: globals()[j['kind']](job,**j['params'])
        update(job,state='complete',stage='완료',progress=100)
    except Exception as e:
        traceback.print_exc(); update(job,state='failed',error=str(e),stage='실패')

def main():
    cmd=sys.argv[1]
    if cmd=='worker': worker(sys.argv[2]); return
    args=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
    try:
        if cmd=='status': result=status()
        elif cmd=='videos': result=videos()
        elif cmd=='probe': result=probe(args['path'])
        elif cmd=='start': result=start(args['kind'],args.get('params',{}))
        elif cmd=='log':
            if not all(c.isalnum() or c=='_' for c in args['job']): raise ValueError('잘못된 작업 ID')
            result={'text':(JOBS/(args['job']+'.log')).read_text(errors='replace')[-18000:]}
        else: raise ValueError('지원하지 않는 명령')
        print(json.dumps({'ok':True,'data':result},ensure_ascii=False))
    except Exception as e: print(json.dumps({'ok':False,'error':str(e)},ensure_ascii=False)); sys.exit(1)

if __name__=='__main__': main()
