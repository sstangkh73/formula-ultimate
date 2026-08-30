$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & py -3.14 (Join-Path $repoRoot "scripts\structural\run_fatigue_damage_acceptance.py") --config (Join-Path $repoRoot "config\structural\fatigue_damage_acceptance_v1.json") --artifact-root (Join-Path $repoRoot "artifacts\work044")
    if ($LASTEXITCODE -ne 0) { throw "Work 044 failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
