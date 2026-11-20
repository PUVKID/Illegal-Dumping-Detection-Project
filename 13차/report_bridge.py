"""원본 보고서를 보존하면서 재개 실험의 추가 계약을 연결합니다."""
import argparse
from contextlib import contextmanager
import copy
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parent
BASE_ROOT=ROOT.parent/'12차'


def load_module(name, path):
    spec=importlib.util.spec_from_file_location(name,Path(path))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextmanager
def import_aliases(values):
    """기존 모듈의 import 이름만 잠시 연결하고 외부 모듈 상태를 복원합니다."""
    before={name:sys.modules.get(name) for name in values}
    absent={name for name in values if name not in sys.modules}
    sys.modules.update(values)
    try:
        yield
    finally:
        for name in values:
            if name in absent:
                sys.modules.pop(name,None)
            else:
                sys.modules[name]=before[name]


def enrich_sections(sections, recovery_metadata=None, expected_canonical=None, failed=False):
    """측정값과 원문을 바꾸지 않고 복구 범위와 한계만 덧붙입니다."""
    result=copy.deepcopy(sections)
    by_id={row['id']:row for row in result['sections']}
    additions={
        'architecture':'원래 7차 준비 코드의 고정 계약을 보존하고 13차의 실효 실행 코드와 ID 대응 복구 계약을 별도로 동결하였다. 두 계약의 SHA-256을 구분하여 원본 코드가 바뀐 것처럼 기록하지 않았다.',
        'preprocess':'보존 이미지의 파일명과 공식 주석 및 과거 저장 코드의 대응을 확인하여 원본 ID를 복구하였다. 과거 JPEG는 재인코딩됐으므로 보존 파일의 SHA-256과 새 공식 원본의 SHA-256이 서로 같다는 뜻은 아니다. 모호하거나 확인되지 않은 ID는 추정으로 채우지 않는다.',
        'limits':'이전 실패 시도와 당시 미완료 보고서는 보존하고 재개 시도를 별도로 연결하였다. ID 대응과 실행 복구는 성능 향상을 입증하는 실험이 아니며, 고정 테스트의 실제 결과와 정밀도·재현율 목표 판정은 기존 기준으로 보고한다.'}
    if failed:
        additions['limits']+=' 이번 재개 시도도 정상 완료되지 않았다면 실효 데이터와 최종 성능은 확정하지 않는다.'
    elif recovery_metadata is not None:
        meta=recovery_metadata['meta']
        counts=recovery_metadata['provenance_counts']
        additions['architecture']+=' 결과와 작업에 저장된 복구 메타데이터를 고정 계약과 대조하였다.'
        if expected_canonical is not None:
            additions['architecture']+=' 검증한 실효 코드 묶음의 SHA-256은 '+expected_canonical+'이다.'
        additions['architecture']+=' 기준 준비 코드 SHA-256은 '+meta['base_preparation_sha256']+'이며 실효 준비 코드 SHA-256은 '+meta['effective_preparation_sha256']+'이다.'
        additions['preprocess']+=f" 복구 원장의 이전 사용 기록은 {counts['prior']}개, 중복은 {counts['overlap']}개, 과거 사용 합집합은 {counts['union']}개로 확인하였다."
        if recovery_metadata['limits']:
            additions['limits']+=' '+' '.join(recovery_metadata['limits'])
    for name,text in additions.items():
        if name not in by_id:
            raise ValueError('기존 보고서에 필요한 절이 없습니다: '+name)
        by_id[name]['paragraphs'].append(text)
    return result


def load_watcher(project, plan, recovery_module=None):
    """12차의 원본 함수와 경계를 유지하고 추가 검증만 연결합니다."""
    project=Path(project).resolve()
    if Path(plan['project_root']).resolve()!=project:
        raise ValueError('계획과 지정 프로젝트가 다릅니다.')
    expected=plan.get('recovery13_expected_canonical')
    if not isinstance(expected,str) or not re.fullmatch('[a-f0-9]{64}',expected):
        raise ValueError('비공개 계획의 13차 실효 canonical SHA-256이 필요합니다.')
    core=load_module('bridge_round12_core',BASE_ROOT/'report_core.py')
    with import_aliases({'report_core':core}):
        outputs=load_module('bridge_round12_outputs',BASE_ROOT/'report_outputs.py')
    with import_aliases({'report_core':core,'report_outputs':outputs}):
        watcher=load_module('bridge_round12_watcher',BASE_ROOT/'watcher.py')
    recovery=recovery_module if recovery_module is not None else load_module('bridge_round13_recovery',ROOT/'recovery.py')
    original_validate=watcher.validate_bundle
    original_receipt=watcher.verify_receipt
    original_create=watcher.create_docx

    def validate(project_root,job,read_json):
        bundle=original_validate(project_root,job,read_json)
        metadata=recovery.validate_recovery(project_root,job,bundle['final'],expected_canonical=expected)
        if not isinstance(metadata,dict):
            raise ValueError('복구 검증 메타데이터가 객체가 아닙니다.')
        bundle['recovery13']=copy.deepcopy(metadata)
        for name,reference in metadata['references'].items():
            verified={}
            core.verify_hash(core.local_path(name,project_root),reference['sha256'],verified,project_root)
            actual=verified[name]
            if actual!=reference:
                raise ValueError('복구 근거의 크기와 해시가 다릅니다: '+name)
            if name in bundle['references'] and bundle['references'][name]!=actual:
                raise ValueError('기본 계약과 복구 계약의 파일 대응이 충돌합니다: '+name)
            bundle['references'][name]=actual
        return bundle

    def verify_receipt(receipt,private_plan,project_root,output,reader):
        value=original_receipt(receipt,private_plan,project_root,output,reader)
        if receipt['state']=='complete':
            job=reader.safe_read_json(core.job_path(project_root,private_plan['job_id']))
            validate(project_root,job,reader.safe_read_json)
        return value

    def create_docx(path,sections,bundle,curves,epochs,support,font_path,author='작성자',fixture=False,failure=None):
        metadata=bundle.get('recovery13') if bundle is not None else None
        if bundle is not None and metadata is None:
            raise ValueError('복구 검증 전에 정상 완료 보고서를 만들 수 없습니다.')
        enriched=enrich_sections(sections,metadata,expected,failed=failure is not None)
        return original_create(path,enriched,bundle,curves,epochs,support,font_path,
                               author=author,fixture=fixture,failure=failure)

    watcher.validate_bundle=validate
    watcher.verify_receipt=verify_receipt
    watcher.create_docx=create_docx
    return watcher


def main():
    parser=argparse.ArgumentParser(description='재개 실험의 Word 및 동일 원고 PDF 보고서 연결')
    parser.add_argument('--plan',required=True,help='새 작업의 비공개 계획 JSON')
    parser.add_argument('--once',action='store_true')
    args=parser.parse_args()
    # 별도 고정 계획을 읽을 뿐 이전 계획이나 운영 작업 JSON을 수정하지 않습니다.
    plan=json.loads(Path(args.plan).read_text(encoding='utf-8'))
    watcher=load_watcher(plan['project_root'],plan)
    before=sys.argv
    try:
        sys.argv=[str(BASE_ROOT/'watcher.py'),'--plan',args.plan]+(['--once'] if args.once else [])
        watcher.main()
    finally:
        sys.argv=before


if __name__=='__main__':
    main()
