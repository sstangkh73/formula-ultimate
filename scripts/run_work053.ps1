$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
py -3.14 scripts/structural/run_vehicle_frame_refinement.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
