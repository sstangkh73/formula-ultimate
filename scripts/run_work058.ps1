$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

& py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind main --artifact-root artifacts/work058 --admission artifacts/work057/campaign_summary.json
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
