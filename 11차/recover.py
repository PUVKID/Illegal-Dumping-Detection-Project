"""7차 계약을 보존하며 작은 범위의 원자료 수신을 앞에 연결합니다."""
import argparse
import hashlib
import http.client
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback
import uuid

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / '7차'
MIN_RANGE = 64 * 1024
MAX_RANGE = 4 * 1024 * 1024


def validate_pipeline(value):
    path = Path(value)
    if path.is_symlink() or path.resolve() != (ORIGINAL / 'worker.py').resolve():
        raise ValueError('고정된 7차 작업자 경로만 허용합니다.')
    return path.resolve()


def verify_original():
    baseline = json.loads((ROOT / 'original-baseline.json').read_text(encoding='utf-8'))
    for name, expected in baseline.items():
        path = ORIGINAL / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('7차 고정 원본이 변경됐습니다: ' + name)
    return baseline


def originals():
    verify_original()
    sys.path.insert(0, str(ORIGINAL))
    modules = tuple(importlib.import_module(name) for name in ('worker', 'prepare_dataset', 'train_pipeline'))
    for module in modules:
        if Path(module.__file__).resolve().parent != ORIGINAL.resolve():
            raise ValueError('다른 프로젝트의 모듈은 실행할 수 없습니다.')
    return modules


class Progress:
    """원장 합산은 매 본문마다 유지하고 화면 쓰기만 합칩니다."""
    def __init__(self, notify, clock=time.monotonic):
        self.notify, self.clock = notify, clock
        self.latest = {}
        self.last = float('-inf')
    def __call__(self, force=False, **changes):
        retry_transition = 'retry_reason' in changes and (changes['retry_reason'] is not None or self.latest.get('retry_reason') is not None)
        stage_transition = 'stage' in changes and changes['stage'] != self.latest.get('stage')
        self.latest.update(changes)
        now = self.clock()
        if force or retry_transition or stage_transition or now - self.last >= 2:
            self.notify(**self.latest)
            self.last = now


class NetworkRetry(Exception):
    """연결·본문 읽기 경계의 실제 일시 오류만 나타냅니다."""
    def __init__(self, error):
        self.error = error


class Receiver:
    def __init__(self, data, worker, notify, clock=time.monotonic, sleep=time.sleep, opener=None):
        self.data, self.worker, self.notify = data, worker, notify
        self.clock, self.sleep = clock, sleep
        self.opener = opener or data.open_request
    def emit(self, **event):
        self.notify(event)
    def network_open(self, spec, start, end):
        try:
            return self.opener(spec['url'], {'Range': f'bytes={start}-{end}'})
        except (OSError, http.client.HTTPException) as error:
            if isinstance(error, self.data.urllib.error.HTTPError):
                error.close()
            if self.data._temporary_download_error(error):
                raise NetworkRetry(error) from error
            raise
    def receive(self, spec, target, budget):
        target = Path(target)
        lock = target.with_name(target.name + '.receiving.lock')
        partial = target.with_suffix(target.suffix + '.part')
        metadata = target.with_suffix(target.suffix + '.part.json')
        marker = target.with_suffix(target.suffix + '.recovery-pending.json')
        for path in (target, partial, metadata, marker, lock):
            if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
                raise ValueError('수신 경로의 연결 파일을 허용하지 않습니다.')
        with self.worker.file_lock(lock, blocking=False):
            identity = {key: spec[key] for key in ('url', 'size', 'md5')}
            if marker.exists():
                raise ValueError('이전 수신의 원장·디스크 반영이 불확실합니다. 복구 기록 감사가 필요합니다.')
            if target.exists():
                self.finish(spec, target)
                return target
            if partial.exists() and (not metadata.exists() or self.data.load(metadata) != identity):
                raise ValueError('부분 파일의 공식 원자료 계약이 다릅니다.')
            start = partial.stat().st_size if partial.exists() else 0
            if start > spec['size']:
                raise ValueError('부분 파일이 공식 원본보다 큽니다.')
            budget.space(spec['size'] - start + 8192)
            self.data.atomic_json(metadata, identity)
            chunk_size = MIN_RANGE
            while start < spec['size']:
                end = min(spec['size'], start + chunk_size) - 1
                for attempt in range(7):
                    if start > end:
                        self.emit(retry_reason=None, retry_attempt=0, retry_wait_seconds=0)
                        break
                    saved = partial.stat().st_size if partial.exists() else 0
                    if saved != start or self.data.load(metadata) != identity:
                        raise ValueError('수신 중 부분 파일·계약이 변경됐습니다.')
                    if budget.used + end - start + 1 > budget.limit:
                        raise ValueError('남은 전송 예산이 부족합니다.')
                    # 요청 전 불확실 구간을 기록합니다. 원장·상태·디스크 오류면 지우지 않습니다.
                    self.data.atomic_json(marker, {'identity': identity, 'start': start, 'end': end,
                        'ledger_before_bytes': budget.used,
                        'ledger_before_sha256': self.data.sha256_file(budget.path) if budget.path.exists() else None})
                    began = self.clock()
                    range_start = start
                    split = False
                    failure = None
                    try:
                        with self.network_open(spec, start, end) as response:
                            if response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}':
                                raise ValueError('공식 범위 응답이 요청과 다릅니다.')
                            with partial.open('ab') as stream:
                                while start <= end:
                                    if self.clock() - began >= 40:
                                        if start > range_start:
                                            split = True
                                            break
                                        raise NetworkRetry(TimeoutError('진행 없는 범위가 40초를 초과했습니다.'))
                                    budget.space(min(256 * 1024, end - start + 1) + 8192)
                                    interrupted = None
                                    try:
                                        block = response.read1(min(256 * 1024, end - start + 1))
                                    except http.client.IncompleteRead as error:
                                        block, interrupted = error.partial, error
                                    except (OSError, http.client.HTTPException) as error:
                                        if self.data._temporary_download_error(error):
                                            raise NetworkRetry(error) from error
                                        raise
                                    if not block:
                                        raise NetworkRetry(interrupted or EOFError('범위 본문이 중간에 끝났습니다.'))
                                    # 이 아래의 원장·통지·디스크 오류는 네트워크 재시도로 잡지 않습니다.
                                    budget.charge(len(block))
                                    if len(block) > end - start + 1:
                                        raise ValueError('수신 본문이 공식 범위를 넘었습니다.')
                                    budget.space(len(block) + 8192)
                                    if stream.write(block) != len(block):
                                        raise OSError('부분 파일을 모두 기록하지 못했습니다.')
                                    start += len(block)
                                    self.emit(stage='공식 원자료 작은 범위 복구 수신', source=spec.get('source'), file=target.name,
                                        downloaded_bytes=start, file_bytes=spec['size'], range_bytes=chunk_size)
                                    if interrupted:
                                        raise NetworkRetry(interrupted) from interrupted
                    except NetworkRetry as error:
                        failure = error.error
                    # 정상 닫힘과 실제 저장 위치·원장 확인 뒤에만 불확실 표식을 해제합니다.
                    if (partial.stat().st_size if partial.exists() else 0) != start:
                        raise ValueError('닫힌 부분 파일의 실제 저장량이 다릅니다.')
                    if budget.path.exists() and self.data.load(budget.path)['download_bytes'] != budget.used:
                        raise ValueError('실제 전송 원장이 메모리 계상과 다릅니다.')
                    marker.unlink()
                    if failure is not None:
                        self.emit(stage='공식 원자료 복구 재시도' if attempt < 6 else '공식 원자료 복구 재시도 한도 초과',
                            source=spec.get('source'), file=target.name, downloaded_bytes=start, file_bytes=spec['size'],
                            retry_reason=type(failure).__name__ + ': ' + str(failure), retry_attempt=min(attempt + 1, 6),
                            retry_limit=6, retry_wait_seconds=self.data._download_retry_delay(failure, attempt) if attempt < 6 else 0)
                        if attempt == 6:
                            raise failure
                        if start <= end:
                            self.sleep(self.data._download_retry_delay(failure, attempt))
                        continue
                    elapsed = self.clock() - began
                    if split or elapsed >= 20:
                        chunk_size = max(MIN_RANGE, chunk_size // 2)
                    elif elapsed < 10:
                        chunk_size = min(MAX_RANGE, chunk_size * 2)
                    self.emit(source=spec.get('source'), file=target.name, downloaded_bytes=start, file_bytes=spec['size'],
                        retry_reason=None, retry_attempt=0, retry_wait_seconds=0)
                    break
            if partial.stat().st_size != spec['size'] or self.data.digest_file(partial, 'md5') != spec['md5']:
                raise ValueError('완성 원자료의 공식 크기·MD5가 다릅니다.')
            partial.replace(target)
            self.finish(spec, target)
            return target
    def finish(self, spec, target):
        if target.stat().st_size != spec['size'] or self.data.digest_file(target, 'md5') != spec['md5']:
            raise ValueError('기존 원자료의 공식 크기·MD5가 다릅니다.')
        self.data.freeze(target.with_suffix(target.suffix + '.verified.json'),
            {**{key: spec[key] for key in ('url', 'size', 'md5')}, 'sha256': self.data.sha256_file(target)})


def entry_evidence():
    return {'entry': str(Path(__file__).resolve()), 'entry_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'argv': list(sys.orig_argv), 'original_baseline': verify_original(), 'recovery': '작은 범위 원자료 수신 후 원래 7차 준비·학습 호출'}


def verify_contract(data):
    expected = {'source_files': data.SOURCE_FILES, 'normalization': data.NORMALIZATION, 'seed': data.SEED,
        'preparation_sha256': data.sha256_file(data.__file__),
        'previous_manifest_sha256': data.sha256_file(data.PREVIOUS / 'data_manifest.json'),
        'config_sha256': data.sha256_file(data.ROOT / 'configs/training.json'),
        'protected_sources_sha256': data.sha256_file(data.ROOT / 'configs/protected_sources.json'),
        'prior_additional_manifest_sha256': data.sha256_file(data.ARCHIVE / 'sources/additional_manifest.json')}
    if data.load(data.TRAINING / 'preparation_contract.json') != expected:
        raise ValueError('원래 준비 계약과 보존 입력이 다릅니다. 계약을 갱신하지 않습니다.')
    if data.load(data.SOURCES / 'source_contract.json') != {'files': data.SOURCE_FILES, 'license_evidence': 'evidence/공식데이터출처.json'}:
        raise ValueError('고정 공식 원자료 계약이 다릅니다.')


def import_frozen_prefetch(data, worker, budget):
    budget.import_prefetch(data.WORK / 'preflight/download_ledger.json')
    spec = next(row for row in data.SOURCE_FILES if row['name'] == 'images.zip')
    target = data.SOURCES / 'downloads/images.zip'
    with worker.file_lock(target.with_name(target.name + '.receiving.lock'), blocking=False):
        prefetch = data.WORK / 'prefetch'
        state = data.load(prefetch / 'status.json') if (prefetch / 'status.json').exists() else {}
        if state.get('state') == 'running':
            raise ValueError('기존 사전 수신 상태가 실행 중입니다.')
        budget.import_prefetch(prefetch / 'download_ledger.json')
        if state.get('state') == 'complete':
            receipt = data.load(prefetch / 'complete.json')
            if (any(state.get(key) != value for key, value in receipt.items())
                    or receipt['expected_bytes'] != spec['size'] or receipt['md5'] != spec['md5']
                    or receipt['url'] != spec['url'] or data.local(receipt['path']).resolve() != target.resolve()
                    or int(data.load(prefetch / 'download_ledger.json')['download_bytes']) != receipt['download_bytes']
                    or not target.exists() or data.sha256_file(target) != receipt['sha256']):
                raise ValueError('동결 사전 수신 영수증과 공식 자료가 다릅니다.')


def prefetch_then_run(job, notify, resume, original_run, data, worker):
    if resume is not True:
        raise ValueError('기존 계약의 명시적 재개만 허용합니다.')
    evidence = entry_evidence()
    verify_contract(data)
    progress = Progress(notify)
    budget = data.DownloadBudget(data.SOURCES, notify=progress)
    import_frozen_prefetch(data, worker, budget)
    receiver = Receiver(data, worker, lambda event: progress(**event))
    files = []
    for spec in data.SOURCE_FILES:
        destination = data.SOURCES / 'downloads' / spec['name']
        partial = destination.with_suffix(destination.suffix + '.part')
        observed = destination.stat().st_size if destination.exists() else partial.stat().st_size if partial.exists() else 0
        progress(force=True, stage='11차 원자료 복구·기존 계약 확인', source=spec['source'], file=spec['name'],
            downloaded_bytes=observed, file_bytes=spec['size'], retry_reason=None, retry_attempt=0, retry_wait_seconds=0)
        target = receiver.receive(spec, destination, budget)
        files.append({'name': spec['name'], 'receipt': data.load(target.with_suffix(target.suffix + '.verified.json'))})
    data.atomic_json(ROOT / 'work' / 'receipts' / (worker.identity(job) + '.json'),
        {'job': job, **evidence, 'files': files, 'download_bytes': budget.used, 'observed_at': time.time()})
    progress(force=True, stage='복구 원자료 검증 완료·원래 7차 준비로 연결', retry_reason=None, retry_attempt=0, retry_wait_seconds=0)
    return original_run(job, notify=notify, resume=True)


def execute(job, pipeline):
    validate_pipeline(pipeline)
    worker, data, training = originals()
    original_run = training.run
    def wrapped(current_job, notify, resume):
        training.verify_models()
        return prefetch_then_run(current_job, notify, resume, original_run, data, worker)
    training.run = wrapped
    try:
        worker.execute(job)
    finally:
        training.run = original_run


def start(pipeline):
    validate_pipeline(pipeline)
    worker, data, training = originals()
    if os.name != 'posix':
        raise ValueError('실제 복구는 동일 Docker Linux에서 실행해야 합니다.')
    with worker.file_lock(worker.WORK / 'jobs/start.lock'):
        worker._reconcile()
        if any(value.get('state') in worker.ACTIVE for value in worker.jobs()):
            raise ValueError('준비 또는 학습 작업이 이미 진행 중입니다.')
        with worker.file_lock(worker.WORK / 'run.lock', blocking=False):
            pass
        job = time.strftime('%Y%m%d_%H%M%S') + '_' + uuid.uuid4().hex[:8]
        argv = [sys.executable, '-u', '-B', '-X', 'utf8', str(ROOT / 'recover.py'), '--pipeline', str(validate_pipeline(pipeline)), '--worker', job]
        evidence = entry_evidence()
        evidence['argv'] = argv
        worker.save(worker.WORK / 'jobs' / (job + '.json'), {'id': job, 'kind': 'train', 'state': 'queued',
            'params': {'resume': True}, 'created': time.time(), 'stage': '11차 원자료 복구 시작 대기', 'recovery': evidence})
        try:
            with (worker.WORK / 'jobs' / (job + '.log')).open('ab') as log:
                child = subprocess.Popen(argv, cwd=str(ORIGINAL), stdin=subprocess.DEVNULL, stdout=log,
                    stderr=subprocess.STDOUT, shell=False, start_new_session=True)
            worker._update(job, pid=child.pid)
        except Exception as error:
            with (worker.WORK / 'jobs' / (job + '.log')).open('a', encoding='utf-8') as log:
                log.write(traceback.format_exc())
                log.flush()
            worker._update(job, state='failed', error=str(error), finished=time.time())
            raise
        return {'job': job, 'pid': child.pid, 'state': 'queued'}


def main():
    parser = argparse.ArgumentParser(description='고정 7차 원본과 계약을 보존하는 복구 실행기')
    parser.add_argument('--pipeline', required=True)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--start', action='store_true')
    choice.add_argument('--worker')
    args = parser.parse_args()
    if args.start:
        print(json.dumps(start(args.pipeline), ensure_ascii=False))
    else:
        execute(args.worker, args.pipeline)


if __name__ == '__main__':
    main()
