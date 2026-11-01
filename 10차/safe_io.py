"""원자 교체를 막지 않는 읽기 전용 파일 접근을 제공합니다."""
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path

_WINDOWS = os.name == 'nt'
_kernel32 = None
if _WINDOWS:
    _kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    _kernel32.CreateFileW.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    ]
    _kernel32.CreateFileW.restype = wintypes.HANDLE
    _kernel32.ReadFile.argtypes = [
        wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID,
    ]
    _kernel32.ReadFile.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL


def _windows_error(path):
    error = ctypes.WinError(ctypes.get_last_error())
    error.filename = str(path)
    return error


def _read_windows_bytes(path):
    # 읽기 권한만 요청하며 다른 프로세스의 쓰기·삭제·원자 교체를 허용합니다.
    handle = _kernel32.CreateFileW(str(path), 0x80000000, 0x1 | 0x2 | 0x4,
                                   None, 3, 0x80, None)
    if handle == ctypes.c_void_p(-1).value:
        raise _windows_error(path)
    try:
        chunks = []
        buffer = ctypes.create_string_buffer(64 * 1024)
        size = wintypes.DWORD()
        while True:
            if not _kernel32.ReadFile(handle, buffer, len(buffer), ctypes.byref(size), None):
                raise _windows_error(path)
            if not size.value:
                return b''.join(chunks)
            chunks.append(buffer.raw[:size.value])
    finally:
        if not _kernel32.CloseHandle(handle):
            raise _windows_error(path)


def safe_read_text(path, encoding='utf-8'):
    """기존 호출자의 경로 검증을 유지하며 엄격하게 텍스트를 읽습니다."""
    path = Path(path)
    if not _WINDOWS:
        return path.read_text(encoding=encoding)
    # 핸들을 먼저 닫으므로 디코딩 오류도 열린 핸들을 남기지 않습니다.
    text = _read_windows_bytes(path).decode(encoding, errors='strict')
    return text.replace('\r\n', '\n').replace('\r', '\n')


def safe_read_json(path, default=None):
    """파일이 없을 때만 기본값을 반환하고 해독·JSON·접근 오류는 전파합니다."""
    try:
        text = safe_read_text(path, encoding='utf-8')
    except FileNotFoundError:
        return default
    return json.loads(text)
