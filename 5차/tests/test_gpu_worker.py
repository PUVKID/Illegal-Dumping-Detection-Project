"""중단 작업과 재사용 PID를 실제 실행 작업으로 오인하지 않는지 확인합니다."""
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
import gpu_worker


class WorkerOwnershipTests(unittest.TestCase):
    def test_deployment_uses_selected_validation_resolution(self):
        function = Mock()
        gpu_worker.configured_predict(function, {"imgsz": 1280})("models", "image", conf=.17)
        function.assert_called_once_with("models", "image", imgsz=1280, conf=.17)

    def test_past_model_keeps_past_resolution(self):
        function = Mock()
        gpu_worker.configured_predict(function, {})("models", "image")
        function.assert_called_once_with("models", "image", imgsz=1536)

    def test_same_pid_with_another_command_is_not_our_job(self):
        with patch.object(Path, "read_text", return_value="22 (python) S 1 2"), patch.object(Path, "read_bytes", return_value=b"other-program\x00job-a\x00"):
            self.assertFalse(gpu_worker.is_alive(22, "job-a"))

    def test_worker_identity_and_command_must_match(self):
        command = b"python\0" + str(Path(gpu_worker.__file__).resolve()).encode() + b"\0--worker\0job-a\0"
        with patch.object(Path, "read_text", return_value="22 (python) S 1 2"), patch.object(Path, "read_bytes", return_value=command):
            self.assertTrue(gpu_worker.is_alive(22, "job-a"))
            self.assertFalse(gpu_worker.is_alive(22, "job-b"))

    def test_zombie_worker_is_not_running(self):
        command = str(Path(gpu_worker.__file__).resolve()).encode() + b"\0job-a\0"
        with patch.object(Path, "read_text", return_value="22 (python) Z 1 2"), patch.object(Path, "read_bytes", return_value=command):
            self.assertFalse(gpu_worker.is_alive(22, "job-a"))
