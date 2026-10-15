# The judge of "done": exit 0 = goal met, anything else = not yet.
# Protected: the loop stops if this file changes.
#
# Gate 1  material publication boundary (repository rule)
# Gate 2  the whole repository unittest suite (nothing may regress)
# Gate 3  the acceptance suites: v1 hierarchical composition and v2 functional composition (the goal)

$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)

# The acceptance suites' fixture hooks are for self-checks only.
foreach ($name in 'FU_ACCEPTANCE_GENERATOR', 'FU_ACCEPTANCE_GENERATOR_V2', 'FU_ACCEPTANCE_EVALUATOR') {
    Remove-Item "Env:$name" -ErrorAction SilentlyContinue
}

Write-Host '== Gate 1: material publication boundary'
python scripts/validation/check_material_publication_boundary.py
if ($LASTEXITCODE -ne 0) { Write-Host "Gate 1 FAILED (exit $LASTEXITCODE)"; exit 1 }

Write-Host '== Gate 2: repository unittest suite'
python -m unittest discover -s tests
if ($LASTEXITCODE -ne 0) { Write-Host "Gate 2 FAILED (exit $LASTEXITCODE)"; exit 2 }

Write-Host '== Gate 3: acceptance (v1 hierarchical + v2 functional composition)'
python -m unittest discover -s auto-loop/acceptance -v
if ($LASTEXITCODE -ne 0) { Write-Host "Gate 3 FAILED (exit $LASTEXITCODE)"; exit 3 }

Write-Host 'ALL GATES PASSED'
exit 0
