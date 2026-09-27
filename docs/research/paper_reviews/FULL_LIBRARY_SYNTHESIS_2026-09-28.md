# Full Paper-Library Synthesis for Formula Ultimate

Thai companion: `FULL_LIBRARY_SYNTHESIS_2026-09-28.th.md`

Reading date: 2026-09-28 (Asia/Bangkok)

## Scope and method

This report covers every PDF present under `papers/` at extraction time: **261 papers, 6,280 pages, and approximately 3,503,351 extracted words**. Full text was processed page by page into a reading manifest binding source path, SHA-256, page coverage, section cues, and high-information cue pages. The evidence was then synthesized across the library's 15 topics.

Two review depths are explicit: 15 decision-critical papers receive deep reviews with methods, numbers, findings, limitations, page locators, and paper-specific proposals; the other 246 receive full-text transfer records binding a curated takeaway to a topic-specific target, experiment/control, and pass/fail evidence. The latter should not be read as equivalent to a critical replication.

Important boundary: reading is not replication. The authors' computations and experiments were not independently rerun, and simulation, benchmark, or review evidence is not promoted to physical validation of Formula Ultimate.

Six PDFs had text coverage below 95%. Their low-text pages were rendered and inspected: they were figure-only plates (CFD fields, geometry grids, diagrams, or dataset visualizations) or a blank trailing page, not unread scanned prose. No PDF was classified as an unreadable scan.

## Cross-library conclusions

1. The literature supports an open-ended Formula Ultimate objective, but openness must operate inside explicit physical constraints and evidence gates.
2. Representation, evaluator, and compute allocation are part of the discovery result, not implementation details that can be ignored.
3. Novel-looking geometry must pass a ladder: constructible geometry -> causal physical response -> assembly/vehicle function -> fair superiority over optimized baselines -> higher-fidelity and holdout survival -> external novelty assessment.
4. The most urgent gaps still match the current roadmap: transient tyre/contact, aero fields, energy/thermal endurance, independently recovered structural evidence, tolerance/fatigue, and coupled whole-vehicle replay.
5. AI agents and generative models should increase proposal and repair throughput, but must not judge the correctness of their own artifacts.
6. QD and multifidelity search fit the problem only with descriptor versioning, uncertainty, false-negative audits, resource ledgers, and untouched holdouts.
7. Public data can calibrate, pretrain, and test pipelines, but domain shift must be declared and project-specific conditions must remain independently held out.
8. Autonomous-racing work shows the need for a strong optimized controller baseline before attributing gains to vehicle morphology.

## Prioritized project improvements

1. **Credible evaluators before more search:** close field-equilibrium, contact, tyre, aero, and thermal-energy gaps; retain invalid and numerical failures as outcomes.
2. **Coupled full-race transient:** combine vehicle, tyre, aero, energy, brake, thermal, and controller states under total race time and a finish gate.
3. **Fair search:** matched seeds, compute, evaluator access, controller allocation, optimized fixed-topology baselines, and resource accounting.
4. **Auditable multifidelity promotion:** uncertainty envelopes, discrepancy models, stratified audits, and independent replay.
5. **Progressive physical evidence:** specimen -> connection/subsystem -> assembly -> vehicle; never skip stages using simulation claims.
6. **Four separate claims:** geometric novelty, causal functional difference, performance superiority, and external technology novelty.

## OE: Open-ended, evolutionary and morphology/control co-design discovery

**Scope:** Work that searches over body/topology and behaviour together, or studies what makes open-ended design search productive. Closest to the project's discovery objective; none of it validates a racing vehicle.

**Cross-paper findings**
- Body topology, controller learning, and environment difficulty interact; evaluating a new body with an under-trained controller systematically removes potentially useful morphology.
- Generative encodings, graph grammars, and differentiable refinement offer different search biases. No representation is neutral, so representation coverage must itself be audited.
- The strongest precedents close part of the sim-to-real loop through fabrication or physical trials; virtual novelty alone is not a technology-discovery claim.

**What is especially interesting**

- [OE-002](by_paper/OE-002_review.md): Closes the loop from evolved design to a manufactured, physically tested machine; the template for an eventual build-and-test gate after Level-0 search.
- [OE-016](by_paper/OE-016_review.md): The paper isolates controller-adaptation lag as a selection bias: a structurally promising child can look worse only because it inherits a controller specialized for its parent (p. 5).
- [OE-029](by_paper/OE-029_review.md): Quantifies how the split of compute between design and control changes co-optimisation outcomes; directly relevant to budget-matched fairness rules.

Across these 33 papers, the leading evidence profiles are optimization/search study (29), empirical/experimental evidence (24), control/learning study (23), simulation/numerical evidence (14), physical-test evidence (8), dataset/benchmark (8), review/synthesis (2), mathematical/formal evidence (2). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Add controller-allocation fairness and morphology-age protection to the Work 124 search scheduler.
- Compare direct, generative, graph, and continuous-refinement representations at matched compute and evaluator access.
- Require physical-correlation gates from Works 131-133 before promoting unconventional morphology beyond simulation.

**Per-paper reports and principal takeaways**
- [OE-001: Evolving Virtual Creatures](by_paper/OE-001_review.md) — Founding example of evolving body graphs and controllers together; the typed-genome and topology mutation work (Works 093-094) descends from this idea.
- [OE-002: Automatic design and manufacture of robotic lifeforms](by_paper/OE-002_review.md) — Closes the loop from evolved design to a manufactured, physically tested machine; the template for an eventual build-and-test gate after Level-0 search.
- [OE-004: Evolution Gym: A Large-Scale Benchmark for Evolving Soft Robots](by_paper/OE-004_review.md) — Shared co-design benchmark with fixed tasks and budgets; borrow its benchmark discipline for fair GRID/RANDOM/EVOLUTION/QD comparisons.
- [OE-005: Neural Graph Evolution: Towards Efficient Automatic Robot Design](by_paper/OE-005_review.md) — Reuses graph-network controllers across morphology mutations to cut retraining cost; relevant if every topology needs its own optimised driver.
- [OE-006: Embodied Intelligence via Learning and Evolution](by_paper/OE-006_review.md) — Shows environment complexity shapes evolved morphology (DERL); evidence and method for testing H3 across race environments.
- [OE-007: DiffAqua: A Differentiable Computational Design Pipeline for Soft Underwater Swimmers with Shape Interpolation](by_paper/OE-007_review.md) — Differentiable shape-and-control co-design; a model for gradient refinement inside an admitted topology, not for topology change itself.
- [OE-008: Multi-Objective Graph Heuristic Search for Terrestrial Robot Design](by_paper/OE-008_review.md) — Discrete graph design search under competing objectives; a comparator for multi-objective race time, energy, mass and reliability (H2).
- [OE-009: Racing a Wheeled Quadruped: Active Load Transfer Mitigation via Model Predictive Control](by_paper/OE-009_review.md) — Physical racing of an unconventional ground-contact architecture with lap-time gains from active leg mechanics; the closest published analogue to a non-car racing morphology.
- [OE-010: Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions](by_paper/OE-010_review.md) — Co-evolves environments and solutions; useful for curriculum tracks, provided held-out evaluation tracks stay fixed.
- [OE-011: Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions](by_paper/OE-011_review.md) — Adds a domain-general novelty measure and transfer between environment-solution pairs; relevant to measuring environment novelty honestly.
- [OE-012: Reality-assisted evolution of soft robots through large-scale physical experimentation: a review](by_paper/OE-012_review.md) — Reviews putting physical experiments inside the evolutionary loop; informs the physical-correlation programmes (Works 131-133).
- [OE-013: Evolving Neural Networks through Augmenting Topologies](by_paper/OE-013_review.md) — NEAT: historical markings, speciation and complexification for evolving graph topology; the standard answer to crossover between different topologies (Work 094).
- [OE-016: Scalable Co-Optimization of Morphology and Control in Embodied Machines](by_paper/OE-016_review.md) — **deep review** — With morphology protection, mean fitness rose from 18.715 at generation 0 to 22.916 at generation 5,000 (p < 0.001). An alternative protection treatment did not beat no protection (p = 0.240) and was significantly worse than morphology protection (p = 1.211e-4) (p. 4).
- [OE-017: Environmental influence on the evolution of morphological complexity in machines](by_paper/OE-017_review.md) — Measures how environment shapes evolved morphological complexity; a direct method reference for H3 environment-dependent specialisation.
- [OE-020: Efficient automatic design of robots](by_paper/OE-020_review.md) — Gradient-based whole-body design found in seconds and fabricated; a benchmark for how fast a topology search can be once differentiable physics exists.
- [OE-021: Reinforcement Learning for Improving Agent Design](by_paper/OE-021_review.md) — Joint learning of body parameters and policy; shows the optimiser exploits body freedom in unexpected ways, a warning for our objective checks.
- [OE-022: Jointly Learning to Construct and Control Agents using Deep Reinforcement Learning](by_paper/OE-022_review.md) — Design-conditioned policy shared across a design distribution; a way to amortise driver optimisation over many candidate vehicles.
- [OE-023: Data-efficient Co-Adaptation of Morphology and Behaviour with Deep Reinforcement Learning](by_paper/OE-023_review.md) — Uses learned value functions to evaluate new designs without full rollouts; relevant to cheap pre-screening before Level-0 races.
- [OE-024: Transform2Act: Learning a Transform-and-Control Policy for Efficient Agent Design](by_paper/OE-024_review.md) — Policy that first edits the body graph then controls it; an alternative to evolutionary topology mutation worth comparing at equal budget.
- [OE-025: An End-to-End Differentiable Framework for Contact-Aware Robot Design](by_paper/OE-025_review.md) — Differentiable contact-aware design with cage-based deformation; relevant to ground-interaction and contact-driven geometry.
- [OE-026: SoftZoo: A Soft Robot Co-design Benchmark For Locomotion In Diverse Environments](by_paper/OE-026_review.md) — Co-design benchmark across diverse environments; a pattern for running one search across several race environments and comparing specialisation.
- [OE-027: Evolution and learning in differentiable robots](by_paper/OE-027_review.md) — Combines evolution of bodies with gradient learning of control at scale; informs the split between discrete search and continuous refinement.
- [OE-028: Co-optimising Robot Morphology and Controller in a Simulated Open-Ended Environment](by_paper/OE-028_review.md) — Morphology-controller co-optimisation under POET-style open-ended environments; shows how environment generation interacts with body search.
- [OE-029: An Empirical Study on the Computation Budget of Co-Optimization of Robot Design and Control in Simulation](by_paper/OE-029_review.md) — Quantifies how the split of compute between design and control changes co-optimisation outcomes; directly relevant to budget-matched fairness rules.
- [OE-030: Convergent Functions, Divergent Forms](by_paper/OE-030_review.md) — Studies how distinct forms reach the same function in morphology search; relevant to separating appearance novelty from functional novelty.
- [OE-031: Embodied Co-Design for Rapidly Evolving Agents](by_paper/OE-031_review.md) — Recent survey of morphology-control co-design from virtual creatures to physical robots; a map of methods and open problems.
- [OE-032: Shaping the Evolutionary Dynamics of Robot Morphology via Adaptive Control Learning](by_paper/OE-032_review.md) — How controller learning speed shapes which morphologies survive; relevant to controller-allocation bias in our search.
- [OE-033: Shape Your Body: Value Gradients for Multi-Embodiment Robot Design](by_paper/OE-033_review.md) — Uses value gradients of a multi-embodiment policy to improve body design; a continuous-design comparator.
- [OE-034: Seeking Quality Diversity in Evolutionary Co-design of Morphology and Control of Soft Tensegrity Modular Robots](by_paper/OE-034_review.md) — Quality-diversity applied to morphology/control co-design; a precedent for the executable morphology archive (Work 099).
- [OE-035: Open-Endedness is Essential for Artificial Superhuman Intelligence](by_paper/OE-035_review.md) — Defines open-endedness as novelty plus learnability to an observer; a usable definition for what our discovery claims should mean.
- [OE-038: Design Mining Interacting Wind Turbines](by_paper/OE-038_review.md) — Evolves physical designs evaluated by 3D printing and wind-tunnel tests with surrogates; an example of physical evaluation in the loop.
- [OE-039: Keep Rollin' - Whole-Body Motion Control and Planning for Wheeled Quadrupedal Robots](by_paper/OE-039_review.md) — Hybrid wheel-leg locomotion control; shows what a non-conventional ground-contact endpoint demands from control.
- [OE-040: Automated Antenna Design with Evolutionary Algorithms](by_paper/OE-040_review.md) — NASA ST5 evolved antenna that flew; a rare case of an evolved, non-intuitive hardware design passing real qualification.

## AG: LLM and AI agents for engineering design, CAD code and simulation

**Scope:** Agents and generative models that propose engineering designs, write CAD programs or drive solvers, plus work on how such systems are evaluated. Relevant because Formula Ultimate's designer is an agent that writes CadQuery and is judged by independent evaluators.

**Cross-paper findings**
- LLM agents are most useful as proposal, code, and workflow generators when paired with executable verifiers; fluent output is not engineering evidence.
- CAD and CAE benchmarks repeatedly expose a gap between visual plausibility or tool completion and functional, geometric, or multiphysics correctness.
- Search benefits from archives, reflection, and test-time candidate generation, but evaluation leakage and self-judging can manufacture apparent progress.

**What is especially interesting**

- [AG-003](by_paper/AG-003_review.md): Evolutionary coding agent with a MAP-Elites-style program database and machine-checkable scores, including a hardware-circuit result; a reference architecture for our design agent.
- [AG-004](by_paper/AG-004_review.md): Questions whether reported gains of LLM evolutionary search survive fair baselines and budgets; directly supports our falsification and matched-budget rules.
- [AG-026](by_paper/AG-026_review.md): A generated program can execute and match one nominal shape while encoding the wrong parameter dependency, causing its structural-response family to diverge (p. 5).

Across these 43 papers, the leading evidence profiles are empirical/experimental evidence (34), dataset/benchmark (32), simulation/numerical evidence (26), physical-test evidence (21), optimization/search study (12), review/synthesis (11), mathematical/formal evidence (10), control/learning study (7). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Keep agents outside the authority boundary: they may propose artifacts, but deterministic geometry, physics, provenance, and test gates decide admission.
- Add CAD/CAE task suites with hidden negative controls, exact artifact checks, and failure localization rather than natural-language grading.
- Record prompts, tool versions, retries, token/compute cost, and verifier outcomes in the experiment ledger.

**Per-paper reports and principal takeaways**
- [AG-001: Evolution through Large Models](by_paper/AG-001_review.md) — LLM as the mutation operator inside MAP-Elites, generating locomoting Sodarace morphologies as code; the closest template for an LLM that mutates CadQuery vehicle programs.
- [AG-002: Mathematical discoveries from program search with large language models](by_paper/AG-002_review.md) — FunSearch pairs an LLM proposer with an automatic, trusted evaluator; its separation of generation from evaluation mirrors our independent-evaluator rule.
- [AG-003: AlphaEvolve: A coding agent for scientific and algorithmic discovery](by_paper/AG-003_review.md) — Evolutionary coding agent with a MAP-Elites-style program database and machine-checkable scores, including a hardware-circuit result; a reference architecture for our design agent.
- [AG-004: Evolution or Illusion? Rethinking Evaluation in LLM Evolutionary Search](by_paper/AG-004_review.md) — Questions whether reported gains of LLM evolutionary search survive fair baselines and budgets; directly supports our falsification and matched-budget rules.
- [AG-005: The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery](by_paper/AG-005_review.md) — End-to-end automated research loop; useful mainly for its documented failure modes (overclaiming, weak review), which our evidence tiers are designed to block.
- [AG-006: How Can Large Language Models Help Humans in Design and Manufacturing?](by_paper/AG-006_review.md) — Systematic test of an LLM across CAD generation, performance evaluation, optimisation and manufacturing; maps where language models fail on geometry and physics.
- [AG-007: Large Language Model Agent as a Mechanical Designer](by_paper/AG-007_review.md) — LLM agent iterating truss designs with FEM feedback, compared against NSGA-II at equal evaluations; a direct method and fairness comparator.
- [AG-008: An LLM-enabled Multi-Agent Autonomous Mechatronics Design Framework](by_paper/AG-008_review.md) — Multi-agent design of a physical mechatronic prototype across mechanical, electronic and software domains; comparable to our multi-domain part-to-vehicle pipeline.
- [AG-009: Physics-in-the-Loop: A Hybrid Agentic Architecture for Validated CAD Engineering Design](by_paper/AG-009_review.md) — Generate-simulate-refine CAD agent with a validated physics tool in the loop rather than visual feedback; the same pattern as our CadQuery-to-evaluator loop.
- [AG-010: Engineering.ai: A Platform for Teams of AI Engineers in Computational Design](by_paper/AG-010_review.md) — LLM agents running CAD, meshing, multidisciplinary simulation and optimisation in a closed loop; a comparable system to benchmark against.
- [AG-011: Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback](by_paper/AG-011_review.md) — Uses FEA results as the feedback signal for a CAD-writing agent; directly relevant to geometry-structural coupling (Works 082, 138).
- [AG-012: FEABench: Evaluating Language Models on Multiphysics Reasoning Ability](by_paper/AG-012_review.md) — Benchmark for LLM agents driving a finite-element package end to end; a yardstick for how far agents can be trusted with solver setup.
- [AG-013: FEM-Bench: A Structured Scientific Reasoning Benchmark](by_paper/AG-013_review.md) — Graduate-level FEM coding tasks with automatic checks; useful for testing any agent that writes our element or solver code.
- [AG-014: What Do CAE Simulation Agents Really Need Beyond a Generic Harness?](by_paper/AG-014_review.md) — Analyses what tooling CAE agents need beyond a generic coding harness; informs the CAD/solver tool interface design.
- [AG-015: VFEAgent: A Multimodal Agent Framework for End-to-End Automated Finite Element Analysis](by_paper/AG-015_review.md) — Vision-augmented agent for FEA setup with an expert-graded benchmark including topology optimisation; a comparator for automated structural evaluation.
- [AG-016: MechAgents: Large language model multi-agent collaborations can solve mechanics problems, generate new data, and integrate knowledge](by_paper/AG-016_review.md) — Multi-agent LLMs writing and checking FEniCS elasticity code; shows self-correction value and its limits.
- [AG-017: Large Language and Text-to-3D Models for Engineering Design Optimization](by_paper/AG-017_review.md) — Text-to-3D car shapes optimised for CFD drag inside an evolutionary loop; directly relevant to generating vehicle bodies scored by aerodynamics.
- [AG-018: Drag-guided diffusion models for vehicle image generation](by_paper/AG-018_review.md) — Guides a generative model with a drag surrogate; illustrates the risk that surrogate guidance rewards surrogate errors.
- [AG-019: Text-to-CadQuery: A New Paradigm for CAD Generation with Scalable Large Model Capabilities](by_paper/AG-019_review.md) — Trains LLMs to emit CadQuery directly; the same CAD language our agents write, with a dataset and error statistics we can reuse.
- [AG-020: CAD-Recode: Reverse Engineering CAD Code from Point Clouds](by_paper/AG-020_review.md) — Recovers CadQuery programs from point clouds with a large synthetic CadQuery corpus; useful data and a geometry-to-code check.
- [AG-021: Generating CAD Code with Vision-Language Models for 3D Designs](by_paper/AG-021_review.md) — CADCodeVerify: the model renders its own CAD output and self-verifies; a cheap pre-check before our independent geometry witnesses.
- [AG-022: CADDesigner: Conceptual CAD Model Generation with a General-Purpose Agent](by_paper/AG-022_review.md) — General-purpose agent with structured diagnostics for failed CAD scripts; relevant to turning kernel errors into repairable feedback.
- [AG-023: Towards High-Fidelity CAD Generation via LLM-Driven Program Generation and Text-Based B-Rep Primitive Grounding](by_paper/AG-023_review.md) — FutureCAD: LLM writes CadQuery and grounds references to B-rep primitives; addresses the fragile face/edge selection problem in generated CAD.
- [AG-024: Clarify Before You Draw: Proactive Agents for Robust Text-to-CAD Generation](by_paper/AG-024_review.md) — Agents that resolve underspecified CAD requests before drawing; relevant to typed interface specifications for generated parts.
- [AG-025: Test-Time Scaling for CAD Generation via Verifier-Free Consensus Selection](by_paper/AG-025_review.md) — Selects among sampled CAD programs by consensus; a cheap filter, but consensus is not a physical check.
- [AG-026: CADEngBench: It Looks Like CAD, but Does It Work? Evaluating Parametric Design, Assembly Reasoning, and Physics Simulation](by_paper/AG-026_review.md) — **deep review** — Editing supplied CAD is substantially easier than generating it; complex edits and matched linear-static FEA remain difficult. Assembly models often find the right region but not the recorded joint or mating entities, and no model leads every evaluation stage (pp. 1, 5, 22-23).
- [AG-027: Automated Design Optimization via Strategic Search with Large Language Models](by_paper/AG-027_review.md) — LLM-guided strategic search for engineering design optimisation; a comparator for LLM-proposed parameter moves.
- [AG-028: Generative Reliability-Based Design Optimization Using In-Context Learning Capabilities of Large Language Models](by_paper/AG-028_review.md) — LLM in-context design generation under reliability constraints; relevant to uncertainty-aware gates.
- [AG-029: From Concept to Manufacturing: Evaluating Vision-Language Models for Engineering Design](by_paper/AG-029_review.md) — Broad evaluation of vision-language models on engineering design tasks; documents where they cannot be trusted.
- [AG-030: Deep Generative Models in Engineering Design: A Review](by_paper/AG-030_review.md) — Review of generative models for engineering design, including validity and performance gaps; a map of methods for geometry proposal.
- [AG-031: Beyond Statistical Similarity: Rethinking Metrics for Deep Generative Models in Engineering Design](by_paper/AG-031_review.md) — Argues generated designs must be scored on constraint satisfaction, performance and novelty rather than similarity to data; aligned with our discovery criteria.
- [AG-032: Constraining Generative Models for Engineering Design with Negative Data](by_paper/AG-032_review.md) — Trains on infeasible examples to keep generators inside constraints; our rejection ledgers are exactly such negative data.
- [AG-033: BIKED: A Dataset for Computational Bicycle Design with Machine Learning Benchmarks](by_paper/AG-033_review.md) — Parametric vehicle-design dataset with structural and performance labels; a public example of vehicle design data with validity checks.
- [AG-034: The impact of AI on engineering design procedures for dynamical systems](by_paper/AG-034_review.md) — Discusses how AI changes design procedures for dynamical systems, including validation obligations.
- [AG-035: Eureka: Human-Level Reward Design via Coding Large Language Models](by_paper/AG-035_review.md) — LLM writes reward code for control tasks; a caution that agent-written objectives must be frozen and audited before search.
- [AG-036: RoboMorph: Evolving Robot Morphology using Large Language Models](by_paper/AG-036_review.md) — LLM-driven evolutionary search over modular robot morphologies; a direct analogue of LLM-guided topology mutation.
- [AG-037: Text2Robot: Evolutionary Robot Design from Text Descriptions](by_paper/AG-037_review.md) — Text to evolved, fabricated legged robots; shows the manufacturing constraints needed for generated bodies to be buildable.
- [AG-038: Large Language Models as Optimizers](by_paper/AG-038_review.md) — OPRO: LLMs propose solutions from a scored history; a baseline for LLM-as-optimiser behaviour.
- [AG-039: CodeEvolve: an open-source evolutionary framework for algorithmic discovery and optimization](by_paper/AG-039_review.md) — Open-source AlphaEvolve-style framework; a runnable reference implementation for LLM evolutionary search.
- [AG-040: OMNI: Open-endedness via Models of human Notions of Interestingness](by_paper/AG-040_review.md) — Uses a foundation model to judge which tasks are interesting; relevant to deciding which novel mechanisms deserve evaluation budget.
- [AG-041: Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents](by_paper/AG-041_review.md) — Survey of LLM scientific agents; context for positioning an engineering-discovery agent.
- [AG-042: LLEMA: Evolutionary Search with LLMs for Multi-Objective Materials Discovery](by_paper/AG-042_review.md) — LLM-guided evolutionary search in materials; the project restricts itself to catalog materials, so this is context rather than a method to adopt.
- [AG-043: Physical Design using Differentiable Learned Simulators](by_paper/AG-043_review.md) — Optimises designs through learned graph-network simulators (airfoils, fluid tools); shows both the speed and the surrogate-exploitation risk.

## QD: Quality diversity, search algorithms, surrogates and multifidelity

**Scope:** Algorithms for spending evaluation budget on diverse, high-quality and credible candidates: MAP-Elites and descendants, novelty search, evolution strategies, Bayesian and multifidelity optimisation, and sim-to-real transferability.

**Cross-paper findings**
- QD methods separate finding one optimum from illuminating many high-quality niches; descriptor choice determines what diversity is visible.
- Surrogate and multifidelity methods save expensive evaluations only when uncertainty, fidelity discrepancy, and false-negative audits are explicit.
- Novelty can unlock stepping stones, but novelty without feasibility and external task holdouts does not establish useful discovery.

**What is especially interesting**

- [QD-001](by_paper/QD-001_review.md): MAP-Elites: keeps the best design per behaviour cell; the base algorithm of the executable morphology archive (Work 099).
- [QD-003](by_paper/QD-003_review.md): Besides saving evaluations, SAIL exposes encoding bias: its maps show which regions an encoding can express and where the surrogate is easy or hard to learn (discussion, pp. 25-26).
- [QD-005](by_paper/QD-005_review.md): The reference for combining cheap and expensive models without trusting the cheap one; underpins the fidelity ladder and promotion audits.

Across these 31 papers, the leading evidence profiles are empirical/experimental evidence (24), optimization/search study (22), simulation/numerical evidence (15), dataset/benchmark (14), control/learning study (12), physical-test evidence (7), review/synthesis (6), mathematical/formal evidence (5). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Implement descriptor-versioned archives and report archive coverage, QD score, feasible coverage, and descriptor occupancy separately.
- Use registered multifidelity promotion with stratified proxy audits and `not_estimable` outcomes for unresolved high-fidelity labels.
- Budget-match QD, objective optimization, random search, and fixed-topology baselines across seeds.

**Per-paper reports and principal takeaways**
- [QD-001: Illuminating search spaces by mapping elites](by_paper/QD-001_review.md) — MAP-Elites: keeps the best design per behaviour cell; the base algorithm of the executable morphology archive (Work 099).
- [QD-002: Quality Diversity: A New Frontier for Evolutionary Computation](by_paper/QD-002_review.md) — Defines quality diversity and separates coverage, novelty and quality; vocabulary for the design-diversity contract (Work 090).
- [QD-003: Data-Efficient Design Exploration through Surrogate-Assisted Illumination](by_paper/QD-003_review.md) — **deep review** — The paper reports hundreds of diverse high-performing designs with orders-of-magnitude fewer evaluations than MAP-Elites or CMA-ES in the 2-D task, and demonstrates high-performing illumination maps in the 3-D task (p. 1). UCB sampling improves accuracy around high-fitness regions relative to uniform or variance-only sampling (p. 13).
- [QD-004: Covariance Matrix Adaptation MAP-Annealing](by_paper/QD-004_review.md) — CMA-MAE improves continuous QD search; a stronger continuous-parameter baseline once basic MAP-Elites works.
- [QD-005: Survey of multifidelity methods in uncertainty propagation, inference, and optimization](by_paper/QD-005_review.md) — The reference for combining cheap and expensive models without trusting the cheap one; underpins the fidelity ladder and promotion audits.
- [QD-006: Multi-fidelity Bayesian Optimisation with Continuous Approximations](by_paper/QD-006_review.md) — BOCA chooses both candidate and fidelity by cost; relevant when mesh size or time step is a controllable fidelity.
- [QD-007: Crossing the Reality Gap: a Short Introduction to the Transferability Approach](by_paper/QD-007_review.md) — Learns which simulated behaviours transfer to reality and optimises for transferability; a model for promotion-aware selection.
- [QD-009: Abandoning Objectives: Evolution Through the Search for Novelty Alone](by_paper/QD-009_review.md) — Novelty search escapes deceptive objectives; relevant when race time alone traps search in conventional layouts.
- [QD-011: Using Centroidal Voronoi Tessellations to Scale Up the Multidimensional Archive of Phenotypic Elites Algorithm](by_paper/QD-011_review.md) — CVT-MAP-Elites keeps archive size fixed in high-dimensional descriptor spaces; needed if vehicle descriptors grow.
- [QD-012: Covariance Matrix Adaptation for the Rapid Illumination of Behavior Space](by_paper/QD-012_review.md) — CMA-ME: CMA-ES emitters inside MAP-Elites; a standard QD comparator.
- [QD-013: pyribs: A Bare-Bones Python Library for Quality Diversity Optimization](by_paper/QD-013_review.md) — Reference QD library with archives and emitters; a tested implementation to cross-check our archive code.
- [QD-014: Accelerated Quality-Diversity through Massive Parallelism](by_paper/QD-014_review.md) — QDax: QD on accelerators with large batches; relevant to compute-ledger comparisons of batch size and evaluations.
- [QD-015: Multi-Objective Quality Diversity Optimization](by_paper/QD-015_review.md) — MOME keeps a Pareto front per cell; fits H2's race time/energy/mass/reliability trade-offs inside a diverse archive.
- [QD-016: Quality Diversity for Multi-task Optimization](by_paper/QD-016_review.md) — One search solving many related tasks with shared elites; maps directly onto one design search across many race environments.
- [QD-017: Multi-Task Multi-Behavior MAP-Elites](by_paper/QD-017_review.md) — Extends multi-task QD to diverse behaviours per task; relevant to environment-specialised archives (H3).
- [QD-018: BOP-Elites, a Bayesian Optimisation algorithm for Quality-Diversity search](by_paper/QD-018_review.md) — Bayesian optimisation for QD with very few evaluations; relevant when each evaluation is a CFD or FE run.
- [QD-019: Designing Air Flow with Surrogate-assisted Phenotypic Niching](by_paper/QD-019_review.md) — Surrogate-assisted QD for air-flow design with phenotypic niching; direct method for diverse aero/cooling geometry.
- [QD-020: Prototype Discovery using Quality-Diversity](by_paper/QD-020_review.md) — Clusters a QD archive into prototypes for human review; useful for summarising which architecture families emerged.
- [QD-021: Robots that can adapt like animals](by_paper/QD-021_review.md) — A precomputed MAP-Elites archive is reused for fast recovery after damage; a pattern for reusing archives under degraded conditions.
- [QD-022: Open-ended search for environments and adapted agents using MAP-Elites](by_paper/QD-022_review.md) — MAP-Elites over environments and agents together; relevant to curricula over tracks and conditions.
- [QD-023: The CMA Evolution Strategy: A Tutorial](by_paper/QD-023_review.md) — Authoritative CMA-ES tutorial; the default continuous optimiser for tuned fixed-topology baselines.
- [QD-025: Practical Bayesian Optimization of Machine Learning Algorithms](by_paper/QD-025_review.md) — Practical Gaussian-process Bayesian optimisation including cost-aware acquisition; a baseline for expensive parameter tuning.
- [QD-026: A Tutorial on Bayesian Optimization](by_paper/QD-026_review.md) — Clear tutorial of Bayesian optimisation including multi-fidelity and noisy settings.
- [QD-027: Scalable Global Optimization via Local Bayesian Optimization](by_paper/QD-027_review.md) — TuRBO trust-region Bayesian optimisation for higher dimensions; a strong baseline for tuning conventional vehicles.
- [QD-028: Bayesian Optimization of Combinatorial Structures](by_paper/QD-028_review.md) — BOCS handles discrete, combinatorial design variables; relevant to discrete topology choices.
- [QD-029: Multi-fidelity optimization via surrogate modelling](by_paper/QD-029_review.md) — Co-kriging multi-fidelity surrogate optimisation with an aerodynamic example; the classic engineering formulation.
- [QD-032: A composite neural network that learns from multi-fidelity data: Application to function approximation and inverse PDE problems](by_paper/QD-032_review.md) — Neural multi-fidelity model; an alternative to Gaussian processes at larger data sizes.
- [QD-033: Efficient Global Optimization of Expensive Black-Box Functions](by_paper/QD-033_review.md) — EGO and expected improvement; the foundation of surrogate-based optimisation of expensive simulations.
- [QD-034: Dominated Novelty Search: Rethinking Local Competition in Quality-Diversity](by_paper/QD-034_review.md) — Replaces grid archives with competition-based fitness transformation; an archive-free QD alternative for unbounded descriptor spaces.
- [QD-035: Aerodynamic Design Exploration through Surrogate-Assisted Illumination](by_paper/QD-035_review.md) — The aerodynamic application paper of SAIL, with 2D airfoil CFD; closest to diverse aero-surface search.
- [QD-036: Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations](by_paper/QD-036_review.md) — Physics-informed neural networks; a surrogate family that embeds governing equations, relevant when data is scarce.

## CAD: CAD, B-rep and assembly representation, generation and datasets

**Scope:** How solid models, construction sequences, joints and assemblies are represented, learned and generated, plus the public CAD datasets. Relevant to the parametric/freeform B-rep grammars, semantic geometry witnesses, joint kernel and part-resolution work (Works 078-096, 135-142).

**Cross-paper findings**
- CAD generation must preserve construction semantics, topology, constraints, and editability; image similarity or point-cloud proximity misses functional defects.
- B-rep and assembly learning depend on explicit face-edge-loop and mating relationships, not unordered geometry alone.
- Execution-guided and verifier-guided generation improves validity, but does not replace tolerance, interference, material, or load-path evidence.

**What is especially interesting**

- [CAD-003](by_paper/CAD-003_review.md): Learns directly on B-rep face/edge/coedge topology; candidate descriptor for mechanically meaningful diversity measures.
- [CAD-013](by_paper/CAD-013_review.md): Equivalent labels materially raise measured accuracy (p. 22), showing that assembly evaluation must distinguish genuine geometric equivalence from forgiving an incorrect mate.
- [CAD-018](by_paper/CAD-018_review.md): Argues learned models must see a canonical solid, not file-order artefacts; the same concern as our deterministic geometry identity and hashing.

Across these 30 papers, the leading evidence profiles are dataset/benchmark (29), empirical/experimental evidence (22), physical-test evidence (9), optimization/search study (8), control/learning study (8), simulation/numerical evidence (6), review/synthesis (5), mathematical/formal evidence (1), technical/methodological study (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Extend the Work 138 geometry-general evaluator with semantic topology, constraint, editability, and assembly-mate checks.
- Maintain exact geometry-to-mesh-to-reduced-model revision identity and quantify every adapter discrepancy.
- Score generated CAD on physical and manufacturing tasks, not render similarity.

**Per-paper reports and principal takeaways**
- [CAD-001: DeepCAD: A Deep Generative Network for Computer-Aided Design Models](by_paper/CAD-001_review.md) — Generates sketch-and-extrude construction sequences; a proposal representation whose outputs still need our load-path and process gates.
- [CAD-002: Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts](by_paper/CAD-002_review.md) — Text to CAD sequences with graded prompt levels; a data and evaluation reference for language-to-geometry proposals.
- [CAD-003: BRepNet: A topological message passing system for solid models](by_paper/CAD-003_review.md) — Learns directly on B-rep face/edge/coedge topology; candidate descriptor for mechanically meaningful diversity measures.
- [CAD-004: Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences](by_paper/CAD-004_review.md) — Human CAD construction sequences plus a reconstruction environment; data for learning realistic part-construction priors.
- [CAD-005: DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation](by_paper/CAD-005_review.md) — Implicit signed-distance shape representation; an option for smooth body surfaces, with meshing and feature-tolerance obligations.
- [CAD-006: ABC: A Big CAD Model Dataset For Geometric Deep Learning](by_paper/CAD-006_review.md) — One million B-rep models with parametric curves and surfaces; a benchmark source for geometry-kernel robustness tests.
- [CAD-007: UV-Net: Learning from Boundary Representations](by_paper/CAD-007_review.md) — Samples B-rep faces and edges on their UV domains for learning; a practical B-rep encoder for surrogates on native geometry.
- [CAD-008: SolidGen: An Autoregressive Model for Direct B-rep Synthesis](by_paper/CAD-008_review.md) — Direct B-rep synthesis with indexed boundary representation; shows how to generate valid topology without a construction history.
- [CAD-009: SkexGen: Autoregressive Generation of CAD Construction Sequences with Disentangled Codebooks](by_paper/CAD-009_review.md) — Disentangles topology and geometry codes in CAD sequences; relevant to separating structural choices from dimensions in the genome.
- [CAD-010: Hierarchical Neural Coding for Controllable CAD Model Generation](by_paper/CAD-010_review.md) — Hierarchical codes for loops, profiles and solids; enables controlled partial edits, analogous to local mutation of a part.
- [CAD-011: BrepGen: A B-rep Generative Diffusion Model with Structured Latent Geometry](by_paper/CAD-011_review.md) — Diffusion over a structured latent B-rep tree including freeform surfaces; a candidate generator for freeform solids (Work 092).
- [CAD-012: ComplexGen: CAD Reconstruction by B-Rep Chain Complex Generation](by_paper/CAD-012_review.md) — Reconstructs B-rep as a chain complex with explicit topological constraints; relevant to topology-consistency checks.
- [CAD-013: JoinABLe: Learning Bottom-up Assembly of Parametric CAD Joints](by_paper/CAD-013_review.md) — **deep review** — The reported joint-axis accuracy is 79.53%, close to the 80% human result and above the tested baselines (p. 1). Performance is higher for hole-based joints; edge length and entity type are important features, while face area can hurt (results appendix, pp. 22-25).
- [CAD-014: AutoMate: A Dataset and Learning Approach for Automatic Mating of CAD Assemblies](by_paper/CAD-014_review.md) — Large dataset of real CAD mates and a B-rep mate predictor; data for testing whether generated interfaces resemble real mechanical mates.
- [CAD-015: Assemble Them All: Physics-Based Planning for Generalizable Assembly by Disassembly](by_paper/CAD-015_review.md) — Physics-based disassembly planning proves an assembly can be put together; a buildability gate for generated multi-part vehicles.
- [CAD-016: ASAP: Automated Sequence Planning for Complex Robotic Assembly with Physical Feasibility](by_paper/CAD-016_review.md) — Assembly-sequence planning with gravity and stability checks; relevant to manufacturing handoff (Work 130).
- [CAD-017: Geometric Deep Learning for Computer-Aided Design: A Survey](by_paper/CAD-017_review.md) — Survey of learning on CAD data (B-rep, sequences, assemblies); a map of available methods and datasets.
- [CAD-018: Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations](by_paper/CAD-018_review.md) — Argues learned models must see a canonical solid, not file-order artefacts; the same concern as our deterministic geometry identity and hashing.
- [CAD-019: TG-Diff: Coupling Discrete Topology Diffusion and Topology-conditioned Geometry Diffusions for B-Rep Generation](by_paper/CAD-019_review.md) — Generates B-rep topology first then geometry; mirrors the topology-then-dimensions split in our genome.
- [CAD-020: HiFi-BRep: High-Fidelity Latent Representation for Robust B-Rep Generation](by_paper/CAD-020_review.md) — Targets robustness of generated B-rep (watertightness, valid solids); relevant to constructive validity gates (Work 095).
- [CAD-021: CADENA: Stepwise CAD Reverse Engineering](by_paper/CAD-021_review.md) — Stepwise recovery of editable CAD from geometry; useful for turning evolved meshes or fields back into editable parts.
- [CAD-022: HoLa: B-Rep Generation using a Holistic Latent Representation](by_paper/CAD-022_review.md) — Single latent space for B-rep geometry and topology; a follow-up to BrepGen for freeform solid proposals.
- [CAD-023: AutoBrep: Autoregressive B-Rep Generation with Unified Topology and Geometry](by_paper/CAD-023_review.md) — Autoregressive B-rep generation with unified topology and geometry tokens; alternative generator with sequence-level control.
- [CAD-025: DTGBrepGen: A Novel B-rep Generative Model through Decoupling Topology and Geometry](by_paper/CAD-025_review.md) — Decouples topology and geometry generation for B-rep; another data point on validity versus diversity.
- [CAD-026: CAD-MLLM: Unifying Multimodality-Conditioned CAD Generation With MLLM](by_paper/CAD-026_review.md) — Multimodal (text, image, point cloud) conditioned CAD generation; relevant to conditioning part proposals on interface geometry.
- [CAD-027: FlexCAD: Unified and Versatile Controllable CAD Generation with Fine-tuned Large Language Models](by_paper/CAD-027_review.md) — LLM-based controllable CAD editing at different hierarchy levels; analogous to hierarchical mutation operators.
- [CAD-028: GenCAD: Image-Conditioned Computer-Aided Design Generation with Transformer-Based Contrastive Representation and Diffusion Priors](by_paper/CAD-028_review.md) — Image-conditioned CAD programme generation; another proposal route that must still pass physical gates.
- [CAD-029: Self-Supervised Representation Learning for CAD](by_paper/CAD-029_review.md) — Self-supervised B-rep embeddings trained without labels; useful descriptors when labelled engineering data is scarce.
- [CAD-033: KDH-CAD: Knowledge-data hybrid CAD learning under data scarcity](by_paper/CAD-033_review.md) — Combines engineering knowledge with scarce CAD data; relevant because vehicle-part data is small and proprietary.
- [CAD-034: MatchMaker: Automated Asset Generation for Robotic Assembly](by_paper/CAD-034_review.md) — Generates mating part pairs with clearance for assembly; relevant to interface clearance and fit generation.

## ST: Topology optimisation, meshing, finite elements, contact and failure numerics

**Scope:** Methods that turn admitted geometry into solved fields and failure states: structural topology optimisation, robust tetrahedral meshing, element verification problems, frictional contact, fracture and fatigue damage models. The Work 102 review ranks independent geometry-to-field evaluation as the top gap.

**Cross-paper findings**
- Structural credibility depends on equilibrium, discretization, constitutive assumptions, contact treatment, and convergence rather than a single stress scalar.
- Topology optimization can create useful material layouts, but filters, length scales, manufacturing constraints, and mesh dependence strongly shape the result.
- Robust contact methods treat penetration, friction, solver failure, and non-convergence as observable outcomes.

**What is especially interesting**

- [ST-011](by_paper/ST-011_review.md): The mesher of the geometry-mesh bridge (Work 110); read with its documentation before trusting mesh quality settings.
- [ST-015](by_paper/ST-015_review.md): The paper treats missed collision and infeasible linearized constraints as numerical failures rather than hiding them with non-physical fail-safes (pp. 5, 7).
- [ST-016](by_paper/ST-016_review.md): Extends IPC to curved high-order meshes; relevant once CAD-conforming meshes are used.

Across these 9 papers, the leading evidence profiles are simulation/numerical evidence (9), dataset/benchmark (6), optimization/search study (3), mathematical/formal evidence (2), physical-test evidence (2), control/learning study (2), review/synthesis (1), empirical/experimental evidence (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Promote only field solutions with independently recovered reactions, residual histories, failure locations, and at least three registered refinement levels.
- Add contact/mesh failure taxonomies and prevent geometry healing from silently changing candidate identity.
- Carry manufacturing length scales and uncertainty into structural search instead of applying them after optimization.

**Per-paper reports and principal takeaways**
- [ST-003: Efficient topology optimization in MATLAB using 88 lines of code](by_paper/ST-003_review.md) — Faster, filtered successor to the 99-line code; the practical reference implementation for a 2D structural baseline.
- [ST-004: Giga-voxel computational morphogenesis for structural design](by_paper/ST-004_review.md) — Topology optimisation of a full aircraft wing at billion-voxel resolution discovered non-conventional internal structure; closest structural analogue to whole-part discovery.
- [ST-008: An efficient 3D topology optimization code written in Matlab](by_paper/ST-008_review.md) — Compact 3D topology optimisation reference; a 3D structural baseline for part-level comparisons.
- [ST-009: Current and future trends in topology optimization for additive manufacturing](by_paper/ST-009_review.md) — Reviews manufacturing constraints (overhang, minimum feature, support) in topology optimisation; inputs for the manufacturing language.
- [ST-011: Gmsh: A 3-D finite element mesh generator with built-in pre- and post-processing facilities](by_paper/ST-011_review.md) — The mesher of the geometry-mesh bridge (Work 110); read with its documentation before trusting mesh quality settings.
- [ST-012: Fast Tetrahedral Meshing in the Wild](by_paper/ST-012_review.md) — fTetWild meshes arbitrary, imperfect triangle soups robustly; a fallback when generated CAD is not clean enough for CAD-based meshing.
- [ST-015: Incremental Potential Contact: Intersection- and Inversion-free, Large-Deformation Dynamics](by_paper/ST-015_review.md) — **deep review** — The method produces intersection- and inversion-free trajectories across the reported examples and permits independent dynamics and surface-conformation tolerances (p. 1). Resolution raises contact count, iteration count, memory roughly linearly, and timing slightly superlinearly in the mat study (p. 16).
- [ST-016: High-Order Incremental Potential Contact for Elastodynamic Simulation on Curved Meshes](by_paper/ST-016_review.md) — Extends IPC to curved high-order meshes; relevant once CAD-conforming meshes are used.
- [ST-018: Affine Body Dynamics: Fast, Stable & Intersection-free Simulation of Stiff Materials](by_paper/ST-018_review.md) — Stiff bodies as affine deformations with IPC contact; a fast option for many-part assemblies.

## SI: Simulation, optimal-control and MDO infrastructure, coupling and integrators

**Scope:** Engines, solvers and modelling languages the project could adopt or cross-check against: multibody dynamics, differentiable simulation, co-simulation coupling, acausal energy-port modelling, structure-preserving integrators and nonlinear-programming solvers used for minimum-time problems.

**Cross-paper findings**
- Fast differentiable and GPU simulators enable co-design scale, but gradient availability is not evidence of model applicability.
- Contact, deformables, rigid bodies, and multiphysics each impose different numerical failure modes and validation duties.
- Simulator benchmarks are meaningful only with disclosed hardware, tolerances, time-step sensitivity, and accuracy-cost trade-offs.

**What is especially interesting**

- [SI-001](by_paper/SI-001_review.md): Differentiable simulation language; a route to gradient refinement inside an admitted topology, with the caveat that gradients do not prove accuracy.
- [SI-006](by_paper/SI-006_review.md): Partitioned multiphysics coupling (fluid-structure, conjugate heat) with convergence acceleration; relevant to coupled thermal-solid work (Work 115).
- [SI-020](by_paper/SI-020_review.md): The error signal is independently observable at the interface rather than constructed by negating a prescribed input, matching the project's need for transferred-energy evidence.

Across these 12 papers, the leading evidence profiles are simulation/numerical evidence (8), control/learning study (6), optimization/search study (5), mathematical/formal evidence (5), physical-test evidence (4), empirical/experimental evidence (4), review/synthesis (2), dataset/benchmark (2). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Create evaluator applicability records per candidate class and treat solver/gradient failure as first-class ledger outcomes.
- Benchmark runtime together with solution error, conservation residuals, and stability across time-step and mesh refinement.
- Use differentiable solvers for local refinement only inside validated domains; retain discrete topology search outside them.

**Per-paper reports and principal takeaways**
- [SI-001: DiffTaichi: Differentiable Programming for Physical Simulation](by_paper/SI-001_review.md) — Differentiable simulation language; a route to gradient refinement inside an admitted topology, with the caveat that gradients do not prove accuracy.
- [SI-005: OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization](by_paper/SI-005_review.md) — Coupled-analysis orchestration with derivatives; a pattern for design/control/energy/structure coupling.
- [SI-006: preCICE v2: A sustainable and user-friendly coupling library](by_paper/SI-006_review.md) — Partitioned multiphysics coupling (fluid-structure, conjugate heat) with convergence acceleration; relevant to coupled thermal-solid work (Work 115).
- [SI-007: DOLFINx: The next generation FEniCS problem solving environment](by_paper/SI-007_review.md) — Open finite-element environment; candidate independent solver for geometry-general evaluation (Work 138).
- [SI-009: Brax: A Differentiable Physics Engine for Large Scale Rigid Body Simulation](by_paper/SI-009_review.md) — Massively parallel accelerator physics; relevant to the compute ledger when comparing search algorithms by wall time.
- [SI-010: Dojo: A Differentiable Physics Engine for Robotics](by_paper/SI-010_review.md) — Differentiable contact via interior-point complementarity; a gradient-through-contact option for ground interaction.
- [SI-011: A pressure field model for fast, robust approximation of net contact force and moment between nominally rigid objects](by_paper/SI-011_review.md) — Hydroelastic contact giving distributed pressure rather than point forces; relevant to contact patches of arbitrary ground-contact endpoints.
- [SI-012: Discrete mechanics and variational integrators](by_paper/SI-012_review.md) — Structure-preserving integrators with bounded energy error; the theory behind treating energy residuals as observable outputs.
- [SI-017: CasADi: a software framework for nonlinear optimization and optimal control](by_paper/SI-017_review.md) — The standard open tool for direct-collocation minimum-lap-time problems; needed for optimised driver baselines.
- [SI-018: On the implementation of an interior-point filter line-search algorithm for large-scale nonlinear programming](by_paper/SI-018_review.md) — IPOPT, the NLP solver used by most published minimum-lap-time work; know its convergence behaviour before trusting a lap.
- [SI-020: Energy conservation and power bonds in co-simulations: non-iterative adaptive step size control and error estimation](by_paper/SI-020_review.md) — **deep review** — In a reported linear benchmark, residual-energy-based adaptation reduces residual energy by about 90%; alternative system partitioning produces larger errors, showing that coupling topology itself matters (pp. 10-11).
- [SI-021: Co-simulation: State of the art](by_paper/SI-021_review.md) — Survey of co-simulation orchestration, stability and accuracy; background for coupling many subsystem models.

## LT: Minimum-lap-time optimal control, vehicle dynamics, tracks and design/control co-optimisation

**Scope:** How race vehicles are driven optimally and how design parameters are optimised together with that driving. This is the evaluator side of the project: an unconventional vehicle can only be judged fairly with an optimised driver on a spatial track.

**Cross-paper findings**
- Minimum-lap-time optimization couples vehicle states, controls, path constraints, tyre limits, and power/energy constraints; isolated peak metrics are poor substitutes.
- Simultaneous design and control optimization changes the preferred hardware because the controller can exploit or expose component trade-offs.
- Numerical transcription, scaling, initialization, and constraint enforcement materially affect whether a computed lap is credible.

**What is especially interesting**

- [LT-001](by_paper/LT-001_review.md): Minimum-lap-time control with vehicle parameters as optimisation variables; the template for design/driver fairness.
- [LT-005](by_paper/LT-005_review.md): Aero and suspension cannot be optimized as independent peak metrics: the controller changes ride and roll along the lap, moving the aero operating point.
- [LT-032](by_paper/LT-032_review.md): Recent efficient free-trajectory lap-time optimisation; relevant to the cost of giving every candidate an optimised driver.

Across these 11 papers, the leading evidence profiles are control/learning study (11), simulation/numerical evidence (7), empirical/experimental evidence (6), optimization/search study (1), mathematical/formal evidence (1), physical-test evidence (1), dataset/benchmark (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Replace disconnected subsystem scores with a coupled transient lap objective that preserves tyre, energy, thermal, brake, and stability constraints.
- Audit optimal-control feasibility by replaying controls in an independently configured forward simulation.
- Compare co-design against separately optimized fixed-topology baselines under the same track, energy profile, seeds, and compute.

**Per-paper reports and principal takeaways**
- [LT-001: Optimal control for a Formula One car with variable parameters](by_paper/LT-001_review.md) — Minimum-lap-time control with vehicle parameters as optimisation variables; the template for design/driver fairness.
- [LT-002: Optimal control of a Formula One car on a three-dimensional track-part 1: track modeling and identification](by_paper/LT-002_review.md) — Builds and identifies a 3D track ribbon (curvature, elevation, banking) from data; the guide for replacing our synthetic tracks.
- [LT-004: Minimum time optimal control simulation of a GP2 race car](by_paper/LT-004_review.md) — 14-DOF car, nonlinear tyres, ride-height aero and telemetry comparison; the nearest public coupled-model target.
- [LT-005: Optimizing the aero-suspension interactions in a Formula One car](by_paper/LT-005_review.md) — **deep review** — Reported surrogate errors are at most 0.147 mm in front ride height and 0.038 degrees in roll over the tested mesh. Including steer and sideslip aero sensitivities raises the reported lap time to 83.45 s, and lower high-speed ride height gains downforce while roll degrades it (pp. 6, 11).
- [LT-010: A Curvilinear Abscissa Approach for the Lap Time Optimization of Racing Vehicles](by_paper/LT-010_review.md) — Curvilinear-coordinate formulation used by most modern lap-time solvers; needed to pose our track-relative dynamics.
- [LT-013: Online Time-Optimal Trajectory Planning on Three-Dimensional Race Tracks](by_paper/LT-013_review.md) — Point-mass time-optimal planning on 3D tracks with open code; a cheap lower-fidelity rung of the ladder.
- [LT-015: GripMap: An Efficient, Spatially Resolved Constraint Framework for Offline and Online Trajectory Planning in Autonomous Racing](by_paper/LT-015_review.md) — Spatially resolved grip constraints for planning; a data structure for track-position-dependent grip.
- [LT-023: Minimum-lap-time Control Strategies for All-wheel Drive Electric Race Cars via Convex Optimization](by_paper/LT-023_review.md) — Per-tyre grip limits with all-wheel drive in a convex lap formulation; relevant to independent-wheel torque allocation.
- [LT-024: Time-optimal Design and Control of Electric Race Cars Equipped with Multi-speed Transmissions](by_paper/LT-024_review.md) — Compares fixed, CVT and multi-speed transmissions with jointly optimised control; an architecture choice evaluated fairly.
- [LT-025: Time-optimal Control Strategies for Electric Race Cars with Different Transmission Technologies](by_paper/LT-025_review.md) — Earlier transmission-technology comparison under time-optimal control; precedent for architecture comparison at equal control effort.
- [LT-032: A Sequential Convex Programming Approach to Free-trajectory Minimum-lap-time Optimization of Racing Cars](by_paper/LT-032_review.md) — Recent efficient free-trajectory lap-time optimisation; relevant to the cost of giving every candidate an optimised driver.

## EN: Race energy management, powertrain architecture and energy storage

**Scope:** Energy-limited racing strategy, hybrid and electric powertrain control, powertrain topology synthesis, and the models and measured data for batteries, flywheels and supercapacitors. Supports the carried-energy race contract, the typed energy graph and onboard energy realisation (Work 120).

**Cross-paper findings**
- Usable race energy is constrained by power limits, efficiency maps, temperature, state of charge, degradation, and containment mass, not nominal joules alone.
- Optimal energy management is trajectory-dependent and coupled to lap time, thermal state, and component sizing.
- Equivalent comparisons need complete carrier, conversion, cooling, and recovery accounting with observable losses.

**What is especially interesting**

- [EN-012](by_paper/EN-012_review.md): The paper does not show a generic architecture-ranking reversal; it shows a narrower fidelity split: simple models may suffice for sizing, but not for interpreting optimal energy-control trajectories.
- [EN-016](by_paper/EN-016_review.md): Co-design of electric propulsion components and control; method for sizing components within a chosen topology.
- [EN-030](by_paper/EN-030_review.md): Stochastic hybrid energy strategy accounting for competitors; relevant if race time depends on interaction, not only on the lone vehicle.

Across these 15 papers, the leading evidence profiles are control/learning study (9), simulation/numerical evidence (6), mathematical/formal evidence (6), empirical/experimental evidence (5), dataset/benchmark (3), review/synthesis (3), technical/methodological study (2), physical-test evidence (2). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Implement stateful storage and converter maps with power, temperature, degradation, and failure bounds in the Work 120 energy realization.
- Make the race-energy profile include containment, auxiliaries, cooling, and recovery provenance.
- Optimize energy management jointly with trajectory and sizing, then replay the full balance independently.

**Per-paper reports and principal takeaways**
- [EN-007: Low-level Online Control of the Formula 1 Power Unit with Feedforward Cylinder Deactivation](by_paper/EN-007_review.md) — Online F1 power-unit control; shows real-time constraints on energy strategies.
- [EN-009: Maximum-distance Race Strategies for a Fully Electric Endurance Race Car](by_paper/EN-009_review.md) — Endurance strategy under fixed energy with pit decisions; relevant to race-long energy budgeting.
- [EN-010: Optimal Endurance Race Strategies for a Fully Electric Race Car under Thermal Constraints](by_paper/EN-010_review.md) — Adds battery and motor thermal limits to endurance strategy; a direct coupling of our thermal and energy gates.
- [EN-011: Human-in-the-loop Energy and Thermal Management for Electric Racing Cars through Optimization-based Control](by_paper/EN-011_review.md) — Optimisation-based energy and thermal guidance delivered to a human driver; relevant to realistic driver execution of optimal strategies.
- [EN-012: Battery model impact on time-optimal co-design for electric racing cars: review and application](by_paper/EN-012_review.md) — **deep review** — The simple model gives consistent battery-sizing results, while detailed models are needed to study credible control-variable evolution. For the detailed models, race-time difference between 24 and 25 parallel cells is negligible; convex relaxation can also yield non-physical energy-variable profiles (pp. 1-2, 9, 11).
- [EN-013: Minimum Race-Time Planning-Strategy for an Autonomous Electric Racecar](by_paper/EN-013_review.md) — Race-long energy and thermal planning for an electric racecar with open tooling; a public reference implementation.
- [EN-016: Joint Design and Control of Electric Vehicle Propulsion Systems](by_paper/EN-016_review.md) — Co-design of electric propulsion components and control; method for sizing components within a chosen topology.
- [EN-017: Python Battery Mathematical Modelling (PyBaMM)](by_paper/EN-017_review.md) — The battery modelling package already mirrored in private/materials/sources; the citation for its models and parameter sets.
- [EN-019: Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models](by_paper/EN-019_review.md) — Measured parameter set for an LG M50 cell (PyBaMM Chen2020); real cell data usable for an onboard battery model.
- [EN-020: An asymptotic derivation of a single particle model with electrolyte](by_paper/EN-020_review.md) — Derives SPMe as a controlled reduction of the DFN model; a principled low-fidelity battery rung.
- [EN-021: Lithium-ion battery degradation: how to model it](by_paper/EN-021_review.md) — Coupled degradation mechanisms in PyBaMM; relevant if race energy stores degrade over a stint or season.
- [EN-022: A continuum of physics-based lithium-ion battery models reviewed](by_paper/EN-022_review.md) — Reviews the hierarchy of physics-based cell models; a map for choosing battery fidelity per gate.
- [EN-023: Parameterization of a Physico-Chemical Model of a Lithium-Ion Battery: I. Determination of Parameters](by_paper/EN-023_review.md) — Measured Kokam cell parameters (PyBaMM Ecker2015); a second measured data set for cross-checking battery models.
- [EN-025: A non-academic perspective on the future of lithium-based batteries](by_paper/EN-025_review.md) — Industry-grounded figures on achievable cell energy density and cost; realistic bounds for energy-store candidates.
- [EN-030: Competitors-Aware Stochastic Lap Strategy Optimisation for Race Hybrid Vehicles](by_paper/EN-030_review.md) — Stochastic hybrid energy strategy accounting for competitors; relevant if race time depends on interaction, not only on the lone vehicle.

## TY: Tyres, rubber friction and tyre identification

**Scope:** Tyre force models, transient and thermal behaviour, wear and degradation, rubber friction physics, and identification from test or track data. Tyres/contact is a priority-A gap in the Work 102 review; the current kernel uses a friction envelope and a tanh slip route.

**Cross-paper findings**
- Tyre force depends on combined slip, normal load, camber, pressure, temperature, wear, speed, and road state; a fixed friction circle is only a bounded approximation.
- Transient relaxation and load transfer matter in racing manoeuvres, so steady-state maps alone can mis-rank a design.
- Model identification and uncertainty are central because tyre parameters are condition-specific and difficult to measure.

**What is especially interesting**

- [TY-006](by_paper/TY-006_review.md): How the FSAE TTC measured and distributes tyre data; the most accessible real racing-tyre data source to request.
- [TY-011](by_paper/TY-011_review.md): The experiment links manoeuvre design to uncertainty: ordinary accessible driving may not excite the parameters that a racing controller needs.
- [TY-012](by_paper/TY-012_review.md): Bayesian state-space tyre degradation estimated from real 2025 F1 lap times; data-driven degradation rates for race-length simulation.

Across these 5 papers, the leading evidence profiles are review/synthesis (4), control/learning study (4), physical-test evidence (3), empirical/experimental evidence (1), simulation/numerical evidence (1), optimization/search study (1), dataset/benchmark (1), mathematical/formal evidence (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Upgrade the ground-interaction contract to combined-slip transient force with load, temperature, wear, and validity envelopes.
- Calibrate against declared data and propagate tyre uncertainty into lap-time and safety margins.
- Retain the present simple model only as a low-fidelity gate with audited promotion error.

**Per-paper reports and principal takeaways**
- [TY-006: The Formula SAE Tire Test Consortium-Tire Testing and Data Handling](by_paper/TY-006_review.md) — How the FSAE TTC measured and distributes tyre data; the most accessible real racing-tyre data source to request.
- [TY-010: Tire Modeling and Friction Estimation](by_paper/TY-010_review.md) — Thesis on brush-type tyre models and friction estimation; a physical basis for combined-slip behaviour.
- [TY-011: Bayesian Optimization-based Tire Parameter and Uncertainty Estimation for Real-World Data](by_paper/TY-011_review.md) — **deep review** — The method estimates parameter distributions rather than one best fit and shows that excitation affects parameter accuracy. The paper also reports that tire-only parameter identification can perform worse than identifying the fuller model, warning against treating other vehicle parameters as known (pp. 2-3).
- [TY-012: A State-Space Approach to Modeling Tire Degradation in Formula 1 Racing](by_paper/TY-012_review.md) — Bayesian state-space tyre degradation estimated from real 2025 F1 lap times; data-driven degradation rates for race-length simulation.
- [TY-013: Extended Pacejka Tire Model for Enhanced Vehicle](by_paper/TY-013_review.md) — Extends the Pacejka model with additional effects for vehicle simulation; a comparator for tyre-model extensions.

## AE: Aerodynamics, CFD validation, aero datasets and neural surrogates

**Scope:** Race-car aerodynamic mechanisms (ground effect, wheels, wakes), experimentally anchored CFD cases, adjoint shape optimisation, open automotive CFD datasets, and neural surrogates with their out-of-distribution limits. Aero is an A/B gap: there is no validated geometry-to-aero-map route yet.

**Cross-paper findings**
- Vehicle aerodynamics is geometry-, attitude-, wheel-, ground-, and flow-condition-dependent; isolated scalar coefficients hide spatial loads and balance shifts.
- Open CFD and experimental datasets can support surrogates and validation, but their geometry and Reynolds-number domains constrain transfer.
- Shape optimization needs drag, downforce, balance, cooling flow, sensitivity, and uncertainty together rather than one coefficient.

**What is especially interesting**

- [AE-002](by_paper/AE-002_review.md): A visually plausible lower-resolution field gives the wrong load trend, so aero validation must include resolution and averaging-time sensitivity, not only one coefficient snapshot.
- [AE-007](by_paper/AE-007_review.md): Benchmarks surrogate accuracy, physical consistency, cost and uncertainty including unseen categories; the evaluation protocol for any aero surrogate we use.
- [AE-024](by_paper/AE-024_review.md): Measures surrogate failure and adaptation on new vehicle families; directly relevant because novel architectures are out of distribution.

Across these 22 papers, the leading evidence profiles are simulation/numerical evidence (20), dataset/benchmark (18), empirical/experimental evidence (17), physical-test evidence (8), optimization/search study (7), review/synthesis (5), control/learning study (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Add geometry-derived aero surfaces/fields with ride-height, yaw, wheel, and ground-effect sweeps to Work 121 and the coupled vehicle model.
- Use public datasets for pipeline validation and pretraining, then hold out project-specific geometries and conditions for independent tests.
- Promote aero surrogates only with uncertainty and periodic CFD/experimental audits.

**Per-paper reports and principal takeaways**
- [AE-002: Spectral/hp element simulation of flow past a Formula One front wing: validation against experiments](by_paper/AE-002_review.md) — **deep review** — The third-order case is under-resolved. The fifth-order case best matches experimental reattachment and flow features; its downforce is 4.5% above the fourth-order case, and its lift stabilizes only late in the averaging window (pp. 8, 16).
- [AE-004: Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design](by_paper/AE-004_review.md) — Open CFD and adjoint design suite; an independent second solver for aero cross-checks.
- [AE-005: DrivAerNet: A Parametric Car Dataset for Data-Driven Aerodynamic Design and Prediction](by_paper/AE-005_review.md) — Thousands of parametric car CFD results; training/validation data for drag surrogates, limited to road-car shapes.
- [AE-006: DrivAerNet++: A Large-Scale Multimodal Car Dataset with Computational Fluid Dynamics Simulations and Deep Learning Benchmarks](by_paper/AE-006_review.md) — 8,000+ multimodal car CFD cases with benchmarks; the largest open automotive aero dataset.
- [AE-007: CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics](by_paper/AE-007_review.md) — Benchmarks surrogate accuracy, physical consistency, cost and uncertainty including unseen categories; the evaluation protocol for any aero surrogate we use.
- [AE-008: DrivAerML: High-Fidelity Computational Fluid Dynamics Dataset for Road-Car External Aerodynamics](by_paper/AE-008_review.md) — 500 DrivAer variants with hybrid RANS-LES at 160M cells, open licence; high-fidelity reference data for surrogate validation.
- [AE-009: AhmedML: High-Fidelity Computational Fluid Dynamics Dataset for Incompressible, Low-Speed Bluff Body Aerodynamics](by_paper/AE-009_review.md) — 500 Ahmed-body variants with hybrid RANS-LES; a simpler bluff-body benchmark for testing aero pipelines.
- [AE-010: WindsorML: High-Fidelity Computational Fluid Dynamics Dataset For Automotive Aerodynamics](by_paper/AE-010_review.md) — Wall-modelled LES of Windsor-body variants (CC-BY-SA); open high-fidelity data including ground proximity.
- [AE-011: Ground Effect Aerodynamics of Race Cars](by_paper/AE-011_review.md) — Review of wings, diffusers and wheels in ground effect with experimental data; the physics of ride-height-dependent downforce.
- [AE-016: AB-UPT: Scaling Neural CFD Surrogates for High-Fidelity Automotive Aerodynamics Simulations via Anchored-Branched Universal Physics Transformers](by_paper/AE-016_review.md) — Scales neural surrogates to full high-fidelity car fields; a candidate surrogate architecture, with OOD caveats.
- [AE-017: Transolver: A Fast Transformer Solver for PDEs on General Geometries](by_paper/AE-017_review.md) — Physics-attention transformer for PDEs on arbitrary meshes including car aerodynamics; a general-geometry surrogate candidate.
- [AE-018: Geometry-Informed Neural Operator for Large-Scale 3D PDEs](by_paper/AE-018_review.md) — GINO predicts car surface pressure from geometry; an early neural-operator car-aero result to reproduce.
- [AE-019: Learning Mesh-Based Simulation with Graph Networks](by_paper/AE-019_review.md) — MeshGraphNets learns mesh-based physics including aerodynamics; the base of many geometry-general surrogates.
- [AE-021: Surrogate Modeling of Car Drag Coefficient with Depth and Normal Renderings](by_paper/AE-021_review.md) — Image-based drag surrogate with a large car CFD dataset; a cheap screening surrogate to compare against field surrogates.
- [AE-022: Faster by Design: Interactive Aerodynamics via Neural Surrogates Trained on Expert-Validated CFD](by_paper/AE-022_review.md) — Neural surrogates trained on expert-validated race-car CFD (including an LMP2 car); the closest race-car surrogate study.
- [AE-023: Multi-Granularity Conformal Prediction for Reliable Neural-Operator Automotive Aerodynamic Surrogates](by_paper/AE-023_review.md) — Conformal uncertainty bounds for aero surrogates; a way to attach calibrated error bars to surrogate-based promotion.
- [AE-024: Adapting Automotive Aerodynamics Surrogates to New Vehicle Families via Transfer Learning](by_paper/AE-024_review.md) — Measures surrogate failure and adaptation on new vehicle families; directly relevant because novel architectures are out of distribution.
- [AE-025: Towards a Foundation-Model Paradigm for Aerodynamic Prediction in Three-dimensional Design](by_paper/AE-025_review.md) — Foundation-model approach to 3D aero prediction; context for general-geometry surrogates.
- [AE-026: SMART: Scalable Mesh-free Aerodynamic Simulations from Raw Geometries using a Transformer-based Surrogate Model](by_paper/AE-026_review.md) — Mesh-free surrogate from raw geometry; avoids a meshing step for early screening.
- [AE-027: AirfRANS: High Fidelity Computational Fluid Dynamics Dataset for Approximating Reynolds-Averaged Navier-Stokes Solutions](by_paper/AE-027_review.md) — Airfoil RANS dataset with physics-consistency metrics; relevant to wing-element surrogates and evaluation of physical consistency.
- [AE-028: Adjoint methods for car aerodynamics](by_paper/AE-028_review.md) — Industrial adjoint shape and topology optimisation of car aerodynamics; the method for local aero improvement of admitted bodies.
- [AE-033: Fourier Neural Operator for Parametric Partial Differential Equations](by_paper/AE-033_review.md) — Neural operator learning solution maps of PDEs; the base architecture of many flow surrogates.

## TH: Thermal management, heat generation and cooling design

**Scope:** Heat-generation and thermal-network models for batteries and electric machines, and geometry-level cooling design. Supports the lumped thermal physics, coupled thermal-solid and flow/heat-exchange work (Works 014, 115, 121).

**Cross-paper findings**
- Thermal limits emerge from transient heat generation, storage, transfer, coolant/airflow, and control; a lumped steady temperature cannot establish race endurance.
- Cooling hardware costs mass, volume, pressure loss, parasitic power, and aerodynamic opportunity, so thermal design must be coupled to the vehicle objective.
- Reduced thermal models require calibrated envelopes and escalation when a candidate leaves them.

**What is especially interesting**

- [TH-001](by_paper/TH-001_review.md): Equal terminal temperature does not imply equal internal thermal mechanism, so a final-temperature check can hide incorrect heat-source provenance.
- [TH-004](by_paper/TH-004_review.md): Full 3D conjugate-heat-transfer topology optimisation producing non-intuitive heat sinks; a precedent for discovered cooling geometry.

Across these 2 papers, the leading evidence profiles are empirical/experimental evidence (1), mathematical/formal evidence (1), simulation/numerical evidence (1), optimization/search study (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Couple Work 115/121 thermal-solid and flow-heat models to storage, converter, brakes, aero ducts, and the full-stint finish gate.
- Track heat-source provenance, stored energy, boundary flux, coolant pumping, and rejected heat as one balance.
- Add thermal soak, repeated-lap, hot-ambient, blockage, and pump/fan-failure cases.

**Per-paper reports and principal takeaways**
- [TH-001: A General Energy Balance for Battery Systems](by_paper/TH-001_review.md) — **deep review** — The two mechanisms can reach the same final adiabatic-reversible temperature yet follow different heat-generation histories and slope changes. The common single-reaction balance is justified only when phase-change, mixing, and simultaneous-reaction effects are negligible (results/conclusion, pp. 7-9).
- [TH-004: Large scale three-dimensional topology optimisation of heat sinks cooled by natural convection](by_paper/TH-004_review.md) — Full 3D conjugate-heat-transfer topology optimisation producing non-intuitive heat sinks; a precedent for discovered cooling geometry.

## MA: Materials, material data, fasteners and joints, crash structures, manufacturing and tolerances

**Scope:** Where real material and joint behaviour comes from, and how manufacturing and tolerances constrain designs. The project picks catalog materials only (no new composition design); real material values stay in private/ under the material data policy.

**Cross-paper findings**
- Material and joint performance is process-, orientation-, surface-, temperature-, tolerance-, and load-history-dependent; a handbook scalar is not a universal constitutive law.
- Fatigue and reliability require distributions, damage accumulation, and failure modes, not only static factor of safety.
- Manufacturing feasibility must be tied to a declared process and inspection plan.

**What is especially interesting**

- [MA-003](by_paper/MA-003_review.md): The paper models process-structure-property linkage rather than composition alone, which matches the project's rule that material values depend on manufacturing history.
- [MA-012](by_paper/MA-012_review.md): GNoME's large-scale 'discovery' claim; paired with MA-013 as a case study in how discovery claims are challenged.

Across these 2 papers, the leading evidence profiles are dataset/benchmark (2), empirical/experimental evidence (2), simulation/numerical evidence (2), mathematical/formal evidence (1), review/synthesis (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Apply the material-data policy at every constitutive lookup and keep unsupported conditions as explicit unknowns.
- Extend Works 113/114/116/130 with joint preload, contact, tolerance, thermal, fatigue, and process-specific failure envelopes.
- Add specimen and assembly correlation before transferring a material/joint model to a complete vehicle.

**Per-paper reports and principal takeaways**
- [MA-003: Exploration of data science techniques to predict fatigue strength of steel from composition and processing parameters](by_paper/MA-003_review.md) — **deep review** — Several models reach R2 around 0.98 with reported error below 4%, improving earlier efforts and ranking predictive composition/process variables (pp. 1, 13-15).
- [MA-012: Scaling deep learning for materials discovery](by_paper/MA-012_review.md) — GNoME's large-scale 'discovery' claim; paired with MA-013 as a case study in how discovery claims are challenged.

## VV: Verification, validation, calibration, statistics, reproducibility and claim discipline

**Scope:** How to show a solver solves its equations, how to show a model predicts reality, how to compare stochastic search methods honestly, and how optimisers exploit objectives and simulators. Grounds the evidence tiers, fidelity gates and review discipline in AGENTS.md.

**Cross-paper findings**
- Verification asks whether equations were solved correctly; validation asks whether the equations represent reality for the intended use. Neither is replaced by passing software tests.
- Uncertainty, sensitivity, convergence, calibration/validation separation, and multiplicity control determine how strong a claim can be.
- Adaptive search and benchmark reuse create selection bias; untouched holdouts and append-only evidence are necessary for credible discovery claims.

**What is especially interesting**

- [VV-008](by_paper/VV-008_review.md): A code can be verified while its model is invalid for the application; equally, experimental agreement at one tier does not automatically validate a complete-system prediction.
- [VV-012](by_paper/VV-012_review.md): Power analysis for choosing seed counts; directly applicable to sizing paired-seed search campaigns.
- [VV-024](by_paper/VV-024_review.md): Taxonomy of data leakage that inflates results; applicable to held-out tracks and surrogate training data.

Across these 20 papers, the leading evidence profiles are empirical/experimental evidence (15), dataset/benchmark (13), physical-test evidence (10), review/synthesis (9), simulation/numerical evidence (9), control/learning study (7), optimization/search study (6), mathematical/formal evidence (5), technical/methodological study (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Turn the Validation Strategy into executable, domain-specific evidence gates with traceable intended-use statements.
- Require convergence, sensitivity/UQ, calibration/holdout separation, multiplicity-aware inference, and negative controls in every admitted study.
- Use claim templates that bind each conclusion to candidate, evaluator, dataset, fidelity, and uncertainty identities.

**Per-paper reports and principal takeaways**
- [VV-002: Bayesian calibration of computer models](by_paper/VV-002_review.md) — Kennedy-O'Hagan calibration with an explicit model-discrepancy term; the plan for calibrating subsystems against measurements.
- [VV-003: Deep Reinforcement Learning at the Edge of the Statistical Precipice](by_paper/VV-003_review.md) — Interval estimates and robust aggregates for few-run comparisons; the reporting standard for seed-limited search campaigns.
- [VV-008: Verification, validation, and predictive capability in computational engineering and physics](by_paper/VV-008_review.md) — **deep review** — Verification assesses accuracy in solving the computational model; validation assesses agreement with experimental reality for intended use. Validation requires numerical error, experimental uncertainty, and model discrepancy to remain distinct, and prediction outside the validation database requires weaker inference (pp. 3-4, 14, 21).
- [VV-012: How Many Random Seeds? Statistical Power Analysis in Deep Reinforcement Learning Experiments](by_paper/VV-012_review.md) — Power analysis for choosing seed counts; directly applicable to sizing paired-seed search campaigns.
- [VV-013: Deep Reinforcement Learning that Matters](by_paper/VV-013_review.md) — Shows seeds, implementations and hyperparameters can flip conclusions; motivates full replay metadata.
- [VV-014: Statistical Comparisons of Classifiers over Multiple Data Sets](by_paper/VV-014_review.md) — Non-parametric tests for comparing algorithms across many tasks; applicable to comparing search methods across circuits.
- [VV-015: Time for a Change: a Tutorial for Comparing Multiple Classifiers Through Bayesian Analysis](by_paper/VV-015_review.md) — Bayesian comparison with a region of practical equivalence; a way to say 'no practical difference' rather than 'not significant'.
- [VV-016: Benchmarking in Optimization: Best Practice and Open Issues](by_paper/VV-016_review.md) — Community best practice for benchmarking optimisers (budgets, baselines, reporting); a checklist for our campaign protocols.
- [VV-017: COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting](by_paper/VV-017_review.md) — Budget-based anytime performance comparison of optimisers; a model for reporting quality versus evaluations.
- [VV-019: Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)](by_paper/VV-019_review.md) — Reproducibility checklist and findings; complements the replay metadata requirement.
- [VV-020: Troubling Trends in Machine Learning Scholarship](by_paper/VV-020_review.md) — Catalogues overclaiming, speculation presented as explanation and ablation gaps; a reviewer's checklist for our own reports.
- [VV-021: The Surprising Creativity of Digital Evolution: A Collection of Anecdotes from the Evolutionary Computation and Artificial Life Research Communities](by_paper/VV-021_review.md) — Dozens of cases where evolution exploited simulator bugs and loopholes; the evidence behind treating numerical exploits as an alternative explanation.
- [VV-022: Concrete Problems in AI Safety](by_paper/VV-022_review.md) — Defines reward hacking and side effects; vocabulary for objective loopholes in design search.
- [VV-023: Defining and Characterizing Reward Hacking](by_paper/VV-023_review.md) — Formal definition of when a proxy objective is hackable; relevant to Level-0 race time as a proxy for real race time.
- [VV-024: Leakage and the reproducibility crisis in machine-learning-based science](by_paper/VV-024_review.md) — Taxonomy of data leakage that inflates results; applicable to held-out tracks and surrogate training data.
- [VV-025: The garden of forking paths: Why multiple comparisons can be a problem, even when there is no fishing expedition or p-hacking and the research hypothesis was posited ahead of time](by_paper/VV-025_review.md) — Data-dependent analysis choices inflate false positives even without intent; supports freezing analyses before results.
- [VV-028: Robot Learning from Randomized Simulations: A Review](by_paper/VV-028_review.md) — Reviews domain randomisation for sim-to-real; relevant to robustness across uncertain parameters.
- [VV-029: Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](by_paper/VV-029_review.md) — Randomising simulator parameters to transfer to reality; a robustness tactic for held-out conditions.
- [VV-031: A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](by_paper/VV-031_review.md) — Distribution-free prediction intervals for any surrogate; a simple way to bound surrogate error in promotion decisions.
- [VV-032: SALib: An open-source Python library for Sensitivity Analysis](by_paper/VV-032_review.md) — Global sensitivity analysis tooling (Sobol, Morris); for finding which parameters drive race-time rankings.

## AR: Autonomous racing control, learned drivers, real telemetry and race strategy

**Scope:** Controllers and learned drivers that can drive each candidate near its limit, public real-car racing data, model identification from track data, and race-level strategy simulation. A weak driver makes good mechanics look bad, so driver quality is part of fairness.

**Cross-paper findings**
- Racing performance requires perception, state estimation, prediction, planning, control, system identification, and safety to remain coupled at the limit.
- MPC and learning complement each other when learned components expose uncertainty and hard constraints remain enforceable.
- Real-track systems show that latency, localization faults, opponents, changing grip, and operational safety dominate beyond ideal simulation.

**What is especially interesting**

- [AR-003](by_paper/AR-003_review.md): The paper directly challenges the assumption that a globally 'better' model preserves controller rankings or closed-loop error behavior.
- [AR-012](by_paper/AR-012_review.md): Compares optimal control and RL for drone racing at the limit; evidence for choosing driver methods under model mismatch.
- [AR-022](by_paper/AR-022_review.md): Identifies tyre/vehicle models from about 30 s of driving data; a fast calibration route for physical correlation.

Across these 23 papers, the leading evidence profiles are dataset/benchmark (17), control/learning study (16), empirical/experimental evidence (11), physical-test evidence (11), simulation/numerical evidence (9), optimization/search study (4), review/synthesis (4), mathematical/formal evidence (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Use an optimized autonomous racing stack as a fair controller baseline before attributing gains to vehicle morphology.
- Add online identification, uncertainty-aware prediction, latency/fault injection, and opponent scenarios to held-out evaluation.
- Keep strategy decisions inside the same energy, tyre, thermal, and safety accounting as the vehicle design.

**Per-paper reports and principal takeaways**
- [AR-001: Outracing champion Gran Turismo drivers with deep reinforcement learning](by_paper/AR-001_review.md) — Learned driver beating top humans in a high-fidelity game; a method for strong per-design drivers, not physical validation.
- [AR-002: Optimization-Based Autonomous Racing of 1:43 Scale RC Cars](by_paper/AR-002_review.md) — Model predictive contouring control for racing; an implementable controller baseline with explicit horizon and actuator limits.
- [AR-003: Analyzing the Impact of Simulation Fidelity on the Evaluation of Autonomous Driving Motion Control](by_paper/AR-003_review.md) — **deep review** — Maximum lateral error alone discards important error structure, and retuning the baseline model for better approximation can disproportionately worsen lateral-error disparity (pp. 5-6). Model fidelity and controller-evaluation fidelity are therefore not monotonically equivalent.
- [AR-004: Autonomous Racing using Learning Model Predictive Control](by_paper/AR-004_review.md) — Iterative learning MPC improves lap time from previous laps; a controller that approaches each vehicle's limit.
- [AR-005: Autonomous Vehicles on the Edge: A Survey on Autonomous Vehicle Racing](by_paper/AR-005_review.md) — Survey of perception, planning, control and simulation in autonomous racing; a map of tools and datasets.
- [AR-006: Indy Autonomous Challenge - Autonomous Race Cars at the Handling Limits](by_paper/AR-006_review.md) — Full-scale autonomous racing at the handling limit with real vehicle behaviour; a reference for model-reality gaps at speed.
- [AR-007: TUM Autonomous Motorsport: An Autonomous Racing Software for the Indy Autonomous Challenge](by_paper/AR-007_review.md) — Complete open autonomous racing stack with planning and control; reusable components for a driver baseline.
- [AR-008: RACECAR -- The Dataset for High-Speed Autonomous Racing](by_paper/AR-008_review.md) — Open multi-sensor data from full-scale autonomous Indy cars up to 273 km/h including banked tracks; real data for vehicle-model validation.
- [AR-009: AMZ Driverless: The Full Autonomous Racing System](by_paper/AR-009_review.md) — Complete Formula Student driverless system with vehicle models and MPC; a well-documented reference implementation.
- [AR-011: Super-Human Performance in Gran Turismo Sport Using Deep Reinforcement Learning](by_paper/AR-011_review.md) — RL driver reaching super-human lap times in time trials; a learned-driver baseline method.
- [AR-012: Reaching the Limit in Autonomous Racing: Optimal Control versus Reinforcement Learning](by_paper/AR-012_review.md) — Compares optimal control and RL for drone racing at the limit; evidence for choosing driver methods under model mismatch.
- [AR-013: Champion-level drone racing using deep reinforcement learning](by_paper/AR-013_review.md) — Learned policy beating human champions in the real world with residual models from real data; an example of closing the sim-to-real gap.
- [AR-017: Towards Learning-Based Formula 1 Race Strategies](by_paper/AR-017_review.md) — Learning-based F1 strategy; recent context for race-level decision making.
- [AR-018: Game Theory in Formula 1: From Physical to Strategic Interactions](by_paper/AR-018_review.md) — Game-theoretic view of F1 interactions; relevant only if multi-car races enter the environment.
- [AR-019: Opponent State Inference Under Partial Observability: An HMM-POMDP Framework for 2026 Formula 1 Energy Strategy](by_paper/AR-019_review.md) — Models 2026-regulation energy strategy including Override Mode; context for the regulation profile our race contract pins.
- [AR-020: Bridging RL and MPC for mixed-integer optimal control with application to Formula 1 race strategies](by_paper/AR-020_review.md) — Combines RL and MPC for mixed-integer race strategy; relevant to discrete strategy choices.
- [AR-021: Mission Performance: Automatic and Adaptive Race Pace Progression for Autonomous Racing](by_paper/AR-021_review.md) — Adaptive pace progression towards the limit; relevant to safely finding each candidate's achievable pace.
- [AR-022: Learning-Based On-Track System Identification for Scaled Autonomous Racing in Under a Minute](by_paper/AR-022_review.md) — Identifies tyre/vehicle models from about 30 s of driving data; a fast calibration route for physical correlation.
- [AR-023: Deep Dynamics: Vehicle Dynamics Modeling with a Physics-Informed Neural Network for Autonomous Racing](by_paper/AR-023_review.md) — Physics-informed network that estimates interpretable vehicle parameters from data; a hybrid model-identification option.
- [AR-024: F1TENTH: An Open-source Evaluation Environment for Continuous Control and Reinforcement Learning](by_paper/AR-024_review.md) — Open scaled-racing evaluation environment with physical cars; a low-cost physical testbed idea.
- [AR-025: Real-Time Adaptive Velocity Optimization for Autonomous Electric Cars at the Limits of Handling](by_paper/AR-025_review.md) — Real-time velocity planning with energy and friction limits on an electric racecar; a driver component for energy-limited races.
- [AR-026: Efficient Trajectory Optimization for Autonomous Racing via Formula-1 Data-Driven Initialization](by_paper/AR-026_review.md) — Uses real Formula 1 trajectory data to initialise racing-line optimisation; a source of public F1 line data and a warm-start method.
- [AR-027: Unifying F1TENTH Autonomous Racing: Survey, Methods and Benchmarks](by_paper/AR-027_review.md) — Benchmarks of racing planners and controllers on a common platform; a reference for fair controller comparisons.

## DS: Computational design synthesis, functional representation, assembly synthesis and novelty measurement

**Scope:** Engineering-design research on generating architectures from functions with grammars, decomposing structures into joined parts, and measuring whether a design is actually novel. Relevant to typed interfaces, the physical interface graph, part resolution and the project's definition of a discovery.

**Cross-paper findings**
- Function-to-form mappings and generative models can expand concept production, but generated variety is not automatically useful or novel.
- Novelty has multiple meanings: visual, structural, functional, technological, and prior-art novelty require different evidence.
- Design metrics must separate quantity, quality, variety, and novelty and must be anchored to external references.

**What is especially interesting**

- [DS-009](by_paper/DS-009_review.md): Learns function-to-component mappings from real products to synthesise configurations; a data-driven grammar source.
- [DS-012](by_paper/DS-012_review.md): The paper shows why one novelty score is inadequate: a design can use unfamiliar knowledge without adding function, or add function from familiar origins.
- [DS-017](by_paper/DS-017_review.md): Transformer-based concept generation from design knowledge; a text-level proposal route before geometry.

Across these 3 papers, the leading evidence profiles are empirical/experimental evidence (3), review/synthesis (2), dataset/benchmark (2), control/learning study (2), simulation/numerical evidence (1), mathematical/formal evidence (1). The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.

**Where Formula Ultimate should improve**
- Split Formula Ultimate reporting into geometric novelty, causal functional difference, performance benefit, and external technology novelty.
- Add a prior-art search only after a candidate has causal function and fair performance evidence.
- Use function-flow and physical-interface descriptions as search aids, not as proof that hardware exists.

**Per-paper reports and principal takeaways**
- [DS-009: Automated synthesis of electromechanical design configurations from empirical analysis of function to form mapping](by_paper/DS-009_review.md) — Learns function-to-component mappings from real products to synthesise configurations; a data-driven grammar source.
- [DS-012: Measuring technological novelty with patent-based indicators](by_paper/DS-012_review.md) — **deep review** — New functionality and new origins are correlated but convey distinct information; correlations among separate dimension indicators are generally no more than 0.3, and the IPC4-level indicators show positive significant relationships with breakthrough probability (pp. 2, 11-12).
- [DS-017: Generative Transformers for Design Concept Generation](by_paper/DS-017_review.md) — Transformer-based concept generation from design knowledge; a text-level proposal route before geometry.

## Report limitations

- This library covers PDFs present under `papers/` on the reading date; it is not an exhaustive database systematic review.
- Section detection is a navigation aid and can miss unusually formatted headings, while page coverage and word totals are computed across every page.
- Per-paper reports are project-transfer readings, not critical replications or complete statistical-quality appraisals.
