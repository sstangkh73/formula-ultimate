$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & py -3.14 (Join-Path $repoRoot "scripts\structural\run_nonlinear_imperfect_column_acceptance.py") --config (Join-Path $repoRoot "config\structural\nonlinear_imperfect_column_acceptance_v1.json") --artifact-root (Join-Path $repoRoot "artifacts\work038") --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
    if ($LASTEXITCODE -ne 0) { throw "Work 038 failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
