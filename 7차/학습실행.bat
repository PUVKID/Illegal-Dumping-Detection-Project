@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set "PBL_RESUME=false"
if /i "%~1"=="resume" set "PBL_RESUME=true"
echo 7차 자료 준비 후 학습을 독립 프로세스로 실행합니다. Codex 또는 API 토큰이 필요하지 않습니다.
docker exec 2026 /opt/venvs/torch/bin/python -B -X utf8 "/workspace/2026/월요일 PBL/7차/worker.py" --action train --params "{\"resume\":%PBL_RESUME%}"
if errorlevel 1 (
  echo 시작하지 못했습니다. 위 오류와 Docker Desktop, 2026 컨테이너를 확인해 주세요.
  pause
  exit /b 1
)
echo 준비가 끝나면 학습으로 자동 연결됩니다. 창을 닫아도 작업은 계속됩니다.
echo 학습상태.bat으로 실제 상태와 로그 위치를 확인하세요.
endlocal
