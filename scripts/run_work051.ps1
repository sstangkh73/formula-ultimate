$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    & py -3.14 (Join-Path $repoRoot "scripts\structural\run_gate_a_remediation.py") --config (Join-Path $repoRoot "config\structural\gate_a_remediation_v1.json") --artifact-root (Join-Path $repoRoot "artifacts\work051") --cadquery-python (Join-Path $repoRoot ".tools\cadquery-mcp\Scripts\python.exe") --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
    if ($LASTEXITCODE -ne 0) { throw "Work 051 failed with exit code $LASTEXITCODE" }
} finally {
    Pop-Location
}
