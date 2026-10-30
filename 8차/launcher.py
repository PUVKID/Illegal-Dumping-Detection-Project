"""독립 대시보드 실행기입니다. 학습은 자동 시작하지 않습니다."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import http.client
import webbrowser

from dashboard import ROOT, create_server


def health(port, query):
    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=3)
    try:
        connection.request('GET', '/api/health?' + query)
        response = connection.getresponse()
        if response.status != 200:
            raise ValueError('루프백 상태 검사에 실패했습니다.')
        return json.loads(response.read(4096).decode('utf-8'))
    finally:
        connection.close()


def session_health(root=ROOT):
    path = Path(root) / 'work' / 'session.json'
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
        from urllib.parse import urlsplit
        url = urlsplit(value['url'])
        if url.scheme != 'http' or url.hostname != '127.0.0.1' or not url.port:
            return None
        result = health(url.port, url.query)
        if result.get('ok') and result['data'].get('service') == 'cleanview-dashboard':
            return value
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return None


def main():
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    if '--pipeline' in sys.argv:
        sys.argv.remove('--pipeline')
        import pipeline
        pipeline.main()
        return
    parser = argparse.ArgumentParser(description='클린뷰 독립 대시보드')
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--hidden', action='store_true')
    args = parser.parse_args()
    if args.hidden and not args.self_test:
        argv = ([sys.executable] if getattr(sys, 'frozen', False) else
                [sys.executable, '-B', '-X', 'utf8', str(ROOT / 'launcher.py')]) + ['--port', str(args.port)]
        if args.no_browser:
            argv.append('--no-browser')
        (ROOT / 'work').mkdir(exist_ok=True)
        with (ROOT / 'work' / 'dashboard.log').open('ab') as log:
            child = subprocess.Popen(argv, cwd=str(ROOT), stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                     shell=False, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        print(json.dumps({'pid': child.pid, 'session': str(ROOT / 'work' / 'session.json')}, ensure_ascii=False))
        return
    if not args.self_test:
        existing = session_health()
        if existing:
            if not args.no_browser:
                webbrowser.open(existing['url'])
            print(json.dumps({'reused': True, 'pid': existing['pid']}, ensure_ascii=False))
            return
    server = create_server(port=args.port)
    url = f'http://127.0.0.1:{server.server_port}/?token={server.app.token}'
    if args.self_test:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            print(json.dumps(health(server.server_port, 'token=' + server.app.token), ensure_ascii=False))
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        return
    session = ROOT / 'work' / 'session.json'
    temporary = session.with_suffix('.tmp')
    temporary.write_text(json.dumps({'url': url, 'pid': os.getpid()}, ensure_ascii=False), encoding='utf-8')
    temporary.replace(session)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if session.exists() and json.loads(session.read_text(encoding='utf-8')).get('pid') == os.getpid():
            session.unlink()


if __name__ == '__main__':
    main()
