# Work 090 Plan: Search-Space Bias and Diversity Contract

Thai companion: `2026-09-04_090_search-space-bias-diversity-contract-plan.th.md`

## Status

Status: Completed

## Objective

Implement the first work in `GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1`: a deterministic, name/rigid-transform/uniform-scale-invariant diversity contract and a reproducible census of the current bounded whole-vehicle proposal space. The result must quantify the fixed-topology/primitive bias before Work 091 expands representation.

## Scope and planned files

- `config/experiments/design_diversity_v1.json`
- `src/formula_ultimate/experiments/design_diversity.py`
- `scripts/experiments/run_design_diversity_baseline.py`
- `tests/test_design_diversity.py`
- `docs/contracts/DESIGN_DIVERSITY_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored evidence under `artifacts/work090/`

## Independent/dependent variables and controls

- Independent inputs: exact current base assembly, exact current Work 050 search protocol, frozen treatment/seed/attempt ledgers, and injected metamorphic/topology controls.
- Dependent outputs: topology signature, normalized geometry signature, primitive fraction, operator/type entropy, curvature-class distribution, graph-path signatures, unique-signature ratios, duplicate phenotype rate, and rejection causes.
- Controls: translation, rigid axis permutation/sign change, component/interface renaming, uniform scale, branch addition, path reroute, primitive-family change, and interface-topology change.

## Validation and success criteria

- Equivalent translation, rotation/reflection represented by signed axis permutations, component/interface renaming, and uniform scale must preserve normalized signatures.
- Branch addition, connectivity reroute, primitive family change, and interface topology change must alter the relevant signatures.
- Census exactly `288` current proposals: three treatments, three seeds, and thirty-two attempts per treatment/seed.
- Same config produces byte-identical result and census outputs across two clean roots.
- Unknown fields, missing identities, non-finite geometry, disconnected references, and source hash changes fail closed.
- Focused, repository-contract, compilation, and full regression tests pass.

## Risks and explicit non-goals

Canonical graph labeling can accidentally depend on names or become ambiguous for symmetric nodes. Geometry normalization can erase meaningful absolute-scale effects; therefore topology/shape diversity metrics remain separate from physical fitness and the raw scale is recorded independently. This work measures the existing opportunity set; it does not expand geometry, propose new topology, prove novelty, or claim physical validation.
