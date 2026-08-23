# CAD and MCP Environment

Date verified: 2026-08-23

## Purpose

This environment is the first executable 3D research layer for Formula
Ultimate. It gives an agent two complementary paths:

- Autodesk Fusion for interactive, history-based CAD through Autodesk's local
  MCP server;
- CadQuery for code-native parametric generation, inspection, rendering, and
  neutral export through a pinned community MCP server;
- FreeCAD as an independent local STEP producer/evaluator through
  `FreeCADCmd`;
- Blender as a future morphology, mesh, and visualization path once the
  installed version meets the official Blender Lab MCP requirement.

Connection is not engineering validation. Geometry produced through any path
must later pass independent topology, unit, manufacturability, physics, and
safety checks.

## Verified Status

| System | Verified version | Role | Status on 2026-08-23 |
|---|---:|---|---|
| Autodesk Fusion | 2704.1.53 | Interactive parametric CAD | Official local MCP enabled and protocol handshake passed |
| CadQuery | 2.8.0 | Code-native parametric CAD | Isolated environment installed; MCP list, inspect, and render passed |
| CadQuery MCP | 0.1.0 at `06b5e50a87fcf6808859f33d84e224fce675f8d7` | STDIO MCP bridge | Connected in project config; `mcp` constrained to 1.29.0 |
| FreeCAD | 1.1.3 revision 20260725 | Independent headless STEP evaluator | 10 x 20 x 30 mm solid export passed; no community MCP installed |
| Blender | 5.0.1 | Mesh/morphology/visualization | Installed, but official Blender Lab MCP not connected because it requires Blender 5.1+ |

The Fusion endpoint and enablement sequence match the [Autodesk MCP Server
help](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html).
The Blender decision follows the [official Blender Lab MCP
requirements](https://www.blender.org/lab/mcp-server/), including its warning
that generated Python executes without guards.

## Project MCP Configuration

The repository-owned `.codex/config.toml` defines:

- `fusion`: Streamable HTTP at `http://127.0.0.1:27182/mcp`;
- `cadquery`: STDIO through `scripts/cadquery_mcp.ps1`;
- both servers as optional, with tool approval set to `prompt`.

Codex supports project-local MCP configuration and local STDIO/Streamable HTTP
servers as described in the [official Codex MCP
documentation](https://developers.openai.com/codex/mcp/). A newly added project
configuration is loaded by a new/reopened task after the project is trusted.
The protocol was also tested directly in Work 005 so the result does not depend
on a UI connection badge.

`prompt` is a review gate, not a security sandbox. It does not make arbitrary
generated Python safe.

## CadQuery Bootstrap

The environment is ignored at `.tools/cadquery-mcp`. Bootstrap or repair it
with:

```powershell
py -3.14 -m pip install --user uv
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\bootstrap_cadquery_mcp.ps1
```

The bootstrap uses Python 3.12 and
`tools/cadquery-mcp-requirements.txt`. The CadQuery contrib source is pinned to
commit `06b5e50a87fcf6808859f33d84e224fce675f8d7`, and `mcp` is constrained to
major version 1 because CadQuery MCP 0.1.0 is incompatible with `mcp` 2.0.0.
The upstream package and tool descriptions are documented in the [CadQuery
contrib MCP README](https://github.com/CadQuery/cadquery-contrib/blob/master/mcp-server/README.md).

Probe it without changing an existing CAD document:

```powershell
$py = (Resolve-Path .tools\cadquery-mcp\Scripts\python.exe).Path
$server = (Resolve-Path .tools\cadquery-mcp\Scripts\cadquery-mcp.exe).Path
& $py scripts\cad\mcp_probe.py `
  --output artifacts\work005\cadquery_mcp_probe.json `
  stdio --command $server --inspect-box `
  --render-output artifacts\work005\cadquery_box.svg
```

The deterministic probe produces a 10 x 20 x 30 mm box. The 2026-08-23 run
reported volume 6000 mm3, surface area 2200 mm2, one solid, six faces, twelve
edges, eight vertices, and an SVG response with `render_is_error=false`.

## Fusion Probe

Fusion must remain open with **Preferences > General > API > Fusion MCP
Server** enabled. Test the endpoint without invoking a mutation tool:

```powershell
$py = (Resolve-Path .tools\cadquery-mcp\Scripts\python.exe).Path
& $py scripts\cad\mcp_probe.py `
  --output artifacts\work005\fusion_mcp_probe.json `
  http --url http://127.0.0.1:27182/mcp
```

The verified tool inventory was:

- `fusion_mcp_read`;
- `fusion_mcp_update`;
- `fusion_mcp_execute`;
- `fusion_mcp_electronics_read`.

Work 005 intentionally performed initialization and tool discovery only. It did
not call Fusion mutation/execute tools or create a cloud document.

## FreeCAD Headless Check

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\freecad_smoke.ps1
```

The launcher generates ignored artifacts under `artifacts/work005/`, confirms
the `ISO-10303-21;` STEP header, and prints dimensions, volume, byte size, and a
SHA-256 digest. FreeCAD 1.1.3 on this Windows installation mis-parsed CLI paths
containing spaces, so the launcher uses filesystem-provided 8.3 aliases for the
script and disposable output directory.

FreeCAD is presently an independent headless evaluator, not an MCP-connected
authoring surface. No unreviewed FreeCAD community MCP bridge was installed.

## Security Boundary

CadQuery MCP's four tools accept agent-supplied Python and evaluate it through
CadQuery CQGI. Its export tool also accepts a caller-supplied filename. The
current bridge therefore has arbitrary-code and arbitrary-path risk within the
user account. Controls in this bootstrap are limited to:

- isolated Python environment;
- pinned source revision and MCP major version;
- project-local launchers and configuration;
- approval prompts;
- disposable test geometry and ignored artifact paths;
- no credentials in configuration.

These controls improve auditability but do not provide process, filesystem, or
network isolation. Until a constrained structured design service is built,
inspect every generated script and export path before approval. Do not expose
this server to untrusted prompts or unrelated repositories.

Fusion update/execute tools also require review because they can mutate the
active document. Blender Lab carries an equivalent upstream warning for
generated Python; it remains disconnected in this environment.

## Next Recommended Work

Work 006 should define the first constrained 3D design experiment rather than
immediately granting open Python execution. Recommended boundary:

1. define a small typed component/design grammar and units;
2. generate a parameterized reference part through CadQuery;
3. export STEP and inspect it independently in FreeCAD;
4. compare computed mass/volume with the Level 0 physics kernel;
5. store design genome, tool calls, geometry hashes, and evaluator results;
6. only then test a Fusion mutation on a new disposable local design;
7. upgrade Blender to 5.1+ and review the official Lab bridge in a separate
   planned work item before enabling it.
