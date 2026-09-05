# Formula Ultimate Related-Work Catalog — 2026-09-05

Thai companion: `RELATED_WORK_CATALOG_2026-09-05.th.md`

Contains **62 academic works (P01–P62)** and **8 industry/tool sources (I01–I08)**. See the [assessment](../reports/LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.md) for conclusions and development priorities.

## Scope and selection method

Broad primary-source search through 2026-09-05: publishers, arXiv, university repositories, author sites, developer repositories and official team/supplier pages. Selection covers both directly similar objectives and methods useful for missing capabilities. This is not a systematic review or an exhaustive claim. Preprint and published versions of one work are not counted twice. Substantive follow-on works are separate, with dependencies noted.

Reading depth: **E** = selected full-text/technical sections inspected, including limitations; **A** = primary abstract/project explanation inspected, sometimes through search indexing; **M** = bibliographic/project identity checked, without full methodological assessment. No label means reproduced. Not every full paper was read; no external research code or large dataset was run/downloaded.

**First / Next / Later** is a reading priority for the current project, not a journal-quality ranking. Each entry distinguishes useful transfer from unsupported extrapolation. Original titles are retained for retrieval.

Representative queries: `robot morphology controller co-design graph grammar`, `quality diversity surrogate assisted illumination`, `multifidelity optimization`, `CAD generation BRep graph`, `Formula One minimum lap time three-dimensional track`, `aero suspension optimization`, `tyre thermal transient Magic Formula`, `simulation fidelity autonomous racing telemetry`, `CFD front wing experimental validation`, `DrivAerNet CarBench`, `F1 simulator correlation Mercedes McLaren Ferrari`, plus exact titles found through reference following.

Access limitations: some Taylor & Francis/ScienceDirect pages and author PDFs returned 403 or fetch errors. Available primary indexed abstracts or institutional copies were used, and depth was lowered when methods were unavailable. P28/P29/P54 are M, not solver endorsements; P38 had restricted direct publisher access. Web upload dates can differ from publication: P30 is SIGGRAPH 2023 (preprint 2022), P42 is IEEE IV 2024 (arXiv deposit 2026). P10 is accepted for AVEC 2026, scheduled for 2026-09-07 through 2026-09-11, after this review date. No independent replication of the recent 2026 results is claimed.

## Morphology and controller co-design

### P01 — Evolving Virtual Creatures

Sims · 1994 · SIGGRAPH · **Next · E** · [Primary source](https://www.karlsims.com/papers/siggraph94.pdf)

Jointly evolves body graphs and control. Foundational precedent for morphology discovery; virtual locomotion is not race-vehicle validation.

### P02 — Automatic design and manufacture of robotic lifeforms

Lipson & Pollack · 2000 · Nature · **Next · A** · [Primary source](https://web.mit.edu/people/hlipson/papers/design.pdf)

Connects evolved bodies to manufactured robots. Use as a precedent for an eventual build-and-test gate; demonstrated mechanisms and tasks are restricted.

### P03 — RoboGrammar: Graph Grammar for Terrain-Optimized Robot Design

Zhao et al. · 2020 · ACM TOG · **First · A** · [Primary source](https://people.csail.mit.edu/jiex/papers/robogrammar/index.html)

Graph grammar plus control evaluation searches mechanically meaningful designs. Adapt grammar validity and controller allocation; its component rules still restrict the design space.

### P04 — Evolution Gym: A Large-Scale Benchmark for Evolving Soft Robots

Bhatia et al. · 2021 · NeurIPS; arXiv 2022 · **Next · A** · [Primary source](https://arxiv.org/abs/2201.09863)

A shared morphology/control benchmark supports fair algorithm comparisons. Borrow benchmark discipline, not its 2D voxel physics as evidence for 3D racing.

### P05 — Neural Graph Evolution: Towards Efficient Automatic Robot Design

Wang et al. · 2019 · arXiv · **Next · A** · [Primary source](https://arxiv.org/abs/1906.05370)

Reuses graph-based control knowledge across morphology changes. Useful against repeated retraining cost; transfer benefits must be remeasured under our budgets.

### P06 — Embodied Intelligence via Learning and Evolution

Gupta et al. · 2021 · arXiv · **Next · A** · [Primary source](https://arxiv.org/abs/2102.02202)

Studies evolution with learning across environments. Test whether discovered mechanics remain learnable across tracks; manufacturing feasibility is a separate obligation.

### P07 — DiffAqua: A Differentiable Computational Design Pipeline for Soft Underwater Swimmers with Shape Interpolation

Ma et al. · 2021 · ACM TOG · **Later · A** · [Primary source](https://arxiv.org/abs/2104.00837)

Differentiable shape/control co-design illustrates coupled optimization. Shape interpolation and underwater soft-body assumptions do not cover arbitrary racing topology.

### P08 — DiffTaichi: Differentiable Programming for Physical Simulation

Hu et al. · 2020 · ICLR; preprint 2019 · **Next · A** · [Primary source](https://arxiv.org/abs/1910.00935)

Provides differentiable simulation machinery. Consider local continuous optimization inside an admitted topology; gradients do not establish physical accuracy or smooth contact.

### P09 — Multi-Objective Graph Heuristic Search for Terrestrial Robot Design

Xu et al. · 2021 · ICRA · **First · A** · [Primary source](https://arxiv.org/abs/2107.05858)

Searches discrete robot designs across competing objectives. Useful for mechanics-performance trade-offs; retain the project's declared race objective and constraints.

### P10 — Racing a Wheeled Quadruped: Active Load Transfer Mitigation via Model Predictive Control

Eisman et al. · 2026 · arXiv; accepted AVEC 2026 · **First · A** · [Primary source](https://arxiv.org/abs/2606.26313)

Physical wheeled-quadruped racing links active leg mechanics to load transfer and lap performance. Especially relevant unconventional architecture; it controls a supplied robot rather than discovering its topology.

## Quality diversity, multifidelity and transfer

### P11 — Illuminating search spaces by mapping elites

Mouret & Clune · 2015 · arXiv · **First · A** · [Primary source](https://arxiv.org/abs/1504.04909)

MAP-Elites retains high-performing alternatives across descriptors. Directly informs Work 099; descriptor diversity can still hide mechanically equivalent designs.

### P12 — Quality Diversity: A New Frontier for Evolutionary Computation

Pugh, Soros & Stanley · 2016 · Frontiers · **Next · A** · [Primary source](https://doi.org/10.3389/frobt.2016.00040)

Organizes quality-diversity concepts and evaluation. Use to distinguish coverage, novelty and quality; a larger archive is not automatically better physical discovery.

### P13 — Data-Efficient Design Exploration through Surrogate-Assisted Illumination

Gaier, Asteroth & Mouret · 2018 · arXiv · **First · A** · [Primary source](https://arxiv.org/abs/1806.05865)

Combines surrogate models with illumination, including aerodynamic design examples. Useful for expensive evaluators; verify elite predictions and rejected-candidate false negatives.

### P14 — Covariance Matrix Adaptation MAP-Annealing

Fontaine & Nikolaidis · 2022 · arXiv · **Later · A** · [Primary source](https://arxiv.org/abs/2205.10752)

Improves continuous quality-diversity search. Benchmark after basic MAP-Elites; adaptation in parameter space does not itself create a general topology representation.

### P15 — Survey of multifidelity methods in uncertainty propagation, inference, and optimization

Peherstorfer, Willcox & Gunzburger · 2018 · SIAM Review · **First · E** · [Primary source](https://arxiv.org/abs/1806.10761)

Explains coordinated cheap and expensive models. Foundation for Work 098: model discrepancy, promotion and cost accounting; fidelity labels require demonstrated relations.

### P16 — Multi-fidelity Bayesian Optimisation with Continuous Approximations

Kandasamy et al. · 2017 · ICML · **Next · A** · [Primary source](https://proceedings.mlr.press/v70/kandasamy17a.html)

BOCA selects both candidate and fidelity using cost-aware acquisition. Useful when fidelity is controllable; assumed correlations may fail across topology discontinuities.

### P17 — Crossing the Reality Gap: a Short Introduction to the Transferability Approach

Mouret, Koos & Doncieux · 2013 · arXiv · **First · A** · [Primary source](https://arxiv.org/abs/1307.1870)

Models whether simulated behavior transfers to reality. Use a discrepancy-aware admission objective with physical evidence; simulation-only agreement is insufficient.

### P18 — Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions

Wang et al. · 2019 · arXiv · **Later · A** · [Primary source](https://arxiv.org/abs/1901.01753)

Coevolves challenges and solutions. Useful later for training environments; keep fixed hidden evaluation tracks so changing challenges cannot move the goalposts.

### P19 — Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions

Wang et al. · 2020 · arXiv · **Later · A** · [Primary source](https://arxiv.org/abs/2003.08536)

Extends open-ended challenge generation and transfer. Relevant to curricula rather than immediate mechanical validation; track environment and policy budgets separately.

### P20 — Reality-assisted evolution of soft robots through large-scale physical experimentation: a review

Howison et al. · 2020 · accepted-manuscript preprint · **Next · A** · [Primary source](https://arxiv.org/abs/2009.13960)

Reviews using physical experiments inside evolutionary design. Useful for an eventual automated bench loop; soft-robot evidence does not supply race-car material data.

## CAD, topology, meshing and contact

### P21 — DeepCAD: A Deep Generative Network for Computer-Aided Design Models

Wu, Xiao & Zheng · 2021 · ICCV · **Next · A** · [Primary source](https://arxiv.org/abs/2105.09492)

Generates CAD construction sequences. Useful proposal representation; syntactically valid CAD still requires connectivity, load-path, process and performance gates.

### P22 — Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts

Khan et al. · 2024 · arXiv / NeurIPS · **Later · A** · [Primary source](https://arxiv.org/abs/2409.17106)

Maps text to sequential CAD. Could seed proposals or aid authoring; language plausibility is not mechanics. The proceedings title uses 'Designs' instead of 'Models'.

### P23 — BRepNet: A topological message passing system for solid models

Lambourne et al. · 2021 · CVPR · **Next · A** · [Primary source](https://arxiv.org/abs/2104.00706)

Learns on solid boundary topology. Useful geometry descriptors and feature recognition; learned embeddings require invariance and failure-case audits.

### P24 — Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences

Willis et al. · 2021 · ACM TOG; preprint 2020 · **Next · E** · [Primary source](https://www.research.autodesk.com/publications/fusion-360-gallery/)

Provides human CAD sequence data. Its reconstruction discussion motivates semantic checks: high shape overlap can miss small functional features.

### P25 — DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation

Park et al. · 2019 · CVPR · **Later · A** · [Primary source](https://arxiv.org/abs/1901.05103)

Represents continuous implicit surfaces. An alternative search representation; watertight conversion, feature tolerances and manufacturing semantics remain separate tasks.

### P26 — Generating optimal topologies in structural design using a homogenization method

Bendsøe & Kikuchi · 1988 · CMAME · **Next · A** · [Primary source](https://www.sciencedirect.com/science/article/pii/0045782588900862)

Structural topology optimization establishes a physics-constrained precedent. Useful local load-frame baseline; specified load cases and material assumptions bound the result.

### P27 — A 99 line topology optimization code written in Matlab

Sigmund · 2001 · Structural and Multidisciplinary Optimization · **Next · A** · [Primary source](https://www.topopt.mek.dtu.dk/apps-and-software/a-99-line-topology-optimization-code-written-in-matlab)

Compact educational compliance-optimization baseline. Useful to test search against a strong simple method; its restricted discretization is not a whole-vehicle evaluator.

### P28 — Gmsh: a three-dimensional finite element mesh generator with built-in pre- and post-processing facilities

Geuzaine & Remacle · 2009 · IJNME · **First · M** · [Primary source](https://orbi.uliege.be/handle/2268/22742?locale=en)

Relevant mesh-generation foundation for real CAD-to-elements evaluation. Publication metadata checked; implementation decisions need its documentation and benchmark reproduction.

### P29 — Incremental Potential Contact: Intersection- and Inversion-free, Large-Deformation Dynamics

Li et al. · 2020 · ACM TOG · **Next · M** · [Primary source](https://github.com/ipc-sim/IPC)

Nonlinear contact reference implementation and paper identity checked. Candidate future contact method; numerical nonpenetration does not calibrate friction or failure.

### P30 — High-Order Incremental Potential Contact for Elastodynamic Simulation on Curved Meshes

Ferguson et al. · 2023 · SIGGRAPH; preprint 2022 · **Later · A** · [Primary source](https://arxiv.org/abs/2205.13727)

Connects high-order curved elements to robust contact. Useful once basic CAD meshing works; mathematical guarantees do not establish the material model's real-world validity.

## Racing dynamics, tracks and optimal control

### P31 — Optimal control for a Formula One car with variable parameters

Perantoni & Limebeer · 2014 · Vehicle System Dynamics · **First · A** · [Primary source](https://ora.ox.ac.uk/objects/uuid%3Ace1a7106-0a2c-41af-8449-41541220809f)

Couples vehicle parameters and minimum-time driving optimization. A direct academic reference for design/control fairness; historical F1 assumptions are not our vehicle constraints.

### P32 — Optimal control of a Formula One car on a three-dimensional track-part 1: track modeling and identification

Perantoni & Limebeer · 2015 · ASME JDSMC · **First · A** · [Primary source](https://ora.ox.ac.uk/objects/uuid%3A3a7cfbe2-facf-479f-9208-089b1b22b2ae)

Constructs and identifies a 3D track description. Direct guide for replacing ordinal track demand with spatial curvature, elevation and banking; source data still matter.

### P33 — Optimal Control of a Formula One Car on a Three-Dimensional Track - Part 2: Optimal Control

Limebeer & Perantoni · 2015 · ASME JDSMC · **Next · A** · [Primary source](https://pure.uj.ac.za/en/publications/optimal-control-of-a-formula-one-car-on-a-three-dimensional-track-3/)

Applies optimal control on the 3D track. Pair with P32 to test track-dynamics coupling; optimization success remains conditional on the supplied model.

### P34 — Minimum time optimal control simulation of a GP2 race car

Dal Bianco, Lot & Gadola · 2018 issue; online 2017 · VSD · **First · E** · [Primary source](https://eprints.soton.ac.uk/417133/)

A 14-DOF transient car, nonlinear tyres and aerodynamic ride-height effects are compared with telemetry. Practical coupled-model target; GP2 data and calibration do not automatically transfer.

### P35 — Optimizing the aero-suspension interactions in a Formula One car

Imani Masouleh & Limebeer · 2016 issue; online 2015 · IEEE TCST · **First · A** · [Primary source](https://ora.ox.ac.uk/objects/uuid%3A856dd2b0-3df9-4daa-a4f7-9462dc7cd2f8)

Studies suspension geometry and aero interaction inside optimization. Supports a coupled ride-height/downforce/load-transfer benchmark; fixed F1 suspension structure is a baseline only.

### P36 — Optimal control of Formula One car energy recovery systems

Limebeer, Perantoni & Rao · 2014 · International Journal of Control · **Next · E** · [Primary source](https://www.anilvrao.com/Publications/JournalPublications/F-1-Optimal-Control-Energy-Recovery.pdf)

Jointly schedules energy recovery and minimum-time driving. Transfer the optimal-control formulation; its historical regulatory power and energy limits are not current rules.

### P37 — Optimal energy management for formula-E cars with regulatory limits and thermal constraints

Liu, Fotouhi & Auger · 2020 · Applied Energy · **First · A** · [Primary source](https://dspace.lib.cranfield.ac.uk/bitstream/1826/15797/1/Optimal_energy_management_for_formula-E_cars_with_regulatory_limits_and_thermal_constraints-2020.pdf)

Battery temperature and energy limits change optimal race control. Useful for full-stint energy/thermal coupling; simulated generation comparisons are not measurements of our system.

### P38 — Optimal tyre usage for a Formula One car

Tremlett & Limebeer · 2016 · Vehicle System Dynamics · **First · A** · [Primary source](https://www.tandfonline.com/doi/abs/10.1080/00423114.2016.1213861)

Connects tyre condition with racing decisions over a stint. Relevant beyond one best lap; primary indexed abstract inspected, direct publisher access was restricted.

### P39 — Minimum curvature trajectory planning and control for an autonomous race car

Heilmeier et al. · 2020 issue; online 2019 · VSD · **Next · A** · [Primary source](https://www.tandfonline.com/doi/abs/10.1080/00423114.2019.1631455)

Practical raceline planning and control with an author code route. Useful initial baseline; minimizing curvature is not identical to minimizing lap time.

### P40 — Outracing champion Gran Turismo drivers with deep reinforcement learning

Wurman et al. · 2022 · Nature · **Later · E** · [Primary source](https://www.nature.com/articles/s41586-021-04357-7)

Demonstrates strong learned racing control in a game. Useful controller methodology; neither real F1 model correlation nor autonomous vehicle morphology discovery is established.

### P41 — Optimization-Based Autonomous Racing of 1:43 Scale RC Cars

Liniger, Domahidi & Morari · 2015 issue; arXiv 2017 · OCA · **Next · A** · [Primary source](https://arxiv.org/abs/1711.07300)

Model predictive contouring control supplies an implementable racing-controller baseline. Scale and tyre conditions differ; compare controller budgets and actuator limits explicitly.

### P42 — Analyzing the Impact of Simulation Fidelity on the Evaluation of Autonomous Driving Motion Control

Sagmeister et al. · IEEE IV 2024; arXiv deposit 2026 · **First · A** · [Primary source](https://arxiv.org/abs/2602.07984)

Compares fidelity variants with real autonomous-racing telemetry. Direct template for ablation near handling limits; the 2026 deposit must not be mistaken for first publication.

## Tyres and tyre thermodynamics

### P43 — Tyre Modelling for Use in Vehicle Dynamics Studies

Bakker, Nyborg & Pacejka · 1987 · SAE 870421 · **First · A** · [Primary source](https://saemobilus.sae.org/papers/tyre-modelling-use-vehicle-dynamics-studies-870421)

Foundational fitted tyre-force relations. Start a measured tyre-map baseline; the equations do not supply coefficients and pure steady-state fits do not cover all transient combined slip.

### P44 — Magic Formula Tyre Model with Transient Properties

Pacejka & Besselink · 1997 · Vehicle System Dynamics · **First · A** · [Primary source](https://www.tandfonline.com/doi/abs/10.1080/00423119708969658)

Adds transient tyre behavior to a Magic Formula framework. Useful for relaxation and combined-demand studies; identify parameters against relevant measured conditions.

### P45 — An improved Magic Formula/Swift tyre model that can handle inflation pressure changes

Besselink, Schmeitz & Pacejka · 2010 · VSD · **Next · A** · [Primary source](https://pure.tue.nl/ws/files/3139490/Metis245615.pdf)

Extends tyre modeling for pressure and related effects. Guides a pressure/camber applicability envelope; additional parameters need data rather than guessed detail.

### P46 — TRT: thermo racing tyre a physical model to predict the tyre temperature distribution

Farroni et al. · 2014 issue; online 2013 · Meccanica · **Next · E** · [Primary source](https://link.springer.com/article/10.1007/s11012-013-9821-9)

Models tyre heat distribution and compares with track telemetry. Useful thermal architecture; confidential operating data prevent treating the paper as an open F1 calibration dataset.

## Aerodynamics and learned surrogates

### P47 — Aerodynamics of Race Cars

Katz · 2006 · Annual Review of Fluid Mechanics · **Next · A** · [Primary source](https://www.annualreviews.org/content/journals/10.1146/annurev.fluid.38.050304.092016)

Reviews race-car aerodynamic mechanisms and ground effects. Use to choose causal tests and interactions; a review does not provide a validated map for a new geometry.

### P48 — Spectral/hp element simulation of flow past a Formula One front wing: validation against experiments

Buscariolo et al. · 2019 · arXiv · **First · A** · [Primary source](https://arxiv.org/abs/1909.06701)

Provides an experimentally anchored front-wing CFD benchmark. Useful isolated aero validation before whole-vehicle claims; a validated wing is not a validated car.

### P49 — DAFoam: An Open-Source Adjoint Framework for Multidisciplinary Design Optimization with OpenFOAM

He et al. · 2020 · AIAA Journal · **Next · A** · [Primary source](https://mdolab.engin.umich.edu/bibliography/He2020b)

Adjoint CFD-based design optimization. Candidate local aero shape optimizer; meshes, turbulence, boundary conditions and adjoint checks remain required.

### P50 — Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design

Palacios et al. · 2013 · AIAA · **Next · A** · [Primary source](https://su2code.github.io/documents/SU2_AIAA_ASM2013.pdf)

Open multiphysics/design solver framework. Evaluate as a backend on common benchmark cases; installing a solver is not evidence of predictive accuracy.

### P51 — DrivAerNet: A Parametric Car Dataset for Data-Driven Aerodynamic Design and Prediction

Elrefaie et al. · 2024 · arXiv · **Next · A** · [Primary source](https://arxiv.org/abs/2403.08055)

Parametric road-car CFD data supports aero surrogate experiments. Useful data pipeline reference; the geometry distribution does not cover arbitrary race vehicles.

### P52 — DrivAerNet++: A Large-Scale Multimodal Car Dataset with Computational Fluid Dynamics Simulations and Deep Learning Benchmarks

Elrefaie et al. · 2024 · NeurIPS · **Next · A** · [Primary source](https://arxiv.org/abs/2406.09624)

Expanded multimodal car dataset and prediction benchmarks. Related to P51, not independent physical replication; CFD-generated labels retain solver/model bias.

### P53 — CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics

Elrefaie et al. · 2025 preprint; revised 2026-08-20 · **Next · A** · [Primary source](https://arxiv.org/abs/2512.07847)

Benchmarks surrogate accuracy, physical consistency, cost and uncertainty. Useful evaluation template; it reuses DrivAerNet++ and cannot certify out-of-distribution novel topologies.

## Simulation infrastructure and scientific validation

### P54 — Chrono: An Open Source Multi-physics Dynamics Engine

Tasora et al. · 2016 · LNCS · **Next · M** · [Primary source](https://projectchrono.org/faq/)

Official project bibliography verifies this engine paper. Candidate general dynamics backend; inspect benchmark suitability instead of assuming an engine name ensures fidelity.

### P55 — Chrono::Vehicle: template-based ground vehicle modelling and simulation

Serban, Taylor, Negrut & Tasora · 2019 · IJVP · **First · A** · [Primary source](https://www.inderscience.com/info/inarticle.php?artid=97096)

Modular multibody vehicle simulation provides a stronger public comparison route. Use templates for controlled baselines while preserving free-topology generation upstream.

### P56 — MuJoCo: A physics engine for model-based control

Todorov, Erez & Tassa · 2012 · IROS · **Next · A** · [Primary source](https://homes.cs.washington.edu/~todorov/papers/TodorovIROS12.pdf)

Efficient contact-rich dynamics supports control training comparisons. General robot contact is not a substitute for calibrated racing tyres, aero or material failure.

### P57 — OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization

Gray et al. · 2019 · Structural and Multidisciplinary Optimization · **Next · E** · [Primary source](https://link.springer.com/article/10.1007/s00158-019-02211-z)

Organizes coupled analyses and derivatives. Useful orchestration pattern for design/control/energy/structure; the framework does not supply missing physics.

### P58 — Bayesian calibration of computer models

Kennedy & O'Hagan · 2001 · JRSS B · **First · A** · [Primary source](https://rss.onlinelibrary.wiley.com/doi/pdf/10.1111/1467-9868.00294)

Separates calibration uncertainty from model discrepancy. Useful measured-data plan; parameter fitting and discrepancy can be confounded without informative experiments.

### P59 — Verification and validation in computational fluid dynamics

Oberkampf & Trucano · 2002 · Progress in Aerospace Sciences · **First · E** · [Primary source](https://www.sciencedirect.com/science/article/pii/S0376042102000052)

Distinguishes solving equations correctly from agreement with experiments. Direct foundation for independent residuals, convergence studies and evidence-tier language.

### P60 — Deep Reinforcement Learning at the Edge of the Statistical Precipice

Agarwal et al. · 2021 · NeurIPS · **First · A** · [Primary source](https://arxiv.org/abs/2108.13264)

Shows why few-run aggregate comparisons need uncertainty-aware statistics. Useful seed, confidence-interval and robust-reporting practice; it does not prove any Formula Ultimate algorithm wins.

### P61 — The Formula SAE Tire Test Consortium-Tire Testing and Data Handling

Kasprzak & Gentz · 2006 · SAE 2006-01-3606 · **Next · A** · [Primary source](https://saemobilus.sae.org/papers/formula-sae-tire-test-consortium-tire-testing-data-handling-2006-01-3606)

Describes coordinated tyre testing and data handling. Useful experimental acquisition reference; consortium access and tyre applicability must be checked separately.

### P62 — Autonomous Racing using Learning Model Predictive Control

Rosolia, Carvalho & Borrelli · 2016 · arXiv · **Next · A** · [Primary source](https://arxiv.org/abs/1610.06534)

Uses previous racing experience to improve predictive control. A controller-learning comparator; safety and improvement depend on its assumptions and modeled setting.

## Industry and tool evidence — excluded from the 62-paper count

### I01 — Mercedes — How Does F1 Simulation Work?

Team article; historical 2020 context · [Direct source](https://www.mercedesamgf1.com/news/how-does-f1-simulation-work)

Explains computer simulation, driver-in-loop and correlation with real track/car data. Evidence of workflow, not a public numerical error budget.

### I02 — McLaren — The secrets of the sim

Team article; historical public description · [Direct source](https://www.mclaren.com/racing/latest-news/mclarenracing/article/secrets-formula-1-simulator/)

Describes simulator preparation and matching vehicle/track conditions. Supports integration requirements; it does not disclose the proprietary model.

### I03 — Dynisma — Ferrari simulator completion

Supplier announcement; 2021-07-07 · [Direct source](https://www.dynisma.com/news/dynisma-completes-scuderia-ferrari-mission-winnows-new-simulator)

Confirms a dedicated Ferrari driver simulator. Motion bandwidth/latency claims concern hardware response, not measured whole-model prediction accuracy.

### I04 — rFpro — Terrain Server

Supplier product description; accessed 2026-09-05 · [Direct source](https://rfpro.com/simulation-software/terrain-server/)

Claims road detail of 1 cm horizontally, 1 mm vertically and feed rates up to 5 kHz. These are road representation/feed specifications, not F1 lap-error or complete-solver rates.

### I05 — Formula 1 / Rob Smedley — What is correlation?

Official F1 explanation; 2019 · [Direct source](https://www.formula1.com/en/latest/article/smedley-what-is-correlation.3gcOwCLuQ7rxk4bNeBKf1p)

Explains matching simulations and real-car results. Supports making correlation a separate gate; public explanation supplies no universal F1 accuracy threshold.

### I06 — Fastest-lap

Author-maintained open-source project · [Direct source](https://github.com/juanmanzanero/fastest-lap)

Offers minimum-lap-time optimization and public vehicle examples. A practical baseline to reproduce; a public F1 example is not a team's proprietary simulator.

### I07 — MFeval — Equation source

Implementation author's documentation · [Direct source](https://mfeval.wordpress.com/equation-source/)

Explains sources and corrections for Magic Formula equations. Useful implementation cross-check; equations are separate from licensed or measured tyre coefficients.

### I08 — Milliken Research — FSAE Tire Test Consortium

Data-owner information · [Direct source](https://www.millikenresearch.com/fsaettc.html)

A route to investigate tyre data access and testing practice. No data access, purchase, licence or F1 tyre equivalence is assumed.
