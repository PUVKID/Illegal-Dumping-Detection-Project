"""지정 작업 하나만 관찰하며 학습을 시작하거나 재개하지 않습니다."""
import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from report_core import (confined, decision, digest, epoch_rows, job_path, load_sections,
                         reconstruct_curves, relative, safe_reader, validate_bundle)
from report_outputs import create_docx, render_document, write_json

ROOT = Path(__file__).resolve().parent
INTERVAL_SECONDS = 60


@contextmanager
def watch_lock(path):
    """프로세스가 종료되면 운영체제가 해제하는 단일 관찰 잠금입니다."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        if stream.tell() == 0:
            stream.write(b'\0')
            stream.flush()
        stream.seek(0)
        acquired = False
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except OSError as error:
            raise RuntimeError('같은 지정 작업의 보고서 관찰자가 이미 실행 중입니다.') from error
        try:
            yield
        finally:
            if acquired:
                stream.seek(0)
                if os.name == 'nt':
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def validate_plan(plan):
    if plan.get('schema') != 1:
        raise ValueError('지원하지 않는 비공개 계획 형식입니다.')
    project = Path(plan['project_root']).resolve()
    job_path(project, plan['job_id'])
    output = confined(project / plan['output_dir'], project)
    support = confined(project / plan['support_dir'], project)
    if not output.is_relative_to(project / '최종'):
        raise ValueError('납품 위치는 프로젝트 최종 폴더 안이어야 합니다.')
    if not support.is_relative_to(project / '12차/work'):
        raise ValueError('비공개 지원 자료는 12차 work 안이어야 합니다.')
    if output == project / '최종' or output == support:
        raise ValueError('기존 최종 폴더를 직접 덮어쓸 수 없습니다.')
    if plan.get('deliver_formats') != ['docx', 'pdf']:
        raise ValueError('최종 납품은 Word와 같은 원고 PDF 두 개만 허용합니다.')
    if not isinstance(plan.get('author'), str) or not plan['author'].strip():
        raise ValueError('비공개 계획에 작성자를 지정해야 합니다.')
    return project, output, support


def mark_authoring(config):
    node = Path(config['node']).resolve()
    script = Path(config['script']).resolve()
    if not node.is_file() or not script.is_file():
        raise ValueError('저작 마커의 실제 Node 또는 스크립트가 없습니다.')
    result = subprocess.run([str(node),str(script),'--operation-kind','create',
                             '--expected-output-count','1','--output-format','docx'],
                            shell=False,cwd=str(ROOT.parent),capture_output=True,timeout=30)
    if result.returncode:
        raise RuntimeError('문서 저작 마커 실패: '+result.stderr.decode('utf-8','replace')[-4000:])


def publish_pair(docx, pdf, output):
    """검증된 같은 원고 두 파일만 신규 납품 폴더에 저장합니다."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(docx, output / '최종보고서.docx')
    shutil.copy2(pdf, output / '최종보고서.pdf')
    if {p.name for p in output.iterdir()} != {'최종보고서.docx', '최종보고서.pdf'}:
        raise RuntimeError('최종 납품 폴더의 파일 구성이 두 형식과 다릅니다.')
    return {p.name: {'sha256':digest(p),'bytes':p.stat().st_size} for p in output.iterdir()}


def verify_receipt(receipt, plan, project, output, reader):
    """운영 영수증만으로 완료를 믿지 않고 실제 두 파일과 입력을 대조합니다."""
    expected_names={'최종보고서.docx','최종보고서.pdf'}
    if (receipt.get('job_id')!=plan['job_id'] or receipt.get('state') not in ('complete','incomplete_report')
            or receipt.get('output_dir')!=relative(output,project)
            or set(receipt.get('outputs',{}))!=expected_names):
        raise ValueError('기존 완료 영수증의 작업·출력 위치·파일 목록이 다릅니다.')
    if not output.is_dir() or {p.name for p in output.iterdir()}!=expected_names:
        raise ValueError('완료 영수증에 해당하는 실제 두 보고서 파일이 없습니다.')
    for name in expected_names:
        path=output/name
        expected=receipt['outputs'][name]
        if (not path.is_file() or path.resolve().parent!=output.resolve()
                or type(expected.get('bytes')) is not int or expected['bytes']<=0
                or path.stat().st_size!=expected['bytes'] or digest(path)!=expected.get('sha256')):
            raise ValueError('완료 보고서의 경로·크기·SHA-256이 영수증과 다릅니다.')
    job=reader.safe_read_json(job_path(project,plan['job_id']))
    state=decision(job,plan['job_id'])
    if receipt['state']=='complete':
        final=reader.safe_read_json(project/'7차/work/training/final.json')
        if (state!='validate' or not isinstance(final,dict) or job.get('result')!=final
                or digest(project/'7차/work/training/final.json')!=receipt.get('input_final_sha256')):
            raise ValueError('완료 보고서의 지정 작업 및 최종 입력 바인딩이 다릅니다.')
    elif state!='incomplete' or receipt.get('input_final_sha256') is not None:
        raise ValueError('미완료 보고서와 현재 지정 작업의 상태가 다릅니다.')
    return receipt


def process_once(plan, reader=None, marker=mark_authoring, renderer=render_document):
    project, output, support = validate_plan(plan)
    reader = reader or safe_reader(project)
    support.mkdir(parents=True, exist_ok=True)
    receipt_path = support/'completion_receipt.json'
    previous = reader.safe_read_json(receipt_path)
    if previous:
        try:
            return verify_receipt(previous,plan,project,output,reader)
        except ValueError as error:
            write_json(support/'watch_status.json',{'state':'blocked_invalid_receipt','error':str(error),
                       'observed_kst':datetime.now().astimezone().isoformat(),'training_action':'없음'})
            raise
    if output.exists():
        raise FileExistsError('기존 최종 결과는 덮어쓰지 않습니다.')
    job = reader.safe_read_json(job_path(project, plan['job_id']))
    status = decision(job, plan['job_id'])
    now = time.time()
    observation = {'job_id':plan['job_id'],'observed_kst':datetime.now().astimezone().isoformat(),
                   'state':status,'job_state':job.get('state') if job else None,
                   'age_seconds':max(0,now-job.get('updated',now)) if job else None,
                   'process_liveness':'미검증','training_action':'없음'}
    observation['stale'] = observation['age_seconds'] is not None and observation['age_seconds'] > 300
    write_json(support/'watch_status.json',observation)
    if status in ('waiting','missing'):
        return observation
    # 성공 보고서는 해시·세 테스트·예측 정합성 검증이 끝난 뒤에만 작성합니다.
    bundle = validate_bundle(project,job,reader.safe_read_json) if status == 'validate' else None
    curves = reconstruct_curves(project,bundle,reader) if bundle else {}
    sections = load_sections(ROOT/'report_sections.json',reader.safe_read_json)
    epochs = {}
    if bundle:
        for directory in sorted((project/'7차/work/training/runs').glob('*')):
            csv_path = directory/'results.csv'
            if csv_path.is_file():
                epochs[directory.name] = epoch_rows(csv_path,reader.safe_read_text)
    renderer_config = reader.safe_read_json(Path(plan['renderer_config'])) if plan.get('renderer_config') else None
    if renderer_config is None or renderer_config.get('approved') is not True:
        observation.update(state='blocked_renderer',reason='허용된 Word/PDF 렌더 설정을 기다립니다.')
        write_json(support/'watch_status.json',observation)
        return observation
    # 저작 마커는 실제 DOCX 작성 직전에 이 생성 작업에서 한 번 호출합니다.
    marker(plan['marker'])
    docx = support/'최종보고서_편집원본.docx'
    create_docx(docx,sections,bundle,curves,epochs,support/'analysis',
                confined(project/plan['font'],project),author=plan['author'],failure=job if not bundle else None)
    if bundle:
        write_json(support/'input_hashes.json',bundle['references'])
    pdf,pages = renderer(docx,support/'render',renderer_config)
    hashes = publish_pair(docx,pdf,output)
    receipt = {'schema':1,'job_id':plan['job_id'],'state':'complete' if bundle else 'incomplete_report',
               'output_dir':relative(output,project),
               'finished_kst':datetime.now().astimezone().isoformat(),'outputs':hashes,
               'rendered_pages':len(pages),'human_visual_review':False,
               'qa':'정합성 검사와 자동 렌더 완료. 미래 인간 시각 검토를 수행했다고 주장하지 않습니다.',
               'input_final_sha256':digest(project/'7차/work/training/final.json') if bundle else None}
    write_json(receipt_path,receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description='지정된 마지막 실험의 완료 후 보고서 생성')
    parser.add_argument('--plan',required=True,help='비공개 계획 JSON')
    parser.add_argument('--once',action='store_true',help='한 번 읽고 종료하며 학습은 실행하지 않음')
    args = parser.parse_args()
    # 최초 계획은 고정 운영 파일이므로 다른 프로세스가 교체하지 않는 사본만 사용합니다.
    plan = json.loads(Path(args.plan).read_text(encoding='utf-8'))
    project,_,support = validate_plan(plan)
    reader = safe_reader(project)
    lock = ROOT/'work'/('watch_'+hashlib.sha256(plan['job_id'].encode()).hexdigest()[:20]+'.lock')
    with watch_lock(lock):
        while True:
            try:
                result = process_once(plan,reader)
            except Exception as error:
                support.mkdir(parents=True,exist_ok=True)
                write_json(support/'postprocess_failure.json',{'kst':datetime.now().astimezone().isoformat(),
                           'error':str(error),'exception':type(error).__name__,'training_action':'없음'})
                raise
            print(json.dumps(result,ensure_ascii=False,allow_nan=False),flush=True)
            if args.once or result['state'] in ('complete','incomplete_report','blocked_renderer'):
                break
            time.sleep(INTERVAL_SECONDS)


if __name__ == '__main__':
    main()
