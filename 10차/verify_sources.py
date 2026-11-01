"""10차 배포 소스·공식 의존·보존 원본을 직접 검사합니다."""
import ast
import hashlib
import json
from safe_io import safe_read_json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = ['safe_io.py','pipeline.py','dashboard.py','launcher.py','verify_sources.py','대시보드실행.bat',
            'web/index.html','web/app.js','web/scene.js','web/presentation.js','web/style.css',
            'web/fonts/NanumGothic-Bold.ttf','web/fonts/OFL.txt','web/assets/brand-leaf.png',
            'docs/설계.md','docs/original_sources.json','docs/vendor-manifest.json','docs/icon-manifest.json',
            'tests/test_safe_io.py','tests/test_adapter.py','tests/test_presentation.py','tests/test_presentation.cjs']


def main():
    for name in REQUIRED:
        if not (ROOT / name).is_file(): raise ValueError('필수 파일이 없습니다: ' + name)
    checked = 0
    suffixes = {'.py','.js','.cjs','.json','.md','.html','.css','.svg','.txt','.bat'}
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if not path.is_file() or relative.parts[0] in ('evidence','work','.codex') or path.suffix not in suffixes: continue
        text = path.read_bytes().decode('utf-8-sig', errors='strict')
        if '\ufffd' in text: raise ValueError('대체 문자가 있습니다: ' + str(relative))
        if path.suffix == '.py': ast.parse(text, filename=str(relative))
        checked += 1
    original = safe_read_json(ROOT / 'docs/original_sources.json')
    for name, expected in original.items():
        if hashlib.sha256((ROOT.parent / name).read_bytes()).hexdigest() != expected:
            raise ValueError('이전 원본이 변경됐습니다: ' + name)
    vendor_count=0
    for manifest in ('vendor-manifest.json','icon-manifest.json'):
        for row in safe_read_json(ROOT/'docs'/manifest):
            if hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest() != row['sha256']:
                raise ValueError('공식 의존 파일이 다릅니다: ' + row['file'])
            vendor_count += 1
    print(json.dumps({'ok':True,'text_files':checked,'required_files':len(REQUIRED),'preserved_sources':len(original),'official_dependencies':vendor_count,'limit':'UTF-8·Python AST·필수 파일·해시 검사이며 실제 브라우저·운영 동작 및 독립 검증을 대신하지 않습니다.'},ensure_ascii=False))


if __name__ == '__main__': main()
