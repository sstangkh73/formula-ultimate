# Work 043 Result: Fracture-Initiation Evidence

Status: Completed

Thai companion: `2026-08-30_043_fracture-initiation-evidence-result.th.md`

## Outcome

The ideal LEFM evaluator passed all declared arithmetic, representation, ledger, identity, and invalid-domain gates for three crack lengths. The result deliberately does not claim solver crack-tip fields or propagation.

## Files changed

- `config/structural/fracture_initiation_acceptance_v1.json`
- `src/formula_ultimate/structural/fracture.py` and structural exports
- `scripts/structural/run_fracture_initiation_acceptance.py`
- `scripts/run_work043.ps1`
- `tests/test_fracture_initiation.py`
- `docs/physics/FRACTURE_INITIATION_ACCEPTANCE.md` and `.th.md`
- matching Work 043 plan/result pairs

Ignored evidence is under `artifacts/work043/`.

## Decisions and results

- Selected the roadmap's independently verified evaluator route because no admitted CalculiX contour-integral parser exists.
- Used `K_I=sigma sqrt(pi a)` only inside a narrow `Y=1` infinite-plate domain.
- Required finite-width, plane-strain thickness, small-scale-yielding, and yield-before-fracture screens.
- Preserved exact crack-tip tags across `8/16/32` segment representations; no singular peak stress is consumed.
- Three initiation loads localized with zero relative error; last-two `K_I`, reaction, and work-ledger residuals were zero.
- Six invalid controls failed closed with exact classified reasons.

## Validation

```powershell
py -3.14 -m unittest tests.test_fracture_initiation -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work043.ps1
# exit 0; status=passed; case_count=3; negative_controls=6

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 303 tests in 19.264s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

## Limitations and follow-up

The gross elastic work ledger is not crack energy. There is no solver field, J integral, propagation, path, dissipated fracture energy, uncertainty distribution, or physical toughness record. Work 044 fatigue remains a distinct Miner/S-N evidence mechanism and must not be presented as crack-growth validation.
