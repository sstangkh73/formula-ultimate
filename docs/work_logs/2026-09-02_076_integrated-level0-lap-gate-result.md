# Work 076 Result: Integrated Level-0 Closed-Loop Lap Gate

Status: Completed

Thai companion: `2026-09-02_076_integrated-level0-lap-gate-result.th.md`

## Outcome and files

Implemented an integrated spatial lap gate combining Work 074 steering, Work 075 linkage geometry, Work 073 vertical dynamics, and the existing drivetrain/planar plant. Added configuration, integration module/exports, runner, eight focused tests, bilingual research, and this result. Evidence is ignored under `artifacts/work076/`.

## Evidence

The synthetic `314.1592653589793 m` lap finished in localized time `22.14108931044568 s` after `4429` steps. Finish position/heading residuals were `0.047685317265362355 m` and `3.56130463712072e-05 rad`. Maximum cross-track error was `0.0714069338543296 m`, saturation count `0`, minimum load `156.44738786029893 N`, maximum travel `0.024331844801589377 m`, maximum relative energy residual `7.449174538254737e-08`, and progress-spatial residual `0.0007138905266217827 m`.

Mirror, replay, open-loop departure, narrow-corridor departure, contact loss, timeout, and short-segment refinement controls passed. Work 074/075 identities remained unchanged.

Result/canonical evidence/file SHA-256 values are `719b39293ecb818560acbd88cf1262da8b3407ffb3e5f150a0130860cf9e0dc3`, `bdbdf31f63dc4da79c12e159d05e1a0e3c870a7994c846b53e73aba9ac2a9df2`, and `F6E8C83A72510837C32B07F925132BAA594C531D1D9B4DBC4C5087C4AD6F80CB`.

## Validation record

```text
python -m unittest tests.test_integrated_lap_gate -q
Exit: 0
Ran 8 tests in 111.721s — OK

python scripts/experiments/run_integrated_lap_gate.py --config config/vehicle/integrated_level0_lap_gate_v1.json --vehicle-root config/vehicle --output artifacts/work076/experiment_evidence.json
Exit: 0; status=passed

same command with --output artifacts/work076/replay/experiment_evidence.json
Exit: 0; byte-identical SHA-256 F6E8C83A72510837C32B07F925132BAA594C531D1D9B4DBC4C5087C4AD6F80CB

python -m unittest discover -s tests -q
Exit: 0
Ran 479 tests in 319.119s — OK
```

Full regression, repository contract, compilation, scoped commit, and post-commit replay follow before final handoff.

## Limitations and follow-up

This is only an analytical-circle Level-0 lap. CAD-derived joints, nonlinear tyres, aerodynamics, braking/speed control, real 3D corridor evidence, structural failure loads, and physical correlation remain missing. It must not be reported as a real race-capable car.
