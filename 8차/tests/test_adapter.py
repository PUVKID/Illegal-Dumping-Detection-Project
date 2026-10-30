"""상태 출처와 시각·중복 시작·원래 HTTP 경계를 회귀 검사합니다."""
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.parse import quote
from unittest.mock import patch
import dashboard
import pipeline


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / '7차'
        self.old = self.base / '5차'
        self.job = {'id': 'known_7', 'kind': 'train', 'state': 'running', 'created': 100,
                    'updated': 200, 'stage': '공식 원자료 다운로드', 'download_bytes': 321}
        self.save(self.root / 'work/jobs/known_7.json', self.job)
        self.save(self.root / 'configs/training.json', {'candidates': [{'name': 'one'}, {'name': 'two'}]})

    def save(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')

    def status(self, now=220):
        return pipeline.status(self.root, self.old, now)

    def test_preparation_not_gpu_training(self):
        value = self.status()
        self.assertEqual(value['training']['phase'], '자료 준비')
        self.assertEqual(value['training']['downloaded_bytes'], 321)
        self.assertTrue(value['busy'])

    def test_gpu_stage(self):
        self.job['stage'] = '학습 one'
        self.save(self.root / 'work/jobs/known_7.json', self.job)
        self.assertEqual(self.status()['training']['phase'], 'GPU 학습')

    def test_no_past_test_metrics(self):
        self.save(self.old / 'work/training/final.json', {'test': {'operating': {'precision': .99}}})
        self.assertIsNone(self.status()['metrics']['precision'])
        self.assertEqual(len(self.status()['training']['runs']), 2)
        self.assertEqual(self.status()['training']['runs'][0]['history'], [])

    def test_final_metrics_only_round7(self):
        self.save(self.root / 'work/training/final.json', {'test': {'operating': {'precision': .4, 'recall': .5}, 'metrics': {'AP50': .6}}})
        self.assertEqual(self.status()['metrics']['map50'], .6)

    def test_utc_date_rollover_to_korea(self):
        self.assertEqual(pipeline.kst(57600), '1970-01-02 01:00:00 한국 시각 (Asia/Seoul)')

    def test_stale_is_not_failure(self):
        value = self.status(500)
        self.assertTrue(value['training']['stale'])
        self.assertEqual(value['training']['state'], 'running')
        self.assertFalse(value['training']['live_process_verified'])

    def test_failed_state_preserved(self):
        self.job.update(state='failed', error='원문 실패')
        self.save(self.root / 'work/jobs/known_7.json', self.job)
        self.assertFalse(self.status()['busy'])
        self.assertEqual(self.status()['training']['error'], '원문 실패')

    def test_missing_job(self):
        (self.root / 'work/jobs/known_7.json').unlink()
        self.assertIsNone(self.status()['training']['observed_kst'])
        self.assertTrue(self.status()['training']['stale'])

    def test_busy_never_calls_worker(self):
        with patch.object(pipeline, 'status', return_value={'busy': True}), patch.object(pipeline.legacy, 'docker_call') as call:
            with self.assertRaisesRegex(ValueError, '이미 진행'):
                pipeline.action('train', {'resume': True})
            call.assert_not_called()

    def test_explicit_start_uses_guarded_original_worker(self):
        with patch.object(pipeline, 'status', return_value={'busy': False}), patch.object(pipeline.legacy, 'docker_call', return_value={}) as call:
            pipeline.action('train', {'resume': False})
            self.assertEqual(call.call_args.args[0][0], '/workspace/2026/월요일 PBL/7차/worker.py')

    def test_train_rejects_non_boolean_and_extra_fields(self):
        for value in ({'resume': 1}, {'resume': False, 'force': True}):
            with self.assertRaises(ValueError):
                pipeline.action('train', value)

    def test_log_allowlist_and_utf8_bounded_tail(self):
        app = dashboard.Dashboard(dashboard.ROOT, 'test', self.old, self.root)
        path = self.root / 'work/jobs/known_7.log'
        path.write_text('한글\n' * 20000, encoding='utf-8')
        value = app.log('round7/jobs/known_7.log')
        self.assertTrue(value['truncated'])
        self.assertLessEqual(value['captured_bytes'], 65536)
        for name in ('round7/jobs/../known_7.log', 'round7/jobs/unknown.log', 'round7/jobs/known_7.json'):
            with self.assertRaises(ValueError):
                app.log(name)

    def test_video_boundary_does_not_expand_to_round7(self):
        app = dashboard.Dashboard(dashboard.ROOT, 'test', self.old, self.root)
        secret = self.root / 'work/jobs/known_7.json'
        with self.assertRaises(ValueError):
            app.confined(str(secret), ('uploads', 'results'))
        self.assertEqual(app.work, (self.old / 'work').resolve())
        self.assertEqual(app.root, dashboard.ROOT)

    def test_preserved_detect_result_maps_container_to_windows(self):
        remote = '/workspace/2026/월요일 PBL/5차/work/results/saved/result.mp4'
        self.save(self.old / 'work/jobs/saved.json',
                  {'id': 'saved', 'kind': 'detect', 'state': 'complete', 'created': 1, 'result': remote})
        result = next(row for row in self.status()['jobs'] if row['kind'] == 'detect')
        expected = str(Path('D:/2026') / '월요일 PBL/5차/work/results/saved/result.mp4')
        self.assertEqual(result['result'], expected)
        self.assertFalse(result['result'].startswith('/workspace/'))

    def test_two_real_histories(self):
        path = self.root / 'work/training/runs/one/results.csv'
        path.parent.mkdir(parents=True)
        path.write_text('epoch,metrics/precision(B),metrics/recall(B),metrics/mAP50(B)\n1,0.2,0.3,0.4\n', encoding='utf-8')
        runs = self.status()['training']['runs']
        self.assertEqual(runs[0]['history'][0]['precision'], .2)
        self.assertEqual(runs[1]['history'], [])


class HttpBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = dashboard.create_server(token='unit-token')
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, method, path, headers=None, body=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            return response.status, response.read()
        finally:
            connection.close()

    def test_token_required(self):
        self.assertEqual(self.request('GET', '/api/status')[0], 403)

    def test_host_required(self):
        self.assertEqual(self.request('GET', '/api/health?token=unit-token', {'Host': 'evil.example'})[0], 403)

    def test_csrf_and_origin_required(self):
        self.assertEqual(self.request('POST', '/api/train', {'X-Token': 'unit-token', 'Content-Type': 'application/json'}, '{}')[0], 403)

    def test_static_root_is_original_layout_round8(self):
        code, body = self.request('GET', '/?token=unit-token')
        self.assertEqual(code, 200)
        self.assertIn('8차'.encode(), body)
        self.assertIn(b'id="videos"', body)

    def test_arbitrary_file_route_not_served(self):
        self.assertEqual(self.request('GET', '/pipeline.py?token=unit-token')[0], 404)

    def test_asset_path_confined(self):
        self.assertEqual(self.request('GET', '/asset?token=unit-token&path=../pipeline.py')[0], 400)

    def test_confined_result_video_range_is_playable(self):
        # 임시 결과 파일도 실제 HTTP 핸들러와 경로 검증을 거쳐 범위 응답을 확인합니다.
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary) / 'work'
            result = work / 'results/saved/result.mp4'
            result.parent.mkdir(parents=True)
            result.write_bytes(b'0123456789')
            with patch.object(self.server.app, 'work', work):
                code, body = self.request('GET', '/asset?token=unit-token&path=' + quote(str(result)),
                                          {'Range': 'bytes=2-5'})
                self.assertEqual(code, 206)
                self.assertEqual(body, b'2345')
                outside = Path(temporary) / 'outside.mp4'
                outside.write_bytes(b'private')
                code, _ = self.request('GET', '/asset?token=unit-token&path=' + quote(str(outside)),
                                       {'Range': 'bytes=0-2'})
                self.assertEqual(code, 400)

    def test_upload_limit_preserved(self):
        headers = {'X-Token': 'unit-token', 'X-CSRF-Token': 'unit-token',
                   'Origin': 'http://127.0.0.1:' + str(self.server.server_port), 'Content-Length': str(4 * 1024**3 + 1)}
        self.assertEqual(self.request('POST', '/api/upload', headers)[0], 400)


if __name__ == '__main__':
    unittest.main()
