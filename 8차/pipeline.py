"""5차 영상 파이프라인을 보존하며 7차 상태만 읽는 8차 어댑터입니다."""
import csv
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import math
from pathlib import Path
import re
import time

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / '5차'
TRAINING_ROOT = ROOT.parent / '7차'
ACTIVE = {'running', 'queued', 'starting'}
KST = timezone(timedelta(hours=9), 'Asia/Seoul')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


legacy = load_module('cleanview_round5_pipeline', PREVIOUS / 'pipeline.py')


def read(path, default=None):
    try:
        value = json.loads(Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError:
        return default
    return value


def kst(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        return None
    return datetime.fromtimestamp(value, KST).strftime('%Y-%m-%d %H:%M:%S') + ' 한국 시각 (Asia/Seoul)'


def job_records(work):
    values = []
    for path in (work / 'jobs').glob('*.json'):
        value = read(path)
        if not isinstance(value, dict) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value.get('id', '')) or path.stem != value['id']:
            raise ValueError('작업 기록 ID와 파일명이 일치하지 않습니다.')
        values.append(value)
    return sorted(values, key=lambda row: row.get('created', 0), reverse=True)


def histories(work, candidates):
    result = []
    for candidate in candidates:
        name = candidate['name']
        if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
            raise ValueError('학습 후보 이름이 잘못됐습니다.')
        path = work / 'training/runs' / name / 'results.csv'
        rows = []
        if path.is_file():
            with path.open(encoding='utf-8', newline='') as stream:
                for raw in csv.DictReader(stream):
                    raw = {key.strip(): value for key, value in raw.items()}
                    row = {'epoch': int(float(raw['epoch']))}
                    for key, column in [('precision', 'metrics/precision(B)'), ('recall', 'metrics/recall(B)'), ('map50', 'metrics/mAP50(B)')]:
                        value = raw.get(column)
                        number = float(value) if value not in (None, '') else None
                        if number is not None and not math.isfinite(number):
                            raise ValueError('학습 곡선에 유효하지 않은 값이 있습니다.')
                        row[key] = number
                    rows.append(row)
        result.append({'run': name, 'history': rows, 'source': str(path) if path.is_file() else None,
                       'phase_complete': (path.parent / 'phase_complete.json').is_file()})
    return result


def status(root=TRAINING_ROOT, previous=PREVIOUS, now=None):
    now = time.time() if now is None else now
    work = Path(root) / 'work'
    jobs = job_records(work)
    current = next((row for row in jobs if row.get('kind') == 'train'), {})
    training = dict(current)
    training['job'] = current.get('id')
    stage = current.get('stage', '')
    training['phase'] = ('GPU 학습' if stage.startswith(('학습 ', '새 후보 학습', 'checkpoint 재개')) else
                         '평가' if '평가' in stage or '테스트 완료' in stage else '자료 준비')
    training['downloaded_bytes'] = current.get('downloaded_bytes', current.get('download_bytes'))
    observed = current.get('updated', current.get('created'))
    delay = max(0, now - observed) if isinstance(observed, (int, float)) and not isinstance(observed, bool) else None
    training.update(observed_kst=kst(observed), delay_seconds=round(delay, 1) if delay is not None else None,
                    stale=delay is None or delay > 120, live_process_verified=False)
    config = read(Path(root) / 'configs/training.json', {})
    training['runs'] = histories(work, config.get('candidates', []))
    training['history'] = []
    final = read(work / 'training/final.json', {})
    primary = final.get('test', {})
    operating = primary.get('operating', {})
    metrics = {'precision': operating.get('precision'), 'recall': operating.get('recall'),
               'map50': primary.get('metrics', {}).get('AP50'),
               'split': '7차 고정 테스트' if primary else '7차 최종 평가 미측정'}
    display_jobs = []
    for job in jobs[:20]:
        job = dict(job)
        job['log_path'] = 'round7/jobs/' + job['id'] + '.log'
        display_jobs.append(job)
    # 영상 탐지 결과만 기존 작업에서 가져오며 이전 학습 수치와 혼합하지 않습니다.
    display_jobs += [legacy.local_paths(row) for row in job_records(Path(previous) / 'work')
                     if row.get('kind') == 'detect'][:20]
    return {'jobs': display_jobs, 'training': training, 'metrics': metrics,
            'dataset': read(work / 'training/data_manifest.json', {}).get('counts', {}),
            'contracts': {'experiment': (work / 'training/experiment_contract.json').is_file(),
                          'selection': (work / 'training/selection.json').is_file(),
                          'test': (work / 'training/test_contract.json').is_file()},
            'busy': any(row.get('state') in ACTIVE for row in jobs), 'now_kst': kst(now),
            'project': '8차 클린뷰 · 7차 학습 연결',
            'note': '작업 JSON의 마지막 저장 관측입니다. 현재 프로세스 생존을 보장하지 않습니다. 영상 탐지는 기존 5차 검증 모델을 사용합니다.'}


def action(name, params):
    if not isinstance(params, dict):
        raise ValueError('설정은 JSON 객체여야 합니다.')
    if name == 'status':
        return status()
    if name == 'train':
        if set(params) - {'resume'} or type(params.get('resume', False)) is not bool:
            raise ValueError('resume은 명시적 참 또는 거짓만 허용합니다.')
        if status()['busy']:
            raise ValueError('7차 자료 준비 또는 학습 작업이 이미 진행 중입니다.')
        # 중복 시작 최종 판단은 컨테이너의 원래 worker 잠금이 수행합니다.
        return legacy.docker_call(['/workspace/2026/월요일 PBL/7차/worker.py', '--action', 'train',
                                   '--params', json.dumps(params)], timeout=25)
    if name in {'videos', 'probe', 'detect'}:
        return legacy.action(name, params)
    raise ValueError('지원하지 않는 작업입니다.')
