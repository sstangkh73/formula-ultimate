$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $repoRoot "scripts\structural\run_beam_bending_acceptance.py"
$config = Join-Path $repoRoot "config\structural\beam_bending_acceptance_v1.json"
$artifactRoot = Join-Path $repoRoot "artifacts\work035"
$gmsh = "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe"
$ccx = "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"

Push-Location $repoRoot
try {
    & py -3.14 $runner `
        --config $config `
        --artifact-root $artifactRoot `
        --gmsh $gmsh `
        --ccx $ccx
    if ($LASTEXITCODE -ne 0) {
        throw "Work 035 beam-bending acceptance failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
