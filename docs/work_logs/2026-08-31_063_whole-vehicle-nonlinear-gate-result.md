# Work 063 Result: Whole-Vehicle Geometric-Nonlinearity Gate

Status: Completed

Thai companion: `2026-08-31_063_whole-vehicle-nonlinear-gate-result.th.md`

## Outcome

Implemented and froze `whole_vehicle_geometric_nonlinearity_gate_v1`. The B31 deck builder now supports explicit CalculiX `NLGEOM` execution without changing default linear behavior. The new adjudicator records process/confirmation failures, invalid numeric evidence, displacement/stress amplification, yield margin, terminal status, and canonical result hashes. Candidate aggregation requires the exact preregistered two-case set and rejects duplicates, missing cases, tampering, and identity mismatches.

## Files changed

- `config/structural/whole_vehicle_nonlinear_gate_v1.json`
- `src/formula_ultimate/structural/vehicle_frame_refinement.py`
- `src/formula_ultimate/structural/vehicle_nonlinear_gate.py`
- `src/formula_ultimate/structural/__init__.py`
- `tests/test_vehicle_nonlinear_gate.py`
- English/Thai research, plan, and result documents for Work 063.

## Validation

- `py -3.14 -m unittest tests.test_vehicle_nonlinear_gate tests.test_vehicle_frame_refinement -q` → exit `0`; `Ran 10 tests`, `OK`.
- Live CalculiX smoke through the generated nonlinear B31 deck → exit `0`; solver confirmation present; maximum displacement `0.03504475926921773 m`; parsed maximum integration-point von Mises stress `37,828,269.82752862 Pa`; parsed section-force rows `50`.
- `py -3.14 -m unittest discover -s tests -q` → exit `0`; `Ran 377 tests in 33.012s`, `OK`.
- `py -3.14 -m compileall -q src scripts tests` → exit `0`.

## Identities and decisions

- Frozen configuration SHA-256: `2dff176188c2fcbf1ec73b1727e3637c3de6062e10aa1fc372a7306cfee8d1b9`.
- Gate-module SHA-256 before documentation commit: `72670a6e61b93d140989437adbbb875a0d9796c5d205517df402596a0ab3e247`.
- Thresholds: displacement amplification `<= 1.10`, stress amplification `<= 1.15`, yield margin `>= 1.10`.
- Candidate outcomes were deliberately not run with uncommitted code. The committed adapter will be applied in a new work item.

## Limitations and follow-up

This gate covers geometric-nonlinearity sensitivity in a linear-elastic B31 beam network. It does not cover initial imperfections, eigenvalue/post-buckling behavior, solids, contact, plasticity, fracture, fatigue, calibrated material data, manufacturing tolerances, or hardware. The next work item must execute all and only the 51 Work 062 CAD-passed finalists from a clean committed tree, preserve terminal failure evidence, and verify exact replay before independent replication begins.
