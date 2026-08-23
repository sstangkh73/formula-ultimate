$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$serverExecutable = Join-Path $workspaceRoot ".tools\cadquery-mcp\Scripts\cadquery-mcp.exe"

if (-not (Test-Path -LiteralPath $serverExecutable -PathType Leaf)) {
    throw "CadQuery MCP environment is missing. Follow docs/3d/CAD_MCP_ENVIRONMENT.md."
}

& $serverExecutable
exit $LASTEXITCODE
