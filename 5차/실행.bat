@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
if exist "%~dp0CleanView5.exe" (
  start "" "%~dp0CleanView5.exe" --hidden
  exit /b 0
)
set "PBL_PY=%~dp0runtime\python.exe"
if not exist "%PBL_PY%" set "PBL_PY=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if not exist "%PBL_PY%" (
  echo 실행 가능한 Python이 없습니다. 사용안내.txt의 런타임 경로를 확인해 주세요.
  pause
  exit /b 1
)
"%PBL_PY%" -B -X utf8 "%~dp0launcher.py" --hidden
if errorlevel 1 pause
endlocal
