"""문서의 실측·가상 구분과 렌더 차단을 검사합니다."""
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from report_outputs import percent, render_document, create_docx


class OutputContract(unittest.TestCase):
    def test_missing_value_is_not_zero(self):
        self.assertEqual(percent(None),'미측정')
        self.assertEqual(percent(0),'0.00%')

    def test_unapproved_renderer_never_executes(self):
        with self.assertRaisesRegex(RuntimeError,'승인'):
            render_document('not-created.docx','not-created',None)

    def test_fixture_docx_labels_fake_values(self):
        # 별도 저작 없이 현재 저작한 제어 사례를 검사합니다.
        path=ROOT/'work/fixture_docx_v1/가상결과_보고서_편집초안.docx'
        if not path.exists():
            self.skipTest('비공개 시각 검토용 사례는 공개 배포에 포함하지 않습니다.')
        with ZipFile(path) as archive:
            text=archive.read('word/document.xml').decode('utf-8')
        self.assertIn('가상 결과',text)
        self.assertIn('실제 실험 성능이 아니며',text)
        self.assertIn('정의하지 않음',text)
        self.assertIn('선택 checkpoint의 epoch',text)
        self.assertIn('미확인',text)

    def test_author_setting_is_separate_from_static_narrative(self):
        from docx import Document
        narrative={'title':'가상 보고서','sections':[], 'references':[]}
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'draft.docx'
            create_docx(output,narrative,None,{}, {},Path(directory)/'support',None,
                        author='가상 작성자',fixture=True,failure={'state':'failed','stage':'제어 사례'})
            document=Document(output)
            self.assertEqual(document.core_properties.author,'가상 작성자')
            self.assertTrue(any('가상 작성자' in p.text for p in document.paragraphs))
            self.assertNotIn('author',narrative)

    def test_document_styles_and_table_grid_follow_explicit_layout(self):
        from docx import Document
        from docx.oxml.ns import qn
        from docx.shared import Mm
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'draft.docx'
            create_docx(output,{'title':'가상 보고서','sections':[]},None,{}, {},
                        Path(directory)/'support',None,failure={'state':'failed'})
            document=Document(output)
            self.assertIsNone(document.styles['Title']._element.find(qn('w:pPr')).find(qn('w:pBdr')))
            for name in ('Normal','Title','Heading 1','Heading 2'):
                fonts=document.styles[name]._element.rPr.rFonts
                self.assertFalse(any(k.rsplit('}',1)[-1].lower().endswith('theme') for k in fonts.attrib))
                self.assertEqual(fonts.get(qn('w:eastAsia')),'NanumGothic')
            widths=[col.w for col in document.tables[0]._tbl.tblGrid.gridCol_lst]
            self.assertLess(abs(widths[0]-Mm(35)),1000)
            self.assertLess(abs(widths[1]-Mm(137)),1000)
