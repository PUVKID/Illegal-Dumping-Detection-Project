
import json,os,select,sys,ctypes,struct
from pathlib import Path
p=Path(sys.argv[1]);job=sys.argv[2]
libc=ctypes.CDLL(None,use_errno=True)
fd=libc.inotify_init1(os.O_CLOEXEC)
if fd<0:raise OSError(ctypes.get_errno(),'inotify_init1')
wd=libc.inotify_add_watch(fd,os.fsencode(p.parent),0x80)
if wd<0:raise OSError(ctypes.get_errno(),'inotify_add_watch')
state=json.loads(p.read_text());pidfd=None
if state.get('state') in ('running','queued'):
    try:
        pidfd=os.pidfd_open(int(state['pid']))
        cmd=(Path('/proc')/str(state['pid'])/'cmdline').read_bytes()
        if job.encode() not in cmd or b'backend.py' not in cmd:raise RuntimeError('Worker PID mismatch')
    except (ProcessLookupError,FileNotFoundError):pidfd=None
print('READY',flush=True)
events=select.poll();events.register(fd,select.POLLIN)
if pidfd is not None:events.register(pidfd,select.POLLIN)
while state.get('state') in ('queued','running') and pidfd is not None:
    ready=events.poll()  # OS events only: no timer, periodic queries, or AI calls.
    exited=any(n==pidfd for n,mask in ready)
    if exited:state=json.loads(p.read_text());break
    raw=os.read(fd,65536);offset=0
    while offset<len(raw):
        wd,mask,cookie,length=struct.unpack_from('iIII',raw,offset)
        name=raw[offset+16:offset+16+length].split(bytes([0]),1)[0];offset+=16+length
        if name==os.fsencode(p.name):state=json.loads(p.read_text())
if pidfd is not None:os.close(pidfd)
os.close(fd)
print(json.dumps(state,ensure_ascii=False),flush=True)
