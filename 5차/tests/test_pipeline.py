"""허용 경로와 API 설정 실패 경로를 확인합니다."""
import tempfile
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import pipeline


class TrainingStatusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name) / 'work'
        (self.work / 'jobs').mkdir(parents=True)
        (self.work / 'training').mkdir()
        self.work_patch = patch.object(pipeline, 'WORK', self.work)
        self.archive_patch = patch.object(pipeline, 'ARCHIVE', Path(self.temp.name) / 'archive')
        self.work_patch.start()
        self.archive_patch.start()

    def tearDown(self):
        self.archive_patch.stop()
        self.work_patch.stop()
        self.temp.cleanup()

    def save(self, relative, value):
        (self.work / relative).write_text(json.dumps(value), encoding='utf-8')

    def test_failed_job_overrides_stale_preparation_status(self):
        self.save('jobs/latest.json', {'id': 'latest', 'kind': 'train', 'created': 10,
                                      'state': 'failed', 'error': '고정 이미지 변경: plitter_381',
                                      'epoch': 0, 'epochs': 180, 'updated': 20})
        self.save('training/status.json', {'job': 'latest', 'stage': '자료 확인', 'epoch': 0, 'updated': 11})
        training = pipeline.status()['training']
        self.assertEqual(training.get('state'), 'failed')
        self.assertEqual(training.get('error'), '고정 이미지 변경: plitter_381')
        self.assertEqual(training.get('job'), 'latest')
        self.assertEqual(training.get('updated'), 20)
        self.assertEqual(training.get('epoch'), 0)

    def test_complete_job_overrides_stale_state_and_error(self):
        self.save('jobs/done.json', {'id': 'done', 'kind': 'train', 'created': 10,
                                    'state': 'complete', 'stage': '최종 평가 완료', 'epoch': 79})
        self.save('training/status.json', {'job': 'done', 'state': 'failed', 'error': '과거 오류', 'epoch': 0})
        training = pipeline.status()['training']
        self.assertEqual(training.get('state'), 'complete')
        self.assertIsNone(training.get('error'))
        self.assertEqual(training.get('epoch'), 79)

    def test_other_job_progress_is_not_current_training(self):
        self.save('jobs/new.json', {'id': 'new', 'kind': 'train', 'created': 20,
                                   'state': 'failed', 'epoch': 0, 'stage': '자료 확인'})
        self.save('jobs/detection.json', {'id': 'detection', 'kind': 'detect', 'created': 30, 'state': 'complete'})
        self.save('training/status.json', {'job': 'old', 'epoch': 79, 'images': 5000, 'stage': '학습 중'})
        training = pipeline.status()['training']
        self.assertEqual(training.get('job'), 'new')
        self.assertEqual(training.get('epoch'), 0)
        self.assertEqual(training.get('stage'), '자료 확인')
        self.assertNotIn('images', training)

    def test_completed_history_is_separate_from_latest_failed_zero_epoch(self):
        self.save('jobs/old.json', {'id': 'old', 'kind': 'train', 'created': 10, 'state': 'failed', 'epoch': 79})
        self.save('jobs/new.json', {'id': 'new', 'kind': 'train', 'created': 20, 'state': 'failed', 'epoch': 0})
        run = self.work / 'training/runs/prior_run'
        run.mkdir(parents=True)
        (run / 'results.csv').write_text('epoch,metrics/precision(B)\n78,0.7\n', encoding='utf-8')
        (run / 'phase_complete.json').write_text('{"completed":30}', encoding='utf-8')
        training = pipeline.status()['training']
        self.assertEqual(training.get('epoch'), 0)
        self.assertEqual(training['history'][-1]['epoch'], 78)
        self.assertEqual(training['history_context']['run'], 'prior_run')
        self.assertTrue(training['history_context']['phase_complete'])
        self.assertEqual(training['history_context']['last_epoch'], 78)

    def test_orphan_status_does_not_imply_running_job(self):
        self.save('training/status.json', {'job': 'unknown', 'state': 'running', 'epoch': 79})
        training = pipeline.status()['training']
        self.assertNotEqual(training.get('state'), 'running')
        self.assertNotIn('epoch', training)


class PipelineTests(unittest.TestCase):
    def test_only_declared_video_roots(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            allowed = base / "allowed"
            allowed.mkdir()
            good = allowed / "a.mp4"
            good.write_bytes(b"a")
            bad = base / "secret.mp4"
            bad.write_bytes(b"a")
            with patch.object(pipeline, "VIDEO_ROOTS", [allowed]):
                self.assertEqual(pipeline.video_path(good), good.resolve())
                with self.assertRaisesRegex(ValueError, "허용"):
                    pipeline.video_path(bad)

    def test_settings_must_be_an_object(self):
        with self.assertRaises(ValueError):
            pipeline.action("train", [])

    def test_unknown_action_rejected(self):
        with self.assertRaises(ValueError):
            pipeline.action("delete", {})

    def test_log_tail_is_bounded(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "large.log"
            path.write_bytes(b"x" * 50000)
            self.assertLessEqual(len(pipeline.tail(path).encode()), 12000)

    def test_status_does_not_export_entire_dataset(self):
        import json
        rows = [{"image": "image.jpg", "url": "https://example.org/" + "x" * 600} for _ in range(5000)]
        def fake_load(path, default=None):
            if Path(path).name == "data_manifest.json":
                return {"records": rows, "counts": {"train": 5000}, "sources": []}
            return default
        with patch.object(pipeline, "load", side_effect=fake_load):
            result = pipeline.status()
        self.assertFalse("records" in result["dataset"], "대시보드 상태에는 전체 데이터 레코드를 포함하면 안 됩니다.")
        self.assertLess(len(json.dumps(result)), 100000)


if __name__ == "__main__":
    unittest.main()
