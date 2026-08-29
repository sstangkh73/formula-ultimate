$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & py -3.14 (Join-Path $repoRoot "scripts\structural\run_near_critical_element_verification.py") --config (Join-Path $repoRoot "config\structural\near_critical_element_verification_v1.json") --artifact-root (Join-Path $repoRoot "artifacts\work041") --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
    if ($LASTEXITCODE -ne 0) { throw "Work 041 failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
