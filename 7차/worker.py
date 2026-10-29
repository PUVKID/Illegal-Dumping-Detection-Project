"""준비와 GPU 학습을 Codex 없이 이어 실행하는 독립 작업자입니다."""
import argparse
from contextlib import contextmanager
import html
import json
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess
import sys
import time
import traceback
import uuid

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
PROC = Path('/proc')
ACTIVE = {'queued', 'running'}


def identity(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value):
        raise ValueError('허용되지 않는 작업 ID입니다.')
    return value


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        temporary.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2), encoding='utf-8')
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def read(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError:
        return default


@contextmanager
def file_lock(path, blocking=True):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        acquired = False
        try:
            if os.name == 'nt':
                import msvcrt
                stream.seek(0, 2)
                if stream.tell() == 0:
                    stream.write(b'\0')
                    stream.flush()
                stream.seek(0)
                try:
                    msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK, 1)
                except OSError as error:
                    if not blocking:
                        raise RuntimeError('준비 또는 학습 작업이 이미 진행 중입니다.') from error
                    raise
            else:
                import fcntl
                try:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
                except BlockingIOError as error:
                    raise RuntimeError('준비 또는 학습 작업이 이미 진행 중입니다.') from error
            acquired = True
            yield
        finally:
            if acquired:
                if os.name == 'nt':
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def is_alive(pid, job):
    try:
        if type(pid) is not int or pid <= 0:
            return False
        identity(job)
        process = PROC / str(pid)
        state = (process / 'stat').read_text().rsplit(') ', 1)[1].split()[0]
        command = (process / 'cmdline').read_bytes().split(b'\0')
        return (state not in {'Z', 'X'} and str(Path(__file__).resolve()).encode() in command
                and any(command[index:index + 2] == [b'--worker', job.encode()]
                        for index in range(len(command) - 1)))
    except (OSError, ValueError, IndexError):
        return False


def jobs():
    return sorted((read(path) for path in (WORK / 'jobs').glob('*.json')),
                  key=lambda value: value.get('created', 0), reverse=True)


def publish():
    values = jobs()
    current = values[0] if values else {'state': 'idle', 'stage': '아직 시작하지 않았습니다.'}
    save(WORK / 'status.json', current)
    names = {'idle': '대기', 'queued': '시작 대기', 'running': '진행 중', 'complete': '완료',
             'failed': '실패', 'interrupted': '중단'}
    text = lambda value: html.escape(str(value), quote=True)
    fields = [('작업', current.get('id', '없음')), ('상태', names.get(current.get('state'), current.get('state'))),
              ('단계', current.get('stage', '')), ('에포크', current.get('epoch', '미시작')),
              ('계획 에포크', current.get('epochs', '미확인')), ('다운로드 바이트', current.get('download_bytes', current.get('downloaded_bytes', '미확인'))),
              ('이미지', current.get('images', current.get('train', '미확인')))]
    rows = ''.join('<tr><th>' + text(key) + '</th><td>' + text(value) + '</td></tr>' for key, value in fields)
    error = '<p class="error">' + text(current.get('error', '')) + '</p>' if current.get('error') else ''
    source = ROOT.parent / '5차/web/fonts/NanumGothic-Bold.ttf'
    font_url = (PureWindowsPath('D:/2026/' + source.as_posix().removeprefix('/workspace/2026/')).as_uri()
                if source.as_posix().startswith('/workspace/2026/') else source.as_uri())
    # 정적 파일은 마지막 저장 시점의 관측입니다. 프로세스 생존 확인은 상태 명령이 수행합니다.
    page = '<!doctype html><html lang="ko"><meta charset="utf-8"><meta http-equiv="refresh" content="15"><title>7차 학습 상태</title><style>@font-face{font-family:Nanum;src:url("' + font_url + '");font-weight:700}body{font:700 16px/1.7 Nanum,sans-serif;background:#f1f5f7;color:#163d40;max-width:960px;margin:40px auto;padding:24px}table{background:white;width:100%;border-collapse:collapse}td,th{padding:14px;text-align:left;border-bottom:1px solid #dde7e9}.error{color:#a12626;white-space:pre-wrap}</style><h1>7차 독립 학습 상태</h1><p>마지막 관측: ' + text(time.strftime('%Y-%m-%d %H:%M:%S %z')) + '</p><p>이 파일은 마지막 저장 상태입니다. PC·Docker가 중단되면 학습상태.bat으로 실제 생존 상태를 확인하세요.</p><table>' + rows + '</table>' + error + '<p>정밀도·재현율 각각 90%는 목표이며 실측 달성을 보장하지 않습니다. 로그와 작업 기록은 work/jobs에 보존합니다.</p></html>'
    destination = WORK / '학습상태.html'
    temporary = destination.with_suffix('.' + uuid.uuid4().hex + '.tmp')
    temporary.write_text(page, encoding='utf-8')
    temporary.replace(destination)
    return {'current': current, 'jobs': values[:20]}


def _update(job, **changes):
    path = WORK / 'jobs' / (identity(job) + '.json')
    value = read(path)
    if not isinstance(value, dict):
        raise ValueError('작업 기록이 없습니다.')
    value.update(changes, updated=time.time())
    save(path, value)
    publish()
    return value


def update(job, **changes):
    with file_lock(WORK / 'jobs/start.lock'):
        return _update(job, **changes)


def _reconcile():
    for value in jobs():
        if value.get('state') in ACTIVE and not is_alive(value.get('pid'), value.get('id')):
            _update(value['id'], state='interrupted',
                    error='작업 프로세스가 종료됐습니다. 원인 확인 후 명시적으로 체크포인트 재개를 선택하세요.',
                    finished=time.time())


def status():
    with file_lock(WORK / 'jobs/start.lock'):
        _reconcile()
        return publish()


def start(params):
    if not isinstance(params, dict) or set(params) - {'resume'} or type(params.get('resume', False)) is not bool:
        raise ValueError('설정은 resume: true 또는 false만 허용하는 JSON 객체입니다.')
    with file_lock(WORK / 'jobs/start.lock'):
        _reconcile()
        if any(value.get('state') in ACTIVE for value in jobs()):
            raise ValueError('준비 또는 학습 작업이 이미 진행 중입니다.')
        # 작업 기록이 손상되거나 유실돼도 실행 중 준비·학습과 겹치지 않습니다.
        with file_lock(WORK / 'run.lock', blocking=False):
            pass
        job = time.strftime('%Y%m%d_%H%M%S') + '_' + uuid.uuid4().hex[:8]
        save(WORK / 'jobs' / (job + '.json'), {'id': job, 'kind': 'train', 'state': 'queued',
             'params': {'resume': params.get('resume', False)}, 'created': time.time(), 'stage': '독립 프로세스 시작'})
        try:
            with (WORK / 'jobs' / (job + '.log')).open('ab') as log:
                child = subprocess.Popen([sys.executable, '-u', '-B', '-X', 'utf8', str(Path(__file__).resolve()), '--worker', job],
                                         cwd=str(ROOT), stdin=subprocess.DEVNULL, stdout=log,
                                         stderr=subprocess.STDOUT, shell=False, start_new_session=True)
            _update(job, pid=child.pid)
        except Exception as error:
            _update(job, state='failed', error=str(error), traceback=traceback.format_exc(), finished=time.time())
            raise
        return {'job': job, 'pid': child.pid, 'state': 'queued', 'status_file': str(WORK / '학습상태.html')}


def execute(job):
    identity(job)
    with file_lock(WORK / 'run.lock', blocking=False):
        value = read(WORK / 'jobs' / (job + '.json'))
        if not value or value.get('state') != 'queued' or value.get('kind') != 'train':
            raise ValueError('새로 대기 중인 학습 작업만 실행할 수 있습니다.')
        update(job, state='running', pid=os.getpid(), stage='자료 준비와 학습 시작', error=None)
        try:
            from train_pipeline import run
            protected = {'id', 'kind', 'created', 'params', 'pid', 'state', 'error', 'traceback', 'finished', 'updated'}
            def notify(**changes):
                update(job, **{key: value for key, value in changes.items() if key not in protected})
            result = run(job, notify=notify, resume=value['params']['resume'])
            if not isinstance(result, dict):
                raise ValueError('학습 파이프라인이 결과 객체를 반환하지 않았습니다.')
            update(job, state='complete', stage='준비·학습·평가 파이프라인 완료', result=result,
                   error=None, finished=time.time())
        except BaseException as error:
            trace = traceback.format_exc()
            # 실패 상태를 관측할 때는 원문 로그도 이미 저장돼 있어야 합니다.
            print(trace, file=sys.stderr, flush=True)
            update(job, state='interrupted' if isinstance(error, (KeyboardInterrupt, SystemExit)) else 'failed',
                   error=str(error) or type(error).__name__, traceback=trace, finished=time.time())
            raise


def main():
    parser = argparse.ArgumentParser(description='7차 준비·학습 독립 실행')
    parser.add_argument('--action', choices=['train', 'status'])
    parser.add_argument('--params', default='{}')
    parser.add_argument('--worker')
    args = parser.parse_args()
    try:
        if args.worker:
            execute(args.worker)
            return
        if args.action == 'train':
            result = start(json.loads(args.params))
        elif args.action == 'status':
            result = status()
        else:
            raise ValueError('--action train 또는 status가 필요합니다.')
        print(json.dumps({'ok': True, 'data': result}, ensure_ascii=False, allow_nan=False))
    except Exception as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
