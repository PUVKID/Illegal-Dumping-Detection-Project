param([string]$Python = '')
$ErrorActionPreference = 'Stop'
$assetDir = $PSScriptRoot
$workspace = Split-Path $assetDir -Parent
$workDir = Join-Path $workspace '_작업'
$py = if ($Python) { $Python } else { Join-Path $workDir 'buildenv/Scripts/python.exe' }
if (-not (Test-Path -LiteralPath $py)) {
    $command = Get-Command python -ErrorAction SilentlyContinue
    if (-not $command) { throw 'Python with PyInstaller is required for rebuilding. Pass -Python C:\path\python.exe. Running CleanView.exe does not require Python.' }
    $py = $command.Source
}
$argsList = @('-X','utf8','-m','PyInstaller','--noconfirm','--onefile','--windowed','--name','CleanView','--distpath',$assetDir,'--workpath',(Join-Path $workDir 'pyinstaller2'),'--specpath',$workDir)
foreach ($file in @('index.html','backend.py','detector.py','inference.py','data_pipeline.py','train_round3.py')) { $argsList += @('--add-data',"$assetDir\$file;.") }
$argsList += @('--add-data',"$assetDir\fonts;fonts",(Join-Path $assetDir 'launcher.py'))
Push-Location -LiteralPath $workspace
try {
    & $py @argsList
    if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
} finally { Pop-Location }
