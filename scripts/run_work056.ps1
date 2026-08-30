$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
py -3.14 scripts/experiments/prepare_main_campaign_runner.py --mode prepare
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
