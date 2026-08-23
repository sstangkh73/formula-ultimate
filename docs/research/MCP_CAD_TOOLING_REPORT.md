# MCP-Compatible Engineering CAD Tooling Report

Research date: 2026-08-23

> This is the English source for `MCP_CAD_TOOLING_REPORT.th.md`.

## Executive Verdict

Formula Ultimate should not choose one program for both open-ended geometric
search and authoritative engineering review. The strongest current architecture
is a two-engine pipeline:

1. **CadQuery + CadQuery MCP** for deterministic, code-first, headless B-rep
   generation and high-volume candidate screening.
2. **Autodesk Fusion + the official Fusion MCP Server** for detailed interactive
   mechanical CAD, human review, assemblies, manufacturing handoff, and selected
   higher-fidelity work.

**Onshape + the official Onshape Labs FeatureScript MCP Server** is the strongest
cloud-native alternative and may become the best long-term agent-native
parametric system, especially for reusable component generators. It is currently
an Onshape Labs early-access feature, whereas Autodesk lists Fusion MCP as
General Availability.

FreeCAD is the preferred open-source independent CAD/CAE route, but its MCP
servers are community projects rather than official FreeCAD integrations.
Blender is valuable for morphology, lattices, procedural meshes, and visual
inspection, but should not be the source of truth for precision mechanical
solids. OpenSCAD is excellent for a small deterministic demo but too limited as
the final Formula Ultimate geometry engine.

## What “Detailed Part Design” Requires

For this project, MCP connectivity alone is insufficient. A credible tool must
support most of the following:

- exact solids or B-rep, not only triangle meshes;
- parametric dimensions and stable design intent;
- sketches, constraints, booleans, fillets, chamfers, lofts, and sweeps;
- assemblies or explicit component interfaces;
- material assignment and independently computed mass/volume/inertia;
- neutral export such as STEP and BREP;
- deterministic regeneration and inspectable source/history;
- batch/headless operation for search;
- an independent path to FEA, CFD, thermal, or manufacturing validation;
- bounded MCP tools, artifact isolation, and reproducible tool-call logs.

## Comparison Summary

| Tool | Geometry/design depth | MCP status on research date | Headless/search fit | Main limitation | Formula Ultimate role |
|---|---|---|---|---|---|
| Autodesk Fusion | Professional parametric/direct/surface/mesh CAD, assemblies, CAM/CAE | **Official Autodesk, GA**, local dynamic MCP | Low–medium; live desktop session | Proprietary, session-based, not a natural 100k-candidate engine | Authoritative interactive CAD and manufacturing review |
| Onshape | Professional cloud parametric CAD, FeatureScript, assemblies/PDM | **Official Onshape Labs**, early access | Medium–high through FeatureScript/API | Cloud/IP boundary; Labs feature; license tiers | Agent-authored reusable features and cloud collaboration |
| CadQuery | OCCT B-rep, Python parametric parts, constrained assemblies | CadQuery-project `cadquery-contrib` MCP, not a vendor service | **High** | Less mature GUI/drawings/CAE workflow | Primary code-first geometry generator |
| FreeCAD | Full-precision OCCT B-rep/NURBS, parametric CAD, assemblies, drawings, FEM/CAM | Community MCP servers; no verified official FreeCAD MCP | Medium–high with Python/headless tools | MCP fragmentation and variable maturity | Open-source independent CAD/CAE evaluator |
| Blender | Mesh/curve/procedural Geometry Nodes, sculpting/rendering | Official Blender Lab MCP; community alternatives also exist | High for procedural mesh/render work | Not a precision mechanical B-rep/constraint system | Morphology exploration and visualization |
| OpenSCAD | Deterministic constructive solid geometry scripts | Community MCP servers | High | Primarily mesh export; weak assemblies/surfacing; no native STEP in reviewed MCP | Small baseline and simple parametric fixtures |
| SOLIDWORKS | Professional mechanical CAD, assemblies, drawings | Community MCP bridges; explicitly not vendor-endorsed | Low–medium, Windows desktop | Licensed proprietary CAD plus community bridge | Only if an existing licensed workflow justifies it |

## Detailed Findings

### 1. Autodesk Fusion — best official local MCP for detailed interactive CAD

Autodesk now documents the **Autodesk Fusion MCP Server as General
Availability**. It runs locally inside an active Fusion desktop session, exposes
dynamic tools to MCP clients, performs real-time modeling and command
operations, and is local-only without remote authentication. Fusion must remain
open and the server is enabled under `Preferences > General > API`; the default
endpoint is `http://127.0.0.1:27182/mcp`.
([Autodesk MCP catalog](https://help.autodesk.com/view/ADSKMCP/ENU/),
[Fusion MCP documentation](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_autodesk_fusion_mcp_server_html),
[connection guide](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html))

Fusion itself supports constrained sketches, history-based parametric features,
direct editing, surfaces, meshes, freeform T-splines, sheet metal, assemblies,
rendering, and integrated manufacturing workflows.
([official Fusion feature list](https://www.autodesk.com/products/fusion-360/features))

Why it fits Formula Ultimate:

- It is the strongest current “connect an agent to professional CAD now” option.
- The agent can work in a live model while a human observes and reviews changes.
- Native part/assembly history is more useful for engineering review than a
  final mesh alone.
- Fusion can act as a promotion environment after a candidate passes cheap
  headless screening.

Why it should not be the only search engine:

- The MCP server is session-based and its tool surface is discovered dynamically.
- Fusion must be running on one desktop, which is awkward for massive parallel
  evolution.
- Native files and some advanced simulation/generative capabilities create
  licensing and cloud dependencies.
- The local MCP endpoint has no authentication because it is local-only; the
  MCP client and workstation still need strict tool permissions and isolation.

Licensing note: Autodesk states that qualifying students and educators can use
Fusion educational access, while personal-use access is limited to qualifying
non-commercial work. Generative Design uses specific entitlements, an extension,
or tokens, so availability must be verified separately.
([Fusion eligibility](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Do-I-qualify-for-free-use-of-Fusion-360.html),
[Generative Design overview](https://help.autodesk.com/view/fusion360/ENU/?contextId=GD-F360-GENERATIVE-DESIGN))

Verdict: **Recommended as the first official MCP-connected engineering CAD and
human-review environment, but not as the high-volume evolutionary backend.**

### 2. Onshape FeatureScript MCP — best official agent-native parametric path

Onshape released an official **FeatureScript MCP Server through Onshape Labs**.
It connects MCP clients to Onshape's native FeatureScript language so an agent
can generate, insert, run, evaluate, and revise reusable parametric custom
features. Onshape describes this as text-to-code-to-CAD rather than one-off mesh
generation. The service is currently an early-access Labs feature.
([Onshape announcement](https://www.onshape.com/en/blog/featurescript-mcp-server-enables-text-code-cad))

FeatureScript is the same parametric language underlying Onshape Part Studio
features. It has 3D math types, robust geometric references, access to the
standard feature library, and a stated determinism principle: models should
regenerate the same way every time and cannot depend on external time or
randomness.
([FeatureScript introduction](https://cad.onshape.com/FsDoc/index.html),
[language model and determinism](https://cad.onshape.com/FsDoc/intro.html))

This is unusually well aligned with Formula Ultimate:

- The agent produces reusable geometry-generating programs, not only final
  artifacts.
- FeatureScript parameters can represent interface ports, keep-out regions,
  manufacturing limits, and component families.
- Onshape provides version history, branching, sharing, parts, assemblies, and
  neutral exports including STEP/STEP AP242.
  ([Onshape export support](https://www.onshape.com/en/resource-center/tech-tips/how-to-import-and-export-with-onshape))

Important boundaries:

- The official Labs MCP is FeatureScript-focused; it should not be assumed to
  expose every assembly, drawing, simulation, or PDM operation.
- The workflow is cloud-native, so IP, account permissions, network dependency,
  and bulk-evaluation cost must be reviewed.
- Labs means the service and tool surface may change.
- Engineering review remains required; Onshape explicitly makes this point in
  its own AI/CAD discussion.

Cost/privacy note: Onshape Free stores documents publicly and is non-commercial.
The free Student plan offers professional modeling, assemblies, drawings, data
management, and collaboration, but not all educator/professional simulation
features. Paid private plans are currently listed at USD 1,500/user/year for
Standard and USD 2,500/user/year for Professional.
([Onshape pricing](https://www.onshape.com/en/pricing),
[education plans](https://www.onshape.com/en/education/plans))

Verdict: **Recommended for a second proof of concept and potentially the best
long-term reusable component-grammar system, subject to Labs stability and IP
policy.**

### 3. CadQuery MCP — best first engine for reproducible automated search

CadQuery is a Python parametric CAD framework built on Open CASCADE/OCCT and
uses B-rep solids. It supports constrained assemblies and STEP assembly export.
([CadQuery concepts](https://cadquery.readthedocs.io/en/stable/primer.html),
[assembly constraints](https://cadquery.readthedocs.io/en/latest/assy.html),
[STEP export](https://cadquery.readthedocs.io/en/latest/importexport.html))

The `CadQuery/cadquery-contrib` repository contains a CadQuery MCP server. It can
execute CadQuery scripts, render multiple views, inspect bounding box, volume,
surface area, center of mass and topology counts, extract script parameters, and
export STEP, STL, SVG, DXF, AMF, 3MF, VRML, and BREP.
([CadQuery MCP primary repository](https://github.com/CadQuery/cadquery-contrib/tree/master/mcp-server))

Why this is the best Formula Ultimate starting point:

- Geometry is code, so every candidate has a diffable, hashable genotype.
- It runs without a heavy interactive CAD session and can be placed in a worker
  process or container.
- B-rep and STEP preserve an engineering-solid path rather than immediately
  collapsing every candidate to triangles.
- The MCP already exposes property inspection and neutral export needed for an
  early trusted-evaluator gate.
- Python integrates naturally with the existing Formula Ultimate simulator,
  telemetry, optimization, and test infrastructure.

Limitations and risks:

- The MCP executes generated Python/CadQuery code; it must run in a sandbox with
  a bounded workspace, resource limits, and no secrets/network by default.
- CadQuery is code-first, not a complete professional drawing/CAM/CAE desktop.
- OCCT operations can fail on pathological fillets, tiny features, or invalid
  topology; failure rate must become research telemetry, not be retried silently.
- A rendered preview does not prove a valid, manufacturable solid.

Verdict: **Recommended as Phase A: the first MCP geometry generator and batch
screening engine.**

### 4. FreeCAD + community MCP — best open-source independent evaluator

FreeCAD officially provides full-precision solids using Open CASCADE, B-rep and
NURBS, parametric objects, constraint sketches, assemblies, Python automation,
STEP/IGES/STL export, drawings, FEM, CAM, and other engineering workbenches.
([official FreeCAD capabilities](https://www.freecad.org/features.php?lang=eng_EN))
FreeCAD is LGPL2+ and supports unrestricted commercial or non-commercial use of
the application and produced designs.
([FreeCAD licensing](https://www.freecad.org/contributing.php?lang=eng))

Several community MCP servers exist. A representative engineering-focused
server from TESSA Labs exposes parametric creation, material/mass properties,
design sweeps, STEP export, drawings, defeaturing, meshing, boundary tagging,
and handoff to Elmer/CalculiX/OpenFOAM. It is MIT-licensed but is a small,
independent project, not an official FreeCAD integration.
([TESSA Labs FreeCAD MCP](https://github.com/tessalabs-space/freecad-mcp))

Formula Ultimate role:

- independent re-open/recompute/check of STEP or FCStd artifacts;
- second OCCT-based implementation for detecting pipeline inconsistencies;
- open-source meshing and CAE preparation;
- local use when cloud CAD is unacceptable.

Main concern: there is no single canonical FreeCAD MCP. Multiple servers expose
different tool sets and bridge architectures. Selecting one requires source
review, pinned revisions, live acceptance tests with the exact FreeCAD release,
and possibly building a small project-owned MCP surface instead.

Verdict: **Recommended as an independent open-source evaluator and future
project-owned bridge, not the first unreviewed generation server.**

### 5. Blender MCP — excellent exploration, not engineering authority

Blender now has an official Blender Lab MCP server for Blender 5.1+. It provides
natural-language access to Blender's Python API, but Blender explicitly warns
that generated code executes without guards and recommends using a virtual
machine or a system without sensitive data.
([official Blender Lab MCP page](https://www.blender.org/lab/mcp-server/))

Blender's procedural Geometry Nodes and Python API are powerful for:

- unusual morphology and organic/exotic forms;
- lattices, fields, ducts, surface textures, and mesh experiments;
- visual rendering and human inspection;
- geometry that may be difficult to express in sketch/extrude CAD grammars.

A community fork also documents structured, revisioned Geometry Nodes patches
with dry-run and actual-diff behavior, which is safer conceptually than arbitrary
`bpy` execution but still requires third-party source review.
([structured Blender MCP Geometry Nodes tools](https://github.com/newo-ether/blender-mcp/blob/main/docs/geometry-nodes.md))

Inference: because the reviewed Blender workflow is mesh/Geometry-Nodes based,
it should not be treated as the authoritative source for exact B-rep features,
engineering sketches, tolerances, or manufacturing drawings. Generated geometry
must pass manifold/solid checks, dimensional extraction, material assignment,
mesh convergence, and independent FEA/CFD before entering fitness.

Verdict: **Add only after the B-rep pipeline works; use it as a novelty branch
and visualizer, not as the only CAD truth source.**

### 6. OpenSCAD MCP — simplest deterministic baseline

Community OpenSCAD MCP servers can validate `.scad`, render multiple views,
analyze dimensions/triangle count, manage project files, and export STL, 3MF,
AMF, OFF, DXF, or SVG. The reviewed server does not list STEP/B-rep export.
([OpenSCAD MCP primary repository](https://github.com/quellant/openscad-mcp),
[official OpenSCAD CLI](https://files.openscad.org/documentation/manual/Using_OpenSCAD_in_a_command_line_environment.html))

OpenSCAD is useful for a one-day MCP smoke test because its text source is
deterministic and easy to parameter sweep. It is less suitable for advanced
surfaces, robust feature history, constrained assemblies, or detailed
manufacturing handoff.

Verdict: **Useful as a minimal baseline or fixture generator, but CadQuery
dominates it for Formula Ultimate's main engineering path.**

### 7. SOLIDWORKS community MCP — capable but not the first choice

SOLIDWORKS is a deep mechanical CAD environment, and community MCP bridges now
expose parts, assemblies, configurations, drawings, inspection, verification,
and automation plans through Windows COM or optional in-process add-ins. The
reviewed project explicitly states that it is independent and not endorsed by
Dassault Systèmes/SOLIDWORKS, and requires Windows plus a licensed installation.
([representative SOLIDWORKS MCP repository](https://github.com/danielproxd2/solidworks-mcp))

This path is reasonable only if Formula Ultimate already has a licensed
SOLIDWORKS workflow or requires specific supplier compatibility. Otherwise it
adds license cost and a community automation bridge without improving the
high-volume open-ended search architecture.

Verdict: **Do not prioritize for the initial research prototype.**

## Recommended Formula Ultimate Architecture

```text
Research requirement / component interface schema
  -> search agent
  -> CadQuery source generator through a restricted MCP tool surface
  -> isolated execution worker
  -> B-rep validity + bounding box + volume + center of mass
  -> STEP/BREP + source + parameters + hashes
  -> Level-0 property contract and 1D race screening
  -> selected candidates only
      -> Autodesk Fusion official MCP for detailed review/editing
      -> FreeCAD/project-owned MCP for independent re-open and CAE preparation
      -> FEA / thermal / CFD authoritative solvers
  -> solver results and failures returned to search

Optional novelty branch after baseline validation:
  Blender Geometry Nodes / implicit-mesh generator
  -> manifold + dimensions + material + mesh-convergence gates
  -> independent simulation
```

Onshape can replace or complement Fusion when reusable FeatureScript component
families, cloud collaboration, branching, and PDM provide more value than local
desktop control.

## Why a Project-Owned MCP Layer Is Still Necessary

Even when the CAD vendor provides MCP, Formula Ultimate should eventually expose
its own narrow tools rather than giving the search agent every CAD command:

- `create_candidate(source, parameters, interface_schema)`
- `validate_solid(candidate_id)`
- `inspect_mass_properties(candidate_id, material_id)`
- `export_neutral(candidate_id, format)`
- `promote_candidate(candidate_id, fidelity_level)`
- `run_authoritative_analysis(candidate_id, case_id)`

The wrapper should enforce workspace roots, immutable candidate IDs, time/memory
limits, allowlisted imports, no implicit network, material-library control,
artifact hashes, solver versions, and append-only telemetry. This turns MCP into
a controlled research interface rather than unrestricted remote control of a
desktop application.

## Proof-of-Concept Sequence

### PoC A — CadQuery MCP geometry gate

1. Install CadQuery and pin a reviewed `cadquery-contrib` revision.
2. Run the MCP server in an isolated environment without secrets or unrestricted
   filesystem/network access.
3. Define one component interface schema: two mounting planes, four bolt holes,
   a keep-out volume, load points, material, and maximum envelope.
4. Ask the agent to generate ten parametrically distinct mounting brackets.
5. Require valid single solids, exact interface geometry, STEP/BREP export,
   bounding box, volume, surface area, and center of mass.
6. Rebuild each candidate twice and compare source/artifact/property hashes.
7. Record invalid-solid rate, regeneration rate, wall time, and diversity.

### PoC B — official Fusion MCP promotion

1. Enable the official Fusion MCP locally and inspect the runtime-discovered
   tool list; do not assume undocumented tools.
2. Import the best three STEP candidates into copies of a review project.
3. Verify dimensions, interfaces, editable conversion path, material assignment,
   assembly fit, and manufacturing drawing capability.
4. Record every manual repair. A candidate needing hidden repair fails automatic
   promotion.

### PoC C — Onshape FeatureScript grammar

1. Use an education/private-appropriate account and review Onshape Labs terms.
2. Ask the official MCP to build one reusable custom feature for the same
   bracket interface rather than ten unrelated parts.
3. Generate parameter families and verify deterministic regeneration, version
   history, STEP export, and branch comparison.
4. Compare token/tool calls and failure rate against CadQuery.

### PoC D — novelty geometry branch

Only after A–C are reliable, introduce Blender/implicit geometry for lattice or
duct candidates. Do not promote any mesh because it looks innovative; require
the same interface, material, manifold, minimum-feature, mesh-convergence, and
solver gates.

## Acceptance Metrics

- valid-solid generation rate;
- exact interface compliance rate;
- deterministic rebuild/hash agreement;
- STEP re-import success in two independent CAD systems;
- property disagreement between generators/evaluators;
- wall time and compute cost per valid candidate;
- number of hidden/manual repairs;
- FEA/CFD meshing success and convergence rate;
- topology/shape diversity after removing parameter-only duplicates;
- promotion survival from cheap model to authoritative analysis.

## Security and Research-Integrity Requirements

- Pin exact MCP and CAD versions; never install community servers from a moving
  branch inside the research environment.
- Review source and dependencies before connection.
- Run code-executing MCP servers in isolated workers with no project secrets.
- Give each candidate a fresh bounded directory and deny paths outside it.
- Separate read/inspect tools from mutate/execute/export tools.
- Require explicit promotion approval before high-cost solvers or cloud uploads.
- Preserve prompts, tool calls, responses, source, geometry, hashes, CAD version,
  solver version, seed, and failures.
- Treat CAD rebuild failure and solver disagreement as data, not inconvenient
  errors to hide.

## Final Recommendation

If only one program is installed first, choose **Autodesk Fusion with its
official GA MCP** because the user is on Windows, needs detailed real mechanical
parts, and may qualify for educational access.

If the objective is the first autonomous geometry experiment, start with
**CadQuery MCP** because it is code-first, B-rep based, headless-friendly,
testable, and easy to connect to the existing Python research stack.

Therefore the practical order is:

1. CadQuery MCP sandbox and component-interface PoC.
2. Autodesk Fusion official MCP as human-visible promotion/review CAD.
3. FreeCAD as independent open-source re-import/CAE checker.
4. Onshape Labs FeatureScript MCP experiment for reusable component grammars.
5. Blender novelty branch only after engineering gates are reliable.

This arrangement gives the agent real geometric freedom without allowing the
same agent or MCP server to invent both the shape and the evidence that the shape
works.
