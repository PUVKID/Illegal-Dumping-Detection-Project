"""소스 UTF-8·구문·실제 진입점·기존 모델 보존을 검사합니다."""
import ast
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    files=[ROOT/name for name in ('prepare_dataset.py','train_pipeline.py','worker.py','verify_sources.py')]
    files+=list((ROOT/'tests').glob('*.py'))+list((ROOT/'docs').glob('*.md'))+list((ROOT/'configs').glob('*.json'))
    checked=0
    for path in files:
        text=path.read_bytes().decode('utf-8',errors='strict')
        if '\ufffd' in text:raise ValueError('대체 문자가 있습니다: '+str(path))
        if path.suffix=='.py':ast.parse(text,filename=str(path))
        if path.suffix=='.json':json.loads(text)
        checked+=1
    import prepare_dataset
    import train_pipeline
    train_pipeline.verify_models()
    config=prepare_dataset.load(ROOT/'configs/training.json')
    if config['download_limit_bytes']!=100*1024**3 or config['minimum_disk_free_bytes']!=100*1024**3:
        raise ValueError('신규 전송 예산·잔여 공간 계약이 다릅니다.')
    if len(config['candidates'])!=2 or any(row['patience']!=12 for row in config['candidates']):
        raise ValueError('검토한 두 후보 명세가 다릅니다.')
    print(json.dumps({'checked_sources':checked,'protected_files':6,'utf8':'strict','syntax':'pass'},ensure_ascii=False))


if __name__=='__main__':main()
