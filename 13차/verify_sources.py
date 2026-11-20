"""원본 불변과 네 지점의 실효 변환 및 전체 공개 제품을 대조합니다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PUBLIC_FILES = (
    'legacy_ids.py', 'effective_prepare.py', 'recovery.py', 'verify_sources.py',
    'original-baseline.json', 'source_contract.json', 'report_bridge.py',
    'tests/test_legacy_ids.py', 'tests/test_recovery.py', 'tests/test_report_bridge.py',
    'README.md', '변경기록.md', 'ROUTING-LESSONS.md',
    'docs/요구사항.md', 'docs/설계.md', 'docs/보고서.md',
)


def hash_file(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            result.update(block)
    return result.hexdigest()


def check_overlay(base, effective):
    """원본에서 허용된 네 AST 변화만 구성한 뒤 전체 트리를 비교합니다."""
    newline='\r\n' if '\r\n' in base else '\n'
    replacements=(
        ('from pathlib import Path, PurePosixPath',
         'from pathlib import Path, PurePosixPath'+newline+'from legacy_ids import legacy_match'),
        ('ROOT = Path(__file__).resolve().parent',
         "ROOT = Path(__file__).resolve().parent.parent / '7차'"),
        ("match=re.search(r'street_(\\d+)',row['image'])","match=legacy_match(row['image'])"),
        ("'preparation_sha256':sha256_file(__file__)",
         "'preparation_sha256':sha256_file(ROOT/'prepare_dataset.py')"),
    )
    expected_text=base
    for before,after in replacements:
        if expected_text.count(before)!=1:
            raise ValueError('원본의 유일한 텍스트 변환 지점을 확인할 수 없습니다.')
        expected_text=expected_text.replace(before,after,1)
    if effective!=expected_text:
        raise ValueError('네 허용 지점 이외에 주석·공백·개행을 포함한 텍스트 변화가 있습니다.')
    tree = ast.parse(base)
    counts = [0, 0, 0]
    for index, node in enumerate(tree.body):
        if isinstance(node, ast.ImportFrom) and node.module == 'pathlib':
            tree.body.insert(index+1, ast.ImportFrom(module='legacy_ids',
                names=[ast.alias(name='legacy_match')], level=0))
            break
    else:
        raise ValueError('원본 import 경계를 확인할 수 없습니다.')

    class Allowed(ast.NodeTransformer):
        def visit_Assign(self, node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='ROOT':
                counts[0]+=1
                node.value=ast.parse("Path(__file__).resolve().parent.parent / '7차'",mode='eval').body
            return self.generic_visit(node)

        def visit_Call(self, node):
            if (isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name)
                    and node.func.value.id=='re' and node.func.attr=='search'
                    and len(node.args)==2 and isinstance(node.args[0],ast.Constant)
                    and node.args[0].value==r'street_(\d+)' and not node.keywords):
                counts[1]+=1
                return ast.Call(func=ast.Name(id='legacy_match',ctx=ast.Load()),args=[node.args[1]],keywords=[])
            if (isinstance(node.func,ast.Name) and node.func.id=='sha256_file'
                    and len(node.args)==1 and isinstance(node.args[0],ast.Name)
                    and node.args[0].id=='__file__' and not node.keywords):
                counts[2]+=1
                node.args=[ast.parse("ROOT/'prepare_dataset.py'",mode='eval').body]
            return self.generic_visit(node)

    expected = Allowed().visit(tree)
    if counts != [1,1,1] or ast.dump(expected,include_attributes=False) != ast.dump(ast.parse(effective),include_attributes=False):
        raise ValueError('네 허용 지점 이외의 실효 준비 코드 변화가 있습니다.')
    return True


def verify_all(expected_canonical=None, root=ROOT):
    root=Path(root).resolve()
    if expected_canonical is not None and (not isinstance(expected_canonical,str)
            or not re.fullmatch('[a-f0-9]{64}',expected_canonical)):
        raise ValueError('외부 동결 canonical은 SHA-256이어야 합니다.')
    baseline=json.loads((root/'original-baseline.json').read_text(encoding='utf-8'))
    references={}
    source_contract=json.loads((root/'source_contract.json').read_text(encoding='utf-8'))
    expected_sources=list(baseline['files'].items())+list(source_contract.get('dependencies',{}).items())
    for name,expected in expected_sources:
        path=root.parent/name
        if (Path(name).is_absolute() or '..' in Path(name).parts
                or not path.resolve().is_relative_to(root.parent)):
            raise ValueError('보존 원본 경계 밖의 상대 경로입니다.')
        if path.is_symlink() or not path.is_file() or hash_file(path)!=expected:
            raise ValueError('보존 원본이 달라졌습니다: '+name)
        references[name]={'sha256':expected,'bytes':path.stat().st_size}
    files={}
    for name in PUBLIC_FILES:
        path=root/name
        if path.is_symlink() or not path.is_file():
            raise ValueError('공개 제품 파일이 없거나 링크입니다: '+name)
        raw=path.read_bytes()
        text=raw.decode('utf-8',errors='strict')
        if '\ufffd' in text:
            raise ValueError('대체 문자가 포함된 제품입니다: '+name)
        if path.suffix=='.py':
            compile(text,str(path),'exec')
        elif path.suffix=='.json':
            json.loads(text)
        files[name]=hashlib.sha256(raw).hexdigest()
    check_overlay((root.parent/'7차/prepare_dataset.py').read_bytes().decode('utf-8'),
                  (root/'effective_prepare.py').read_bytes().decode('utf-8'))
    canonical=hashlib.sha256(''.join(name+'\0'+files[name]+'\n' for name in sorted(files)).encode('utf-8')).hexdigest()
    if expected_canonical is not None and canonical!=expected_canonical:
        raise ValueError('실효13차 전체 제품 canonical이 외부 동결값과 다릅니다.')
    return {'canonical':canonical,'files':files,'originals':references,
            'product_count':len(files),'original_count':len(references),'allowed_ast_changes':4}


def main():
    parser=argparse.ArgumentParser(description='13차 원본 및 실효 소스 검증')
    parser.add_argument('--expected-canonical')
    args=parser.parse_args()
    print(json.dumps(verify_all(args.expected_canonical),ensure_ascii=False))


if __name__=='__main__':
    main()
