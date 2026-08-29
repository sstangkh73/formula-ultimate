$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $PSScriptRoot "structural\run_tension_acceptance.py"
$config = Join-Path $workspaceRoot "config\structural\tension_solver_acceptance_v1.json"
$artifactRoot = Join-Path $workspaceRoot "artifacts\work034"
$gmsh = "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe"
$ccx = "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"

foreach ($requiredFile in @($runner, $config, $gmsh, $ccx)) {
    if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
        throw "Required Work 034 dependency was not found: $requiredFile"
    }
}

py -3.14 $runner `
    --config $config `
    --artifact-root $artifactRoot `
    --gmsh $gmsh `
    --ccx $ccx
if ($LASTEXITCODE -ne 0) {
    throw "Work 034 tension solver acceptance failed with exit code $LASTEXITCODE."
}
