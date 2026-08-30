$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
py -3.14 scripts/simulation/run_vehicle_load_cases.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
