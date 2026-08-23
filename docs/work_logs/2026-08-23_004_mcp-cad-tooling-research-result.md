# Work Result 004: MCP-Compatible Engineering CAD Research

Date: 2026-08-23
Status: Completed

## Summary

Completed a bilingual, source-linked evaluation of software for detailed
mechanical-part design through MCP. The research distinguishes official vendor
MCP implementations from Labs/community bridges and recommends a multi-tool
Formula Ultimate geometry pipeline rather than treating any single CAD package
as generator, evaluator, and proof of correctness.

## Deliverables

- `docs/research/MCP_CAD_TOOLING_REPORT.md`
- `docs/research/MCP_CAD_TOOLING_REPORT.th.md`
- Separate English and Thai Work 004 plan/result records.

## Tools Evaluated

- Autodesk Fusion
- Onshape / FeatureScript
- CadQuery
- FreeCAD
- Blender
- OpenSCAD
- SOLIDWORKS

## Principal Findings

1. Autodesk Fusion MCP is now an official Autodesk General Availability local
   desktop integration with dynamic tools against a live Fusion session.
2. Onshape has an official Labs FeatureScript MCP for agent-generated,
   reusable, parametric text-to-code-to-CAD features.
3. CadQuery's project-contrib MCP provides the strongest first path for
   deterministic, code-first, headless B-rep generation and inspection.
4. FreeCAD has strong official CAD/CAE/Python capabilities, but the reviewed MCP
   options are separate community projects with fragmented tool surfaces.
5. Blender's official Lab MCP is valuable for procedural morphology, but its own
   page warns that generated code executes without guards; Blender mesh output
   is not treated as engineering proof.
6. OpenSCAD is a useful deterministic baseline, while SOLIDWORKS MCP remains a
   licensed community-bridge path rather than the first research choice.

## Recommendation

Use a layered pipeline:

```text
CadQuery MCP generation and property gate
  -> Level-0 / 1D screening
  -> Autodesk Fusion official MCP promotion and human review
  -> FreeCAD/project-owned bridge and authoritative FEA/CFD/thermal validation
```

Evaluate Onshape FeatureScript MCP as the reusable component-grammar path, then
introduce Blender as a separately gated novelty branch after the B-rep pipeline
is reliable.

## Source Validation Evidence

- Research date recorded: `2026-08-23`.
- English report unique primary/official source URLs: `24`.
- Thai report unique primary/official source URLs: `24`.
- URL-set difference between reports: none.
- Official CAD capability claims use vendor/project documentation.
- Community MCP capability claims link to the primary project repository.
- Official, Labs, community, and unverified/custom categories are stated
  separately.

## Repository Validation Evidence

Command:

```powershell
python -m unittest discover -s tests -v
```

Environment: Windows, Python 3.14.3

Exit code: `0`

Result:

```text
Ran 14 tests
OK
```

Final maintained documentation count after both result files:

```text
English Markdown files: 18
Thai companion files:   18
Missing companions:      0
```

Additional commands:

```powershell
python -m compileall -q src tests
git diff --cached --check
```

Exit code for each: `0`.

## Claims Supported

- The cited official MCP status of Fusion, Onshape Labs, and Blender Lab on the
  research date.
- The documented geometry/API/export capabilities of the evaluated tools.
- The exposed tool surface described by the linked primary community MCP
  repositories.
- A defensible toolchain recommendation based on Formula Ultimate's declared
  generation, validation, reproducibility, and security requirements.

## Missing Evidence and Limitations

- No CAD package or MCP server was installed or live-tested in this work item.
- Fusion's dynamic runtime tool inventory has not been captured from the user's
  installation.
- Onshape Labs availability, account permissions, and exact tool behavior have
  not been tested with the user's account.
- Community MCP source and dependencies have not yet undergone a security audit.
- Cost and feature availability can change by region, plan, and future release.
- Recommendations are therefore architecture-level with medium confidence;
  production selection requires the proposed proof of concepts.

## Deviations from Plan

- None. No external installation, account mutation, or purchase occurred.

## Recommended Next Work

Begin a separate bilingual installation/PoC work item for the restricted
CadQuery MCP geometry gate. Before installation, pin and review the exact server
revision and define the sandbox, candidate workspace, and component-interface
schema.
