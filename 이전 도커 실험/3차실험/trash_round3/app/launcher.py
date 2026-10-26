"""Windows executable: local UI + Docker GPU worker (no Python install needed)."""
import os, sys, json, subprocess, tempfile, threading, webbrowser, secrets, time
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs, unquote

CONTAINER='2026-2'
REMOTE='/root/환경 PBL/trash_round3/app'
ASSETS=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))
TOKEN=secrets.token_urlsafe(32)
CACHE=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'TrashDetector3'
CACHE.mkdir(parents=True,exist_ok=True)
DOCKER='docker'
FLAGS=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0

def run(args, timeout=120):
    try:
        p=subprocess.run([DOCKER,*args],capture_output=True,creationflags=FLAGS,timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise RuntimeError('Docker가 응답하지 않습니다. Docker Desktop과 2026-2 컨테이너의 실행 상태를 확인하세요.') from e
    if p.returncode: raise RuntimeError(p.stderr.decode('utf-8',errors='replace')[-2500:] or p.stdout.decode('utf-8',errors='replace')[-2500:])
    return p.stdout

def api(command,args=None):
    raw=run(['exec',CONTAINER,'python',REMOTE+'/backend.py',command,json.dumps(args or {},ensure_ascii=False)],20 if command=='status' else 120)
    value=json.loads(raw.decode('utf-8'))
    if not value['ok']: raise RuntimeError(value['error'])
    return value['data']

def initialize():
    global DOCKER
    import shutil
    if not shutil.which(DOCKER):
        candidate=Path(os.environ.get('ProgramFiles','C:/Program Files'))/'Docker/Docker/resources/bin/docker.exe'
        if candidate.exists(): DOCKER=str(candidate)
        else: raise RuntimeError('Docker Desktop을 설치하고 2026-2 컨테이너를 준비하세요.')
    running=run(['inspect',CONTAINER,'--format','{{.State.Running}}']).decode().strip()
    if running!='true': run(['start',CONTAINER])
    run(['exec',CONTAINER,'mkdir','-p',REMOTE])
    for filename in ['backend.py','detector.py','inference.py','data_pipeline.py','train_round3.py']:
        run(['cp',str(ASSETS/filename),CONTAINER+':'+REMOTE+'/'+filename])
    run(['cp',str(ASSETS/'fonts'),CONTAINER+':'+REMOTE+'/'])
    run(['exec',CONTAINER,'python','-c','import ultralytics, cv2, yaml, requests, imageio_ffmpeg'])

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*_): pass
    def reply(self,obj,status=200):
        b=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def authorized(self):
        u=urlsplit(self.path); q=parse_qs(u.query)
        return secrets.compare_digest(self.headers.get('X-Token','') or q.get('token',[''])[0],TOKEN)
    def asset(self,remote):
        # Only generated results can be copied from the container.
        from pathlib import PurePosixPath
        p=PurePosixPath(remote)
        if '..' in p.parts or not p.is_relative_to(PurePosixPath(REMOTE+'/results')): raise ValueError('잘못된 결과 경로')
        import hashlib
        dest=CACHE/(hashlib.sha256(remote.encode()).hexdigest()+p.suffix)
        if not dest.exists(): run(['cp',CONTAINER+':'+remote,str(dest)])
        return dest
    def sendfile(self,p):
        import mimetypes
        size=p.stat().st_size; start=0; end=size-1; code=200
        range_header=self.headers.get('Range')
        if range_header:
            try:
                bounds=range_header.removeprefix('bytes=').split('-')
                start=int(bounds[0] or 0); end=min(size-1,int(bounds[1]) if bounds[1] else size-1)
                if start<0 or start>end: raise ValueError()
                code=206
            except (ValueError,IndexError): self.send_error(416); return
        self.send_response(code); self.send_header('Content-Type',mimetypes.guess_type(p.name)[0] or 'application/octet-stream')
        self.send_header('Accept-Ranges','bytes'); self.send_header('Content-Length',str(end-start+1))
        if code==206: self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.end_headers()
        try:
            with p.open('rb') as f:
                f.seek(start); left=end-start+1
                while left:
                    chunk=f.read(min(left,1024*1024))
                    if not chunk: break
                    self.wfile.write(chunk); left-=len(chunk)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError): pass
    def do_GET(self):
        u=urlsplit(self.path); q=parse_qs(u.query)
        if not self.authorized(): self.reply({'error':'접근 토큰이 필요합니다.'},403); return
        try:
            if u.path=='/':
                b=(ASSETS/'index.html').read_bytes().replace(b'__TOKEN__',TOKEN.encode())
                self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8')
                self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
            elif u.path=='/font': self.sendfile(ASSETS/'fonts'/'NanumGothic-Bold.ttf')
            elif u.path=='/api/status': self.reply(api('status'))
            elif u.path=='/api/videos': self.reply(api('videos'))
            elif u.path=='/api/log': self.reply(api('log',{'job':q['job'][0]}))
            elif u.path=='/asset': self.sendfile(self.asset(q['path'][0]))
            else: self.send_error(404)
        except Exception as e: self.reply({'error':str(e)},400)
    def do_POST(self):
        if not self.authorized(): self.reply({'error':'접근 토큰이 필요합니다.'},403); return
        try:
            u=urlsplit(self.path); length=int(self.headers.get('Content-Length','0'))
            if u.path=='/api/upload':
                name=Path(unquote(self.headers.get('X-Filename','video.mp4'))).name
                ext=Path(name).suffix.lower()
                if ext not in {'.mp4','.avi','.mov','.mkv','.m4v'}: raise ValueError('지원하지 않는 영상 확장자')
                if not 0<length<=4*1024**3: raise ValueError('파일 크기는 0 초과 4GB 이하이어야 합니다.')
                with tempfile.TemporaryDirectory(dir=CACHE) as td:
                    p=Path(td)/('upload_'+secrets.token_hex(5)+ext)
                    with p.open('wb') as f:
                        remaining=length
                        while remaining:
                            chunk=self.rfile.read(min(1024*1024,remaining))
                            if not chunk: raise ValueError('영상 업로드가 중단되었습니다.')
                            f.write(chunk); remaining-=len(chunk)
                    remote=REMOTE+'/uploads/'+p.name
                    run(['cp',str(p),CONTAINER+':'+remote],timeout=600)
                self.reply({'path':remote,'name':name}); return
            if not 0<length<1024*1024: raise ValueError('잘못된 요청 크기')
            data=json.loads(self.rfile.read(length))
            if u.path=='/api/probe': self.reply(api('probe',data))
            elif u.path=='/api/start': self.reply(api('start',data))
            elif u.path=='/api/quit':
                self.reply({'ok':True}); threading.Thread(target=self.server.shutdown,daemon=True).start()
            else: self.send_error(404)
        except Exception as e: self.reply({'error':str(e)},400)

def main():
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--no-browser',action='store_true'); parser.add_argument('--port',type=int,default=0)
    parser.add_argument('--self-test',action='store_true'); args=parser.parse_args()
    try:
        initialize()
        if args.self_test:
            result={'status':api('status'),'videos':api('videos')}
            (CACHE/'self-test.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8'); return
        server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
        url=f'http://127.0.0.1:{server.server_port}/?token={TOKEN}'
        (CACHE/'session.json').write_text(json.dumps({'url':url,'pid':os.getpid()}),encoding='utf-8')
        if not args.no_browser: webbrowser.open(url)
        server.serve_forever(); server.server_close()
    except Exception:
        import traceback
        error=traceback.format_exc(); (CACHE/'error.log').write_text(error,encoding='utf-8')
        if os.name=='nt' and not args.no_browser and not args.self_test:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0,'시작하지 못했습니다. Docker Desktop과 2026-2 컨테이너를 확인하세요.\n\n'+error[-1800:],'CCTV 쓰레기 탐지',16)
        sys.exit(1)

if __name__=='__main__': main()
