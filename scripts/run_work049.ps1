$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
py -3.14 scripts/experiments/run_whole_vehicle_baseline.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
