$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$environmentPath = Join-Path $workspaceRoot ".tools\cadquery-mcp"
$requirementsPath = Join-Path $workspaceRoot "tools\cadquery-mcp-requirements.txt"

py -3.14 -m uv python install 3.12
if ($LASTEXITCODE -ne 0) {
    throw "uv could not install or locate Python 3.12."
}

if (-not (Test-Path -LiteralPath $environmentPath -PathType Container)) {
    py -3.14 -m uv venv $environmentPath --python 3.12
    if ($LASTEXITCODE -ne 0) {
        throw "uv could not create the CadQuery MCP environment."
    }
}

$environmentPython = Join-Path $environmentPath "Scripts\python.exe"
py -3.14 -m uv pip install --python $environmentPython -r $requirementsPath
if ($LASTEXITCODE -ne 0) {
    throw "uv could not install the pinned CadQuery MCP requirements."
}

& $environmentPython -c (
    "import cadquery, importlib.metadata as m; " +
    "print('CadQuery ' + cadquery.__version__); " +
    "print('cadquery-mcp ' + m.version('cadquery-mcp')); " +
    "print('mcp ' + m.version('mcp'))"
)
