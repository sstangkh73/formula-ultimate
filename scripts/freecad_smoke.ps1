$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$freeCadExecutable = "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe"
$scriptPath = Join-Path $PSScriptRoot "cad\freecad_smoke.py"
$artifactDirectory = Join-Path $workspaceRoot "artifacts\work005"

if (-not (Test-Path -LiteralPath $freeCadExecutable -PathType Leaf)) {
    throw "FreeCADCmd was not found at the verified Work 005 path."
}

New-Item -ItemType Directory -Force -Path $artifactDirectory | Out-Null

# FreeCAD 1.1.3 mis-parses passed Windows paths containing spaces. Use the
# filesystem-provided 8.3 aliases for this local compatibility launcher.
$fileSystem = New-Object -ComObject Scripting.FileSystemObject
$shortScriptPath = $fileSystem.GetFile($scriptPath).ShortPath
$shortArtifactDirectory = $fileSystem.GetFolder($artifactDirectory).ShortPath
$outputPath = Join-Path $shortArtifactDirectory "freecad_box.step"

& $freeCadExecutable $shortScriptPath --pass $outputPath
if ($LASTEXITCODE -ne 0) {
    throw "FreeCAD smoke test failed with exit code $LASTEXITCODE."
}

$resolvedOutput = Join-Path $artifactDirectory "freecad_box.step"
$artifact = Get-Item -LiteralPath $resolvedOutput
$digest = Get-FileHash -Algorithm SHA256 -LiteralPath $artifact.FullName
$header = [string](Get-Content -LiteralPath $artifact.FullName -TotalCount 1)
$evidence = [string](Get-Content -Raw -LiteralPath ($artifact.FullName + ".json"))

[pscustomobject]@{
    ExitCode = 0
    File = $artifact.FullName
    Bytes = $artifact.Length
    SHA256 = $digest.Hash
    Header = $header
    Evidence = $evidence
} | ConvertTo-Json -Depth 4
