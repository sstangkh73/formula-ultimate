# Work 078 Plan: Parametric B-rep Feature Grammar V1

Status: Completed

Thai companion: `2026-09-02_078_parametric-brep-feature-grammar-plan.th.md`

## Objective and scope

Implement a bounded, SI-unit parametric B-rep feature grammar that an agent can use to construct and replay real single-part solids. V1 covers sketch profiles, extrude, revolve, pocket/cut, through hole, stepped bore, shaft shoulder, rib/web, shell/wall thickness, linear/circular pattern, bounded fillet/chamfer, and boolean union/subtract/intersect.

The admitted corpus contains a shaft, bracket, hollow housing, ribbed plate, and hub-like rotating part. This work validates only the exact grammar, CadQuery/OCCT execution route, valid-solid final state, and deterministic STEP identity. It does not establish material adequacy, manufacturability, structural capacity, assembly behavior, or physical validation.

## Experiment design

- Independent variables: feature operator/order, bounded SI dimensions, parent-feature references, profile type, pattern count/spacing/angle, wall/fillet/chamfer size, and boolean operation.
- Dependent variables: parse admission/rejection, feature execution status, final solid count/validity/volume/bounds, STEP SHA-256, and replay identity.
- Controls: five canonical part families; config/order replay; zero thickness, out-of-bound parameter, unknown operator/field/unit, forward/unknown parent, self-erasing subtract, empty intersection, shell failure, and final multi-solid controls.
- Preferred hypothesis: all five canonical families execute into one valid positive-volume solid and replay to byte-identical canonical STEP hashes under the pinned CadQuery toolchain; invalid declarations or kernel results fail closed.
- Falsification: operator skipped, implicit unit conversion, invalid/intermediate kernel state accepted, empty or multi-solid final admitted, hidden geometry repair, timestamp/path hash drift, or a replay mismatch.

## Planned files

- `config/cad/brep_feature_grammar_v1.json`
- `src/formula_ultimate/components/brep_grammar.py` and component exports
- `scripts/cad/generate_brep_feature_corpus.py`
- `tests/test_brep_grammar.py`
- `docs/contracts/PARAMETRIC_BREP_FEATURE_GRAMMAR_V1.md` and Thai companion
- this plan and matching bilingual result record
- ignored evidence under `artifacts/work078/`

## Validation and success criteria

Every listed operator must be executed by at least one admitted corpus feature. Each of the five required families must produce exactly one valid solid with finite positive volume and a canonical STEP artifact. Two independent output roots must produce identical per-candidate STEP SHA-256 and identical canonical manifest identity under the pinned toolchain. Negative controls must reject zero thickness, unknown field/unit/operator, invalid ancestry/bounds, empty boolean results, and invalid final solid state. Focused parser/kernel tests, full regression, compilation, bilingual contract, scoped staging, `git diff --cached --check`, one commit, and post-commit replay must pass.

## Risks and explicit non-goals

OCCT booleans, shelling, and edge treatment can fail on legal-looking parameter combinations; that failure must remain observable rather than repaired. Stable STEP bytes are toolchain-specific and do not imply stable face numbering. The bounded five-family corpus is not arbitrary topology, a manufacturing process model, FEA evidence, or proof of complete part-design capability.
