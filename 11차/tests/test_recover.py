"""작은 공식 범위 수신과 기존 작업자 연결의 실패 경로를 검사합니다."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / '7차'))
import prepare_dataset as data
import worker


@contextlib.contextmanager
def server(content, behavior=lambda number: {}):
    calls = []
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            start, end = map(int, self.headers['Range'].split('=')[1].split('-'))
            calls.append((start, end))
            reply = behavior(len(calls))
            self.send_response(reply.get('status', 206))
            self.send_header('Content-Range', reply.get('range', f'bytes {start}-{end}/{len(content)}'))
            if 'retry_after' in reply:
                self.send_header('Retry-After', reply['retry_after'])
            self.end_headers()
            try:
                self.wfile.write(reply.get('body', content[start:end + 1]))
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
        def log_message(self, *args):
            pass
    service = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=service.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{service.server_port}/fixture', calls
    finally:
        service.shutdown()
        service.server_close()
        thread.join(2)


class Clock:
    def __init__(self):
        self.value = 0
    def __call__(self):
        return self.value


class Response:
    def __init__(self, body, start, end, total, clock=None, step=0, failure=None):
        self.body = io.BytesIO(body)
        self.status = 206
        self.headers = {'Content-Range': f'bytes {start}-{end}/{total}'}
        self.clock, self.step, self.failure = clock, step, failure
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()
    def close(self):
        self.body.close()
    def read1(self, count):
        if self.clock:
            self.clock.value += self.step
        if self.failure:
            error, self.failure = self.failure, None
            raise error
        return self.body.read(min(count, 1024))


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        if not (ROOT / 'recover.py').is_file():
            self.fail('작은 범위 복구 수신기와 원본 작업자 연결이 아직 구현되지 않았습니다.')
        import recover
        self.r = recover
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.content = '공식 원자료 대신 사용하는 고정 검사 본문'.encode('utf-8') * 1600
        self.events = []
        self.sleeps = []
        self.budget = data.DownloadBudget(self.folder, limit=2**24, minimum_free=0)
        self.target = self.folder / 'sample.zip'
    def spec(self, url):
        return {'url': url, 'size': len(self.content), 'md5': hashlib.md5(self.content).hexdigest(), 'source': 'fixture', 'name': 'sample.zip'}
    def receiver(self, **kwargs):
        return self.r.Receiver(data, worker, self.events.append, sleep=self.sleeps.append, **kwargs)
    def test_small_ranges_complete_and_verified_receipt(self):
        with server(self.content) as (url, calls):
            self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(self.target.read_bytes(), self.content)
        self.assertEqual(self.budget.used, len(self.content))
        self.assertGreater(len(calls), 1)
        self.assertTrue(all(end - start + 1 <= 4 * 1024 * 1024 for start, end in calls))
        receipt = data.load(self.target.with_suffix('.zip.verified.json'))
        self.assertEqual(receipt['sha256'], hashlib.sha256(self.content).hexdigest())
    def test_resume_preserves_existing_prefix(self):
        with server(self.content) as (url, calls):
            spec = self.spec(url)
            self.target.with_suffix('.zip.part').write_bytes(self.content[:1234])
            data.atomic_json(self.target.with_suffix('.zip.part.json'), {key: spec[key] for key in ('url', 'size', 'md5')})
            self.receiver().receive(spec, self.target, self.budget)
        self.assertEqual(calls[0][0], 1234)
        self.assertEqual(self.target.read_bytes(), self.content)
        self.assertEqual(self.budget.used, len(self.content) - 1234)
    def test_short_body_retries_saved_offset(self):
        with server(self.content, lambda number: {'body': self.content[:1234]} if number == 1 else {}) as (url, calls):
            self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(calls[1][0], 1234)
        self.assertEqual(self.target.read_bytes(), self.content)
        self.assertTrue(self.sleeps)
    def test_slow_progress_splits_range_without_retry_exhaustion(self):
        clock = Clock()
        calls = []
        def open_fixture(url, headers):
            start, end = map(int, headers['Range'].split('=')[1].split('-'))
            calls.append((start, end))
            return Response(self.content[start:end + 1], start, end, len(self.content), clock, 21)
        self.receiver(clock=clock, opener=open_fixture).receive(self.spec('https://fixture.invalid/sample'), self.target, self.budget)
        self.assertEqual(self.target.read_bytes(), self.content)
        self.assertEqual(self.budget.used, len(self.content))
        self.assertEqual(self.sleeps, [])
        self.assertGreater(len(calls), 7)
    def test_timeout_without_progress_exhausts_six_retries(self):
        calls = []
        def unavailable(url, headers):
            calls.append(headers)
            raise TimeoutError('검사용 연결 시간 초과')
        with self.assertRaises(TimeoutError):
            self.receiver(opener=unavailable).receive(self.spec('https://fixture.invalid/sample'), self.target, self.budget)
        self.assertEqual(len(calls), 7)
        self.assertEqual(self.sleeps, [2, 4, 8, 16, 32, 60])
        self.assertFalse(self.target.exists())
    def test_partial_timeout_keeps_received_bytes(self):
        calls = []
        def interrupted(url, headers):
            start, end = map(int, headers['Range'].split('=')[1].split('-'))
            calls.append(start)
            if len(calls) == 1:
                import http.client
                return Response(b'', start, end, len(self.content), failure=http.client.IncompleteRead(self.content[:17], end - start + 1))
            return Response(self.content[start:end + 1], start, end, len(self.content))
        self.receiver(opener=interrupted).receive(self.spec('https://fixture.invalid/sample'), self.target, self.budget)
        self.assertEqual(calls[1], 17)
        self.assertEqual(self.target.read_bytes(), self.content)
        self.assertEqual(self.budget.used, len(self.content))
    def test_wrong_range_is_fatal(self):
        with server(self.content, lambda number: {'range': 'bytes 1-2/3'}) as (url, calls):
            with self.assertRaises(ValueError):
                self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.sleeps, [])
    def test_http_403_is_fatal(self):
        with server(self.content, lambda number: {'status': 403}) as (url, calls):
            with self.assertRaises(Exception):
                self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.sleeps, [])
    def test_retry_after_is_bounded(self):
        with server(self.content, lambda number: {'status': 503, 'retry_after': '120'} if number == 1 else {}) as (url, calls):
            self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(self.sleeps[0], 60)
    def test_budget_fails_before_request(self):
        self.budget.limit = 1
        with server(self.content) as (url, calls):
            with self.assertRaises(ValueError):
                self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(calls, [])
    def test_ledger_failure_is_not_retried(self):
        original = data.atomic_json
        def ledger_only(path, value):
            if Path(path) == self.budget.path:
                raise OSError('본문 수신 뒤 원장 쓰기 실패')
            return original(path, value)
        with server(self.content) as (url, calls), patch.object(data, 'atomic_json', side_effect=ledger_only):
            with self.assertRaises(OSError):
                self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(len(calls), 1)
        self.assertGreater(self.budget.used, 0)
        self.assertEqual(self.target.with_suffix('.zip.part').stat().st_size, 0)
        self.assertTrue(self.target.with_suffix('.zip.recovery-pending.json').exists())
        self.assertEqual(self.sleeps, [])
    def test_notify_failure_is_not_retried(self):
        def failed(event):
            raise OSError('상태 통지 쓰기 실패')
        with server(self.content) as (url, calls):
            with self.assertRaises(OSError):
                self.r.Receiver(data, worker, failed, sleep=self.sleeps.append).receive(self.spec(url), self.target, self.budget)
        self.assertEqual(self.sleeps, [])
    def test_metadata_mismatch_preserves_prefix(self):
        self.target.with_suffix('.zip.part').write_bytes(b'keep')
        data.atomic_json(self.target.with_suffix('.zip.part.json'), {'url': 'https://other.invalid'})
        with self.assertRaises(ValueError):
            self.receiver().receive(self.spec('https://fixture.invalid/sample'), self.target, self.budget)
        self.assertEqual(self.target.with_suffix('.zip.part').read_bytes(), b'keep')
    def test_wrong_md5_keeps_partial_and_no_success_receipt(self):
        with server(self.content) as (url, calls):
            spec = self.spec(url)
            spec['md5'] = '0' * 32
            with self.assertRaises(ValueError):
                self.receiver().receive(spec, self.target, self.budget)
        self.assertEqual(self.target.with_suffix('.zip.part').read_bytes(), self.content)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.target.with_suffix('.zip.verified.json').exists())
    def test_existing_verified_file_not_downloaded(self):
        self.target.write_bytes(self.content)
        with server(self.content) as (url, calls):
            self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(calls, [])
        self.assertEqual(self.budget.used, 0)
    def test_throttle_preserves_latest_progress_and_clears_retry(self):
        clock = Clock()
        sent = []
        progress = self.r.Progress(lambda **event: sent.append(event), clock=clock)
        for number in range(100):
            progress(download_bytes=number)
        self.assertEqual(len(sent), 1)
        clock.value = 3
        progress(downloaded_bytes=9, retry_reason=None, retry_attempt=0, retry_wait_seconds=0)
        self.assertEqual(sent[-1]['download_bytes'], 99)
        self.assertIsNone(sent[-1]['retry_reason'])

    def test_retry_stage_and_clear_are_immediate_inside_throttle_window(self):
        clock = Clock()
        sent = []
        progress = self.r.Progress(lambda **event: sent.append(event), clock=clock)
        progress(stage='본문 수신', download_bytes=1)
        progress(stage='재시도 대기', retry_reason='TimeoutError', retry_attempt=1, retry_wait_seconds=60)
        self.assertEqual(sent[-1]['stage'], '재시도 대기')
        progress(stage='본문 수신', retry_reason=None, retry_attempt=0, retry_wait_seconds=0)
        self.assertIsNone(sent[-1]['retry_reason'])
        progress(stage='원자료 해시 검증')
        self.assertEqual(sent[-1]['stage'], '원자료 해시 검증')
    def test_pipeline_path_rejects_forged_target(self):
        with self.assertRaises(ValueError):
            self.r.validate_pipeline(self.folder / 'worker.py')
        self.assertEqual(self.r.validate_pipeline(ROOT.parent / '7차/worker.py'), (ROOT.parent / '7차/worker.py').resolve())

    def test_entry_evidence_preserves_real_interpreter_flags(self):
        code = "import sys,json;sys.path.insert(0," + repr(str(ROOT)) + ");import recover;print(json.dumps(recover.entry_evidence()['argv']))"
        argv = [sys.executable, '-B', '-X', 'utf8', '-c', code]
        result = subprocess.run(argv, cwd=ROOT.parent, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8', 'replace'))
        self.assertEqual(json.loads(result.stdout), argv)
    def test_original_baseline_matches_real_files(self):
        self.r.verify_original()
    def test_original_contract_mismatch_is_rejected_without_rebase(self):
        with patch.object(self.r, 'ORIGINAL', self.folder):
            with self.assertRaises((ValueError, FileNotFoundError)):
                self.r.verify_original()
    def test_receiving_lock_blocks_duplicate_receiver(self):
        if sys.platform == 'win32':
            self.skipTest('동일 Linux flock은 Docker에서 검사합니다.')
        lock = self.target.with_name(self.target.name + '.receiving.lock')
        with worker.file_lock(lock, blocking=False):
            with self.assertRaises(RuntimeError):
                self.receiver().receive(self.spec('https://fixture.invalid/sample'), self.target, self.budget)

    def test_full_boundary_incomplete_read_never_requests_reversed_range(self):
        import http.client
        content = b'fixture'
        calls = []
        def response(url, headers):
            start, end = map(int, headers['Range'].split('=')[1].split('-'))
            self.assertLessEqual(start, end)
            calls.append((start, end))
            return Response(b'', start, end, len(content), failure=http.client.IncompleteRead(content, 1))
        spec = {'url': 'https://fixture.invalid', 'size': 7, 'md5': hashlib.md5(content).hexdigest()}
        self.receiver(opener=response).receive(spec, self.target, self.budget)
        self.assertEqual(calls, [(0, 6)])
        self.assertEqual(self.target.read_bytes(), content)

    def test_fast_ranges_grow_but_never_exceed_original_four_mib(self):
        content = b'x' * (9 * 1024 * 1024)
        calls = []
        def response(url, headers):
            start, end = map(int, headers['Range'].split('=')[1].split('-'))
            calls.append((start, end))
            result = Response(content[start:end + 1], start, end, len(content))
            result.read1 = result.body.read
            return result
        spec = {'url': 'https://fixture.invalid', 'size': len(content), 'md5': hashlib.md5(content).hexdigest()}
        self.receiver(opener=response).receive(spec, self.target, self.budget)
        sizes = [end - start + 1 for start, end in calls]
        self.assertEqual(sizes[:3], [65536, 131072, 262144])
        self.assertEqual(max(sizes), 4194304)
        self.assertEqual(self.target.read_bytes(), content)

    def test_uncertain_previous_charge_blocks_new_network_and_preserves_marker(self):
        marker = self.target.with_suffix('.zip.recovery-pending.json')
        marker.write_text('{"audit":"required"}', encoding='utf-8')
        with server(self.content) as (url, calls):
            with self.assertRaisesRegex(ValueError, '감사'):
                self.receiver().receive(self.spec(url), self.target, self.budget)
        self.assertEqual(calls, [])
        self.assertTrue(marker.exists())

    def test_prefetch_ledgers_import_once_and_changed_receipt_is_rejected(self):
        work = self.folder / 'work'
        for name, count in [('preflight', 10), ('prefetch', 20)]:
            data.atomic_json(work / name / 'download_ledger.json', {'download_bytes': count})
        fake = SimpleNamespace(WORK=work, SOURCES=work / 'sources', SOURCE_FILES=[{'name': 'images.zip'}],
            load=data.load, local=data.local, sha256_file=data.sha256_file)
        budget = data.DownloadBudget(fake.SOURCES, limit=100, minimum_free=0)
        self.r.import_frozen_prefetch(fake, worker, budget)
        self.r.import_frozen_prefetch(fake, worker, budget)
        self.assertEqual(budget.used, 30)
        self.assertEqual(data.load(budget.path)['download_bytes'], 30)
        data.atomic_json(work / 'prefetch/download_ledger.json', {'download_bytes': 21})
        with self.assertRaises(ValueError):
            self.r.import_frozen_prefetch(fake, worker, budget)
        self.assertEqual(budget.used, 30)

    def test_contract_mismatch_prevents_original_run(self):
        original_calls = []
        with patch.object(self.r, 'verify_contract', side_effect=ValueError('검사용 계약 불일치')):
            with self.assertRaises(ValueError):
                self.r.prefetch_then_run('fixture', lambda **kw: None, True,
                    lambda *args, **kw: original_calls.append(args), data, worker)
        self.assertEqual(original_calls, [])

    def test_ledger_failure_prevents_original_run(self):
        fake = SimpleNamespace(SOURCES=self.folder, SOURCE_FILES=[self.spec('https://fixture.invalid/sample')],
            DownloadBudget=lambda *args, **kw: self.budget, open_request=data.open_request)
        original_calls = []
        with patch.object(self.r, 'verify_contract'), patch.object(self.r, 'import_frozen_prefetch'), \
                patch.object(self.r.Receiver, 'receive', side_effect=OSError('본문 계상 실패')):
            with self.assertRaises(OSError):
                self.r.prefetch_then_run('fixture', lambda **kw: None, True,
                    lambda *args, **kw: original_calls.append(args), fake, worker)
        self.assertEqual(original_calls, [])

    def pipeline_fixture(self):
        base = self.folder / 'pipeline'
        original = base / '7차'
        recovery = base / '11차'
        baseline = json.loads((ROOT / 'original-baseline.json').read_text(encoding='utf-8'))
        for name in baseline:
            destination = original / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT.parent / '7차' / name, destination)
        recovery.mkdir()
        for name in ('recover.py', 'original-baseline.json'):
            shutil.copy2(ROOT / name, recovery / name)
        return original, recovery

    @unittest.skipIf(sys.platform == 'win32', '실제 시작은 Docker Linux에서만 허용합니다.')
    def test_start_failure_persists_failed_job_and_log(self):
        original, recovery = self.pipeline_fixture()
        with patch.object(self.r, 'ORIGINAL', original), patch.object(self.r, 'ROOT', recovery), \
                patch.object(self.r, 'originals', return_value=(worker, data, None)), \
                patch.object(worker, 'WORK', original / 'work'), patch.object(worker, 'ROOT', original), \
                patch.object(self.r.subprocess, 'Popen', side_effect=OSError('검사용 기동 실패')):
            with self.assertRaises(OSError):
                self.r.start(original / 'worker.py')
            job = worker.jobs()[0]
            self.assertEqual(job['state'], 'failed')
            self.assertIn('기동 실패', job['error'])
            self.assertIn('기동 실패', (worker.WORK / 'jobs' / (job['id'] + '.log')).read_text(encoding='utf-8'))

    @unittest.skipIf(sys.platform == 'win32', '동일 Linux 실행 잠금은 Docker에서 검사합니다.')
    def test_global_run_lock_prevents_new_job(self):
        original, recovery = self.pipeline_fixture()
        with patch.object(self.r, 'ORIGINAL', original), patch.object(self.r, 'ROOT', recovery), \
                patch.object(self.r, 'originals', return_value=(worker, data, None)), \
                patch.object(worker, 'WORK', original / 'work'), patch.object(worker, 'ROOT', original):
            with worker.file_lock(worker.WORK / 'run.lock', blocking=False):
                with self.assertRaises(RuntimeError):
                    self.r.start(original / 'worker.py')
            self.assertEqual(worker.jobs(), [])

    @unittest.skipIf(sys.platform == 'win32', '별도 Linux 자식과 실제 상태 기록은 Docker에서 검사합니다.')
    def test_actual_child_failure_records_state_before_returning_to_user(self):
        original, recovery = self.pipeline_fixture()
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(recovery / 'recover.py'),
            '--pipeline', str(original / 'worker.py'), '--start'], cwd=ROOT.parent, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8', 'replace'))
        launched = json.loads(result.stdout)
        job_path = original / 'work/jobs' / (launched['job'] + '.json')
        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                job = data.load(job_path)
                if job['state'] == 'failed':
                    break
                time.sleep(.1)
            self.assertEqual(job['state'], 'failed')
            self.assertTrue(job['error'])
            self.assertTrue(job_path.with_suffix('.log').read_text(encoding='utf-8').strip())
            self.assertEqual(Path(job['recovery']['entry']).name, 'recover.py')
            self.assertIn(str(original / 'worker.py'), job['recovery']['argv'])
        finally:
            # failed JSON 뒤의 publish가 끝날 때까지 fixture 소유 PID만 기다립니다.
            process = Path('/proc') / str(launched['pid'])
            def alive():
                try:
                    if (process / 'stat').read_text().rsplit(') ', 1)[1].split()[0] in {'Z', 'X'}:
                        return False
                    command = (process / 'cmdline').read_bytes().split(b'\0')
                    return str(recovery / 'recover.py').encode() in command and launched['job'].encode() in command
                except (FileNotFoundError, ProcessLookupError):
                    return False
            deadline = time.monotonic() + 5
            while alive() and time.monotonic() < deadline:
                time.sleep(.05)
            if alive():
                os.kill(launched['pid'], signal.SIGTERM)
                deadline = time.monotonic() + 2
                while alive() and time.monotonic() < deadline:
                    time.sleep(.05)
                if alive():
                    os.kill(launched['pid'], signal.SIGKILL)
                    deadline = time.monotonic() + 2
                    while alive() and time.monotonic() < deadline:
                        time.sleep(.05)
            self.assertFalse(alive(), 'fixture 자식 종료 전 임시 폴더를 정리할 수 없습니다.')

    def test_dead_or_mismatched_child_is_reconciled_as_interrupted(self):
        with patch.object(worker, 'WORK', self.folder / 'work'), patch.object(worker, 'ROOT', ROOT.parent / '7차'):
            worker.save(worker.WORK / 'jobs/fixture.json', {'id': 'fixture', 'kind': 'train', 'state': 'queued',
                'created': time.time(), 'pid': os.getpid(), 'params': {'resume': True}})
            worker._reconcile()
            self.assertEqual(worker.read(worker.WORK / 'jobs/fixture.json')['state'], 'interrupted')


if __name__ == '__main__':
    unittest.main()
