# Work 103 Result: Correct Benchmark Equations and Balance Evidence

Thai companion: `2026-09-05_103_correct-benchmark-equations-result.th.md`

Status: Completed

## Outcome and files

Corrected `src/formula_ultimate/structural/generalized_geometry_benchmarks.py`, versioned outputs in `scripts/structural/run_generalized_geometry_benchmarks.py`, extended `tests/test_generalized_geometry_benchmarks.py`, and updated both `docs/contracts/GENERALIZED_GEOMETRY_BENCHMARKS_V1.md` and `.th.md`. This work also adds the four bilingual Work 103 plan/result records. Only these nine files belong to the commit.

New retained outputs: `artifacts/work103/run_a/result.json` and `artifacts/work103/run_b/result.json`, excluded from Git. Historical Work 097 outputs and all input config/load/threshold/source identities are unchanged.

## Equations and evidence decisions

- Compute K from geometry/material/discrete compliance before response evaluation. Test q = K*u^p instead of inferring K from q/u.
- For quasistatic Hertz loading, integrate F = K*delta^(3/2): U = (2/5)*K*delta^(5/2), not (1/2)*F*delta. Use one E* = E/[2(1-nu^2)] and effective-radius proxy in both indentation and contact pressure.
- Preserve a supplied positive contact radius even when thickness is larger; use thickness only when radius is absent. Invalid radius is rejected.
- Pressure-displacement work is J/m^2; force-displacement work is J.
- Replace constructed field force/moment/energy residuals with null plus `full_balance_validated=false`. Named scalar equation/energy residuals are useful consistency checks but are not independent field balance.
- Derive convergence from actual scalar residuals. Record Newton history and actual effort; exhausted budget returns invalid without fallback.
- Recompute scalar evidence/reference error during adjudication, check doubling order, and reject forged/legacy field zeros or missing scope.
- Mark output `evaluator_version=generalized_geometry_equations_v2`; input schema remains V1. Old and new results cannot be treated as identical replay.

The Hertz normal-contact relationships were checked against [CompuTiX theory](https://computix.gitlabpages.inria.fr/computix/db/d6e/group__Hertz.html). The energy coefficient is obtained by direct integration of that force law. Equal elastic materials, effective-radius proxy and quasistatic loading remain explicit assumptions.

## Tests and measured outputs

Exact commands from `C:\Formula Ultimate`, each checked separately for exit status:

```powershell
python -m unittest tests.test_generalized_geometry_benchmarks -v
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work103/run_a/result.json
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work103/run_b/result.json --replay-reference artifacts/work103/run_a/result.json
python -m unittest discover -s tests -q
python -m unittest tests.test_repository_contract -q
git diff --check
git diff --cached --check
```

- Focused tests: exit 0, 17 tests in 0.319 s, OK (8 new test methods). A nonzero-Poisson/equal-effective-modulus assertion was added while the full suite was running and covered by this final focused run; production code did not change during the full run.
- Full suite: exit 0, `Ran 697 tests in 427.395s`, `OK (skipped=7)`.
- Repository contracts and whitespace checks: final passing state verified before commit.
- Runner and exact replay: exit 0, seven cases passed, unchanged configuration. Result SHA-256: `1b38f6468cd94f8c604120aa8af8f8c7a5c14842420c894926a22bc45bed466d`.
- Retained contact case: pressure changes from 211763869.07630363 Pa to 144061379.89067543 Pa; yield-screen ratio changes from 0.8792554763052145 to 0.6084455195627017. No load/threshold was tuned.
- Hertz indentation = 1.6584132504364747e-06 m; stored energy = 1.6584132504364745e-05 J; 5 Newton iterations. Relative residual history: [0.6464466094067258, 0.16862910096068973, 0.004122917441717817, 2.8227306565042907e-06, 1.3281464816827792e-12, 0.0].
- Maximum scalar equilibrium residual across all levels = 1.4551915228366853e-16. Field balance is still uncomputed; this small scalar value is not a physical-validation claim.

Independent regression evidence includes a 400 N/m linear spring, direct numerical integration and dU/ddelta = F, a Hertz case with known 1 N load / 1e-4 m indentation / 4e-5 J energy / 4774.64829275686 Pa peak pressure, load/modulus scaling, equal E* under different E/nu, pressure units, perturbed responses, natural Newton exhaustion and invalid domains.

## Review discipline and limitations

Independent variables: corrected implementation, iteration/refinement level and test perturbations. Controls: frozen config/material/witness/load/threshold identities. Metrics: displacement, energy, contact pressure, residuals, convergence, failure screens and exact replay. Success criteria passed: known-law checks, perturbation rejection, seven scoped cases and replay. Supporting evidence is the independent numeric/integral/scaling checks; counterevidence to broader validation is the continued absence of independent field reactions. Alternative explanation for tiny residuals is exact satisfaction of a reduced constitutive law, explicitly recorded rather than interpreted as real-world accuracy.

High confidence in the corrected scalar Hertz relationships and regression behavior; no physical validation of the synthetic material, radius proxy, frictional contact, general STEP geometry or whole vehicle. Other failure screens remain bounded proxies. Future work must add independent mesh/field reactions and assess each physical model's applicability.

An initial patch-context mismatch changed no files and was reapplied against exact source. The initial exploratory searches included two nonexistent wildcard/directory targets; corrected direct paths were used afterward. These were editing/discovery issues, not failed validation gates. The original 9-test suite passed before the 8 new regression methods were added.

After final gates, stage only the nine declared files, inspect staged scope, commit, and verify the new commit and clean status. The short hash is reported in the final handoff; no push or history rewrite.
