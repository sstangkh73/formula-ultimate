# Work 080 Result: Mechanical Assembly and Joint Kernel

Thai companion: `2026-09-02_080_mechanical-assembly-joint-kernel-result.th.md`

## Status and outcome

Status: Completed

The reference assembly passed a calculated 19-row, rank-19 rigid-body constraint system with zero redundant rows and 5 realized DOFs. Four ground-connected components exercise fixed, revolute, prismatic, and spherical joints. Their exact Work 078 STEP SHA-256 identities are part of the canonical assembly declaration. The full declared proxy motion has zero collisions and a minimum conservative envelope gap of `0.13999999999999999 m`.

This result supports deterministic declaration validation, calculated DOFs, mate residual checks, and continuous conservative proxy-envelope clearance only. It does not establish physical validation, exact B-rep collision clearance, moving-parent multibody envelope correctness, bearing life, joint strength, wear, friction, fatigue, or safety.

## Files changed

- `config/assembly/mechanical_assembly_joint_kernel_v1.json`
- `src/formula_ultimate/assembly/__init__.py`
- `src/formula_ultimate/assembly/joint_kernel.py`
- `scripts/assembly/run_joint_kernel_acceptance.py`
- `tests/test_joint_kernel.py`
- `docs/contracts/MECHANICAL_ASSEMBLY_JOINT_KERNEL_V1.md` and Thai companion
- this result and its Thai companion
- the Work 080 plan and Thai companion, whose statuses changed to `Completed`

Ignored runtime evidence was written under `artifacts/work080/` and was not committed.

## Decisions and evidence

- Constraint rank is calculated by deterministic Gaussian elimination at the declared absolute tolerance; expected rank/DOF values are post-calculation assertions.
- Frames must be finite, right-handed, orthonormal, and already aligned. No hidden snapping, healing, clipping, or repair occurs.
- Interface types are checked against bounded joint compatibility sets.
- Prismatic collision proxies use continuous segment sweeps. Revolute/spherical proxies use conservative swept spheres about joint centres.
- Mapping-key order leaves declaration and result identities unchanged; mutating an exact component geometry hash changes both identities.
- Negative controls rejected axis/origin mismatch, redundant constraints, false declared/expected DOFs, non-integer expected DOF, excessive clearance, invalid limits, continuous motion collision, missing/duplicate/incompatible interfaces, non-finite values, and left-handed frames.

Supporting evidence: the admitted reference calculated `constraint_rank=19`, `realized_dof_count=5`, `constraint_redundancy_count=0`, `collision_count=0`, and `minimum_motion_envelope_gap_m=0.13999999999999999`. Contradicting evidence: none among the admitted controls. Alternative explanation addressed: acceptance cannot be caused by copying declared DOFs because wrong declared and expected values fail independently. Missing evidence: independent B-rep measurement and exact geometry collision remain Work 081 scope.

## Exact validation commands and results

```powershell
python -m unittest tests.test_joint_kernel -v
# exit 0; Ran 10 tests; OK

python scripts/assembly/run_joint_kernel_acceptance.py `
  --output artifacts/work080/acceptance.json
# exit 0; declaration_sha256=81100a8a98b47b404ff925015886e81e1ab3229b264144fa814b4f611509c778
# result_sha256=2db26f683c4cf552c120a6e7878a69be61e2a07ccab8506fde882fec483ff9a1

python -m unittest tests.test_repository_contract -v
# exit 0; Ran 6 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -v
# exit 0; Ran 514 tests in 300.407s; OK (skipped=3 pinned CadQuery-environment tests)

python scripts/assembly/run_joint_kernel_acceptance.py `
  --output artifacts/work080/replay_a.json > $null
python scripts/assembly/run_joint_kernel_acceptance.py `
  --output artifacts/work080/replay_b.json > $null
Get-FileHash artifacts/work080/replay_a.json -Algorithm SHA256
Get-FileHash artifacts/work080/replay_b.json -Algorithm SHA256
# exit 0; both exact output files:
# ae5abe0025210071c91923446f2feb8635f5885ee292c52ecb135c4c9ffd7c6b
```

## Limitations and follow-up

V1 collision bounds use declared component-local spheres. The admitted fixture has one ground joint per component; moving-parent kinematic chains are not validated by this envelope implementation. Work 081 must independently import the exact STEP bytes with FreeCAD, verify topology and hash, measure SI geometry/mass properties without healing, and recover interface witnesses from geometry signatures rather than face indices.
