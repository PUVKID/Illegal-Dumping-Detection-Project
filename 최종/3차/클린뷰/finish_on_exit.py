"""One local completion-file event subscription. No periodic queries or AI/API calls."""
import csv, ctypes, json, msvcrt, os, subprocess, sys, time, traceback
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
DEST = SOURCE.parent
WORK = DEST / '_작업' / 'completion_once'
JOB = '20261013_060956_6d373b'
REMOTE_STATE = '/root/환경 PBL/trash_round3/app/state/jobs/' + JOB + '.json'
FLAGS = subprocess.CREATE_NO_WINDOW

# An OS file-change event reports completion even if Python worker teardown hangs.
# A process-exit handle detects unexpected failure. Neither uses periodic queries.
WAIT_CODE = r'''
import json,os,select,sys,ctypes,struct
from pathlib import Path
p=Path(sys.argv[1]);job=sys.argv[2]
libc=ctypes.CDLL(None,use_errno=True)
fd=libc.inotify_init1(os.O_CLOEXEC)
if fd<0:raise OSError(ctypes.get_errno(),'inotify_init1')
wd=libc.inotify_add_watch(fd,os.fsencode(p.parent),0x80)
if wd<0:raise OSError(ctypes.get_errno(),'inotify_add_watch')
state=json.loads(p.read_text());pidfd=None
if state.get('state') in ('running','queued'):
    try:
        pidfd=os.pidfd_open(int(state['pid']))
        cmd=(Path('/proc')/str(state['pid'])/'cmdline').read_bytes()
        if job.encode() not in cmd or b'backend.py' not in cmd:raise RuntimeError('Worker PID mismatch')
    except (ProcessLookupError,FileNotFoundError):pidfd=None
print('READY',flush=True)
events=select.poll();events.register(fd,select.POLLIN)
if pidfd is not None:events.register(pidfd,select.POLLIN)
while state.get('state') in ('queued','running') and pidfd is not None:
    ready=events.poll()  # OS events only: no timer, periodic queries, or AI calls.
    exited=any(n==pidfd for n,mask in ready)
    if exited:state=json.loads(p.read_text());break
    raw=os.read(fd,65536);offset=0
    while offset<len(raw):
        wd,mask,cookie,length=struct.unpack_from('iIII',raw,offset)
        name=raw[offset+16:offset+16+length].split(bytes([0]),1)[0];offset+=16+length
        if name==os.fsencode(p.name):state=json.loads(p.read_text())
if pidfd is not None:os.close(pidfd)
os.close(fd)
print(json.dumps(state,ensure_ascii=False),flush=True)
'''

def state(stage, **fields):
    p=WORK/'state.json';tmp=p.with_suffix('.tmp')
    tmp.write_text(json.dumps({'stage':stage,'pid':os.getpid(),'job':JOB,'updated':time.time(),**fields},ensure_ascii=False,indent=2),encoding='utf-8')
    os.replace(tmp,p)

def notify(text, error=False):
    ctypes.windll.user32.MessageBoxW(None,text,'클린뷰 · 학습 결과',0x10 if error else 0x40)

def verify_report():
    receipt=json.loads((DEST/'완료.json').read_text(encoding='utf-8'))
    summary=json.loads((DEST/'보고서/summary.json').read_text(encoding='utf-8'))
    assert receipt['final'] and receipt['job']==JOB
    assert receipt['test']==summary['test']
    op=summary['test']['operating'];metrics=summary['test']['metrics']
    expected={'정밀도':op['precision'],'재현율':op['recall'],'F1':op['f1'],
              'mAP50':metrics['metrics/mAP50(B)'],'mAP50–95':metrics['metrics/mAP50-95(B)']}
    with (DEST/'보고서/최종성능.csv').open(encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==len(expected)
    for row in rows:assert abs(float(row['비율'])-expected[row['지표']])<1e-10
    for name in ['최종성능.png','학습곡선.png','검증임계값.png','테스트곡선.png','탐지개수.png']:
        p=DEST/'보고서'/name
        with p.open('rb') as f:assert f.read(8)==b'\x89PNG\r\n\x1a\n'
        assert p.stat().st_size>1000
    assert (DEST/'보고서/3차_최종보고서.html').stat().st_size>1000
    return summary

def main():
    WORK.mkdir(parents=True,exist_ok=True)
    lock=(WORK/'listener.lock').open('a+b')
    if lock.tell()==0:lock.write(b'0');lock.flush()
    lock.seek(0)
    try:msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    except OSError:return  # An existing event subscriber owns this job.
    previous=WORK/'state.json'
    if previous.exists() and json.loads(previous.read_text(encoding='utf-8')).get('stage')=='complete':return
    sys.stdout=sys.stderr=(WORK/'completion.log').open('a',encoding='utf-8',buffering=1)
    try:
        state('subscribing')
        proc=subprocess.Popen(['docker','exec','2026-2','python','-u','-c',WAIT_CODE,REMOTE_STATE,JOB],
                              stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=FLAGS)
        ready=proc.stdout.readline().decode('utf-8').strip()
        if ready!='READY':raise RuntimeError(proc.stderr.read().decode('utf-8',errors='replace') or ready)
        state('waiting_for_completion_event',mechanism='Linux atomic completion-file event; no periodic checks',docker_wait_pid=proc.pid)
        output=proc.stdout.read()  # Blocks on the process-exit event, no polling.
        error=proc.stderr.read()
        proc.wait()
        if proc.returncode:raise RuntimeError(error.decode('utf-8',errors='replace'))
        job=json.loads(output.decode('utf-8'))
        if job.get('state')!='complete' or not job.get('test_metrics'):
            raise RuntimeError(job.get('error') or '학습 프로세스가 최종 평가 완료 전에 종료되었습니다.')
        state('saving_files')
        subprocess.run([sys.executable,'-X','utf8',str(SOURCE/'finalize_round3.py')],
                       stdout=sys.stdout,stderr=sys.stderr,creationflags=FLAGS,check=True)
        summary=verify_report();op=summary['test']['operating']
        state('complete',folder=str(DEST),target_met=summary['target_met'],test=summary['test'])
        notify('학습·평가와 파일 저장이 끝났습니다.\n\n'
               f"정밀도 {op['precision']*100:.2f}% / 재현율 {op['recall']*100:.2f}%\n"
               f"90% 목표: {'달성' if summary['target_met'] else '미달성'}\n\n"
               f'파일 위치: {DEST}\n보고서: 보고서 폴더의 3차_최종보고서.html')
    except Exception as e:
        traceback.print_exc();state('failed',error=str(e))
        notify('학습 또는 결과 저장 중 확인이 필요한 오류가 발생했습니다.\n'
               '학습을 자동으로 재시작하지 않았습니다.\n\n'+str(e)[-700:]+
               '\n\n오류 기록: '+str(WORK/'completion.log'),error=True)

if __name__=='__main__':main()
