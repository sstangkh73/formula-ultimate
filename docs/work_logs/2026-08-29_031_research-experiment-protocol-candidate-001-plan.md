# Work 031 Plan: Research Experiment Protocol and Candidate 001

Status: Completed

Thai companion: `2026-08-29_031_research-experiment-protocol-candidate-001-plan.th.md`

## Objective

Create a versioned Research Experiment Protocol for geometry-derived Formula
Ultimate experiments and execute the first protocol candidate through the
closed `3D -> STEP -> FreeCAD -> Level 0` evidence route.

## Scope

- Define protocol identity, candidate identity, immutable input/evidence
  requirements, stage gates, claim levels, replay metadata, and falsification
  review requirements.
- Predeclare one bounded first candidate, `FU-C0001`, using the existing
  `mounting_plate_v1` grammar as a geometry-evidence specimen.
- Generate the candidate as a CadQuery B-rep, export a hashed STEP file, import
  and measure that exact file in FreeCAD, and admit only the FreeCAD measurement
  to the existing Level 0 point-mass evaluation.
- Record structured success or failure evidence without silent geometry repair,
  parameter clipping, or analytical substitution.
- Add focused automated tests for the protocol evidence contract and maintain
  English/Thai documentation pairs.

## Planned Files

- `docs/research/RESEARCH_EXPERIMENT_PROTOCOL.md`
- `docs/research/RESEARCH_EXPERIMENT_PROTOCOL.th.md`
- `config/experiments/research_experiment_protocol_v1.json`
- `config/experiments/candidate_fu-c0001.json`
- `src/formula_ultimate/experiments/research_protocol.py`
- `src/formula_ultimate/experiments/__init__.py`
- `scripts/cad/run_research_candidate.py`
- `scripts/run_candidate_001.ps1`
- `tests/test_research_protocol.py`
- matching Work 031 plan/result records in English and Thai

Generated CAD and result evidence will remain Git-ignored under
`artifacts/work031/FU-C0001/`.

## Experiment Definition

### Preferred hypothesis

The declared `FU-C0001` input can traverse every required evidence boundary
without hidden repair: one valid CadQuery solid can be exported to STEP,
FreeCAD can import the exact hashed STEP as one valid solid, the independently
reported dimensions and volume can pass declared tolerances, and Level 0 can
consume the FreeCAD-derived mass.

This is a pipeline-coherence hypothesis, not a performance, structural, safety,
manufacturing, novelty, or complete-vehicle hypothesis.

### Independent variables

- candidate geometry declaration and candidate ID;
- protocol and grammar versions.

The first run contains one predeclared candidate, so it does not estimate a
design-variable effect or rank alternatives.

### Dependent variables

- CAD validity and solid count;
- STEP header, byte size, and SHA-256 identity;
- CadQuery and FreeCAD volume, bounds, and centre of mass;
- cross-tool and analytical residuals;
- density-derived component mass;
- Level 0 final speed and final distance;
- stage status, failure code, tool versions, source hashes, and wall time.

### Controls

- `mounting_plate_v1` grammar and declared material density;
- geometry parameters, Level 0 base mass, force, duration, and timestep;
- CAD/STEP/FreeCAD adapter route and evidence tolerances;
- deterministic seed and repository/source identity.

### Falsification and failure criteria

- Reject undeclared IDs, versions, units, non-finite values, invalid topology,
  a missing/invalid STEP header, hash mismatch, FreeCAD import failure, a solid
  count other than one, invalid FreeCAD geometry, tolerance failure, missing
  evidence, or Level 0 contract failure.
- Preserve the failing stage and message; never substitute an analytical value
  for absent or rejected FreeCAD evidence.
- Record supporting evidence, contradicting evidence, alternative explanations,
  missing evidence, and confidence even when the pipeline passes.

## Validation

Planned fail-fast commands:

```powershell
py -3.14 -m unittest tests.test_research_protocol -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_candidate_001.ps1
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exact commands, exit statuses, relevant output, artifact hashes, limitations,
and the resulting commit hash will be recorded in the Work 031 result.

## Success Criteria

- The protocol and candidate declarations are versioned and machine-readable.
- `FU-C0001` produces one valid solid and one STEP artifact without hidden
  repair.
- FreeCAD measures the exact STEP hash as one valid solid.
- Analytical, CadQuery, and FreeCAD evidence agrees within predeclared
  tolerances.
- Only FreeCAD-derived volume and declared density determine the mass passed to
  Level 0.
- The result contains sufficient source/config/tool/repository identity for
  deterministic semantic replay.
- Focused and full validation pass, explicit work-item files are committed, and
  the commit succeeds.

## Risks

- CadQuery and FreeCAD both use OCCT-family geometry technology, limiting the
  independence of their agreement.
- STEP byte hashes may change across exports because exporter metadata can
  include time-dependent fields; replay must compare declared geometry and
  physical properties within tolerance as well as authenticate each run's
  exact artifact.
- A single bounded component cannot establish complete-vehicle feasibility or
  compare candidate performance.
- Level 0 reduces this geometry to constant-density added point mass and omits
  structural, thermal, aerodynamic, manufacturing, assembly, and safety
  behavior.

## Explicit Non-Goals

- No claim of a complete vehicle, race readiness, optimality, discovery, or
  physical validation.
- No free-topology generation, conventional vehicle-layout prescription, or
  comparison against optimized baselines.
- No FEA, CFD, fatigue, crash, thermal, electromagnetic, manufacturing, or
  empirical validation.
- No Fusion mutation, external upload, publication, push, or history rewrite.
