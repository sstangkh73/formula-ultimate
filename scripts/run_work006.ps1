$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$cadQueryPython = Join-Path $workspaceRoot ".tools\cadquery-mcp\Scripts\python.exe"
$freeCadPython = "C:\Program Files\FreeCAD 1.1\bin\python.exe"
$generatorPath = Join-Path $PSScriptRoot "cad\generate_mounting_plate.py"
$inspectorPath = Join-Path $PSScriptRoot "cad\inspect_step_freecad.py"
$aggregatorPath = Join-Path $PSScriptRoot "cad\aggregate_work006.py"
$configPath = Join-Path $workspaceRoot "config\work006_mounting_plate.json"
$artifactRoot = Join-Path $workspaceRoot "artifacts\work006"
$summaryPath = Join-Path $artifactRoot "experiment_summary.json"

foreach ($requiredFile in @(
    $cadQueryPython,
    $freeCadPython,
    $generatorPath,
    $inspectorPath,
    $aggregatorPath,
    $configPath
)) {
    if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
        throw "Required Work 006 dependency was not found: $requiredFile"
    }
}

New-Item -ItemType Directory -Force -Path $artifactRoot | Out-Null
$config = Get-Content -Raw -LiteralPath $configPath | ConvertFrom-Json

foreach ($candidate in $config.valid_candidates) {
    $candidateDirectory = Join-Path $artifactRoot $candidate.candidate_id
    New-Item -ItemType Directory -Force -Path $candidateDirectory | Out-Null
    $stepPath = Join-Path $candidateDirectory "component.step"
    $manifestPath = Join-Path $candidateDirectory "cadquery_manifest.json"
    $failurePath = Join-Path $candidateDirectory "grammar_failure.json"
    $reportPath = Join-Path $candidateDirectory "freecad_measurement.json"

    & $cadQueryPython $generatorPath `
        --config $configPath `
        --candidate-id $candidate.candidate_id `
        --output-step $stepPath `
        --manifest $manifestPath `
        --failure-json $failurePath
    if ($LASTEXITCODE -ne 0) {
        throw "CadQuery generation failed for $($candidate.candidate_id)."
    }

    if (Test-Path -LiteralPath $reportPath -PathType Leaf) {
        Remove-Item -LiteralPath $reportPath -Force
    }
    & $freeCadPython $inspectorPath $stepPath $reportPath
    if ($LASTEXITCODE -ne 0) {
        throw "FreeCAD STEP inspection failed for $($candidate.candidate_id)."
    }
    if (-not (Test-Path -LiteralPath $reportPath -PathType Leaf)) {
        throw "FreeCAD returned success without evidence for $($candidate.candidate_id)."
    }
}

$invalid = $config.invalid_candidate
$invalidDirectory = Join-Path $artifactRoot $invalid.candidate_id
New-Item -ItemType Directory -Force -Path $invalidDirectory | Out-Null
$invalidStepPath = Join-Path $invalidDirectory "component.step"
$invalidManifestPath = Join-Path $invalidDirectory "cadquery_manifest.json"
$invalidFailurePath = Join-Path $invalidDirectory "grammar_failure.json"
foreach ($staleInvalidArtifact in @($invalidStepPath, $invalidManifestPath, $invalidFailurePath)) {
    if (Test-Path -LiteralPath $staleInvalidArtifact -PathType Leaf) {
        Remove-Item -LiteralPath $staleInvalidArtifact -Force
    }
}

& $cadQueryPython $generatorPath `
    --config $configPath `
    --candidate-id $invalid.candidate_id `
    --output-step $invalidStepPath `
    --manifest $invalidManifestPath `
    --failure-json $invalidFailurePath
$invalidExitCode = $LASTEXITCODE
if ($invalidExitCode -ne 2) {
    throw "Invalid candidate returned $invalidExitCode; expected grammar rejection 2."
}

py -3.14 $aggregatorPath `
    --config $configPath `
    --artifact-root $artifactRoot `
    --output $summaryPath
if ($LASTEXITCODE -ne 0) {
    throw "Work 006 evidence aggregation failed with exit code $LASTEXITCODE."
}

$summary = Get-Content -Raw -LiteralPath $summaryPath | ConvertFrom-Json
[pscustomobject]@{
    Status = $summary.status
    ExperimentId = $summary.experiment_id
    CandidateCount = $summary.candidates.Count
    Seed = $summary.seed
    Summary = $summaryPath
    MonotonicChecks = $summary.monotonic_checks
} | ConvertTo-Json -Depth 5
