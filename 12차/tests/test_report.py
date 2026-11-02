"""실제 학습 없이 고정 결과의 완료 판정과 보고서 정합성을 검사합니다."""
import importlib.util
from pathlib import Path
import sys
import unittest
import copy
import tempfile
from fixtures import fixture, Reader, save

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class CompletionContract(unittest.TestCase):
    def test_completion_module_is_available(self):
        self.assertIsNotNone(importlib.util.find_spec('report_core'),
                             '지정 작업과 동결 결과를 검증하는 모듈이 필요합니다.')

    def test_running_never_completes_from_age(self):
        from report_core import decision
        self.assertEqual(decision({'id': 'x', 'kind': 'train', 'state': 'running', 'updated': 0}, 'x'), 'waiting')

    def test_missing_is_not_complete(self):
        from report_core import decision
        self.assertEqual(decision(None, 'x'), 'missing')

    def test_wrong_job_rejected(self):
        from report_core import decision
        with self.assertRaises(ValueError):
            decision({'id': 'other', 'kind': 'train', 'state': 'complete'}, 'x')

    def test_failed_and_interrupted_are_incomplete(self):
        from report_core import decision
        for state in ('failed', 'interrupted'):
            self.assertEqual(decision({'id': 'x', 'kind': 'train', 'state': state}, 'x'), 'incomplete')

    def test_job_path_rejects_traversal(self):
        from report_core import job_path
        with self.assertRaises(ValueError):
            job_path(ROOT, '../other')

    def test_path_rejects_external_reference(self):
        from report_core import local_path
        with self.assertRaises(ValueError):
            local_path('../outside.pt', ROOT)

    def test_docker_reference_maps_to_project(self):
        from report_core import local_path
        self.assertEqual(local_path('/workspace/2026/' + ROOT.name + '/7차/a', ROOT), ROOT / '7차/a')


class BundleContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.job = fixture(self.project)

    def validate(self):
        from report_core import validate_bundle
        return validate_bundle(self.project, self.job, Reader.safe_read_json)

    def test_validated_fixture_not_live_performance(self):
        self.assertEqual(len(self.validate()['final']['tests']), 3)

    def test_complete_requires_final_file(self):
        (self.project / '7차/work/training/final.json').unlink()
        with self.assertRaises(ValueError):
            self.validate()

    def test_result_job_mismatch_rejected(self):
        self.job['result'] = {}
        with self.assertRaises(ValueError):
            self.validate()

    def test_weight_tamper_rejected(self):
        model = next(iter(self.job['result']['selected']['weights_sha256']))
        Path(model).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            self.validate()

    def test_source_contract_tamper_rejected(self):
        (self.project / '7차/train_pipeline.py').write_text('changed', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            self.validate()

    def test_missing_third_test_rejected(self):
        final = self.job['result']
        del final['tests']['source_heldout_uav']
        save(self.project / '7차/work/training/final.json', final)
        with self.assertRaisesRegex(ValueError, '세 고정'):
            self.validate()

    def test_curves_reconstruct_fixed_prediction_counts(self):
        from report_core import reconstruct_curves
        curves = reconstruct_curves(self.project, self.validate(), Reader)
        self.assertEqual(curves['historical_taco'][-1]['fp'], 1)
        self.assertEqual(curves['historical_taco'][0]['recall'], 1)

    def test_prediction_tamper_is_not_silent(self):
        from report_core import reconstruct_curves
        bundle = self.validate()
        save(self.project / '7차/work/training/evaluation/tests/historical_taco/predictions/historical_taco.json', [])
        with self.assertRaisesRegex(ValueError, 'TP/FP/FN'):
            reconstruct_curves(self.project, bundle, Reader)

    def test_primary_target_is_independent_of_json_order(self):
        final=self.job['result']
        auxiliary=copy.deepcopy(final['tests']['new_plastopol'])
        auxiliary['operating'].update(precision=1.,recall=1.,f1=1.,fp=0)
        auxiliary['sizes']['small']=copy.deepcopy(auxiliary['operating'])
        final['tests']['new_plastopol']=auxiliary
        final['tests']={name:final['tests'][name] for name in ('new_plastopol','source_heldout_uav','historical_taco')}
        save(self.project/'7차/work/training/evaluation/tests/new_plastopol/metrics.json',auxiliary)
        save(self.project/'7차/work/training/final.json',final)
        self.assertFalse(self.validate()['final']['target_met'])

    def test_evaluation_parameters_must_match_frozen_config(self):
        for key in ('imgsz','conf_floor','nms_iou','max_det','evaluator'):
            with self.subTest(key=key):
                path=self.project/'7차/work/training/evaluation/tests/historical_taco/contract.json'
                contract=Reader.safe_read_json(path)
                original=copy.deepcopy(contract)
                contract[key]='tampered'
                save(path,contract)
                with self.assertRaises(ValueError):
                    self.validate()
                save(path,original)


class AnalysisContract(unittest.TestCase):
    def test_confusion_numeric_consistency(self):
        from report_core import validate_result
        with self.assertRaisesRegex(ValueError, '일치'):
            validate_result({'operating': {'tp': 1, 'fp': 1, 'fn': 0, 'precision': 1., 'recall': 1., 'f1': 1.}})

    def test_equal_confidence_grouped_for_pr(self):
        from report_core import curve_points
        points = curve_points([(.5, True), (.5, False)], 1)
        self.assertEqual(len(points), 1)
        self.assertEqual(points[0]['precision'], .5)

    def test_greedy_matching_duplicate_is_fp(self):
        from report_core import match_rows
        matched = match_rows([[0,0,10,10,.9],[0,0,10,10,.8]], [[0,0,10,10]])
        self.assertEqual(matched, [(.9, True), (.8, False)])

    def test_epoch_csv_is_actual_not_planned(self):
        from report_core import epoch_rows
        rows = epoch_rows(None, lambda _: 'epoch, metrics/precision(B)\n1,0.2\n2,0.4\n')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[-1]['epoch'], 2)

    def test_report_outputs_module_is_available(self):
        self.assertIsNotNone(importlib.util.find_spec('report_outputs'), '검증된 표·그림·문서 생성기가 필요합니다.')

    def test_watcher_module_is_available(self):
        self.assertIsNotNone(importlib.util.find_spec('watcher'), '단일 작업 전용 완료 후 처리기가 필요합니다.')


if __name__ == '__main__':
    unittest.main()
