# Work 095 Plan: Constructive Validity and Manufacturing Gate

Thai companion: `2026-09-04_095_constructive-validity-manufacturing-gate-plan.th.md`

## Status

Status: Completed

## Objective

Implement a deterministic fail-closed gate that prevents richer geometry from exploiting invalid B-rep declarations or bypassing declared process limits. The gate must separate constructive validity from coarse process-envelope checks, record all rejection causes, and make every permitted pre-evaluation repair part of genotype/provenance identity.

## Scope and planned files

- `config/manufacturing/constructive_validity_gate_v1.json`
- `src/formula_ultimate/components/constructive_validity.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/experiments/run_constructive_validity_pilot.py`
- `tests/test_constructive_validity.py`
- `docs/contracts/CONSTRUCTIVE_VALIDITY_MANUFACTURING_GATE_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored deterministic pilot/replay evidence under `artifacts/work095/`

## Independent/dependent variables and controls

- Independent inputs: representation family, exact source geometry identity, declared material/process, process-specific limits, synthetic measured witness values, repair declaration, repair budget, and evaluation-observed state.
- Dependent outputs: `accepted`, `repaired`, or `rejected`; complete ordered violation codes; constructive and process margins; repair trace; original/repaired genotype identities; validity yield; and rejection-cause counts by representation family.
- Matched controls: one primitive control and five curved/free-form Work 092 identities each receive the same eight frozen scenarios and compute opportunity. The scenario evidence is explicitly synthetic contract-verification data, not a claim that the source STEP has those measured dimensions.
- Negative controls: self-intersection, sliver/minimum feature, zero thickness, inaccessible feature/tool path, unsupported overhang/wall, hidden repair, enclosed void, tolerance, joining access, incompatible material/process, excessive repair budget, post-observation repair, unknown fields, non-finite values, and replay mutation.

## Gate order and repair rules

1. Validate exact schema, source identities, finite SI values, process profiles, compatibility, and equal scenario opportunity.
2. Apply only preregistered deterministic repairs before any evaluation observation. V1 admits `add_support`, `increase_escape_hole`, and `increase_joining_access`, with a fixed maximum operation count.
3. Hash the original candidate, ordered repair trace, and repaired candidate. A declared or detected repair that is missing from the trace is `hidden_repair` and rejects.
4. Evaluate constructive B-rep flags first, then process-specific wall, ligament, radius, minimum feature, tool access, overhang/support, enclosed void/escape, tolerance, joining access, and material/process compatibility.
5. Return every applicable violation rather than silently correcting or stopping after the first failure.

## Success criteria

- Each of six representation families receives exactly eight matched scenarios; unused/rejected opportunities remain counted.
- Baseline scenarios pass, preregistered support repairs return `repaired`, and injected self-intersection, sliver, zero-thickness, inaccessible feature, unsupported wall/overhang, and hidden-repair controls reject visibly for every family.
- Additional controls visibly reject enclosed void, impossible tolerance/joining access, incompatible material/process, repair after observation, and repair-budget violation.
- Original and repaired genotype/provenance hashes differ when a repair occurs; identical clean runs reproduce the complete ledger and result SHA-256.
- Focused tests, compilation, repository contracts, pilot/replay, and full regression pass.

## Risks and explicit non-goals

Coarse witness scalars can miss local geometry, orientation, collision, topology, and supplier-specific production limits. Synthetic matched controls prove gate behavior, not measured manufacturability of any Work 092 STEP. V1 does not infer thickness from CAD, repair arbitrary B-reps, plan tooling, certify a process/material, model cost, execute FEA/CFD, validate strength, or permit result-conditioned changes. Work 096 owns independent semantic geometry measurement.
