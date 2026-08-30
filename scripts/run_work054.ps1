$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
py -3.14 scripts/experiments/adjudicate_refined_readiness.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
