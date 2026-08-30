$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & py -3.14 (Join-Path $repoRoot "scripts\structural\run_fracture_initiation_acceptance.py") --config (Join-Path $repoRoot "config\structural\fracture_initiation_acceptance_v1.json") --artifact-root (Join-Path $repoRoot "artifacts\work043")
    if ($LASTEXITCODE -ne 0) { throw "Work 043 failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
