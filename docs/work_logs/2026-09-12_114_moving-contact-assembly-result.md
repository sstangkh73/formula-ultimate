# Work 114 Result: Moving Contact Assembly

Thai companion: `2026-09-12_114_moving-contact-assembly-result.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 114 implemented a deterministic axial moving-member/contact simulation and prescribed tangential stick/slip probe using the exact Work 113 threaded-reference reduced properties. All three time steps produced `38` opening/closing/slip events and positive swept clearance. Reactions and impulse came from penetration histories, not assigned input values.

Result SHA-256 is `5926e067cbe4b07d0bf90364275649f72a7ad4b4566ff204901172fdd9f1ce5f`; replay is exact. For coarse/medium/fine steps, maximum displacement was `7.087472714465673e-6`, `7.0943046957599814e-6`, `7.099179394127206e-6 m`; maximum force was `19216.63250943933`, `19203.781781291575`, `19196.837823792008 N`; minimum clearance was `4.291252728553433e-5`, `4.290569530424002e-5`, `4.2900820605872797e-5 m`; energy residual was `0.05055660301082888`, `0.02599497047954028`, `0.013144323898850088`.

Last-two changes were `0.000686656597417022` displacement, `0.0003615932308880738` force and `0.00017990058869692504` impulse. Free motion matched analytically; rigid/moving conflict and severed coupling were rejected; a reduced-clearance mutation was blocked locally as collision; opening/slip marked the reduced stick model out of range.

Changed: proposed implementation/config/runner/test files, bilingual `MOVING_CONTACT_ASSEMBLY_V1` contract and this bilingual plan/result. Ignored histories are under `artifacts/work114/run_a|run_b`.

## Validation and limitations

```powershell
python -m unittest tests.test_moving_contact_assembly -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/assembly/moving_contact_assembly.py scripts/development/run_moving_contact_assembly.py
# exit 0
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_a
# exit 0; result SHA-256 above
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_b --replay-reference artifacts/work114/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_detailed_connection_contact tests.test_moving_contact_assembly tests.test_repository_contract -v
# exit 0; 18 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly the 10 declared Work 114 files
git diff --cached --check
# exit 0
```

Tangential history is prescribed, damping is synthetic and no flexible modes, full 3D collision, crash, vehicle-readiness or physical-validation claim is made. The verified commit hash is reported in the final handoff.
