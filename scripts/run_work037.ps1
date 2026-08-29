$ErrorActionPreference="Stop";$r=Split-Path -Parent $PSScriptRoot
& py -3.14 (Join-Path $r "scripts\structural\run_eigenvalue_buckling_acceptance.py") --config (Join-Path $r "config\structural\eigenvalue_buckling_acceptance_v1.json") --artifact-root (Join-Path $r "artifacts\work037") --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
if($LASTEXITCODE){throw "Work 037 failed"}
