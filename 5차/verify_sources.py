"""소스의 UTF-8·문법과 납품 파일 존재를 검사합니다."""
import ast
from pathlib import Path

root = Path(__file__).resolve().parent
paths = list(root.glob("*.py")) + list((root / "tests").glob("*.py"))
for path in paths:
    text = path.read_text(encoding="utf-8", errors="strict")
    if "\ufffd" in text:
        raise ValueError(f"대체문자 발견: {path}")
    ast.parse(text, filename=str(path))
for name in ["pipeline.py", "gpu_worker.py", "dashboard.py", "launcher.py", "prepare_training.py", "train_pipeline.py", "web/index.html", "실행.bat", "사용안내.txt"]:
    if not (root / name).is_file():
        raise FileNotFoundError(name)
print(f"소스 {len(paths)}개 UTF-8·문법 및 필수 파일 검사 통과")
