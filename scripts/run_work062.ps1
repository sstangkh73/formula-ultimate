$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

& py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind main --protocol config/experiments/bounded_whole_vehicle_main_campaign_v3.json --artifact-root artifacts/work062 --admission artifacts/work061/campaign_summary.json
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
