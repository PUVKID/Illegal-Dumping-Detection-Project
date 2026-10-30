"""원래 루프백 HTTP 보안과 영상 저장 경계를 유지하는 8차 서버입니다."""
from pathlib import Path
import re
import secrets
from http.server import ThreadingHTTPServer
import pipeline

ROOT = Path(__file__).resolve().parent
original = pipeline.load_module('cleanview_round5_dashboard', pipeline.PREVIOUS / 'dashboard.py')


class Dashboard(original.Dashboard):
    def __init__(self, root, token, previous=pipeline.PREVIOUS, training=pipeline.TRAINING_ROOT):
        super().__init__(previous, token)
        # 영상 작업 경계는 5차 work에 고정하고 화면 소스만 8차로 분리합니다.
        self.root = Path(root).resolve()
        self.training_root = Path(training).resolve()

    def pipeline(self, action, params):
        return pipeline.action(action, params)

    def log(self, value):
        if isinstance(value, str) and value.startswith('round7/'):
            match = re.fullmatch(r'round7/jobs/([A-Za-z0-9_-]{1,100})\.log', value)
            if not match:
                raise ValueError('7차 로그는 등록된 작업 ID만 허용합니다.')
            job = match.group(1)
            records = pipeline.job_records(self.training_root / 'work')
            if not any(row['id'] == job for row in records):
                raise ValueError('등록되지 않은 작업 로그입니다.')
            base = (self.training_root / 'work/jobs').resolve()
            path = (base / (job + '.log')).resolve()
            if path.parent != base or not path.is_file():
                raise ValueError('허용되지 않은 작업 로그입니다.')
            size = path.stat().st_size
            with path.open('rb') as stream:
                stream.seek(max(0, size - original.LOG_LIMIT))
                raw = stream.read(original.LOG_LIMIT)
            if size > original.LOG_LIMIT:
                while raw and raw[0] & 0xC0 == 0x80:
                    raw = raw[1:]
            return {'text': raw.decode('utf-8'), 'original_bytes': size,
                    'captured_bytes': len(raw), 'truncated': size > len(raw)}
        return super().log(value)


Handler = original.Handler


def create_server(root=ROOT, port=0, token=None):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.app = Dashboard(root, token or secrets.token_urlsafe(32))
    # 실행 세션은 8차에만 기록하며 5차 원본 세션은 덮어쓰지 않습니다.
    (Path(root) / 'work').mkdir(exist_ok=True)
    return server
