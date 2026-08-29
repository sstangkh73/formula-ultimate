$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $PSScriptRoot "cad\run_research_candidate.py"
$protocol = Join-Path $workspaceRoot "config\experiments\research_experiment_protocol_v1.json"
$candidate = Join-Path $workspaceRoot "config\experiments\candidate_fu-c0001.json"
$artifactRoot = Join-Path $workspaceRoot "artifacts\work031"
$cadQueryPython = Join-Path $workspaceRoot ".tools\cadquery-mcp\Scripts\python.exe"
$freeCadPython = "C:\Program Files\FreeCAD 1.1\bin\python.exe"

foreach ($requiredFile in @(
    $runner,
    $protocol,
    $candidate,
    $cadQueryPython,
    $freeCadPython
)) {
    if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
        throw "Required Candidate 001 dependency was not found: $requiredFile"
    }
}

py -3.14 $runner `
    --protocol $protocol `
    --candidate $candidate `
    --artifact-root $artifactRoot `
    --cadquery-python $cadQueryPython `
    --freecad-python $freeCadPython
if ($LASTEXITCODE -ne 0) {
    throw "Candidate 001 pipeline failed with exit code $LASTEXITCODE."
}
