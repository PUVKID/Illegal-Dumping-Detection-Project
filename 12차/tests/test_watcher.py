"""운영 작업 없이 1회 생성과 불완료 및 보안 경계를 검사합니다."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fixtures import fixture, Reader, save
from watcher import process_once, publish_pair, validate_plan, watch_lock


class WatcherContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.job = fixture(self.project)
        self.plan = {'schema':1,'project_root':str(self.project),'job_id':'fixture_job',
                     'output_dir':'최종/fixture','support_dir':'12차/work/fixture',
                     'deliver_formats':['docx','pdf'],'author':'작성자','font':'font.ttf',
                     'marker':{},'renderer_config':str(self.project/'renderer.json')}
        self.job_file = self.project/'7차/work/jobs/fixture_job.json'
        save(self.job_file,self.job)

    def test_running_never_calls_authoring_or_renderer(self):
        self.job['state']='running'
        save(self.job_file,self.job)
        def forbidden(*args):
            self.fail('진행 중에는 문서 저작이나 렌더를 호출할 수 없습니다.')
        result=process_once(self.plan,Reader,forbidden,forbidden)
        self.assertEqual(result['state'],'waiting')
        self.assertFalse((self.project/'최종').exists())

    def test_stale_running_remains_running(self):
        self.job.update(state='running',updated=1)
        save(self.job_file,self.job)
        result=process_once(self.plan,Reader)
        self.assertEqual(result['state'],'waiting')
        self.assertTrue(result['stale'])
        self.assertEqual(result['process_liveness'],'미검증')

    def test_complete_without_renderer_stays_blocked(self):
        result=process_once(self.plan,Reader)
        self.assertEqual(result['state'],'blocked_renderer')
        self.assertFalse((self.project/'최종').exists())

    def test_failed_does_not_use_past_success_metrics(self):
        self.job.update(state='failed',error='합성 오류')
        save(self.job_file,self.job)
        result=process_once(self.plan,Reader)
        self.assertEqual(result['job_state'],'failed')
        self.assertEqual(result['state'],'blocked_renderer')

    def test_existing_output_is_never_overwritten(self):
        target=self.project/'최종/fixture'
        target.mkdir(parents=True)
        (target/'old.txt').write_text('preserve',encoding='utf-8')
        with self.assertRaises(FileExistsError):
            process_once(self.plan,Reader)
        self.assertEqual((target/'old.txt').read_text(encoding='utf-8'),'preserve')

    def test_completed_receipt_prevents_repeated_generation(self):
        support=self.project/'12차/work/fixture'
        from report_core import digest
        docx=self.project/'draft.docx';docx.write_bytes(b'fixture docx')
        pdf=self.project/'same.pdf';pdf.write_bytes(b'fixture pdf')
        outputs=publish_pair(docx,pdf,self.project/'최종/fixture')
        receipt={'job_id':'fixture_job','state':'complete','outputs':outputs,'output_dir':'최종/fixture',
                 'input_final_sha256':digest(self.project/'7차/work/training/final.json')}
        save(support/'completion_receipt.json',receipt)
        self.assertEqual(process_once(self.plan,Reader),receipt)

    def test_receipt_without_output_files_is_rejected(self):
        save(self.project/'12차/work/fixture/completion_receipt.json',
             {'job_id':'fixture_job','state':'complete','outputs':{}})
        with self.assertRaises(ValueError):
            process_once(self.plan,Reader)
        self.assertFalse((self.project/'최종').exists())

    def test_changed_output_is_not_reused(self):
        self.test_completed_receipt_prevents_repeated_generation()
        (self.project/'최종/fixture/최종보고서.pdf').write_bytes(b'changed')
        with self.assertRaises(ValueError):
            process_once(self.plan,Reader)

    def test_changed_final_is_not_reused(self):
        self.test_completed_receipt_prevents_repeated_generation()
        final=self.job['result'];final['finished']=1700000100
        save(self.project/'7차/work/training/final.json',final)
        with self.assertRaises(ValueError):
            process_once(self.plan,Reader)

    def test_other_output_directory_is_not_reused(self):
        self.test_completed_receipt_prevents_repeated_generation()
        self.plan['output_dir']='최종/other'
        with self.assertRaises(ValueError):
            process_once(self.plan,Reader)

    def test_lock_rejects_second_observer(self):
        path=self.project/'observer.lock'
        with watch_lock(path):
            with self.assertRaises(RuntimeError):
                with watch_lock(path):
                    self.fail('중복 관찰 잠금이 허용됐습니다.')

    def test_lock_releases_after_exception(self):
        path=self.project/'observer.lock'
        with self.assertRaises(ValueError):
            with watch_lock(path):
                raise ValueError('제어 오류')
        with watch_lock(path):
            self.assertTrue(path.exists())

    def test_output_contains_exactly_docx_and_pdf(self):
        docx=self.project/'draft.docx'
        pdf=self.project/'same.pdf'
        docx.write_bytes(b'fixture docx')
        pdf.write_bytes(b'fixture same-source pdf')
        target=self.project/'최종/pair'
        result=publish_pair(docx,pdf,target)
        self.assertEqual(set(result),{'최종보고서.docx','최종보고서.pdf'})
        self.assertEqual(len(list(target.iterdir())),2)

    def test_plan_rejects_html_delivery(self):
        self.plan['deliver_formats']=['docx','pdf','html']
        with self.assertRaises(ValueError):
            validate_plan(self.plan)

    def test_plan_rejects_external_support(self):
        self.plan['support_dir']='../outside'
        with self.assertRaises(ValueError):
            validate_plan(self.plan)
