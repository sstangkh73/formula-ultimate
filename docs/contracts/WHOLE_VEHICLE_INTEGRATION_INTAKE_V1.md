# Whole-Vehicle Integration Intake V1

Thai companion: `WHOLE_VEHICLE_INTEGRATION_INTAKE_V1.th.md`

Status: Implemented as Work 105, the first bounded phase toward the roadmap Work 101 milestone

## Purpose and claim boundary

This intake prevents a locally feasible or graph-diverse subsystem from being silently promoted into a whole-vehicle claim. It consumes the exact deterministic portion of Work 100 registration V2 evidence, preserves every scoped survivor, distinguishes active functional topology from inactive appendages, and reports missing vehicle capabilities and evidence classes.

The output is analysis-only typed subsystem intake. It is not a new physics solve, complete vehicle, `promotion_ready` decision, whole-vehicle admission, race comparison, technology-discovery result or physical validation. Work 101 remains a program milestone requiring later integration and stronger evidence.

## Active-path method

For each original edge and each field, the analyzer aggregates the maximum absolute flow over the finest registered Work 100 subdivision:

```text
mechanical_activity = max(abs(edge force)) / 5000 N
thermal_activity    = max(abs(edge heat flow)) / 30 W
```

An edge is active in one domain only when its relative activity is greater than `1e-8`. A coupled active edge must be active in both domains. Subdivision node labels are removed by recovering the first and last endpoints of each original edge. Inactive edges are retained in the report but excluded from the active topology.

The active simple graph is canonicalized over all node permutations, up to the frozen bound of eight active nodes. This produces an identifier-independent exact unlabelled simple-graph identity within that bound; oversize graphs fail rather than falling back to names. The identity deliberately does not encode source/sink coloring, geometry, parallel-edge multiplicity or direction, so it is an intake descriptor rather than universal mechanism proof.

Each candidate is paired with the fixed control of the same seed. A candidate becomes `functional_mechanism_candidate` only if:

1. it is already a Work 100 `candidate_survivor`;
2. its coupled active-topology identity differs from the paired fixed control; and
3. the absolute coupled-utilization difference is at least the frozen meaningful threshold `0.05`.

Differences must also exceed the sum of candidate and fixed numerical errors to be called detectable. Declared graph differences whose extra edges are inactive become `declared_topology_only_inactive_appendage`. Detectable geometry response with unchanged active topology remains a shape-response variant. A meaningful difference is not automatically an improvement because the registered objective minimizes utilization.

## Technology-neutral integration coverage

The required capabilities come directly from the existing functional vehicle contract rather than conventional component names or layout assumptions:

- energy storage and conversion;
- power transmission and ground propulsion;
- direction control and braking;
- load structure and heat rejection;
- controller.

Work 100 supplies credible local evidence only for `load_structure`. Its thermal conduction path does not prove a heat-rejection capability. It supplies scoped `candidate_survivor` and holdout evidence, but not independent higher fidelity, safety, coupled transient, energy, contact, failure or optimized-baseline evidence.

## Work 105 result

The input identities matched Work 100 registration `2c3aaa21ffb6ed36da532493c82c6e1f0195b13990180dc5d055c75fb47bdd45` and deterministic evidence `652ba7d9db9d76ed841d5b2c24af421075cc2d266a9098bc065fe4a8ac45da61`. Final-source runs C and D produced exact result SHA-256 `559fb55a4513003af35e302ddff9120ece830b88d8f19f62188a052c3411229e`.

- All ten scoped survivors remain eligible as typed load-structure subsystem inputs.
- Functional-mechanism candidates: `0`.
- Declared-topology inactive appendages: `4` (both `GRAPH_ONLY` and both `JOINT_MORPHOLOGY_CONTROLLER` candidates).
- Shape-response variants: `4` (two `MORPHOLOGY_ONLY` and two `RANDOM_CONTROL` candidates).
- `RANDOM_CONTROL`, seed `7`, exceeded the absolute `0.05` meaningful threshold with `+0.0586275`; because utilization is minimized, this is a meaningful worsening, not an improvement, and active topology remained unchanged.
- Missing vehicle capabilities: `8`; missing program-exit evidence classes: `7`.
- Final status: `blocked_incomplete_capability_and_evidence_coverage`; `work101_program_exit = false`; no whole-vehicle candidate was created.

The preferred hypothesis that Work 100 contained an active-topology functional-mechanism candidate was falsified at this intake fidelity. This does not erase local feasibility or geometry-response evidence.

## Reproduction

```powershell
$env:PYTHONPATH = Join-Path $PWD 'src'
python -m unittest tests.test_integration_intake -v
python scripts/experiments/run_integration_intake.py --output artifacts/work105/run_c/result.json
python scripts/experiments/run_integration_intake.py --output artifacts/work105/run_d/result.json --replay-reference artifacts/work105/run_c/result.json
```

Generated evidence under `artifacts/work105/` is ignored by Git. A later integration phase must add missing survivor types and evidence; it must not reclassify this negative intake or prescribe a conventional vehicle layout to make coverage easier.
