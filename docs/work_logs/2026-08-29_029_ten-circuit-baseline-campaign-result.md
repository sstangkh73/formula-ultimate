# Work 029 Result: Ten-Circuit Fixed-Topology Baseline Campaign

Status: Completed

Thai companion: `2026-08-29_029_ten-circuit-baseline-campaign-result.th.md`

## Outcome

Implemented and executed a strict fixed-topology Level-0 baseline campaign across all ten versioned circuit profile distances. One energy-consuming reference family completed all `30/30` circuit/seed runs under a common architecture, component opportunity, energy profile, timestep, run budget, design-evaluation budget, seed set, and immutable calibration/holdout split.

Every result remains `profile-distance-analytical-proxy` with `real_circuit_admitted = false` because measured local corridor and event-time weather evidence are unavailable.

## Files Changed

- Added `config/simulation/fixed_topology_baseline_protocol_v1.json`.
- Added `src/formula_ultimate/simulation/baseline_campaign.py` and public exports.
- Added ten focused campaign tests and `scripts/validate_baseline_campaign.py`.
- Added typed `synthetic_control` weather support through step input and aerodynamic adapters, their tests, validators, and bilingual documentation.
- Added the bilingual baseline campaign model record, this plan/result pair, three bilingual problem reports, and updated the implementation queue.

## Resolved Problems

1. Weather evidence could not represent a synthetic analytical control without falsely calling it observed.
2. The first baseline contact state placed `300 K` in `suspension_travel_m` through positional construction, causing every run to fail closed.
3. The first aggregate exposed family-profile pair count as profile count, which would over-count a future multi-family campaign.

## Decisions

- Use nonzero aerodynamic drag and balancing propulsion rather than a frictionless, zero-energy coast.
- Pin primary energy `50,000,000 J`, drive efficiency `0.9`, reference area `1.5 m^2`, drag coefficient `0.5`, and maximum drive force `1000 N`.
- Pin `1000 s` timestep, `40000 s` timeout, `64` maximum steps/run, design-evaluation budget `1`, and seeds `(17, 29, 43)`.
- Fix seven calibration and three holdout profiles before execution.
- Treat actual step count as consumed compute while retaining identical maximum opportunity.
- Keep unresolved static width as `indeterminate`, never passed.
- Reject hidden protocol fields, implicit budget coercion, partition mismatch, evidence-grade escalation, and real-circuit admission.

## Experiment and Falsification Result

- Independent variables: ten circuit profiles and three seeds.
- Dependent evidence: outcome, time, distance, primary energy, steps, residuals, replay identity, width status, and partition.
- Controls: architecture v4, one four-contact family, component library, steady-drag strategy, energy, synthetic environment, timestep, budgets, and holdout assignment.
- Result: `30/30` runs finished; ten profiles completed; all residuals passed; no run exceeded `31/64` steps.
- Energy used ranged from `12.676688 MJ` at Monaco to `15.012090 MJ` at Bahrain.
- Same-circuit metrics were equal across seeds while replay identities remained seed-specific.
- Falsification rejected overlapping/incomplete partitions, hidden fields, float integer budgets, evidence escalation, and mutated opportunity. A one-step budget produced observable timeouts with no extension. Catalog permutation replayed exactly.
- Contradicting evidence: none for the declared software/fairness contracts.
- Alternative explanation: completion follows a straight synthetic path and constant environment, not the physical circuit layout.
- Missing evidence: surveyed local geometry, observed event weather, braking/cornering/traffic, calibrated models, uncertainty, and higher fidelity.
- Confidence: high for deterministic campaign controls and execution; low for real-circuit performance, which is explicitly unadmitted.

## Validation Commands and Evidence

All commands returned exit status `0`:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_step_inputs tests.test_aero_load_coupling tests.test_whole_race tests.test_baseline_campaign -v
python -m unittest discover -s tests
python scripts/validate_step_inputs.py
python scripts/validate_aero_load_coupling.py
python scripts/validate_whole_race.py
python scripts/validate_baseline_campaign.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

- focused Work 023/024/028/029 regression: 39 passed in `12.748 s`;
- full repository suite: 252 passed in `14.879 s`;
- completed runs/profiles: `30/30`, `10/10`;
- architecture fingerprint: `abf3148cfba2063f8fdba23951239b2b0a4a899c391503d3e46db69fd203618d`;
- protocol fingerprint: `4c1c93a21c8ada5d8859eebbce1adb11f750787b2f522ba671f30be08ea6f2a6`;
- controls fingerprint: `9c6a168a90a1e8d7cf33f72f3410e8d193cfd4edffddf7a136c84a1bed0371c9`;
- result fingerprint: `44dc7f85fac097b8ecbb38c04ff14a595702e8e4a0b9134ba70403fc451bfa98`;
- real-circuit admission: `false` for the campaign and every run.

## Limitations

The campaign is a Level-0 profile-distance analytical proxy. It does not traverse physical circuit geometry, reproduce lap times, optimize the reference, or validate safety/manufacturability. Constant dry weather, straight corridor, steady speed, zero traffic, no rolling resistance, and uncalibrated component/aero assumptions limit interpretation.

## Follow-up

Work 030 must close deliberate integration-defect falsification, numerical refinement, uncertainty/claim review, and cross-model promotion/release gates. Unsupported candidates must remain unpromoted.
