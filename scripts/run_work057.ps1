$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

& py -3.14 scripts/experiments/probe_campaign_process_resume.py --action reserve --artifact-root artifacts/work057/process_resume_probe
if ($LASTEXITCODE -ne 75) { throw "Process-resume reservation phase returned unexpected exit code $LASTEXITCODE." }

& py -3.14 scripts/experiments/probe_campaign_process_resume.py --action resume --artifact-root artifacts/work057/process_resume_probe
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind burn-in --artifact-root artifacts/work057
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
