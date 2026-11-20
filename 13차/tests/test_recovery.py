"""재개 계약의 경로·불변 입력·결과 바인딩을 검사합니다."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import patch

try:
    import recovery
except ModuleNotFoundError:
    recovery = None


def synthetic_project(directory, lifecycle=False):
    """GPU와 실제 프로젝트에 쓰지 않는 자체 동결 제어 사례를 만듭니다."""
    import verify_sources
    actual=Path(__file__).resolve().parents[2]
    project=Path(directory); root=project/'13차';root.mkdir(parents=True)
    baseline=json.loads((actual/'13차/original-baseline.json').read_text(encoding='utf-8'))
    for name in baseline['files']:
        target=project/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(actual/name,target)
    for name in verify_sources.PUBLIC_FILES:
        target=root/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(actual/'13차'/name,target)
    dependencies=json.loads((root/'source_contract.json').read_text(encoding='utf-8')).get('dependencies',{})
    for name in dependencies:
        target=project/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(actual/name,target)
    if lifecycle:
        fake=project/'7차/train_pipeline.py'
        fake.write_text("""from pathlib import Path
import time
from prepare_dataset import ROOT, prepare
def run(job,notify=lambda **kw:None,resume=False):
    notify(stage='격리 프로세스 검증 대기')
    deadline=time.monotonic()+15
    while not (ROOT/'work/release.fixture').exists():
        if time.monotonic()>deadline:raise RuntimeError('격리 fixture 대기 상한')
        time.sleep(.02)
    raise RuntimeError('격리 fixture 통제 종료: GPU와 실제 학습 없음')
""",encoding='utf-8')
        # 제어 사례 자체의 다른 가짜 파이프라인을 고정하며 제품 baseline은 수정하지 않습니다.
        baseline['files']['7차/train_pipeline.py']=hashlib.sha256(fake.read_bytes()).hexdigest()
        (root/'original-baseline.json').write_text(json.dumps(baseline,ensure_ascii=False),encoding='utf-8')
    image={'id':47668,'file_name':'site.jpg','path':'/datasets/site.jpg','width':1920,'height':1080}
    annotation={'images':[image],'annotations':[],'categories':[]}
    row={'source':'pLitterStreet','image':'/legacy/plitter_47668.jpg',
         'url':'https://zenodo.org/api/records/8288500/files/images.zip/content','sha256':'a'*64}
    source=json.loads((root/'source_contract.json').read_text(encoding='utf-8'))
    for name in source['inputs']:
        target=project/name;target.parent.mkdir(parents=True,exist_ok=True)
        if name.endswith('additional_manifest.json'):
            value=[row]
        elif name.endswith('pLitter_annotations.json') or name.endswith('annotations_all.json'):
            value=annotation
        elif name.endswith('5차/work/training/data_manifest.json'):
            value={'records':[{'source':'pLitterStreet','source_id':'47668'}]}
        elif name.endswith('annotations.zip'):
            target.write_bytes(b'identical controlled annotation archive');continue
        else:
            if (actual/name).is_file():shutil.copy2(actual/name,target)
            continue
        target.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
    source['inputs']={name:hashlib.sha256((project/name).read_bytes()).hexdigest() for name in source['inputs']}
    source['counts']={'prior':1,'previous_round5':1,'overlap':1,'union':1}
    cache=project/'7차/work/sources/downloads/cached.zip';cache.parent.mkdir(parents=True,exist_ok=True);cache.write_bytes(b'abc')
    receipt=cache.with_suffix('.zip.verified.json');receipt.write_text('{}',encoding='utf-8')
    source['cache']=[{'path':'7차/work/sources/downloads/cached.zip','size':3,
                     'md5':'900150983cd24fb0d6963f7d28e17f72',
                     'sha256':'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
                     'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest()}]
    (root/'source_contract.json').write_text(json.dumps(source,ensure_ascii=False),encoding='utf-8')
    parent=project/'7차/work/jobs/old.json';parent.parent.mkdir(parents=True,exist_ok=True)
    parent.write_text(json.dumps({'id':'old','kind':'train','state':'failed','error':'제어된 과거 오류'}),encoding='utf-8')
    canonical=verify_sources.verify_all(root=root)['canonical']
    spec,mapping,refs,map_sha=recovery.audit_inputs(project)
    contract={'schema':1,'job':'new','effective_canonical':canonical,
              'base_preparation_sha256':hashlib.sha256((project/'7차/prepare_dataset.py').read_bytes()).hexdigest(),
              'effective_preparation_sha256':hashlib.sha256((root/'effective_prepare.py').read_bytes()).hexdigest(),
              'resolver_sha256':hashlib.sha256((root/'legacy_ids.py').read_bytes()).hexdigest(),
              'source_contract_sha256':hashlib.sha256((root/'source_contract.json').read_bytes()).hexdigest(),
              'legacy_id_map_sha256':map_sha,'provenance_counts':mapping['counts'],
              'lineage':{'parent_job':'old','parent_job_sha256':hashlib.sha256(parent.read_bytes()).hexdigest()}}
    path=recovery.contract_path(project,'new');recovery.freeze(path,contract)
    recovery.freeze(path.parent/'legacy_id_map.json',mapping)
    meta=recovery._metadata(project,'new',contract,path)
    manifest=project/'7차/work/training/data_manifest.json';manifest.write_text('{"fixture":true}',encoding='utf-8')
    prepared={'schema':1,'job':'new','recovery_contract_sha256':meta['contract_sha256'],
              'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
              'base_preparation_contract_sha256':hashlib.sha256((project/'7차/work/training/preparation_contract.json').read_bytes()).hexdigest()}
    prepared_path=path.parent/'prepared.json';recovery.freeze(prepared_path,prepared)
    meta.update(prepared_path=prepared_path.relative_to(project).as_posix(),
                prepared_sha256=hashlib.sha256(prepared_path.read_bytes()).hexdigest())
    final={'manifest_sha256':prepared['manifest_sha256'],'recovery13':meta}
    job={'id':'new','kind':'train','state':'complete','resume_of':'old','params':{'resume':True},
         'recovery13':meta,'result':final}
    if lifecycle:
        manifest.unlink()
    return project,job,final,canonical


class RecoveryTests(unittest.TestCase):
    def test_explicit_resume_plan_preserves_parent_job(self):
        function = getattr(recovery, 'validate_plan', lambda value: None)
        value = function({'schema': 1, 'resume_of': 'old_job'})
        self.assertEqual(value, {'schema': 1, 'resume_of': 'old_job'})

    def test_invalid_or_extra_plan_fields_are_rejected(self):
        for value in ({}, {'schema':1,'resume_of':'../other'},
                      {'schema':1,'resume_of':'old','fresh':True},
                      {'schema':True,'resume_of':'old'}, []):
            with self.subTest(value=value), self.assertRaises(ValueError):
                recovery.validate_plan(value)

    def test_unbound_success_is_not_accepted_as_recovered_success(self):
        with self.assertRaises(ValueError):
            recovery.validate_recovery(Path(__file__).resolve().parents[2],
                {'id':'new','state':'complete'}, {})

    def test_pipeline_is_fixed_to_original_worker(self):
        root=Path(__file__).resolve().parents[2]
        self.assertEqual(recovery.validate_pipeline(root/'7차/worker.py'),
                         (root/'7차/worker.py').resolve())
        with self.assertRaises(ValueError):
            recovery.validate_pipeline(root/'13차/recovery.py')

    def test_contract_paths_cannot_escape_fixed_job_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            project=Path(directory)
            value=recovery.contract_path(project,'new')
            self.assertEqual(value,project/'13차/work/contracts/new/recovery13.json')
            for job in ('../bad','',None):
                with self.assertRaises(ValueError):recovery.contract_path(project,job)

    def test_freeze_preserves_existing_bytes_and_rejects_changed_value(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'immutable.json'
            recovery.freeze(path,{'value':1}); before=path.read_bytes()
            recovery.freeze(path,{'value':1})
            self.assertEqual(path.read_bytes(),before)
            with self.assertRaises(ValueError):recovery.freeze(path,{'value':2})
            self.assertEqual(path.read_bytes(),before)

    def test_wrong_cached_bytes_never_invoke_network(self):
        with tempfile.TemporaryDirectory() as directory:
            project=Path(directory); file=project/'cached.zip';file.write_bytes(b'bad')
            receipt=file.with_suffix('.zip.verified.json');receipt.write_text('{}',encoding='utf-8')
            spec={'path':'cached.zip','size':3,'md5':'0'*32,'sha256':'0'*64,
                  'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest()}
            with patch('urllib.request.urlopen',side_effect=AssertionError('통신 금지')):
                with self.assertRaisesRegex(ValueError,'MD5'):
                    recovery.verify_cache(project,{'cache':[spec]})

    def test_verified_cached_bytes_remain_unchanged_without_network(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            project=Path(directory); file=project/'cached.zip';file.write_bytes(b'abc')
            receipt=file.with_suffix('.zip.verified.json');receipt.write_text('{}',encoding='utf-8')
            spec={'path':'cached.zip','size':3,'md5':'900150983cd24fb0d6963f7d28e17f72',
                  'sha256':'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
                  'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest()}
            with patch('urllib.request.urlopen',side_effect=AssertionError('통신 금지')):
                result=recovery.verify_cache(project,{'cache':[spec]})
            self.assertEqual(result['cached.zip']['bytes'],3)
            self.assertEqual(file.read_bytes(),b'abc')

    def test_effective_original_downloader_reuses_finished_cache_offline(self):
        project=Path(__file__).resolve().parents[2]
        effective=recovery.module_from_path('fixture_effective_cache',project/'13차/effective_prepare.py')
        worker=recovery.module_from_path('fixture_cache_lock',project/'7차/worker.py')
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'cached.zip';target.write_bytes(b'abc')
            spec={'url':'https://example.invalid/unused.zip','size':3,
                  'md5':'900150983cd24fb0d6963f7d28e17f72','source':'controlled'}
            receipt={**{key:spec[key] for key in ('url','size','md5')},
                     'sha256':'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'}
            effective.freeze(target.with_suffix('.zip.verified.json'),receipt)
            before=target.read_bytes();budget=effective.DownloadBudget(Path(directory)/'budget')
            with patch.dict(sys.modules,{'worker':worker}),patch.object(effective,'open_request',side_effect=AssertionError('새 수신 금지')):
                output=effective.download(spec,target,budget)
            self.assertEqual(output,target)
            self.assertEqual(target.read_bytes(),before)
            self.assertEqual(budget.used,0)
            self.assertFalse(budget.path.exists())

    def test_additional_effective_ast_change_is_rejected(self):
        import verify_sources
        project=Path(__file__).resolve().parents[2]
        base=(project/'7차/prepare_dataset.py').read_text(encoding='utf-8')
        effective=(project/'13차/effective_prepare.py').read_text(encoding='utf-8')
        self.assertTrue(verify_sources.check_overlay(base,effective))
        with self.assertRaises(ValueError):
            verify_sources.check_overlay(base,effective.replace('SEED = 20261030','SEED = 9'))

    def test_complete_recovery_binding_and_each_tampered_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            project,job,final,canonical=synthetic_project(directory)
            meta=recovery.validate_recovery(project,job,final,canonical)
            self.assertEqual(meta['meta']['parent_job'],'old')
            self.assertEqual(meta['provenance_counts'],{'prior':1,'previous_round5':1,'overlap':1,'union':1})
            for field in ('contract_sha256','legacy_id_map_sha256','effective_preparation_sha256','prepared_sha256'):
                broken=copy.deepcopy(job);broken['recovery13'][field]='0'*64
                broken['result']['recovery13']=broken['recovery13']
                with self.subTest(field=field),self.assertRaises(ValueError):
                    recovery.validate_recovery(project,broken,broken['result'],canonical)

    def test_real_recovery_metadata_enters_real_report_enrichment(self):
        import report_bridge
        with tempfile.TemporaryDirectory() as directory:
            project,job,final,canonical=synthetic_project(directory)
            metadata=recovery.validate_recovery(project,job,final,canonical)
            self.assertIn('meta',metadata,'보고서 소비자가 요구하는 중첩 계약이어야 합니다.')
            sections={'sections':[{'id':name,'paragraphs':[]} for name in ('architecture','preprocess','limits')]}
            enriched=report_bridge.enrich_sections(sections,metadata,canonical)
            self.assertIn('1개',enriched['sections'][1]['paragraphs'][-1])
            self.assertIn('5b555b1c597734072be12ab46b1c0f9a74f4dbb3a84144cb3ba9c7e74fc19ced',
                          enriched['sections'][0]['paragraphs'][-1])
            self.assertEqual(sections['sections'][0]['paragraphs'],[])

    def test_other_valid_attempt_metadata_cannot_enter_queued_worker(self):
        with tempfile.TemporaryDirectory() as directory:
            project,job,final,canonical=synthetic_project(directory)
            plan=project/'13차/work/plan.json';plan.write_text('{"schema":1,"resume_of":"old"}',encoding='utf-8')
            first=recovery.contract_path(project,'new')
            second=recovery.contract_path(project,'other')
            contract=json.loads(first.read_text(encoding='utf-8'))
            contract.update(job='other',plan_sha256=hashlib.sha256(plan.read_bytes()).hexdigest())
            recovery.freeze(second,contract)
            recovery.freeze(second.parent/'legacy_id_map.json',json.loads((first.parent/'legacy_id_map.json').read_text(encoding='utf-8')))
            other_meta=recovery._metadata(project,'other',contract,second)
            queued={'id':'new','kind':'train','state':'queued','params':{'resume':True},
                    'resume_of':'old','recovery13':other_meta}
            current=project/'7차/work/jobs/new.json';current.write_text(json.dumps(queued),encoding='utf-8')
            def forbidden_worker(job_id):
                raise AssertionError('다른 시도의 유효 메타로 worker에 들어갔습니다.')
            worker=types.SimpleNamespace(WORK=project/'7차/work',read=recovery.read,execute=forbidden_worker)
            data=types.SimpleNamespace(TRAINING=project/'7차/work/training')
            training=types.SimpleNamespace(run=lambda *args,**kwargs:None,prepare=lambda **kwargs:None)
            with patch.object(recovery,'ROOT',project/'13차'),patch.object(recovery,'ORIGINAL',project/'7차'),\
                 patch.object(recovery,'originals',return_value=(worker,data,training)):
                with self.assertRaises(ValueError):
                    recovery.execute('new',project/'7차/worker.py',plan,canonical)

    def test_wrong_external_canonical_and_changed_manifest_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            project,job,final,canonical=synthetic_project(directory)
            with self.assertRaises(ValueError):recovery.validate_recovery(project,job,final,'0'*64)
            (project/'7차/work/training/data_manifest.json').write_text('{}',encoding='utf-8')
            with self.assertRaises(ValueError):recovery.validate_recovery(project,job,final,canonical)

    def test_id_map_sha_names_the_physical_immutable_file(self):
        with tempfile.TemporaryDirectory() as directory:
            project,job,final,canonical=synthetic_project(directory)
            path=recovery.contract_path(project,'new').parent/'legacy_id_map.json'
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),job['recovery13']['legacy_id_map_sha256'])

    def test_extra_comment_outside_four_text_changes_is_rejected(self):
        import verify_sources
        project=Path(__file__).resolve().parents[2]
        base=(project/'7차/prepare_dataset.py').read_text(encoding='utf-8')
        effective=(project/'13차/effective_prepare.py').read_text(encoding='utf-8')
        with self.assertRaises(ValueError):
            verify_sources.check_overlay(base,effective+'\n# 허용되지 않은 추가 설명\n')

    def test_reformatted_id_map_is_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            project,job,final,canonical=synthetic_project(directory)
            path=recovery.contract_path(project,'new').parent/'legacy_id_map.json'
            path.write_bytes(path.read_bytes()+b'\n')
            with self.assertRaises(ValueError):recovery.validate_recovery(project,job,final,canonical)

    def test_changed_font_dependency_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            project,job,final,canonical=synthetic_project(directory)
            font=project/'10차/web/fonts/NanumGothic-Bold.ttf'
            font.write_bytes(b'changed')
            with self.assertRaises(ValueError):recovery.validate_recovery(project,job,final,canonical)

    @unittest.skipUnless(os.name=='posix','실제 Linux flock과 /proc 프로세스 검사는 Docker에서 수행합니다.')
    def test_linux_original_worker_liveness_duplicate_start_and_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            project,_,_,canonical=synthetic_project(directory,lifecycle=True)
            plan=project/'13차/work/plan.json';plan.write_text('{"schema":1,"resume_of":"old"}',encoding='utf-8')
            argv=[sys.executable,'-B','-X','utf8',str(project/'13차/recovery.py'),
                  '--pipeline',str(project/'7차/worker.py'),'--plan',str(plan),
                  '--expected-canonical',canonical,'--start']
            before=(project/'7차/work/jobs/old.json').read_bytes()
            child=None
            try:
                result=subprocess.run(argv,cwd=project/'7차',capture_output=True,text=True,timeout=15)
                self.assertEqual(result.returncode,0,result.stderr)
                launched=json.loads(result.stdout);child=launched['pid'];job_path=project/'7차/work/jobs'/(launched['job']+'.json')
                deadline=time.monotonic()+8
                while time.monotonic()<deadline:
                    value=json.loads(job_path.read_text(encoding='utf-8'))
                    if value.get('stage')=='격리 프로세스 검증 대기':break
                    time.sleep(.03)
                self.assertEqual(value['state'],'running',value)
                worker=recovery.module_from_path('fixture_original_worker',project/'7차/worker.py')
                self.assertTrue(worker.is_alive(child,launched['job']))
                repeated=subprocess.run(argv,cwd=project/'7차',capture_output=True,text=True,timeout=10)
                self.assertNotEqual(repeated.returncode,0)
                self.assertIn('이미 진행',repeated.stderr)
                (project/'7차/work/release.fixture').write_text('release',encoding='utf-8')
                deadline=time.monotonic()+8
                while time.monotonic()<deadline:
                    value=json.loads(job_path.read_text(encoding='utf-8'))
                    if value.get('state')=='failed' and not worker.is_alive(child,launched['job']):break
                    time.sleep(.03)
                self.assertEqual(value['state'],'failed',value)
                self.assertIn('격리 fixture 통제 종료',value['error'])
                self.assertEqual(value['resume_of'],'old')
                self.assertEqual((project/'7차/work/jobs/old.json').read_bytes(),before)
            finally:
                (project/'7차/work/release.fixture').write_text('release',encoding='utf-8')
                if child:
                    deadline=time.monotonic()+5
                    while time.monotonic()<deadline and Path('/proc',str(child),'stat').is_file():
                        stat=Path('/proc',str(child),'stat').read_text()
                        if stat.rsplit(') ',1)[1].split()[0]=='Z':break
                        time.sleep(.03)


if __name__=='__main__':
    unittest.main()
