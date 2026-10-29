@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
docker exec 2026 /opt/venvs/torch/bin/python -B -X utf8 "/workspace/2026/월요일 PBL/7차/worker.py" --action status
if errorlevel 1 (
  echo 상태를 갱신하지 못했습니다. Docker가 중단됐으면 마지막 HTML 기록을 현재 실행 상태로 해석하지 마세요.
  pause
  exit /b 1
)
if exist "%~dp0work\학습상태.html" start "" "%~dp0work\학습상태.html"
echo 상세 오류와 전체 로그는 work\jobs 폴더에 보존합니다.
endlocal
