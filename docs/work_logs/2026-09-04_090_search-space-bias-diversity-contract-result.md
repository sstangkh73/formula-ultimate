# Work 090 Result: Search-Space Bias and Diversity Contract

Thai companion: `2026-09-04_090_search-space-bias-diversity-contract-result.th.md`

## Status and outcome

Status: Completed

The deterministic diversity contract and current-search census are complete. The exact Work 050 opportunity ledger produced `288` descriptor-valid proposals, but only `1` topology signature and `1` functional-path signature. It produced `264` normalized geometry signatures because scale parameters vary, yet every candidate remains primitive-only. This directly measures the distinction between parametric variation and topology diversity.

The mean primitive fraction is `1.0`; mean curved-surface-area fraction is `0.0598413769094221`; primitive-type entropy is `0.8112781244591328 bits`; and normalized phenotype duplication is `8.333333333333337%`. The bounded Work 050 evaluator recorded `207` non-failures and `81` structural failures, but those categories are not general physical failure-mode coverage.

## Files changed

- `config/experiments/design_diversity_v1.json`
- `src/formula_ultimate/experiments/design_diversity.py`
- `scripts/experiments/run_design_diversity_baseline.py`
- `tests/test_design_diversity.py`
- `docs/contracts/DESIGN_DIVERSITY_V1.md` and Thai companion
- this result and its Thai companion
- the Work 090 plan and Thai companion, changed to `Completed`

Generated census/replay evidence under `artifacts/work090/` is ignored and was not committed.

## Exact evidence

- Config identity: `fef23e7250a1a451f775f96bd799872b4967ba2f448f484438bb89d11d6cc2ff`.
- Census identity: `8b2f1e52fdc72c6743aea5cf472eb6c29ddde01220a97f9d352b9fb6941bc69c`.
- Result identity: `5729ed2b3282e3634e601ac91a983f58f2c3dcbc205fa8203379a3f3dad170e9`.
- Byte-identical result file SHA-256: `5f38578d9d4b8cbbcc90ac02ce4f40f37e8f4e1fa0ef2e25f1621135465b2604`.
- Byte-identical census file SHA-256: `57138cbae2df84f6fa007818fb8ecd9bf44f8ccc330794352bfcca69d99b24da`.
- `288/288` candidates described; `264` unique normalized geometry signatures; `1` unique topology signature; `1` unique functional-path signature.
- All invariance and change-detection controls passed.

## Exact validation commands and results

```powershell
python -m unittest tests.test_design_diversity tests.test_repository_contract -v
# exit 0; Ran 16 tests; OK

python -m compileall -q src scripts tests
# exit 0

python scripts/experiments/run_design_diversity_baseline.py `
  --config config/experiments/design_diversity_v1.json `
  --output-root artifacts/work090/run_a
# exit 0; attempted_candidates=288; unique_topology_signatures=1

python scripts/experiments/run_design_diversity_baseline.py `
  --config config/experiments/design_diversity_v1.json `
  --output-root artifacts/work090/run_b `
  --replay-reference artifacts/work090/run_a/result.json
# exit 0; result and census byte-identical to run_a

python -m unittest discover -s tests -q
# exit 0; Ran 630 tests in 418.326s; OK (skipped=3)

git diff --check
# exit 0
```

## Evidence review and limitations

Supporting evidence is the exact source locking, complete equal-budget proposal ledger, invariant controls, topology-change controls, and exact replay. Contradicting evidence against current design freedom is decisive: geometry dimensions vary while topology and functional paths do not. A high unique-geometry ratio therefore cannot be interpreted as architectural diversity. V1's bounded Weisfeiler-Lehman-style signature may have rare non-isomorphic collisions and the radial geometry descriptor intentionally loses chirality; Work 091 and later must extend the descriptor as new representations become executable.

This result establishes a measurement baseline only. It does not create a new profile, topology, physical evaluator, or discovery.
