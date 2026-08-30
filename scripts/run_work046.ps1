$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & py -3.14 (Join-Path $repoRoot "scripts\simulation\run_structural_failure_coupling.py") --config (Join-Path $repoRoot "config\simulation\structural_failure_coupling_v1.json") --artifact-root (Join-Path $repoRoot "artifacts\work046")
    if ($LASTEXITCODE -ne 0) { throw "Work 046 failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
