"""8차의 실측 상태와 작업 경계를 재사용하는 10차 표시 어댑터입니다."""
import importlib.util
import json
from safe_io import safe_read_json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / '5차'
TRAINING_ROOT = ROOT.parent / '7차'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


round8 = load_module('cleanview_round8_pipeline', ROOT.parent / '8차/pipeline.py')
# 10차에 로드한 모듈의 읽기만 바꾸며 8차 원본 파일은 보존합니다.
round8.read = safe_read_json
legacy = round8.legacy
kst = round8.kst
job_records = round8.job_records
ACTIVE = round8.ACTIVE


def presentation(training):
    stage = training.get('stage', '')
    state = training.get('state')
    resource_wait = stage == '다른 GPU 작업을 보존하며 여유 VRAM 확인'
    index = None
    if training.get('job'):
        if state == 'complete': index = 4
        elif stage.startswith('고정 검증·평가 '): index = 4 if '/tests' in stage or any(name in stage for name in ('historical_taco', 'new_plastopol', 'source_heldout_uav')) else 3
        elif stage == '학습 전용 작은 객체 crop': index = 1
        elif stage.startswith(('학습 ', '새 후보 학습', 'checkpoint 재개', '다른 GPU 작업')): index = 2
        elif any(word in stage for word in ('다운로드', '수신', 'MD5')): index = 0
        else: index = 1
    titles = ['데이터를 다운로드하고 있습니다', '학습 데이터를 준비하고 있습니다', 'GPU 학습을 진행하고 있습니다', '후보 모델을 검증하고 있습니다', '최종 성능을 평가하고 있습니다']
    descriptions = ['자료 준비가 끝나면 GPU 학습이 자동으로 시작됩니다.', '원본 검사·추출·이미지 정규화와 고정 분할을 준비합니다. 아직 GPU 학습 전입니다.', '정해진 학습 계획으로 후보 모델을 학습합니다. 아래 곡선은 실제 저장된 에포크 기록입니다.', '검증 자료로 모델과 추론 방식을 비교합니다. 최종 테스트 성능과 구분합니다.', '고정한 모델과 임계값으로 테스트를 평가합니다. 최종 결과가 저장될 때 성능을 표시합니다.']
    labels = ['다운로드', '데이터 준비', 'GPU 학습', '검증', '최종 평가']
    title = titles[index] if index is not None else '아직 시작한 작업이 없습니다'
    description = descriptions[index] if index is not None else '기록된 작업이 없습니다. 대시보드 조회만으로 학습을 시작하지 않습니다.'
    badge = '진행 중'
    if state in ('failed', 'interrupted'):
        title = '작업이 실패했습니다' if state == 'failed' else '작업이 중단됐습니다'
        description = ('자료 수신이 중단됐습니다. 받은 자료는 유지됩니다. 작업 기록에서 오류를 확인하세요.'
                       if index == 0 else '작업이 중단됐습니다. 기존 자료와 기록은 유지됩니다. 작업 기록에서 오류를 확인하세요.')
        badge = '실패' if state == 'failed' else '중단'
    elif state == 'complete': title, badge = '실험 작업이 완료됐습니다', '완료'
    elif state in ('queued', 'starting'): title, badge = '작업 시작을 기다리고 있습니다', '대기'
    elif state is None: badge = '자료 없음'
    if resource_wait and state in ACTIVE:
        title, badge = 'GPU 자원을 기다리고 있습니다', '자원 대기'
        description = '다른 GPU 작업을 보존하면서 필요한 여유 메모리를 확인합니다. 아직 학습을 시작한 상태가 아닙니다.'
    retry = bool(training.get('retry_reason') and training.get('retry_attempt', 0))
    if retry and state in ACTIVE:
        title, badge = '자료 다운로드를 재시도하고 있습니다', '재시도'
        description = '원래 독립 작업자가 수신을 재시도합니다. 재시도 사유와 횟수는 실제 기록을 표시합니다.'
    downloaded = training.get('downloaded_bytes')
    total = training.get('file_bytes')
    valid = lambda v: type(v) in (int, float) and round8.math.isfinite(v) and v >= 0
    percent = min(100., max(0., downloaded / total * 100)) if valid(downloaded) and valid(total) and total > 0 else None
    next_stage = ('작업 대기 / 기록 없음' if index is None else
                  '다운로드 검증 및 데이터 준비' if index == 0 else
                  labels[index + 1] if index < 4 else
                  '저장된 최종 결과 확인' if state == 'complete' else '최종 결과 저장')
    next_description = ('작업 기록이 생기면 다음 단계를 안내합니다.' if index is None else [
        '다운로드가 완료되면 자동으로 진행됩니다.',
        '자료 준비가 끝나면 GPU 학습이 자동으로 시작됩니다.',
        '후보 학습이 끝나면 고정 검증 자료로 모델을 비교합니다.',
        '검증으로 선택을 고정한 뒤 최종 테스트를 진행합니다.',
        '테스트 평가가 끝나면 최종 성능 결과를 저장합니다.'][index])
    if resource_wait:
        next_stage = '대기 중인 GPU 작업 계속'
        next_description = '여유 메모리가 확보되면 대기 중인 GPU 작업을 이어갑니다.'
    if state in ('failed', 'interrupted'):
        next_stage = '오류 기록 확인'
        next_description = '원인과 기록을 확인한 뒤 재개 여부를 결정합니다.'
    elif state == 'complete':
        next_description = '완료된 작업 기록과 저장된 최종 평가를 확인하세요.'
    return {'step': index, 'title': title, 'description': description, 'badge': badge,
            'steps': [{'name': name, 'status': 'complete' if state == 'complete' or (index is not None and index >= 2 and i < index) else 'active' if i == index else 'pending'} for i, name in enumerate(labels)],
            'next': next_stage, 'next_description': next_description,
            'file_percent': percent, 'downloaded_bytes': downloaded if valid(downloaded) else None,
            'file_bytes': total if valid(total) else None, 'retry': retry,
            'gpu_state': '대기 중' if resource_wait else '학습 중' if index == 2 and state in ACTIVE else '학습 단계 종료' if index in (3, 4) else '대기 중',
            'epoch': training.get('epoch') if index == 2 and not resource_wait else None}


def status(root=TRAINING_ROOT, previous=PREVIOUS, now=None):
    value = round8.status(root, previous, now)
    value['presentation'] = presentation(value['training'])
    value['project'] = '10차 클린뷰 · 7차 독립 실험 연결'
    return value


def action(name, params):
    if not isinstance(params, dict):
        raise ValueError('설정은 JSON 객체여야 합니다.')
    if name == 'status': return status()
    if name == 'train':
        if set(params) - {'resume'} or type(params.get('resume', False)) is not bool:
            raise ValueError('resume은 명시적 참 또는 거짓만 허용합니다.')
        if status()['busy']:
            raise ValueError('7차 자료 준비 또는 학습 작업이 이미 진행 중입니다.')
        return legacy.docker_call(['/workspace/2026/월요일 PBL/7차/worker.py', '--action', 'train', '--params', json.dumps(params)], timeout=25)
    return round8.action(name, params)
