# Fixed-Topology End-to-End Whole-Vehicle Baseline

Thai companion: `FIXED_TOPOLOGY_END_TO_END_BASELINE.th.md`

## Result boundary

Work 049 proves deterministic orchestration for one fixed Work 047 candidate through the evidence classes currently implemented:

```text
3D declaration -> STEP -> FreeCAD mass properties
-> frozen Work 048 load cases -> bounded failure coupling
-> deterministic Level 0 distance/time/energy fixture
```

It does not prove that the candidate is physically strong, aerodynamically valid, safe, manufacturable, optimized, or competitive. The structural stage remains rigid-component cut-load algebra with declared synthetic capacities.

## Frozen experiment

The reference candidate and Work 048 training/holdout identities are immutable. The Level 0 fixture uses `1000 m`, reference speed `25 m/s`, initial energy `150000 J`, propulsion demand `100 J/m`, and auxiliary power `200 W`. This is a synthetic orchestration fixture, not a circuit or lap-time model.

The reference is evaluated at timesteps `1.0/0.5/0.25 s` and bounded capacity factors `0.995/1.000/1.002`. Exact finish-event localization makes the timestep comparison deterministic. Capacity factors audit sensitivity only; they are not finite-element meshes.

## Reference and falsification controls

| Variant | Outcome | Time | Energy used | Maximum utilization | Meaning |
|---|---:|---:|---:|---:|---|
| reference | `finished` | `40.0 s` | `108000 J` | `0.715678478993928` | fixed reviewed baseline |
| weak control | `DNF` | n/a | n/a | greater than `1` | structural capacity deliberately halved |
| disconnected control | `DNF` | n/a | n/a | unchanged demand | explicit load-path removal |
| heavy feasible control | `finished` | `43.81780460041329 s` | `128763.56092008266 J` | `0.8588141747927136` | `1.2` mass scale, topology unchanged |

The heavy control shows that this evaluator does not require the lowest mass to be feasible: it finishes while paying explicit time, energy, and structural-demand penalties.

## Refinement and replay

- finish-time maximum relative change: `0`
- bounded structural-utilization maximum relative change: `0.007035175879396918`
- allowed structural change: `0.01`
- reference result SHA-256: `12774be503f21212cd35cc10b48f1eb60ab5740005ab264dfa17b35f87eb1097`
- nine-cell reference matrix SHA-256: `237b2454eb0d4d83c750177ce96964d3fdadbcf52e456687f47e2c43f28fb71c`
- negative controls rejected: `4`

All seven frozen training/holdout load cases appear in every reference record. Same-input evaluation is exact. Missing evidence, changed STEP identity, incomplete nominal case set, and an unregistered timestep fail closed.

## Falsification record

The first acceptance runner attempted to make an incomplete-case control by dropping the last Work 048 record. That record was the separate overload control, so the nominal set remained complete and the negative control was correctly admitted. The fixture was corrected to remove a named training case; no evaluator, threshold, or result formula changed.

Supporting evidence is strong for orchestration and bookkeeping. Contradicting evidence is decisive for readiness: the so-called structural-resolution matrix changes declared capacity factors and provides no independent stress field, deformation field, mesh convergence, or alternate solver. Work 050 may run the bounded pilot to test fairness mechanics, but its readiness review must carry this unresolved blocker.

## Reproduction

```powershell
.\scripts\run_work049.ps1
py -3.14 -m unittest tests.test_whole_vehicle_baseline -v
```
