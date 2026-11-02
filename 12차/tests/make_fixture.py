"""문서 품질 점검용 합성 결과만 생성하며 운영 작업을 읽지 않습니다."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fixtures import fixture, Reader
from report_core import validate_bundle, reconstruct_curves, load_sections
from report_outputs import create_docx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--font', required=True)
    parser.add_argument('--author', default='작성자')
    args = parser.parse_args()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    project = output/'synthetic_project'
    job = fixture(project)
    bundle = validate_bundle(project, job, Reader.safe_read_json)
    curves = reconstruct_curves(project, bundle, Reader)
    epochs = {'fixture_candidate': [{'epoch': i,'metrics/precision(B)':.2+i*.1,'metrics/recall(B)':.25+i*.08,'metrics/mAP50(B)':.2+i*.05} for i in range(1,5)]}
    sections = load_sections(ROOT/'report_sections.json', Reader.safe_read_json)
    receipt = create_docx(output/'가상결과_보고서_편집초안.docx',sections,bundle,curves,epochs,
                          output/'support',args.font,args.author,fixture=True)
    print('가상 결과 Word 편집초안 저장, 렌더 미완료:', output)
    print(receipt)


if __name__ == '__main__':
    main()
