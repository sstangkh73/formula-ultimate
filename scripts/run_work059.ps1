$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

& py -3.14 scripts/experiments/probe_campaign_process_resume.py --action reserve --protocol config/experiments/bounded_whole_vehicle_main_campaign_v2.json --artifact-root artifacts/work059/process_resume_probe
if ($LASTEXITCODE -ne 75) { throw "Process-resume reservation phase returned unexpected exit code $LASTEXITCODE." }

& py -3.14 scripts/experiments/probe_campaign_process_resume.py --action resume --protocol config/experiments/bounded_whole_vehicle_main_campaign_v2.json --artifact-root artifacts/work059/process_resume_probe
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind burn-in --protocol config/experiments/bounded_whole_vehicle_main_campaign_v2.json --artifact-root artifacts/work059
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
