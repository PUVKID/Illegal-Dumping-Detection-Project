"""공식 원자료를 보존하고 별도 정규화 사본·고정 분할을 준비합니다."""
import argparse
import collections
import email.utils
import errno
import hashlib
import http.client
import io
import json
import math
import os
import re
import shutil
import socket
import ssl
import stat
import time
import urllib.error
import urllib.request
import uuid
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
SOURCES = WORK / 'sources'
TRAINING = WORK / 'training'
ARCHIVE = ROOT.parent / '이전 도커 실험/3차실험/trash_round3'
PREVIOUS = ROOT.parent / '5차/work/training'
SEED = 20261030
MAX_BYTES = 100 * 1024**3
MINIMUM_FREE = 100 * 1024**3
NORMALIZATION = 'rgb-jpeg-quality95-subsampling0-no-exif-no-rotation-v1'
SOURCE_FILES = [
    {'source':'pLitterStreet','record':'8288500','name':'images.zip','size':13728630001,
     'md5':'02382a3b9620ae7b086ff4c7fd11891d'},
    {'source':'pLitterStreet','record':'8288500','name':'annotations.zip','size':8764662,
     'md5':'2484e076b1e9d66036b0a15e9928692f'},
    {'source':'PlastOPol','record':'5829156','name':'PlastOpol_oneclass.zip','size':7709841780,
     'md5':'b5648f444ae79a9566adf23f0786e402'},
    {'source':'UAVVaste','record':'8214061','name':'UAVVasteDataset.zip','size':3010727259,
     'md5':'1575c32c04bdf944047563e4a1786c2a'},
]
for _source in SOURCE_FILES:
    _source['url'] = 'https://zenodo.org/api/records/'+_source['record']+'/files/'+_source['name']+'/content'
    _source['license'] = 'CC-BY-4.0'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2)+'\n', encoding='utf-8')
    temporary.replace(path)


def sha256_file(path):
    return digest_file(path, 'sha256')


def digest_file(path, algorithm):
    digest = hashlib.new(algorithm)
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            digest.update(block)
    return digest.hexdigest()


def freeze(path, value):
    path = Path(path)
    if path.exists():
        if load(path) != value:
            raise ValueError('고정 계약이 변경됐습니다: '+str(path))
    else:
        atomic_json(path, value)


def local(path):
    text = str(path)
    if os.name == 'nt' and text.startswith('/workspace/2026/'):
        return Path('D:/2026') / text.removeprefix('/workspace/2026/')
    if text.startswith('/root/환경 PBL/trash_round3/'):
        return ARCHIVE / text.removeprefix('/root/환경 PBL/trash_round3/')
    return Path(path)


def portable(path):
    text = Path(path).resolve().as_posix()
    return '/workspace/2026/'+text[8:] if text.startswith('D:/2026/') else text


def validate_yolo(text):
    rows = []
    for line in text.split('\n'):
        if not line.strip():
            continue
        row = list(map(float, line.split()))
        if len(row) != 5 or row[0] != 0 or not all(map(math.isfinite, row)):
            raise ValueError('단일 trash 클래스와 유한한 좌표가 필요합니다.')
        _, x, y, width, height = row
        tolerance = 1e-7
        if width <= 0 or height <= 0 or not (-tolerance <= x-width/2 and x+width/2 <= 1+tolerance
                                          and -tolerance <= y-height/2 and y+height/2 <= 1+tolerance):
            raise ValueError('라벨이 이미지 경계를 벗어났습니다.')
        rows.append([0, x, y, width, height])
    return rows


def coco_labels(image, annotations, mapping):
    width, height = float(image['width']), float(image['height'])
    if not all(math.isfinite(x) and x > 0 for x in (width, height)):
        raise ValueError('COCO 이미지 크기가 잘못됐습니다.')
    rows = []
    for annotation in annotations:
        category = annotation['category_id']
        if category not in mapping:
            raise ValueError('명세에 없는 클래스입니다: '+str(category))
        if mapping[category] is None:
            continue
        x, y, w, h = map(float, annotation['bbox'])
        if not all(map(math.isfinite, (x,y,w,h))) or w <= 0 or h <= 0:
            raise ValueError('COCO 상자가 잘못됐습니다.')
        tolerance = 1e-5
        if x < -tolerance or y < -tolerance or x+w > width+tolerance or y+h > height+tolerance:
            raise ValueError('COCO 상자가 이미지 범위를 벗어났습니다.')
        rows.append([0, (x+w/2)/width, (y+h/2)/height, w/width, h/height])
    return validate_yolo('\n'.join(' '.join(map(str,r)) for r in rows))


def fingerprint(image):
    import numpy as np
    pixels = np.asarray(image.convert('L').resize((32,32)), dtype=float)
    basis = np.cos(np.pi*(2*np.arange(32)+1)[None,:]*np.arange(8)[:,None]/64)
    values = (basis @ pixels @ basis.T).flatten()
    middle = float(np.median(values[1:]))
    return f'{sum(int(v > middle) << i for i,v in enumerate(values)):016x}'


def normalize_image(source, target, expected_size, reserve):
    from PIL import Image
    source, target = Path(source), Path(target)
    if source.resolve() == target.resolve():
        raise ValueError('원본을 정규화 결과로 덮어쓸 수 없습니다.')
    raw_hash = sha256_file(source)
    receipt = target.with_suffix('.normalization.json')
    if target.exists() and receipt.exists():
        result = load(receipt)
        if result['raw_sha256'] != raw_hash or result['normalization'] != NORMALIZATION or result['sha256'] != sha256_file(target):
            raise ValueError('정규화 사본의 보존 계약이 다릅니다.')
        if (result['width'],result['height']) != tuple(expected_size):
            raise ValueError('정규화 사본과 주석 크기가 다릅니다.')
        return result
    if target.exists():
        raise ValueError('출처 대응이 없는 기존 정규화 사본입니다.')
    with Image.open(source) as original:
        original.verify()
    with Image.open(source) as original:
        original.load()
        if original.size != tuple(expected_size) or original.width*original.height > 100000000:
            raise ValueError('해독한 원본 크기와 주석 좌표계가 다릅니다.')
        orientation = original.getexif().get(274,1)
        # 주석은 저장 픽셀 좌표입니다. 픽셀을 돌리지 않고 EXIF만 제거합니다.
        image = original.convert('RGB')
        image.info.clear()
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=95, subsampling=0, exif=b'')
        encoded = output.getvalue()
        if not encoded.endswith(b'\xff\xd9'):
            raise ValueError('정규화 JPEG의 종료 표식이 없습니다.')
        reserve(len(encoded)+4096)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.part')
        temporary.write_bytes(encoded)
        temporary.replace(target)
        result = {'raw_sha256':raw_hash, 'sha256':hashlib.sha256(encoded).hexdigest(),
                  'width':image.width,'height':image.height,'signature':fingerprint(image),
                  'bytes':len(encoded),'raw_orientation':orientation,'normalization':NORMALIZATION}
    atomic_json(receipt,result)
    return result


class DownloadBudget:
    def __init__(self, root, limit=MAX_BYTES, minimum_free=MINIMUM_FREE, notify=lambda **kw:None):
        self.root = Path(root)
        self.root.mkdir(parents=True,exist_ok=True)
        self.path = self.root/'download_ledger.json'
        self.limit, self.minimum_free, self.notify = min(int(limit),MAX_BYTES), int(minimum_free), notify
        saved = load(self.path) if self.path.exists() else {}
        self.used = int(saved.get('download_bytes',0))
        self.imports = saved.get('imports',{})
        if self.used < 0 or self.used > self.limit:
            raise ValueError('기존 전송량이 7차 예산과 맞지 않습니다.')

    def space(self, count):
        free = shutil.disk_usage(self.root).free
        if count < 0 or free-count < self.minimum_free:
            raise ValueError('쓰기 후 잔여 공간 100GiB를 보장할 수 없습니다.')

    def charge(self, count):
        if count < 0 or self.used+count > self.limit:
            raise ValueError('7차 누적 전송 예산을 초과했습니다.')
        self.used += count
        atomic_json(self.path,{'download_bytes':self.used,'limit_bytes':self.limit,'imports':self.imports})
        self.notify(download_bytes=self.used,download_limit_bytes=self.limit)

    def import_prefetch(self, path):
        path = Path(path)
        if not path.exists():
            return
        identity = portable(path)
        value = {'sha256':sha256_file(path),'bytes':int(load(path)['download_bytes'])}
        if identity in self.imports:
            if self.imports[identity] != value:
                raise ValueError('이미 합산한 사전 전송 영수증이 변경됐습니다.')
            return
        if value['bytes'] < 0 or self.used+value['bytes'] > self.limit:
            raise ValueError('사전 전송을 합치면 7차 전송 예산을 초과합니다.')
        self.imports[identity] = value
        self.charge(value['bytes'])


def open_request(url, headers=None):
    if not url.startswith('https://') and not url.startswith('http://127.0.0.1:'):
        raise ValueError('공식 HTTPS 출처만 허용됩니다.')
    request = urllib.request.Request(url, headers={'User-Agent':'CleanView7 research preparation',**(headers or {})})
    return urllib.request.urlopen(request,timeout=40)


class _DownloadRetry(Exception):
    """통신 경계에서 확인한 일시 오류만 재시도 경로로 전달합니다."""
    def __init__(self, error):
        super().__init__(str(error))
        self.error = error


def _temporary_download_error(error):
    if isinstance(error,urllib.error.HTTPError):
        return error.code==429 or 500<=error.code<=599
    if isinstance(error,urllib.error.URLError):
        return _temporary_download_error(error.reason)
    if isinstance(error,(TimeoutError,ConnectionError,http.client.IncompleteRead,ssl.SSLEOFError)):
        return True
    if isinstance(error,socket.gaierror):
        return error.errno==socket.EAI_AGAIN
    return isinstance(error,OSError) and error.errno in {
        errno.ETIMEDOUT,errno.ECONNRESET,errno.ECONNABORTED,errno.ECONNREFUSED,
        errno.EPIPE,errno.ENETUNREACH,errno.EHOSTUNREACH,
    }


def _download_retry_delay(error, attempt):
    delay = min(60,2**(attempt+1))
    if isinstance(error,urllib.error.HTTPError):
        value = error.headers.get('Retry-After','').strip()
        try:
            if re.fullmatch(r'[0-9]+',value):
                requested = float(value)
            else:
                requested = email.utils.parsedate_to_datetime(value).timestamp()-time.time()
            delay = min(60,max(delay,requested))
        except (ValueError,TypeError,OverflowError):
            pass
    return delay


def download(spec, target, budget):
    from worker import file_lock
    target=Path(target)
    lock=target.with_name(target.name+'.receiving.lock')
    deadline=time.monotonic()+12*3600
    # 실제 수신은 모두 같은 Linux Docker의 flock으로 조정합니다.
    while True:
        guard=file_lock(lock,blocking=False)
        try:
            guard.__enter__()
            break
        except RuntimeError:
            if time.monotonic()>=deadline:raise TimeoutError('공식 자료 수신 잠금 대기 12시간을 초과했습니다.')
            budget.notify(stage='사전 공식자료 수신 완료 대기',file=target.name)
            time.sleep(15)
    try:
        if target.name=='images.zip' and target.parent.resolve()==(SOURCES/'downloads').resolve():
            prefetch=WORK/'prefetch'
            state=load(prefetch/'status.json') if (prefetch/'status.json').exists() else {}
            if state.get('state')=='running':
                raise ValueError('수신 잠금은 풀렸지만 사전 수신 상태가 running입니다. 원인을 확인해야 합니다.')
            budget.import_prefetch(prefetch/'download_ledger.json')
            if state.get('state')=='complete':
                receipt=load(prefetch/'complete.json')
                if (any(state.get(key)!=value for key,value in receipt.items())
                        or receipt['expected_bytes']!=spec['size'] or receipt['md5']!=spec['md5']
                        or receipt['url']!=spec['url'] or local(receipt['path']).resolve()!=target.resolve()
                        or int(load(prefetch/'download_ledger.json')['download_bytes'])!=receipt['download_bytes']):
                    raise ValueError('사전 수신 최종 영수증과 공식 원자료 계약이 다릅니다.')
                if not target.exists() or sha256_file(target)!=receipt['sha256']:
                    raise ValueError('사전 수신 SHA와 완성 원자료가 다릅니다.')
        return _download(spec,target,budget)
    finally:
        guard.__exit__(None,None,None)


def _download(spec, target, budget):
    target = Path(target)
    target.parent.mkdir(parents=True,exist_ok=True)
    identity = {k:spec[k] for k in ('url','size','md5')}
    if target.exists():
        if target.stat().st_size != spec['size'] or digest_file(target,'md5') != spec['md5']:
            raise ValueError('공식 크기·MD5와 기존 원자료가 다릅니다: '+target.name)
        freeze(target.with_suffix(target.suffix+'.verified.json'),{**identity,'sha256':sha256_file(target)})
        return target
    partial = target.with_suffix(target.suffix+'.part')
    metadata = target.with_suffix(target.suffix+'.part.json')
    if partial.exists():
        if not metadata.exists():
            raise ValueError('출처 없는 부분 다운로드입니다.')
        old = load(metadata)
        if old.get('url') != identity['url'] or old.get('size') != identity['size'] or old.get('md5',identity['md5']) != identity['md5']:
            raise ValueError('부분 다운로드의 원자료 계약이 다릅니다.')
    start = partial.stat().st_size if partial.exists() else 0
    if start > spec['size']:
        raise ValueError('부분 파일 크기가 원본보다 큽니다.')
    budget.space(spec['size']-start+8192)
    atomic_json(metadata,identity)
    while start < spec['size']:
        end = min(spec['size'],start+4*1024*1024)-1
        for attempt in range(7):
            # 실패 때 닫힌 스트림의 실제 저장량을 다시 확인하고 같은 범위의 나머지만 받습니다.
            saved = partial.stat().st_size if partial.exists() else 0
            if saved!=start or load(metadata)!=identity:
                raise ValueError('재시도 전 부분 파일 크기·원자료 계약이 변경됐습니다.')
            remaining = end-start+1
            if not remaining:break
            if budget.used+remaining > budget.limit:
                raise ValueError('남은 전송 예산이 부족합니다.')
            deadline = time.monotonic()+40
            try:
                try:
                    response = open_request(spec['url'],{'Range':f'bytes={start}-{end}'})
                except (OSError,http.client.HTTPException) as error:
                    if isinstance(error,urllib.error.HTTPError):error.close()
                    if _temporary_download_error(error):raise _DownloadRetry(error) from error
                    raise
                with response:
                    if response.status != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{spec["size"]}':
                        raise ValueError('서버가 원본 범위 요청을 보존하지 않았습니다.')
                    with partial.open('ab') as stream:
                        while remaining:
                            if time.monotonic() > deadline:
                                raise _DownloadRetry(TimeoutError('개별 범위 요청 40초를 초과했습니다.'))
                            budget.space(min(256*1024,remaining)+8192)
                            interrupted = None
                            try:
                                # 한 번에 반환 가능한 본문을 받아 timeout 직전의 일부 수신도 보존합니다.
                                block = response.read1(min(256*1024,remaining))
                            except http.client.IncompleteRead as error:
                                block,interrupted = error.partial,error
                            except (OSError,http.client.HTTPException) as error:
                                if _temporary_download_error(error):raise _DownloadRetry(error) from error
                                raise
                            if not block:
                                raise _DownloadRetry(interrupted or EOFError('부분 전송이 중간에 끊겼습니다.'))
                            budget.charge(len(block))
                            if len(block)>remaining:
                                raise ValueError('수신 본문이 요청한 원본 범위를 초과했습니다.')
                            budget.space(len(block)+8192)
                            stream.write(block)
                            remaining -= len(block)
                            start += len(block)
                            if interrupted:raise _DownloadRetry(interrupted) from interrupted
                break
            except _DownloadRetry as failure:
                saved = partial.stat().st_size if partial.exists() else 0
                if saved!=start or load(metadata)!=identity:
                    raise ValueError('실패 수신 후 부분 파일 크기·원자료 계약이 변경됐습니다.') from failure
                reason = type(failure.error).__name__+': '+str(failure.error)
                if attempt==6:
                    budget.notify(stage='공식 원자료 수신 재시도 한도 초과: '+reason,
                                  source=spec.get('source'),file=target.name,downloaded_bytes=start,
                                  file_bytes=spec['size'],retry_reason=reason,retry_attempt=6,retry_limit=6)
                    raise failure.error from failure
                delay = _download_retry_delay(failure.error,attempt)
                budget.notify(stage=f'공식 원자료 수신 재시도 {attempt+1}/6: '+reason,
                              source=spec.get('source'),file=target.name,downloaded_bytes=start,
                              file_bytes=spec['size'],retry_reason=reason,retry_attempt=attempt+1,
                              retry_limit=6,retry_wait_seconds=delay)
                time.sleep(delay)
        budget.notify(stage='공식 원자료 다운로드',source=spec.get('source'),file=target.name,
                      downloaded_bytes=start,file_bytes=spec['size'],retry_reason=None,retry_attempt=0,retry_wait_seconds=0)
    if partial.stat().st_size != spec['size'] or digest_file(partial,'md5') != spec['md5']:
        raise ValueError('완성 원자료의 공식 MD5가 일치하지 않습니다.')
    partial.replace(target)
    freeze(target.with_suffix(target.suffix+'.verified.json'),{**identity,'sha256':sha256_file(target)})
    return target


def extract_zip(archive, destination, reserve):
    destination = Path(destination)
    if destination.is_symlink() or getattr(destination,'is_junction',lambda:False)():
        raise ValueError('ZIP 추출 시작 위치가 파일 링크입니다.')
    destination.mkdir(parents=True,exist_ok=True)
    boundary=destination.resolve()
    with zipfile.ZipFile(archive) as zipped:
        for info in zipped.infolist():
            path = PurePosixPath(info.filename.replace('\\','/'))
            if path.is_absolute() or '..' in path.parts or ':' in info.filename or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('ZIP에 허용하지 않는 경로가 있습니다.')
            if info.is_dir():
                continue
            target = destination.joinpath(*path.parts)
            for existing in [target,*target.parents]:
                if existing==destination.parent:break
                if existing.is_symlink() or getattr(existing,'is_junction',lambda:False)():
                    raise ValueError('ZIP 추출 경로에 기존 파일 링크가 있습니다.')
            if not target.resolve().is_relative_to(boundary):
                raise ValueError('ZIP 추출 경로가 원본 보관 폴더를 벗어납니다.')
            if target.exists():
                crc = 0
                with target.open('rb') as stream:
                    for block in iter(lambda:stream.read(1024*1024),b''):
                        crc = zlib.crc32(block,crc)
                if target.stat().st_size != info.file_size or crc != info.CRC:
                    raise ValueError('기존 ZIP 추출 원본이 변경됐습니다: '+info.filename)
                continue
            reserve(info.file_size+4096)
            target.parent.mkdir(parents=True,exist_ok=True)
            temporary = target.with_suffix(target.suffix+'.part')
            if temporary.is_symlink() or not temporary.resolve().is_relative_to(boundary):
                raise ValueError('ZIP 임시 파일이 허용 경로를 벗어납니다.')
            with zipped.open(info) as source, temporary.open('wb') as out:
                shutil.copyfileobj(source,out,1024*1024)
            if temporary.stat().st_size != info.file_size:
                raise ValueError('ZIP 추출 크기가 다릅니다.')
            temporary.replace(target)


def components(records, distance=4):
    ordered = sorted(records,key=lambda r:r['id'])
    parents = list(range(len(ordered)))
    def find(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index
    def union(left,right):
        a,b = find(left),find(right)
        parents[max(a,b)] = min(a,b)
    hashes, groups, urls, segments = {}, {}, {}, collections.defaultdict(list)
    signatures = []
    # 거리 4 이하는 다섯 비트 구간 중 적어도 한 구간이 같습니다.
    shifts = [(0,13),(13,13),(26,13),(39,13),(52,12)]
    for index,row in enumerate(ordered):
        for lookup,key in ((hashes,row.get('sha256')),(groups,row.get('group')),(urls,row.get('original_url') or None)):
            if key is not None:
                if key in lookup:union(index,lookup[key])
                else:lookup[key]=index
        signature = int(row['signature'],16) if row.get('signature') else None
        signatures.append(signature)
        if signature is None:continue
        candidates = set()
        for shift,bits in shifts:
            candidates.update(segments[(shift,(signature >> shift)&((1<<bits)-1))])
        for previous in candidates:
            if (signature ^ signatures[previous]).bit_count() <= distance:
                union(index,previous)
        for shift,bits in shifts:
            segments[(shift,(signature >> shift)&((1<<bits)-1))].append(index)
    return {row['id']:ordered[find(index)]['id'] for index,row in enumerate(ordered)}


def protect_splits(records):
    mapping = components(records)
    buckets = collections.defaultdict(list)
    for row in records:buckets[mapping[row['id']]].append(row)
    kept,rejected = [],[]
    for identity,rows in sorted(buckets.items()):
        seen = any(r.get('previously_used') or r['split'] in ('seen','historical_val','historical_test') for r in rows)
        legacy_holdout = any(r['split'] in ('historical_val','historical_test') for r in rows)
        new = [r for r in rows if r['split'] in ('val','test','external_test')]
        for row in rows:
            if row['split'] == 'seen':
                continue
            if seen and row in new:
                rejected.append({**row,'reason':'과거 사용 사진과 동일·근접 그룹'})
            elif legacy_holdout and row['split']=='train':
                rejected.append({**row,'reason':'과거 고정 평가와 동일·근접 그룹'})
            else:
                destination = row['split']
                if not seen and destination=='train' and new:
                    destination = max((r['split'] for r in new),key=lambda s:{'val':1,'test':2,'external_test':3}[s])
                elif not seen and destination in ('val','test') and any(r['split']=='external_test' for r in new):
                    destination='external_test'
                elif not seen and destination=='val' and any(r['split']=='test' for r in new):
                    destination='test'
                kept.append({**row,'split':destination,'component':identity})
    unique=[]
    used_hashes={}
    for row in sorted(kept,key=lambda r:(0 if r['split'] in ('historical_val','historical_test') else 1,r['id'])):
        digest=row['sha256']
        if digest in used_hashes and row['split'] not in ('historical_val','historical_test'):
            rejected.append({**row,'reason':'동일 원본 바이트 중복','duplicate_of':used_hashes[digest]})
        else:
            unique.append(row)
            used_hashes[digest]=row['id']
    return sorted(unique,key=lambda r:r['id']),rejected


def crop_labels(parent, labels, rectangle):
    if parent['split'] != 'train':
        raise ValueError('crop 증강은 train 부모에서만 생성합니다.')
    left,top,right,bottom = rectangle
    if not (0 <= left < right <= parent['width'] and 0 <= top < bottom <= parent['height']):
        raise ValueError('crop 영역이 부모 이미지 범위를 벗어났습니다.')
    result=[]
    for _,x,y,w,h in labels:
        x1,y1=(x-w/2)*parent['width'],(y-h/2)*parent['height']
        x2,y2=(x+w/2)*parent['width'],(y+h/2)*parent['height']
        a,b,c,d=max(left,x1),max(top,y1),min(right,x2),min(bottom,y2)
        if c <= a or d <= b:continue
        # 경계에서 일부만 남은 객체를 배경으로 오학습하지 않도록 crop 자체를 제외합니다.
        if (c-a)*(d-b)/(w*h*parent['width']*parent['height']) < .9:return None
        if min(c-a,d-b)<2:return None
        result.append([0,((a+c)/2-left)/(right-left),((b+d)/2-top)/(bottom-top),
                       (c-a)/(right-left),(d-b)/(bottom-top)])
    return result


def balanced_paths(records):
    pools = collections.defaultdict(list)
    for row in records:
        if row['split']=='train':pools[row['source']].append(row['image'])
    biggest = max(map(len,pools.values()),default=0)
    paths=[]
    for source,values in sorted(pools.items()):
        repeats = min(4,max(1,math.ceil(biggest*.3/len(values))))
        paths.extend(sorted(values)*repeats)
    return paths


def write_labels(path, rows):
    text=''.join(' '.join(f'{v:.10g}' for v in row)+'\n' for row in rows)
    validate_yolo(text)
    path=Path(path)
    if path.exists() and path.read_text(encoding='utf-8')!=text:
        raise ValueError('기존 학습 라벨이 새 변환과 다릅니다.')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')


def verify_records(records, include_raw=True):
    for row in records:
        for key,hash_key in [('image','sha256'),('label','label_sha256')]+([('raw_image','raw_sha256')] if include_raw else []):
            if sha256_file(local(row[key])) != row[hash_key]:
                raise ValueError('고정 파일 해시가 다릅니다: '+row['id']+' '+key)


def historical_protection(old_additional, records):
    from PIL import Image
    ghosts=[]
    known={r['raw_sha256'] for r in records if r['source']=='TACO'}
    for index,row in enumerate(old_additional):
        if row['source']=='pLitterStreet':continue
        path=local(row['image'])
        ghost={'id':'prior_additional_'+str(index),'group':'prior_additional:'+str(index),
               'sha256':row['sha256'],'split':'seen','source':row['source'],'previously_used':True,
               'original_url':row.get('url'),'available':path.exists()}
        if path.exists():
            if sha256_file(path)!=row['sha256']:raise ValueError('과거 추가 자료가 보존 manifest와 다릅니다.')
            with Image.open(path) as image:
                image.load();ghost['signature']=fingerprint(image)
            ghost['raw_image']=portable(path)
        ghosts.append(ghost)
    for path in sorted((ARCHIVE/'data/full/images/train').glob('*')):
        if not path.is_file():continue
        digest=sha256_file(path)
        if digest in known:continue
        with Image.open(path) as image:
            image.load();signature=fingerprint(image)
        ghosts.append({'id':'prior_original_'+path.stem,'group':'taco:'+path.stem,'sha256':digest,
                       'signature':signature,'split':'seen','source':'TACO earlier train',
                       'previously_used':True,'available':True,'raw_image':portable(path)})
    return ghosts


def verify_history(manifest):
    path=TRAINING/'historical_protection.json'
    if sha256_file(path)!=manifest['historical_protection_sha256']:
        raise ValueError('과거 사용 자료 보호 명세가 바뀌었습니다.')
    for row in load(path):
        if row.get('available') and sha256_file(local(row['raw_image']))!=row['sha256']:
            raise ValueError('추가로 대조한 과거 사용 원본이 바뀌었습니다.')


def make_record(raw, identity, source, split, group, rows, size, budget, **extra):
    image=TRAINING/'data/images'/split/(identity+'.jpg')
    label=TRAINING/'data/labels'/split/(identity+'.txt')
    result=normalize_image(raw,image,size,budget.space)
    budget.space(8192)
    write_labels(label,rows)
    return {**result,'id':identity,'source':source,'split':split,'group':group,
            'image':portable(image),'label':portable(label),'label_sha256':sha256_file(label),
            'raw_image':portable(raw),'boxes':len(rows),**extra}


def indexed_images(directory):
    names=collections.defaultdict(list)
    for path in sorted(Path(directory).rglob('*')):
        if path.is_file() and path.suffix.lower() in ('.jpg','.jpeg','.png'):
            names[path.name].append(path)
    return names


def find_image(index, image):
    choices=index.get(image['file_name'],[])
    suffix=str(image.get('path','')).removeprefix('/datasets/')
    exact=[p for p in choices if suffix and p.as_posix().endswith(suffix)]
    if len(exact)==1:return exact[0]
    if len(choices)==1:return choices[0]
    raise ValueError('원본 이미지를 유일하게 식별할 수 없습니다: '+image['file_name'])


def add_crops(records, budget, notify):
    from PIL import Image
    eligible=collections.defaultdict(list)
    for row in records:
        if row['split']!='train':continue
        labels=validate_yolo(local(row['label']).read_text(encoding='utf-8'))
        small=[r for r in labels if r[3]*r[4]*row['width']*row['height']*(1280/max(row['width'],row['height']))**2 < 32**2]
        if small:eligible[row['source']].append((row,labels,small[0]))
    cap=max(1,sum(r['split']=='train' for r in records)//10//max(1,len(eligible)))
    crops=[]
    for source,pool in sorted(eligible.items()):
        pool.sort(key=lambda item:hashlib.sha256(item[0]['id'].encode()).hexdigest())
        for row,labels,focus in pool[:cap]:
            width,height=row['width'],row['height']
            side=min(768,width,height)
            x,y=focus[1]*width,focus[2]*height
            left,top=max(0,min(width-side,int(x-side/2))),max(0,min(height-side,int(y-side/2)))
            rectangle=(left,top,left+side,top+side)
            cropped=crop_labels(row,labels,rectangle)
            if not cropped:continue
            target=TRAINING/'data/images/train'/(row['id']+'_crop.jpg')
            raw=TRAINING/'crop_intermediates'/(row['id']+'.png')
            raw.parent.mkdir(parents=True,exist_ok=True)
            budget.space(side*side*4+8192)
            if not raw.exists():
                with Image.open(local(row['image'])) as image:image.crop(rectangle).save(raw)
            crop=make_record(raw,row['id']+'_crop',source,'train',row['group'],cropped,(side,side),budget,
                             parent_id=row['id'],parent_split='train',crop=list(rectangle),augmentation=True)
            crops.append(crop)
        notify(stage='학습 전용 작은 객체 crop',crops=len(crops))
    return crops


def prepare(notify=lambda **kw:None):
    if os.name!='posix':
        raise ValueError('실제 자료 준비는 동일 Docker2026/Linux 안에서 실행해야 합니다.')
    TRAINING.mkdir(parents=True,exist_ok=True)
    contract={'source_files':SOURCE_FILES,'normalization':NORMALIZATION,'seed':SEED,
              'preparation_sha256':sha256_file(__file__),'previous_manifest_sha256':sha256_file(PREVIOUS/'data_manifest.json'),
              'config_sha256':sha256_file(ROOT/'configs/training.json'),
              'protected_sources_sha256':sha256_file(ROOT/'configs/protected_sources.json'),
              'prior_additional_manifest_sha256':sha256_file(ARCHIVE/'sources/additional_manifest.json')}
    freeze(TRAINING/'preparation_contract.json',contract)
    manifest_path=TRAINING/'data_manifest.json'
    if manifest_path.exists():
        manifest=load(manifest_path)
        if manifest['contract']!=contract:raise ValueError('준비된 데이터 계약이 다릅니다.')
        notify(stage='고정 원본·정규화·라벨 해시 재검사')
        verify_records(manifest['records'])
        verify_history(manifest)
        return manifest
    budget=DownloadBudget(SOURCES,notify=notify)
    budget.import_prefetch(WORK/'preflight/download_ledger.json')
    freeze(SOURCES/'source_contract.json',{'files':SOURCE_FILES,'license_evidence':'evidence/공식데이터출처.json'})
    for spec in SOURCE_FILES:
        notify(stage='공식 원자료 MD5 검사·재개 수신',source=spec['source'],file=spec['name'])
        archive=download(spec,SOURCES/'downloads'/spec['name'],budget)
        notify(stage='공식 ZIP CRC 검사·원본 추출',source=spec['source'])
        extract_zip(archive,SOURCES/'raw'/spec['source'],budget.space)
    plast=SOURCES/'raw/PlastOPol'
    extract_zip(plast/'images.zip',plast/'images',budget.space)
    extract_zip(plast/'plastopol-annotations_folds.zip',plast/'annotations',budget.space)
    records=[]
    previous=load(PREVIOUS/'data_manifest.json')
    previous_ids=set()
    for row in previous['records']:
        if row['source']=='pLitterStreet':previous_ids.add(str(row['source_id']))
        if row['source']!='TACO preserved':continue
        raw,label=local(row['image']),local(row['label'])
        if sha256_file(raw)!=row['sha256'] or sha256_file(label)!=row['label_sha256']:
            raise ValueError('보존 TACO 원본·라벨 계약과 다릅니다.')
        split={'val':'historical_val','test':'historical_test','train':'train'}[row['split']]
        records.append(make_record(raw,row['id'],'TACO',split,row['group'],validate_yolo(label.read_text(encoding='utf-8')),
                                   (row['width'],row['height']),budget,previously_used=True))
        if len(records)%100==0:notify(stage='TACO 원본 보존 사본 준비',prepared=len(records))
    old_additional=load(ARCHIVE/'sources/additional_manifest.json')
    for row in old_additional:
        if row['source']=='pLitterStreet':
            match=re.search(r'street_(\d+)',row['image'])
            if not match:raise ValueError('과거 pLitter 원본 ID를 확인할 수 없습니다.')
            previous_ids.add(match.group(1))
    pannotation=next(p for p in (SOURCES/'raw/pLitterStreet').rglob('annotations_all.json') if p.as_posix().endswith('10_class_splits/annotations_all.json'))
    sources=[('pLitterStreet',load(pannotation),SOURCES/'raw/pLitterStreet',{i:(None if i==4 else 0) for i in range(1,11)}),
             ('PlastOPol',load(plast/'annotations/annotations/full_plastopol.json'),plast/'images',{1:0}),
             ('UAVVaste',load(SOURCES/'raw/UAVVaste/annotations/annotations.json'),SOURCES/'raw/UAVVaste/images',{0:0})]
    plast_test={r['file_name'] for r in load(plast/'annotations/annotations/plastopol_test.json')['images']}
    plast_val={r['file_name'] for r in load(plast/'annotations/annotations/plastopol_val_fold-1.json')['images']}
    for source,annotation,directory,mapping in sources:
        by_id=collections.defaultdict(list)
        for item in annotation['annotations']:by_id[item['image_id']].append(item)
        index=indexed_images(directory)
        for image in sorted(annotation['images'],key=lambda r:str(r['id'])):
            raw=find_image(index,image)
            split='external_test' if source=='UAVVaste' else 'test' if source=='PlastOPol' and image['file_name'] in plast_test else 'val' if source=='PlastOPol' and image['file_name'] in plast_val else 'train'
            group=source+':'+str(image['id'])
            if source=='pLitterStreet':
                path=str(image.get('path',image['file_name'])).removeprefix('/datasets/')
                group='pLitterStreet:'+path.split('/')[0]
            if source=='UAVVaste':group='UAVVaste:entire-source-held-out'
            labels=coco_labels(image,by_id[image['id']],mapping)
            records.append(make_record(raw,source.lower()+'_'+str(image['id']),source,split,group,labels,
                                       (image['width'],image['height']),budget,source_id=str(image['id']),license='CC-BY-4.0',
                                       url=next(s['url'] for s in SOURCE_FILES if s['source']==source),
                                       original_url=image.get('flickr_url') or image.get('coco_url'),
                                       previously_used=source=='pLitterStreet' and str(image['id']) in previous_ids))
            if len(records)%100==0:notify(stage='원본 대응 정규화·좌표 검증',source=source,prepared=len(records))
    # 없어진 과거 사진은 해시·URL 대조만 가능하므로 근접 중복 완전 검증이라고 부르지 않습니다.
    ghosts=historical_protection(old_additional,records)
    freeze(TRAINING/'historical_protection.json',ghosts)
    raw_for_matching=[{**r,'sha256':r['raw_sha256']} for r in records]
    accepted,rejected=protect_splits(raw_for_matching+ghosts)
    original={r['id']:r for r in records}
    records=[{**original[r['id']],'split':r['split'],'component':r['component']} for r in accepted]
    counts=collections.Counter(r['split'] for r in records)
    groups={s:len({r['component'] for r in records if r['split']==s}) for s in counts}
    for split,minimum in [('train',5000),('val',100),('test',100),('external_test',100),('historical_val',150),('historical_test',150)]:
        if counts[split]<minimum:raise ValueError('누출 배제 뒤 평가·학습 최소 수가 부족합니다: '+split)
    if groups['val']<3 or groups['test']<3:
        raise ValueError('PlastOPol 검증·테스트의 독립 이미지 그룹이 부족합니다.')
    crops=add_crops(records,budget,notify)
    records+=crops
    train_paths=balanced_paths(records)
    for split in ['train','historical_val','historical_test','val','test','external_test']:
        paths=train_paths if split=='train' else [r['image'] for r in records if r['split']==split]
        budget.space(sum(len(p.encode('utf-8'))+1 for p in paths)+4096)
        (TRAINING/(split+'.txt')).write_text(''.join(p+'\n' for p in paths),encoding='utf-8',newline='\n')
    atomic_json(TRAINING/'dataset.yaml',{'train':portable(TRAINING/'train.txt'),'val':portable(TRAINING/'historical_val.txt'),'names':{'0':'trash'}})
    summary={'original_images':len(records)-len(crops),'crops':len(crops),'training_exposures':len(train_paths),
             'splits':dict(collections.Counter(r['split'] for r in records)),
             'source_originals':dict(collections.Counter(r['source'] for r in records if not r.get('augmentation'))),
             'split_components':groups,'excluded':len(rejected),'missing_prior_photos':sum(not r['available'] for r in ghosts),
             'additional_prior_available_photos':sum(r['available'] for r in ghosts),
             'restored_pLitter_ids':sum(r['source']=='pLitterStreet' and r.get('previously_used',False) and not r.get('augmentation') for r in records),
             'new_pLitter_ids':sum(r['source']=='pLitterStreet' and not r.get('previously_used',False) and not r.get('augmentation') for r in records)}
    summary['unique_original_sha256']=len({r['raw_sha256'] for r in records if not r.get('augmentation')})
    manifest={'schema':1,'contract':contract,'records':records,'counts':summary,'created':time.time(),
              'historical_protection_sha256':sha256_file(TRAINING/'historical_protection.json'),
              'near_duplicate':'64-bit DCT perceptual hash distance <=4; transitive components; source groups joined',
              'limits':['PlastOPol official split is image-level; capture location independence unknown',
                        'UAVVaste source-held-out aerial auxiliary test; not CCTV equivalent',
                        'missing prior photos only SHA/URL auditable; no absolute historic near-duplicate guarantee',
                        'TACO test is a previously evaluated historical benchmark'],
              'class_mapping':{'pLitterStreet':sources[0][3],'PlastOPol':{1:0},'UAVVaste':{0:0},'name':'trash'}}
    freeze(TRAINING/'excluded.json',rejected)
    freeze(manifest_path,manifest)
    notify(stage='대규모 데이터 고정 완료',**summary,download_bytes=budget.used)
    return manifest


def smoke():
    previous=load(PREVIOUS/'data_manifest.json')
    row=next(r for r in previous['records'] if r['source']=='TACO preserved' and r['split']=='train')
    raw,label=local(row['image']),local(row['label'])
    before=sha256_file(raw)
    if before!=row['sha256'] or sha256_file(label)!=row['label_sha256']:
        raise ValueError('smoke 원본이 보존 계약과 다릅니다.')
    budget=DownloadBudget(WORK/'smoke')
    target=WORK/'smoke'/('normalized_'+raw.name)
    result=normalize_image(raw,target,(row['width'],row['height']),budget.space)
    labels=validate_yolo(label.read_text(encoding='utf-8'))
    if sha256_file(raw)!=before:raise ValueError('smoke에서 원본이 변경됐습니다.')
    report={'source_id':row['id'],'raw_sha256':before,'normalized_sha256':result['sha256'],
            'width':result['width'],'height':result['height'],'boxes':len(labels),
            'network_bytes':0,'source_unchanged':True,'normalization':NORMALIZATION}
    atomic_json(WORK/'smoke/result.json',report)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='공식 데이터 준비')
    parser.add_argument('--prepare',action='store_true')
    parser.add_argument('--smoke',action='store_true')
    args=parser.parse_args()
    if args.smoke:print(json.dumps(smoke(),ensure_ascii=False))
    elif args.prepare:prepare(notify=lambda **kw:print(json.dumps(kw,ensure_ascii=False),flush=True))
    else:parser.error('실제 수신·변환에는 --prepare, 한 장 검사에는 --smoke가 필요합니다.')
