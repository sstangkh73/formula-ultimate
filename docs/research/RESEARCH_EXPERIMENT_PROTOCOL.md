# Research Experiment Protocol v1

Thai companion: `RESEARCH_EXPERIMENT_PROTOCOL.th.md`

Protocol ID: `formula_ultimate_research_experiment_protocol_v1`

Status: Active Phase-1 protocol

## Purpose and Claim Boundary

This protocol turns a declared 3D candidate into auditable evidence through:

```text
versioned declaration
  -> constrained CadQuery 3D B-rep
  -> hashed STEP exchange artifact
  -> FreeCAD import and independent measurement
  -> evidence admission
  -> Level 0 evaluation from FreeCAD-derived properties
  -> falsification review
```

Passing supports **geometry-to-Level-0 pipeline coherence only**. It does not
support a claim of physical validation, complete-vehicle feasibility, race
performance, safety, manufacturability, optimality, novelty, or discovery.
Level 0 remains a selection gate.

The protocol does not prescribe a conventional vehicle layout or known shape.
The first candidate deliberately uses the existing bounded
`mounting_plate_v1` grammar because the current repository does not yet contain
a complete-vehicle grammar, assembly-interface solver, or packaging/collision
system.

## Protocol Artifacts

- Protocol declaration:
  `config/experiments/research_experiment_protocol_v1.json`
- Candidate declaration:
  `config/experiments/candidate_fu-c0001.json`
- Admission contract:
  `src/formula_ultimate/experiments/research_protocol.py`
- Reproducible launcher: `scripts/run_candidate_001.ps1`
- Generated run evidence: `artifacts/work031/FU-C0001/` (Git-ignored)

Candidate declarations are immutable inputs to a run. A changed declaration,
protocol, grammar, adapter, or tolerance creates a new run identity; results
must never be rewritten to conceal the change.

## Required Stage Gates

| Stage | Required input | Pass condition | Observable failure |
|---|---|---|---|
| `declaration_gate` | protocol and candidate JSON | IDs, versions, class, SI values, grammar, controls, and tolerances are admitted | malformed/undeclared identity or invalid value |
| `cadquery_3d_generation` | admitted candidate | exactly one valid CadQuery solid without hidden repair | generation error, invalid shape, or solid count other than one |
| `step_export_identity` | generated B-rep | STEP begins `ISO-10303-21;`; size and SHA-256 are recorded | absent/invalid file or hash mismatch |
| `freecad_import_measurement` | exact STEP artifact | FreeCAD imports the same hash as one valid solid and reports volume, bounds, and centre of mass | import error, invalid shape, wrong hash, missing report, or wrong solid count |
| `level0_evidence_admission` | analytical, CadQuery, and FreeCAD evidence | dimensions/volumes pass predeclared tolerances; FreeCAD volume times declared density supplies mass | tolerance/contract failure; no analytical substitution |
| `falsification_review` | all stage evidence | supporting, contradicting, alternative, missing-evidence, and confidence fields are recorded | incomplete review or inflated claim |

No stage may silently clip parameters, repair geometry, replace missing
FreeCAD evidence with an analytical value, or convert a failure into a pass.
The runner writes `experiment_failure.json` with the failed stage and process
evidence when a boundary fails.

## Experiment Design Requirements

Every experiment must predeclare:

- protocol, experiment, candidate, grammar, component/material, and seed IDs;
- the preferred hypothesis and its claim boundary;
- independent variables, dependent variables, controls, and SI units;
- evidence tolerances and explicit success/failure criteria;
- compute route and tool/source/config/repository identity;
- intended baseline and budget controls when more than one candidate is ranked.

Every result must report supporting evidence, contradicting evidence,
alternative explanations, missing evidence, and confidence. Candidate/solver
failures remain observations in the dataset.

## Candidate `FU-C0001`

`FU-C0001` is a bounded component geometry specimen, not a whole vehicle. It
uses a `0.200 x 0.120 x 0.008 m` rounded plate, four declared mounting holes, a
central lightening radius of `0.025 m`, and a constant-density aluminium
assumption of `2700 kg/m^3`. Seed `31001` is recorded even though the current
grammar is deterministic.

Preferred hypothesis: the declared input can cross every required evidence
boundary without hidden repair or analytical substitution. With one candidate,
this run does not estimate a design-variable effect and cannot rank designs.

Controls for its Level 0 specimen evaluation are base vehicle mass `300 kg`,
tractive force `1200 N`, duration `5 s`, and timestep `0.05 s`. Level 0 uses
only the FreeCAD-measured volume to derive component mass.

## First Recorded Run

Command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_candidate_001.ps1
```

The first Work 031 run passed all six stages:

| Evidence | Recorded value |
|---|---:|
| STEP bytes | `55,774` |
| STEP SHA-256 | `13881EC14571A6AA8BC8EC3911E46D38C0364ED5691B002B6AB12BF0A0462383` |
| CadQuery volume | `0.0001739968154162849 m^3` |
| FreeCAD 1.1.3 volume | `0.00017399681541628494 m^3` |
| FreeCAD minus CadQuery volume | `5.421010862427522e-20 m^3` |
| FreeCAD solid count / validity | `1 / true` |
| FreeCAD-derived component mass | `0.4697914016239693 kg` |
| Level 0 final speed | `19.968729541866246 m/s` |
| Level 0 final distance | `49.9218238546656 m` |

The exact machine-readable result is
`artifacts/work031/FU-C0001/experiment_result.json`. The STEP hash authenticates
this run's artifact; semantic replay compares declared dimensions and physical
properties within tolerance because STEP exporter metadata may change bytes.

## Interpretation and Promotion Rule

The run supports that this local input crossed the declared software/evidence
route. It does not show that material removal is structurally useful or that
the part belongs in a competitive vehicle. CadQuery and FreeCAD also share
OCCT-family geometry technology, so their agreement is not independent theory.

Do not promote `FU-C0001` as a design discovery. Future promotion requires, at
minimum, declared interfaces and loads, stronger independent models, numerical
convergence, manufacturing/assembly/safety evidence, and fair comparison with
optimized baselines under equal candidate-evaluation or measured compute
budgets.
