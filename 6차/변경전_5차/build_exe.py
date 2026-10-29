"""PyInstaller 의존성 확인과 사용자가 선택한 빌드를 수행합니다."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import shutil
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true', help='확인만 하지 않고 실제 EXE를 빌드합니다.')
    args = parser.parse_args()
    available = importlib.util.find_spec('PyInstaller') is not None
    print('PyInstaller: ' + ('사용 가능' if available else '미설치 · 소스 실행은 가능합니다.'))
    if not args.build:
        return
    if not available:
        raise SystemExit('빌드하려면 별도로 PyInstaller를 준비해야 합니다. 자동 설치하지 않습니다.')
    root = Path(__file__).resolve().parent
    subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--onedir', '--name', 'CleanView5',
                    '--hidden-import', 'pipeline',
                    '--distpath', str(root / 'work' / 'dist'), '--workpath', str(root / 'work' / 'build'),
                    '--specpath', str(root / 'work'), str(root / 'launcher.py')], cwd=str(root), check=True, shell=False,
                   env={**os.environ, 'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8'})
    # EXE를 원래 프로젝트 옆에 두어 고정된 데이터·Docker 경로를 유지합니다.
    source = root / 'work/dist/CleanView5'
    shutil.copy2(source / 'CleanView5.exe', root / 'CleanView5.exe')
    shutil.copytree(source / '_internal', root / '_internal', dirs_exist_ok=True)
    print('프로젝트의 CleanView5.exe를 생성했습니다. web·GPU 작업 소스와 함께 유지해 주세요.')


if __name__ == '__main__':
    main()
