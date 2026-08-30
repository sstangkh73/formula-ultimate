$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & py -3.14 (Join-Path $repoRoot "scripts\topology\run_vehicle_assembly_acceptance.py") --config (Join-Path $repoRoot "config\vehicle\topology_neutral_vehicle_v1.json") --artifact-root (Join-Path $repoRoot "artifacts\work047") --cadquery-python (Join-Path $repoRoot ".tools\cadquery-mcp\Scripts\python.exe") --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"
    if ($LASTEXITCODE -ne 0) { throw "Work 047 failed with exit code $LASTEXITCODE" }
} finally { Pop-Location }
