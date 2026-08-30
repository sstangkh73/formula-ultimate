# Work 044 Result: Fatigue Damage and Life Acceptance

Status: Completed

Thai companion: `2026-08-30_044_fatigue-damage-life-acceptance-result.th.md`

## Outcome

The synthetic fatigue accounting route passed. Rainflow cycle count, constant/variable amplitude damage, Goodman correction, first crossing, uncertainty, exact replay, and all invalid-domain controls are observable. No fatigue value is admitted as real design data.

## Files changed

- `config/structural/fatigue_damage_acceptance_v1.json`
- `src/formula_ultimate/structural/fatigue.py` and structural exports
- `scripts/structural/run_fatigue_damage_acceptance.py`
- `scripts/run_work044.ps1`
- `tests/test_fatigue_damage.py`
- `docs/physics/FATIGUE_DAMAGE_ACCEPTANCE.md` and `.th.md`
- matching Work 044 plan/result pairs

Ignored evidence is under `artifacts/work044/`.

## Decisions and results

- Implemented a deterministic stack rainflow version and retained endpoint half-cycle accounting.
- Processed independent blocks separately so concatenation cannot invent transition cycles.
- Used decimal damage accumulation and serialized every increment/cumulative value; damage remains `1.2` after crossing rather than clipping.
- Constant history counted `1200` cycles exactly and crossed at `1000`.
- High→low and low→high both ended at `D=1.074176`, while first crossing differed at `1073.632813` and `1270.190329` cycles.
- Six unsupported/malformed inputs failed closed.

## Validation

```powershell
py -3.14 -m unittest tests.test_fatigue_damage -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work044.ps1
# exit 0; status=passed; negative_controls=6

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 307 tests in 19.738s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

## Limitations and follow-up

Miner/S-N arithmetic is not crack growth or physical service life. The record omits sourced curve scatter, notch/surface/process/environment factors, plastic hysteresis, residual-stress evolution, multiaxiality, and load interaction. Work 046 may later consume the typed crossing event only after Work 045; it must retain these evidence limitations.
