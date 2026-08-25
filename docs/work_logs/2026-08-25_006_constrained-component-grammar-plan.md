# Work 006 Plan: Constrained 3D Component Grammar and Evidence Loop

Status: Completed

Thai companion: `2026-08-25_006_constrained-component-grammar-plan.th.md`

## Objective

Create the first versioned, constrained 3D component grammar and execute a
reproducible evidence loop from CadQuery generation, through neutral STEP
exchange and independent FreeCAD measurement, into the existing Level 0
longitudinal physics kernel.

## Scope

- Define `mounting_plate_v1`, a deliberately small grammar for a rounded
  structural mounting plate with:
  - one bounded plate body;
  - one fixed four-hole mounting interface;
  - one optional bounded central lightening cut;
  - an explicit material density;
  - SI-unit inputs and an explicit millimetre conversion only at the CAD API
    boundary.
- Reject invalid or non-finite parameter combinations before CadQuery runs.
- Generate deterministic single-solid CadQuery geometry and STEP artifacts.
- Re-import each STEP artifact in headless FreeCAD and independently report
  solid count, volume, bounding box, and centre of mass.
- Convert the FreeCAD-measured volume to component mass and add it to a fixed
  vehicle baseline in the Level 0 longitudinal model.
- Run a controlled three-candidate lightening-radius experiment and one
  deliberately invalid candidate intended to falsify the grammar gate.
- Preserve machine-readable manifests, hashes, replay inputs, and results under
  the ignored `artifacts/work006/` tree.
- Add unit and integration tests for every implemented grammar rule and for the
  CAD-to-Level-0 evidence contract that can be tested without launching external
  CAD processes.
- Maintain all new or changed Markdown in separate English and Thai files.

## Planned Files

- `src/formula_ultimate/components/grammar.py`
- `src/formula_ultimate/components/__init__.py`
- `src/formula_ultimate/experiments/cad_level0.py`
- `src/formula_ultimate/experiments/__init__.py`
- `scripts/cad/generate_mounting_plate.py`
- `scripts/cad/inspect_step_freecad.py`
- `scripts/run_work006.ps1`
- `tests/test_component_grammar.py`
- `tests/test_cad_level0.py`
- `docs/3d/CONSTRAINED_COMPONENT_GRAMMAR.md`
- `docs/3d/CONSTRAINED_COMPONENT_GRAMMAR.th.md`
- matching Work 006 plan and result records in English and Thai

The exact list may change if repository inspection exposes a smaller safe
interface. Any deviation will be recorded in the result.

## Experiment Definition

### Preferred hypothesis

For otherwise identical valid plates, increasing the central lightening radius
will monotonically reduce independently measured volume and mass. Under the
same fixed Level 0 tractive force and environment, the lower total vehicle mass
will monotonically increase final speed and distance.

This is a pipeline-coherence hypothesis, not a structural-performance claim.

### Independent variable

- central lightening-cut radius in metres, with three predeclared valid levels

### Dependent variables

- CadQuery and analytical volume;
- FreeCAD STEP-import volume, solid count, bounding box, and centre of mass;
- density-derived component mass;
- Level 0 final speed and distance;
- cross-tool volume residuals and artifact hashes.

### Controls

- grammar version and generator implementation;
- plate outer dimensions, thickness, corner radius, mounting-hole diameter, and
  mounting-hole coordinates;
- material and density;
- CadQuery and FreeCAD versions;
- base vehicle mass, tractive force, environment, duration, and timestep;
- deterministic seed (recorded even though version 1 has no stochastic rule).

### Falsification and failure cases

- Submit a predeclared central cut that violates the minimum-web constraint and
  require rejection before CAD execution.
- Treat any non-finite input, invalid single-solid topology, STEP import
  failure, unexpected solid count, excessive volume disagreement, or
  non-monotonic controlled result as an observable failure.
- Record supporting evidence, contradicting evidence, alternative
  explanations, missing evidence, and confidence in the result.

## Validation

Planned commands include:

```powershell
py -3.14 -m unittest discover -s tests -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work006.ps1
py -3.14 -m compileall -q src scripts tests
git diff --check
```

The launcher will invoke the pinned Work 005 CadQuery Python environment and
the verified FreeCAD 1.1 headless executable. Exact commands, exit statuses,
relevant output, versions, hashes, and artifact paths will be captured in the
result record.

## Success Criteria

- The grammar rejects the deliberate invalid candidate before CadQuery runs.
- Every valid candidate produces one deterministic valid solid and a STEP file.
- FreeCAD independently imports every STEP file as exactly one solid.
- Analytical, CadQuery, and FreeCAD volumes agree within declared absolute and
  relative tolerances; no discrepancy is silently corrected.
- FreeCAD-derived mass is the value used by Level 0, with SI units explicit.
- The controlled outputs satisfy the predeclared monotonic expectation or the
  work is reported as failed/stopped with the contradicting evidence.
- Unit, integration, repository-contract, compile, and whitespace checks pass.
- Replay metadata is sufficient to rerun the experiment on the verified local
  toolchain.

## Risks

- CadQuery and FreeCAD use the same OCCT family, so agreement is an independent
  application/import check but not fully independent geometric theory.
- STEP tolerances or topology healing may create small volume differences.
- FreeCAD 1.1.3 mis-parses command-line paths containing spaces; the launcher
  must use the already verified short temporary-path pattern.
- A geometry that passes this grammar is not thereby strong, manufacturable,
  fatigue-safe, collision-safe, or suitable for a vehicle.
- The mass effect in a simple Level 0 constant-force case may be numerically
  small; results must retain adequate precision rather than exaggerate it.

## Explicit Non-Goals

- No FEA, CFD, thermal analysis, fatigue analysis, crash analysis, topology
  optimization, manufacturing certification, or real-world safety validation.
- No claim that `mounting_plate_v1` is a race-ready or optimal component.
- No Fusion mutation and no FreeCAD community MCP installation.
- No free-topology comparison or scientific conclusion about design discovery.
- No silent parameter clipping, topology repair, or substitution of failed CAD
  evidence with analytical values.
