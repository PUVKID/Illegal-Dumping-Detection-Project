"""검증된 결과로 Word 초안과 비공개 표·그림을 만듭니다."""
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from report_core import source_splits

LABELS = {'historical_taco': '과거 TACO 고정 테스트', 'new_plastopol': 'PlastOPol 고정 테스트',
          'source_heldout_uav': 'UAVVaste 외부 출처 테스트'}


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + '\n', encoding='utf-8')


def percent(value):
    return '미측정' if value is None else f'{value * 100:.2f}%'


def csv_file(path, rows, headers):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows({k: row.get(k) for k in headers} for row in rows)


def plot(path, title, series, font_path, x_label, y_label, x_max=1., y_max=1.):
    """축과 단위 및 범례가 있는 정적 그래프를 별도 분석 도구 없이 그립니다."""
    image = Image.new('RGB', (1500, 870), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(font_path), 25)
    title_font = ImageFont.truetype(str(font_path), 34)
    draw.text((95, 26), title, font=title_font, fill='#111827')
    left, top, width, height = 125, 110, 1260, 565
    for i in range(6):
        t = i / 5
        y = top + height * (1-t)
        x = left + width * t
        draw.line((left, y, left+width, y), fill='#dbe2e0', width=2)
        draw.text((35, y-13), f'{t*y_max:.2f}', font=font, fill='#374151')
        draw.text((x-18, top+height+15), f'{t*x_max:.2f}', font=font, fill='#374151')
    draw.line((left, top, left, top+height, left+width, top+height), fill='#374151', width=3)
    draw.text((left, 78), y_label, font=font, fill='#374151')
    draw.text((left+width-240, top+height+57), x_label, font=font, fill='#374151')
    colors = ['#07865f', '#2563eb', '#b45309', '#7c3aed']
    for i, (name, points) in enumerate(series):
        color = colors[i % len(colors)]
        positions = [(left+max(0,min(1,x/x_max))*width, top+(1-max(0,min(1,y/y_max)))*height)
                     for x, y in points]
        if len(positions) > 1:
            draw.line(positions, fill=color, width=4)
        if len(positions) == 1:
            x, y = positions[0]
            draw.ellipse((x-5,y-5,x+5,y+5), fill=color)
        lx = 115 + (i % 2) * 650
        ly = 775 + (i // 2) * 38
        draw.line((lx, ly+14, lx+40, ly+14), fill=color, width=5)
        draw.text((lx+53, ly), name, font=font, fill='#374151')
    if not any(points for _, points in series):
        draw.text((510, 360), '측정된 곡선 없음', font=title_font, fill='#6b7280')
    image.save(path)


def table(document, headers, rows, widths=None):
    item = document.add_table(rows=1, cols=len(headers))
    item.autofit = False
    if widths:
        for column, grid, width in zip(item.columns,item._tbl.tblGrid.gridCol_lst,widths):
            column.width=Mm(width)
            grid.w=Mm(width)
    for i, text in enumerate(headers):
        item.rows[0].cells[i].text = str(text)
    repeat = OxmlElement('w:tblHeader')
    item.rows[0]._tr.get_or_add_trPr().append(repeat)
    for row in rows:
        cells = item.add_row().cells
        for i, text in enumerate(row):
            cells[i].text = str(text)
    for row in item.rows:
        for i, cell in enumerate(row.cells):
            if widths:
                cell.width = Mm(widths[i])
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(4)
                paragraph.paragraph_format.space_before = Pt(4)
                for run in paragraph.runs:
                    run.font.size = Pt(9)
            props = cell._tc.get_or_add_tcPr()
            borders = OxmlElement('w:tcBorders')
            for side in ('top', 'left', 'bottom', 'right'):
                edge = OxmlElement('w:' + side)
                for key, val in (('val','single'),('sz','4'),('color','D9D9D9')):
                    edge.set(qn('w:'+key), val)
                borders.append(edge)
            props.append(borders)
    for cell in item.rows[0].cells:
        fill = OxmlElement('w:shd')
        fill.set(qn('w:fill'), 'F0F3F2')
        cell._tc.get_or_add_tcPr().append(fill)
    document.add_paragraph()


def create_docx(path, sections, bundle, curves, epochs, support, font_path, author='작성자', fixture=False, failure=None):
    """저작 전 마커는 이 함수를 호출하는 진입점에서 실행해야 합니다."""
    support = Path(support)
    support.mkdir(parents=True, exist_ok=True)
    document = Document()
    sec = document.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.top_margin, sec.bottom_margin = Mm(20), Mm(19)
    sec.left_margin = sec.right_margin = Mm(19)
    style_ids={'Normal','Title','Heading1','Heading2','TitleChar','Heading1Char','Heading2Char'}
    for style in document.styles:
        if style.style_id not in style_ids:
            continue
        style.font.name = 'NanumGothic'
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string('111827')
        fonts=style._element.get_or_add_rPr().rFonts
        for attribute in list(fonts.attrib):
            if attribute.rsplit('}',1)[-1].lower().endswith('theme'):
                del fonts.attrib[attribute]
        for script in ('ascii','hAnsi','eastAsia','cs'):
            fonts.set(qn('w:'+script),'NanumGothic')
    # 기본 문서 양식의 제목 장식선을 제거하고 검은 제목만 남깁니다.
    title_props=document.styles['Title']._element.find(qn('w:pPr'))
    if title_props is not None:
        for border in list(title_props.findall(qn('w:pBdr'))):
            title_props.remove(border)
    normal = document.styles['Normal']
    normal.font.size = Pt(10)
    normal.paragraph_format.line_spacing = 1.25
    normal.paragraph_format.space_after = Pt(6)
    document.styles['Title'].font.size = Pt(23)
    document.styles['Heading 1'].font.size = Pt(15)
    document.styles['Heading 2'].font.size = Pt(12)
    footer = sec.footer.paragraphs[0]
    footer.alignment = 2
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    footer._p.append(field)
    document.add_heading(sections['title'], 0)
    document.add_paragraph('최종 실험 보고서' if not failure else '실험 미완료 보고서')
    document.add_paragraph('작성자 ' + author)
    document.add_paragraph('작성일 ' + datetime.now().astimezone().strftime('%Y년 %m월 %d일'))
    if fixture:
        document.add_paragraph('가상 결과를 사용한 제어 사례입니다. 아래 수치는 실제 실험 성능이 아니며 최종 결과로 사용할 수 없습니다.')
    document.add_paragraph('이 보고서는 진행 중이던 마지막 실험의 동결 기록을 설명한다. 추가 학습이나 새로운 데이터 수신을 실행하지 않는다.')
    if failure:
        document.add_heading('확인한 미완료 상태', 1)
        document.add_paragraph('지정 실험이 정상 완료되지 않아 성능과 목표 달성 여부를 확정하지 않았다. 받은 자료와 기존 결과는 보존한다.')
        table(document, ['항목', '관측값'], [('상태', failure['state']), ('단계', failure.get('stage','미확인')),
                                        ('오류 원문', failure.get('error') or '기록 없음'), ('성능 및 목표', '미측정')], [35,137])
    final = bundle['final'] if bundle else None
    tests = final['tests'] if final else {}
    charts = []
    if final:
        rows = []
        for name, result in tests.items():
            op = result['operating']
            rows.append(dict(test=name, **op, AP50=result['metrics']['AP50'], AP50_95=result['metrics']['AP50_95']))
            csv_file(support / (name+'_curve.csv'), curves[name], ['threshold','precision','recall','f1','tp','fp','fn'])
        csv_file(support / 'test_metrics.csv', rows, ['test','precision','recall','f1','tp','fp','fn','threshold','AP50','AP50_95'])
        splits = source_splits(bundle['manifest'])
        csv_file(support / 'source_splits.csv', splits, ['source','split','augmentation','images'])
        pr = support / 'precision_recall.png'
        plot(pr, '고정 테스트의 정밀도 재현율 곡선', [(LABELS[k],[(r['recall'],r['precision']) for r in v]) for k,v in curves.items()],font_path,'재현율','정밀도')
        f1 = support / 'f1_threshold.png'
        plot(f1, '고정 테스트의 신뢰도별 F1', [(LABELS[k],[(r['threshold'],r['f1']) for r in v]) for k,v in curves.items()],font_path,'신뢰도 임계값','F1')
        charts = [pr,f1]
    for section in sections['sections']:
        document.add_heading(section['title'], 1)
        for paragraph in section['paragraphs']:
            document.add_paragraph(paragraph)
        sid = section['id']
        if not final:
            if sid in ('dataset','training','selection','results','analysis','conclusion'):
                document.add_paragraph('이 절의 실제 결과는 미측정이다. 정상 완료 결과와 동결 해시를 확인하지 못했으므로 성능 수치를 채우지 않았다.')
            continue
        if sid == 'overview':
            op = tests['historical_taco']['operating']
            document.add_paragraph(f"과거 TACO 고정 테스트의 정밀도는 {percent(op['precision'])}, 재현율은 {percent(op['recall'])}, F1은 {percent(op['f1'])}였다. 정밀도 90% 목표는 {'달성' if op['precision']>=.9 else '미달'}했고 재현율 90% 목표는 {'달성' if op['recall']>=.9 else '미달'}했다. 이 결과를 다른 출처나 CCTV 행동 인식 전체의 정확도로 해석하지 않았다.")
        elif sid == 'dataset':
            table(document,['출처','분할','종류','이미지 수'],[(r['source'],r['split'],'증강' if r['augmentation'] else '원본',r['images']) for r in source_splits(bundle['manifest'])],[42,61,29,40])
            document.add_paragraph('원본 이미지와 train 전용 crop 및 반복 학습 노출 수는 서로 다른 집계이다. 고정 manifest의 집계를 아래에 보존하였다.')
            table(document,['항목','고정 집계'],[(k,json.dumps(v,ensure_ascii=False)) for k,v in final['counts'].items()],[64,108])
        elif sid == 'training':
            if not epochs:
                document.add_paragraph('읽을 수 있는 실제 epoch 기록이 없어 학습 곡선과 완료 epoch는 미확인으로 남겼다.')
            for name, rows in epochs.items():
                document.add_heading(name, 2)
                document.add_paragraph(f"실제 CSV 기록은 {len(rows)}개이며 마지막 기록 epoch는 {int(rows[-1]['epoch']) if rows else '미확인'}이다. 이는 계획 epoch 또는 선택된 best checkpoint의 epoch와 다르다.")
                keys = [k for k in ('metrics/precision(B)','metrics/recall(B)','metrics/mAP50(B)') if any(k in r for r in rows)]
                path_chart = support / (name+'_epochs.png')
                plot(path_chart, name+' 실제 epoch 기록', [(key,[(r['epoch'],r[key]) for r in rows if key in r]) for key in keys],font_path,'실제 epoch','학습 중 validation 값',max([r['epoch'] for r in rows],default=1))
                document.add_picture(str(path_chart), width=Mm(168))
                charts.append(path_chart)
        elif sid == 'selection':
            selected = final['selected']
            document.add_paragraph(f"선택된 후보는 {selected['name']}이며 추론 방식은 {selected['policy']}, 입력 크기는 {selected['imgsz']}px, 고정 신뢰도는 {selected['operating']['threshold']:.6g}이다. 임계값은 검증에서만 정했고 테스트 곡선을 이용해 다시 조정하지 않았다.")
            document.add_paragraph('선택 checkpoint의 epoch는 현재 동결 결과에 명시되지 않아 미확인이다. 마지막 CSV epoch를 best epoch로 대체하지 않았다. baseline이 선택된 경우 두 신규 후보의 epoch를 해당 baseline의 epoch로 표시하지 않았다.')
            table(document,['검증 후보','TACO P','TACO R','F1','PlastOPol R'],[(r['name'],percent(r['operating']['precision']),percent(r['operating']['recall']),percent(r['operating']['f1']),percent(r.get('plastopol',{}).get('operating',{}).get('recall'))) for r in bundle['comparison']],[56,29,29,29,29])
        elif sid == 'results':
            table(document,['고정 테스트','P','R','F1','자체 AP50'],[(LABELS[k],percent(r['operating']['precision']),percent(r['operating']['recall']),percent(r['operating']['f1']),percent(r['metrics']['AP50'])) for k,r in tests.items()],[58,28,28,28,30])
            table(document,['고정 테스트','TP','FP','FN','TN'],[(LABELS[k],r['operating']['tp'],r['operating']['fp'],r['operating']['fn'],'정의하지 않음') for k,r in tests.items()],[62,23,23,23,41])
            document.add_paragraph('TP는 올바르게 대응한 쓰레기 상자, FP는 대응 정답이 없는 예측, FN은 놓친 정답이다. 객체 탐지에는 배경의 모든 가능한 상자를 세는 유한한 TN 정의가 없으므로 일반 분류 혼동행렬의 TN과 전체 accuracy를 계산하지 않았다.')
            for chart in charts[:2]:
                document.add_picture(str(chart), width=Mm(168))
            document.add_paragraph('PR과 신뢰도별 F1은 보존된 예측과 정답의 IoU .5 일대일 탐욕 매칭으로 재구성했다. 새로운 추론 또는 테스트 임계값 선택을 하지 않았다. AP는 7차 자체 101점 보간 지표이며 공식 COCO API AP가 아니다.')
        elif sid == 'analysis':
            table(document,['테스트와 크기','P','R','TP','FP','FN'],[(LABELS[k]+' / '+size,percent(v['precision']),percent(v['recall']),v['tp'],v['fp'],v['fn']) for k,r in tests.items() for size,v in r['sizes'].items()],[67,26,26,18,18,17])
            document.add_paragraph('작은 객체는 종횡비를 보존해 긴 변을 1280으로 맞춘 좌표에서 면적 32² 미만, 중간은 96² 미만, 큰 객체는 그 이상이다. 공식 COCO APs와 같지 않다. 정답과 예측 크기 기준이 달라 크기별 정밀도의 의미도 전체 지표와 구분한다.')
            table(document,['테스트','음성 이미지','음성 FP','이미지당 FP'],[(LABELS[k],r['negative_images'],r['negative_false_positives'],'미측정' if r['false_positives_per_negative_image'] is None else f"{r['false_positives_per_negative_image']:.4f}") for k,r in tests.items()],[65,35,30,42])
        elif sid == 'limits':
            for limit in final.get('limits',[]):
                document.add_paragraph('동결 기록의 한계: '+limit)
            document.add_paragraph('10차 영상 탐지는 보존된 5차 경로를 사용하므로 이 보고서의 선택 모델이 해당 영상 기능에 자동 적용됐다고 주장하지 않는다. 투기 행동 정답을 별도로 평가하지 않아 행동 정확도는 미측정이다.')
        elif sid == 'conclusion':
            for k,r in tests.items():
                op=r['operating']
                document.add_paragraph(f"{LABELS[k]}에서 정밀도 90%는 {'달성' if op['precision']>=.9 else '미달'}, 재현율 90%는 {'달성' if op['recall']>=.9 else '미달'}이다. 이후 추가 후보 학습이나 추가 데이터 수신 없이 이번 실험을 마무리한다.")
    document.add_heading('참고 자료',1)
    for ref in sections.get('references',[]):
        document.add_paragraph(ref['title']+' '+ref['url'])
    if bundle:
        document.add_heading('재현을 위한 파일 대응',1)
        document.add_paragraph('데이터와 가중치 파일은 중복 복사하지 않았다. 아래 위치는 프로젝트 기준 상대 경로이며 SHA-256으로 같은 파일인지 대조한다. 모든 개별 정답 파일의 해시는 비공개 검증 영수증에 보존하였다.')
        for name, info in bundle['references'].items():
            if '/labels/' not in name:
                document.add_paragraph(name+'\nSHA-256 '+info['sha256'])
    document.core_properties.author = author
    document.core_properties.title = sections['title']
    document.core_properties.subject = '가상 결과 제어 사례' if fixture else ('미완료 실험' if failure else '고정 실험 결과')
    document.save(path)
    receipt = {'fixture':fixture,'document_state':'draft_render_pending','render_status':'blocked',
               'human_visual_review':False,'reason':'허용된 렌더러와 전체 페이지 시각 검토가 아직 필요합니다.',
               'docx_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}
    write_json(support/'generation_receipt.json',receipt)
    return receipt


def render_document(docx, support, config):
    """검토한 명시적 렌더 설정 없이는 실행하지 않습니다."""
    if not config or config.get('approved') is not True:
        raise RuntimeError('문서 렌더 환경의 명시적 승인 전에는 최종 납품을 준비하지 않습니다.')
    python = Path(config['python']).resolve()
    helper = Path(config['helper']).resolve()
    soffice = Path(config['soffice']).resolve()
    if not all(p.is_file() for p in (python,helper,soffice)):
        raise ValueError('렌더 설정의 실제 실행 파일이 없습니다.')
    if config.get('helper_sha256') != hashlib.sha256(helper.read_bytes()).hexdigest():
        raise ValueError('검토한 렌더 도구 해시가 다릅니다.')
    import os
    env = os.environ.copy()
    env['PATH'] = str(soffice.parent)+os.pathsep+env.get('PATH','')
    command = [str(python),'-B','-X','utf8',str(helper),str(Path(docx).resolve()),'--output_dir',str(Path(support).resolve()),'--emit_pdf']
    result = subprocess.run(command, shell=False, cwd=str(Path(docx).resolve().parent),env=env,capture_output=True,timeout=180)
    write_json(Path(support)/'renderer_receipt.json',{'argv':command,'exit_code':result.returncode,
                'stdout':result.stdout.decode('utf-8','replace')[-24000:], 'stderr':result.stderr.decode('utf-8','replace')[-24000:],
                'human_visual_review':False})
    if result.returncode:
        raise RuntimeError('공식 문서 렌더 명령이 실패했습니다. 비공개 렌더 영수증을 확인하세요.')
    pdf = Path(support)/(Path(docx).stem+'.pdf')
    pages = sorted(Path(support).glob('page-*.png'))
    if not pdf.is_file() or not pdf.stat().st_size or not pages:
        raise RuntimeError('PDF 또는 전체 페이지 렌더 결과가 없습니다.')
    return pdf,pages
