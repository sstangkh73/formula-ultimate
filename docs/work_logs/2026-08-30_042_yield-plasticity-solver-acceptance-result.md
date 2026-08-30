# Work 042 Result: Yield and Plasticity Solver Acceptance

Status: Completed

Thai companion: `2026-08-30_042_yield-plasticity-solver-acceptance-result.th.md`

## Outcome

The synthetic bilinear CalculiX acceptance passed. Solver evidence contains yield transition, nonzero `PEEQ`, residual strain, unloading/reversal, reaction closure, `ELSE` internal energy, two-mesh agreement, hashes, and replay metadata. This is implementation evidence only and is prohibited from serving as a real design material record.

## Files changed

- `config/structural/yield_plasticity_acceptance_v1.json`
- `src/formula_ultimate/structural/plasticity.py` and structural exports
- `scripts/structural/run_yield_plasticity_acceptance.py`
- `scripts/run_work042.ps1`
- `tests/test_plasticity_acceptance.py`
- `docs/physics/YIELD_PLASTICITY_ACCEPTANCE.md` and `.th.md`
- matching Work 042 plan/result pairs

Ignored solver evidence is under `artifacts/work042/`.

## Decisions and deviations

- Used deterministic structured C3D8 meshes so the fixture isolates constitutive behavior from tetrahedral geometry error.
- Converted total tangent `Et` to `*PLASTIC` hardening slope `H=E Et/(E-Et)`.
- Integrated actual solver force-displacement endpoints and compared them with solver `ELSE`; no analytical energy was substituted for solver evidence.
- The first exploratory solve was not admitted. It exposed default every-increment print output and the exact `internal energy (element, energy)` heading. `FREQUENCY=999` and the observed parser contract were then frozen before the admitted rerun.

## Validation

```powershell
py -3.14 -m unittest tests.test_plasticity_acceptance -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work042.ps1
# exit 0; status=passed

py -3.14 -m unittest discover -s tests -v
# exit 0; Ran 299 tests in 19.432s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

The fine-mesh yield/tangent/plastic/residual relative errors were `1.0145e-9`, `5.0000e-8`, `2.1739e-7`, and `2.1739e-7`. Maximum reaction and energy residuals were `1.0840e-16` and `2.7508e-7`. All three response convergence metrics were zero.

## Limitations and follow-up

The fixture has no sourced real material, geometric concentration, temperature/rate dependence, cyclic hardening, fracture, or fatigue. Work 043 may consume the typed provenance requirement and analytical material-state boundary, but it must not reinterpret this synthetic law as toughness evidence.
