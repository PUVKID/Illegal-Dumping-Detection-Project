"""허용 경로와 API 설정 실패 경로를 확인합니다."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import pipeline


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
