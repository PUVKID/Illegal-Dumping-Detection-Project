"""분할 누출, 잘못된 라벨, 중단 재개와 모델 선택을 확인합니다."""
import importlib
import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class TrainingTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / "prepare_training.py").is_file(), "데이터 준비 기능이 아직 없습니다.")
        self.assertTrue((ROOT / "train_pipeline.py").is_file(), "학습 파이프라인이 아직 없습니다.")
        self.data = importlib.import_module("prepare_training")
        self.train = importlib.import_module("train_pipeline")

    def test_label_rejects_nonfinite_and_outside_box(self):
        # NaN이나 이미지 바깥 상자를 허용하는 변경을 탐지합니다.
        for text in ["0 nan .5 .1 .1", "0 .98 .5 .2 .2", "1 .5 .5 .2 .2", "0 .5 .5 0 .2"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.data.validate_yolo(text)
        self.assertEqual(self.data.validate_yolo("0 .5 .5 .2 .4\n"), [[0, .5, .5, .2, .4]])

    def test_seven_decimal_label_rounding_preserves_original_values(self):
        text = "0 0.3706140 0.2953750 0.7412281 0.5907500"
        self.assertEqual(self.data.validate_yolo(text), [[0, .3706140, .2953750, .7412281, .5907500]])
        with self.assertRaises(ValueError):
            self.data.validate_yolo("0 0.37060 0.2953750 0.7412281 0.5907500")

    def test_coco_clips_valid_partial_box(self):
        self.assertEqual(self.data.coco_to_yolo({"width": 100, "height": 100}, [{"bbox": [-10, 10, 40, 20]}]),
                         [[0, .15, .2, .3, .2]])

    def test_coco_rejects_invalid_geometry(self):
        for box in [[0, 0, -1, 10], [200, 0, 10, 10], [0, 0, float("inf"), 5]]:
            with self.subTest(box=box), self.assertRaises(ValueError):
                self.data.coco_to_yolo({"width": 100, "height": 100}, [{"bbox": box}])

    def test_group_keeps_gopro_chapters_together(self):
        a = self.data.group_key("street", {"path": "/datasets/Chiangrai_2021/piles/GH010132_009.jpg"})
        b = self.data.group_key("street", {"path": "/datasets/Chiangrai_2021/plastic/GH020132_999.jpg"})
        self.assertEqual(a, b)
        self.assertNotEqual(a, self.data.group_key("street", {"path": "/datasets/Ubon_2022/GH010132_009.jpg"}))

    def test_prior_identity_uses_source_id_not_reencoded_bytes(self):
        rows = [{"source": "pLitterStreet", "image": "/old/plitter_42.jpg", "sha256": "old-jpeg"},
                {"source": "pLitterStreet", "image": "/old/street_99.jpg", "sha256": "other-jpeg"},
                {"source": "SALSA", "image": "/old/salsa_13.jpg"}]
        self.assertEqual(self.data.prior_street_ids(rows), {"42", "99"})
        with self.assertRaises(ValueError):
            self.data.prior_street_ids([{"source": "pLitterStreet", "image": "unknown.jpg"}])

    def test_groups_do_not_cross_splits_and_seen_groups_stay_training(self):
        records = [{"id": str(i), "group": "g" + str(i // 2)} for i in range(80)]
        out = self.data.split_groups(records, seen_groups={"g0", "g1"}, seed=20261028)
        groups = {}
        for row in out:
            groups.setdefault(row["group"], set()).add(row["split"])
        self.assertTrue(all(len(s) == 1 for s in groups.values()))
        self.assertEqual(groups["g0"], {"train"})
        self.assertEqual({r["split"] for r in out}, {"train", "external_val", "external_test"})
        self.assertEqual(out, self.data.split_groups(list(reversed(records)), {"g0", "g1"}, 20261028))

    def test_duplicate_filter_prioritizes_holdout(self):
        protected = [{"sha256": "held", "signature": "0000000000000000"}]
        rows = [{"id": "same", "sha256": "held", "signature": "ffffffffffffffff"},
                {"id": "near", "sha256": "other", "signature": "0000000000000001"},
                {"id": "new", "sha256": "new", "signature": "ffffffffffffffff"}]
        accepted, rejected = self.data.deduplicate(rows, protected)
        self.assertEqual([r["id"] for r in accepted], ["new"])
        self.assertEqual({r["id"] for r in rejected}, {"same", "near"})

    def test_budget_survives_restart(self):
        with tempfile.TemporaryDirectory() as td:
            self.data.DownloadBudget(Path(td), limit=10).charge(7)
            budget = self.data.DownloadBudget(Path(td), limit=10)
            with self.assertRaises(ValueError):
                budget.charge(4)
            self.assertEqual(budget.used, 7)

    def test_concurrent_requests_cannot_overbook_budget(self):
        with tempfile.TemporaryDirectory() as td:
            budget = self.data.DownloadBudget(Path(td), limit=10)
            budget.reserve(7)
            with self.assertRaises(ValueError):
                budget.reserve(4)
            budget.charge(5, reserved=True)
            budget.release(2)
            budget.charge(4)
            self.assertEqual(budget.used, 9)

    def test_downloader_resumes_only_matching_etag(self):
        payload = b"cleanview-data" * 80
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass
            def do_HEAD(self):
                self.send_response(200)
                self.send_header("Content-Length", str(len(payload)))
                self.send_header("ETag", '"fixture-v1"')
                self.end_headers()
            def do_GET(self):
                start = int(self.headers.get("Range", "bytes=0-").split("=")[1].split("-")[0])
                self.send_response(206 if start else 200)
                self.send_header("Content-Length", str(len(payload) - start))
                self.send_header("ETag", '"fixture-v1"')
                if start:
                    self.send_header("Content-Range", f"bytes {start}-{len(payload)-1}/{len(payload)}")
                self.end_headers()
                self.wfile.write(payload[start:])
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                destination = root / "image.bin"
                url = f"http://127.0.0.1:{server.server_port}/data"
                destination.with_suffix(".bin.part").write_bytes(payload[:100])
                self.data.atomic_json(destination.with_suffix(".bin.part.json"), {"url": url, "etag": '"fixture-v1"', "size": len(payload)})
                budget = self.data.DownloadBudget(root, limit=2000)
                self.data.download(url, destination, budget)
                self.assertEqual(destination.read_bytes(), payload)
                self.assertEqual(budget.used, len(payload) - 100)
                self.data.download(url, destination, budget)
                self.assertEqual(budget.used, len(payload) - 100)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_corrupt_image_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.jpg"
            p.write_bytes(b"not a jpeg")
            with self.assertRaises(ValueError):
                self.data.image_info(p)

    def test_frozen_manifest_cannot_be_replaced(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "frozen.json"
            self.data.freeze_manifest(p, {"records": [{"sha256": "original"}]})
            with self.assertRaises(ValueError):
                self.data.freeze_manifest(p, {"records": [{"sha256": "changed"}]})
            self.assertEqual(json.loads(p.read_text())["records"][0]["sha256"], "original")

    def test_baseline_is_retained_when_new_model_is_worse_or_tied(self):
        baseline = {"name": "baseline", "operating": {"precision": .7, "recall": .6, "f1": .646, "threshold": .2}, "metrics": {"metrics/mAP50(B)": .65}}
        worse = {"name": "new", "operating": {"precision": .9, "recall": .5, "f1": .643, "threshold": .1}, "metrics": {"metrics/mAP50(B)": .8}}
        self.assertEqual(self.train.choose_candidate([baseline, worse])["name"], "baseline")
        tie = {**baseline, "name": "tie"}
        self.assertEqual(self.train.choose_candidate([baseline, tie])["name"], "baseline")

    def test_resume_refuses_different_dataset(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "weights").mkdir()
            (root / "weights/last.pt").write_bytes(b"checkpoint")
            self.data.atomic_json(root / "run_contract.json", {"manifest_sha256": "old"})
            with self.assertRaises(ValueError):
                self.train.resume_decision(root, {"manifest_sha256": "new"})

    def test_resume_completed_run_does_not_restart(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.data.atomic_json(root / "run_contract.json", {"manifest_sha256": "same"})
            self.data.atomic_json(root / "phase_complete.json", {"done": True})
            self.assertEqual(self.train.resume_decision(root, {"manifest_sha256": "same"}), "complete")

    def test_checkpoint_requires_explicit_resume(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "weights").mkdir()
            (root / "weights/last.pt").write_bytes(b"checkpoint")
            self.data.atomic_json(root / "run_contract.json", {"manifest_sha256": "same"})
            with self.assertRaises(ValueError):
                self.train.resume_decision(root, {"manifest_sha256": "same"}, allow_resume=False)

    def test_average_precision_penalizes_earlier_false_positive(self):
        self.assertEqual(self.train.average_precision([(.9, [True])], 1, 0), 1.0)
        self.assertEqual(self.train.average_precision([(.95, [False]), (.9, [True])], 1, 0), .5)

    def test_matching_cannot_count_same_object_twice(self):
        predictions = [[0, 0, 10, 10, .9], [0, 0, 10, 10, .8]]
        self.assertEqual(self.train.match_predictions(predictions, [[0, 0, 10, 10]], .5), [True, False])

    def test_threshold_selection_uses_validation_counts(self):
        selected = self.train.select_threshold({"tp": [8, 9], "fp": [2, 9], "fn": [2, 1]}, [.5, .1])
        self.assertEqual(selected["threshold"], .5)
        self.assertAlmostEqual(selected["precision"], .8)
        self.assertAlmostEqual(selected["recall"], .8)


if __name__ == "__main__":
    unittest.main()
