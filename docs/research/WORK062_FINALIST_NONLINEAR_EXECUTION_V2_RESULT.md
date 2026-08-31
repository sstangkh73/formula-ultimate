# Work 062 Finalist Nonlinear Execution v2 Result

Thai companion: `WORK062_FINALIST_NONLINEAR_EXECUTION_V2_RESULT.th.md`

## Decision

Execution protocol `work062_finalist_nonlinear_execution_v2`, campaign `FU-NLG-002`, completed with `51/51` candidate passes and `102/102` case passes. The append-only ledger replayed exactly before result documentation. All 306 CalculiX processes exited zero and contained the required geometric-nonlinearity confirmation.

This means the frozen Work 062 finalists showed negligible geometric-nonlinearity amplification under the two frozen Work 048 holdout loads in the Work 063 linear-elastic B31 beam model. It does not establish absence of buckling, physical strength, safety, or real-material validity.

## Controlled experiment

- Independent variable: exact finalist geometry for all and only 51 Work 062 refinement/STEP/FreeCAD survivors.
- Paired cases per candidate: `aero_extreme` and `holdout_combined`.
- Controls: Work 062 stage fingerprint, 16 subdivisions per branch, identical candidate-derived loads/boundaries, `E = 70 GPa`, Poisson ratio `0.3`, nominal synthetic yield stress `250 MPa`, CalculiX SHA-256, and frozen Work 063 thresholds.
- Falsification thresholds: displacement amplification `> 1.10`, stress amplification `> 1.15`, yield margin `< 1.10`, solver/process/evidence failure, or incomplete replay.
- Failure policy: no retry, no silent repair, and no Work 064 result reuse.

## Results

| Metric | Minimum | Maximum |
| --- | ---: | ---: |
| Nonlinear/linear displacement amplification | 1.0000041846576189 | 1.0000299794481688 |
| Nonlinear/linear surface-stress amplification | 1.0000069976482437 | 1.0000338606574917 |
| Nonlinear yield margin | 358.6735825412834 | 1068.5258384564943 |

The largest displacement and stress amplification occurred for `candidate-647b5e46141aebdf` in `aero_extreme`. The minimum yield margin occurred for `candidate-0b48ef541807e8ef` in `holdout_combined`. No preregistered threshold was approached, no failure code was emitted, and no nonlinear process failed.

The correct interpretation is that geometric effects were very small for this load/model domain. An alternative explanation is that the frozen loads and coarse beam abstraction are insufficiently severe or expressive to expose instability. The high nominal yield margins also reflect synthetic material and idealized section/load transfer rather than calibrated allowables.

## Replay and provenance

- Execution source commit: `729edcbfa7574a5bfa2d3aa972fb15acec7e4295`.
- Gate configuration SHA-256: `2dff176188c2fcbf1ec73b1727e3637c3de6062e10aa1fc372a7306cfee8d1b9`.
- Execution protocol SHA-256: `7b04d0af6363d4520bcca0d52c1ab956a1ba13965f6361348493ebe4ef018a26`.
- Candidate-set SHA-256: `3c383e41d5c2685fae2a2a60a157ee0284fd541d4f91719232714b71cd6ad442`.
- Ledger fingerprint SHA-256: `ffbc7eef129b5c51cb114bfa6ec849fae15617f32bbc0c022aa05e1f50825e27`.
- Summary SHA-256: `4d28434bd2a050045fdd8579bd4ce5e75ab11c827af3e0744da2d321dfd6227f`.
- CalculiX SHA-256: `2ff89a72b6aac9c361cb716e44220dfcd01d2bb3e66abd6b6455b01b7250f350`.
- Recorded external-process wall time: `92.728518 s` across 306 processes.

Work 064 remains preserved as stopped evidence because its JSON replay comparison failed. Work 065 used a fresh ledger and reran all solver processes after strict-JSON normalization was committed; no Work 064 observation entered this result.

## Remaining evidence gap

Confidence is high for exact execution/replay and the small geometric-nonlinearity response inside this bounded B31 domain, but low for real-vehicle transfer. Remaining structural work includes initial imperfections and eigen/post-buckling analysis, solid elements and joints, contact, nonlinear calibrated materials, fracture, fatigue spectra, subsystem failure propagation, tolerances, and hardware correlation. Independent search replication also remains required before any algorithm-superiority claim.
