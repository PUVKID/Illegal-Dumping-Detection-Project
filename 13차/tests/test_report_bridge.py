"""실제 학습 없이 기존 보고서와 복구 계약의 연결을 검사합니다."""
import importlib.util
from pathlib import Path
import sys
import unittest
import copy
import hashlib
import json
import tempfile
import types

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


class BridgeAvailability(unittest.TestCase):
    def test_bridge_module_exists(self):
        self.assertIsNotNone(importlib.util.find_spec('report_bridge'),
                             '원본 보고서 검증에 복구 계약을 연결하는 모듈이 필요합니다.')


class BridgeContract(unittest.TestCase):
    def setUp(self):
        import report_bridge as bridge
        self.bridge=bridge
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project=Path(self.temp.name)
        fixtures=bridge.load_module('bridge_fixture12',ROOT.parent/'12차/tests/fixtures.py')
        self.reader=fixtures.Reader
        self.save=fixtures.save
        self.job=fixtures.fixture(self.project)
        self.canonical='a'*64
        self.meta={'schema':1,'job':self.job['id'],'parent_job':'fixture_parent',
                   'contract_path':'13차/work/contracts/fixture_recovery/recovery13.json',
                   'contract_sha256':'b'*64,'effective_canonical':self.canonical,
                   'legacy_id_map_sha256':'c'*64,'base_preparation_sha256':'d'*64,
                   'effective_preparation_sha256':'e'*64,'resolver_sha256':'f'*64}
        self.job['recovery13']=copy.deepcopy(self.meta)
        self.job['result']['recovery13']=copy.deepcopy(self.meta)
        self.job['resume_of']='fixture_parent'
        self.save(self.project/'7차/work/training/final.json',self.job['result'])
        self.save(self.project/'7차/work/jobs/fixture_job.json',self.job)
        reference=self.project/self.meta['contract_path']
        self.save(reference,{'fixture':True})
        self.references={self.meta['contract_path']:{'sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'bytes':reference.stat().st_size}}
        self.calls=[]
        def validate(project,job,final,expected_canonical=None):
            self.calls.append((Path(project),copy.deepcopy(job),copy.deepcopy(final),expected_canonical))
            if job.get('recovery13')!=final.get('recovery13') or expected_canonical!=self.canonical:
                raise ValueError('합성 복구 계약 불일치')
            return {'meta':copy.deepcopy(self.meta),'references':copy.deepcopy(self.references),
                    'provenance_counts':{'prior':3,'overlap':1,'union':5},
                    'limits':['과거 JPEG 재인코딩 때문에 원본 SHA 동일성을 주장하지 않는다.']}
        self.recovery=types.SimpleNamespace(validate_recovery=validate)
        self.plan={'schema':1,'project_root':str(self.project),'job_id':'fixture_job',
                   'author':'가상 작성자','output_dir':'최종/fixture_recovery',
                   'support_dir':'12차/work/fixture_recovery','deliver_formats':['docx','pdf'],
                   'recovery13_expected_canonical':self.canonical}

    def watcher(self):
        return self.bridge.load_watcher(self.project,self.plan,self.recovery)

    def test_original_root_interval_and_sources_preserved(self):
        sources=[ROOT.parent/'12차'/name for name in ('watcher.py','report_core.py','report_outputs.py','report_sections.json')]
        before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
        watcher=self.watcher()
        self.assertEqual(watcher.ROOT,ROOT.parent/'12차')
        self.assertEqual(watcher.INTERVAL_SECONDS,60)
        self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})

    def test_expected_canonical_is_mandatory(self):
        del self.plan['recovery13_expected_canonical']
        with self.assertRaises(ValueError):self.watcher()

    def test_import_aliases_are_restored(self):
        old_core=sys.modules.get('report_core')
        old_outputs=sys.modules.get('report_outputs')
        self.watcher()
        self.assertIs(sys.modules.get('report_core'),old_core)
        self.assertIs(sys.modules.get('report_outputs'),old_outputs)

    def test_base_validation_then_recovery_and_references(self):
        bundle=self.watcher().validate_bundle(self.project,self.job,self.reader.safe_read_json)
        self.assertEqual(len(self.calls),1)
        self.assertEqual(self.calls[0][-1],self.canonical)
        self.assertEqual(bundle['recovery13']['meta'],self.meta)
        self.assertEqual(bundle['references'][self.meta['contract_path']],self.references[self.meta['contract_path']])

    def test_base_failure_cannot_be_overridden_by_recovery(self):
        model=Path(self.job['result']['selected']['weights'][0])
        model.write_bytes(b'tampered')
        with self.assertRaises(ValueError):
            self.watcher().validate_bundle(self.project,self.job,self.reader.safe_read_json)
        self.assertEqual(self.calls,[])

    def test_recovery_failure_blocks_complete_bundle(self):
        self.job['recovery13']['parent_job']='other_fixture'
        with self.assertRaisesRegex(ValueError,'복구'):
            self.watcher().validate_bundle(self.project,self.job,self.reader.safe_read_json)

    def test_returned_reference_tamper_is_not_silent(self):
        (self.project/self.meta['contract_path']).write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.watcher().validate_bundle(self.project,self.job,self.reader.safe_read_json)

    def test_running_does_not_start_or_author(self):
        self.job['state']='running'
        self.save(self.project/'7차/work/jobs/fixture_job.json',self.job)
        result=self.watcher().process_once(self.plan,self.reader)
        self.assertEqual(result['state'],'waiting')
        self.assertEqual(self.calls,[])
        self.assertFalse((self.project/'최종').exists())

    def test_existing_output_is_preserved(self):
        output=self.project/'최종/fixture_recovery'
        output.mkdir(parents=True)
        (output/'old.docx').write_bytes(b'preserve')
        with self.assertRaises(FileExistsError):
            self.watcher().process_once(self.plan,self.reader)
        self.assertEqual((output/'old.docx').read_bytes(),b'preserve')

    def test_cached_receipt_revalidates_recovery(self):
        watcher=self.watcher()
        docx=self.project/'fixture.docx';docx.write_bytes(b'fixture Word')
        pdf=self.project/'fixture.pdf';pdf.write_bytes(b'fixture PDF')
        outputs=watcher.publish_pair(docx,pdf,self.project/'최종/fixture_recovery')
        receipt={'job_id':'fixture_job','state':'complete','output_dir':'최종/fixture_recovery',
                 'outputs':outputs,'input_final_sha256':watcher.digest(self.project/'7차/work/training/final.json')}
        self.save(self.project/'12차/work/fixture_recovery/completion_receipt.json',receipt)
        self.assertEqual(watcher.process_once(self.plan,self.reader),receipt)
        self.assertEqual(len(self.calls),1)
        self.recovery.validate_recovery=lambda *a,**kw: (_ for _ in ()).throw(ValueError('계약 오염'))
        with self.assertRaisesRegex(ValueError,'계약 오염'):
            watcher.process_once(self.plan,self.reader)

    def test_sections_deep_copy_and_actual_counts(self):
        sections={'title':'가상 보고서','sections':[{'id':name,'paragraphs':['원문']} for name in ('architecture','preprocess','limits')]}
        before=copy.deepcopy(sections)
        metadata=self.recovery.validate_recovery(self.project,self.job,self.job['result'],self.canonical)
        enriched=self.bridge.enrich_sections(sections,metadata,self.canonical)
        self.assertEqual(sections,before)
        text=' '.join(p for row in enriched['sections'] for p in row['paragraphs'])
        self.assertIn('3개',text)
        self.assertIn('1개',text)
        self.assertIn('5개',text)
        self.assertIn(self.meta['base_preparation_sha256'],text)
        self.assertIn('재인코딩',text)

    def test_failure_text_never_claims_completion(self):
        sections={'title':'가상 보고서','sections':[{'id':name,'paragraphs':['원문']} for name in ('architecture','preprocess','limits')]}
        enriched=self.bridge.enrich_sections(sections,failed=True)
        text=' '.join(p for row in enriched['sections'] for p in row['paragraphs'])
        self.assertIn('실효 데이터와 최종 성능은 확정하지 않는다',text)

    def test_unvalidated_bundle_cannot_author(self):
        with self.assertRaises(ValueError):
            self.watcher().create_docx('not-created.docx',{}, {},{}, {},'not-created',None)


if __name__=='__main__':
    unittest.main()
