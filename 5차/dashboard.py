"""Codex와 독립 실행되는 루프백 전용 대시보드입니다."""
import json
import mimetypes
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

LOG_LIMIT = 64 * 1024
MAX_UPLOAD = 4 * 1024**3
VIDEO_EXT = {'.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm'}
ROOT = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent


class Dashboard:
    def __init__(self, root, token):
        self.root = Path(root).resolve()
        self.work = self.root / 'work'
        self.token = token
        for name in ('uploads', 'results', 'logs'):
            (self.work / name).mkdir(parents=True, exist_ok=True)

    def pipeline(self, action, params):
        argv = ([sys.executable, '--pipeline'] if getattr(sys, 'frozen', False) else
                [sys.executable, '-B', '-X', 'utf8', str(self.root / 'pipeline.py')])
        argv += ['--action', action, '--params', json.dumps(params, ensure_ascii=False)]
        # 출력은 임시 파일로 받아 메모리에 무제한 누적하지 않습니다.
        with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
            result = subprocess.run(argv, cwd=str(self.root), shell=False, stdout=output,
                                    stderr=errors, timeout=15 if action == 'status' else 60,
                                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            output.seek(0, 2)
            size = output.tell()
            if size > 2 * 1024**2:
                raise RuntimeError('파이프라인 JSON 응답이 2MB 상한을 넘었습니다.')
            output.seek(0)
            raw = output.read()
            errors.seek(0, 2)
            errors.seek(max(0, errors.tell() - LOG_LIMIT))
            error = errors.read().decode('utf-8', errors='replace')
        try:
            value = json.loads(raw.decode('utf-8'))
        except (ValueError, UnicodeError) as exc:
            raise RuntimeError('파이프라인 JSON 응답이 잘못되었습니다. ' + error[-2000:]) from exc
        if not isinstance(value, dict) or not isinstance(value.get('ok'), bool):
            raise RuntimeError('파이프라인 JSON 응답 형식이 잘못되었습니다.')
        if result.returncode or not value['ok']:
            raise RuntimeError(str(value.get('error') or error or f'종료 코드 {result.returncode}'))
        return value.get('data')

    def confined(self, value, areas):
        if not isinstance(value, str) or not value:
            raise ValueError('파일 경로가 필요합니다.')
        path = Path(value)
        if not path.is_absolute():
            path = self.work / path
        path = path.resolve()
        if not any(path.is_relative_to((self.work / area).resolve()) for area in areas):
            raise ValueError('허용된 작업 폴더 밖의 경로입니다.')
        if not path.is_file():
            raise ValueError('파일이 없습니다.')
        return path

    def log(self, value):
        path = self.confined(value, ('logs', 'results', 'jobs', 'training'))
        if path.suffix.lower() not in ('.log', '.txt'):
            raise ValueError('로그 파일만 읽을 수 있습니다.')
        size = path.stat().st_size
        with path.open('rb') as stream:
            stream.seek(max(0, size - LOG_LIMIT))
            raw = stream.read(LOG_LIMIT)
        # 잘린 첫 UTF-8 문자만 제거하고 원본의 잘못된 바이트는 오류로 알립니다.
        if size > LOG_LIMIT:
            while raw and raw[0] & 0xC0 == 0x80:
                raw = raw[1:]
        text = raw.decode('utf-8')
        return {'text': text, 'original_bytes': size, 'captured_bytes': len(raw),
                'truncated': size > len(raw)}


class Handler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(60)

    def log_message(self, *_):
        pass

    def reply(self, value, status=200, content_type='application/json; charset=utf-8'):
        raw = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' blob:; media-src 'self' blob:; font-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(raw)

    def authorized(self, mutation=False):
        expected = f'127.0.0.1:{self.server.server_port}'
        if self.headers.get('Host') != expected:
            return False
        query = parse_qs(urlsplit(self.path).query)
        token = self.headers.get('X-Token') or query.get('token', [''])[0]
        if not secrets.compare_digest(token, self.server.app.token):
            return False
        if mutation:
            if not secrets.compare_digest(self.headers.get('X-CSRF-Token', ''), self.server.app.token):
                return False
            if self.headers.get('Origin') != f'http://{expected}':
                return False
        return True

    def sendfile(self, path):
        size = path.stat().st_size
        start, end, status = 0, size - 1, 200
        requested = self.headers.get('Range')
        if requested:
            try:
                if not requested.startswith('bytes=') or ',' in requested:
                    raise ValueError()
                first, last = requested[6:].split('-')
                if first:
                    start = int(first)
                    end = min(size - 1, int(last)) if last else size - 1
                else:
                    length = int(last)
                    if length <= 0:
                        raise ValueError()
                    start = max(0, size - length)
                if start < 0 or start > end or start >= size:
                    raise ValueError()
                status = 206
            except ValueError:
                self.reply({'ok': False, 'error': '유효하지 않은 파일 범위입니다.'}, 416)
                return
        self.send_response(status)
        self.send_header('Content-Type', mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(max(0, end - start + 1)))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Cache-Control', 'no-store')
        if status == 206:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        with path.open('rb') as stream:
            stream.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk = stream.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def do_GET(self):
        if not self.authorized():
            self.reply({'ok': False, 'error': '로컬 접속 토큰이 필요합니다.'}, 403)
            return
        url = urlsplit(self.path)
        query = parse_qs(url.query)
        try:
            if url.path == '/api/health':
                self.reply({'ok': True, 'data': {'service': 'cleanview-dashboard', 'pid': os.getpid()}})
            elif url.path in ('/api/status', '/api/videos'):
                self.reply({'ok': True, 'data': self.server.app.pipeline(url.path.rsplit('/', 1)[1], {})})
            elif url.path == '/api/log':
                self.reply({'ok': True, 'data': self.server.app.log(query.get('path', [''])[0])})
            elif url.path == '/asset':
                self.sendfile(self.server.app.confined(query.get('path', [''])[0], ('uploads', 'results')))
            elif url.path in ('/', '/app.js', '/style.css', '/fonts/NanumGothic-Bold.ttf'):
                name = 'index.html' if url.path == '/' else url.path[1:]
                path = self.server.app.root / 'web' / name
                if name in ('index.html', 'style.css'):
                    content = path.read_text(encoding='utf-8')
                    for asset in ('/style.css', '/app.js', '/fonts/NanumGothic-Bold.ttf'):
                        content = content.replace(asset, asset + '?token=' + self.server.app.token)
                    self.reply(content.encode('utf-8'), content_type='text/html; charset=utf-8' if name == 'index.html' else 'text/css; charset=utf-8')
                else:
                    self.sendfile(path)
            else:
                self.reply({'ok': False, 'error': '없는 주소입니다.'}, 404)
        except (ValueError, OSError, UnicodeError) as exc:
            self.reply({'ok': False, 'error': str(exc)}, 400)
        except (RuntimeError, subprocess.SubprocessError) as exc:
            self.reply({'ok': False, 'error': str(exc)}, 502)

    def do_POST(self):
        if not self.authorized(mutation=True):
            self.reply({'ok': False, 'error': '토큰·요청 출처를 확인해 주세요.'}, 403)
            return
        try:
            if self.headers.get('Transfer-Encoding'):
                raise ValueError('Content-Length가 있는 요청만 허용합니다.')
            length = int(self.headers.get('Content-Length', '0'))
            route = urlsplit(self.path).path
            if route == '/api/upload':
                if not 0 < length <= MAX_UPLOAD:
                    raise ValueError('영상은 0 초과 4GB 이하만 업로드할 수 있습니다.')
                suffix = Path(unquote(self.headers.get('X-Filename', ''))).suffix.lower()
                if suffix not in VIDEO_EXT:
                    raise ValueError('지원하지 않는 영상 확장자입니다.')
                destination = self.server.app.work / 'uploads' / (uuid.uuid4().hex + suffix)
                try:
                    with destination.open('xb') as output:
                        remaining = length
                        while remaining:
                            chunk = self.rfile.read(min(1024 * 1024, remaining))
                            if not chunk:
                                raise ValueError('영상 업로드가 중단되었습니다.')
                            output.write(chunk)
                            remaining -= len(chunk)
                except Exception:
                    destination.unlink(missing_ok=True)
                    raise
                self.reply({'ok': True, 'data': {'path': str(destination), 'name': destination.name}})
                return
            if not 0 < length <= 64 * 1024:
                raise ValueError('JSON 요청은 64KB 이하이어야 합니다.')
            params = json.loads(self.rfile.read(length).decode('utf-8'))
            if not isinstance(params, dict):
                raise ValueError('JSON 객체가 필요합니다.')
            if route not in ('/api/probe', '/api/detect', '/api/train'):
                self.reply({'ok': False, 'error': '없는 주소입니다.'}, 404)
                return
            self.reply({'ok': True, 'data': self.server.app.pipeline(route.rsplit('/', 1)[1], params)})
        except (ValueError, OSError, UnicodeError) as exc:
            self.reply({'ok': False, 'error': str(exc)}, 400)
        except (RuntimeError, subprocess.SubprocessError) as exc:
            self.reply({'ok': False, 'error': str(exc)}, 502)


def create_server(root=ROOT, port=0, token=None):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.app = Dashboard(root, token or secrets.token_urlsafe(32))
    return server
