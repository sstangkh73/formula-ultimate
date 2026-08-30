$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & py -3.14 (Join-Path $repoRoot "scripts\structural\run_yield_plasticity_acceptance.py") --config (Join-Path $repoRoot "config\structural\yield_plasticity_acceptance_v1.json") --artifact-root (Join-Path $repoRoot "artifacts\work042") --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
    if ($LASTEXITCODE -ne 0) { throw "Work 042 failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
