"""배포 파일과 엄격 UTF-8 및 보존한 원본 해시를 검사합니다."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC_FILES = (
    'report_core.py','report_outputs.py','watcher.py','verify_sources.py','report_sections.json',
    'README.md','변경기록.md','ROUTING-LESSONS.md','docs/설계.md','docs/요구사항.md',
    'docs/계획서식.json','docs/렌더설정서식.json','docs/source_contract.json','docs/결과해시스키마.json',
    'tests/fixtures.py','tests/test_report.py','tests/test_watcher.py','tests/test_outputs.py','tests/make_fixture.py')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_json(text):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:
                raise ValueError('중복 JSON 키: '+key)
            result[key]=value
        return result
    def reject(value):
        raise ValueError('비유한 JSON 수치: '+value)
    return json.loads(text,object_pairs_hook=unique,parse_constant=reject)


def verify():
    text_count=0
    for name in PUBLIC_FILES:
        path=ROOT/name
        if not path.is_file():
            raise ValueError('필수 공개 파일 없음: '+name)
        text=path.read_bytes().decode('utf-8',errors='strict')
        if '\ufffd' in text:
            raise ValueError('대체 문자 포함: '+name)
        text_count+=1
        if path.suffix=='.py':
            ast.parse(text,filename=name)
        elif path.suffix=='.json':
            strict_json(text)
    contract=strict_json((ROOT/'docs/source_contract.json').read_text(encoding='utf-8'))
    originals=contract['round7_originals']
    for name,expected in originals.items():
        if sha(ROOT.parent/'7차'/name)!=expected:
            raise ValueError('7차 원본 불변 위반: '+name)
    for name,expected in contract['dependencies'].items():
        if sha(ROOT.parent/name)!=expected:
            raise ValueError('고정 의존 파일 불일치: '+name)
    if sha(ROOT/'report_sections.json')!=contract['narrative_sha256']:
        raise ValueError('별도 담당자가 동결한 본문이 변경됐습니다.')
    for name in ('docx','PIL','pdf2image'):
        if importlib.util.find_spec(name) is None:
            raise ValueError('필수 문서 의존 모듈 없음: '+name)
    print(f'공개 파일 {text_count}개 엄격 UTF-8·구문 검사, 7차 원본 {len(originals)}개와 의존 {len(contract["dependencies"])}개 해시 대조 통과. 렌더 성공 판정은 별도입니다.')


if __name__=='__main__':
    verify()
