"""학습을 실행하지 않고 보존된 실험 결과와 해시를 검증합니다."""
from collections import Counter
import csv
import hashlib
import importlib.util
import math
from pathlib import Path
import re

TEST_SPLITS = {'historical_taco': 'historical_test', 'new_plastopol': 'test',
               'source_heldout_uav': 'external_test'}
EVALUATOR = 'single-class confidence-greedy IoU; 101-point interpolated AP; v2'
TEST_PROTOCOL = 'freeze model, tiles and threshold before tests; no test tuning; per-image prediction cache'
SECTIONS = ('overview', 'problem', 'development', 'architecture', 'dataset', 'preprocess',
            'training', 'selection', 'results', 'analysis', 'application', 'limits', 'conclusion')


def safe_reader(project):
    """공유 삭제 핸들을 사용한 기존 읽기를 원본 수정 없이 불러옵니다."""
    path = Path(project) / '10차' / 'safe_io.py'
    spec = importlib.util.spec_from_file_location('report_safe_io', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def confined(path, project):
    project = Path(project).resolve()
    path = Path(path).resolve()
    if not path.is_relative_to(project):
        raise ValueError('근거 파일이 지정 프로젝트 경계를 벗어났습니다.')
    return path


def local_path(value, project):
    """기존 Docker 경로를 지정 프로젝트 안의 실제 파일로 대응합니다."""
    project = Path(project).resolve()
    value = str(value)
    portable_prefix = '/workspace/2026/' + project.name + '/'
    if value.startswith(portable_prefix):
        path = project / value[len(portable_prefix):]
    elif value.startswith('/root/환경 PBL/trash_round3/'):
        path = project / '이전 도커 실험/3차실험/trash_round3' / value.removeprefix('/root/환경 PBL/trash_round3/')
    elif Path(value).is_absolute():
        path = Path(value)
    else:
        path = project / value
    return confined(path, project)


def relative(path, project):
    return confined(path, project).relative_to(Path(project).resolve()).as_posix()


def job_path(project, job_id):
    if not isinstance(job_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', job_id):
        raise ValueError('허용되지 않는 작업 ID입니다.')
    return Path(project) / '7차/work/jobs' / (job_id + '.json')


def decision(job, job_id):
    if job is None:
        return 'missing'
    if not isinstance(job, dict) or job.get('id') != job_id or job.get('kind') != 'train':
        raise ValueError('지정 작업의 식별자 또는 종류가 일치하지 않습니다.')
    state = job.get('state')
    if state in ('queued', 'running'):
        return 'waiting'
    if state in ('failed', 'interrupted'):
        return 'incomplete'
    if state == 'complete':
        return 'validate'
    raise ValueError('알 수 없는 작업 상태입니다.')


def numeric(value, name, lower=0, upper=1):
    if type(value) not in (int, float) or not math.isfinite(value) or not lower <= value <= upper:
        raise ValueError('잘못된 수치: ' + name)
    return value


def validate_result(row):
    op = row['operating']
    for key in ('tp', 'fp', 'fn'):
        if type(op.get(key)) is not int or op[key] < 0:
            raise ValueError('TP/FP/FN은 음수가 아닌 정수여야 합니다.')
    tp, fp, fn = (op[k] for k in ('tp', 'fp', 'fn'))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    for key, expected in (('precision', precision), ('recall', recall), ('f1', f1)):
        if not math.isclose(numeric(op[key], key), expected, abs_tol=1e-9):
            raise ValueError('성능과 혼동 수가 일치하지 않습니다: ' + key)
    numeric(op['threshold'], 'threshold')
    if op.get('iou') != .5:
        raise ValueError('고정 IoU .5 계약이 아닙니다.')
    for key in ('AP50', 'AP50_95'):
        numeric(row['metrics'][key], key)
    if type(row.get('images')) is not int or row['images'] <= 0:
        raise ValueError('실제 평가 이미지 수가 없습니다.')
    return precision >= .9 and recall >= .9


def verify_hash(path, expected, refs, project):
    if not isinstance(expected, str) or not re.fullmatch('[a-f0-9]{64}', expected):
        raise ValueError('SHA-256 형식이 잘못됐습니다.')
    path = confined(path, project)
    actual = digest(path)
    if actual != expected:
        raise ValueError('근거 파일 SHA-256 불일치: ' + relative(path, project))
    refs[relative(path, project)] = {'sha256': actual, 'bytes': path.stat().st_size}


def validate_bundle(project, job, read_json):
    """완료 상태와 결과 및 모든 동결 계약이 함께 맞을 때만 반환합니다."""
    project = Path(project).resolve()
    training = project / '7차/work/training'
    if job.get('state') != 'complete':
        raise ValueError('정상 완료 작업만 성공 보고서를 만들 수 있습니다.')
    final = read_json(training / 'final.json')
    if not isinstance(final, dict) or job.get('result') != final:
        raise ValueError('작업 결과와 최종 결과가 일치하지 않습니다.')
    manifest = read_json(training / 'data_manifest.json')
    experiment = read_json(training / 'experiment_contract.json')
    selection = read_json(training / 'selection.json')
    test_contract = read_json(training / 'test_contract.json')
    comparison = read_json(training / 'validation_comparison.json')
    config = read_json(project / '7차/configs/training.json')
    if selection != final['selected'] or test_contract['selected'] != selection or test_contract['experiment'] != experiment:
        raise ValueError('선택 및 테스트 계약이 최종 결과와 다릅니다.')
    if selection not in comparison:
        raise ValueError('검증 비교표에 선택된 모델이 없습니다.')
    if test_contract.get('protocol') != TEST_PROTOCOL:
        raise ValueError('고정 테스트의 프로토콜이 다릅니다.')
    if (selection.get('imgsz') != config['evaluation_imgsz']
            or selection.get('policy') not in config['validation_policies']
            or selection.get('evaluator') != EVALUATOR):
        raise ValueError('선택된 모델의 추론 및 평가 설정이 고정 명세와 다릅니다.')
    if set(final['tests']) != set(TEST_SPLITS):
        raise ValueError('세 고정 테스트가 모두 있어야 합니다.')
    if final.get('test') != final['tests']['historical_taco']:
        raise ValueError('주평가 결과가 과거 TACO와 일치하지 않습니다.')
    refs = {}
    if final['manifest_sha256'] != experiment['manifest_sha256']:
        raise ValueError('최종 manifest 계약이 다릅니다.')
    verify_hash(training / 'data_manifest.json', final['manifest_sha256'], refs, project)
    for key, filename in (('config_sha256', 'configs/training.json'),
                          ('pipeline_sha256', 'train_pipeline.py'),
                          ('preparation_sha256', 'prepare_dataset.py'),
                          ('protected_sources_sha256', 'configs/protected_sources.json')):
        verify_hash(project / '7차' / filename, experiment[key], refs, project)
    if final['counts'] != manifest['counts']:
        raise ValueError('데이터 집계와 manifest가 다릅니다.')
    selected_weights = selection['weights_sha256']
    if set(selection['weights']) != set(selected_weights):
        raise ValueError('선택 가중치와 해시 목록이 다릅니다.')
    for value, sha in selected_weights.items():
        verify_hash(local_path(value, project), sha, refs, project)
    validate_result(selection)
    for name, split in TEST_SPLITS.items():
        result = final['tests'][name]
        validate_result(result)
        if (result['weights_sha256'] != selected_weights or result['weights'] != selection['weights']
                or result['policy'] != selection['policy'] or result['imgsz'] != selection['imgsz']
                or result.get('evaluator') != EVALUATOR
                or result['operating']['threshold'] != selection['operating']['threshold']):
            raise ValueError('테스트가 선택된 모델과 추론 계약을 따르지 않습니다: ' + name)
        records = [r for r in manifest['records'] if r['split'] == split]
        if result['images'] != len(records):
            raise ValueError('평가 이미지 수와 고정 분할이 다릅니다: ' + name)
        evaluation = training / 'evaluation/tests' / name
        if read_json(evaluation / 'metrics.json') != result:
            raise ValueError('테스트 평가 파일과 최종 결과가 다릅니다: ' + name)
        contract = read_json(evaluation / 'contract.json')
        expected_settings = {'weights':selected_weights,'policy':selection['policy'],
                             'threshold':selection['operating']['threshold'],
                             'imgsz':config['evaluation_imgsz'],'conf_floor':config['evaluation_conf_floor'],
                             'nms_iou':config['evaluation_nms_iou'],'max_det':config['evaluation_max_det'],
                             'evaluator':EVALUATOR}
        if any(contract.get(key) != expected for key,expected in expected_settings.items()):
            raise ValueError('평가 동결 계약이 다릅니다: ' + name)
        expected_images = {r['id']: [r['sha256'], r['label_sha256']] for r in records}
        if contract['images'] != expected_images:
            raise ValueError('평가 이미지 해시 목록이 manifest와 다릅니다: ' + name)
        for row in records:
            verify_hash(local_path(row['label'], project), row['label_sha256'], refs, project)
        for size in ('small', 'medium', 'large'):
            size_row = result['sizes'][size]
            # 크기별 AP는 없으므로 P/R/F1과 혼동 수만 검사합니다.
            validate_result({'operating': size_row, 'metrics': result['metrics'], 'images': result['images']})
    targets = {name:validate_result(value) for name,value in final['tests'].items()}
    if (final.get('target_met') != targets['historical_taco']
            or final.get('all_test_targets_met') != all(targets.values())):
        raise ValueError('기록된 목표 판정과 실제 정밀도·재현율이 다릅니다.')
    for file in ('final.json', 'experiment_contract.json', 'selection.json', 'test_contract.json', 'validation_comparison.json'):
        path = training / file
        refs[relative(path, project)] = {'sha256': digest(path), 'bytes': path.stat().st_size}
    return {'final': final, 'manifest': manifest, 'comparison': comparison, 'references': refs}


def iou(a, b):
    intersection = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
    union = max(0, a[2] - a[0]) * max(0, a[3] - a[1]) + max(0, b[2] - b[0]) * max(0, b[3] - b[1]) - intersection
    return intersection / union if union else 0.0


def match_rows(predictions, targets):
    """7차와 같은 신뢰도 내림차순 탐욕 매칭이며 새 추론을 하지 않습니다."""
    used = set()
    flags = [False] * len(predictions)
    for index in sorted(range(len(predictions)), key=lambda i: predictions[i][4], reverse=True):
        overlap, identity = max(((iou(predictions[index], box), j) for j, box in enumerate(targets)
                                 if j not in used), default=(0, -1))
        if overlap >= .5:
            flags[index] = True
            used.add(identity)
    return [(float(p[4]), flags[i]) for i, p in enumerate(predictions)]


def curve_points(scored, total):
    ordered = sorted(scored, key=lambda row: row[0], reverse=True)
    points = []
    tp = 0
    for index, (threshold, matched) in enumerate(ordered):
        tp += int(matched)
        if index + 1 < len(ordered) and ordered[index + 1][0] == threshold:
            continue
        p = tp / (index + 1)
        r = tp / total if total else 0.0
        points.append({'threshold': threshold, 'precision': p, 'recall': r,
                       'f1': 2 * p * r / (p + r) if p + r else 0.0,
                       'tp': tp, 'fp': index + 1 - tp, 'fn': total - tp})
    return points


def reconstruct_curves(project, bundle, reader):
    curves = {}
    training = Path(project) / '7차/work/training'
    for name, split in TEST_SPLITS.items():
        scored, total = [], 0
        for row in bundle['manifest']['records']:
            if row['split'] != split:
                continue
            targets = []
            for line in reader.safe_read_text(local_path(row['label'], project)).split('\n'):
                if not line.strip():
                    continue
                values = list(map(float, line.split()))
                if len(values) != 5 or values[0] != 0 or not all(math.isfinite(v) for v in values):
                    raise ValueError('고정 정답 라벨 형식이 잘못됐습니다.')
                _, x, y, w, h = values
                targets.append([(x-w/2)*row['width'], (y-h/2)*row['height'],
                                (x+w/2)*row['width'], (y+h/2)*row['height']])
            predictions = reader.safe_read_json(training / 'evaluation/tests' / name / 'predictions' / (row['id'] + '.json'))
            if not isinstance(predictions, list) or any(len(p) != 5 or not all(math.isfinite(v) for v in p) for p in predictions):
                raise ValueError('고정 예측 캐시 형식이 잘못됐습니다.')
            scored.extend(match_rows(predictions, targets))
            total += len(targets)
        points = curve_points(scored, total)
        op = bundle['final']['tests'][name]['operating']
        chosen = [matched for threshold, matched in scored if threshold >= op['threshold']]
        if (sum(chosen), len(chosen) - sum(chosen), total - sum(chosen)) != tuple(op[k] for k in ('tp', 'fp', 'fn')):
            raise ValueError('예측에서 재구성한 TP/FP/FN이 최종 결과와 다릅니다: ' + name)
        curves[name] = points
    return curves


def source_splits(manifest):
    counts = Counter((r['source'], r['split'], bool(r.get('augmentation'))) for r in manifest['records'])
    return [{'source': source, 'split': split, 'augmentation': aug, 'images': count}
            for (source, split, aug), count in sorted(counts.items())]


def epoch_rows(path, read_text):
    rows = []
    for raw in csv.DictReader(read_text(path).split('\n')):
        row = {key.strip(): value.strip() for key, value in raw.items() if key is not None}
        values = {}
        for key, value in row.items():
            try:
                number = float(value)
            except ValueError:
                continue
            if math.isfinite(number):
                values[key] = number
        if 'epoch' in values:
            rows.append(values)
    return rows


def load_sections(path, read_json):
    data = read_json(path)
    if tuple(row['id'] for row in data['sections']) != SECTIONS:
        raise ValueError('보고서 고정 본문의 절 구성이 계약과 다릅니다.')
    if not all(row['paragraphs'] and all(isinstance(p, str) and p.strip() for p in row['paragraphs']) for row in data['sections']):
        raise ValueError('보고서 본문 문단이 비었습니다.')
    return data
