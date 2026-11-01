"""읽기 공유, 엄격한 오류 처리와 핸들 정리를 실제 임시 파일로 검사합니다."""
import ctypes
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import safe_io

ROOT = Path(__file__).resolve().parents[1]
WINDOWS = os.name == 'nt'


class SafeReadTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / 'work' / 'safe-io'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_korean_json_and_pathlike(self):
        path = self.root / '한글 상태.json'
        value = {'단계': '자료 다운로드', '바이트': 123}
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        self.assertEqual(safe_io.safe_read_json(path), value)
        self.assertEqual(safe_io.safe_read_json(str(path)), value)

    def test_universal_newline_matches_path_read_text(self):
        path = self.root / 'newlines.txt'
        path.write_bytes('첫째\r\n둘째\r셋째\n'.encode('utf-8'))
        self.assertEqual(safe_io.safe_read_text(path), path.read_text(encoding='utf-8'))

    def test_explicit_encoding(self):
        path = self.root / 'utf16.txt'
        path.write_text('한글\r\n자료', encoding='utf-16', newline='')
        self.assertEqual(safe_io.safe_read_text(path, encoding='utf-16'), '한글\n자료')

    def test_multibyte_text_crosses_read_chunks(self):
        path = self.root / 'large.txt'
        text = '가' * 90000 + '끝'
        path.write_text(text, encoding='utf-8')
        self.assertEqual(safe_io.safe_read_text(path), text)

    def test_empty_text_and_json_error(self):
        path = self.root / 'empty.json'
        path.write_bytes(b'')
        self.assertEqual(safe_io.safe_read_text(path), '')
        with self.assertRaises(json.JSONDecodeError):
            safe_io.safe_read_json(path, default={})

    def test_missing_json_returns_only_given_default(self):
        default = object()
        self.assertIs(safe_io.safe_read_json(self.root / 'missing.json', default), default)
        self.assertIsNone(safe_io.safe_read_json(self.root / 'missing.json'))

    def test_missing_text_and_parent_raise(self):
        for path in (self.root / 'missing.txt', self.root / 'missing' / 'state.json'):
            with self.subTest(path=path):
                with self.assertRaises(FileNotFoundError):
                    safe_io.safe_read_text(path)

    def test_invalid_utf8_is_not_default(self):
        path = self.root / 'invalid.json'
        path.write_bytes(b'{"value":"\xff"}')
        with self.assertRaises(UnicodeDecodeError):
            safe_io.safe_read_json(path, default={})

    def test_invalid_json_is_not_default(self):
        path = self.root / 'invalid.json'
        path.write_text('{"unfinished":', encoding='utf-8')
        with self.assertRaises(json.JSONDecodeError):
            safe_io.safe_read_json(path, default={})

    def test_directory_is_not_missing(self):
        with self.assertRaises(OSError):
            safe_io.safe_read_json(self.root, default={})

    @unittest.skipUnless(WINDOWS, 'Windows 공유 모드 전용 검사입니다.')
    def test_delete_share_allows_replace_during_read_and_keeps_snapshot(self):
        path = self.root / 'state.json'
        replacement = self.root / 'replacement.json'
        path.write_text('이전 상태', encoding='utf-8')
        replacement.write_text('새 상태', encoding='utf-8')
        native_read = safe_io._kernel32.ReadFile
        replaced = False

        def replace_during_read(*args):
            nonlocal replaced
            if not replaced:
                # 실제 운영처럼 Linux 바인드 마운트에서 원자 교체합니다.
                prefix = '/workspace/2026/'
                source = prefix + replacement.relative_to(Path('D:/2026')).as_posix()
                target = prefix + path.relative_to(Path('D:/2026')).as_posix()
                argv = ['docker', 'exec', '-w', '/workspace/2026/월요일 PBL/10차',
                        '2026', '/opt/venvs/torch/bin/python', '-B', '-X', 'utf8',
                        '-c', 'import os,sys; os.replace(sys.argv[1],sys.argv[2])',
                        source, target]
                result = subprocess.run(argv, cwd=ROOT, capture_output=True,
                                        encoding='utf-8', errors='strict',
                                        timeout=12, shell=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                replaced = True
            return native_read(*args)

        with mock.patch.object(safe_io._kernel32, 'ReadFile', side_effect=replace_during_read):
            self.assertEqual(safe_io.safe_read_text(path), '이전 상태')
        self.assertTrue(replaced)
        self.assertEqual(safe_io.safe_read_text(path), '새 상태')

    @unittest.skipUnless(WINDOWS, 'Windows 공유 모드 전용 검사입니다.')
    def test_real_sharing_permission_error_propagates(self):
        path = self.root / 'exclusive.json'
        path.write_text('{}', encoding='utf-8')
        kernel = safe_io._kernel32
        handle = kernel.CreateFileW(str(path), 0x80000000, 0, None, 3, 0x80, None)
        self.assertNotEqual(handle, ctypes.c_void_p(-1).value)
        try:
            with self.assertRaises(PermissionError):
                safe_io.safe_read_json(path, default={})
        finally:
            self.assertTrue(kernel.CloseHandle(handle))

    @unittest.skipUnless(WINDOWS, 'Windows 핸들 전용 검사입니다.')
    def test_native_read_error_closes_handle_and_propagates(self):
        path = self.root / 'state.txt'
        path.write_text('자료', encoding='utf-8')
        kernel = safe_io._kernel32
        native_close = kernel.CloseHandle
        closed = []

        def fail_read(*args):
            ctypes.set_last_error(5)
            return 0

        def record_close(handle):
            closed.append(handle)
            return native_close(handle)

        with mock.patch.object(kernel, 'ReadFile', side_effect=fail_read):
            with mock.patch.object(kernel, 'CloseHandle', side_effect=record_close):
                with self.assertRaises(PermissionError):
                    safe_io.safe_read_text(path)
        self.assertEqual(len(closed), 1)

    @unittest.skipUnless(WINDOWS, 'Windows 핸들 전용 검사입니다.')
    def test_decode_and_encoding_failures_do_not_leak_handles(self):
        from ctypes import wintypes
        kernel = safe_io._kernel32
        kernel.GetCurrentProcess.argtypes = []
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        kernel.GetProcessHandleCount.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.GetProcessHandleCount.restype = wintypes.BOOL

        def count():
            value = wintypes.DWORD()
            self.assertTrue(kernel.GetProcessHandleCount(kernel.GetCurrentProcess(), ctypes.byref(value)))
            return value.value

        path = self.root / 'invalid.txt'
        path.write_bytes(b'\xff')
        before = count()
        for _ in range(30):
            with self.assertRaises(UnicodeDecodeError):
                safe_io.safe_read_text(path)
            with self.assertRaises(LookupError):
                safe_io.safe_read_text(path, encoding='없는-인코딩')
        self.assertEqual(count(), before)


if __name__ == '__main__':
    unittest.main()
