"""보고서 검사용 합성 자료이며 실제 실험 결과가 아닙니다."""
import copy
import hashlib
import json
from pathlib import Path


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, allow_nan=False), encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(root):
    root = Path(root)
    train = root / '7차/work/training'
    model = train / 'runs/fixture/weights/best.pt'
    model.parent.mkdir(parents=True)
    model.write_bytes(b'fixture-only-not-a-model')
    paths = ['configs/training.json', 'train_pipeline.py', 'prepare_dataset.py', 'configs/protected_sources.json']
    for file in paths:
        p = root / '7차' / file
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('{}', encoding='utf-8')
    config = {'evaluation_imgsz':1280,'evaluation_conf_floor':.001,
              'evaluation_nms_iou':.5,'evaluation_max_det':1000,
              'validation_policies':['full','full_grid3']}
    save(root/'7차/configs/training.json',config)
    records = []
    names = {'historical_taco': 'historical_test', 'new_plastopol': 'test', 'source_heldout_uav': 'external_test'}
    for name, split in names.items():
        label = train / 'labels' / (name + '.txt')
        label.parent.mkdir(exist_ok=True)
        label.write_text('0 0.5 0.5 0.2 0.2\n', encoding='utf-8')
        records.append({'id': name, 'source': name, 'split': split, 'label': str(label),
                        'label_sha256': sha(label), 'sha256': 'a'*64, 'width': 100, 'height': 100})
    manifest = {'counts': {'original_images': 3}, 'records': records, 'limits': ['합성 자료']}
    save(train / 'data_manifest.json', manifest)
    op = {'precision': .5, 'recall': 1., 'f1': 2/3, 'tp': 1, 'fp': 1, 'fn': 0, 'threshold': .2, 'iou': .5}
    empty = {'precision': 0., 'recall': 0., 'f1': 0., 'tp': 0, 'fp': 0, 'fn': 0, 'threshold': .2, 'iou': .5}
    result = {'operating': op, 'metrics': {'AP50': 1., 'AP50_95': 1.}, 'images': 1,
              'weights': [str(model)], 'weights_sha256': {str(model): sha(model)},
              'policy': 'full', 'imgsz': 1280, 'evaluator':'single-class confidence-greedy IoU; 101-point interpolated AP; v2',
              'sizes': {'small': op, 'medium': empty, 'large': empty},
              'negative_images': 0, 'negative_false_positives': 0, 'false_positives_per_negative_image': None}
    selected = dict(copy.deepcopy(result), name='fixture_full')
    comparison = [selected]
    save(train / 'validation_comparison.json', comparison)
    save(train / 'selection.json', selected)
    experiment = dict(zip(['config_sha256', 'pipeline_sha256', 'preparation_sha256', 'protected_sources_sha256'],
                          [sha(root / '7차' / p) for p in paths]))
    experiment['manifest_sha256'] = sha(train / 'data_manifest.json')
    save(train / 'experiment_contract.json', experiment)
    save(train / 'test_contract.json', {'experiment': experiment, 'selected': selected,
         'protocol':'freeze model, tiles and threshold before tests; no test tuning; per-image prediction cache'})
    for row in records:
        directory = train / 'evaluation/tests' / row['id']
        save(directory / 'metrics.json', result)
        save(directory / 'contract.json', {'weights': selected['weights_sha256'], 'policy': 'full', 'threshold': .2,
                                           'imgsz':1280,'conf_floor':.001,'nms_iou':.5,'max_det':1000,
                                           'evaluator':result['evaluator'],
                                           'images': {row['id']: [row['sha256'], row['label_sha256']]}})
        save(directory / 'predictions' / (row['id'] + '.json'), [[40,40,60,60,.8], [0,0,10,10,.3]])
    final = {'selected': selected, 'tests': {name: copy.deepcopy(result) for name in names},
             'test': result, 'target_met': False, 'all_test_targets_met': False,
             'manifest_sha256': experiment['manifest_sha256'], 'counts': manifest['counts'], 'finished': 1700000000,
             'limits': ['합성 제어 사례이며 실제 성능이 아닙니다.']}
    save(train / 'final.json', final)
    job = {'id': 'fixture_job', 'kind': 'train', 'state': 'complete', 'result': final, 'updated': 1700000000}
    return job


class Reader:
    @staticmethod
    def safe_read_json(path, default=None):
        try:
            return json.loads(Path(path).read_text(encoding='utf-8'))
        except FileNotFoundError:
            return default

    @staticmethod
    def safe_read_text(path, encoding='utf-8'):
        return Path(path).read_text(encoding=encoding)
