"""배포 파일의 문자·구문과 의존 원본 불변을 검사합니다."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ['dashboard.py', 'pipeline.py', 'launcher.py', 'verify_sources.py', 'tests/test_adapter.py',
          'web/index.html', 'web/app.js', 'web/style.css', 'web/fonts/NanumGothic-Bold.ttf', 'web/fonts/OFL.txt', 'docs/5차대비.diff',
          'docs/original_sources.json', 'docs/설계.md', '사용안내.md', '변경기록.md']


def main():
    checked = 0
    for name in PUBLIC:
        path = ROOT / name
        if not path.is_file():
            raise ValueError('필수 배포 파일이 없습니다: ' + name)
        if path.suffix != '.ttf':
            text = path.read_bytes().decode('utf-8-sig', errors='strict')
            if '\ufffd' in text:
                raise ValueError('대체 문자가 있습니다: ' + name)
            if path.suffix == '.py':
                ast.parse(text, filename=name)
        checked += 1
    manifest = json.loads((ROOT / 'docs/original_sources.json').read_text(encoding='utf-8'))
    for name, expected in manifest.items():
        actual = hashlib.sha256((ROOT.parent / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('보존 원본이 변경됐습니다: ' + name)
    print(json.dumps({'ok': True, 'public_files': checked, 'preserved_dependencies': len(manifest),
                      'limit': '문자·구문·필수 파일·고정 원본 해시 검사이며 의미상 완전 무오류 보장은 아닙니다.'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
