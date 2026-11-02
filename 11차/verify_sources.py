"""외부에서 고정한 11차 전체 해시와 7차 원본 불변을 검사합니다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PRODUCTS = ('README.md', 'docs/복구설계.md', 'original-baseline.json', 'recover.py', 'tests/test_recover.py', 'verify_sources.py', '변경기록.md')


def snapshot():
    files = {}
    for name in PRODUCTS:
        path = ROOT / name
        if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
            raise ValueError('제품 파일의 링크를 허용하지 않습니다.')
        raw = path.read_bytes()
        text = raw.decode('utf-8', errors='strict')
        if '\ufffd' in text:
            raise ValueError('대체 문자가 있습니다: ' + name)
        if path.suffix == '.py':
            ast.parse(text, filename=name)
        elif path.suffix == '.json':
            json.loads(text)
        files[name] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in {'evidence', 'work'} or '__pycache__' in relative.parts:
            continue
        if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
            raise ValueError('제품 경로의 링크를 허용하지 않습니다.')
        if path.is_file() and relative.as_posix() not in files:
            raise ValueError('동결 목록에 없는 제품 파일입니다: ' + relative.as_posix())
    canonical = json.dumps(files, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return files, hashlib.sha256(canonical).hexdigest()


def main():
    parser = argparse.ArgumentParser(description='11차 동결 해시·엄격 UTF-8·구문·7차 원본 불변 검사')
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--expected-digest')
    choice.add_argument('--print-digest', action='store_true')
    args = parser.parse_args()
    files, digest = snapshot()
    import recover
    baseline = recover.verify_original()
    if args.expected_digest and (not re.fullmatch(r'[0-9a-f]{64}', args.expected_digest) or digest != args.expected_digest):
        raise ValueError('외부 검사 명세에 고정한 11차 해시와 다릅니다.')
    print(json.dumps({'mode': '동결 후보 계산' if args.print_digest else '외부 고정값 검증', 'digest': digest,
        'checked_sources': len(files), 'original_files': len(baseline), 'files': files, 'utf8': 'strict', 'syntax': 'pass'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
