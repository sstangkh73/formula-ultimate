# Formula Ultimate: Literature and Simulator Gap Review

Thai companion: `LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.th.md`

Review date: 2026-09-05. Inspected starting revision: `251ede5`. Work 102 is a documentation/research review, not a new experiment.

## Assessment

**Formula Ultimate currently has a substantial, testable research scaffold for physics-constrained design exploration, but not a physically validated whole-vehicle race simulator.** Its strongest demonstrated properties are traceability, rejection accounting, replay and bounded computational checks. The largest gaps are independent physical evidence, actual geometry-to-field evaluation, coupled transient vehicle prediction and design/controller co-optimization.

The code is more advanced than the top-level README's early longitudinal summary: planar, vertical, drivetrain, control, aero-map, thermal and mechanical/CAD work exist. Their existence does not imply that every domain participates in the same validated race simulation.

The [catalog](../research/RELATED_WORK_CATALOG_2026-09-05.md) contains 62 academic works and 8 official industry/tool sources, with relevance, limitations and reading depth. This review preserves the project's open-ended geometry and technology-neutral energy objective. A conventional F1 car is a comparison baseline, not a compulsory architecture.

## Current evidence: what actually passes

| Evidence | Observed result | What it establishes / does not establish |
| --- | --- | --- |
| Current test suite | `python -m unittest discover -s tests -q`: 689 tests in 285.212 s, exit 0, 7 skipped | Software regression evidence; skipped tests and this suite do not establish physical validity. |
| [FU-BMC-003 / Work 062](../research/BOUNDED_MAIN_CAMPAIGN_V3_RESULT.md) | 2,880 attempts, 36 streams, 12 paired seeds, 960 attempts per treatment; 2,107 feasible, 773 structural failures | A real bounded search campaign with controlled allocation, not open-ended whole-car discovery. |
| Same campaign's promoted candidates | 72 holdout-feasible; 51 pass refinement; 21 fail as `refined_disagreement`; 51 valid four-solid STEP/FreeCAD survivors | 21/72 = **29.17%** of promoted Level-0 survivors fail refinement. This conditional rate is not the false-positive rate of all 2,880 proposals. |
| Same campaign's search comparison | EVOLUTION vs RANDOM supported-finisher rate difference +0.1667; exact McNemar p = 0.5. Nine common-success seeds: median best-time difference -2.232959 s; sign-flip p = 0.0625 | Favorable observed direction, insufficient evidence of superiority at 0.05. The bounded five-variable grammar and conditional common-success subset limit generalization. |
| [Work 076 integrated lap](../research/INTEGRATED_LEVEL0_LAP_GATE_V1.md) | Synthetic 50 m-radius circle; lap 22.14108931044568 s; fixed throttle 0.3; dt = 0.005 s | Demonstrates closed-loop steering and coupled dynamics on an analytical circle. Not a real-circuit minimum-time lap or full race. |
| [Work 088 admission audit](../work_logs/2026-09-04_088_whole-mechanical-vehicle-candidate-001-result.md) | `audit_status=passed`, `candidate_verdict=not_ready`; 13/13 artifact classes; 11/11 cases evaluated; 0/11 ready | Successful audit correctly blocks the candidate; audit completion is not vehicle completion. |
| [Work 097 benchmarks](../work_logs/2026-09-05_097_generalized-meshing-contact-failure-evaluation-result.md) | Seven scoped adapters; largest fine relative error 0.0014270788520555852; largest last-two change 0.0042775693130952114 | Agreement/refinement for reduced models, not arbitrary STEP-derived nonlinear 3D finite-element validation. |

Retained `artifacts/work088/run_a/result.json` and `artifacts/work097/run_a/result.json` were inspected alongside code and records. They were not regenerated. Work 088 explicitly records `not_run_pre_admission_blocked`; Work 097 records `design_use_allowed=false` and `arbitrary_3d_nonlinear_contact_solved=false`.

The Work 088 mechanical blockers are concrete: eight positive-overlap pairs plus one zero-clearance pair; suspension motion gives 0.007 m misalignment against a 0.000001 m rigid-interface tolerance; the new load frame lacks meshed convergence evidence; material/process evidence is synthetic. These precede any claim that this candidate can finish a race.

## The most consequential code-level finding

In [generalized_geometry_benchmarks.py](../../src/formula_ultimate/structural/generalized_geometry_benchmarks.py), lines 144–194, reference and discrete paths reduce geometry to sampled section scalars and analytical/quadrature responses. Lines 193–194 construct:

```text
force residual = abs(load + (-load)) / scale
moment residual = abs(torque + (-torque)) / scale
stiffness = generalized_load / response
external = 0.5 * generalized_load * response
internal = 0.5 * stiffness * response**2
solver_converged = True
```

The force/moment residuals cancel by construction; energy agreement follows from the defined stiffness. They do not measure independently recovered reactions or a solved 3D stress/displacement field. Response refinement can still be a useful scoped numerical test. However, these residuals and the unconditional convergence flag cannot provide the missing independent equilibrium evidence. Negative-control rejection tests do not change that limitation.

This finding is scoped to this adapter. The older campaign really invokes CalculiX through [campaign_physics.py](../../src/formula_ultimate/experiments/campaign_physics.py); its beam-model evidence should not be erased or described as nonexistent. The distinction is between real solver evidence for a bounded beam problem and a general evaluator for new solid geometry.

Before Work 100 promotes unfamiliar mechanisms, introduce an actual mesh/solver route for the admitted geometry classes, with independently extracted reactions, residual histories, stress/displacement fields and failure states. Keep the present reduced tests as a lower-fidelity gate. [P28](https://orbi.uliege.be/handle/2268/22742?locale=en), [P29](https://github.com/ipc-sim/IPC), [P59](https://www.sciencedirect.com/science/article/pii/S0376042102000052)

## How far behind F1 simulation?

**There is no defensible percentage, number of years, or common lap-error ratio available from this evidence.** We have not run the same measured vehicle, track, inputs and scoring protocol as an F1 team; teams do not publicly expose a complete numerical error budget. A count of features, tests or simulated laps cannot supply that comparison.

Public F1 descriptions show a workflow combining computer models, driver-in-loop simulation and correlation against real car/track observations. A driver simulator's motion performance is a different property from vehicle-model predictive accuracy. [Mercedes I01](https://www.mercedesamgf1.com/news/how-does-f1-simulation-work), [McLaren I02](https://www.mclaren.com/racing/latest-news/mclarenracing/article/secrets-formula-1-simulator/), [Formula 1 I05](https://www.formula1.com/en/latest/article/smedley-what-is-correlation.3gcOwCLuQ7rxk4bNeBKf1p), [Dynisma I03](https://www.dynisma.com/news/dynisma-completes-scuderia-ferrari-mission-winnows-new-simulator)

The useful qualitative distance is **several missing evidence transitions**: a runnable coupled model, converged independent numerical benchmarks, calibrated subsystems with unseen-condition validation, then a correlated whole-vehicle/race model. Some Formula Ultimate subsystems have pieces of the first two; the inspected whole-vehicle candidate has not passed admission. Public F1 material demonstrates real-car correlation practice, but does not allow scoring every team on one universal scale.

A closer, reproducible intermediate target is public academic racing simulation. The GP2 study already combines a 14-DOF transient model, nonlinear tyres, ride-height aero and telemetry comparison. The fidelity-ablation study evaluates model simplifications against actual autonomous-racing data. They demonstrate capabilities our current integrated evidence does not yet show; their publication dates do not translate into a calendar delay for our project. [P34](https://eprints.soton.ac.uk/417133/), [P42](https://arxiv.org/abs/2602.07984)

## Gap matrix and priorities

Priority A = blocks credible discovery/race claims now; B = next fidelity expansion after an admitted baseline; C = later or conditional.

| Domain | Current inspected capability | Missing evidence/capability and consequence | Priority / sources |
| --- | --- | --- | --- |
| Geometry to mechanics | CAD graphs, witnesses, STEP inspection, bounded CalculiX beams, seven reduced adapters | Meshing actual admitted free-form geometry; boundary-condition transfer; independent field convergence, reactions and local failure. Otherwise selection can reward a proxy artifact. | A — P26–P30, P59 |
| Mechanical integration | Work 088 complete admission accounting | Clear interferences, compatible moving interfaces, load-frame mesh evidence, real material/process properties. The current candidate is `not_ready`. | A — local Work 088 |
| Tyres/contact | [Friction envelope](../../src/formula_ultimate/physics/tyre.py); [positive longitudinal slip/tanh route](../../src/formula_ultimate/simulation/drive_ground_coupling.py), lines 300–303 | Calibrated combined slip, load sensitivity, camber, relaxation and pressure/temperature applicability. Constant-friction capacity cannot establish near-limit lap rankings. It would be inaccurate to say no slip model exists. | A — P43–P46, P61, I07–I08 |
| Aero | [Maps](../../src/formula_ultimate/physics/aerodynamics.py) over speed, ride height, yaw and active state; forces/moments/cooling metadata | No demonstrated new-geometry CFD-to-validated-map pipeline in the inspected route; geometry, aero balance and cooling need measured/numerical support. An evidence enum `cfd` or `measured` does not supply that evidence. | A/B — P35, P47–P53 |
| Vehicle coupling | [Work 076](../../src/formula_ultimate/simulation/integrated_lap_gate.py) steering, planar/drivetrain/vertical interaction | Validated simultaneous tyre/aero/suspension/power/brake/thermal effects; transient maneuvers, force/moment closure and time-step sensitivity. Separate module tests cannot prove whole-system coupling. | A — P34–P35, P42, P55 |
| Track | Analytical circle; [sourced circuit descriptions](../research/REAL_CIRCUIT_SOURCE_REPORT.md) | A sourced spatial track with width, elevation, banking, surface and uncertainty; boundary-aware lap solver. Circuit length/ordinal demand is not a 3D road. | A — P32–P33, I04 |
| Driving optimization | Heading/cross-track controller and fixed-throttle lap | Comparable optimized speed, braking, steering and energy policies for each design; controller training/solve budget. A weak driver can make good mechanics look bad. | A — P03, P31, P39, P41, P62 |
| Energy and endurance | Powertrain accounting and [lumped thermal model](../../src/formula_ultimate/physics/thermal.py), derating/failure states | Full-stint thermal/energy limits, cooling interactions and repeatable finish criteria; eventually tyre wear, fatigue and robustness. One quick lap may not finish the race. | A for finish gate; B for richer models — P36–P38, P46 |
| Search and novelty | Bounded campaign plus geometry/topology machinery; planned QD | Mechanically meaningful diversity, actual topology/controller co-design, optimized baselines and full compute ledger. Five-scalar results are not open-ended discovery proof. | A — P03, P09, P11–P16 |
| Data and uncertainty | Replay, provenance, rejection records | Measured subsystem data, identification, measurement uncertainty, held-out conditions, model discrepancy and ranking stability. This is the largest gap to predictive engineering. | A — P17, P42, P58–P60 |
| Real time / human loop | Numerical time step and deterministic simulation | Deadline, latency/jitter measurements, controls/force feedback, motion and human correlation if driver-in-loop is needed. Low immediate value for autonomous discovery. | C — I01–I04 |
| Race environment | Bounded task/holdout treatment | Later traffic/wake, weather, surface evolution and multi-stint strategy if the declared research question needs them. Add only after a validated controlled race task. | B/C — P18–P19, P38, P40 |

The Work 076 time step corresponds to **200 Hz numerical sampling**, not demonstrated real-time throughput. rFpro's **up to 5 kHz** road feed and **1 cm / 1 mm** horizontal/vertical road detail describe a supplier's subsystem; dividing 5,000 by 200 would not establish that our simulator is 25 times behind. [I04](https://rfpro.com/simulation-software/terrain-server/)

## Literature closest to our actual objective

Three families need to meet:

1. **Discover mechanics and control together:** RoboGrammar, multi-objective graph search, Neural Graph Evolution, DERL and Evolution Gym. They are closer to our action than a fixed-car lap simulator, but each constrains its bodies, components or environment. P01–P10.
2. **Spend computation on credible, diverse candidates:** MAP-Elites, surrogate-assisted illumination, multifidelity optimization and transferability. These fit Works 098–100 and help prevent optimization against an inaccurate proxy. P11–P17.
3. **Predict racing behavior and verify it:** optimal-control GP2/F1 models, aero-suspension interaction, tyre/transient/thermal work, CFD experiments and uncertainty calibration. These supply the evaluator, not the discovery representation. P31–P59.

An especially close unconventional-vehicle example is the 2026 wheeled-quadruped racing paper: the authors report physical active-roll experiments with up to 44% lower mean load-transfer ratio and an 8.7% improvement in fastest lap time. Those results belong to that robot and baseline; they support investigating unusual active mechanics, not an F1-performance extrapolation or a claim that the paper discovered its morphology. [P10](https://arxiv.org/abs/2606.26313)

No inspected paper establishes the entire Formula Ultimate ambition end to end. That is a statement about this search, not proof of global novelty. A defensible prospective contribution is: **a geometry-to-evidence discovery process that finds distinct functional mechanisms which survive independent higher-fidelity checks and improve a declared racing objective under matched design/control budgets.** The present evidence supports building that study, not claiming it has succeeded.

## Recommended sequence and falsifiable experiments

These are proposals, not experiments executed by Work 102. They refine the existing [Works 098–101 roadmap](GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1.md), without changing it or assuming Work 097's completion solves unrestricted meshing.

| Order / experiment | Independent variables and controls | Dependent variables / metrics | Success and failure criteria |
| --- | --- | --- | --- |
| 1. Independent geometry evaluator | Actual admitted shape, mesh resolution and solver method; freeze SI units, material, load, boundary conditions and geometry identity | Displacement/stress, recovered reactions, residual history, contact penetration, runtime, invalid states | Predeclare analytic/experimental cases and uncertainty-based tolerances; at least three refinement levels and an independent comparison. Fail on nonconvergence, unexplained imbalance, missing field evidence or changed failure/ranking beyond the declared error budget. |
| 2. Coupled racing baseline | Model fidelity and time step; identical vehicle, input trace, track, data split and numerical tolerances | Speed/yaw/load traces, braking distance, energy, temperature, lap/sector error, runtime | Establish a matched public-model baseline and measured held-out subsystem tests; freeze tolerances before observing results. Fail if a good lap time hides wrong traces, if parameters need retuning per holdout, or if time-step changes reverse conclusions. |
| 3. Design/controller fairness | GRID, RANDOM, EVOLUTION, then QD; fixed-topology optimized baseline and free-topology treatment; paired seeds, same library, constraints and total budget | Supported finishers, best supported race score, diversity, invalid fraction, controller cost | Report all failures and paired uncertainty. Select seed budget by pilot variance/power planning, not just the best run. Fail the superiority claim if exact tests/intervals do not support it or the advantage disappears with a comparably trained controller. |
| 4. Multifidelity promotion audit | Promotion policy and fidelity; freeze candidate pool or paired proposal budgets and stratified audit sampling | False positives, false negatives, rank agreement, verified elite quality per compute | Audit some rejected candidates, not only survivors. Count CAD calls, solver seconds, mesh/iteration effort and controller training. Fail if missed good designs or fidelity bias explain the apparent gain. |
| 5. Isolated mechanism discovery, then integration | Topology family and active/passive/control choices; same interfaces, material/process, energy and race objectives | Functional improvement, manufacturability, independent checks, transfer across held-out loads/tracks | Promote only a reproducible subsystem survivor with a causal ablation. Integration must pass Work 088-type interference/kinematic/load checks. Fail when benefit is cosmetic, proxy-specific, energy-accounting dependent or disappears after integration. |

**Read first in this order:** P59/P15 for evidence and fidelity; P28 with actual solver documentation for meshing; P34/P42 for the coupled benchmark; P43/P44 for tyre behavior; P03/P09 for design/control search; P11/P13 for diversity and cost. Use [Fastest-lap I06](https://github.com/juanmanzanero/fastest-lap) and [Chrono::Vehicle P55](https://www.inderscience.com/info/inarticle.php?artid=97096) as candidates for a reproduced public baseline. Do not rewrite all mature numerical infrastructure before testing whether it can serve an adapter.

Highest immediate value: correct the meaning of independent solver evidence, obtain one admitted functional subsystem and one correlated racing baseline, then let search exploit that evaluator. More render detail, a motion platform or an unrestricted generator cannot substitute for those gates.

## Confidence, counterevidence and limits

- **High confidence:** current Work 088 not-ready status, scoped Work 076 circle behavior, the Work 097 residual construction, campaign counts/statistics and test result; grounded in inspected files and code.
- **Moderate confidence:** priority ordering and transferable methods; informed engineering judgment, not measured project-specific return on effort.
- **Unknown:** proprietary F1 accuracy, full current team architectures, time/cost to parity, our physical lap error, and whether unseen literature already covers the proposed contribution.
- **Supporting evidence:** preserved failures, deterministic replay, bounded solver/CAD campaigns and explicit non-promotion flags are valuable foundations.
- **Contradicting evidence:** 29.17% promoted-candidate refinement disagreement, non-significant search comparisons, zero ready Work 088 cases, synthetic properties and constructed residuals restrict stronger claims.
- **Alternative explanations:** apparent evolutionary gains may reflect grammar/controller allocation or low-fidelity bias; apparent solver agreement can reflect shared assumptions; CAD validity can coexist with mechanical incompatibility.
- **Missing evidence:** independent measured data and uncertainty, calibrated coupled laps, general admitted-geometry field solves, and robust free-topology superiority.

The full suite was rerun; historical campaigns and third-party papers/software were not reproduced. No physics code, configuration, solver installations or roadmap commitments were changed by this review.
