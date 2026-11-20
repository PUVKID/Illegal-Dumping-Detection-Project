"""원본 계약과 실효 복구 계약을 함께 고정하고 같은 실험만 이어갑니다."""
import argparse
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time
import traceback
import uuid

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / '7차'


def module_from_path(name, path):
    spec=importlib.util.spec_from_file_location(name,Path(path))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(path):
    result=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            result.update(block)
    return result.hexdigest()


def identity(value):
    if not isinstance(value,str) or not re.fullmatch('[A-Za-z0-9_-]{1,100}',value):
        raise ValueError('작업 ID 형식이 올바르지 않습니다.')
    return value


def relative_file(project, name):
    project=Path(project).resolve()
    if not isinstance(name,str) or '\\' in name or ':' in name:
        raise ValueError('프로젝트 내부 상대 경로가 필요합니다.')
    value=PurePosixPath(name)
    if value.is_absolute() or '..' in value.parts:
        raise ValueError('프로젝트 경계를 벗어난 경로입니다.')
    path=project.joinpath(*value.parts)
    if path.is_symlink() or not path.resolve().is_relative_to(project):
        raise ValueError('근거 파일 경계가 올바르지 않습니다.')
    return path


def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        encoded=(json.dumps(value,ensure_ascii=False,allow_nan=False,sort_keys=True,
                            separators=(',',':'))+'\n').encode('utf-8')
        temporary.write_bytes(encoded)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def freeze(path,value):
    path=Path(path)
    if path.exists():
        if read(path)!=value:
            raise ValueError('복구 불변 계약이 변경됐습니다: '+path.name)
    else:
        atomic_json(path,value)


def validate_plan(value):
    if (not isinstance(value,dict) or set(value)!={'schema','resume_of'}
            or type(value.get('schema')) is not int or value['schema']!=1):
        raise ValueError('계획은 schema1과 resume_of만 포함해야 합니다.')
    identity(value['resume_of'])
    return dict(value)


def validate_pipeline(value):
    path=Path(value)
    if path.is_symlink() or path.resolve()!=(ORIGINAL/'worker.py').resolve() or not path.is_file():
        raise ValueError('보존7차 작업자 경로만 허용합니다.')
    return path.resolve()


def contract_path(project,job):
    return Path(project)/'13차/work/contracts'/identity(job)/'recovery13.json'


def verify_runtime(project,expected_canonical):
    if not isinstance(expected_canonical,str) or not re.fullmatch('[a-f0-9]{64}',expected_canonical):
        raise ValueError('실제 기동에는 외부 동결 canonical이 필요합니다.')
    validator=module_from_path('pbl13_source_validator',Path(project)/'13차/verify_sources.py')
    return validator.verify_all(expected_canonical,root=Path(project)/'13차')


def audit_inputs(project):
    """공식 주석과 보존 생성 코드의 대응을 다시 계산합니다. GPU는 불러오지 않습니다."""
    project=Path(project).resolve()
    spec=read(project/'13차/source_contract.json')
    refs={}
    for name,expected in spec['inputs'].items():
        path=relative_file(project,name)
        if not path.is_file() or digest(path)!=expected:
            raise ValueError('보존 입력이 고정값과 다릅니다: '+name)
        refs[name]={'sha256':expected,'bytes':path.stat().st_size}
    ids=module_from_path('pbl13_legacy_id_audit',project/'13차/legacy_ids.py')
    archived=project/'이전 도커 실험/3차실험/trash_round3/sources'
    previous=read(project/'5차/work/training/data_manifest.json')
    previous_ids=[str(r['source_id']) for r in previous['records'] if r.get('source')=='pLitterStreet']
    mapping=ids.provenance_map(read(archived/'additional_manifest.json'),
        read(archived/'pLitter_annotations.json'),
        read(project/'7차/work/sources/raw/pLitterStreet/annotations/10_class_splits/annotations_all.json'),
        previous_ids)
    if mapping['counts']!=spec['counts']:
        raise ValueError('보존 ID 전수 집계가 동결값과 다릅니다.')
    return spec,mapping,refs,ids.map_digest(mapping)


def verify_cache(project,spec,metadata_only=False,notify=lambda **kw:None):
    """기존 완성 파일만 읽습니다. 이 함수는 네트워크와 새 수신을 사용하지 않습니다."""
    result={}
    for row in spec['cache']:
        path=relative_file(project,row['path'])
        receipt=path.with_suffix(path.suffix+'.verified.json')
        if not path.is_file() or path.stat().st_size!=row['size'] or not receipt.is_file():
            raise ValueError('완료 원자료 캐시가 없습니다. 새로 수신하지 않습니다: '+path.name)
        if digest(receipt)!=row['receipt_sha256']:
            raise ValueError('기존 원자료 검증 영수증이 다릅니다: '+path.name)
        if not metadata_only:
            notify(stage='완료 원자료 캐시 MD5·SHA 재검사',source=row.get('source'),file=path.name)
            before=path.stat(); md5=hashlib.md5();sha=hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda:stream.read(4*1024*1024),b''):
                    md5.update(block);sha.update(block)
            after=path.stat()
            if (before.st_size!=after.st_size or before.st_mtime_ns!=after.st_mtime_ns
                    or md5.hexdigest()!=row['md5'] or sha.hexdigest()!=row['sha256']):
                raise ValueError('공식 크기·MD5·보존SHA와 캐시가 다릅니다: '+path.name)
        result[row['path']]={'sha256':row['sha256'],'bytes':row['size']}
    return result


def _metadata(project,job,contract,contract_file):
    return {'schema':1,'job':job,'parent_job':contract['lineage']['parent_job'],
            'contract_path':contract_file.relative_to(project).as_posix(),
            'contract_sha256':digest(contract_file),
            'effective_canonical':contract['effective_canonical'],
            'legacy_id_map_sha256':contract['legacy_id_map_sha256'],
            'base_preparation_sha256':contract['base_preparation_sha256'],
            'effective_preparation_sha256':contract['effective_preparation_sha256'],
            'resolver_sha256':contract['resolver_sha256']}


def _source_binding(project,meta,expected_canonical):
    project=Path(project).resolve()
    if not isinstance(meta,dict) or type(meta.get('schema')) is not int or meta['schema']!=1:
        raise ValueError('실효 복구 메타데이터가 없습니다.')
    job=identity(meta.get('job')); parent=identity(meta.get('parent_job'))
    if job==parent:
        raise ValueError('재개 작업과 부모 작업은 구분돼야 합니다.')
    expected_canonical=expected_canonical or meta.get('effective_canonical')
    runtime=verify_runtime(project,expected_canonical)
    path=contract_path(project,job)
    if meta.get('contract_path')!=path.relative_to(project).as_posix() or not path.is_file():
        raise ValueError('복구 계약 경로가 지정 작업과 다릅니다.')
    contract=read(path)
    base=_metadata(project,job,contract,path)
    if any(meta.get(key)!=value for key,value in base.items()) or base['effective_canonical']!=runtime['canonical']:
        raise ValueError('작업과 실효 소스 및 복구 계약이 다릅니다.')
    if (contract.get('schema')!=1 or contract.get('job')!=job
            or contract.get('source_contract_sha256')!=digest(project/'13차/source_contract.json')
            or contract.get('base_preparation_sha256')!=digest(project/'7차/prepare_dataset.py')
            or contract.get('effective_preparation_sha256')!=digest(project/'13차/effective_prepare.py')
            or contract.get('resolver_sha256')!=digest(project/'13차/legacy_ids.py')):
        raise ValueError('원본과 실효 복구 소스의 합성 계약이 다릅니다.')
    spec,mapping,refs,mapping_hash=audit_inputs(project)
    ids_path=path.parent/'legacy_id_map.json'
    ids=module_from_path('pbl13_legacy_binding',project/'13차/legacy_ids.py')
    if (contract['legacy_id_map_sha256']!=mapping_hash or not ids_path.is_file()
            or digest(ids_path)!=mapping_hash
            or ids.map_digest(read(ids_path))!=mapping_hash or read(ids_path)!=mapping):
        raise ValueError('동결한 보존 ID 대응과 현재 공식 입력이 다릅니다.')
    parent_path=project/'7차/work/jobs'/(parent+'.json')
    lineage=contract['lineage']
    old=read(parent_path)
    if (lineage.get('parent_job')!=parent or lineage.get('parent_job_sha256')!=digest(parent_path)
            or old.get('id')!=parent or old.get('kind')!='train'
            or old.get('state') not in ('failed','interrupted')):
        raise ValueError('재개 부모의 실패 기록이 동결 계보와 다릅니다.')
    refs.update(runtime['originals'])
    for name,expected in runtime['files'].items():
        file=project/'13차'/name
        refs['13차/'+name]={'sha256':expected,'bytes':file.stat().st_size}
    for file in (path,ids_path,project/'13차/source_contract.json',parent_path):
        refs[file.relative_to(project).as_posix()]={'sha256':digest(file),'bytes':file.stat().st_size}
    return base,contract,spec,mapping,refs


def _prepared_binding(project,meta,contract_sha256):
    project=Path(project).resolve();job=identity(meta['job'])
    path=contract_path(project,job).parent/'prepared.json'
    if (meta.get('prepared_path')!=path.relative_to(project).as_posix() or not path.is_file()
            or meta.get('prepared_sha256')!=digest(path)):
        raise ValueError('준비 완료의 별도 불변 영수증이 없습니다.')
    prepared=read(path);manifest=project/'7차/work/training/data_manifest.json'
    if (prepared.get('schema')!=1 or prepared.get('job')!=job
            or prepared.get('recovery_contract_sha256')!=contract_sha256
            or prepared.get('manifest_sha256')!=digest(manifest)
            or prepared.get('base_preparation_contract_sha256')!=digest(project/'7차/work/training/preparation_contract.json')):
        raise ValueError('실효 복구와 실제 준비 manifest의 바인딩이 다릅니다.')
    return prepared,path


def validate_recovery(project,job,final,expected_canonical=None):
    """보고서가 원본 계약만으로 실효 전체를 완료라고 쓰지 않게 검사합니다."""
    project=Path(project).resolve()
    meta=job.get('recovery13') if isinstance(job,dict) else None
    if (not isinstance(meta,dict) or not isinstance(final,dict) or final.get('recovery13')!=meta
            or job.get('state')!='complete' or job.get('result')!=final
            or job.get('id')!=meta.get('job') or job.get('resume_of')!=meta.get('parent_job')
            or job.get('params')!={'resume':True}):
        raise ValueError('정상 완료 작업과 최종 결과의 복구 태그가 일치하지 않습니다.')
    base,contract,spec,mapping,refs=_source_binding(project,meta,expected_canonical)
    prepared,path=_prepared_binding(project,meta,base['contract_sha256'])
    if final.get('manifest_sha256')!=prepared['manifest_sha256']:
        raise ValueError('최종 평가 manifest가 실효 준비 영수증과 다릅니다.')
    refs[path.relative_to(project).as_posix()]={'sha256':digest(path),'bytes':path.stat().st_size}
    for name in ('effective_prepare.py','legacy_ids.py','recovery.py','verify_sources.py'):
        file=project/'13차'/name
        refs[file.relative_to(project).as_posix()]={'sha256':digest(file),'bytes':file.stat().st_size}
    return {'meta':dict(meta),'references':refs,'provenance_counts':mapping['counts'],
            'limits':[spec['normalization_limit'],spec['base_contract_scope']]}


def originals():
    sys.path.insert(0,str(ORIGINAL))
    modules=tuple(importlib.import_module(name) for name in ('worker','prepare_dataset','train_pipeline'))
    if any(Path(module.__file__).resolve().parent!=ORIGINAL.resolve() for module in modules):
        raise ValueError('다른 프로젝트의 작업자를 실행할 수 없습니다.')
    return modules


def _read_plan(path):
    path=Path(path).resolve()
    if not path.is_relative_to((ROOT/'work').resolve()) or path.is_symlink() or not path.is_file():
        raise ValueError('기동 계획은13차 비공개 work 안에 있어야 합니다.')
    return path,validate_plan(read(path))


def start(pipeline,plan_path,expected_canonical):
    validate_pipeline(pipeline)
    if os.name!='posix':
        raise ValueError('실제 재개는 동일 Docker2026/Linux에서만 수행합니다.')
    project=ROOT.parent
    verify_runtime(project,expected_canonical)
    plan_path,plan=_read_plan(plan_path)
    spec,mapping,refs,mapping_hash=audit_inputs(project)
    verify_cache(project,spec,metadata_only=True)
    worker,data,training=originals()
    with worker.file_lock(worker.WORK/'jobs/start.lock'):
        worker._reconcile()
        if any(row.get('state') in worker.ACTIVE for row in worker.jobs()):
            raise ValueError('준비 또는 학습 작업이 이미 진행 중입니다.')
        with worker.file_lock(worker.WORK/'run.lock',blocking=False):
            pass
        parent_path=worker.WORK/'jobs'/(plan['resume_of']+'.json')
        parent=worker.read(parent_path)
        if (not parent or parent.get('id')!=plan['resume_of'] or parent.get('kind')!='train'
                or parent.get('state') not in ('failed','interrupted')):
            raise ValueError('명시한 부모는 보존된 실패 또는 중단 학습 작업이어야 합니다.')
        if (data.TRAINING/'final.json').exists():
            raise ValueError('이미 최종 결과가 있습니다. 자동으로 새 실험을 시작하지 않습니다.')
        if (data.TRAINING/'data_manifest.json').exists():
            old_meta=parent.get('recovery13')
            if not isinstance(old_meta,dict):
                raise ValueError('실효 복구 근거 없는 기존 manifest를 이어 쓸 수 없습니다.')
            _source_binding(project,old_meta,expected_canonical)
            _prepared_binding(project,old_meta,old_meta['contract_sha256'])
        job=time.strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:8]
        path=contract_path(project,job)
        contract={'schema':1,'job':job,'effective_canonical':expected_canonical,
            'base_preparation_sha256':digest(ORIGINAL/'prepare_dataset.py'),
            'effective_preparation_sha256':digest(ROOT/'effective_prepare.py'),
            'resolver_sha256':digest(ROOT/'legacy_ids.py'),
            'source_contract_sha256':digest(ROOT/'source_contract.json'),
            'legacy_id_map_sha256':mapping_hash,'provenance_counts':mapping['counts'],
            'lineage':{'parent_job':plan['resume_of'],'parent_job_sha256':digest(parent_path)},
            'plan_sha256':digest(plan_path),'scope':spec['base_contract_scope']}
        freeze(path.parent/'legacy_id_map.json',mapping)
        freeze(path,contract)
        meta=_metadata(project,job,contract,path)
        argv=[sys.executable,'-u','-B','-X','utf8',str(ROOT/'recovery.py'),
              '--pipeline',str(validate_pipeline(pipeline)),'--plan',str(plan_path),
              '--expected-canonical',expected_canonical,'--worker',job]
        worker.save(worker.WORK/'jobs'/(job+'.json'),{'id':job,'kind':'train','state':'queued',
            'params':{'resume':True},'resume_of':plan['resume_of'],'recovery13':meta,
            'recovery13_state':'source_frozen','argv':argv,'created':time.time(),
            'stage':'동일 실험의 원본ID 복구 시작 대기'})
        try:
            with (worker.WORK/'jobs'/(job+'.log')).open('ab') as log:
                child=subprocess.Popen(argv,cwd=str(ORIGINAL),stdin=subprocess.DEVNULL,
                    stdout=log,stderr=subprocess.STDOUT,shell=False,start_new_session=True)
            worker._update(job,pid=child.pid)
        except BaseException as error:
            with (worker.WORK/'jobs'/(job+'.log')).open('a',encoding='utf-8') as log:
                log.write(traceback.format_exc());log.flush()
            worker._update(job,state='failed',error=str(error),finished=time.time())
            raise
    return {'job':job,'pid':child.pid,'state':'queued','resume_of':plan['resume_of']}


def execute(job,pipeline,plan_path,expected_canonical):
    identity(job);validate_pipeline(pipeline)
    project=ROOT.parent
    verify_runtime(project,expected_canonical)
    plan_path,plan=_read_plan(plan_path)
    worker,data,training=originals()
    current=worker.read(worker.WORK/'jobs'/(job+'.json'))
    meta=current.get('recovery13') if isinstance(current,dict) else None
    params=current.get('params') if isinstance(current,dict) else None
    if (not isinstance(current,dict) or current.get('id')!=job
            or current.get('kind')!='train' or current.get('state')!='queued'
            or params!={'resume':True} or params.get('resume') is not True
            or current.get('resume_of')!=plan['resume_of']
            or not isinstance(meta,dict) or meta.get('job')!=job
            or meta.get('parent_job')!=plan['resume_of']):
        raise ValueError('대기 작업과 재개 계획이 다릅니다.')
    base,contract,spec,mapping,refs=_source_binding(project,meta,expected_canonical)
    if contract['plan_sha256']!=digest(plan_path):
        raise ValueError('실제 실행 계획이 시작 계약과 다릅니다.')
    effective=module_from_path('pbl13_effective_preparation',ROOT/'effective_prepare.py')
    original_run=training.run;original_prepare=training.prepare
    sealed={}

    def prepare_bound(notify=lambda **kw:None):
        manifest=effective.prepare(notify=notify)
        # 원장 재합산이나 새 수신은 이 복구의 허용 범위가 아닙니다.
        for name,expected in spec['inputs'].items():
            if digest(relative_file(project,name))!=expected:
                raise ValueError('준비 중 보존 입력 또는 전송 원장이 변경됐습니다: '+name)
        receipt={'schema':1,'job':job,'recovery_contract_sha256':base['contract_sha256'],
                 'manifest_sha256':digest(data.TRAINING/'data_manifest.json'),
                 'base_preparation_contract_sha256':digest(data.TRAINING/'preparation_contract.json')}
        prepared=contract_path(project,job).parent/'prepared.json'
        freeze(prepared,receipt)
        sealed.update(base,prepared_path=prepared.relative_to(project).as_posix(),prepared_sha256=digest(prepared))
        worker.update(job,recovery13=dict(sealed),recovery13_state='prepared')
        return manifest

    def wrapped(current_job,notify,resume):
        if current_job!=job or resume is not True:
            raise ValueError('동일 작업의 명시적 재개만 허용합니다.')
        verify_cache(project,spec,notify=notify)
        result=original_run(current_job,notify=notify,resume=True)
        if not sealed:
            raise ValueError('실효 준비 영수증이 없어 정상 완료할 수 없습니다.')
        final_path=data.TRAINING/'final.json'
        if read(final_path)!=result:
            raise ValueError('원래 파이프라인의 결과와 저장 파일이 다릅니다.')
        if 'recovery13' in result and result['recovery13']!=sealed:
            raise ValueError('기존 결과의 복구 계약을 덮어쓸 수 없습니다.')
        result={**result,'recovery13':dict(sealed)}
        data.atomic_json(final_path,result)
        return result

    training.prepare=prepare_bound
    training.run=wrapped
    try:
        worker.execute(job)
    finally:
        training.run=original_run
        training.prepare=original_prepare


def main():
    parser=argparse.ArgumentParser(description='동결한 마지막 실험의 원본ID 복구 재개')
    parser.add_argument('--pipeline',required=True)
    parser.add_argument('--plan',required=True)
    parser.add_argument('--expected-canonical',required=True)
    choice=parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--start',action='store_true')
    choice.add_argument('--worker')
    args=parser.parse_args()
    if args.start:
        print(json.dumps(start(args.pipeline,args.plan,args.expected_canonical),ensure_ascii=False))
    else:
        execute(args.worker,args.pipeline,args.plan,args.expected_canonical)


if __name__=='__main__':
    main()
