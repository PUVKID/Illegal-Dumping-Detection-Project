@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -Command "$candidates = @((Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe')); $installed = Join-Path $env:LOCALAPPDATA 'Programs\Python'; if (Test-Path -LiteralPath $installed) { $candidates += @(Get-ChildItem -LiteralPath $installed -Filter python.exe -Recurse -File | Select-Object -ExpandProperty FullName) }; foreach ($candidate in $candidates) { if (Test-Path -LiteralPath $candidate) { & $candidate -B -X utf8 -c 'import sys;sys.exit(0 if sys.version_info >= (3,11) else 1)'; if ($LASTEXITCODE -eq 0) { & $candidate -B -X utf8 launcher.py --hidden; exit $LASTEXITCODE } } }; $py = Get-Command py.exe -ErrorAction SilentlyContinue; if ($py) { & $py.Source -3 -B -X utf8 launcher.py --hidden; exit $LASTEXITCODE }; Write-Host 'Python 3.11 이상을 찾지 못했습니다. 사용 안내를 확인해 주세요.'; exit 1"
if errorlevel 1 pause
