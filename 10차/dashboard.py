"""8차 인증·영상 경계를 상속하고 명시한 로컬 3D 모듈만 제공합니다."""
from http.server import ThreadingHTTPServer
from pathlib import Path
import secrets
from urllib.parse import urlsplit
import pipeline

ROOT = Path(__file__).resolve().parent
round8 = pipeline.load_module('cleanview_round8_dashboard', ROOT.parent / '8차/dashboard.py')
original = round8.original
Dashboard = round8.Dashboard
ASSETS = {'/assets/brand-leaf.png': 'image/png', **{'/icons/' + name + '.svg': 'image/svg+xml' for name in ('flask-conical', 'video', 'chart-no-axes-column', 'notebook-text', 'refresh-cw', 'cpu', 'clock-3', 'chevrons-right')}}
MODULES = {'/scene.js', '/presentation.js', '/vendor/three.module.js', '/vendor/three.core.js'}


class Handler(round8.Handler):
    def reply(self, value, status=200, content_type='application/json; charset=utf-8'):
        if isinstance(value, bytes) and content_type.startswith('text/html'):
            text = value.decode('utf-8')
            for asset in ASSETS:
                text = text.replace('"' + asset + '"', '"' + asset + '?token=' + self.server.app.token + '"')
            value = text.encode('utf-8')
        return super().reply(value, status, content_type)

    def do_GET(self):
        route = urlsplit(self.path).path
        if route not in MODULES and route not in ASSETS:
            return super().do_GET()
        if not self.authorized():
            return self.reply({'ok': False, 'error': '로컬 접속 토큰이 필요합니다.'}, 403)
        try:
            if route in ASSETS:
                return self.reply((self.server.app.root / 'web' / route[1:]).read_bytes(), content_type=ASSETS[route])
            content = (self.server.app.root / 'web' / route[1:]).read_text(encoding='utf-8')
            # 모듈의 상대 의존 요청도 동일 토큰 검사에 결합합니다.
            for dependency in ('./vendor/three.module.js', './three.core.js'):
                content = content.replace("'" + dependency + "'", "'" + dependency + '?token=' + self.server.app.token + "'")
            return self.reply(content.encode('utf-8'), content_type='text/javascript; charset=utf-8')
        except (OSError, UnicodeError) as error:
            return self.reply({'ok': False, 'error': str(error)}, 400)


def create_server(root=ROOT, port=0, token=None):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.app = Dashboard(root, token or secrets.token_urlsafe(32))
    (Path(root) / 'work').mkdir(exist_ok=True)
    return server
