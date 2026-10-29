"""독립 작업의 중복 배제·상태·명시 재개 계약을 검사합니다."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
import time
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.find_spec('worker')
if spec:
    import worker
else:
    worker = None


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(worker, '독립 worker 구현이 필요합니다.')
        self.temp = tempfile.TemporaryDirectory()
        self.fixture_children = []
        self.work = Path(self.temp.name) / 'work'
        self.work.mkdir()
        self.work_patch = patch.object(worker, 'WORK', self.work)
        self.work_patch.start()

    def tearDown(self):
        if hasattr(self, 'temp'):
            try:
                # 완료 상태 뒤의 마지막 화면 저장까지 자식 종료 후 임시 폴더를 정리합니다.
                for pid in self.fixture_children:
                    deadline = time.monotonic() + 5
                    while time.monotonic() < deadline:
                        try:
                            state = (Path('/proc') / str(pid) / 'stat').read_text().rsplit(') ', 1)[1].split()[0]
                        except FileNotFoundError:
                            break
                        if state in {'Z', 'X'}:
                            break
                        time.sleep(0.02)
                    else:
                        self.fail('검사가 만든 자식 프로세스가 정리 시간 안에 종료되지 않았습니다.')
                self.temp.cleanup()
            finally:
                self.work_patch.stop()

    def job(self, identity='fixture', **values):
        data = {'id': identity, 'kind': 'train', 'state': 'queued', 'params': {'resume': False}, 'created': 1}
        data.update(values)
        worker.save(self.work / 'jobs' / (identity + '.json'), data)
        return data

    def test_resume_must_be_explicit_boolean(self):
        for bad in ({'resume': 'false'}, {'resume': 1}, {'resume': None}, {'force': True}, []):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                worker.start(bad)
        self.assertFalse((self.work / 'jobs').exists())

    def test_invalid_identity_cannot_escape_jobs(self):
        for identity in ('../outside', 'a/b', '', 'a\\b'):
            with self.subTest(identity=identity), self.assertRaises(ValueError):
                worker.execute(identity)

    def test_preparation_and_training_have_one_lifetime_lock(self):
        self.job()
        with worker.file_lock(self.work / 'run.lock', blocking=False):
            with self.assertRaisesRegex(RuntimeError, '진행 중'):
                worker.execute('fixture')
        self.assertEqual(worker.read(self.work / 'jobs/fixture.json')['state'], 'queued')

    def test_success_forwards_resume_and_keeps_current_status(self):
        self.job(params={'resume': True})
        received = []
        def run(identity, notify, resume):
            received.append((identity, resume))
            notify(stage='자료 준비', epoch=0)
            self.assertEqual(worker.read(self.work / 'status.json')['stage'], '자료 준비')
            return {'result': '실측 결과'}
        with patch.dict(sys.modules, {'train_pipeline': types.SimpleNamespace(run=run)}):
            worker.execute('fixture')
        value = worker.read(self.work / 'status.json')
        self.assertEqual(received, [('fixture', True)])
        self.assertEqual(value['state'], 'complete')
        self.assertEqual(value['result'], {'result': '실측 결과'})

    def test_failure_keeps_error_and_traceback(self):
        self.job()
        def run(*args, **kwargs):
            raise ValueError('고정 manifest 불일치')
        with patch.dict(sys.modules, {'train_pipeline': types.SimpleNamespace(run=run)}), patch('sys.stderr'):
            with self.assertRaisesRegex(ValueError, 'manifest'):
                worker.execute('fixture')
        value = worker.read(self.work / 'status.json')
        self.assertEqual(value['state'], 'failed')
        self.assertEqual(value['error'], '고정 manifest 불일치')
        self.assertIn('ValueError', value['traceback'])

    def test_live_owned_job_blocks_second_start(self):
        self.job(state='running', pid=123)
        with patch.object(worker, 'is_alive', return_value=True):
            with self.assertRaisesRegex(ValueError, '진행 중'):
                worker.start({'resume': True})
        self.assertEqual(len(list((self.work / 'jobs').glob('*.json'))), 1)

    def test_dead_job_is_interrupted_on_status(self):
        self.job(state='running', pid=123)
        with patch.object(worker, 'is_alive', return_value=False):
            value = worker.status()
        self.assertEqual(value['current']['state'], 'interrupted')
        self.assertIn('재개', value['current']['error'])

    def test_pid_reuse_and_zombie_cannot_be_accepted(self):
        proc = Path(self.temp.name) / 'proc'
        target = proc / '123'
        target.mkdir(parents=True)
        (target / 'stat').write_text('123 (python worker) S 0', encoding='utf-8')
        with patch.object(worker, 'PROC', proc):
            (target / 'cmdline').write_bytes(b'python\0other.py\0--worker\0fixture\0')
            self.assertFalse(worker.is_alive(123, 'fixture'))
            command = b'python\0' + str(Path(worker.__file__).resolve()).encode() + b'\0--worker\0fixture\0'
            (target / 'cmdline').write_bytes(command)
            self.assertTrue(worker.is_alive(123, 'fixture'))
            self.assertFalse(worker.is_alive(123, 'another'))
            (target / 'stat').write_text('123 (python worker) Z 0', encoding='utf-8')
            self.assertFalse(worker.is_alive(123, 'fixture'))

    def test_failed_child_spawn_is_recorded(self):
        with patch.object(worker.subprocess, 'Popen', side_effect=OSError('프로세스 생성 실패')):
            with self.assertRaises(OSError):
                worker.start({'resume': False})
        self.assertEqual(worker.read(self.work / 'status.json')['state'], 'failed')

    def test_older_job_update_does_not_overwrite_new_current_job(self):
        self.job('old', created=1, state='failed')
        self.job('new', created=2, state='failed', error='새 작업 오류')
        worker.update('old', epoch=79)
        value = worker.read(self.work / 'status.json')
        self.assertEqual(value['id'], 'new')
        self.assertNotIn('epoch', value)

    def test_html_escapes_error_and_does_not_claim_success(self):
        self.job(state='failed', error='<script>위험</script>')
        value = worker.status()
        html = (self.work / '학습상태.html').read_text(encoding='utf-8')
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>', html)
        self.assertEqual(value['current']['state'], 'failed')

    @unittest.skipUnless(os.name == 'posix', '실제 Linux PID·fcntl 동작 fixture는 Docker에서 실행합니다.')
    def test_real_cli_background_lock_failure_log_and_resume(self):
        base = Path(self.temp.name) / 'isolated'
        base.mkdir()
        shutil.copy2(worker.__file__, base / 'worker.py')
        (base / 'train_pipeline.py').write_text(
            "import time\ndef run(job, notify, resume=False):\n"
            "    notify(stage='fixture preparation', epoch=0)\n"
            "    if not resume:\n"
            "        time.sleep(0.7)\n"
            "        raise ValueError('fixture expected failure')\n"
            "    return {'resume':resume}\n", encoding='utf-8')
        command = [sys.executable, '-B', '-X', 'utf8', str(base / 'worker.py')]
        first = subprocess.run(command + ['--action', 'train', '--params', '{"resume":false}'],
                               capture_output=True, timeout=5, shell=False)
        self.assertEqual(first.returncode, 0, first.stderr)
        info = json.loads(first.stdout)['data']
        self.fixture_children.append(info['pid'])
        path = base / 'work/jobs' / (info['job'] + '.json')
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            current = json.loads(path.read_text(encoding='utf-8'))
            if current['state'] == 'running':
                break
            time.sleep(0.02)
        self.assertEqual(current['state'], 'running')
        duplicate = subprocess.run(command + ['--action', 'train'], capture_output=True, timeout=5, shell=False)
        self.assertEqual(duplicate.returncode, 1)
        self.assertIn('진행 중', json.loads(duplicate.stdout)['error'])
        while time.monotonic() < deadline:
            current = json.loads(path.read_text(encoding='utf-8'))
            if current['state'] == 'failed':
                break
            time.sleep(0.02)
        self.assertEqual(current['state'], 'failed')
        self.assertEqual(current['error'], 'fixture expected failure')
        self.assertIn('ValueError', current['traceback'])
        log = path.with_suffix('.log').read_text(encoding='utf-8')
        self.assertIn('fixture expected failure', log)
        resumed = subprocess.run(command + ['--action', 'train', '--params', '{"resume":true}'],
                                 capture_output=True, timeout=5, shell=False)
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        resumed_info = json.loads(resumed.stdout)['data']
        self.fixture_children.append(resumed_info['pid'])
        next_path = base / 'work/jobs' / (resumed_info['job'] + '.json')
        while time.monotonic() < deadline:
            value = json.loads(next_path.read_text(encoding='utf-8'))
            if value['state'] == 'complete':
                break
            time.sleep(0.02)
        self.assertEqual(value['state'], 'complete')
        self.assertTrue(value['result']['resume'])


if __name__ == '__main__':
    unittest.main()
