# Work 084 Result: Energy Conversion and Torque-Path Candidate 001

Thai companion: `2026-09-03_084_energy-torque-path-candidate-001-result.th.md`

## Status and outcome

Status: Partial

Every deliverable declared in the Work 084 plan exists and every declared validation passed. CadQuery `2.8.0` generated a seven-part energy-conversion and torque-path candidate, canonical per-part STEP files, and a seven-solid assembly STEP. FreeCAD `1.1.3` / OCCT `7.8.1` imported the exact files without a healing call, retained seven separate valid solids, and saved an inspectable FCStd document containing seven named objects.

The calculated assembly mobility is exactly `1 DOF` about `+y`, from a seven-joint constraint tree of `40` rows plus one separately declared loop-closing rolling coupling row. The calculated torque ratio is exactly `3.0`, taken from the same two frozen radii that generate the B-rep. Exact B-rep checks over all twenty-one part pairs found `0 m3` overlap, at least `0.001 m` clearance for every forbidden pair, and `0.005 m` clearance between the transformation body and the frozen Work 083 contact plane. Torque, reaction, energy, and thermal residuals are `0.0`, `1.42e-16`, `0.0`, and `9.00e-16`, inside the respective `1e-5`, `1e-5`, `1e-4`, and `1e-4` gates. All ten falsification controls produced their preregistered measurable consequence, and two clean runs reproduced every canonical identity exactly.

The status is `Partial` rather than `Completed` for the reason preregistered in the plan: **the Work 084 meshed structural completion gate is not met.** The candidate is also deliberately not design-admitted; its verdict is `not_admitted_synthetic_evidence` with `design_use_allowed=false`.

## Files changed

- `config/candidates/energy_torque_path_candidate_001.json`
- `src/formula_ultimate/subsystems/energy_torque_path.py`
- `scripts/candidates/build_energy_torque_path_candidate_001.py`
- `scripts/candidates/inspect_energy_torque_path_freecad.py`
- `tests/test_energy_torque_path_candidate_001.py`
- `docs/contracts/ENERGY_TORQUE_PATH_CANDIDATE_001.md` and Thai companion
- this result and its Thai companion
- the Work 084 plan and Thai companion, whose statuses changed to `Partial`

Generated CAD, FCStd, manifests, evaluations, and replay evidence under `artifacts/work084/` are ignored and were not committed.

## Decisions and measured evidence

- The candidate is one inspectable declaration rather than a topology built into the general evaluator. Its seven separate solids are `energy_store`, `converter_housing`, `converter_rotor`, `input_shaft`, `ratio_drum`, `output_shaft`, and `support_block`.
- Mechanism efficiency is **derived** from the declared `1.2 Nm` support drag torque rather than declared as a second free scalar. The reference derived value is `0.95`, and the overall drive efficiency is `0.855`.
- The onboard pre-race primary energy is geometry-derived: the CadQuery cavity volume `6.1056e-4 m3` times the declared medium density `800 kg/m3` gives a medium mass of `0.488448 kg`, and the declared specific energy `1.8e6 J/kg` gives `879206.4 J`.
- The drive segment draws `10666.666666666666 J` of primary energy, delivers `9120.0 J`, and rejects `1066.666666666666 J` of converter heat and `480.0 J` of mechanism heat. The braking segment takes `3600.0 J` from the declared `60000 J` conserved kinetic source, returns `2160.0 J` to the store, and rejects `1440.0 J`. Final store energy is `870699.7333333335 J`, below the initial `879206.4000000001 J`. External primary inflow is exactly `0 J`.
- The traction interface force is `800.0 N` computed identically from both radii. Statics place `384.6153846153847 N` on the support bore and `415.3846153846154 N` on the Work 083 axle interface, closing to the applied force.
- Thermal states are solved, not clipped. Drive-segment housing temperature is `323.188 K` with a `2.114 K` coolant rise; brake-segment housing temperature is `329.969 K` with a `2.622 K` coolant rise. Both are inside the declared `400 K` and `8 K` domains, and coolant velocity is `0.2105 m/s` against a `3.0 m/s` limit.
- Two surface quantities are cross-checked against the frozen build parameters at `1e-6` relative tolerance and passed: measured coolant passage area delta `0.00422230052642468 m2` against analytic `0.004222300526424682 m2`, and measured fin area delta `0.005920000000000002 m2` against analytic `0.00592 m2`.
- The measured `output_shaft` inboard interface is `y = 0.019 m`, radius `0.005799999999999997 m`, axis `(-0.04, -0.104) m`, matching the frozen Work 083 axle inside `1e-6 m`.
- Geometry-derived total synthetic mass is `1.5135706418525483 kg` from a single synthetic material identity `72a1b5527e4aede10c6de73523c54835f11458f80100c6383d2a304d4d912097`; part mass is rejected unless it equals CadQuery volume times that declared density.
- Maximum analytic structural utilization is `0.5823428918158171` at `output_shaft_combined`; the other cases are `0.142952` (`input_shaft_combined`), `0.056938` (`support_block_bearing`), and `0.003712` (`converter_housing_mount`).
- Identities: declaration `4fab24bff4faaeed0fa7f7c789ac06b2ecd51e9f3033ae2565a4c5ed017e49d3`, geometry manifest `c6902beac7bd4bf07928c5322387d8d3740ecceddf31fbfbd70bd43e5e9fc7a5`, assembly STEP `d3c20ceca370ac02ec9ec63da6ff8ce4d1728f0561a04f641519cbe467e13e30`, FreeCAD report `b83a54bab70712802a7eeb8f9de278e987ef1b75cb48ca62083d6ffba10276cc`, evaluation `d3ad0ca97f99e6f14d3112bfbb647e08a03736aed3670aebbe98aacb0e25b817`, result `c87fa43572efc0a8bc6ef67e375589943d73ecc4ca3b3a3d7a51df4ddb3edb66`.
- Runs `run_a` and `run_b` produced byte-identical `result.json` files with SHA-256 `af68e8c2c47a616962e887e35b23afa1c535f6f49ddea02ac019af43d13a9a8b`; replay identity is `307a5cd7ed2e5fdd347a0d1203a08fb3d2d9ad853c847d719df26b31227c0372` with `exact=true`. As in Work 083, raw FCStd bytes are not claimed deterministic; the canonical FreeCAD report is the replay evidence for the FCStd witness.

## Deviations from plan

- `src/formula_ultimate/subsystems/__init__.py` was listed as a planned file but required no change; the package docstring already covers the new module and Work 083 exports nothing there either. No edit was made rather than adding a gratuitous export.
- Two evaluator rules were corrected during implementation, before the first admitted CAD run, after a fabricated-fixture smoke check exposed them:
  - the `seized_support` preregistered consequence was changed from `no_delivered_power` to `rejected` plus `housing_temperature_exceeded_drive`. Injecting a drag torque equal to the transformed torque dissipates the full `2400 W` in the support, which the solved thermal model shows drives the housing to `488.8 K`, past its declared `400 K` domain. The control now asserts both the thermal rejection and zero delivered work, which is a stronger consequence than originally preregistered.
  - a `primary_energy_creation` rejection that fired whenever final store energy exceeded initial store energy was removed as physically wrong: recovered energy that traces to the declared conserved braking source is not external primary inflow, and the rule misfired on the `locked_converter` control. It was replaced by `recovered_energy_exceeds_source`, and the stricter "does not end above onboard pre-race energy" check was kept but scoped to the reference case only.
- Both corrections changed preregistered expectations, so they are recorded here rather than presented as the original plan. Neither was made after observing an admitted CAD or replay result.

## Evidence review

Supporting evidence: seven independently inspectable solids, exact STEP identities, a seven-object FCStd, calculated one-DOF mobility, a geometry-taken torque ratio, twenty-one exact pair-clearance records, single continuous torque and reaction paths identity-coupled to the frozen Work 083 evidence, closed quasi-static and quasi-steady ledgers, two geometry-versus-analytic surface-area cross-checks, ten causal controls, and exact canonical replay.

Contradicting evidence: the statics place `415.4 N` radially on the Work 083 axle, a load case Work 082 never evaluated — its only structural witness is the `500 N` tangential bracket family — so this candidate imposes an unvalidated demand on its upstream subsystem. The declared coupling to that axle is a butt interface with no modelled fastener. The traction coupling has no modelled engagement elements, so its no-slip ratio is declared rather than demonstrated. The energy store doubles as the reaction terminal, which is a placeholder that Work 085 must replace. Raw FCStd byte identity also does not replay. These facts are retained rather than hidden.

Alternative explanations: the residuals near machine epsilon follow from algebraically paired torque, statics, and energy relations rather than from experimental measurement, exactly as in Work 083; the thermal residual is a check on a closed-form solution, not an independent measurement. Apparent feasibility may follow from generous clearances, a single frozen operating point, and quasi-steady assumptions. CadQuery and FreeCAD share OCCT technology, so their agreement is a `toolchain_cross_check`, not independent physical validation. The comfortable structural utilizations reflect a low-power bounded specimen rather than a race-representative duty.

Missing evidence: meshed structural solves for the shaft, support, and housing; design-eligible material and process records; fastener, bearing, lubrication, and engagement-element models; transient thermal and speed-decay behaviour; fatigue, fracture, buckling, and contact analysis; packaging and service envelopes at vehicle scale; manufacturing tolerances; physical tests; and integration with Works 085 and 086.

Confidence is high for exact software identities, seven separate CAD solids, the declared mobility and ratio arithmetic, static clearance at the frozen assembly state, ledger closure, domain enforcement, and fault propagation under this fixture. Confidence is low for any real-world capacity, durability, thermal adequacy, controllability, or production claim.

## Exact validation commands and results

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\candidates\build_energy_torque_path_candidate_001.py `
  --config config\candidates\energy_torque_path_candidate_001.json `
  --output-root artifacts\work084\run_a `
  --work083-result artifacts\work083\run_b\result.json `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"
# exit 0; 7 parts; 7 assembly solids; 1 DOF; torque ratio 3.0;
# minimum clearance 0.0009999999999999898 m; maximum overlap 0.0 m3;
# drum ground clearance 0.0050000000000000044 m;
# torque/reaction/energy/thermal residual 0.0 / 1.42e-16 / 0.0 / 9.00e-16;
# maximum structural utilization 0.5823428918158171;
# verdict=not_admitted_synthetic_evidence

& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\candidates\build_energy_torque_path_candidate_001.py `
  --config config\candidates\energy_torque_path_candidate_001.json `
  --output-root artifacts\work084\run_b `
  --work083-result artifacts\work083\run_b\result.json `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work084\run_a\result.json
# exit 0; replay_exact=true;
# result_sha256=c87fa43572efc0a8bc6ef67e375589943d73ecc4ca3b3a3d7a51df4ddb3edb66

python -m unittest tests.test_energy_torque_path_candidate_001 -v
# exit 0; Ran 31 tests; OK

python -m unittest `
  tests.test_energy_torque_path_candidate_001 `
  tests.test_repository_contract -v
# exit 0; Ran 37 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 577 tests in 362.348s; OK (skipped=3)
```

Environment: Python 3.14 for the repository test suite, the pinned `.tools/cadquery-mcp` CadQuery `2.8.0` environment for geometry generation, and FreeCAD `1.1.3` with OCCT `7.8.1` for the independent import witness, on Windows 11.

## Limitations and follow-up

Work 084 does not close its meshed structural completion gate. The Work 082 evaluator maps its loaded region as a `z`-axis cylindrical hole and its support as a constant-`x` plane, so it cannot accept this candidate's `y`-axis bores, torsional loading, or bearing reactions without changing the frozen Work 082 configuration identity, which program rule 4.1 forbids. A separately numbered remedial work must add a generalised meshed torsion, bearing, and housing route, and must include the `415.4 N` radial demand this candidate places on the Work 083 axle.

Until that remedial work completes, Gate B in `WORKS_080_086_DETAILED_EXECUTION_PLAN.md` may not be claimed, and Work 085 may consume this candidate's mount, torque, and heat interfaces only as a synthetic integration fixture, never as validated hardware interfaces. The design-evidence blocker inherited from Work 079 and Work 083 also remains open: no design-eligible material, process, or measurement record has been admitted.
