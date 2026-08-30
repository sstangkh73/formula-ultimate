# Work 051 Result: Gate A Element and Boundary Remediation

Status: Completed

Thai companion: `2026-08-30_051_gate-a-remediation-result.th.md`

## Outcome

Gate A is `narrowly_bounded`, not globally closed. C3D10 refinement is supported and equivalent two-support encodings replay identically. C3D4 near-critical promotion remains excluded, and the one-support Work 045 result remains an out-of-domain topology mutation. Work 046 may start only as the bounded policy experiment defined in the physics report.

## Files changed

- `config/structural/gate_a_remediation_v1.json`
- `src/formula_ultimate/structural/gate_a_remediation.py` and structural exports
- `scripts/structural/run_gate_a_remediation.py`
- `scripts/run_work051.ps1`
- `tests/test_gate_a_remediation.py`
- `docs/physics/GATE_A_ELEMENT_BOUNDARY_REMEDIATION.md` and `.th.md`
- matching Work 051 bilingual plan/result records

Ignored solver evidence is under `artifacts/work051/`.

## Decisions and evidence

- C3D10 `1.8/1.4/1.2 mm` meshes contained `29,770/57,426/89,833` nodes.
- Maximum last-two amplification change was `0.01702%`; maximum secant error was `0.5391%`; maximum eigenvalue error was `0.0417%`.
- Reversing the two-support list preserved the same topology signature and STEP SHA-256 with zero compliance and resultant change.
- Removing one support remained a topology mutation. Its symmetric compliance change was `119.843%`; Work 045's retained reference-denominator value remains `299.021%`.
- The first focused unit run exposed an invalid `strict=True` use on intentionally offset refinement pairs. It failed before solver execution, was corrected without changing the preregistered meshes or thresholds, and the repeated focused test passed.
- The admitted experiment took `1009.88 s` for element remediation, `6.43 s` for the reference boundary replay, and `7.97 s` for the equivalent-encoding replay. Observed live working set reached approximately `1.17 GiB`, but this observation is not a calibrated peak-RSS measurement.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_gate_a_remediation tests.test_repository_contract -q
# exit 0; Ran 10 tests; OK

.\scripts\run_work051.ps1
# exit 0; status=passed; element_status=supported
# boundary_status=narrowly_bounded; gate_a_decision=narrowly_bounded
# work046_may_start_bounded_policy_experiment=true

py -3.14 -m unittest tests.test_element_verification tests.test_loaded_interface tests.test_gate_a_remediation -q
# exit 0; Ran 11 tests; OK

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 314 tests in 19.712s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0
```

Repository-contract checks, staged `git diff --cached --check`, the explicit scoped commit, and clean-tree Work 051 replay are verified after this result exists and are reported in the final handoff.

## Limitations and follow-up

This is numerical-domain remediation, not hardware validation. It has no post-critical continuation, independent solver, contact, preload, friction, fastener flexibility, physical calibration, or real material record. Work 046 must enforce the exact admitted identities and fail closed outside them; it may validate deterministic failure-state coupling but may not claim real fracture dynamics, crash safety, or arbitrary-joint transferability.
