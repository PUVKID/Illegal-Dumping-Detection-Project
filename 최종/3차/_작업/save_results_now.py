"""Save finished results without filling the system drive with new training photos."""
import json, sys, time
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / '클린뷰'
sys.path.insert(0, str(SOURCE))
from finalize_round3 import Archive, DEST, ROOT, REMOTE, JOB, docker, sha, write

def main():
    state = json.loads(docker('exec', '2026-2', 'cat', REMOTE+'/state/jobs/'+JOB+'.json'))
    final = json.loads(docker('exec', '2026-2', 'cat', ROOT+'/final.json'))
    assert state['state'] == 'complete' and state['test_metrics'] == final['test']['metrics']
    for name in ('make_report.py', 'data_pipeline.py'):
        docker('cp', str(SOURCE/name), '2026-2:'+REMOTE+'/'+name)
    print(docker('exec','2026-2','python',REMOTE+'/make_report.py').decode('utf-8'), flush=True)
    archive = Archive()
    archive.local(SOURCE, SOURCE)
    for folder, target in [('runs','실험기록'), ('evaluation','평가원자료'), ('sources','출처'), ('pretrained','사전학습가중치')]:
        archive.remote(ROOT+'/'+folder, DEST/target)
    archive.remote(REMOTE, DEST/'실행기록', subdirs=['state','results','uploads','selected_model.json'])
    names = json.loads(docker('exec','2026-2','python','-c',"import json;from pathlib import Path;print(json.dumps([p.name for p in Path('/root/환경 PBL/trash_round3').iterdir() if p.is_file()]))"))
    for name in names:
        target = DEST/'실험설정'/name
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(docker('exec','2026-2','cat',ROOT+'/'+name))
    archive.remote(ROOT+'/report', DEST/'보고서')
    models = {}
    for weights, expected in final['best_sha256'].items():
        local = DEST/'실험기록'/weights.removeprefix(ROOT+'/runs/')
        models[weights] = sha(local)
        assert models[weights] == expected
    receipt = {'job':JOB, 'training_complete':True, 'results_saved':True,
               'all_materials_saved':False, 'pending':['Docker data/additional', 'Docker data/zoom', 'Docker data/full'],
               'reason':'C drive free space insufficient for complete training-data archive',
               'model_sha256':models, 'test':final['test'], 'target_met':final['target_met'],
               'files':len(archive.records), 'bytes':sum(r['bytes'] for r in archive.records),
               'records':archive.records, 'created':time.time()}
    write(DEST/'결과저장.json', receipt)
    write(DEST/'보고서/보관검증.json', {k:v for k,v in receipt.items() if k!='records'})
    (DEST/'저장현황.txt').write_text('학습과 최종 테스트 완료. 모델·보고서·평가 원자료·실행 기록 저장 및 모델 SHA-256 확인 완료.\n추가 학습 사진과 확대 사진 전체는 C드라이브 공간 부족으로 아직 Docker에만 보관돼 있습니다.\n학습을 새로 시작하거나 테스트를 다시 수행하지 않았습니다.\n', encoding='utf-8-sig')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('records','test')},ensure_ascii=False), flush=True)

if __name__ == '__main__': main()
