$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
py -3.14 scripts/experiments/validate_main_campaign_protocol.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
