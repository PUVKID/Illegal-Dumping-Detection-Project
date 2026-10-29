"""실제 HTTP 경계와 파이프라인 오류 전달을 검사합니다."""
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import dashboard


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.server = dashboard.create_server(self.root, token='test-token')
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def request(self, path, method='GET', body=None, auth=True, **headers):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        if auth:
            headers.update({'X-Token': 'test-token'})
        if method == 'POST':
            headers.setdefault('X-CSRF-Token', 'test-token')
            headers.setdefault('Origin', f'http://127.0.0.1:{self.server.server_port}')
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        result = (response.status, response.read(), dict(response.getheaders()))
        connection.close()
        return result

    def test_no_auth(self):
        self.assertEqual(self.request('/api/status', auth=False)[0], 403)

    def test_missing_file(self):
        self.assertEqual(self.request('/asset?path=uploads/missing.mp4')[0], 400)

    def test_upload_extension_and_size(self):
        self.assertEqual(self.request('/api/upload', 'POST', b'content', **{'X-Filename': 'unsafe.html'})[0], 400)
        self.assertEqual(self.request('/api/upload', 'POST', b'x', **{'X-Filename': 'x.mp4', 'Content-Length': str(dashboard.MAX_UPLOAD + 1)})[0], 400)
        self.assertEqual(list((self.root / 'work/uploads').iterdir()), [])

    def test_host_boundary(self):
        self.assertEqual(self.request('/api/health', Host='evil.example')[0], 403)

    def test_origin_and_csrf(self):
        self.assertEqual(self.request('/api/train', 'POST', b'{}', Origin='https://evil.example')[0], 403)
        self.assertEqual(self.request('/api/train', 'POST', b'{}', **{'X-CSRF-Token': 'bad'})[0], 403)

    def test_bad_json(self):
        self.assertEqual(self.request('/api/train', 'POST', b'{')[0], 400)
        self.assertEqual(self.request('/api/train', 'POST', b'[]')[0], 400)

    def test_traversal(self):
        secret = self.root / 'secret.txt'
        secret.write_text('private', encoding='utf-8')
        self.assertEqual(self.request('/asset?path=../secret.txt')[0], 400)
        self.assertEqual(self.request('/asset?path=' + str(secret))[0], 400)

    def test_upload_preserves_original(self):
        original = self.root / 'original.mp4'
        original.write_bytes(b'original')
        status, raw, _ = self.request('/api/upload', 'POST', b'new-video', **{'X-Filename': '../../original.mp4'})
        self.assertEqual(status, 200)
        data = json.loads(raw)['data']
        self.assertEqual(Path(data['path']).read_bytes(), b'new-video')
        self.assertEqual(original.read_bytes(), b'original')
        self.assertEqual(Path(data['path']).parent, self.root / 'work' / 'uploads')

    def test_pipeline_error_and_duplicate(self):
        with patch.object(self.server.app, 'pipeline', side_effect=RuntimeError('이미 학습 중입니다.')):
            status, raw, _ = self.request('/api/train', 'POST', b'{}')
        self.assertEqual(status, 502)
        self.assertIn('이미 학습 중', json.loads(raw)['error'])

    def test_log_limit_and_utf8(self):
        log = self.root / 'work' / 'logs' / 'train.log'
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text('가' * 100000, encoding='utf-8')
        status, raw, _ = self.request('/api/log?path=logs/train.log')
        data = json.loads(raw)['data']
        self.assertEqual(status, 200)
        self.assertTrue(data['truncated'])
        self.assertLessEqual(data['captured_bytes'], dashboard.LOG_LIMIT)
        self.assertNotIn('\ufffd', data['text'])

    def test_range_and_health(self):
        video = self.root / 'work' / 'uploads' / 'x.mp4'
        video.write_bytes(b'0123456789')
        status, raw, headers = self.request('/asset?path=uploads/x.mp4', Range='bytes=2-5')
        self.assertEqual((status, raw), (206, b'2345'))
        self.assertEqual(headers['Content-Range'], 'bytes 2-5/10')
        self.assertEqual(self.request('/api/health')[0], 200)

    def test_pipeline_argv_and_invalid_response(self):
        with patch('dashboard.subprocess.run') as run:
            run.return_value.returncode = 0
            def response(*args, **kwargs):
                kwargs['stdout'].write(b'{"ok":true,"data":{"jobs":[]}}')
                return run.return_value
            run.side_effect = response
            self.assertEqual(self.server.app.pipeline('status', {}), {'jobs': []})
            self.assertFalse(run.call_args.kwargs['shell'])
            self.assertEqual(run.call_args.args[0][-4:], ['--action', 'status', '--params', '{}'])
            def invalid(*args, **kwargs):
                kwargs['stdout'].write(b'not json')
                return run.return_value
            run.side_effect = invalid
            with self.assertRaisesRegex(RuntimeError, 'JSON'):
                self.server.app.pipeline('status', {})


if __name__ == '__main__':
    unittest.main()
