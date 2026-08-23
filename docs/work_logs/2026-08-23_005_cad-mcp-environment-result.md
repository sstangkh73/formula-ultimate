# Work Result 005: CAD and MCP Environment Bootstrap

Date: 2026-08-23
Status: Completed

## Summary

Established and tested the first local 3D agent toolchain for Formula Ultimate:

- enabled Autodesk Fusion's vendor-provided local MCP server and completed a
  real Streamable HTTP initialize/list-tools handshake;
- installed CadQuery and the CadQuery contrib MCP in an ignored Python 3.12
  environment, pinned the source revision, repaired an upstream dependency
  incompatibility, and completed inspect/render protocol calls;
- proved FreeCAD 1.1.3 headless solid creation and STEP export with independent
  dimensions, volume, file header, size, and hash evidence;
- inventoried Blender 5.0.1 and left its official Blender Lab MCP disconnected
  because the official server requires Blender 5.1 or newer;
- added reproducible launchers, project MCP configuration, bilingual operating
  documentation, and repository-contract coverage for ignored tool trees.

No existing CAD document was edited. No Fusion mutation or execute tool was
called. No design was uploaded or shared.

## Changed Files

### MCP and environment configuration

- `.codex/config.toml`: optional, approval-gated project definitions for Fusion
  HTTP MCP and CadQuery STDIO MCP.
- `.gitignore`: ignores `.tools/` and the user-extracted
  `cadquery-contrib-master/` tree.
- `tools/cadquery-mcp-requirements.txt`: pins CadQuery MCP source commit,
  `mcp` major version, and pytest version.

### Reproducible tools

- `scripts/bootstrap_cadquery_mcp.ps1`: idempotent Python 3.12/uv bootstrap.
- `scripts/cadquery_mcp.ps1`: project-relative STDIO launcher.
- `scripts/cad/mcp_probe.py`: direct STDIO/Streamable HTTP initialization,
  tool inventory, CadQuery inspect, and SVG render evidence.
- `scripts/cad/freecad_smoke.py`: disposable FreeCAD solid and STEP generator.
- `scripts/freecad_smoke.ps1`: Windows path compatibility wrapper plus artifact
  header/size/SHA-256 evidence.

### Documentation and tests

- `docs/3d/CAD_MCP_ENVIRONMENT.md` and `.th.md`: verified stack, commands,
  evidence, limitations, and security boundary.
- matching Work 005 plan/result records in English and Thai.
- `tests/test_repository_contract.py`: excludes ignored `.tools` and
  `cadquery-contrib-master` dependency trees from maintained bilingual Markdown
  coverage while continuing to check repository documentation.

## Key Decisions

1. **Use Fusion's official server instead of a community bridge.** The installed
   Fusion build exposes its own localhost MCP endpoint and four tool groups.
2. **Use CadQuery for reproducible generation and inspection.** The community
   bridge is source-pinned at
   `06b5e50a87fcf6808859f33d84e224fce675f8d7`, not installed from a moving
   branch at runtime.
3. **Constrain `mcp` to `>=1,<2`.** The upstream package declares only a lower
   bound but uses SDK APIs removed in MCP 2.0.0. Version 1.29.0 passes the full
   upstream test file.
4. **Keep FreeCAD as an independent evaluator.** No FreeCAD community MCP was
   installed without a separate security review.
5. **Do not install Blender MCP on Blender 5.0.1.** The official Blender Lab
   path requires 5.1+ and explicitly warns that generated Python is unguarded.
6. **Treat approval prompts as review, not isolation.** CadQuery still accepts
   arbitrary Python and caller-selected export paths.

## Validation Evidence

### 1. Installed environment

Command: version inventory using application executables, `uv --version`, and
Python package metadata

Environment: Windows, PowerShell, Python 3.14 host and isolated Python 3.12.14

Exit code: 0

Result:

```text
Fusion 2704.1.53
FreeCAD 1.1.3 Revision: 20260725 (Git shallow)
Blender 5.0.1
uv 0.12.5
Python 3.12.14
CadQuery 2.8.0
cadquery-mcp 0.1.0
mcp 1.29.0
```

### 2. Fusion server socket

Command:

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 27182
```

Exit code: 0

Result: `TcpTestSucceeded : True`

### 3. Fusion MCP protocol

Command:

```powershell
.tools\cadquery-mcp\Scripts\python.exe scripts\cad\mcp_probe.py `
  --output artifacts\work005\fusion_mcp_probe.json `
  http --url http://127.0.0.1:27182/mcp
```

Exit code: 0

Result:

```text
server_name: MCP Server Adapter
server_version: 1.0.0
tools: fusion_mcp_electronics_read, fusion_mcp_execute,
       fusion_mcp_read, fusion_mcp_update
```

### 4. CadQuery bootstrap

Command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File scripts\bootstrap_cadquery_mcp.ps1
```

Exit code: 0

Result:

```text
Python 3.12 is already installed
Checked 77 packages
CadQuery 2.8.0
cadquery-mcp 0.1.0
mcp 1.29.0
```

### 5. CadQuery upstream tests and dependency failure record

Initial environment: `mcp 2.0.0`

Initial command: upstream `test_cadquery_mcp_server.py`

Initial exit code: 1

Initial result: `27 failed`; root exception was
`AttributeError: 'Server' object has no attribute 'list_tools'`.

Correction command:

```powershell
py -3.14 -m uv pip install `
  --python .tools\cadquery-mcp\Scripts\python.exe "mcp<2"
```

Final command:

```powershell
.tools\cadquery-mcp\Scripts\python.exe -m pytest -q `
  -p no:cacheprovider `
  cadquery-contrib-master\cadquery-contrib-master\mcp-server\test_cadquery_mcp_server.py
```

Final exit code: 0

Final result: `27 passed, 1 warning in 2.76s`. The warning is CadQuery CQGI's
use of deprecated `ast.NameConstant` when running on this environment.

### 6. CadQuery MCP inspect and render

Command:

```powershell
.tools\cadquery-mcp\Scripts\python.exe scripts\cad\mcp_probe.py `
  --output artifacts\work005\cadquery_mcp_probe.json `
  stdio --command .tools\cadquery-mcp\Scripts\cadquery-mcp.exe `
  --inspect-box --render-output artifacts\work005\cadquery_box.svg
```

Exit code: 0

Result:

```text
tools: export, get_parameters, inspect, render
inspect_is_error: false
bounds_mm: 10 x 20 x 30
volume_mm3: 6000
surface_area_mm2: 2200
topology: 1 solid, 6 faces, 12 edges, 8 vertices
render_is_error: false
render_mime_type: image/svg+xml
render_bytes: 2420
render_sha256: CB69BA4DD6A23EE8653C1EF37E2BEFC4E55797CC6EC22ACAD0B1163E663A74CA
```

Evidence artifacts are deliberately Git-ignored under `artifacts/work005/`.

### 7. FreeCAD STEP smoke test

Command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\freecad_smoke.ps1
```

Exit code: 0

Result from the final recorded run:

```text
bounds_mm: [10.0, 20.0, 30.0]
volume_mm3: 6000.0
solid_count: 1
STEP header: ISO-10303-21;
bytes: 6854
SHA256: 4C4182EA8152C9327CB9AF4A8AB20FC8FC4470D979380DC0D833EA8D2A5F39D1
```

The first direct attempt using an output path containing `C:\Formula Ultimate`
did not produce the artifact because FreeCAD 1.1.3 split the path at the space.
The committed launcher uses filesystem-provided short paths; the rerun passed.

### 8. Repository tests

Command:

```powershell
py -3.14 -m unittest discover -s tests -v
```

Exit code: 0

Result: `Ran 14 tests ... OK`.

The first run failed 24 bilingual subtests because the contract test traversed
ignored installed/vendor Markdown under `.tools/` and the user's extracted
CadQuery tree. The test scope was corrected to exclude those two ignored trees;
all maintained repository Markdown remains covered.

### 9. Static/configuration checks

Commands:

```powershell
py -3.14 -m py_compile scripts\cad\mcp_probe.py scripts\cad\freecad_smoke.py
py -3.14 -c "import tomllib, pathlib; tomllib.loads(pathlib.Path('.codex/config.toml').read_text())"
git diff --check
```

Exit codes: 0, 0, 0

Result: Python sources compiled, TOML parsed with servers `cadquery,fusion`, and
no whitespace errors were reported.

## Claims Supported

- Fusion's official local server was enabled and answered an MCP handshake.
- CadQuery MCP 0.1.0 can list tools, inspect deterministic geometry, and render
  SVG in the pinned local environment.
- FreeCAD can generate a deterministic reference solid and export a valid STEP
  exchange file headlessly on this machine.
- The repository contains project MCP definitions suitable for a newly loaded,
  trusted Codex task.

## Claims Explicitly Unsupported

- No Fusion mutation/execute tool was tested; no Fusion geometry was created.
- The newly written project MCP config was not hot-loaded into this already
  running task. The packaged `codex mcp list` executable could not be launched
  from PowerShell because WindowsApps returned `Access is denied`; direct MCP
  protocol tests were used instead.
- FreeCAD is not MCP-connected.
- Blender MCP is not installed or connected.
- The reference box is not a validated race-car component.
- No topology discovery, optimizer, CFD, FEA, vehicle dynamics, manufacturing,
  or safety validation was performed.
- Approval prompts do not sandbox CadQuery or Fusion execution.

## Deviations from Plan

- Blender was inventoried but not connected because the installed 5.0.1 build
  does not meet the official 5.1+ requirement.
- A FreeCAD MCP bridge was not selected; headless automation was proven first as
  planned, and the unreviewed community bridge decision remains deferred.
- An environment bootstrap script and requirements file were added to make the
  pinned installation reproducible.

## Known Limitations and Next Work

The current CadQuery bridge exposes arbitrary Python and arbitrary export paths.
Work 006 should build the first constrained 3D component grammar and a closed
CadQuery -> STEP -> FreeCAD -> Level 0 mass/volume evidence loop. Fusion mutation
should be tested only in a new disposable design. Blender upgrade and Lab MCP
review should remain a separate planned work item.
