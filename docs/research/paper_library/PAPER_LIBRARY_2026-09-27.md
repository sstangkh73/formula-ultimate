# Formula Ultimate Paper Library — 2026-09-27

Thai companion: `PAPER_LIBRARY_2026-09-27.th.md`

Work 145 library of papers that bear on Formula Ultimate directly (the same kind of objective or method), indirectly (a method the project could adopt), or through data and findings the project can use. It extends the Work 102 catalog (`../RELATED_WORK_CATALOG_2026-09-05.md`, P01-P62); those papers appear here with their P-number.

## How to read this catalog

- **Relation.** `direct`: same kind of objective or method as the project. `indirect`: a method, tool or argument the project could adopt. `data/findings`: measured data, a dataset or a quantitative finding the project can use.
- **Identity.** A paper is only saved when its title was confirmed against arXiv, Crossref or Semantic Scholar metadata and the curated title words were found on the first pages of the PDF. Remembered identifiers were treated as hints, not facts.
- **Local copy.** PDFs are in `papers/<category>/`, which is git-ignored: most papers, even open-access ones, may not be redistributed under this repository's CC BY 4.0 licence. Only metadata is committed. SHA-256, size and source URL of every file are in `manifest_v1.json`.
- **No local copy.** Recorded as `no open-access copy found` (no source asserted a free copy; obtain through a library), `download failed` (a free copy exists but the host refused scripted access, usually a Cloudflare-style bot check, which was not bypassed) or `identity unconfirmed`. Papers in the second group are listed at the end with a link to open in a browser; save them into any folder and file them with `python scripts/research/build_paper_library.py --ingest <folder>`, which applies the same title check.
- **Relevance notes** are judgement from abstracts and known content, not the result of reading every paper in full, and they are not claims that a method works for this project. A search that did not find a competitor is not evidence of novelty.

Regenerate with `python scripts/research/build_paper_library.py --download`.

| Category | Papers | Direct | Indirect | Data | Local PDF |
| --- | ---: | ---: | ---: | ---: | ---: |
| Open-ended, evolutionary and morphology/control co-design discovery | 43 | 15 | 28 | 0 | 33 |
| LLM and AI agents for engineering design, CAD code and simulation | 43 | 15 | 27 | 1 | 43 |
| Quality diversity, search algorithms, surrogates and multifidelity | 36 | 12 | 24 | 0 | 31 |
| CAD, B-rep and assembly representation, generation and datasets | 34 | 4 | 27 | 3 | 30 |
| Topology optimisation, meshing, finite elements, contact and failure numerics | 24 | 7 | 17 | 0 | 9 |
| Simulation, optimal-control and MDO infrastructure, coupling and integrators | 21 | 5 | 16 | 0 | 12 |
| Minimum-lap-time optimal control, vehicle dynamics, tracks and design/control co-optimisation | 32 | 19 | 12 | 1 | 11 |
| Race energy management, powertrain architecture and energy storage | 31 | 15 | 8 | 8 | 15 |
| Tyres, rubber friction and tyre identification | 17 | 7 | 7 | 3 | 5 |
| Aerodynamics, CFD validation, aero datasets and neural surrogates | 33 | 7 | 15 | 11 | 22 |
| Thermal management, heat generation and cooling design | 6 | 3 | 3 | 0 | 2 |
| Materials, material data, fasteners and joints, crash structures, manufacturing and tolerances | 15 | 7 | 4 | 4 | 2 |
| Verification, validation, calibration, statistics, reproducibility and claim discipline | 32 | 14 | 18 | 0 | 20 |
| Autonomous racing control, learned drivers, real telemetry and race strategy | 27 | 5 | 19 | 3 | 23 |
| Computational design synthesis, functional representation, assembly synthesis and novelty measurement | 17 | 8 | 9 | 0 | 3 |
| **Total** | **411** | **143** | **234** | **34** | **261** |

downloaded: **261** · no open-access copy found: **90** · identity unconfirmed: **0** · download failed: **60**

## Open-ended, evolutionary and morphology/control co-design discovery

Work that searches over body/topology and behaviour together, or studies what makes open-ended design search productive. Closest to the project's discovery objective; none of it validates a racing vehicle.

### OE-001 — Evolving Virtual Creatures

Sims · 1994 · Proceedings of the 21st annual conference on Computer graphics and interactive techniques - SIGGRAPH '94 · **direct** · Work 102 catalog P01

[source](https://doi.org/10.1145/192161.192167) · local PDF: [`papers/01_open_ended_codesign/OE-001_Sims1994_evolving-virtual-creatures.pdf`](../../../papers/01_open_ended_codesign/OE-001_Sims1994_evolving-virtual-creatures.pdf)

Founding example of evolving body graphs and controllers together; the typed-genome and topology mutation work (Works 093-094) descends from this idea.

### OE-002 — Automatic design and manufacture of robotic lifeforms

Lipson & Pollack · 2000 · Nature · **direct** · Work 102 catalog P02

[source](https://doi.org/10.1038/35023115) · local PDF: [`papers/01_open_ended_codesign/OE-002_Lipson2000_automatic-design-and-manufacture-of-robotic-lifefo.pdf`](../../../papers/01_open_ended_codesign/OE-002_Lipson2000_automatic-design-and-manufacture-of-robotic-lifefo.pdf)

Closes the loop from evolved design to a manufactured, physically tested machine; the template for an eventual build-and-test gate after Level-0 search.

### OE-003 — RoboGrammar: Graph Grammar for Terrain-Optimized Robot Design

Zhao et al. · 2020 · ACM Transactions on Graphics · **direct** · Work 102 catalog P03

[source](https://doi.org/10.1145/3414685.3417831) · no local copy (download failed) · [open-access copy to fetch in a browser](https://dl.acm.org/doi/pdf/10.1145/3414685.3417831)

Graph grammar plus per-design controller optimisation over terrains; directly comparable to our constrained component grammar and environment-dependent specialisation hypothesis H3.

### OE-004 — Evolution Gym: A Large-Scale Benchmark for Evolving Soft Robots

Bhatia et al. · 2021 · Neural Information Processing Systems · **indirect** · Work 102 catalog P04

[source](https://arxiv.org/abs/2201.09863) · [arXiv:2201.09863](https://arxiv.org/abs/2201.09863) · local PDF: [`papers/01_open_ended_codesign/OE-004_Bhatia2021_evolution-gym-a-large-scale-benchmark-for-evolving.pdf`](../../../papers/01_open_ended_codesign/OE-004_Bhatia2021_evolution-gym-a-large-scale-benchmark-for-evolving.pdf)

Shared co-design benchmark with fixed tasks and budgets; borrow its benchmark discipline for fair GRID/RANDOM/EVOLUTION/QD comparisons.

### OE-005 — Neural Graph Evolution: Towards Efficient Automatic Robot Design

Wang et al. · 2019 · International Conference on Learning Representations · **indirect** · Work 102 catalog P05

[source](https://arxiv.org/abs/1906.05370) · [arXiv:1906.05370](https://arxiv.org/abs/1906.05370) · local PDF: [`papers/01_open_ended_codesign/OE-005_Wang2019_neural-graph-evolution-towards-efficient-automatic.pdf`](../../../papers/01_open_ended_codesign/OE-005_Wang2019_neural-graph-evolution-towards-efficient-automatic.pdf)

Reuses graph-network controllers across morphology mutations to cut retraining cost; relevant if every topology needs its own optimised driver.

### OE-006 — Embodied Intelligence via Learning and Evolution

Gupta et al. · 2021 · Nature Communications · **direct** · Work 102 catalog P06

[source](https://arxiv.org/abs/2102.02202) · [arXiv:2102.02202](https://arxiv.org/abs/2102.02202) · local PDF: [`papers/01_open_ended_codesign/OE-006_Gupta2021_embodied-intelligence-via-learning-and-evolution.pdf`](../../../papers/01_open_ended_codesign/OE-006_Gupta2021_embodied-intelligence-via-learning-and-evolution.pdf)

Shows environment complexity shapes evolved morphology (DERL); evidence and method for testing H3 across race environments.

### OE-007 — DiffAqua: A Differentiable Computational Design Pipeline for Soft Underwater Swimmers with Shape Interpolation

Ma et al. · 2021 · ACM Transactions on Graphics · **indirect** · Work 102 catalog P07

[source](https://arxiv.org/abs/2104.00837) · [arXiv:2104.00837](https://arxiv.org/abs/2104.00837) · local PDF: [`papers/01_open_ended_codesign/OE-007_Ma2021_diffaqua-a-differentiable-computational-design-pip.pdf`](../../../papers/01_open_ended_codesign/OE-007_Ma2021_diffaqua-a-differentiable-computational-design-pip.pdf)

Differentiable shape-and-control co-design; a model for gradient refinement inside an admitted topology, not for topology change itself.

### OE-008 — Multi-Objective Graph Heuristic Search for Terrestrial Robot Design

Xu et al. · 2021 · IEEE International Conference on Robotics and Automation · **direct** · Work 102 catalog P09

[source](https://arxiv.org/abs/2107.05858) · [arXiv:2107.05858](https://arxiv.org/abs/2107.05858) · local PDF: [`papers/01_open_ended_codesign/OE-008_Xu2021_multi-objective-graph-heuristic-search-for-terrest.pdf`](../../../papers/01_open_ended_codesign/OE-008_Xu2021_multi-objective-graph-heuristic-search-for-terrest.pdf)

Discrete graph design search under competing objectives; a comparator for multi-objective race time, energy, mass and reliability (H2).

### OE-009 — Racing a Wheeled Quadruped: Active Load Transfer Mitigation via Model Predictive Control

Eisman et al. · 2026 · arXiv.org · **direct** · Work 102 catalog P10

[source](https://arxiv.org/abs/2606.26313) · [arXiv:2606.26313](https://arxiv.org/abs/2606.26313) · local PDF: [`papers/01_open_ended_codesign/OE-009_Eisman2026_racing-a-wheeled-quadruped-active-load-transfer-mi.pdf`](../../../papers/01_open_ended_codesign/OE-009_Eisman2026_racing-a-wheeled-quadruped-active-load-transfer-mi.pdf)

Physical racing of an unconventional ground-contact architecture with lap-time gains from active leg mechanics; the closest published analogue to a non-car racing morphology.

### OE-010 — Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions

Wang et al. · 2019 · arXiv.org · **indirect** · Work 102 catalog P18

[source](https://arxiv.org/abs/1901.01753) · [arXiv:1901.01753](https://arxiv.org/abs/1901.01753) · local PDF: [`papers/01_open_ended_codesign/OE-010_Wang2019_paired-open-ended-trailblazer-poet-endlessly-gener.pdf`](../../../papers/01_open_ended_codesign/OE-010_Wang2019_paired-open-ended-trailblazer-poet-endlessly-gener.pdf)

Co-evolves environments and solutions; useful for curriculum tracks, provided held-out evaluation tracks stay fixed.

### OE-011 — Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions

Wang et al. · 2020 · International Conference on Machine Learning · **indirect** · Work 102 catalog P19

[source](https://arxiv.org/abs/2003.08536) · [arXiv:2003.08536](https://arxiv.org/abs/2003.08536) · local PDF: [`papers/01_open_ended_codesign/OE-011_Wang2020_enhanced-poet-open-ended-reinforcement-learning-th.pdf`](../../../papers/01_open_ended_codesign/OE-011_Wang2020_enhanced-poet-open-ended-reinforcement-learning-th.pdf)

Adds a domain-general novelty measure and transfer between environment-solution pairs; relevant to measuring environment novelty honestly.

### OE-012 — Reality-assisted evolution of soft robots through large-scale physical experimentation: a review

Howison et al. · 2020 · Artificial Life · **indirect** · Work 102 catalog P20

[source](https://arxiv.org/abs/2009.13960) · [arXiv:2009.13960](https://arxiv.org/abs/2009.13960) · local PDF: [`papers/01_open_ended_codesign/OE-012_Howison2020_reality-assisted-evolution-of-soft-robots-through.pdf`](../../../papers/01_open_ended_codesign/OE-012_Howison2020_reality-assisted-evolution-of-soft-robots-through.pdf)

Reviews putting physical experiments inside the evolutionary loop; informs the physical-correlation programmes (Works 131-133).

### OE-013 — Evolving Neural Networks through Augmenting Topologies

Stanley & Miikkulainen · 2002 · Evolutionary Computation · **direct**

[source](https://doi.org/10.1162/106365602320169811) · local PDF: [`papers/01_open_ended_codesign/OE-013_Stanley2002_evolving-neural-networks-through-augmenting-topolo.pdf`](../../../papers/01_open_ended_codesign/OE-013_Stanley2002_evolving-neural-networks-through-augmenting-topolo.pdf)

NEAT: historical markings, speciation and complexification for evolving graph topology; the standard answer to crossover between different topologies (Work 094).

### OE-014 — Compositional pattern producing networks: A novel abstraction of development

Stanley · 2007 · Genetic Programming and Evolvable Machines · **indirect**

[source](https://doi.org/10.1007/s10710-007-9028-8) · no local copy (no open-access copy found)

CPPN generative encoding for geometry with regularity and symmetry; a candidate representation for the spatial material fields (Works 108-111).

### OE-015 — Unshackling evolution: evolving soft robots with multiple materials and a powerful generative encoding

Cheney et al. · 2013 · Proceedings of the 15th annual conference on Genetic and evolutionary computation · **indirect**

[source](https://doi.org/10.1145/2463372.2463404) · no local copy (no open-access copy found)

CPPN-encoded multi-material voxel bodies outperform direct encodings; evidence for generative encodings in material-distribution search.

### OE-016 — Scalable Co-Optimization of Morphology and Control in Embodied Machines

Cheney et al. · 2018 · Journal of the Royal Society Interface · **direct**

[source](https://arxiv.org/abs/1706.06133) · [arXiv:1706.06133](https://arxiv.org/abs/1706.06133) · local PDF: [`papers/01_open_ended_codesign/OE-016_Cheney2018_scalable-co-optimization-of-morphology-and-control.pdf`](../../../papers/01_open_ended_codesign/OE-016_Cheney2018_scalable-co-optimization-of-morphology-and-control.pdf)

Shows morphological innovations are lost because the controller has not adapted yet, and proposes protecting them; a known failure mode for our design/driver co-search.

### OE-017 — Environmental influence on the evolution of morphological complexity in machines

Auerbach & Bongard · 2014 · PLoS Computational Biology · **direct**

[source](https://doi.org/10.1371/journal.pcbi.1003399) · local PDF: [`papers/01_open_ended_codesign/OE-017_Auerbach2014_environmental-influence-on-the-evolution-of-morpho.pdf`](../../../papers/01_open_ended_codesign/OE-017_Auerbach2014_environmental-influence-on-the-evolution-of-morpho.pdf)

Measures how environment shapes evolved morphological complexity; a direct method reference for H3 environment-dependent specialisation.

### OE-018 — Morphological change in machines accelerates the evolution of robust behavior

Bongard · 2011 · Proceedings of the National Academy of Sciences · **indirect**

[source](https://doi.org/10.1073/pnas.1015390108) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.ncbi.nlm.nih.gov/pmc/articles/3029735)

Body change during evolution improves robustness of behaviour; relevant to held-out race robustness (Work 128).

### OE-019 — A scalable pipeline for designing reconfigurable organisms

Kriegman et al. · 2020 · Proceedings of the National Academy of Sciences · **direct**

[source](https://doi.org/10.1073/pnas.1910837117) · no local copy (download failed) · [open-access copy to fetch in a browser](https://doi.org/10.1073/pnas.1910837117)

Evolved designs filtered for simulation-to-reality robustness, then built and tested; a worked example of the generated-to-physically-tested evidence ladder.

### OE-020 — Efficient automatic design of robots

Matthews et al. · 2023 · Proceedings of the National Academy of Sciences · **direct**

[source](https://doi.org/10.1073/pnas.2305180120) · [arXiv:2306.03263](https://arxiv.org/abs/2306.03263) · local PDF: [`papers/01_open_ended_codesign/OE-020_Matthews2023_efficient-automatic-design-of-robots.pdf`](../../../papers/01_open_ended_codesign/OE-020_Matthews2023_efficient-automatic-design-of-robots.pdf)

Gradient-based whole-body design found in seconds and fabricated; a benchmark for how fast a topology search can be once differentiable physics exists.

### OE-021 — Reinforcement Learning for Improving Agent Design

Ha · 2019 · Artificial Life · **indirect**

[source](https://arxiv.org/abs/1810.03779) · [arXiv:1810.03779](https://arxiv.org/abs/1810.03779) · local PDF: [`papers/01_open_ended_codesign/OE-021_Ha2019_reinforcement-learning-for-improving-agent-design.pdf`](../../../papers/01_open_ended_codesign/OE-021_Ha2019_reinforcement-learning-for-improving-agent-design.pdf)

Joint learning of body parameters and policy; shows the optimiser exploits body freedom in unexpected ways, a warning for our objective checks.

### OE-022 — Jointly Learning to Construct and Control Agents using Deep Reinforcement Learning

Schaff et al. · 2019 · IEEE International Conference on Robotics and Automation · **indirect**

[source](https://arxiv.org/abs/1801.01432) · [arXiv:1801.01432](https://arxiv.org/abs/1801.01432) · local PDF: [`papers/01_open_ended_codesign/OE-022_Schaff2019_jointly-learning-to-construct-and-control-agents-u.pdf`](../../../papers/01_open_ended_codesign/OE-022_Schaff2019_jointly-learning-to-construct-and-control-agents-u.pdf)

Design-conditioned policy shared across a design distribution; a way to amortise driver optimisation over many candidate vehicles.

### OE-023 — Data-efficient Co-Adaptation of Morphology and Behaviour with Deep Reinforcement Learning

Luck et al. · 2019 · Conference on Robot Learning · **indirect**

[source](https://arxiv.org/abs/1911.06832) · [arXiv:1911.06832](https://arxiv.org/abs/1911.06832) · local PDF: [`papers/01_open_ended_codesign/OE-023_Luck2019_data-efficient-co-adaptation-of-morphology-and-beh.pdf`](../../../papers/01_open_ended_codesign/OE-023_Luck2019_data-efficient-co-adaptation-of-morphology-and-beh.pdf)

Uses learned value functions to evaluate new designs without full rollouts; relevant to cheap pre-screening before Level-0 races.

### OE-024 — Transform2Act: Learning a Transform-and-Control Policy for Efficient Agent Design

Yuan et al. · 2022 · International Conference on Learning Representations · **indirect**

[source](https://arxiv.org/abs/2110.03659) · [arXiv:2110.03659](https://arxiv.org/abs/2110.03659) · local PDF: [`papers/01_open_ended_codesign/OE-024_Yuan2022_transform2act-learning-a-transform-and-control-pol.pdf`](../../../papers/01_open_ended_codesign/OE-024_Yuan2022_transform2act-learning-a-transform-and-control-pol.pdf)

Policy that first edits the body graph then controls it; an alternative to evolutionary topology mutation worth comparing at equal budget.

### OE-025 — An End-to-End Differentiable Framework for Contact-Aware Robot Design

Xu et al. · 2021 · Robotics: Science and Systems Conference · **indirect**

[source](https://arxiv.org/abs/2107.07501) · [arXiv:2107.07501](https://arxiv.org/abs/2107.07501) · local PDF: [`papers/01_open_ended_codesign/OE-025_Xu2021_an-end-to-end-differentiable-framework-for-contact.pdf`](../../../papers/01_open_ended_codesign/OE-025_Xu2021_an-end-to-end-differentiable-framework-for-contact.pdf)

Differentiable contact-aware design with cage-based deformation; relevant to ground-interaction and contact-driven geometry.

### OE-026 — SoftZoo: A Soft Robot Co-design Benchmark For Locomotion In Diverse Environments

Wang et al. · 2023 · International Conference on Learning Representations · **indirect**

[source](https://arxiv.org/abs/2303.09555) · [arXiv:2303.09555](https://arxiv.org/abs/2303.09555) · local PDF: [`papers/01_open_ended_codesign/OE-026_Wang2023_softzoo-a-soft-robot-co-design-benchmark-for-locom.pdf`](../../../papers/01_open_ended_codesign/OE-026_Wang2023_softzoo-a-soft-robot-co-design-benchmark-for-locom.pdf)

Co-design benchmark across diverse environments; a pattern for running one search across several race environments and comparing specialisation.

### OE-027 — Evolution and learning in differentiable robots

Strgar et al. · 2024 · Robotics: Science and Systems Conference · **indirect**

[source](https://arxiv.org/abs/2405.14712) · [arXiv:2405.14712](https://arxiv.org/abs/2405.14712) · local PDF: [`papers/01_open_ended_codesign/OE-027_Strgar2024_evolution-and-learning-in-differentiable-robots.pdf`](../../../papers/01_open_ended_codesign/OE-027_Strgar2024_evolution-and-learning-in-differentiable-robots.pdf)

Combines evolution of bodies with gradient learning of control at scale; informs the split between discrete search and continuous refinement.

### OE-028 — Co-optimising Robot Morphology and Controller in a Simulated Open-Ended Environment

Stensby et al. · 2021 · EvoApplications · **indirect**

[source](https://arxiv.org/abs/2104.03062) · [arXiv:2104.03062](https://arxiv.org/abs/2104.03062) · local PDF: [`papers/01_open_ended_codesign/OE-028_Stensby2021_co-optimising-robot-morphology-and-controller-in-a.pdf`](../../../papers/01_open_ended_codesign/OE-028_Stensby2021_co-optimising-robot-morphology-and-controller-in-a.pdf)

Morphology-controller co-optimisation under POET-style open-ended environments; shows how environment generation interacts with body search.

### OE-029 — An Empirical Study on the Computation Budget of Co-Optimization of Robot Design and Control in Simulation

Arza et al. · 2024 · arXiv · **direct**

[source](https://arxiv.org/abs/2409.08621) · [arXiv:2409.08621](https://arxiv.org/abs/2409.08621) · local PDF: [`papers/01_open_ended_codesign/OE-029_Arza2024_an-empirical-study-on-the-computation-budget-of-co.pdf`](../../../papers/01_open_ended_codesign/OE-029_Arza2024_an-empirical-study-on-the-computation-budget-of-co.pdf)

Quantifies how the split of compute between design and control changes co-optimisation outcomes; directly relevant to budget-matched fairness rules.

### OE-030 — Convergent Functions, Divergent Forms

Jeon et al. · 2025 · Neural Information Processing Systems · **direct**

[source](https://arxiv.org/abs/2505.21665) · [arXiv:2505.21665](https://arxiv.org/abs/2505.21665) · local PDF: [`papers/01_open_ended_codesign/OE-030_Jeon2025_convergent-functions-divergent-forms.pdf`](../../../papers/01_open_ended_codesign/OE-030_Jeon2025_convergent-functions-divergent-forms.pdf)

Studies how distinct forms reach the same function in morphology search; relevant to separating appearance novelty from functional novelty.

### OE-031 — Embodied Co-Design for Rapidly Evolving Agents

Wang et al. · 2025 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2512.04770) · [arXiv:2512.04770](https://arxiv.org/abs/2512.04770) · local PDF: [`papers/01_open_ended_codesign/OE-031_Wang2025_embodied-co-design-for-rapidly-evolving-agents.pdf`](../../../papers/01_open_ended_codesign/OE-031_Wang2025_embodied-co-design-for-rapidly-evolving-agents.pdf)

Recent survey of morphology-control co-design from virtual creatures to physical robots; a map of methods and open problems.

### OE-032 — Shaping the Evolutionary Dynamics of Robot Morphology via Adaptive Control Learning

Song et al. · 2026 · arXiv · **indirect**

[source](https://arxiv.org/abs/2608.23100) · [arXiv:2608.23100](https://arxiv.org/abs/2608.23100) · local PDF: [`papers/01_open_ended_codesign/OE-032_Song2026_shaping-the-evolutionary-dynamics-of-robot-morphol.pdf`](../../../papers/01_open_ended_codesign/OE-032_Song2026_shaping-the-evolutionary-dynamics-of-robot-morphol.pdf)

How controller learning speed shapes which morphologies survive; relevant to controller-allocation bias in our search.

### OE-033 — Shape Your Body: Value Gradients for Multi-Embodiment Robot Design

Bohlinger & Peters · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2606.00702) · [arXiv:2606.00702](https://arxiv.org/abs/2606.00702) · local PDF: [`papers/01_open_ended_codesign/OE-033_Bohlinger2026_shape-your-body-value-gradients-for-multi-embodime.pdf`](../../../papers/01_open_ended_codesign/OE-033_Bohlinger2026_shape-your-body-value-gradients-for-multi-embodime.pdf)

Uses value gradients of a multi-embodiment policy to improve body design; a continuous-design comparator.

### OE-034 — Seeking Quality Diversity in Evolutionary Co-design of Morphology and Control of Soft Tensegrity Modular Robots

Zardini et al. · 2021 · Annual Conference on Genetic and Evolutionary Computation · **indirect**

[source](https://arxiv.org/abs/2104.12175) · [arXiv:2104.12175](https://arxiv.org/abs/2104.12175) · local PDF: [`papers/01_open_ended_codesign/OE-034_Zardini2021_seeking-quality-diversity-in-evolutionary-co-desig.pdf`](../../../papers/01_open_ended_codesign/OE-034_Zardini2021_seeking-quality-diversity-in-evolutionary-co-desig.pdf)

Quality-diversity applied to morphology/control co-design; a precedent for the executable morphology archive (Work 099).

### OE-035 — Open-Endedness is Essential for Artificial Superhuman Intelligence

Hughes et al. · 2024 · International Conference on Machine Learning · **indirect**

[source](https://arxiv.org/abs/2406.04268) · [arXiv:2406.04268](https://arxiv.org/abs/2406.04268) · local PDF: [`papers/01_open_ended_codesign/OE-035_Hughes2024_open-endedness-is-essential-for-artificial-superhu.pdf`](../../../papers/01_open_ended_codesign/OE-035_Hughes2024_open-endedness-is-essential-for-artificial-superhu.pdf)

Defines open-endedness as novelty plus learnability to an observer; a usable definition for what our discovery claims should mean.

### OE-036 — Why Open-Endedness Matters

Stanley · 2019 · Artificial Life · **indirect**

[source](https://doi.org/10.1162/artl_a_00294) · no local copy (no open-access copy found)

Argues why open-ended search matters beyond optimisation; context for the research charter framing.

### OE-037 — Minimal Criterion Coevolution: A New Approach to Open-Ended Search

Brant & Stanley · 2017 · Proceedings of the Genetic and Evolutionary Computation Conference · **indirect**

[source](https://doi.org/10.1145/3071178.3071186) · no local copy (no open-access copy found)

Replaces objectives with minimal viability criteria; analogous to our feasibility gates acting as the only selection pressure.

### OE-038 — Design Mining Interacting Wind Turbines

Preen & Bull · 2016 · Evolutionary Computation · **indirect**

[source](https://arxiv.org/abs/1410.0547) · [arXiv:1410.0547](https://arxiv.org/abs/1410.0547) · local PDF: [`papers/01_open_ended_codesign/OE-038_Preen2016_design-mining-interacting-wind-turbines.pdf`](../../../papers/01_open_ended_codesign/OE-038_Preen2016_design-mining-interacting-wind-turbines.pdf)

Evolves physical designs evaluated by 3D printing and wind-tunnel tests with surrogates; an example of physical evaluation in the loop.

### OE-039 — Keep Rollin' - Whole-Body Motion Control and Planning for Wheeled Quadrupedal Robots

Bjelonic et al. · 2019 · IEEE Robotics and Automation Letters · **indirect**

[source](https://arxiv.org/abs/1809.03557) · [arXiv:1809.03557](https://arxiv.org/abs/1809.03557) · local PDF: [`papers/01_open_ended_codesign/OE-039_Bjelonic2019_keep-rollin-whole-body-motion-control-and-planning.pdf`](../../../papers/01_open_ended_codesign/OE-039_Bjelonic2019_keep-rollin-whole-body-motion-control-and-planning.pdf)

Hybrid wheel-leg locomotion control; shows what a non-conventional ground-contact endpoint demands from control.

### OE-040 — Automated Antenna Design with Evolutionary Algorithms

Hornby et al. · 2006 · Space 2006 · **direct**

[source](https://doi.org/10.2514/6.2006-7242) · local PDF: [`papers/01_open_ended_codesign/OE-040_Hornby2006_automated-antenna-design-with-evolutionary-algorit.pdf`](../../../papers/01_open_ended_codesign/OE-040_Hornby2006_automated-antenna-design-with-evolutionary-algorit.pdf)

NASA ST5 evolved antenna that flew; a rare case of an evolved, non-intuitive hardware design passing real qualification.

### OE-041 — Toward a unified and automated design methodology for multi-domain dynamic systems using bond graphs and genetic programming

Seo et al. · 2003 · Mechatronics · **direct**

[source](https://doi.org/10.1016/s0957-4158(03)00006-0) · no local copy (no open-access copy found)

Evolves bond-graph topology and parameters of multi-domain systems; the closest precedent to our typed energy-graph powertrain search.

### OE-042 — Automated design of both the topology and sizing of analog electrical circuits using genetic programming

Koza et al. · 1996 · Artificial Intelligence in Design ’96 · **indirect**

[source](https://doi.org/10.1007/978-94-009-0279-4_9) · no local copy (no open-access copy found)

Genetic programming discovering circuit topology and component values together; a classic topology-plus-sizing discovery result.

### OE-043 — Evolving three-dimensional objects with a generative encoding inspired by developmental biology

— · 2011 · ECAL 2011: The 11th European Conference on Artificial Life · **indirect**

[source](https://doi.org/10.7551/978-0-262-29714-1-ch024) · no local copy (download failed) · [open-access copy to fetch in a browser](https://doi.org/10.7551/978-0-262-29714-1-ch024)

Generative encoding producing printable 3D objects; relevant to freeform solid grammars (Work 092).


## LLM and AI agents for engineering design, CAD code and simulation

Agents and generative models that propose engineering designs, write CAD programs or drive solvers, plus work on how such systems are evaluated. Relevant because Formula Ultimate's designer is an agent that writes CadQuery and is judged by independent evaluators.

### AG-001 — Evolution through Large Models

Lehman et al. · 2022 · arXiv · **direct**

[source](https://arxiv.org/abs/2206.08896) · [arXiv:2206.08896](https://arxiv.org/abs/2206.08896) · local PDF: [`papers/02_ai_agents_engineering/AG-001_Lehman2022_evolution-through-large-models.pdf`](../../../papers/02_ai_agents_engineering/AG-001_Lehman2022_evolution-through-large-models.pdf)

LLM as the mutation operator inside MAP-Elites, generating locomoting Sodarace morphologies as code; the closest template for an LLM that mutates CadQuery vehicle programs.

### AG-002 — Mathematical discoveries from program search with large language models

Romera-Paredes et al. · 2024 · Nature · **direct**

[source](https://doi.org/10.1038/s41586-023-06924-6) · local PDF: [`papers/02_ai_agents_engineering/AG-002_Paredes2024_mathematical-discoveries-from-program-search-with.pdf`](../../../papers/02_ai_agents_engineering/AG-002_Paredes2024_mathematical-discoveries-from-program-search-with.pdf)

FunSearch pairs an LLM proposer with an automatic, trusted evaluator; its separation of generation from evaluation mirrors our independent-evaluator rule.

### AG-003 — AlphaEvolve: A coding agent for scientific and algorithmic discovery

Novikov et al. · 2025 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2506.13131) · [arXiv:2506.13131](https://arxiv.org/abs/2506.13131) · local PDF: [`papers/02_ai_agents_engineering/AG-003_Novikov2025_alphaevolve-a-coding-agent-for-scientific-and-algo.pdf`](../../../papers/02_ai_agents_engineering/AG-003_Novikov2025_alphaevolve-a-coding-agent-for-scientific-and-algo.pdf)

Evolutionary coding agent with a MAP-Elites-style program database and machine-checkable scores, including a hardware-circuit result; a reference architecture for our design agent.

### AG-004 — Evolution or Illusion? Rethinking Evaluation in LLM Evolutionary Search

Oved et al. · 2026 · arXiv · **direct**

[source](https://arxiv.org/abs/2609.19799) · [arXiv:2609.19799](https://arxiv.org/abs/2609.19799) · local PDF: [`papers/02_ai_agents_engineering/AG-004_Oved2026_evolution-or-illusion-rethinking-evaluation-in-llm.pdf`](../../../papers/02_ai_agents_engineering/AG-004_Oved2026_evolution-or-illusion-rethinking-evaluation-in-llm.pdf)

Questions whether reported gains of LLM evolutionary search survive fair baselines and budgets; directly supports our falsification and matched-budget rules.

### AG-005 — The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery

Lu et al. · 2024 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2408.06292) · [arXiv:2408.06292](https://arxiv.org/abs/2408.06292) · local PDF: [`papers/02_ai_agents_engineering/AG-005_Lu2024_the-ai-scientist-towards-fully-automated-open-ende.pdf`](../../../papers/02_ai_agents_engineering/AG-005_Lu2024_the-ai-scientist-towards-fully-automated-open-ende.pdf)

End-to-end automated research loop; useful mainly for its documented failure modes (overclaiming, weak review), which our evidence tiers are designed to block.

### AG-006 — How Can Large Language Models Help Humans in Design and Manufacturing?

Makatura et al. · 2023 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2307.14377) · [arXiv:2307.14377](https://arxiv.org/abs/2307.14377) · local PDF: [`papers/02_ai_agents_engineering/AG-006_Makatura2023_how-can-large-language-models-help-humans-in-desig.pdf`](../../../papers/02_ai_agents_engineering/AG-006_Makatura2023_how-can-large-language-models-help-humans-in-desig.pdf)

Systematic test of an LLM across CAD generation, performance evaluation, optimisation and manufacturing; maps where language models fail on geometry and physics.

### AG-007 — Large Language Model Agent as a Mechanical Designer

Jadhav & Farimani · 2024 · Journal of engineering design · **direct**

[source](https://arxiv.org/abs/2404.17525) · [arXiv:2404.17525](https://arxiv.org/abs/2404.17525) · local PDF: [`papers/02_ai_agents_engineering/AG-007_Jadhav2024_large-language-model-agent-as-a-mechanical-designe.pdf`](../../../papers/02_ai_agents_engineering/AG-007_Jadhav2024_large-language-model-agent-as-a-mechanical-designe.pdf)

LLM agent iterating truss designs with FEM feedback, compared against NSGA-II at equal evaluations; a direct method and fairness comparator.

### AG-008 — An LLM-enabled Multi-Agent Autonomous Mechatronics Design Framework

Wang et al. · 2025 · 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW) · **direct**

[source](https://arxiv.org/abs/2504.14681) · [arXiv:2504.14681](https://arxiv.org/abs/2504.14681) · local PDF: [`papers/02_ai_agents_engineering/AG-008_Wang2025_an-llm-enabled-multi-agent-autonomous-mechatronics.pdf`](../../../papers/02_ai_agents_engineering/AG-008_Wang2025_an-llm-enabled-multi-agent-autonomous-mechatronics.pdf)

Multi-agent design of a physical mechatronic prototype across mechanical, electronic and software domains; comparable to our multi-domain part-to-vehicle pipeline.

### AG-009 — Physics-in-the-Loop: A Hybrid Agentic Architecture for Validated CAD Engineering Design

Berger et al. · 2026 · Proceedings of the Thirty-Fifth International Joint Conference on Artificial Intelligence · **direct**

[source](https://arxiv.org/abs/2605.19717) · [arXiv:2605.19717](https://arxiv.org/abs/2605.19717) · local PDF: [`papers/02_ai_agents_engineering/AG-009_Berger2026_physics-in-the-loop-a-hybrid-agentic-architecture.pdf`](../../../papers/02_ai_agents_engineering/AG-009_Berger2026_physics-in-the-loop-a-hybrid-agentic-architecture.pdf)

Generate-simulate-refine CAD agent with a validated physics tool in the loop rather than visual feedback; the same pattern as our CadQuery-to-evaluator loop.

### AG-010 — Engineering.ai: A Platform for Teams of AI Engineers in Computational Design

Xu et al. · 2025 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2511.00122) · [arXiv:2511.00122](https://arxiv.org/abs/2511.00122) · local PDF: [`papers/02_ai_agents_engineering/AG-010_Xu2025_engineering-ai-a-platform-for-teams-of-ai-engineer.pdf`](../../../papers/02_ai_agents_engineering/AG-010_Xu2025_engineering-ai-a-platform-for-teams-of-ai-engineer.pdf)

LLM agents running CAD, meshing, multidisciplinary simulation and optimisation in a closed loop; a comparable system to benchmark against.

### AG-011 — Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback

Son et al. · 2026 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2605.17448) · [arXiv:2605.17448](https://arxiv.org/abs/2605.17448) · local PDF: [`papers/02_ai_agents_engineering/AG-011_Son2026_self-improving-cad-generation-agents-with-finite-e.pdf`](../../../papers/02_ai_agents_engineering/AG-011_Son2026_self-improving-cad-generation-agents-with-finite-e.pdf)

Uses FEA results as the feedback signal for a CAD-writing agent; directly relevant to geometry-structural coupling (Works 082, 138).

### AG-012 — FEABench: Evaluating Language Models on Multiphysics Reasoning Ability

Mudur et al. · 2025 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2504.06260) · [arXiv:2504.06260](https://arxiv.org/abs/2504.06260) · local PDF: [`papers/02_ai_agents_engineering/AG-012_Mudur2025_feabench-evaluating-language-models-on-multiphysic.pdf`](../../../papers/02_ai_agents_engineering/AG-012_Mudur2025_feabench-evaluating-language-models-on-multiphysic.pdf)

Benchmark for LLM agents driving a finite-element package end to end; a yardstick for how far agents can be trusted with solver setup.

### AG-013 — FEM-Bench: A Structured Scientific Reasoning Benchmark

Mohammadzadeh et al. · 2025 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2512.20732) · [arXiv:2512.20732](https://arxiv.org/abs/2512.20732) · local PDF: [`papers/02_ai_agents_engineering/AG-013_Mohammadzadeh2025_fem-bench-a-structured-scientific-reasoning-benchm.pdf`](../../../papers/02_ai_agents_engineering/AG-013_Mohammadzadeh2025_fem-bench-a-structured-scientific-reasoning-benchm.pdf)

Graduate-level FEM coding tasks with automatic checks; useful for testing any agent that writes our element or solver code.

### AG-014 — What Do CAE Simulation Agents Really Need Beyond a Generic Harness?

Shi & Zhang · 2026 · arXiv · **indirect**

[source](https://arxiv.org/abs/2609.03718) · [arXiv:2609.03718](https://arxiv.org/abs/2609.03718) · local PDF: [`papers/02_ai_agents_engineering/AG-014_Shi2026_what-do-cae-simulation-agents-really-need-beyond-a.pdf`](../../../papers/02_ai_agents_engineering/AG-014_Shi2026_what-do-cae-simulation-agents-really-need-beyond-a.pdf)

Analyses what tooling CAE agents need beyond a generic coding harness; informs the CAD/solver tool interface design.

### AG-015 — VFEAgent: A Multimodal Agent Framework for End-to-End Automated Finite Element Analysis

Zhang et al. · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2605.28978) · [arXiv:2605.28978](https://arxiv.org/abs/2605.28978) · local PDF: [`papers/02_ai_agents_engineering/AG-015_Zhang2026_vfeagent-a-multimodal-agent-framework-for-end-to-e.pdf`](../../../papers/02_ai_agents_engineering/AG-015_Zhang2026_vfeagent-a-multimodal-agent-framework-for-end-to-e.pdf)

Vision-augmented agent for FEA setup with an expert-graded benchmark including topology optimisation; a comparator for automated structural evaluation.

### AG-016 — MechAgents: Large language model multi-agent collaborations can solve mechanics problems, generate new data, and integrate knowledge

Ni & Buehler · 2024 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2311.08166) · [arXiv:2311.08166](https://arxiv.org/abs/2311.08166) · local PDF: [`papers/02_ai_agents_engineering/AG-016_Ni2024_mechagents-large-language-model-multi-agent-collab.pdf`](../../../papers/02_ai_agents_engineering/AG-016_Ni2024_mechagents-large-language-model-multi-agent-collab.pdf)

Multi-agent LLMs writing and checking FEniCS elasticity code; shows self-correction value and its limits.

### AG-017 — Large Language and Text-to-3D Models for Engineering Design Optimization

Rios et al. · 2023 · IEEE Symposium Series on Computational Intelligence · **direct**

[source](https://arxiv.org/abs/2307.01230) · [arXiv:2307.01230](https://arxiv.org/abs/2307.01230) · local PDF: [`papers/02_ai_agents_engineering/AG-017_Rios2023_large-language-and-text-to-3d-models-for-engineeri.pdf`](../../../papers/02_ai_agents_engineering/AG-017_Rios2023_large-language-and-text-to-3d-models-for-engineeri.pdf)

Text-to-3D car shapes optimised for CFD drag inside an evolutionary loop; directly relevant to generating vehicle bodies scored by aerodynamics.

### AG-018 — Drag-guided diffusion models for vehicle image generation

Aréchiga et al. · 2023 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2306.09935) · [arXiv:2306.09935](https://arxiv.org/abs/2306.09935) · local PDF: [`papers/02_ai_agents_engineering/AG-018_Arechiga2023_drag-guided-diffusion-models-for-vehicle-image-gen.pdf`](../../../papers/02_ai_agents_engineering/AG-018_Arechiga2023_drag-guided-diffusion-models-for-vehicle-image-gen.pdf)

Guides a generative model with a drag surrogate; illustrates the risk that surrogate guidance rewards surrogate errors.

### AG-019 — Text-to-CadQuery: A New Paradigm for CAD Generation with Scalable Large Model Capabilities

Xie & Ju · 2025 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2505.06507) · [arXiv:2505.06507](https://arxiv.org/abs/2505.06507) · local PDF: [`papers/02_ai_agents_engineering/AG-019_Xie2025_text-to-cadquery-a-new-paradigm-for-cad-generation.pdf`](../../../papers/02_ai_agents_engineering/AG-019_Xie2025_text-to-cadquery-a-new-paradigm-for-cad-generation.pdf)

Trains LLMs to emit CadQuery directly; the same CAD language our agents write, with a dataset and error statistics we can reuse.

### AG-020 — CAD-Recode: Reverse Engineering CAD Code from Point Clouds

Rukhovich et al. · 2024 · IEEE International Conference on Computer Vision · **indirect**

[source](https://arxiv.org/abs/2412.14042) · [arXiv:2412.14042](https://arxiv.org/abs/2412.14042) · local PDF: [`papers/02_ai_agents_engineering/AG-020_Rukhovich2024_cad-recode-reverse-engineering-cad-code-from-point.pdf`](../../../papers/02_ai_agents_engineering/AG-020_Rukhovich2024_cad-recode-reverse-engineering-cad-code-from-point.pdf)

Recovers CadQuery programs from point clouds with a large synthetic CadQuery corpus; useful data and a geometry-to-code check.

### AG-021 — Generating CAD Code with Vision-Language Models for 3D Designs

Alrashedy et al. · 2024 · International Conference on Learning Representations · **indirect**

[source](https://arxiv.org/abs/2410.05340) · [arXiv:2410.05340](https://arxiv.org/abs/2410.05340) · local PDF: [`papers/02_ai_agents_engineering/AG-021_Alrashedy2024_generating-cad-code-with-vision-language-models-fo.pdf`](../../../papers/02_ai_agents_engineering/AG-021_Alrashedy2024_generating-cad-code-with-vision-language-models-fo.pdf)

CADCodeVerify: the model renders its own CAD output and self-verifies; a cheap pre-check before our independent geometry witnesses.

### AG-022 — CADDesigner: Conceptual CAD Model Generation with a General-Purpose Agent

Fan et al. · 2025 · Comput. Aided Des. · **indirect**

[source](https://arxiv.org/abs/2508.01031) · [arXiv:2508.01031](https://arxiv.org/abs/2508.01031) · local PDF: [`papers/02_ai_agents_engineering/AG-022_Fan2025_caddesigner-conceptual-cad-model-generation-with-a.pdf`](../../../papers/02_ai_agents_engineering/AG-022_Fan2025_caddesigner-conceptual-cad-model-generation-with-a.pdf)

General-purpose agent with structured diagnostics for failed CAD scripts; relevant to turning kernel errors into repairable feedback.

### AG-023 — Towards High-Fidelity CAD Generation via LLM-Driven Program Generation and Text-Based B-Rep Primitive Grounding

Li et al. · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2603.11831) · [arXiv:2603.11831](https://arxiv.org/abs/2603.11831) · local PDF: [`papers/02_ai_agents_engineering/AG-023_Li2026_towards-high-fidelity-cad-generation-via-llm-drive.pdf`](../../../papers/02_ai_agents_engineering/AG-023_Li2026_towards-high-fidelity-cad-generation-via-llm-drive.pdf)

FutureCAD: LLM writes CadQuery and grounds references to B-rep primitives; addresses the fragile face/edge selection problem in generated CAD.

### AG-024 — Clarify Before You Draw: Proactive Agents for Robust Text-to-CAD Generation

Yuan et al. · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2602.03045) · [arXiv:2602.03045](https://arxiv.org/abs/2602.03045) · local PDF: [`papers/02_ai_agents_engineering/AG-024_Yuan2026_clarify-before-you-draw-proactive-agents-for-robus.pdf`](../../../papers/02_ai_agents_engineering/AG-024_Yuan2026_clarify-before-you-draw-proactive-agents-for-robus.pdf)

Agents that resolve underspecified CAD requests before drawing; relevant to typed interface specifications for generated parts.

### AG-025 — Test-Time Scaling for CAD Generation via Verifier-Free Consensus Selection

Haag et al. · 2026 · arXiv · **indirect**

[source](https://arxiv.org/abs/2608.09706) · [arXiv:2608.09706](https://arxiv.org/abs/2608.09706) · local PDF: [`papers/02_ai_agents_engineering/AG-025_Haag2026_test-time-scaling-for-cad-generation-via-verifier.pdf`](../../../papers/02_ai_agents_engineering/AG-025_Haag2026_test-time-scaling-for-cad-generation-via-verifier.pdf)

Selects among sampled CAD programs by consensus; a cheap filter, but consensus is not a physical check.

### AG-026 — CADEngBench: It Looks Like CAD, but Does It Work? Evaluating Parametric Design, Assembly Reasoning, and Physics Simulation

Singh et al. · 2026 · arXiv · **direct**

[source](https://arxiv.org/abs/2608.09296) · [arXiv:2608.09296](https://arxiv.org/abs/2608.09296) · local PDF: [`papers/02_ai_agents_engineering/AG-026_Singh2026_cadengbench-it-looks-like-cad-but-does-it-work-eva.pdf`](../../../papers/02_ai_agents_engineering/AG-026_Singh2026_cadengbench-it-looks-like-cad-but-does-it-work-eva.pdf)

Benchmark that scores generated CAD on assembly and physics, not appearance; the same principle as our geometry-is-causal-input rule.

### AG-027 — Automated Design Optimization via Strategic Search with Large Language Models

Carreon et al. · 2025 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2511.22651) · [arXiv:2511.22651](https://arxiv.org/abs/2511.22651) · local PDF: [`papers/02_ai_agents_engineering/AG-027_Carreon2025_automated-design-optimization-via-strategic-search.pdf`](../../../papers/02_ai_agents_engineering/AG-027_Carreon2025_automated-design-optimization-via-strategic-search.pdf)

LLM-guided strategic search for engineering design optimisation; a comparator for LLM-proposed parameter moves.

### AG-028 — Generative Reliability-Based Design Optimization Using In-Context Learning Capabilities of Large Language Models

Jiang et al. · 2025 · Journal of Mechanical Design · **indirect**

[source](https://arxiv.org/abs/2503.22401) · [arXiv:2503.22401](https://arxiv.org/abs/2503.22401) · local PDF: [`papers/02_ai_agents_engineering/AG-028_Jiang2025_generative-reliability-based-design-optimization-u.pdf`](../../../papers/02_ai_agents_engineering/AG-028_Jiang2025_generative-reliability-based-design-optimization-u.pdf)

LLM in-context design generation under reliability constraints; relevant to uncertainty-aware gates.

### AG-029 — From Concept to Manufacturing: Evaluating Vision-Language Models for Engineering Design

Picard et al. · 2023 · Artificial Intelligence Review · **indirect**

[source](https://arxiv.org/abs/2311.12668) · [arXiv:2311.12668](https://arxiv.org/abs/2311.12668) · local PDF: [`papers/02_ai_agents_engineering/AG-029_Picard2023_from-concept-to-manufacturing-evaluating-vision-la.pdf`](../../../papers/02_ai_agents_engineering/AG-029_Picard2023_from-concept-to-manufacturing-evaluating-vision-la.pdf)

Broad evaluation of vision-language models on engineering design tasks; documents where they cannot be trusted.

### AG-030 — Deep Generative Models in Engineering Design: A Review

Regenwetter et al. · 2022 · Journal of Mechanical Design · **indirect**

[source](https://arxiv.org/abs/2110.10863) · [arXiv:2110.10863](https://arxiv.org/abs/2110.10863) · local PDF: [`papers/02_ai_agents_engineering/AG-030_Regenwetter2022_deep-generative-models-in-engineering-design-a-rev.pdf`](../../../papers/02_ai_agents_engineering/AG-030_Regenwetter2022_deep-generative-models-in-engineering-design-a-rev.pdf)

Review of generative models for engineering design, including validity and performance gaps; a map of methods for geometry proposal.

### AG-031 — Beyond Statistical Similarity: Rethinking Metrics for Deep Generative Models in Engineering Design

Regenwetter et al. · 2023 · Comput. Aided Des. · **direct**

[source](https://arxiv.org/abs/2302.02913) · [arXiv:2302.02913](https://arxiv.org/abs/2302.02913) · local PDF: [`papers/02_ai_agents_engineering/AG-031_Regenwetter2023_beyond-statistical-similarity-rethinking-metrics-f.pdf`](../../../papers/02_ai_agents_engineering/AG-031_Regenwetter2023_beyond-statistical-similarity-rethinking-metrics-f.pdf)

Argues generated designs must be scored on constraint satisfaction, performance and novelty rather than similarity to data; aligned with our discovery criteria.

### AG-032 — Constraining Generative Models for Engineering Design with Negative Data

Giannone et al. · 2023 · Trans. Mach. Learn. Res. · **indirect**

[source](https://arxiv.org/abs/2306.15166) · [arXiv:2306.15166](https://arxiv.org/abs/2306.15166) · local PDF: [`papers/02_ai_agents_engineering/AG-032_Giannone2023_constraining-generative-models-for-engineering-des.pdf`](../../../papers/02_ai_agents_engineering/AG-032_Giannone2023_constraining-generative-models-for-engineering-des.pdf)

Trains on infeasible examples to keep generators inside constraints; our rejection ledgers are exactly such negative data.

### AG-033 — BIKED: A Dataset for Computational Bicycle Design with Machine Learning Benchmarks

Regenwetter et al. · 2022 · Journal of Mechanical Design · **data/findings**

[source](https://doi.org/10.1115/1.4052585) · [arXiv:2103.05844](https://arxiv.org/abs/2103.05844) · local PDF: [`papers/02_ai_agents_engineering/AG-033_Regenwetter2022_biked-a-dataset-for-computational-bicycle-design-w.pdf`](../../../papers/02_ai_agents_engineering/AG-033_Regenwetter2022_biked-a-dataset-for-computational-bicycle-design-w.pdf)

Parametric vehicle-design dataset with structural and performance labels; a public example of vehicle design data with validity checks.

### AG-034 — The impact of AI on engineering design procedures for dynamical systems

Payrebrune et al. · 2024 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2412.12230) · [arXiv:2412.12230](https://arxiv.org/abs/2412.12230) · local PDF: [`papers/02_ai_agents_engineering/AG-034_Payrebrune2024_the-impact-of-ai-on-engineering-design-procedures.pdf`](../../../papers/02_ai_agents_engineering/AG-034_Payrebrune2024_the-impact-of-ai-on-engineering-design-procedures.pdf)

Discusses how AI changes design procedures for dynamical systems, including validation obligations.

### AG-035 — Eureka: Human-Level Reward Design via Coding Large Language Models

Ma et al. · 2023 · International Conference on Learning Representations · **indirect**

[source](https://arxiv.org/abs/2310.12931) · [arXiv:2310.12931](https://arxiv.org/abs/2310.12931) · local PDF: [`papers/02_ai_agents_engineering/AG-035_Ma2023_eureka-human-level-reward-design-via-coding-large.pdf`](../../../papers/02_ai_agents_engineering/AG-035_Ma2023_eureka-human-level-reward-design-via-coding-large.pdf)

LLM writes reward code for control tasks; a caution that agent-written objectives must be frozen and audited before search.

### AG-036 — RoboMorph: Evolving Robot Morphology using Large Language Models

Qiu et al. · 2024 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2407.08626) · [arXiv:2407.08626](https://arxiv.org/abs/2407.08626) · local PDF: [`papers/02_ai_agents_engineering/AG-036_Qiu2024_robomorph-evolving-robot-morphology-using-large-la.pdf`](../../../papers/02_ai_agents_engineering/AG-036_Qiu2024_robomorph-evolving-robot-morphology-using-large-la.pdf)

LLM-driven evolutionary search over modular robot morphologies; a direct analogue of LLM-guided topology mutation.

### AG-037 — Text2Robot: Evolutionary Robot Design from Text Descriptions

Ringel et al. · 2024 · IEEE International Conference on Robotics and Automation · **indirect**

[source](https://arxiv.org/abs/2406.19963) · [arXiv:2406.19963](https://arxiv.org/abs/2406.19963) · local PDF: [`papers/02_ai_agents_engineering/AG-037_Ringel2024_text2robot-evolutionary-robot-design-from-text-des.pdf`](../../../papers/02_ai_agents_engineering/AG-037_Ringel2024_text2robot-evolutionary-robot-design-from-text-des.pdf)

Text to evolved, fabricated legged robots; shows the manufacturing constraints needed for generated bodies to be buildable.

### AG-038 — Large Language Models as Optimizers

Yang et al. · 2023 · International Conference on Learning Representations · **indirect**

[source](https://arxiv.org/abs/2309.03409) · [arXiv:2309.03409](https://arxiv.org/abs/2309.03409) · local PDF: [`papers/02_ai_agents_engineering/AG-038_Yang2023_large-language-models-as-optimizers.pdf`](../../../papers/02_ai_agents_engineering/AG-038_Yang2023_large-language-models-as-optimizers.pdf)

OPRO: LLMs propose solutions from a scored history; a baseline for LLM-as-optimiser behaviour.

### AG-039 — CodeEvolve: an open-source evolutionary framework for algorithmic discovery and optimization

Assumpção et al. · 2025 · arXiv · **indirect**

[source](https://arxiv.org/abs/2510.14150) · [arXiv:2510.14150](https://arxiv.org/abs/2510.14150) · local PDF: [`papers/02_ai_agents_engineering/AG-039_Assumpcao2025_codeevolve-an-open-source-evolutionary-framework-f.pdf`](../../../papers/02_ai_agents_engineering/AG-039_Assumpcao2025_codeevolve-an-open-source-evolutionary-framework-f.pdf)

Open-source AlphaEvolve-style framework; a runnable reference implementation for LLM evolutionary search.

### AG-040 — OMNI: Open-endedness via Models of human Notions of Interestingness

Zhang et al. · 2023 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2306.01711) · [arXiv:2306.01711](https://arxiv.org/abs/2306.01711) · local PDF: [`papers/02_ai_agents_engineering/AG-040_Zhang2023_omni-open-endedness-via-models-of-human-notions-of.pdf`](../../../papers/02_ai_agents_engineering/AG-040_Zhang2023_omni-open-endedness-via-models-of-human-notions-of.pdf)

Uses a foundation model to judge which tasks are interesting; relevant to deciding which novel mechanisms deserve evaluation budget.

### AG-041 — Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents

Ren et al. · 2025 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2503.24047) · [arXiv:2503.24047](https://arxiv.org/abs/2503.24047) · local PDF: [`papers/02_ai_agents_engineering/AG-041_Ren2025_towards-scientific-intelligence-a-survey-of-llm-ba.pdf`](../../../papers/02_ai_agents_engineering/AG-041_Ren2025_towards-scientific-intelligence-a-survey-of-llm-ba.pdf)

Survey of LLM scientific agents; context for positioning an engineering-discovery agent.

### AG-042 — LLEMA: Evolutionary Search with LLMs for Multi-Objective Materials Discovery

Abhyankar et al. · 2025 · arXiv · **indirect**

[source](https://arxiv.org/abs/2510.22503) · [arXiv:2510.22503](https://arxiv.org/abs/2510.22503) · local PDF: [`papers/02_ai_agents_engineering/AG-042_Abhyankar2025_llema-evolutionary-search-with-llms-for-multi-obje.pdf`](../../../papers/02_ai_agents_engineering/AG-042_Abhyankar2025_llema-evolutionary-search-with-llms-for-multi-obje.pdf)

LLM-guided evolutionary search in materials; the project restricts itself to catalog materials, so this is context rather than a method to adopt.

### AG-043 — Physical Design using Differentiable Learned Simulators

Allen et al. · 2022 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2202.00728) · [arXiv:2202.00728](https://arxiv.org/abs/2202.00728) · local PDF: [`papers/02_ai_agents_engineering/AG-043_Allen2022_physical-design-using-differentiable-learned-simul.pdf`](../../../papers/02_ai_agents_engineering/AG-043_Allen2022_physical-design-using-differentiable-learned-simul.pdf)

Optimises designs through learned graph-network simulators (airfoils, fluid tools); shows both the speed and the surrogate-exploitation risk.


## Quality diversity, search algorithms, surrogates and multifidelity

Algorithms for spending evaluation budget on diverse, high-quality and credible candidates: MAP-Elites and descendants, novelty search, evolution strategies, Bayesian and multifidelity optimisation, and sim-to-real transferability.

### QD-001 — Illuminating search spaces by mapping elites

Mouret & Clune · 2015 · arXiv.org · **direct** · Work 102 catalog P11

[source](https://arxiv.org/abs/1504.04909) · [arXiv:1504.04909](https://arxiv.org/abs/1504.04909) · local PDF: [`papers/03_search_qd_multifidelity/QD-001_Mouret2015_illuminating-search-spaces-by-mapping-elites.pdf`](../../../papers/03_search_qd_multifidelity/QD-001_Mouret2015_illuminating-search-spaces-by-mapping-elites.pdf)

MAP-Elites: keeps the best design per behaviour cell; the base algorithm of the executable morphology archive (Work 099).

### QD-002 — Quality Diversity: A New Frontier for Evolutionary Computation

Pugh et al. · 2016 · Frontiers in Robotics and AI · **indirect** · Work 102 catalog P12

[source](https://doi.org/10.3389/frobt.2016.00040) · local PDF: [`papers/03_search_qd_multifidelity/QD-002_Pugh2016_quality-diversity-a-new-frontier-for-evolutionary.pdf`](../../../papers/03_search_qd_multifidelity/QD-002_Pugh2016_quality-diversity-a-new-frontier-for-evolutionary.pdf)

Defines quality diversity and separates coverage, novelty and quality; vocabulary for the design-diversity contract (Work 090).

### QD-003 — Data-Efficient Design Exploration through Surrogate-Assisted Illumination

Gaier et al. · 2018 · Evolutionary Computation · **direct** · Work 102 catalog P13

[source](https://arxiv.org/abs/1806.05865) · [arXiv:1806.05865](https://arxiv.org/abs/1806.05865) · local PDF: [`papers/03_search_qd_multifidelity/QD-003_Gaier2018_data-efficient-design-exploration-through-surrogat.pdf`](../../../papers/03_search_qd_multifidelity/QD-003_Gaier2018_data-efficient-design-exploration-through-surrogat.pdf)

SAIL combines Gaussian-process surrogates with MAP-Elites on aerodynamic shapes; the direct method for expensive-evaluator illumination.

### QD-004 — Covariance Matrix Adaptation MAP-Annealing

Fontaine & Nikolaidis · 2022 · Annual Conference on Genetic and Evolutionary Computation · **indirect** · Work 102 catalog P14

[source](https://arxiv.org/abs/2205.10752) · [arXiv:2205.10752](https://arxiv.org/abs/2205.10752) · local PDF: [`papers/03_search_qd_multifidelity/QD-004_Fontaine2022_covariance-matrix-adaptation-map-annealing.pdf`](../../../papers/03_search_qd_multifidelity/QD-004_Fontaine2022_covariance-matrix-adaptation-map-annealing.pdf)

CMA-MAE improves continuous QD search; a stronger continuous-parameter baseline once basic MAP-Elites works.

### QD-005 — Survey of multifidelity methods in uncertainty propagation, inference, and optimization

Peherstorfer et al. · 2018 · SIAM Review · **direct** · Work 102 catalog P15

[source](https://arxiv.org/abs/1806.10761) · [arXiv:1806.10761](https://arxiv.org/abs/1806.10761) · local PDF: [`papers/03_search_qd_multifidelity/QD-005_Peherstorfer2018_survey-of-multifidelity-methods-in-uncertainty-pro.pdf`](../../../papers/03_search_qd_multifidelity/QD-005_Peherstorfer2018_survey-of-multifidelity-methods-in-uncertainty-pro.pdf)

The reference for combining cheap and expensive models without trusting the cheap one; underpins the fidelity ladder and promotion audits.

### QD-006 — Multi-fidelity Bayesian Optimisation with Continuous Approximations

Kandasamy et al. · 2017 · International Conference on Machine Learning · **indirect** · Work 102 catalog P16

[source](https://arxiv.org/abs/1703.06240) · [arXiv:1703.06240](https://arxiv.org/abs/1703.06240) · local PDF: [`papers/03_search_qd_multifidelity/QD-006_Kandasamy2017_multi-fidelity-bayesian-optimisation-with-continuo.pdf`](../../../papers/03_search_qd_multifidelity/QD-006_Kandasamy2017_multi-fidelity-bayesian-optimisation-with-continuo.pdf)

BOCA chooses both candidate and fidelity by cost; relevant when mesh size or time step is a controllable fidelity.

### QD-007 — Crossing the Reality Gap: a Short Introduction to the Transferability Approach

Mouret et al. · 2013 · arXiv.org · **direct** · Work 102 catalog P17

[source](https://arxiv.org/abs/1307.1870) · [arXiv:1307.1870](https://arxiv.org/abs/1307.1870) · local PDF: [`papers/03_search_qd_multifidelity/QD-007_Mouret2013_crossing-the-reality-gap-a-short-introduction-to-t.pdf`](../../../papers/03_search_qd_multifidelity/QD-007_Mouret2013_crossing-the-reality-gap-a-short-introduction-to-t.pdf)

Learns which simulated behaviours transfer to reality and optimises for transferability; a model for promotion-aware selection.

### QD-008 — The Transferability Approach: Crossing the Reality Gap in Evolutionary Robotics

Koos et al. · 2013 · IEEE Transactions on Evolutionary Computation · **direct**

[source](https://doi.org/10.1109/tevc.2012.2185849) · no local copy (no open-access copy found)

Full journal version of the transferability approach with experiments; the evidence behind QD-007.

### QD-009 — Abandoning Objectives: Evolution Through the Search for Novelty Alone

Lehman & Stanley · 2011 · Evolutionary Computation · **direct**

[source](https://doi.org/10.1162/evco_a_00025) · local PDF: [`papers/03_search_qd_multifidelity/QD-009_Lehman2011_abandoning-objectives-evolution-through-the-search.pdf`](../../../papers/03_search_qd_multifidelity/QD-009_Lehman2011_abandoning-objectives-evolution-through-the-search.pdf)

Novelty search escapes deceptive objectives; relevant when race time alone traps search in conventional layouts.

### QD-010 — Evolving a diversity of virtual creatures through novelty search and local competition

Lehman & Stanley · 2011 · Proceedings of the 13th annual conference on Genetic and evolutionary computation · **direct**

[source](https://doi.org/10.1145/2001576.2001606) · no local copy (no open-access copy found)

Novelty search with local competition on morphologies; the direct precedent for diverse-yet-competitive vehicle archives.

### QD-011 — Using Centroidal Voronoi Tessellations to Scale Up the Multidimensional Archive of Phenotypic Elites Algorithm

Vassiliades et al. · 2018 · IEEE Transactions on Evolutionary Computation · **indirect**

[source](https://arxiv.org/abs/1610.05729) · [arXiv:1610.05729](https://arxiv.org/abs/1610.05729) · local PDF: [`papers/03_search_qd_multifidelity/QD-011_Vassiliades2018_using-centroidal-voronoi-tessellations-to-scale-up.pdf`](../../../papers/03_search_qd_multifidelity/QD-011_Vassiliades2018_using-centroidal-voronoi-tessellations-to-scale-up.pdf)

CVT-MAP-Elites keeps archive size fixed in high-dimensional descriptor spaces; needed if vehicle descriptors grow.

### QD-012 — Covariance Matrix Adaptation for the Rapid Illumination of Behavior Space

Fontaine et al. · 2020 · Annual Conference on Genetic and Evolutionary Computation · **indirect**

[source](https://arxiv.org/abs/1912.02400) · [arXiv:1912.02400](https://arxiv.org/abs/1912.02400) · local PDF: [`papers/03_search_qd_multifidelity/QD-012_Fontaine2020_covariance-matrix-adaptation-for-the-rapid-illumin.pdf`](../../../papers/03_search_qd_multifidelity/QD-012_Fontaine2020_covariance-matrix-adaptation-for-the-rapid-illumin.pdf)

CMA-ME: CMA-ES emitters inside MAP-Elites; a standard QD comparator.

### QD-013 — pyribs: A Bare-Bones Python Library for Quality Diversity Optimization

Tjanaka et al. · 2023 · Annual Conference on Genetic and Evolutionary Computation · **indirect**

[source](https://arxiv.org/abs/2303.00191) · [arXiv:2303.00191](https://arxiv.org/abs/2303.00191) · local PDF: [`papers/03_search_qd_multifidelity/QD-013_Tjanaka2023_pyribs-a-bare-bones-python-library-for-quality-div.pdf`](../../../papers/03_search_qd_multifidelity/QD-013_Tjanaka2023_pyribs-a-bare-bones-python-library-for-quality-div.pdf)

Reference QD library with archives and emitters; a tested implementation to cross-check our archive code.

### QD-014 — Accelerated Quality-Diversity through Massive Parallelism

Lim et al. · 2023 · Trans. Mach. Learn. Res. · **indirect**

[source](https://arxiv.org/abs/2202.01258) · [arXiv:2202.01258](https://arxiv.org/abs/2202.01258) · local PDF: [`papers/03_search_qd_multifidelity/QD-014_Lim2023_accelerated-quality-diversity-through-massive-para.pdf`](../../../papers/03_search_qd_multifidelity/QD-014_Lim2023_accelerated-quality-diversity-through-massive-para.pdf)

QDax: QD on accelerators with large batches; relevant to compute-ledger comparisons of batch size and evaluations.

### QD-015 — Multi-Objective Quality Diversity Optimization

Pierrot et al. · 2022 · Annual Conference on Genetic and Evolutionary Computation · **direct**

[source](https://arxiv.org/abs/2202.03057) · [arXiv:2202.03057](https://arxiv.org/abs/2202.03057) · local PDF: [`papers/03_search_qd_multifidelity/QD-015_Pierrot2022_multi-objective-quality-diversity-optimization.pdf`](../../../papers/03_search_qd_multifidelity/QD-015_Pierrot2022_multi-objective-quality-diversity-optimization.pdf)

MOME keeps a Pareto front per cell; fits H2's race time/energy/mass/reliability trade-offs inside a diverse archive.

### QD-016 — Quality Diversity for Multi-task Optimization

Mouret & Maguire · 2020 · Annual Conference on Genetic and Evolutionary Computation · **direct**

[source](https://arxiv.org/abs/2003.04407) · [arXiv:2003.04407](https://arxiv.org/abs/2003.04407) · local PDF: [`papers/03_search_qd_multifidelity/QD-016_Mouret2020_quality-diversity-for-multi-task-optimization.pdf`](../../../papers/03_search_qd_multifidelity/QD-016_Mouret2020_quality-diversity-for-multi-task-optimization.pdf)

One search solving many related tasks with shared elites; maps directly onto one design search across many race environments.

### QD-017 — Multi-Task Multi-Behavior MAP-Elites

Anne & Mouret · 2023 · GECCO Companion · **indirect**

[source](https://arxiv.org/abs/2305.01264) · [arXiv:2305.01264](https://arxiv.org/abs/2305.01264) · local PDF: [`papers/03_search_qd_multifidelity/QD-017_Anne2023_multi-task-multi-behavior-map-elites.pdf`](../../../papers/03_search_qd_multifidelity/QD-017_Anne2023_multi-task-multi-behavior-map-elites.pdf)

Extends multi-task QD to diverse behaviours per task; relevant to environment-specialised archives (H3).

### QD-018 — BOP-Elites, a Bayesian Optimisation algorithm for Quality-Diversity search

Kent & Branke · 2020 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2005.04320) · [arXiv:2005.04320](https://arxiv.org/abs/2005.04320) · local PDF: [`papers/03_search_qd_multifidelity/QD-018_Kent2020_bop-elites-a-bayesian-optimisation-algorithm-for-q.pdf`](../../../papers/03_search_qd_multifidelity/QD-018_Kent2020_bop-elites-a-bayesian-optimisation-algorithm-for-q.pdf)

Bayesian optimisation for QD with very few evaluations; relevant when each evaluation is a CFD or FE run.

### QD-019 — Designing Air Flow with Surrogate-assisted Phenotypic Niching

Hagg et al. · 2020 · Lecture Notes in Computer Science · **direct**

[source](https://doi.org/10.1007/978-3-030-58112-1_10) · [arXiv:2105.04256](https://arxiv.org/abs/2105.04256) · local PDF: [`papers/03_search_qd_multifidelity/QD-019_Hagg2020_designing-air-flow-with-surrogate-assisted-phenoty.pdf`](../../../papers/03_search_qd_multifidelity/QD-019_Hagg2020_designing-air-flow-with-surrogate-assisted-phenoty.pdf)

Surrogate-assisted QD for air-flow design with phenotypic niching; direct method for diverse aero/cooling geometry.

### QD-020 — Prototype Discovery using Quality-Diversity

Hagg et al. · 2018 · Lecture Notes in Computer Science · **indirect**

[source](https://doi.org/10.1007/978-3-319-99253-2_40) · [arXiv:1807.09488](https://arxiv.org/abs/1807.09488) · local PDF: [`papers/03_search_qd_multifidelity/QD-020_Hagg2018_prototype-discovery-using-quality-diversity.pdf`](../../../papers/03_search_qd_multifidelity/QD-020_Hagg2018_prototype-discovery-using-quality-diversity.pdf)

Clusters a QD archive into prototypes for human review; useful for summarising which architecture families emerged.

### QD-021 — Robots that can adapt like animals

Cully et al. · 2015 · Nature · **indirect**

[source](https://arxiv.org/abs/1407.3501) · [arXiv:1407.3501](https://arxiv.org/abs/1407.3501) · local PDF: [`papers/03_search_qd_multifidelity/QD-021_Cully2015_robots-that-can-adapt-like-animals.pdf`](../../../papers/03_search_qd_multifidelity/QD-021_Cully2015_robots-that-can-adapt-like-animals.pdf)

A precomputed MAP-Elites archive is reused for fast recovery after damage; a pattern for reusing archives under degraded conditions.

### QD-022 — Open-ended search for environments and adapted agents using MAP-Elites

Norstein et al. · 2023 · EvoApplications · **indirect**

[source](https://arxiv.org/abs/2305.01153) · [arXiv:2305.01153](https://arxiv.org/abs/2305.01153) · local PDF: [`papers/03_search_qd_multifidelity/QD-022_Norstein2023_open-ended-search-for-environments-and-adapted-age.pdf`](../../../papers/03_search_qd_multifidelity/QD-022_Norstein2023_open-ended-search-for-environments-and-adapted-age.pdf)

MAP-Elites over environments and agents together; relevant to curricula over tracks and conditions.

### QD-023 — The CMA Evolution Strategy: A Tutorial

Hansen · 2016 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/1604.00772) · [arXiv:1604.00772](https://arxiv.org/abs/1604.00772) · local PDF: [`papers/03_search_qd_multifidelity/QD-023_Hansen2016_the-cma-evolution-strategy-a-tutorial.pdf`](../../../papers/03_search_qd_multifidelity/QD-023_Hansen2016_the-cma-evolution-strategy-a-tutorial.pdf)

Authoritative CMA-ES tutorial; the default continuous optimiser for tuned fixed-topology baselines.

### QD-024 — A fast and elitist multiobjective genetic algorithm: NSGA-II

Deb et al. · 2002 · IEEE Transactions on Evolutionary Computation · **indirect**

[source](https://doi.org/10.1109/4235.996017) · no local copy (no open-access copy found)

NSGA-II, the standard multi-objective baseline that any new search method should be compared against.

### QD-025 — Practical Bayesian Optimization of Machine Learning Algorithms

Snoek et al. · 2012 · Neural Information Processing Systems · **indirect**

[source](https://arxiv.org/abs/1206.2944) · [arXiv:1206.2944](https://arxiv.org/abs/1206.2944) · local PDF: [`papers/03_search_qd_multifidelity/QD-025_Snoek2012_practical-bayesian-optimization-of-machine-learnin.pdf`](../../../papers/03_search_qd_multifidelity/QD-025_Snoek2012_practical-bayesian-optimization-of-machine-learnin.pdf)

Practical Gaussian-process Bayesian optimisation including cost-aware acquisition; a baseline for expensive parameter tuning.

### QD-026 — A Tutorial on Bayesian Optimization

Frazier · 2018 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/1807.02811) · [arXiv:1807.02811](https://arxiv.org/abs/1807.02811) · local PDF: [`papers/03_search_qd_multifidelity/QD-026_Frazier2018_a-tutorial-on-bayesian-optimization.pdf`](../../../papers/03_search_qd_multifidelity/QD-026_Frazier2018_a-tutorial-on-bayesian-optimization.pdf)

Clear tutorial of Bayesian optimisation including multi-fidelity and noisy settings.

### QD-027 — Scalable Global Optimization via Local Bayesian Optimization

Eriksson et al. · 2019 · Neural Information Processing Systems · **indirect**

[source](https://arxiv.org/abs/1910.01739) · [arXiv:1910.01739](https://arxiv.org/abs/1910.01739) · local PDF: [`papers/03_search_qd_multifidelity/QD-027_Eriksson2019_scalable-global-optimization-via-local-bayesian-op.pdf`](../../../papers/03_search_qd_multifidelity/QD-027_Eriksson2019_scalable-global-optimization-via-local-bayesian-op.pdf)

TuRBO trust-region Bayesian optimisation for higher dimensions; a strong baseline for tuning conventional vehicles.

### QD-028 — Bayesian Optimization of Combinatorial Structures

Baptista & Poloczek · 2018 · International Conference on Machine Learning · **indirect**

[source](https://arxiv.org/abs/1806.08838) · [arXiv:1806.08838](https://arxiv.org/abs/1806.08838) · local PDF: [`papers/03_search_qd_multifidelity/QD-028_Baptista2018_bayesian-optimization-of-combinatorial-structures.pdf`](../../../papers/03_search_qd_multifidelity/QD-028_Baptista2018_bayesian-optimization-of-combinatorial-structures.pdf)

BOCS handles discrete, combinatorial design variables; relevant to discrete topology choices.

### QD-029 — Multi-fidelity optimization via surrogate modelling

Forrester et al. · 2007 · Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences · **direct**

[source](https://doi.org/10.1098/rspa.2007.1900) · local PDF: [`papers/03_search_qd_multifidelity/QD-029_Forrester2007_multi-fidelity-optimization-via-surrogate-modellin.pdf`](../../../papers/03_search_qd_multifidelity/QD-029_Forrester2007_multi-fidelity-optimization-via-surrogate-modellin.pdf)

Co-kriging multi-fidelity surrogate optimisation with an aerodynamic example; the classic engineering formulation.

### QD-030 — Predicting the output from a complex computer code when fast approximations are available

Kennedy · 2000 · Biometrika · **indirect**

[source](https://doi.org/10.1093/biomet/87.1.1) · no local copy (no open-access copy found)

Autoregressive multi-fidelity Gaussian-process model; the statistical basis of co-kriging across fidelity levels.

### QD-031 — Nonlinear information fusion algorithms for data-efficient multi-fidelity modelling

Perdikaris et al. · 2017 · Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences · **indirect**

[source](https://doi.org/10.1098/rspa.2016.0751) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.ncbi.nlm.nih.gov/pmc/articles/5332612)

Nonlinear multi-fidelity Gaussian processes for when cheap and expensive models disagree non-linearly, as Level 0 and refined models do.

### QD-032 — A composite neural network that learns from multi-fidelity data: Application to function approximation and inverse PDE problems

Meng & Karniadakis · 2020 · Journal of Computational Physics · **indirect**

[source](https://arxiv.org/abs/1903.00104) · [arXiv:1903.00104](https://arxiv.org/abs/1903.00104) · local PDF: [`papers/03_search_qd_multifidelity/QD-032_Meng2020_a-composite-neural-network-that-learns-from-multi.pdf`](../../../papers/03_search_qd_multifidelity/QD-032_Meng2020_a-composite-neural-network-that-learns-from-multi.pdf)

Neural multi-fidelity model; an alternative to Gaussian processes at larger data sizes.

### QD-033 — Efficient Global Optimization of Expensive Black-Box Functions

Jones et al. · 1998 · Journal of Global Optimization · **indirect**

[source](https://doi.org/10.1023/a:1008306431147) · [arXiv:2211.00162](https://arxiv.org/abs/2211.00162) · local PDF: [`papers/03_search_qd_multifidelity/QD-033_Jones1998_efficient-global-optimization-of-expensive-black-b.pdf`](../../../papers/03_search_qd_multifidelity/QD-033_Jones1998_efficient-global-optimization-of-expensive-black-b.pdf)

EGO and expected improvement; the foundation of surrogate-based optimisation of expensive simulations.

### QD-034 — Dominated Novelty Search: Rethinking Local Competition in Quality-Diversity

Bahlous-Boldi et al. · 2025 · Proceedings of the Genetic and Evolutionary Computation Conference · **indirect**

[source](https://doi.org/10.1145/3712256.3726310) · [arXiv:2502.00593](https://arxiv.org/abs/2502.00593) · local PDF: [`papers/03_search_qd_multifidelity/QD-034_Boldi2025_dominated-novelty-search-rethinking-local-competit.pdf`](../../../papers/03_search_qd_multifidelity/QD-034_Boldi2025_dominated-novelty-search-rethinking-local-competit.pdf)

Replaces grid archives with competition-based fitness transformation; an archive-free QD alternative for unbounded descriptor spaces.

### QD-035 — Aerodynamic Design Exploration through Surrogate-Assisted Illumination

Gaier et al. · 2017 · 18th AIAA/ISSMO Multidisciplinary Analysis and Optimization Conference · **direct**

[source](https://doi.org/10.2514/6.2017-3330) · local PDF: [`papers/03_search_qd_multifidelity/QD-035_Gaier2017_aerodynamic-design-exploration-through-surrogate-a.pdf`](../../../papers/03_search_qd_multifidelity/QD-035_Gaier2017_aerodynamic-design-exploration-through-surrogate-a.pdf)

The aerodynamic application paper of SAIL, with 2D airfoil CFD; closest to diverse aero-surface search.

### QD-036 — Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations

Raissi et al. · 2017 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/1711.10561) · [arXiv:1711.10561](https://arxiv.org/abs/1711.10561) · local PDF: [`papers/03_search_qd_multifidelity/QD-036_Raissi2017_physics-informed-deep-learning-part-i-data-driven.pdf`](../../../papers/03_search_qd_multifidelity/QD-036_Raissi2017_physics-informed-deep-learning-part-i-data-driven.pdf)

Physics-informed neural networks; a surrogate family that embeds governing equations, relevant when data is scarce.


## CAD, B-rep and assembly representation, generation and datasets

How solid models, construction sequences, joints and assemblies are represented, learned and generated, plus the public CAD datasets. Relevant to the parametric/freeform B-rep grammars, semantic geometry witnesses, joint kernel and part-resolution work (Works 078-096, 135-142).

### CAD-001 — DeepCAD: A Deep Generative Network for Computer-Aided Design Models

Wu et al. · 2021 · IEEE International Conference on Computer Vision · **indirect** · Work 102 catalog P21

[source](https://arxiv.org/abs/2105.09492) · [arXiv:2105.09492](https://arxiv.org/abs/2105.09492) · local PDF: [`papers/04_cad_brep_assembly/CAD-001_Wu2021_deepcad-a-deep-generative-network-for-computer-aid.pdf`](../../../papers/04_cad_brep_assembly/CAD-001_Wu2021_deepcad-a-deep-generative-network-for-computer-aid.pdf)

Generates sketch-and-extrude construction sequences; a proposal representation whose outputs still need our load-path and process gates.

### CAD-002 — Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts

Khan et al. · 2024 · arXiv.org · **indirect** · Work 102 catalog P22

[source](https://arxiv.org/abs/2409.17106) · [arXiv:2409.17106](https://arxiv.org/abs/2409.17106) · local PDF: [`papers/04_cad_brep_assembly/CAD-002_Khan2024_text2cad-generating-sequential-cad-models-from-beg.pdf`](../../../papers/04_cad_brep_assembly/CAD-002_Khan2024_text2cad-generating-sequential-cad-models-from-beg.pdf)

Text to CAD sequences with graded prompt levels; a data and evaluation reference for language-to-geometry proposals.

### CAD-003 — BRepNet: A topological message passing system for solid models

Lambourne et al. · 2021 · Computer Vision and Pattern Recognition · **indirect** · Work 102 catalog P23

[source](https://arxiv.org/abs/2104.00706) · [arXiv:2104.00706](https://arxiv.org/abs/2104.00706) · local PDF: [`papers/04_cad_brep_assembly/CAD-003_Lambourne2021_brepnet-a-topological-message-passing-system-for-s.pdf`](../../../papers/04_cad_brep_assembly/CAD-003_Lambourne2021_brepnet-a-topological-message-passing-system-for-s.pdf)

Learns directly on B-rep face/edge/coedge topology; candidate descriptor for mechanically meaningful diversity measures.

### CAD-004 — Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences

Willis et al. · 2021 · ACM Transactions on Graphics · **data/findings** · Work 102 catalog P24

[source](https://arxiv.org/abs/2010.02392) · [arXiv:2010.02392](https://arxiv.org/abs/2010.02392) · local PDF: [`papers/04_cad_brep_assembly/CAD-004_Willis2021_fusion-360-gallery-a-dataset-and-environment-for-p.pdf`](../../../papers/04_cad_brep_assembly/CAD-004_Willis2021_fusion-360-gallery-a-dataset-and-environment-for-p.pdf)

Human CAD construction sequences plus a reconstruction environment; data for learning realistic part-construction priors.

### CAD-005 — DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation

Park et al. · 2019 · Computer Vision and Pattern Recognition · **indirect** · Work 102 catalog P25

[source](https://arxiv.org/abs/1901.05103) · [arXiv:1901.05103](https://arxiv.org/abs/1901.05103) · local PDF: [`papers/04_cad_brep_assembly/CAD-005_Park2019_deepsdf-learning-continuous-signed-distance-functi.pdf`](../../../papers/04_cad_brep_assembly/CAD-005_Park2019_deepsdf-learning-continuous-signed-distance-functi.pdf)

Implicit signed-distance shape representation; an option for smooth body surfaces, with meshing and feature-tolerance obligations.

### CAD-006 — ABC: A Big CAD Model Dataset For Geometric Deep Learning

Koch et al. · 2019 · Computer Vision and Pattern Recognition · **data/findings**

[source](https://arxiv.org/abs/1812.06216) · [arXiv:1812.06216](https://arxiv.org/abs/1812.06216) · local PDF: [`papers/04_cad_brep_assembly/CAD-006_Koch2019_abc-a-big-cad-model-dataset-for-geometric-deep-lea.pdf`](../../../papers/04_cad_brep_assembly/CAD-006_Koch2019_abc-a-big-cad-model-dataset-for-geometric-deep-lea.pdf)

One million B-rep models with parametric curves and surfaces; a benchmark source for geometry-kernel robustness tests.

### CAD-007 — UV-Net: Learning from Boundary Representations

Jayaraman et al. · 2021 · arXiv · **indirect**

[source](https://arxiv.org/abs/2006.10211) · [arXiv:2006.10211](https://arxiv.org/abs/2006.10211) · local PDF: [`papers/04_cad_brep_assembly/CAD-007_Jayaraman2021_uv-net-learning-from-boundary-representations.pdf`](../../../papers/04_cad_brep_assembly/CAD-007_Jayaraman2021_uv-net-learning-from-boundary-representations.pdf)

Samples B-rep faces and edges on their UV domains for learning; a practical B-rep encoder for surrogates on native geometry.

### CAD-008 — SolidGen: An Autoregressive Model for Direct B-rep Synthesis

Jayaraman et al. · 2023 · Trans. Mach. Learn. Res. · **indirect**

[source](https://arxiv.org/abs/2203.13944) · [arXiv:2203.13944](https://arxiv.org/abs/2203.13944) · local PDF: [`papers/04_cad_brep_assembly/CAD-008_Jayaraman2023_solidgen-an-autoregressive-model-for-direct-b-rep.pdf`](../../../papers/04_cad_brep_assembly/CAD-008_Jayaraman2023_solidgen-an-autoregressive-model-for-direct-b-rep.pdf)

Direct B-rep synthesis with indexed boundary representation; shows how to generate valid topology without a construction history.

### CAD-009 — SkexGen: Autoregressive Generation of CAD Construction Sequences with Disentangled Codebooks

Xu et al. · 2022 · International Conference on Machine Learning · **indirect**

[source](https://arxiv.org/abs/2207.04632) · [arXiv:2207.04632](https://arxiv.org/abs/2207.04632) · local PDF: [`papers/04_cad_brep_assembly/CAD-009_Xu2022_skexgen-autoregressive-generation-of-cad-construct.pdf`](../../../papers/04_cad_brep_assembly/CAD-009_Xu2022_skexgen-autoregressive-generation-of-cad-construct.pdf)

Disentangles topology and geometry codes in CAD sequences; relevant to separating structural choices from dimensions in the genome.

### CAD-010 — Hierarchical Neural Coding for Controllable CAD Model Generation

Xu et al. · 2023 · International Conference on Machine Learning · **indirect**

[source](https://arxiv.org/abs/2307.00149) · [arXiv:2307.00149](https://arxiv.org/abs/2307.00149) · local PDF: [`papers/04_cad_brep_assembly/CAD-010_Xu2023_hierarchical-neural-coding-for-controllable-cad-mo.pdf`](../../../papers/04_cad_brep_assembly/CAD-010_Xu2023_hierarchical-neural-coding-for-controllable-cad-mo.pdf)

Hierarchical codes for loops, profiles and solids; enables controlled partial edits, analogous to local mutation of a part.

### CAD-011 — BrepGen: A B-rep Generative Diffusion Model with Structured Latent Geometry

Xu et al. · 2024 · ACM Transactions on Graphics · **indirect**

[source](https://arxiv.org/abs/2401.15563) · [arXiv:2401.15563](https://arxiv.org/abs/2401.15563) · local PDF: [`papers/04_cad_brep_assembly/CAD-011_Xu2024_brepgen-a-b-rep-generative-diffusion-model-with-st.pdf`](../../../papers/04_cad_brep_assembly/CAD-011_Xu2024_brepgen-a-b-rep-generative-diffusion-model-with-st.pdf)

Diffusion over a structured latent B-rep tree including freeform surfaces; a candidate generator for freeform solids (Work 092).

### CAD-012 — ComplexGen: CAD Reconstruction by B-Rep Chain Complex Generation

Guo et al. · 2022 · ACM Transactions on Graphics · **indirect**

[source](https://arxiv.org/abs/2205.14573) · [arXiv:2205.14573](https://arxiv.org/abs/2205.14573) · local PDF: [`papers/04_cad_brep_assembly/CAD-012_Guo2022_complexgen-cad-reconstruction-by-b-rep-chain-compl.pdf`](../../../papers/04_cad_brep_assembly/CAD-012_Guo2022_complexgen-cad-reconstruction-by-b-rep-chain-compl.pdf)

Reconstructs B-rep as a chain complex with explicit topological constraints; relevant to topology-consistency checks.

### CAD-013 — JoinABLe: Learning Bottom-up Assembly of Parametric CAD Joints

Willis et al. · 2022 · Computer Vision and Pattern Recognition · **direct**

[source](https://arxiv.org/abs/2111.12772) · [arXiv:2111.12772](https://arxiv.org/abs/2111.12772) · local PDF: [`papers/04_cad_brep_assembly/CAD-013_Willis2022_joinable-learning-bottom-up-assembly-of-parametric.pdf`](../../../papers/04_cad_brep_assembly/CAD-013_Willis2022_joinable-learning-bottom-up-assembly-of-parametric.pdf)

Predicts joints between parts from B-rep geometry, with the Fusion 360 assembly/joint dataset; directly relevant to the joint kernel and part resolution.

### CAD-014 — AutoMate: A Dataset and Learning Approach for Automatic Mating of CAD Assemblies

Jones et al. · 2021 · ACM Transactions on Graphics · **direct**

[source](https://arxiv.org/abs/2105.12238) · [arXiv:2105.12238](https://arxiv.org/abs/2105.12238) · local PDF: [`papers/04_cad_brep_assembly/CAD-014_Jones2021_automate-a-dataset-and-learning-approach-for-autom.pdf`](../../../papers/04_cad_brep_assembly/CAD-014_Jones2021_automate-a-dataset-and-learning-approach-for-autom.pdf)

Large dataset of real CAD mates and a B-rep mate predictor; data for testing whether generated interfaces resemble real mechanical mates.

### CAD-015 — Assemble Them All: Physics-Based Planning for Generalizable Assembly by Disassembly

Tian et al. · 2022 · ACM Transactions on Graphics · **direct**

[source](https://doi.org/10.1145/3550454.3555525) · [arXiv:2211.03977](https://arxiv.org/abs/2211.03977) · local PDF: [`papers/04_cad_brep_assembly/CAD-015_Tian2022_assemble-them-all-physics-based-planning-for-gener.pdf`](../../../papers/04_cad_brep_assembly/CAD-015_Tian2022_assemble-them-all-physics-based-planning-for-gener.pdf)

Physics-based disassembly planning proves an assembly can be put together; a buildability gate for generated multi-part vehicles.

### CAD-016 — ASAP: Automated Sequence Planning for Complex Robotic Assembly with Physical Feasibility

Tian et al. · 2024 · IEEE International Conference on Robotics and Automation · **indirect**

[source](https://arxiv.org/abs/2309.16909) · [arXiv:2309.16909](https://arxiv.org/abs/2309.16909) · local PDF: [`papers/04_cad_brep_assembly/CAD-016_Tian2024_asap-automated-sequence-planning-for-complex-robot.pdf`](../../../papers/04_cad_brep_assembly/CAD-016_Tian2024_asap-automated-sequence-planning-for-complex-robot.pdf)

Assembly-sequence planning with gravity and stability checks; relevant to manufacturing handoff (Work 130).

### CAD-017 — Geometric Deep Learning for Computer-Aided Design: A Survey

Heidari & Iosifidis · 2024 · IEEE Access · **indirect**

[source](https://arxiv.org/abs/2402.17695) · [arXiv:2402.17695](https://arxiv.org/abs/2402.17695) · local PDF: [`papers/04_cad_brep_assembly/CAD-017_Heidari2024_geometric-deep-learning-for-computer-aided-design.pdf`](../../../papers/04_cad_brep_assembly/CAD-017_Heidari2024_geometric-deep-learning-for-computer-aided-design.pdf)

Survey of learning on CAD data (B-rep, sequences, assemblies); a map of available methods and datasets.

### CAD-018 — Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations

Jiang et al. · 2026 · arXiv · **direct**

[source](https://arxiv.org/abs/2609.11573) · [arXiv:2609.11573](https://arxiv.org/abs/2609.11573) · local PDF: [`papers/04_cad_brep_assembly/CAD-018_Jiang2026_learn-the-solid-not-the-file-canonical-inputs-for.pdf`](../../../papers/04_cad_brep_assembly/CAD-018_Jiang2026_learn-the-solid-not-the-file-canonical-inputs-for.pdf)

Argues learned models must see a canonical solid, not file-order artefacts; the same concern as our deterministic geometry identity and hashing.

### CAD-019 — TG-Diff: Coupling Discrete Topology Diffusion and Topology-conditioned Geometry Diffusions for B-Rep Generation

Sun et al. · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2607.21928) · [arXiv:2607.21928](https://arxiv.org/abs/2607.21928) · local PDF: [`papers/04_cad_brep_assembly/CAD-019_Sun2026_tg-diff-coupling-discrete-topology-diffusion-and-t.pdf`](../../../papers/04_cad_brep_assembly/CAD-019_Sun2026_tg-diff-coupling-discrete-topology-diffusion-and-t.pdf)

Generates B-rep topology first then geometry; mirrors the topology-then-dimensions split in our genome.

### CAD-020 — HiFi-BRep: High-Fidelity Latent Representation for Robust B-Rep Generation

Hou et al. · 2026 · arXiv · **indirect**

[source](https://arxiv.org/abs/2608.16485) · [arXiv:2608.16485](https://arxiv.org/abs/2608.16485) · local PDF: [`papers/04_cad_brep_assembly/CAD-020_Hou2026_hifi-brep-high-fidelity-latent-representation-for.pdf`](../../../papers/04_cad_brep_assembly/CAD-020_Hou2026_hifi-brep-high-fidelity-latent-representation-for.pdf)

Targets robustness of generated B-rep (watertightness, valid solids); relevant to constructive validity gates (Work 095).

### CAD-021 — CADENA: Stepwise CAD Reverse Engineering

Kabisov et al. · 2026 · arXiv · **indirect**

[source](https://arxiv.org/abs/2608.00799) · [arXiv:2608.00799](https://arxiv.org/abs/2608.00799) · local PDF: [`papers/04_cad_brep_assembly/CAD-021_Kabisov2026_cadena-stepwise-cad-reverse-engineering.pdf`](../../../papers/04_cad_brep_assembly/CAD-021_Kabisov2026_cadena-stepwise-cad-reverse-engineering.pdf)

Stepwise recovery of editable CAD from geometry; useful for turning evolved meshes or fields back into editable parts.

### CAD-022 — HoLa: B-Rep Generation using a Holistic Latent Representation

Liu et al. · 2025 · ACM Transactions on Graphics · **indirect**

[source](https://doi.org/10.1145/3730842) · [arXiv:2504.14257](https://arxiv.org/abs/2504.14257) · local PDF: [`papers/04_cad_brep_assembly/CAD-022_Liu2025_hola-b-rep-generation-using-a-holistic-latent-repr.pdf`](../../../papers/04_cad_brep_assembly/CAD-022_Liu2025_hola-b-rep-generation-using-a-holistic-latent-repr.pdf)

Single latent space for B-rep geometry and topology; a follow-up to BrepGen for freeform solid proposals.

### CAD-023 — AutoBrep: Autoregressive B-Rep Generation with Unified Topology and Geometry

Xu et al. · 2025 · Proceedings of the SIGGRAPH Asia 2025 Conference Papers · **indirect**

[source](https://doi.org/10.1145/3757377.3763814) · [arXiv:2512.03018](https://arxiv.org/abs/2512.03018) · local PDF: [`papers/04_cad_brep_assembly/CAD-023_Xu2025_autobrep-autoregressive-b-rep-generation-with-unif.pdf`](../../../papers/04_cad_brep_assembly/CAD-023_Xu2025_autobrep-autoregressive-b-rep-generation-with-unif.pdf)

Autoregressive B-rep generation with unified topology and geometry tokens; alternative generator with sequence-level control.

### CAD-024 — BrepDiff: Single-stage B-rep Diffusion Model

Lee et al. · 2025 · Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers · **indirect**

[source](https://doi.org/10.1145/3721238.3730698) · no local copy (download failed) · [open-access copy to fetch in a browser](https://doi.org/10.1145/3721238.3730698)

Single-stage diffusion for B-rep; a simpler generator to compare for validity rates.

### CAD-025 — DTGBrepGen: A Novel B-rep Generative Model through Decoupling Topology and Geometry

Li et al. · 2025 · 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) · **indirect**

[source](https://doi.org/10.1109/cvpr52734.2025.01997) · [arXiv:2503.13110](https://arxiv.org/abs/2503.13110) · local PDF: [`papers/04_cad_brep_assembly/CAD-025_Li2025_dtgbrepgen-a-novel-b-rep-generative-model-through.pdf`](../../../papers/04_cad_brep_assembly/CAD-025_Li2025_dtgbrepgen-a-novel-b-rep-generative-model-through.pdf)

Decouples topology and geometry generation for B-rep; another data point on validity versus diversity.

### CAD-026 — CAD-MLLM: Unifying Multimodality-Conditioned CAD Generation With MLLM

Xu et al. · 2024 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2411.04954) · [arXiv:2411.04954](https://arxiv.org/abs/2411.04954) · local PDF: [`papers/04_cad_brep_assembly/CAD-026_Xu2024_cad-mllm-unifying-multimodality-conditioned-cad-ge.pdf`](../../../papers/04_cad_brep_assembly/CAD-026_Xu2024_cad-mllm-unifying-multimodality-conditioned-cad-ge.pdf)

Multimodal (text, image, point cloud) conditioned CAD generation; relevant to conditioning part proposals on interface geometry.

### CAD-027 — FlexCAD: Unified and Versatile Controllable CAD Generation with Fine-tuned Large Language Models

Zhang et al. · 2024 · International Conference on Learning Representations · **indirect**

[source](https://arxiv.org/abs/2411.05823) · [arXiv:2411.05823](https://arxiv.org/abs/2411.05823) · local PDF: [`papers/04_cad_brep_assembly/CAD-027_Zhang2024_flexcad-unified-and-versatile-controllable-cad-gen.pdf`](../../../papers/04_cad_brep_assembly/CAD-027_Zhang2024_flexcad-unified-and-versatile-controllable-cad-gen.pdf)

LLM-based controllable CAD editing at different hierarchy levels; analogous to hierarchical mutation operators.

### CAD-028 — GenCAD: Image-Conditioned Computer-Aided Design Generation with Transformer-Based Contrastive Representation and Diffusion Priors

Alam & Ahmed · 2024 · Trans. Mach. Learn. Res. · **indirect**

[source](https://arxiv.org/abs/2409.16294) · [arXiv:2409.16294](https://arxiv.org/abs/2409.16294) · local PDF: [`papers/04_cad_brep_assembly/CAD-028_Alam2024_gencad-image-conditioned-computer-aided-design-gen.pdf`](../../../papers/04_cad_brep_assembly/CAD-028_Alam2024_gencad-image-conditioned-computer-aided-design-gen.pdf)

Image-conditioned CAD programme generation; another proposal route that must still pass physical gates.

### CAD-029 — Self-Supervised Representation Learning for CAD

Jones et al. · 2023 · 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) · **indirect**

[source](https://doi.org/10.1109/cvpr52729.2023.02043) · [arXiv:2210.10807](https://arxiv.org/abs/2210.10807) · local PDF: [`papers/04_cad_brep_assembly/CAD-029_Jones2023_self-supervised-representation-learning-for-cad.pdf`](../../../papers/04_cad_brep_assembly/CAD-029_Jones2023_self-supervised-representation-learning-for-cad.pdf)

Self-supervised B-rep embeddings trained without labels; useful descriptors when labelled engineering data is scarce.

### CAD-030 — Hierarchical CADNet: Learning from B-Reps for Machining Feature Recognition

Colligan et al. · 2022 · Computer-Aided Design · **indirect**

[source](https://doi.org/10.1016/j.cad.2022.103226) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.sciencedirect.com/science/article/pii/S0010448522000240/pdf)

Recognises machining features on B-reps; a route to automated manufacturability checks in the constructive validity gate.

### CAD-031 — Graph representation of 3D CAD models for machining feature recognition with deep learning

Cao et al. · 2020 · Volume 11A: 46th Design Automation Conference (DAC) · **indirect**

[source](https://doi.org/10.1115/detc2020-22355) · no local copy (no open-access copy found)

Introduces a graph encoding and synthetic machining-feature dataset (MFCAD); data for manufacturability classifiers.

### CAD-032 — LINKS: A dataset of a hundred million planar linkage mechanisms for data-driven kinematic design

Nobari et al. · 2022 · Volume 3A: 48th Design Automation Conference (DAC) · **data/findings**

[source](https://doi.org/10.1115/detc2022-89798) · no local copy (no open-access copy found)

Hundred-million planar linkage dataset with coupler curves; data and methods for linkage and motion-ratio synthesis (Work 075).

### CAD-033 — KDH-CAD: Knowledge-data hybrid CAD learning under data scarcity

Gao et al. · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2606.01702) · [arXiv:2606.01702](https://arxiv.org/abs/2606.01702) · local PDF: [`papers/04_cad_brep_assembly/CAD-033_Gao2026_kdh-cad-knowledge-data-hybrid-cad-learning-under-d.pdf`](../../../papers/04_cad_brep_assembly/CAD-033_Gao2026_kdh-cad-knowledge-data-hybrid-cad-learning-under-d.pdf)

Combines engineering knowledge with scarce CAD data; relevant because vehicle-part data is small and proprietary.

### CAD-034 — MatchMaker: Automated Asset Generation for Robotic Assembly

Wang et al. · 2025 · IEEE International Conference on Robotics and Automation · **indirect**

[source](https://arxiv.org/abs/2503.05887) · [arXiv:2503.05887](https://arxiv.org/abs/2503.05887) · local PDF: [`papers/04_cad_brep_assembly/CAD-034_Wang2025_matchmaker-automated-asset-generation-for-robotic.pdf`](../../../papers/04_cad_brep_assembly/CAD-034_Wang2025_matchmaker-automated-asset-generation-for-robotic.pdf)

Generates mating part pairs with clearance for assembly; relevant to interface clearance and fit generation.


## Topology optimisation, meshing, finite elements, contact and failure numerics

Methods that turn admitted geometry into solved fields and failure states: structural topology optimisation, robust tetrahedral meshing, element verification problems, frictional contact, fracture and fatigue damage models. The Work 102 review ranks independent geometry-to-field evaluation as the top gap.

### ST-001 — Generating optimal topologies in structural design using a homogenization method

Bendsøe & Kikuchi · 1988 · Computer Methods in Applied Mechanics and Engineering · **direct** · Work 102 catalog P26

[source](https://doi.org/10.1016/0045-7825(88)90086-2) · no local copy (no open-access copy found)

Founding structural topology optimisation paper; the physics-constrained precedent for letting load paths emerge.

### ST-002 — A 99 line topology optimization code written in Matlab

Sigmund · 2001 · Structural and Multidisciplinary Optimization · **indirect** · Work 102 catalog P27

[source](https://doi.org/10.1007/s001580050176) · no local copy (download failed) · [open-access copy to fetch in a browser](http://orbit.dtu.dk/en/publications/a-99-line-topology-optimization-code-written-in-matlab(b0794468-93a9-4cca-87b3-b4224938859a).html)

Compact SIMP compliance baseline; a strong, simple method any free-form structural search should beat or match.

### ST-003 — Efficient topology optimization in MATLAB using 88 lines of code

Andreassen et al. · 2011 · Structural and Multidisciplinary Optimization · **indirect**

[source](https://doi.org/10.1007/s00158-010-0594-7) · local PDF: [`papers/05_structures_meshing_contact/ST-003_Andreassen2011_efficient-topology-optimization-in-matlab-using-88.pdf`](../../../papers/05_structures_meshing_contact/ST-003_Andreassen2011_efficient-topology-optimization-in-matlab-using-88.pdf)

Faster, filtered successor to the 99-line code; the practical reference implementation for a 2D structural baseline.

### ST-004 — Giga-voxel computational morphogenesis for structural design

Aage et al. · 2017 · Nature · **direct**

[source](https://doi.org/10.1038/nature23911) · local PDF: [`papers/05_structures_meshing_contact/ST-004_Aage2017_giga-voxel-computational-morphogenesis-for-structu.pdf`](../../../papers/05_structures_meshing_contact/ST-004_Aage2017_giga-voxel-computational-morphogenesis-for-structu.pdf)

Topology optimisation of a full aircraft wing at billion-voxel resolution discovered non-conventional internal structure; closest structural analogue to whole-part discovery.

### ST-005 — Topology optimization approaches: A comparative review

Sigmund & Maute · 2013 · Structural and Multidisciplinary Optimization · **indirect**

[source](https://doi.org/10.1007/s00158-013-0978-6) · no local copy (download failed) · [open-access copy to fetch in a browser](http://orbit.dtu.dk/en/publications/topology-optimization-approaches(f861e156-422e-4bb0-a0ad-d378322003f9).html)

Compares density, level-set, phase-field and evolutionary topology optimisation; clarifies which is appropriate for which gate.

### ST-006 — Material interpolation schemes in topology optimization

Bendsøe & Sigmund · 1999 · Archive of Applied Mechanics (Ingenieur Archiv) · **indirect**

[source](https://doi.org/10.1007/s004190050248) · no local copy (no open-access copy found)

Justifies SIMP penalisation physically; relevant to spatial material-void fields (Work 108).

### ST-007 — Level-set methods for structural topology optimization: a review

Dijk et al. · 2013 · Structural and Multidisciplinary Optimization · **indirect**

[source](https://doi.org/10.1007/s00158-013-0912-y) · no local copy (no open-access copy found)

Level-set boundaries give crisp geometry convertible to CAD; relevant to converting optimised fields into B-rep.

### ST-008 — An efficient 3D topology optimization code written in Matlab

Liu & Tovar · 2014 · Structural and Multidisciplinary Optimization · **indirect**

[source](https://doi.org/10.1007/s00158-014-1107-x) · local PDF: [`papers/05_structures_meshing_contact/ST-008_Liu2014_an-efficient-3d-topology-optimization-code-written.pdf`](../../../papers/05_structures_meshing_contact/ST-008_Liu2014_an-efficient-3d-topology-optimization-code-written.pdf)

Compact 3D topology optimisation reference; a 3D structural baseline for part-level comparisons.

### ST-009 — Current and future trends in topology optimization for additive manufacturing

Liu et al. · 2018 · Structural and Multidisciplinary Optimization · **indirect**

[source](https://doi.org/10.1007/s00158-018-1994-3) · local PDF: [`papers/05_structures_meshing_contact/ST-009_Liu2018_current-and-future-trends-in-topology-optimization.pdf`](../../../papers/05_structures_meshing_contact/ST-009_Liu2018_current-and-future-trends-in-topology-optimization.pdf)

Reviews manufacturing constraints (overhang, minimum feature, support) in topology optimisation; inputs for the manufacturing language.

### ST-010 — A Review of Topology Optimisation for Fluid-Based Problems

Alexandersen & Andreasen · 2020 · Fluids · **indirect**

[source](https://doi.org/10.3390/fluids5010029) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.mdpi.com/2311-5521/5/1/29/pdf)

Reviews topology optimisation of flow and conjugate heat transfer; relevant to ducts and heat exchangers (Work 121).

### ST-011 — Gmsh: A 3-D finite element mesh generator with built-in pre- and post-processing facilities

Geuzaine & Remacle · 2009 · International Journal for Numerical Methods in Engineering · **direct** · Work 102 catalog P28

[source](https://doi.org/10.1002/nme.2579) · local PDF: [`papers/05_structures_meshing_contact/ST-011_Geuzaine2009_gmsh-a-3-d-finite-element-mesh-generator-with-buil.pdf`](../../../papers/05_structures_meshing_contact/ST-011_Geuzaine2009_gmsh-a-3-d-finite-element-mesh-generator-with-buil.pdf)

The mesher of the geometry-mesh bridge (Work 110); read with its documentation before trusting mesh quality settings.

### ST-012 — Fast Tetrahedral Meshing in the Wild

Hu et al. · 2020 · ACM Transactions on Graphics · **direct**

[source](https://arxiv.org/abs/1908.03581) · [arXiv:1908.03581](https://arxiv.org/abs/1908.03581) · local PDF: [`papers/05_structures_meshing_contact/ST-012_Hu2020_fast-tetrahedral-meshing-in-the-wild.pdf`](../../../papers/05_structures_meshing_contact/ST-012_Hu2020_fast-tetrahedral-meshing-in-the-wild.pdf)

fTetWild meshes arbitrary, imperfect triangle soups robustly; a fallback when generated CAD is not clean enough for CAD-based meshing.

### ST-013 — Tetrahedral Meshing in the Wild

Hu et al. · 2018 · ACM Transactions on Graphics · **indirect**

[source](https://doi.org/10.1145/3197517.3201353) · no local copy (download failed) · [open-access copy to fetch in a browser](https://dl.acm.org/doi/pdf/10.1145/3197517.3201353)

TetWild: envelope-based robust tetrahedralisation; the method behind ST-012 with its guarantees.

### ST-014 — TetGen, a Delaunay-Based Quality Tetrahedral Mesh Generator

Si · 2015 · ACM Transactions on Mathematical Software · **indirect**

[source](https://doi.org/10.1145/2629697) · no local copy (no open-access copy found)

Constrained Delaunay tetrahedral meshing with quality bounds; an independent mesher for cross-checking mesh sensitivity.

### ST-015 — Incremental Potential Contact: Intersection- and Inversion-free, Large-Deformation Dynamics

Li et al. · 2020 · ACM Transactions on Graphics · **direct** · Work 102 catalog P29

[source](https://doi.org/10.1145/3386569.3392425) · local PDF: [`papers/05_structures_meshing_contact/ST-015_Li2020_incremental-potential-contact-intersection-and-inv.pdf`](../../../papers/05_structures_meshing_contact/ST-015_Li2020_incremental-potential-contact-intersection-and-inv.pdf)

Guaranteed non-penetrating frictional contact for large deformation; candidate method for moving contact assemblies (Work 114).

### ST-016 — High-Order Incremental Potential Contact for Elastodynamic Simulation on Curved Meshes

Ferguson et al. · 2023 · International Conference on Computer Graphics and Interactive Techniques · **indirect** · Work 102 catalog P30

[source](https://arxiv.org/abs/2205.13727) · [arXiv:2205.13727](https://arxiv.org/abs/2205.13727) · local PDF: [`papers/05_structures_meshing_contact/ST-016_Ferguson2023_high-order-incremental-potential-contact-for-elast.pdf`](../../../papers/05_structures_meshing_contact/ST-016_Ferguson2023_high-order-incremental-potential-contact-for-elast.pdf)

Extends IPC to curved high-order meshes; relevant once CAD-conforming meshes are used.

### ST-017 — Intersection-free Rigid Body Dynamics

Ferguson et al. · 2021 · ACM Transactions on Graphics · **indirect**

[source](https://doi.org/10.1145/3450626.3459802) · no local copy (no open-access copy found)

Rigid-body IPC with curved trajectories; relevant to rigid joint and fastener contact without penetration.

### ST-018 — Affine Body Dynamics: Fast, Stable & Intersection-free Simulation of Stiff Materials

Lan et al. · 2022 · ACM Transactions on Graphics · **indirect**

[source](https://arxiv.org/abs/2201.10022) · [arXiv:2201.10022](https://arxiv.org/abs/2201.10022) · local PDF: [`papers/05_structures_meshing_contact/ST-018_Lan2022_affine-body-dynamics-fast-stable-intersection-free.pdf`](../../../papers/05_structures_meshing_contact/ST-018_Lan2022_affine-body-dynamics-fast-stable-intersection-free.pdf)

Stiff bodies as affine deformations with IPC contact; a fast option for many-part assemblies.

### ST-019 — A proposed standard set of problems to test finite element accuracy

Macneal & Harder · 1985 · Finite Elements in Analysis and Design · **direct**

[source](https://doi.org/10.1016/0168-874x(85)90003-4) · no local copy (no open-access copy found)

MacNeal-Harder element patch and distortion tests; standard verification problems for any element we implement (Work 041).

### ST-020 — A review on phase-field models of brittle fracture and a new fast hybrid formulation

Ambati et al. · 2015 · Computational Mechanics · **indirect**

[source](https://doi.org/10.1007/s00466-014-1109-y) · no local copy (no open-access copy found)

Phase-field fracture review with a fast hybrid formulation; a route from fracture initiation (Work 043) to propagation.

### ST-021 — Cumulative fatigue damage and life prediction theories: a survey of the state of the art for homogeneous materials

Fatemi & Yang · 1998 · International Journal of Fatigue · **direct**

[source](https://doi.org/10.1016/s0142-1123(97)00081-9) · no local copy (no open-access copy found)

Surveys Miner-rule alternatives and their errors under variable amplitude; directly bounds the fatigue-life gate (Work 044).

### ST-022 — Cumulative Damage in Fatigue

Wilkins · 1945 · Colloquium on Fatigue / Colloque de Fatigue / Kolloquium über Ermüdungsfestigkeit · **indirect**

[source](https://doi.org/10.1007/978-3-642-99854-6_35) · no local copy (no open-access copy found)

Miner's linear damage rule, the assumption behind simple fatigue accounting; cite with its known non-conservatism.

### ST-023 — A Critical Analysis of Crack Propagation Laws

Paris & Erdogan · 1963 · Journal of Basic Engineering · **indirect**

[source](https://doi.org/10.1115/1.3656900) · no local copy (no open-access copy found)

Paris-Erdogan crack-growth law; the basis for damage-tolerance rather than safe-life fatigue claims.

### ST-024 — An implicit time-stepping scheme for rigid body dynamics with inelastic collisions and coulomb friction

STEWART & TRINKLE · 1996 · International Journal for Numerical Methods in Engineering · **indirect**

[source](https://doi.org/10.1002/(sici)1097-0207(19960815)39:15<2673::aid-nme972>3.0.co;2-i) · no local copy (no open-access copy found)

Stewart-Trinkle complementarity time stepping for frictional contact; the classic formulation behind many rigid contact solvers.


## Simulation, optimal-control and MDO infrastructure, coupling and integrators

Engines, solvers and modelling languages the project could adopt or cross-check against: multibody dynamics, differentiable simulation, co-simulation coupling, acausal energy-port modelling, structure-preserving integrators and nonlinear-programming solvers used for minimum-time problems.

### SI-001 — DiffTaichi: Differentiable Programming for Physical Simulation

Hu et al. · 2020 · International Conference on Learning Representations · **indirect** · Work 102 catalog P08

[source](https://arxiv.org/abs/1910.00935) · [arXiv:1910.00935](https://arxiv.org/abs/1910.00935) · local PDF: [`papers/06_simulation_infrastructure/SI-001_Hu2020_difftaichi-differentiable-programming-for-physical.pdf`](../../../papers/06_simulation_infrastructure/SI-001_Hu2020_difftaichi-differentiable-programming-for-physical.pdf)

Differentiable simulation language; a route to gradient refinement inside an admitted topology, with the caveat that gradients do not prove accuracy.

### SI-002 — Chrono: An Open Source Multi-physics Dynamics Engine

Tasora et al. · 2016 · Lecture Notes in Computer Science · **indirect** · Work 102 catalog P54

[source](https://doi.org/10.1007/978-3-319-40361-8_2) · no local copy (no open-access copy found)

Open multibody and contact engine; candidate independent backend for cross-checking vehicle dynamics.

### SI-003 — Chrono::Vehicle: template-based ground vehicle modelling and simulation

Serban et al. · 2019 · International Journal of Vehicle Performance · **direct** · Work 102 catalog P55

[source](https://doi.org/10.1504/ijvp.2019.097096) · no local copy (no open-access copy found)

Template vehicle models in an open engine; the most practical public route to a reproduced conventional baseline.

### SI-004 — MuJoCo: A physics engine for model-based control

Todorov et al. · 2012 · 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems · **indirect** · Work 102 catalog P56

[source](https://doi.org/10.1109/iros.2012.6386109) · no local copy (download failed) · [open-access copy to fetch in a browser](https://homes.cs.washington.edu/~todorov/papers/TodorovIROS12.pdf)

Fast contact-rich dynamics for control learning; useful for driver-policy training, not as calibrated tyre or aero evidence.

### SI-005 — OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization

Gray et al. · 2019 · Structural and Multidisciplinary Optimization · **indirect** · Work 102 catalog P57

[source](https://doi.org/10.1007/s00158-019-02211-z) · local PDF: [`papers/06_simulation_infrastructure/SI-005_Gray2019_openmdao-an-open-source-framework-for-multidiscipl.pdf`](../../../papers/06_simulation_infrastructure/SI-005_Gray2019_openmdao-an-open-source-framework-for-multidiscipl.pdf)

Coupled-analysis orchestration with derivatives; a pattern for design/control/energy/structure coupling.

### SI-006 — preCICE v2: A sustainable and user-friendly coupling library

Chourdakis et al. · 2022 · Open Research Europe · **indirect**

[source](https://arxiv.org/abs/2109.14470) · [arXiv:2109.14470](https://arxiv.org/abs/2109.14470) · local PDF: [`papers/06_simulation_infrastructure/SI-006_Chourdakis2022_precice-v2-a-sustainable-and-user-friendly-couplin.pdf`](../../../papers/06_simulation_infrastructure/SI-006_Chourdakis2022_precice-v2-a-sustainable-and-user-friendly-couplin.pdf)

Partitioned multiphysics coupling (fluid-structure, conjugate heat) with convergence acceleration; relevant to coupled thermal-solid work (Work 115).

### SI-007 — DOLFINx: The next generation FEniCS problem solving environment

— · 2023 · **indirect**

[source](https://zenodo.org/records/10447666/files/main.pdf?download=1) · local PDF: [`papers/06_simulation_infrastructure/SI-007_Anon2023_dolfinx-the-next-generation-fenics-problem-solving.pdf`](../../../papers/06_simulation_infrastructure/SI-007_Anon2023_dolfinx-the-next-generation-fenics-problem-solving.pdf)

Open finite-element environment; candidate independent solver for geometry-general evaluation (Work 138).

### SI-008 — The Pinocchio C++ library: A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives

Carpentier et al. · 2019 · 2019 IEEE/SICE International Symposium on System Integration (SII) · **indirect**

[source](https://doi.org/10.1109/sii.2019.8700380) · no local copy (download failed) · [open-access copy to fetch in a browser](https://hal.laas.fr/hal-01866228v2/file/19-sii-pinocchio.pdf)

Rigid-body dynamics with analytical derivatives; useful for linkage and suspension kinematics with gradients.

### SI-009 — Brax: A Differentiable Physics Engine for Large Scale Rigid Body Simulation

Freeman et al. · 2021 · NeurIPS Datasets and Benchmarks · **indirect**

[source](https://arxiv.org/abs/2106.13281) · [arXiv:2106.13281](https://arxiv.org/abs/2106.13281) · local PDF: [`papers/06_simulation_infrastructure/SI-009_Freeman2021_brax-a-differentiable-physics-engine-for-large-sca.pdf`](../../../papers/06_simulation_infrastructure/SI-009_Freeman2021_brax-a-differentiable-physics-engine-for-large-sca.pdf)

Massively parallel accelerator physics; relevant to the compute ledger when comparing search algorithms by wall time.

### SI-010 — Dojo: A Differentiable Physics Engine for Robotics

Howell et al. · 2022 · arXiv · **indirect**

[source](https://arxiv.org/abs/2203.00806) · [arXiv:2203.00806](https://arxiv.org/abs/2203.00806) · local PDF: [`papers/06_simulation_infrastructure/SI-010_Howell2022_dojo-a-differentiable-physics-engine-for-robotics.pdf`](../../../papers/06_simulation_infrastructure/SI-010_Howell2022_dojo-a-differentiable-physics-engine-for-robotics.pdf)

Differentiable contact via interior-point complementarity; a gradient-through-contact option for ground interaction.

### SI-011 — A pressure field model for fast, robust approximation of net contact force and moment between nominally rigid objects

Elandt et al. · 2019 · IEEE/RJS International Conference on Intelligent RObots and Systems · **indirect**

[source](https://arxiv.org/abs/1904.11433) · [arXiv:1904.11433](https://arxiv.org/abs/1904.11433) · local PDF: [`papers/06_simulation_infrastructure/SI-011_Elandt2019_a-pressure-field-model-for-fast-robust-approximati.pdf`](../../../papers/06_simulation_infrastructure/SI-011_Elandt2019_a-pressure-field-model-for-fast-robust-approximati.pdf)

Hydroelastic contact giving distributed pressure rather than point forces; relevant to contact patches of arbitrary ground-contact endpoints.

### SI-012 — Discrete mechanics and variational integrators

Marsden & West · 2001 · Acta Numerica · **direct**

[source](https://doi.org/10.1017/s096249290100006x) · local PDF: [`papers/06_simulation_infrastructure/SI-012_Marsden2001_discrete-mechanics-and-variational-integrators.pdf`](../../../papers/06_simulation_infrastructure/SI-012_Marsden2001_discrete-mechanics-and-variational-integrators.pdf)

Structure-preserving integrators with bounded energy error; the theory behind treating energy residuals as observable outputs.

### SI-013 — Port-Hamiltonian Systems Theory: An Introductory Overview

Schaft & Jeltsema · 2014 · **direct**

[source](https://doi.org/10.1561/9781601987877) · no local copy (no open-access copy found)

Energy-port formalism where interconnection conserves power by construction; a rigorous basis for the typed energy graph and its conservation audit (Works 012-013).

### SI-014 — Physical system modeling with Modelica

Mattsson et al. · 1998 · Control Engineering Practice · **indirect**

[source](https://doi.org/10.1016/S0967-0661(98)00047-1) · no local copy (no open-access copy found)

Acausal, equation-based component modelling with typed connectors; the established design of typed physical ports.

### SI-015 — Bond-graph modeling

Machado & Cunha · 2007 · An Introduction to Bond Graph Modeling with Applications · **indirect**

[source](https://doi.org/10.1201/9781003057741-2) · no local copy (no open-access copy found)

Tutorial on bond graphs for multi-domain energy flow; a compact notation for checking power-conserving connections.

### SI-016 — The Functional Mockup Interface for Tool independent Exchange of Simulation Models

Blochwitz et al. · 2011 · Linköping Electronic Conference Proceedings · **indirect**

[source](https://doi.org/10.3384/ecp11063105) · no local copy (download failed) · [open-access copy to fetch in a browser](http://www.ep.liu.se/ecp/063/013/ecp11063013.pdf)

FMI co-simulation standard; relevant if subsystem models from other tools are coupled into the race simulation.

### SI-017 — CasADi: a software framework for nonlinear optimization and optimal control

Andersson et al. · 2019 · Mathematical Programming Computation · **direct**

[source](https://doi.org/10.1007/s12532-018-0139-4) · local PDF: [`papers/06_simulation_infrastructure/SI-017_Andersson2019_casadi-a-software-framework-for-nonlinear-optimiza.pdf`](../../../papers/06_simulation_infrastructure/SI-017_Andersson2019_casadi-a-software-framework-for-nonlinear-optimiza.pdf)

The standard open tool for direct-collocation minimum-lap-time problems; needed for optimised driver baselines.

### SI-018 — On the implementation of an interior-point filter line-search algorithm for large-scale nonlinear programming

Wächter & Biegler · 2006 · Mathematical Programming · **indirect**

[source](https://doi.org/10.1007/s10107-004-0559-y) · local PDF: [`papers/06_simulation_infrastructure/SI-018_Wachter2006_on-the-implementation-of-an-interior-point-filter.pdf`](../../../papers/06_simulation_infrastructure/SI-018_Wachter2006_on-the-implementation-of-an-interior-point-filter.pdf)

IPOPT, the NLP solver used by most published minimum-lap-time work; know its convergence behaviour before trusting a lap.

### SI-019 — GPOPS-II: A MATLAB Software for Solving Multiple-Phase Optimal Control Problems Using hp-Adaptive Gaussian Quadrature Collocation Methods and Sparse Nonlinear Programming

Patterson & Rao · 2014 · ACM Transactions on Mathematical Software · **indirect**

[source](https://doi.org/10.1145/2558904) · no local copy (no open-access copy found)

hp-adaptive collocation used in the Limebeer F1 optimal-control papers; explains their mesh refinement.

### SI-020 — Energy conservation and power bonds in co-simulations: non-iterative adaptive step size control and error estimation

Sadjina et al. · 2017 · Engineering computations · **direct**

[source](https://arxiv.org/abs/1602.06434) · [arXiv:1602.06434](https://arxiv.org/abs/1602.06434) · local PDF: [`papers/06_simulation_infrastructure/SI-020_Sadjina2017_energy-conservation-and-power-bonds-in-co-simulati.pdf`](../../../papers/06_simulation_infrastructure/SI-020_Sadjina2017_energy-conservation-and-power-bonds-in-co-simulati.pdf)

Measures energy residuals at co-simulation power bonds and uses them to control step size; directly relevant to observable conservation residuals in the coupled race step.

### SI-021 — Co-simulation: State of the art

Gomes et al. · 2018 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/1702.00686) · [arXiv:1702.00686](https://arxiv.org/abs/1702.00686) · local PDF: [`papers/06_simulation_infrastructure/SI-021_Gomes2018_co-simulation-state-of-the-art.pdf`](../../../papers/06_simulation_infrastructure/SI-021_Gomes2018_co-simulation-state-of-the-art.pdf)

Survey of co-simulation orchestration, stability and accuracy; background for coupling many subsystem models.


## Minimum-lap-time optimal control, vehicle dynamics, tracks and design/control co-optimisation

How race vehicles are driven optimally and how design parameters are optimised together with that driving. This is the evaluator side of the project: an unconventional vehicle can only be judged fairly with an optimised driver on a spatial track.

### LT-001 — Optimal control for a Formula One car with variable parameters

Perantoni & Limebeer · 2014 · Vehicle System Dynamics · **direct** · Work 102 catalog P31

[source](https://doi.org/10.1080/00423114.2014.889315) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-001_Perantoni2014_optimal-control-for-a-formula-one-car-with-variabl.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-001_Perantoni2014_optimal-control-for-a-formula-one-car-with-variabl.pdf)

Minimum-lap-time control with vehicle parameters as optimisation variables; the template for design/driver fairness.

### LT-002 — Optimal control of a Formula One car on a three-dimensional track-part 1: track modeling and identification

Perantoni & Limebeer · 2015 · Journal of Dynamic Systems, Measurement, and Control · **direct** · Work 102 catalog P32

[source](https://doi.org/10.1115/1.4028253) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-002_Perantoni2015_optimal-control-of-a-formula-one-car-on-a-three-di.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-002_Perantoni2015_optimal-control-of-a-formula-one-car-on-a-three-di.pdf)

Builds and identifies a 3D track ribbon (curvature, elevation, banking) from data; the guide for replacing our synthetic tracks.

### LT-003 — Optimal Control of a Formula One Car on a Three-Dimensional Track - Part 2: Optimal Control

Limebeer & Perantoni · 2015 · Journal of Dynamic Systems, Measurement, and Control · **direct** · Work 102 catalog P33

[source](https://doi.org/10.1115/1.4029466) · no local copy (no open-access copy found)

Solves minimum-lap-time on the 3D track and shows the lap-time effect of 3D geometry.

### LT-004 — Minimum time optimal control simulation of a GP2 race car

Bianco et al. · 2018 · Proceedings of the Institution of Mechanical Engineers, Part D: Journal of Automobile Engineering · **direct** · Work 102 catalog P34

[source](https://doi.org/10.1177/0954407017728158) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-004_Bianco2018_minimum-time-optimal-control-simulation-of-a-gp2-r.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-004_Bianco2018_minimum-time-optimal-control-simulation-of-a-gp2-r.pdf)

14-DOF car, nonlinear tyres, ride-height aero and telemetry comparison; the nearest public coupled-model target.

### LT-005 — Optimizing the aero-suspension interactions in a Formula One car

Masouleh & Limebeer · 2016 · IEEE Transactions on Control Systems Technology · **direct** · Work 102 catalog P35

[source](https://doi.org/10.1109/tcst.2015.2475396) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-005_Masouleh2016_optimizing-the-aero-suspension-interactions-in-a-f.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-005_Masouleh2016_optimizing-the-aero-suspension-interactions-in-a-f.pdf)

Suspension geometry and ride-height-dependent aero optimised together; the coupled benchmark for aero-chassis coupling (Work 024).

### LT-006 — Minimum curvature trajectory planning and control for an autonomous race car

Heilmeier et al. · 2020 · Vehicle System Dynamics · **indirect** · Work 102 catalog P39

[source](https://doi.org/10.1080/00423114.2019.1631455) · no local copy (download failed) · [open-access copy to fetch in a browser](http://mediatum.ub.tum.de/node?id=1509975)

Practical raceline optimisation with open code and track data; a fast baseline raceline, not a minimum-time one.

### LT-007 — Time-optimal control of the race car: a numerical method to emulate the ideal driver

Kelly & Sharp · 2010 · Vehicle System Dynamics · **direct**

[source](https://doi.org/10.1080/00423110903514236) · no local copy (no open-access copy found)

Transient minimum-time driver emulation; an early optimal-driver formulation to compare against steady-state methods.

### LT-008 — Vehicle dynamics applications of optimal control theory

Sharp & Peng · 2011 · Vehicle System Dynamics · **indirect**

[source](https://doi.org/10.1080/00423114.2011.586707) · no local copy (no open-access copy found)

Review of optimal control in vehicle dynamics; orientation for choosing driver models of different fidelity.

### LT-009 — Lap time optimisation of a racing go-kart

Lot & Bianco · 2016 · Vehicle System Dynamics · **indirect**

[source](https://doi.org/10.1080/00423114.2015.1125514) · no local copy (download failed) · [open-access copy to fetch in a browser](https://eprints.soton.ac.uk/385883/2/Lap%2520time%2520optimisation%2520of%2520a%2520racing%2520go-kart%2520%2528corrected%2520proof%2529.pdf)

Minimum-lap-time for a vehicle without a differential or suspension; evidence that the method transfers to unconventional chassis.

### LT-010 — A Curvilinear Abscissa Approach for the Lap Time Optimization of Racing Vehicles

Lot & Biral · 2014 · IFAC Proceedings Volumes · **indirect**

[source](https://doi.org/10.3182/20140824-6-za-1003.00868) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-010_Lot2014_a-curvilinear-abscissa-approach-for-the-lap-time-o.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-010_Lot2014_a-curvilinear-abscissa-approach-for-the-lap-time-o.pdf)

Curvilinear-coordinate formulation used by most modern lap-time solvers; needed to pose our track-relative dynamics.

### LT-011 — A free-trajectory quasi-steady-state optimal-control method for minimum lap-time of race vehicles

Veneri & Massaro · 2020 · Vehicle System Dynamics · **direct**

[source](https://doi.org/10.1080/00423114.2019.1608364) · no local copy (download failed) · [open-access copy to fetch in a browser](http://hdl.handle.net/11577/3297111)

Quasi-steady-state optimal control with a free racing line and g-g maps; fast enough to evaluate many candidate vehicles.

### LT-012 — A three-dimensional free-trajectory quasi-steady-state optimal-control method for minimum-lap-time of race vehicles

Lovato & Massaro · 2022 · Vehicle System Dynamics · **direct**

[source](https://doi.org/10.1080/00423114.2021.1878242) · no local copy (download failed) · [open-access copy to fetch in a browser](http://hdl.handle.net/11577/3375385)

Extends LT-011 to 3D tracks with g-g-g diagrams; the fast evaluator matching our 3D circuit corridor (Work 010).

### LT-013 — Online Time-Optimal Trajectory Planning on Three-Dimensional Race Tracks

Rowold et al. · 2023 · 2023 IEEE Intelligent Vehicles Symposium (IV) · **indirect**

[source](https://arxiv.org/abs/2304.10954) · [arXiv:2304.10954](https://arxiv.org/abs/2304.10954) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-013_Rowold2023_online-time-optimal-trajectory-planning-on-three-d.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-013_Rowold2023_online-time-optimal-trajectory-planning-on-three-d.pdf)

Point-mass time-optimal planning on 3D tracks with open code; a cheap lower-fidelity rung of the ladder.

### LT-014 — Time-optimal trajectory planning for a race car considering variable tyre-road friction coefficients

Christ et al. · 2021 · Vehicle System Dynamics · **indirect**

[source](https://doi.org/10.1080/00423114.2019.1704804) · no local copy (no open-access copy found)

Spatially varying friction in minimum-time planning; relevant to track-surface uncertainty.

### LT-015 — GripMap: An Efficient, Spatially Resolved Constraint Framework for Offline and Online Trajectory Planning in Autonomous Racing

Werner et al. · 2025 · 2025 IEEE Intelligent Vehicles Symposium (IV) · **indirect**

[source](https://arxiv.org/abs/2504.12115) · [arXiv:2504.12115](https://arxiv.org/abs/2504.12115) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-015_Werner2025_gripmap-an-efficient-spatially-resolved-constraint.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-015_Werner2025_gripmap-an-efficient-spatially-resolved-constraint.pdf)

Spatially resolved grip constraints for planning; a data structure for track-position-dependent grip.

### LT-016 — A quasi steady state approach to race car lap simulation in order to understand the effects of racing line and centre of gravity location

Brayshaw & Harrison · 2005 · Proceedings of the Institution of Mechanical Engineers, Part D: Journal of Automobile Engineering · **indirect**

[source](https://doi.org/10.1243/095440705x11211) · no local copy (no open-access copy found)

Quasi-steady-state lap simulation studying centre-of-gravity effects; a classic reference for low-fidelity lap models.

### LT-017 — Lap Time Simulation: Comparison of Steady State, Quasi-Static and Transient Racing Car Cornering Strategies

Siegler et al. · 2000 · SAE Technical Paper Series · **direct**

[source](https://doi.org/10.4271/2000-01-3563) · no local copy (no open-access copy found)

Direct comparison of lap-simulation fidelities; evidence on when steady-state ranking differs from transient ranking (H4).

### LT-018 — On minimum time vehicle manoeuvring: the theoretical optimal lap

— · 2000 · **direct**

[source](https://dspace.lib.cranfield.ac.uk/handle/1826/1091) · no local copy (download failed) · [open-access copy to fetch in a browser](https://core.ac.uk/download/pdf/138004.pdf)

Casanova's thesis solving the full transient optimal lap and studying vehicle parameter sensitivities.

### LT-019 — Minimum-lap-time optimisation and simulation

Massaro & Limebeer · 2021 · Vehicle System Dynamics · **indirect**

[source](https://doi.org/10.1080/00423114.2021.1910718) · no local copy (download failed) · [open-access copy to fetch in a browser](http://hdl.handle.net/11577/3389257)

Recent review of minimum-lap-time methods by leading authors; orientation for choosing formulation and solver.

### LT-020 — Comparison of direct and indirect methods for minimum lap time optimal control problems

Bianco et al. · 2019 · Vehicle System Dynamics · **indirect**

[source](https://doi.org/10.1080/00423114.2018.1480048) · no local copy (download failed) · [open-access copy to fetch in a browser](https://iris.unitn.it/bitstream/11572/211730/4/2_PDFsam_2018dir_vs_indirpreprint.pdf)

Compares direct and indirect solution of the same lap problem; evidence on solver-induced differences in lap time.

### LT-021 — Optimal control of motorsport differentials

Tremlett et al. · 2015 · Vehicle System Dynamics · **direct**

[source](https://doi.org/10.1080/00423114.2015.1093150) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.tandfonline.com/doi/pdf/10.1080/00423114.2015.1093150?needAccess=true)

Optimises differential behaviour for minimum lap time; relevant to differential and independent wheel dynamics (Works 070-071).

### LT-022 — A Convex Optimization Framework for Minimum Lap Time Design and Control of Electric Race Cars

Borsboom et al. · 2021 · IEEE Transactions on Vehicular Technology · **direct**

[source](https://doi.org/10.1109/tvt.2021.3093164) · no local copy (download failed) · [open-access copy to fetch in a browser](https://research.tue.nl/en/publications/98d6f349-dcae-447b-86cc-8d61e15b7107)

Jointly sizes the electric powertrain and computes the minimum-lap-time strategy by convex optimisation; a direct design/control co-optimisation method.

### LT-023 — Minimum-lap-time Control Strategies for All-wheel Drive Electric Race Cars via Convex Optimization

Broere et al. · 2022 · European Control Conference · **direct**

[source](https://arxiv.org/abs/2111.04650) · [arXiv:2111.04650](https://arxiv.org/abs/2111.04650) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-023_Broere2022_minimum-lap-time-control-strategies-for-all-wheel.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-023_Broere2022_minimum-lap-time-control-strategies-for-all-wheel.pdf)

Per-tyre grip limits with all-wheel drive in a convex lap formulation; relevant to independent-wheel torque allocation.

### LT-024 — Time-optimal Design and Control of Electric Race Cars Equipped with Multi-speed Transmissions

Cartignij & Salazar · 2023 · Vehicle Power and Propulsion Conference · **direct**

[source](https://arxiv.org/abs/2311.03545) · [arXiv:2311.03545](https://arxiv.org/abs/2311.03545) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-024_Cartignij2023_time-optimal-design-and-control-of-electric-race-c.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-024_Cartignij2023_time-optimal-design-and-control-of-electric-race-c.pdf)

Compares fixed, CVT and multi-speed transmissions with jointly optimised control; an architecture choice evaluated fairly.

### LT-025 — Time-optimal Control Strategies for Electric Race Cars with Different Transmission Technologies

Borsboom et al. · 2020 · Vehicle Power and Propulsion Conference · **direct**

[source](https://arxiv.org/abs/2005.07592) · [arXiv:2005.07592](https://arxiv.org/abs/2005.07592) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-025_Borsboom2020_time-optimal-control-strategies-for-electric-race.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-025_Borsboom2020_time-optimal-control-strategies-for-electric-race.pdf)

Earlier transmission-technology comparison under time-optimal control; precedent for architecture comparison at equal control effort.

### LT-026 — Joint Optimisation of Active Aerodynamics and Electric Energy Deployment for Minimum Lap Time in 2026 Formula One

Saxena · 2026 · **direct**

[source](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7045379) · no local copy (no open-access copy found)

Schedules 2026 movable-wing modes with electric deploy and harvest by direct collocation; uses the same regulation year as our race contract.

### LT-027 — Kinematic and dynamic vehicle models for autonomous driving control design

Kong et al. · 2015 · 2015 IEEE Intelligent Vehicles Symposium (IV) · **indirect**

[source](https://doi.org/10.1109/ivs.2015.7225830) · no local copy (no open-access copy found)

Compares kinematic and dynamic bicycle models against data; a small fidelity-ladder example.

### LT-028 — The kinematic bicycle model: A consistent model for planning feasible trajectories for autonomous vehicles?

Polack et al. · 2017 · 2017 IEEE Intelligent Vehicles Symposium (IV) · **indirect**

[source](https://doi.org/10.1109/ivs.2017.7995816) · no local copy (download failed) · [open-access copy to fetch in a browser](https://polytechnique.hal.science/hal-01520869)

Shows when the kinematic bicycle model becomes inconsistent with physics; a caution for low-fidelity gates.

### LT-029 — A quasi-steady-state minimum lap time simulation of race motorcycles using experimental data

Biniewicz & Pyrz · 2023 · Vehicle System Dynamics · **data/findings**

[source](https://doi.org/10.1080/00423114.2023.2170256) · no local copy (no open-access copy found)

Quasi-steady-state lap simulation compared against measured motorcycle data; an example of validating a lap model against telemetry.

### LT-030 — Simultaneous Optimisation of Vehicle Design and Control for Improving Vehicle Performance and Energy Efficiency Using an Open Source Minimum Lap Time Simulation Framework

Elbal et al. · 2024 · World Electric Vehicle Journal · **direct**

[source](https://doi.org/10.3390/wevj15080366) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.mdpi.com/2032-6653/15/8/366/pdf?version=1724141770)

Open-source minimum-lap-time framework that optimises design parameters, active torque distribution, active aero and energy deployment together; a reproducible co-optimisation baseline.

### LT-031 — Optimising the Performance of a Formula One Car Using a Genetic Algorithm

Wloch & Bentley · 2004 · Lecture Notes in Computer Science · **direct**

[source](https://doi.org/10.1007/978-3-540-30217-9_71) · no local copy (no open-access copy found)

Genetic algorithm tuning 66 setup parameters of an F1 car inside a racing simulator; an early evolutionary design-in-simulator result with simulator-dependence caveats.

### LT-032 — A Sequential Convex Programming Approach to Free-trajectory Minimum-lap-time Optimization of Racing Cars

Eshof et al. · 2025 · arXiv · **direct**

[source](https://arxiv.org/abs/2511.13522) · [arXiv:2511.13522](https://arxiv.org/abs/2511.13522) · local PDF: [`papers/07_lap_time_vehicle_dynamics/LT-032_Eshof2025_a-sequential-convex-programming-approach-to-free-t.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-032_Eshof2025_a-sequential-convex-programming-approach-to-free-t.pdf)

Recent efficient free-trajectory lap-time optimisation; relevant to the cost of giving every candidate an optimised driver.


## Race energy management, powertrain architecture and energy storage

Energy-limited racing strategy, hybrid and electric powertrain control, powertrain topology synthesis, and the models and measured data for batteries, flywheels and supercapacitors. Supports the carried-energy race contract, the typed energy graph and onboard energy realisation (Work 120).

### EN-001 — Optimal control of Formula One car energy recovery systems

Limebeer et al. · 2014 · International Journal of Control · **direct** · Work 102 catalog P36

[source](https://doi.org/10.1080/00207179.2014.900705) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.anilvrao.com/Publications/JournalPublications/F-1-Optimal-Control-Energy-Recovery.pdf)

Joint minimum-time driving and ERS scheduling; the formulation for energy-limited racing with recovery.

### EN-002 — Optimal energy management for formula-E cars with regulatory limits and thermal constraints

Liu et al. · 2020 · Applied Energy · **direct** · Work 102 catalog P37

[source](https://doi.org/10.1016/j.apenergy.2020.115805) · no local copy (download failed) · [open-access copy to fetch in a browser](https://dspace.lib.cranfield.ac.uk/bitstream/1826/15797/1/Optimal_energy_management_for_formula-E_cars_with_regulatory_limits_and_thermal_constraints-2020.pdf)

Battery energy and temperature limits shaping race-long control; a full-stint coupling of energy and heat.

### EN-003 — Time-optimal Control Strategies for a Hybrid Electric Race Car

Ebbesen et al. · 2018 · IEEE Transactions on Control Systems Technology · **direct**

[source](https://doi.org/10.1109/tcst.2017.2661824) · no local copy (no open-access copy found)

Convex time-optimal energy management of an F1-style hybrid; the core method family for fuel-plus-electric strategies.

### EN-004 — Time-Optimal Control Policy for a Hybrid Electric Race Car

Salazar et al. · 2017 · IEEE Transactions on Control Systems Technology · **direct**

[source](https://doi.org/10.1109/tcst.2016.2642830) · no local copy (no open-access copy found)

Derives the structure of time-optimal hybrid energy policies; useful for sanity-checking learned or searched strategies.

### EN-005 — Time-optimal gearshift and energy management strategies for a hybrid electric race car

Duhr et al. · 2021 · Applied Energy · **direct**

[source](https://doi.org/10.1016/j.apenergy.2020.115980) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.sciencedirect.com/science/article/pii/S0306261920314288/pdf)

Adds gear selection to hybrid energy management; mixed-integer structure similar to discrete architecture choices.

### EN-006 — Time-optimal low-level control and gearshift strategies for the formula 1 hybrid electric powertrain

Balerna et al. · 2020 · Energies · **direct**

[source](https://doi.org/10.3390/en14010171) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.mdpi.com/1996-1073/14/1/171/pdf?version=1609831608)

Low-level F1 power-unit control including turbocharger and MGU-H; detail for a conventional hybrid baseline.

### EN-007 — Low-level Online Control of the Formula 1 Power Unit with Feedforward Cylinder Deactivation

Neumann et al. · 2023 · IEEE Transactions on Vehicular Technology · **indirect**

[source](https://arxiv.org/abs/2303.00372) · [arXiv:2303.00372](https://arxiv.org/abs/2303.00372) · local PDF: [`papers/08_energy_powertrain/EN-007_Neumann2023_low-level-online-control-of-the-formula-1-power-un.pdf`](../../../papers/08_energy_powertrain/EN-007_Neumann2023_low-level-online-control-of-the-formula-1-power-un.pdf)

Online F1 power-unit control; shows real-time constraints on energy strategies.

### EN-008 — Time-optimal Energy Management of the Formula 1 Power Unit with Active Battery Path Constraints

Duhr et al. · 2021 · 2021 European Control Conference (ECC) · **direct**

[source](https://doi.org/10.23919/ecc54610.2021.9655192) · no local copy (no open-access copy found)

Enforces battery path constraints in time-optimal F1 energy management; relevant to state-of-charge limits in the race contract.

### EN-009 — Maximum-distance Race Strategies for a Fully Electric Endurance Race Car

Kampen et al. · 2022 · European Journal of Control · **direct**

[source](https://arxiv.org/abs/2111.05784) · [arXiv:2111.05784](https://arxiv.org/abs/2111.05784) · local PDF: [`papers/08_energy_powertrain/EN-009_Kampen2022_maximum-distance-race-strategies-for-a-fully-elect.pdf`](../../../papers/08_energy_powertrain/EN-009_Kampen2022_maximum-distance-race-strategies-for-a-fully-elect.pdf)

Endurance strategy under fixed energy with pit decisions; relevant to race-long energy budgeting.

### EN-010 — Optimal Endurance Race Strategies for a Fully Electric Race Car under Thermal Constraints

Kampen et al. · 2023 · IEEE Transactions on Control Systems Technology · **direct**

[source](https://arxiv.org/abs/2301.08060) · [arXiv:2301.08060](https://arxiv.org/abs/2301.08060) · local PDF: [`papers/08_energy_powertrain/EN-010_Kampen2023_optimal-endurance-race-strategies-for-a-fully-elec.pdf`](../../../papers/08_energy_powertrain/EN-010_Kampen2023_optimal-endurance-race-strategies-for-a-fully-elec.pdf)

Adds battery and motor thermal limits to endurance strategy; a direct coupling of our thermal and energy gates.

### EN-011 — Human-in-the-loop Energy and Thermal Management for Electric Racing Cars through Optimization-based Control

Eshof et al. · 2024 · European Journal of Control · **indirect**

[source](https://arxiv.org/abs/2412.15379) · [arXiv:2412.15379](https://arxiv.org/abs/2412.15379) · local PDF: [`papers/08_energy_powertrain/EN-011_Eshof2024_human-in-the-loop-energy-and-thermal-management-fo.pdf`](../../../papers/08_energy_powertrain/EN-011_Eshof2024_human-in-the-loop-energy-and-thermal-management-fo.pdf)

Optimisation-based energy and thermal guidance delivered to a human driver; relevant to realistic driver execution of optimal strategies.

### EN-012 — Battery model impact on time-optimal co-design for electric racing cars: review and application

Riva et al. · 2023 · IEEE Transactions on Transportation Electrification · **direct**

[source](https://arxiv.org/abs/2312.17003) · [arXiv:2312.17003](https://arxiv.org/abs/2312.17003) · local PDF: [`papers/08_energy_powertrain/EN-012_Riva2023_battery-model-impact-on-time-optimal-co-design-for.pdf`](../../../papers/08_energy_powertrain/EN-012_Riva2023_battery-model-impact-on-time-optimal-co-design-for.pdf)

Shows that the battery model choice changes co-design results; direct evidence that energy-store fidelity can flip architecture rankings (H4).

### EN-013 — Minimum Race-Time Planning-Strategy for an Autonomous Electric Racecar

Herrmann et al. · 2020 · 2020 IEEE 23rd International Conference on Intelligent Transportation Systems (ITSC) · **direct**

[source](https://arxiv.org/abs/2005.07127) · [arXiv:2005.07127](https://arxiv.org/abs/2005.07127) · local PDF: [`papers/08_energy_powertrain/EN-013_Herrmann2020_minimum-race-time-planning-strategy-for-an-autonom.pdf`](../../../papers/08_energy_powertrain/EN-013_Herrmann2020_minimum-race-time-planning-strategy-for-an-autonom.pdf)

Race-long energy and thermal planning for an electric racecar with open tooling; a public reference implementation.

### EN-014 — Review of Optimization Strategies for System-Level Design in Hybrid Electric Vehicles

Silvas et al. · 2017 · IEEE Transactions on Vehicular Technology · **direct**

[source](https://doi.org/10.1109/tvt.2016.2547897) · no local copy (download failed) · [open-access copy to fetch in a browser](https://research.tue.nl/en/publications/69ba1672-e399-42f9-a7f4-f3633784ffb8)

Classifies topology, technology, sizing and control co-design for hybrids; the vocabulary for our powertrain topology search.

### EN-015 — Topology Generation for Hybrid Electric Vehicle Architecture Design

Bayrak et al. · 2016 · Journal of Mechanical Design · **direct**

[source](https://doi.org/10.1115/1.4033656) · no local copy (no open-access copy found)

Enumerates feasible hybrid powertrain topologies from components and connection rules; directly comparable to typed-graph topology generation.

### EN-016 — Joint Design and Control of Electric Vehicle Propulsion Systems

Verbruggen et al. · 2020 · 2020 European Control Conference (ECC) · **direct**

[source](https://doi.org/10.23919/ecc51009.2020.9143869) · local PDF: [`papers/08_energy_powertrain/EN-016_Verbruggen2020_joint-design-and-control-of-electric-vehicle-propu.pdf`](../../../papers/08_energy_powertrain/EN-016_Verbruggen2020_joint-design-and-control-of-electric-vehicle-propu.pdf)

Co-design of electric propulsion components and control; method for sizing components within a chosen topology.

### EN-017 — Python Battery Mathematical Modelling (PyBaMM)

Sulzer et al. · 2021 · Journal of Open Research Software · **data/findings**

[source](https://doi.org/10.5334/jors.309) · local PDF: [`papers/08_energy_powertrain/EN-017_Sulzer2021_python-battery-mathematical-modelling-pybamm.pdf`](../../../papers/08_energy_powertrain/EN-017_Sulzer2021_python-battery-mathematical-modelling-pybamm.pdf)

The battery modelling package already mirrored in private/materials/sources; the citation for its models and parameter sets.

### EN-018 — Review of parameterisation and a novel database (LiionDB) for continuum Li-ion battery models

Wang et al. · 2022 · Progress in Energy · **data/findings**

[source](https://doi.org/10.1088/2516-1083/ac692c) · no local copy (download failed) · [open-access copy to fetch in a browser](https://iopscience.iop.org/article/10.1088/2516-1083/ac692c/pdf)

Curated literature parameters for physics-based cell models; the paper behind the private liiondb source and its provenance fields.

### EN-019 — Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models

Chen et al. · 2020 · Journal of The Electrochemical Society · **data/findings**

[source](https://doi.org/10.1149/1945-7111/ab9050) · local PDF: [`papers/08_energy_powertrain/EN-019_Chen2020_development-of-experimental-techniques-for-paramet.pdf`](../../../papers/08_energy_powertrain/EN-019_Chen2020_development-of-experimental-techniques-for-paramet.pdf)

Measured parameter set for an LG M50 cell (PyBaMM Chen2020); real cell data usable for an onboard battery model.

### EN-020 — An asymptotic derivation of a single particle model with electrolyte

Marquis et al. · 2019 · Journal of the Electrochemical Society · **indirect**

[source](https://arxiv.org/abs/1905.12553) · [arXiv:1905.12553](https://arxiv.org/abs/1905.12553) · local PDF: [`papers/08_energy_powertrain/EN-020_Marquis2019_an-asymptotic-derivation-of-a-single-particle-mode.pdf`](../../../papers/08_energy_powertrain/EN-020_Marquis2019_an-asymptotic-derivation-of-a-single-particle-mode.pdf)

Derives SPMe as a controlled reduction of the DFN model; a principled low-fidelity battery rung.

### EN-021 — Lithium-ion battery degradation: how to model it

O’Kane et al. · 2022 · Physical Chemistry, Chemical Physics - PCCP · **indirect**

[source](https://arxiv.org/abs/2112.02037) · [arXiv:2112.02037](https://arxiv.org/abs/2112.02037) · local PDF: [`papers/08_energy_powertrain/EN-021_Kane2022_lithium-ion-battery-degradation-how-to-model-it.pdf`](../../../papers/08_energy_powertrain/EN-021_Kane2022_lithium-ion-battery-degradation-how-to-model-it.pdf)

Coupled degradation mechanisms in PyBaMM; relevant if race energy stores degrade over a stint or season.

### EN-022 — A continuum of physics-based lithium-ion battery models reviewed

Planella et al. · 2022 · Progress in Energy · **indirect**

[source](https://arxiv.org/abs/2203.16091) · [arXiv:2203.16091](https://arxiv.org/abs/2203.16091) · local PDF: [`papers/08_energy_powertrain/EN-022_Planella2022_a-continuum-of-physics-based-lithium-ion-battery-m.pdf`](../../../papers/08_energy_powertrain/EN-022_Planella2022_a-continuum-of-physics-based-lithium-ion-battery-m.pdf)

Reviews the hierarchy of physics-based cell models; a map for choosing battery fidelity per gate.

### EN-023 — Parameterization of a Physico-Chemical Model of a Lithium-Ion Battery: I. Determination of Parameters

Ecker et al. · 2015 · Journal of The Electrochemical Society · **data/findings**

[source](https://doi.org/10.1149/2.0551509jes) · local PDF: [`papers/08_energy_powertrain/EN-023_Ecker2015_parameterization-of-a-physico-chemical-model-of-a.pdf`](../../../papers/08_energy_powertrain/EN-023_Ecker2015_parameterization-of-a-physico-chemical-model-of-a.pdf)

Measured Kokam cell parameters (PyBaMM Ecker2015); a second measured data set for cross-checking battery models.

### EN-024 — Modeling of Galvanostatic Charge and Discharge of the Lithium/Polymer/Insertion Cell

Doyle et al. · 1993 · Journal of The Electrochemical Society · **indirect**

[source](https://doi.org/10.1149/1.2221597) · no local copy (download failed) · [open-access copy to fetch in a browser](https://iopscience.iop.org/article/10.1149/1.2221597/pdf)

The Doyle-Fuller-Newman model, the reference physics-based cell model all reduced models are compared against.

### EN-025 — A non-academic perspective on the future of lithium-based batteries

Frith et al. · 2023 · Nature Communications · **data/findings**

[source](https://doi.org/10.1038/s41467-023-35933-2) · local PDF: [`papers/08_energy_powertrain/EN-025_Frith2023_a-non-academic-perspective-on-the-future-of-lithiu.pdf`](../../../papers/08_energy_powertrain/EN-025_Frith2023_a-non-academic-perspective-on-the-future-of-lithiu.pdf)

Industry-grounded figures on achievable cell energy density and cost; realistic bounds for energy-store candidates.

### EN-026 — Overview of current development in electrical energy storage technologies and the application potential in power system operation

Luo et al. · 2015 · Applied Energy · **data/findings**

[source](https://doi.org/10.1016/j.apenergy.2014.09.081) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.sciencedirect.com/science/article/pii/S0306261914010290/pdf)

Tabulated energy and power density, efficiency and lifetime across storage technologies; inputs for a technology-neutral energy profile.

### EN-027 — Theory of Ragone plots

Christen & Carlen · 2000 · Journal of Power Sources · **direct**

[source](https://doi.org/10.1016/s0378-7753(00)00474-2) · no local copy (no open-access copy found)

Derives energy-versus-power trade-off curves for storage devices; the right comparison frame for batteries, flywheels and supercapacitors under one energy budget.

### EN-028 — A Review of Flywheel Energy Storage System Technologies and Their Applications

Amiryar & Pullen · 2017 · Applied Sciences · **data/findings**

[source](https://doi.org/10.3390/app7030286) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.mdpi.com/2076-3417/7/3/286/pdf?version=1489660272)

Flywheel energy, power and loss data including motorsport KERS; inputs for a mechanical energy-store candidate.

### EN-029 — A Comprehensive Review on Supercapacitor Applications and Developments

Şahin et al. · 2022 · Energies · **data/findings**

[source](https://doi.org/10.3390/en15030674) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.mdpi.com/1996-1073/15/3/674/pdf?version=1642493431)

Supercapacitor performance data and applications; inputs for a high-power, low-energy storage candidate.

### EN-030 — Competitors-Aware Stochastic Lap Strategy Optimisation for Race Hybrid Vehicles

Paparusso et al. · 2022 · IEEE Transactions on Vehicular Technology · **indirect**

[source](https://arxiv.org/abs/2203.00084) · [arXiv:2203.00084](https://arxiv.org/abs/2203.00084) · local PDF: [`papers/08_energy_powertrain/EN-030_Paparusso2022_competitors-aware-stochastic-lap-strategy-optimisa.pdf`](../../../papers/08_energy_powertrain/EN-030_Paparusso2022_competitors-aware-stochastic-lap-strategy-optimisa.pdf)

Stochastic hybrid energy strategy accounting for competitors; relevant if race time depends on interaction, not only on the lone vehicle.

### EN-031 — Modern Electrical Machine Design Optimization: Techniques, Trends, and Best Practices

Bramerdorfer et al. · 2018 · IEEE Transactions on Industrial Electronics · **indirect**

[source](https://doi.org/10.1109/tie.2018.2801805) · no local copy (no open-access copy found)

Review of electric machine design optimisation practice; guidance for sizing or generating motors as components.


## Tyres, rubber friction and tyre identification

Tyre force models, transient and thermal behaviour, wear and degradation, rubber friction physics, and identification from test or track data. Tyres/contact is a priority-A gap in the Work 102 review; the current kernel uses a friction envelope and a tanh slip route.

### TY-001 — Tyre Modelling for Use in Vehicle Dynamics Studies

Bakker et al. · 1987 · SAE Technical Paper Series · **direct** · Work 102 catalog P43

[source](https://doi.org/10.4271/870421) · no local copy (no open-access copy found)

The original Magic Formula; the steady-state force model to replace the constant-friction envelope.

### TY-002 — Magic Formula Tyre Model with Transient Properties

PACEJKA & BESSELINK · 1997 · Vehicle System Dynamics · **direct** · Work 102 catalog P44

[source](https://doi.org/10.1080/00423119708969658) · no local copy (no open-access copy found)

Adds relaxation-length transients to the Magic Formula; needed for transient manoeuvres near the limit.

### TY-003 — An improved Magic Formula/Swift tyre model that can handle inflation pressure changes

Besselink et al. · 2010 · Vehicle System Dynamics · **direct** · Work 102 catalog P45

[source](https://doi.org/10.1080/00423111003748088) · no local copy (download failed) · [open-access copy to fetch in a browser](https://pure.tue.nl/ws/files/3139490/Metis245615.pdf)

Pressure-dependent Magic Formula (MF 6.1 basis); defines the applicability envelope of tyre coefficients.

### TY-004 — TRT: thermo racing tyre a physical model to predict the tyre temperature distribution

Farroni et al. · 2014 · Meccanica · **direct** · Work 102 catalog P46

[source](https://doi.org/10.1007/s11012-013-9821-9) · no local copy (no open-access copy found)

Physical racing-tyre thermal model compared with telemetry; the architecture for a tyre temperature state.

### TY-005 — Optimal tyre usage for a Formula One car

Tremlett & Limebeer · 2016 · Vehicle System Dynamics · **direct** · Work 102 catalog P38

[source](https://doi.org/10.1080/00423114.2016.1213861) · no local copy (no open-access copy found)

Couples tyre thermal state and wear into minimum-time control over a stint; the race-long tyre problem.

### TY-006 — The Formula SAE Tire Test Consortium-Tire Testing and Data Handling

Kasprzak & Gentz · 2006 · SAE Technical Paper Series · **data/findings** · Work 102 catalog P61

[source](https://doi.org/10.4271/2006-01-3606) · local PDF: [`papers/09_tyres_friction/TY-006_Kasprzak2006_the-formula-sae-tire-test-consortium-tire-testing.pdf`](../../../papers/09_tyres_friction/TY-006_Kasprzak2006_the-formula-sae-tire-test-consortium-tire-testing.pdf)

How the FSAE TTC measured and distributes tyre data; the most accessible real racing-tyre data source to request.

### TY-007 — Theory of rubber friction and contact mechanics

Persson · 2001 · The Journal of Chemical Physics · **indirect**

[source](https://doi.org/10.1063/1.1388626) · no local copy (download failed) · [open-access copy to fetch in a browser](http://juser.fz-juelich.de/record/42969/files/6009.pdf)

Persson's viscoelastic rubber friction theory on rough surfaces; physics behind grip dependence on speed, temperature and road texture.

### TY-008 — Rubber friction on road surfaces: Experiment and theory for low sliding speeds

Lorenz et al. · 2015 · The Journal of Chemical Physics · **data/findings**

[source](https://doi.org/10.1063/1.4919221) · no local copy (no open-access copy found)

Measured rubber friction on road surfaces compared with theory; data on how far first-principles friction can be trusted.

### TY-009 — TMeasy - The Handling Tire Model for All Driving Situations

— · 2013 · **indirect**

no local copy (no open-access copy found)

Semi-physical tyre model with few, interpretable parameters; a middle-fidelity option when full Magic Formula data is unavailable.

### TY-010 — Tire Modeling and Friction Estimation

— · 2007 · **indirect**

[source](https://lucris.lub.lu.se/ws/files/4401399/27004.pdf) · local PDF: [`papers/09_tyres_friction/TY-010_Anon2007_tire-modeling-and-friction-estimation.pdf`](../../../papers/09_tyres_friction/TY-010_Anon2007_tire-modeling-and-friction-estimation.pdf)

Thesis on brush-type tyre models and friction estimation; a physical basis for combined-slip behaviour.

### TY-011 — Bayesian Optimization-based Tire Parameter and Uncertainty Estimation for Real-World Data

Goblirsch et al. · 2025 · 2025 IEEE Intelligent Vehicles Symposium (IV) · **direct**

[source](https://arxiv.org/abs/2504.20863) · [arXiv:2504.20863](https://arxiv.org/abs/2504.20863) · local PDF: [`papers/09_tyres_friction/TY-011_Goblirsch2025_bayesian-optimization-based-tire-parameter-and-unc.pdf`](../../../papers/09_tyres_friction/TY-011_Goblirsch2025_bayesian-optimization-based-tire-parameter-and-unc.pdf)

Identifies tyre parameters with uncertainty from real vehicle data; directly relevant to calibrating tyres with declared uncertainty.

### TY-012 — A State-Space Approach to Modeling Tire Degradation in Formula 1 Racing

Cappello & Hoegh · 2025 · Journal of Sports Analytics · **data/findings**

[source](https://arxiv.org/abs/2512.00640) · [arXiv:2512.00640](https://arxiv.org/abs/2512.00640) · local PDF: [`papers/09_tyres_friction/TY-012_Cappello2025_a-state-space-approach-to-modeling-tire-degradatio.pdf`](../../../papers/09_tyres_friction/TY-012_Cappello2025_a-state-space-approach-to-modeling-tire-degradatio.pdf)

Bayesian state-space tyre degradation estimated from real 2025 F1 lap times; data-driven degradation rates for race-length simulation.

### TY-013 — Extended Pacejka Tire Model for Enhanced Vehicle

Singh & Sivaramakrishnan · 2023 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2305.18422) · [arXiv:2305.18422](https://arxiv.org/abs/2305.18422) · local PDF: [`papers/09_tyres_friction/TY-013_Singh2023_extended-pacejka-tire-model-for-enhanced-vehicle.pdf`](../../../papers/09_tyres_friction/TY-013_Singh2023_extended-pacejka-tire-model-for-enhanced-vehicle.pdf)

Extends the Pacejka model with additional effects for vehicle simulation; a comparator for tyre-model extensions.

### TY-014 — TRIP-ID: A tool for a smart and interactive identification of Magic Formula tyre model parameters from experimental data acquired on track

Farroni et al. · 2019 · Mechanical Systems and Signal Processing · **indirect**

[source](https://doi.org/10.1016/j.ymssp.2017.07.025) · no local copy (no open-access copy found)

Identifies Magic Formula parameters from on-track data rather than test rigs; the practical route when rig data is unavailable.

### TY-015 — Tyre wear model: Validation and sensitivity analysis

Braghin et al. · 2006 · Meccanica · **indirect**

[source](https://doi.org/10.1007/s11012-005-1058-9) · no local copy (no open-access copy found)

Physical tyre wear model with validation; a starting point for a wear state over a race.

### TY-016 — Estimation of tire-road friction coefficient and its application in chassis control systems

Singh & Taheri · 2015 · Systems Science &amp; Control Engineering · **indirect**

[source](https://doi.org/10.1080/21642583.2014.985804) · no local copy (download failed) · [open-access copy to fetch in a browser](https://doi.org/10.1080/21642583.2014.985804)

Review of tyre-road friction estimation; relevant to friction uncertainty bounds on held-out tracks.

### TY-017 — Tire multiphysical modeling for the analysis of thermal and wear sensitivity on vehicle objective dynamics and racing performances

Farroni & Sakhnevych · 2022 · Simulation Modelling Practice and Theory · **direct**

[source](https://doi.org/10.1016/j.simpat.2022.102517) · no local copy (no open-access copy found)

Couples tyre thermal and wear models to vehicle dynamics and lap performance; the multiphysics tyre evaluator the project lacks.


## Aerodynamics, CFD validation, aero datasets and neural surrogates

Race-car aerodynamic mechanisms (ground effect, wheels, wakes), experimentally anchored CFD cases, adjoint shape optimisation, open automotive CFD datasets, and neural surrogates with their out-of-distribution limits. Aero is an A/B gap: there is no validated geometry-to-aero-map route yet.

### AE-001 — Aerodynamics of Race Cars

Katz · 2006 · Annual Review of Fluid Mechanics · **direct** · Work 102 catalog P47

[source](https://doi.org/10.1146/annurev.fluid.38.050304.092016) · no local copy (no open-access copy found)

Review of race-car aero mechanisms, ground effect and component interactions; which causal effects an aero model must capture.

### AE-002 — Spectral/hp element simulation of flow past a Formula One front wing: validation against experiments

Buscariolo et al. · 2019 · Journal of Wind Engineering and Industrial Aerodynamics · **data/findings** · Work 102 catalog P48

[source](https://arxiv.org/abs/1909.06701) · [arXiv:1909.06701](https://arxiv.org/abs/1909.06701) · local PDF: [`papers/10_aerodynamics/AE-002_Buscariolo2019_spectral-hp-element-simulation-of-flow-past-a-form.pdf`](../../../papers/10_aerodynamics/AE-002_Buscariolo2019_spectral-hp-element-simulation-of-flow-past-a-form.pdf)

Experimentally validated F1 front-wing CFD case; a public benchmark to validate any aero solver before whole-car use.

### AE-003 — DAFoam: An Open-Source Adjoint Framework for Multidisciplinary Design Optimization with OpenFOAM

He et al. · 2020 · AIAA Journal · **indirect** · Work 102 catalog P49

[source](https://doi.org/10.2514/1.j058853) · no local copy (download failed) · [open-access copy to fetch in a browser](https://arc.aiaa.org/doi/pdf/10.2514/1.J058853)

Adjoint CFD gradients for shape optimisation on OpenFOAM; a local aero refinement tool inside an admitted topology.

### AE-004 — Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design

Palacios et al. · 2013 · 51st AIAA Aerospace Sciences Meeting including the New Horizons Forum and Aerospace Exposition · **indirect** · Work 102 catalog P50

[source](https://doi.org/10.2514/6.2013-287) · local PDF: [`papers/10_aerodynamics/AE-004_Palacios2013_stanford-university-unstructured-su2-an-open-sourc.pdf`](../../../papers/10_aerodynamics/AE-004_Palacios2013_stanford-university-unstructured-su2-an-open-sourc.pdf)

Open CFD and adjoint design suite; an independent second solver for aero cross-checks.

### AE-005 — DrivAerNet: A Parametric Car Dataset for Data-Driven Aerodynamic Design and Prediction

Elrefaie et al. · 2024 · Design Automation Conference · **data/findings** · Work 102 catalog P51

[source](https://arxiv.org/abs/2403.08055) · [arXiv:2403.08055](https://arxiv.org/abs/2403.08055) · local PDF: [`papers/10_aerodynamics/AE-005_Elrefaie2024_drivaernet-a-parametric-car-dataset-for-data-drive.pdf`](../../../papers/10_aerodynamics/AE-005_Elrefaie2024_drivaernet-a-parametric-car-dataset-for-data-drive.pdf)

Thousands of parametric car CFD results; training/validation data for drag surrogates, limited to road-car shapes.

### AE-006 — DrivAerNet++: A Large-Scale Multimodal Car Dataset with Computational Fluid Dynamics Simulations and Deep Learning Benchmarks

Elrefaie et al. · 2024 · Neural Information Processing Systems · **data/findings** · Work 102 catalog P52

[source](https://arxiv.org/abs/2406.09624) · [arXiv:2406.09624](https://arxiv.org/abs/2406.09624) · local PDF: [`papers/10_aerodynamics/AE-006_Elrefaie2024_drivaernet-a-large-scale-multimodal-car-dataset-wi.pdf`](../../../papers/10_aerodynamics/AE-006_Elrefaie2024_drivaernet-a-large-scale-multimodal-car-dataset-wi.pdf)

8,000+ multimodal car CFD cases with benchmarks; the largest open automotive aero dataset.

### AE-007 — CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics

Elrefaie et al. · 2025 · arXiv.org · **direct** · Work 102 catalog P53

[source](https://arxiv.org/abs/2512.07847) · [arXiv:2512.07847](https://arxiv.org/abs/2512.07847) · local PDF: [`papers/10_aerodynamics/AE-007_Elrefaie2025_carbench-a-comprehensive-benchmark-for-neural-surr.pdf`](../../../papers/10_aerodynamics/AE-007_Elrefaie2025_carbench-a-comprehensive-benchmark-for-neural-surr.pdf)

Benchmarks surrogate accuracy, physical consistency, cost and uncertainty including unseen categories; the evaluation protocol for any aero surrogate we use.

### AE-008 — DrivAerML: High-Fidelity Computational Fluid Dynamics Dataset for Road-Car External Aerodynamics

Ashton et al. · 2024 · arXiv.org · **data/findings**

[source](https://arxiv.org/abs/2408.11969) · [arXiv:2408.11969](https://arxiv.org/abs/2408.11969) · local PDF: [`papers/10_aerodynamics/AE-008_Ashton2024_drivaerml-high-fidelity-computational-fluid-dynami.pdf`](../../../papers/10_aerodynamics/AE-008_Ashton2024_drivaerml-high-fidelity-computational-fluid-dynami.pdf)

500 DrivAer variants with hybrid RANS-LES at 160M cells, open licence; high-fidelity reference data for surrogate validation.

### AE-009 — AhmedML: High-Fidelity Computational Fluid Dynamics Dataset for Incompressible, Low-Speed Bluff Body Aerodynamics

Ashton et al. · 2024 · arXiv.org · **data/findings**

[source](https://arxiv.org/abs/2407.20801) · [arXiv:2407.20801](https://arxiv.org/abs/2407.20801) · local PDF: [`papers/10_aerodynamics/AE-009_Ashton2024_ahmedml-high-fidelity-computational-fluid-dynamics.pdf`](../../../papers/10_aerodynamics/AE-009_Ashton2024_ahmedml-high-fidelity-computational-fluid-dynamics.pdf)

500 Ahmed-body variants with hybrid RANS-LES; a simpler bluff-body benchmark for testing aero pipelines.

### AE-010 — WindsorML: High-Fidelity Computational Fluid Dynamics Dataset For Automotive Aerodynamics

Ashton et al. · 2024 · Neural Information Processing Systems · **data/findings**

[source](https://arxiv.org/abs/2407.19320) · [arXiv:2407.19320](https://arxiv.org/abs/2407.19320) · local PDF: [`papers/10_aerodynamics/AE-010_Ashton2024_windsorml-high-fidelity-computational-fluid-dynami.pdf`](../../../papers/10_aerodynamics/AE-010_Ashton2024_windsorml-high-fidelity-computational-fluid-dynami.pdf)

Wall-modelled LES of Windsor-body variants (CC-BY-SA); open high-fidelity data including ground proximity.

### AE-011 — Ground Effect Aerodynamics of Race Cars

Zhang et al. · 2006 · Applied Mechanics Reviews · **direct**

[source](https://doi.org/10.1115/1.2110263) · local PDF: [`papers/10_aerodynamics/AE-011_Zhang2006_ground-effect-aerodynamics-of-race-cars.pdf`](../../../papers/10_aerodynamics/AE-011_Zhang2006_ground-effect-aerodynamics-of-race-cars.pdf)

Review of wings, diffusers and wheels in ground effect with experimental data; the physics of ride-height-dependent downforce.

### AE-012 — Aerodynamics of a single element wing in ground effect

Zerihan & Zhang · 2000 · 38th Aerospace Sciences Meeting and Exhibit · **data/findings**

[source](https://doi.org/10.2514/6.2000-650) · no local copy (no open-access copy found)

Wind-tunnel measurements of an inverted wing versus ground height, including force reduction close to the ground; validation data for ground-effect models.

### AE-013 — A Computational Study of the Flow Around an Isolated Wheel in Contact With the Ground

McManus & Zhang · 2006 · Journal of Fluids Engineering · **indirect**

[source](https://doi.org/10.1115/1.2175158) · no local copy (no open-access copy found)

CFD of a rotating wheel on the ground compared with experiment; relevant to exposed ground-contact endpoints.

### AE-014 — The effects of simplifications on isolated wheel aerodynamics

Diasinos et al. · 2015 · Journal of Wind Engineering and Industrial Aerodynamics · **indirect**

[source](https://doi.org/10.1016/j.jweia.2015.08.004) · no local copy (download failed) · [open-access copy to fetch in a browser](https://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1151&context=aero_fac)

Quantifies how geometric simplifications change wheel aero; guidance on which details a geometry-to-aero route must keep.

### AE-015 — CFD Investigation of the Effect of the Salient Flow Features in the Wake of a Generic Open-Wheel Race Car

Newbon et al. · 2017 · SAE International Journal of Passenger Cars - Mechanical Systems · **indirect**

[source](https://doi.org/10.4271/2015-01-1539) · no local copy (download failed) · [open-access copy to fetch in a browser](http://nrl.northumbria.ac.uk/id/eprint/25043/1/SAE%202015-01-1539_PrePublication_Dominy-Newbon.pdf)

Wake structures of an open-wheel car and their effect on a following car; relevant later if traffic and wake enter the race environment.

### AE-016 — AB-UPT: Scaling Neural CFD Surrogates for High-Fidelity Automotive Aerodynamics Simulations via Anchored-Branched Universal Physics Transformers

Alkin et al. · 2025 · Trans. Mach. Learn. Res. · **indirect**

[source](https://arxiv.org/abs/2502.09692) · [arXiv:2502.09692](https://arxiv.org/abs/2502.09692) · local PDF: [`papers/10_aerodynamics/AE-016_Alkin2025_ab-upt-scaling-neural-cfd-surrogates-for-high-fide.pdf`](../../../papers/10_aerodynamics/AE-016_Alkin2025_ab-upt-scaling-neural-cfd-surrogates-for-high-fide.pdf)

Scales neural surrogates to full high-fidelity car fields; a candidate surrogate architecture, with OOD caveats.

### AE-017 — Transolver: A Fast Transformer Solver for PDEs on General Geometries

Wu et al. · 2024 · International Conference on Machine Learning · **indirect**

[source](https://arxiv.org/abs/2402.02366) · [arXiv:2402.02366](https://arxiv.org/abs/2402.02366) · local PDF: [`papers/10_aerodynamics/AE-017_Wu2024_transolver-a-fast-transformer-solver-for-pdes-on-g.pdf`](../../../papers/10_aerodynamics/AE-017_Wu2024_transolver-a-fast-transformer-solver-for-pdes-on-g.pdf)

Physics-attention transformer for PDEs on arbitrary meshes including car aerodynamics; a general-geometry surrogate candidate.

### AE-018 — Geometry-Informed Neural Operator for Large-Scale 3D PDEs

Li et al. · 2023 · Neural Information Processing Systems · **indirect**

[source](https://arxiv.org/abs/2309.00583) · [arXiv:2309.00583](https://arxiv.org/abs/2309.00583) · local PDF: [`papers/10_aerodynamics/AE-018_Li2023_geometry-informed-neural-operator-for-large-scale.pdf`](../../../papers/10_aerodynamics/AE-018_Li2023_geometry-informed-neural-operator-for-large-scale.pdf)

GINO predicts car surface pressure from geometry; an early neural-operator car-aero result to reproduce.

### AE-019 — Learning Mesh-Based Simulation with Graph Networks

Pfaff et al. · 2021 · International Conference on Learning Representations · **indirect**

[source](https://arxiv.org/abs/2010.03409) · [arXiv:2010.03409](https://arxiv.org/abs/2010.03409) · local PDF: [`papers/10_aerodynamics/AE-019_Pfaff2021_learning-mesh-based-simulation-with-graph-networks.pdf`](../../../papers/10_aerodynamics/AE-019_Pfaff2021_learning-mesh-based-simulation-with-graph-networks.pdf)

MeshGraphNets learns mesh-based physics including aerodynamics; the base of many geometry-general surrogates.

### AE-020 — Learning Three-dimensional Flow for Interactive Aerodynamic Design

Umetani & Bickel · 2018 · ACM Transactions on Graphics · **indirect**

[source](https://doi.org/10.1145/3197517.3201325) · no local copy (download failed) · [open-access copy to fetch in a browser](https://zenodo.org/record/3495498)

Learned 3D flow and drag prediction for interactive car shape design; an early surrogate-in-the-loop design example.

### AE-021 — Surrogate Modeling of Car Drag Coefficient with Depth and Normal Renderings

Song et al. · 2023 · Design Automation Conference · **indirect**

[source](https://arxiv.org/abs/2306.06110) · [arXiv:2306.06110](https://arxiv.org/abs/2306.06110) · local PDF: [`papers/10_aerodynamics/AE-021_Song2023_surrogate-modeling-of-car-drag-coefficient-with-de.pdf`](../../../papers/10_aerodynamics/AE-021_Song2023_surrogate-modeling-of-car-drag-coefficient-with-de.pdf)

Image-based drag surrogate with a large car CFD dataset; a cheap screening surrogate to compare against field surrogates.

### AE-022 — Faster by Design: Interactive Aerodynamics via Neural Surrogates Trained on Expert-Validated CFD

Thumiger et al. · 2026 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2604.18491) · [arXiv:2604.18491](https://arxiv.org/abs/2604.18491) · local PDF: [`papers/10_aerodynamics/AE-022_Thumiger2026_faster-by-design-interactive-aerodynamics-via-neur.pdf`](../../../papers/10_aerodynamics/AE-022_Thumiger2026_faster-by-design-interactive-aerodynamics-via-neur.pdf)

Neural surrogates trained on expert-validated race-car CFD (including an LMP2 car); the closest race-car surrogate study.

### AE-023 — Multi-Granularity Conformal Prediction for Reliable Neural-Operator Automotive Aerodynamic Surrogates

Jia et al. · 2026 · arXiv · **direct**

[source](https://arxiv.org/abs/2607.17297) · [arXiv:2607.17297](https://arxiv.org/abs/2607.17297) · local PDF: [`papers/10_aerodynamics/AE-023_Jia2026_multi-granularity-conformal-prediction-for-reliabl.pdf`](../../../papers/10_aerodynamics/AE-023_Jia2026_multi-granularity-conformal-prediction-for-reliabl.pdf)

Conformal uncertainty bounds for aero surrogates; a way to attach calibrated error bars to surrogate-based promotion.

### AE-024 — Adapting Automotive Aerodynamics Surrogates to New Vehicle Families via Transfer Learning

Keum & Warey · 2026 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2605.27968) · [arXiv:2605.27968](https://arxiv.org/abs/2605.27968) · local PDF: [`papers/10_aerodynamics/AE-024_Keum2026_adapting-automotive-aerodynamics-surrogates-to-new.pdf`](../../../papers/10_aerodynamics/AE-024_Keum2026_adapting-automotive-aerodynamics-surrogates-to-new.pdf)

Measures surrogate failure and adaptation on new vehicle families; directly relevant because novel architectures are out of distribution.

### AE-025 — Towards a Foundation-Model Paradigm for Aerodynamic Prediction in Three-dimensional Design

Yang et al. · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2604.18062) · [arXiv:2604.18062](https://arxiv.org/abs/2604.18062) · local PDF: [`papers/10_aerodynamics/AE-025_Yang2026_towards-a-foundation-model-paradigm-for-aerodynami.pdf`](../../../papers/10_aerodynamics/AE-025_Yang2026_towards-a-foundation-model-paradigm-for-aerodynami.pdf)

Foundation-model approach to 3D aero prediction; context for general-geometry surrogates.

### AE-026 — SMART: Scalable Mesh-free Aerodynamic Simulations from Raw Geometries using a Transformer-based Surrogate Model

Hagnberger & Niepert · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2601.18707) · [arXiv:2601.18707](https://arxiv.org/abs/2601.18707) · local PDF: [`papers/10_aerodynamics/AE-026_Hagnberger2026_smart-scalable-mesh-free-aerodynamic-simulations-f.pdf`](../../../papers/10_aerodynamics/AE-026_Hagnberger2026_smart-scalable-mesh-free-aerodynamic-simulations-f.pdf)

Mesh-free surrogate from raw geometry; avoids a meshing step for early screening.

### AE-027 — AirfRANS: High Fidelity Computational Fluid Dynamics Dataset for Approximating Reynolds-Averaged Navier-Stokes Solutions

Bonnet et al. · 2022 · Neural Information Processing Systems · **data/findings**

[source](https://arxiv.org/abs/2212.07564) · [arXiv:2212.07564](https://arxiv.org/abs/2212.07564) · local PDF: [`papers/10_aerodynamics/AE-027_Bonnet2022_airfrans-high-fidelity-computational-fluid-dynamic.pdf`](../../../papers/10_aerodynamics/AE-027_Bonnet2022_airfrans-high-fidelity-computational-fluid-dynamic.pdf)

Airfoil RANS dataset with physics-consistency metrics; relevant to wing-element surrogates and evaluation of physical consistency.

### AE-028 — Adjoint methods for car aerodynamics

Othmer · 2014 · Journal of Mathematics in Industry · **direct**

[source](https://doi.org/10.1186/2190-5983-4-6) · local PDF: [`papers/10_aerodynamics/AE-028_Othmer2014_adjoint-methods-for-car-aerodynamics.pdf`](../../../papers/10_aerodynamics/AE-028_Othmer2014_adjoint-methods-for-car-aerodynamics.pdf)

Industrial adjoint shape and topology optimisation of car aerodynamics; the method for local aero improvement of admitted bodies.

### AE-029 — Introduction of a New Realistic Generic Car Model for Aerodynamic Investigations

Heft et al. · 2012 · SAE Technical Paper Series · **data/findings**

[source](https://doi.org/10.4271/2012-01-0168) · no local copy (no open-access copy found)

The DrivAer reference geometry and its experimental data; the basis of DrivAerNet/DrivAerML.

### AE-030 — Some Salient Features Of The Time-Averaged Ground Vehicle Wake

Ahmed et al. · 1984 · SAE Technical Paper Series · **data/findings**

[source](https://doi.org/10.4271/840300) · no local copy (no open-access copy found)

Ahmed-body experiments with drag versus slant angle; the classic validation case for vehicle wake CFD.

### AE-031 — Improved two-equation k-omega turbulence models for aerodynamic flows

Menter · 1992 · 23rd Fluid Dynamics, Plasmadynamics, and Lasers Conference · **indirect**

[source](https://doi.org/10.2514/6.1993-2906) · no local copy (no open-access copy found)

Menter's SST model report; the turbulence model most race-car RANS uses, with its known limits in separation.

### AE-032 — Experimental study of the vortex system generated by a Formula 1 front wing

— · 2006 · **data/findings**

[source](https://spiral.imperial.ac.uk/entities/publication/001dea4e-b1e9-490a-8daf-cc80fd398e38) · no local copy (no open-access copy found)

Thesis with detailed measurements of F1 front-wing vortices; experimental data for validating wing wake predictions.

### AE-033 — Fourier Neural Operator for Parametric Partial Differential Equations

Li et al. · 2021 · International Conference on Learning Representations · **indirect**

[source](https://arxiv.org/abs/2010.08895) · [arXiv:2010.08895](https://arxiv.org/abs/2010.08895) · local PDF: [`papers/10_aerodynamics/AE-033_Li2021_fourier-neural-operator-for-parametric-partial-dif.pdf`](../../../papers/10_aerodynamics/AE-033_Li2021_fourier-neural-operator-for-parametric-partial-dif.pdf)

Neural operator learning solution maps of PDEs; the base architecture of many flow surrogates.


## Thermal management, heat generation and cooling design

Heat-generation and thermal-network models for batteries and electric machines, and geometry-level cooling design. Supports the lumped thermal physics, coupled thermal-solid and flow/heat-exchange work (Works 014, 115, 121).

### TH-001 — A General Energy Balance for Battery Systems

Bernardi et al. · 1985 · Journal of The Electrochemical Society · **direct**

[source](https://doi.org/10.1149/1.2113792) · local PDF: [`papers/11_thermal_cooling/TH-001_Bernardi1985_a-general-energy-balance-for-battery-systems.pdf`](../../../papers/11_thermal_cooling/TH-001_Bernardi1985_a-general-energy-balance-for-battery-systems.pdf)

Bernardi's battery heat-generation equation (irreversible plus entropic heat); the source term for any battery thermal state.

### TH-002 — Lumped-parameter electro-thermal model for cylindrical batteries

Lin et al. · 2014 · Journal of Power Sources · **direct**

[source](https://doi.org/10.1016/j.jpowsour.2014.01.097) · no local copy (no open-access copy found)

Two-state core/surface thermal model identified from data; the right fidelity for race-long battery temperature.

### TH-003 — Evolution and Modern Approaches for Thermal Analysis of Electrical Machines

Boglietti et al. · 2009 · IEEE Transactions on Industrial Electronics · **direct**

[source](https://doi.org/10.1109/tie.2008.2011622) · no local copy (download failed) · [open-access copy to fetch in a browser](https://iris.polito.it/bitstream/11583/1938008/1/1938008.pdf)

Review of lumped thermal networks and CFD for electric machines; basis for motor derating in the powertrain model.

### TH-004 — Large scale three-dimensional topology optimisation of heat sinks cooled by natural convection

Alexandersen et al. · 2016 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/1508.04596) · [arXiv:1508.04596](https://arxiv.org/abs/1508.04596) · local PDF: [`papers/11_thermal_cooling/TH-004_Alexandersen2016_large-scale-three-dimensional-topology-optimisatio.pdf`](../../../papers/11_thermal_cooling/TH-004_Alexandersen2016_large-scale-three-dimensional-topology-optimisatio.pdf)

Full 3D conjugate-heat-transfer topology optimisation producing non-intuitive heat sinks; a precedent for discovered cooling geometry.

### TH-005 — A review about the engineering design of optimal heat transfer systems using topology optimization

Dbouk · 2017 · Applied Thermal Engineering · **indirect**

[source](https://doi.org/10.1016/j.applthermaleng.2016.10.134) · no local copy (no open-access copy found)

Review of topology optimisation for heat transfer devices; a map of methods for cooling-path discovery.

### TH-006 — Analysis of heat conduction in a disk brake system

Talati & Jalalifar · 2009 · Heat and Mass Transfer · **indirect**

[source](https://doi.org/10.1007/s00231-009-0476-y) · no local copy (no open-access copy found)

Transient brake-disc heat conduction; relevant to brake thermal limits and energy dissipated by friction braking.


## Materials, material data, fasteners and joints, crash structures, manufacturing and tolerances

Where real material and joint behaviour comes from, and how manufacturing and tolerances constrain designs. The project picks catalog materials only (no new composition design); real material values stay in private/ under the material data policy.

### MA-001 — On the engineering properties of materials

— · 1989 · **direct**

no local copy (no open-access copy found)

Ashby's material property charts and performance indices; the principled way to choose among catalog materials for a function.

### MA-002 — Commentary: The Materials Project: A materials genome approach to accelerating materials innovation

Jain et al. · 2013 · APL Materials · **data/findings**

[source](https://doi.org/10.1063/1.4812323) · no local copy (download failed) · [open-access copy to fetch in a browser](https://aip.scitation.org/doi/pdf/10.1063/1.4812323)

Open computed materials database; context and possible source for element-level properties, not for engineering allowables.

### MA-003 — Exploration of data science techniques to predict fatigue strength of steel from composition and processing parameters

Agrawal et al. · 2014 · Integrating Materials and Manufacturing Innovation · **data/findings**

[source](https://doi.org/10.1186/2193-9772-3-8) · local PDF: [`papers/12_materials_joints_manufacturing/MA-003_Agrawal2014_exploration-of-data-science-techniques-to-predict.pdf`](../../../papers/12_materials_joints_manufacturing/MA-003_Agrawal2014_exploration-of-data-science-techniques-to-predict.pdf)

Uses the NIMS fatigue data set of steels with composition and processing; an open fatigue data source and a model of its limits.

### MA-004 — New Criteria for Self-Loosening of Fasteners Under Vibration

Junker · 1969 · SAE Technical Paper Series · **direct**

[source](https://doi.org/10.4271/690055) · no local copy (no open-access copy found)

Junker's transverse-vibration loosening mechanism; the physics any bolted-joint gate must address.

### MA-005 — Three-dimensional finite element analysis of tightening and loosening mechanism of threaded fastener

Izumi et al. · 2005 · Engineering Failure Analysis · **direct**

[source](https://doi.org/10.1016/j.engfailanal.2004.09.009) · no local copy (no open-access copy found)

3D FE of thread contact during tightening and loosening; a verification reference for detailed connection contact (Work 113).

### MA-006 — Composite materials technology in formula 1 motor racing

— · 2008 · **data/findings**

no local copy (no open-access copy found)

Describes F1 composite structures, processes and failure considerations from a team engineer; context for composite part assumptions.

### MA-007 — Repair of composite structures on Formula 1 race cars

Savage & Oxley · 2010 · Engineering Failure Analysis · **indirect**

[source](https://doi.org/10.1016/j.engfailanal.2008.11.006) · no local copy (no open-access copy found)

Damage and repair of F1 composite parts; relevant to reliability and damage-tolerance assumptions.

### MA-008 — Crash Simulation of an F1 Racing Car Front Impact Structure

— · 2009 · **direct**

no local copy (no open-access copy found)

Explicit crash simulation of an F1 composite nose against the homologation test; a template for a future crash gate.

### MA-009 — A survey of research in the application of tolerance analysis to the design of mechanical assemblies

Chase & Parkinson · 1991 · Research in Engineering Design · **direct**

[source](https://doi.org/10.1007/bf01580066) · no local copy (download failed) · [open-access copy to fetch in a browser](http://adcats.et.byu.edu/WWW/RESEARCH/../Publication/91-1/DesRes_w_figs.PDF)

Worst-case versus statistical tolerance stack-up in assemblies; the method basis for the manufacturing tolerance handoff (Work 130).

### MA-010 — A comprehensive review of tolerancing research

Hong & Chang · 2002 · International Journal of Production Research · **indirect**

[source](https://doi.org/10.1080/00207540210128242) · no local copy (no open-access copy found)

Broad review of tolerance representation, analysis and synthesis; context for tolerance-aware geometry.

### MA-011 — Design for additive manufacturing: Trends, opportunities, considerations, and constraints

Thompson et al. · 2016 · CIRP Annals · **indirect**

[source](https://doi.org/10.1016/j.cirp.2016.05.004) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.sciencedirect.com/science/article/pii/S0007850616301913)

Constraints and opportunities of additive manufacturing; inputs for the declared manufacturing language.

### MA-012 — Scaling deep learning for materials discovery

Merchant et al. · 2023 · Nature · **direct**

[source](https://doi.org/10.1038/s41586-023-06735-9) · local PDF: [`papers/12_materials_joints_manufacturing/MA-012_Merchant2023_scaling-deep-learning-for-materials-discovery.pdf`](../../../papers/12_materials_joints_manufacturing/MA-012_Merchant2023_scaling-deep-learning-for-materials-discovery.pdf)

GNoME's large-scale 'discovery' claim; paired with MA-013 as a case study in how discovery claims are challenged.

### MA-013 — Artificial Intelligence Driving Materials Discovery? Perspective on the Article: Scaling Deep Learning for Materials Discovery

Cheetham & Seshadri · 2024 · Chemistry of Materials · **direct**

[source](https://doi.org/10.1021/acs.chemmater.4c00643) · no local copy (download failed) · [open-access copy to fetch in a browser](https://doi.org/10.1021/acs.chemmater.4c00643)

Critique showing many 'discovered' materials were not novel, useful or credible; a model for our distinction between generated, validated and discovered.

### MA-014 — A statistical distribution function of wide applicability

Weibull · 1951 · Journal of Applied Mechanics · **indirect**

[source](https://doi.org/10.1115/1.4010337) · no local copy (no open-access copy found)

Weibull distribution for strength scatter; relevant to probabilistic failure of brittle and composite parts.

### MA-015 — A comparison of the predictive capabilities of current failure theories for composite laminates, judged against experimental evidence

Hinton et al. · 2002 · Composites Science and Technology · **data/findings**

[source](https://doi.org/10.1016/s0266-3538(02)00125-2) · no local copy (no open-access copy found)

World-Wide Failure Exercise: composite failure theories scored blind against experiments; evidence of how uncertain composite failure prediction is.


## Verification, validation, calibration, statistics, reproducibility and claim discipline

How to show a solver solves its equations, how to show a model predicts reality, how to compare stochastic search methods honestly, and how optimisers exploit objectives and simulators. Grounds the evidence tiers, fidelity gates and review discipline in AGENTS.md.

### VV-001 — Verification and Validation in Computational Fluid Dynamics

OBERKAMPF & TRUCANO · 2002 · **direct** · Work 102 catalog P59

[source](https://doi.org/10.2172/793406) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.osti.gov/servlets/purl/793406)

Separates verification (solving equations right) from validation (right equations); the foundation of the project's evidence-tier language.

### VV-002 — Bayesian calibration of computer models

Kennedy & O'Hagan · 2001 · Journal of the Royal Statistical Society Series B: Statistical Methodology · **direct** · Work 102 catalog P58

[source](https://doi.org/10.1111/1467-9868.00294) · [arXiv:2006.07546](https://arxiv.org/abs/2006.07546) · local PDF: [`papers/13_validation_statistics_claims/VV-002_Kennedy2001_bayesian-calibration-of-computer-models.pdf`](../../../papers/13_validation_statistics_claims/VV-002_Kennedy2001_bayesian-calibration-of-computer-models.pdf)

Kennedy-O'Hagan calibration with an explicit model-discrepancy term; the plan for calibrating subsystems against measurements.

### VV-003 — Deep Reinforcement Learning at the Edge of the Statistical Precipice

Agarwal et al. · 2021 · Neural Information Processing Systems · **direct** · Work 102 catalog P60

[source](https://arxiv.org/abs/2108.13264) · [arXiv:2108.13264](https://arxiv.org/abs/2108.13264) · local PDF: [`papers/13_validation_statistics_claims/VV-003_Agarwal2021_deep-reinforcement-learning-at-the-edge-of-the-sta.pdf`](../../../papers/13_validation_statistics_claims/VV-003_Agarwal2021_deep-reinforcement-learning-at-the-edge-of-the-sta.pdf)

Interval estimates and robust aggregates for few-run comparisons; the reporting standard for seed-limited search campaigns.

### VV-004 — Code Verification by the Method of Manufactured Solutions

SALARI & KNUPP · 2000 · **direct**

[source](https://doi.org/10.2172/759450) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.osti.gov/servlets/purl/759450)

Manufactured solutions to verify order of accuracy of PDE codes; the method for independent solver verification (Work 138).

### VV-005 — A comprehensive framework for verification, validation, and uncertainty quantification in scientific computing

Roy & Oberkampf · 2011 · Computer Methods in Applied Mechanics and Engineering · **direct**

[source](https://doi.org/10.1016/j.cma.2011.03.016) · no local copy (no open-access copy found)

End-to-end VVUQ framework including numerical, input and model-form uncertainty; structure for the fidelity-promotion evidence.

### VV-006 — Procedure for Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications

Celik et al. · 2008 · Journal of Fluids Engineering · **direct**

[source](https://doi.org/10.1115/1.2960953) · no local copy (download failed) · [open-access copy to fetch in a browser](https://asmedigitalcollection.asme.org/fluidsengineering/article-pdf/130/7/078001/5491455/078001_1.pdf)

Grid convergence index procedure with three refinement levels; the reporting rule for mesh convergence claims.

### VV-007 — Perspective: A Method for Uniform Reporting of Grid Refinement Studies

Roache · 1994 · Journal of Fluids Engineering · **indirect**

[source](https://doi.org/10.1115/1.2910291) · no local copy (no open-access copy found)

Roache's original grid convergence index; background for VV-006.

### VV-008 — Verification, validation, and predictive capability in computational engineering and physics

Oberkampf et al. · 2004 · Applied Mechanics Reviews · **direct**

[source](https://doi.org/10.1115/1.1767847) · local PDF: [`papers/13_validation_statistics_claims/VV-008_Oberkampf2004_verification-validation-and-predictive-capability.pdf`](../../../papers/13_validation_statistics_claims/VV-008_Oberkampf2004_verification-validation-and-predictive-capability.pdf)

Defines predictive capability beyond validated conditions; relevant to extrapolating to novel architectures.

### VV-009 — Verification and validation of simulation models

Sargent · 2010 · Proceedings of the 2010 Winter Simulation Conference · **indirect**

[source](https://doi.org/10.1109/wsc.2010.5679166) · no local copy (download failed) · [open-access copy to fetch in a browser](http://repository.lib.ncsu.edu/bitstream/1840.4/5093/1/1994_0012.pdf)

Operational validation techniques for simulation models; practical checks for the race simulation itself.

### VV-010 — Combining field data and computer simulations for calibration and prediction

Higdon et al. · 2004 · SIAM Journal on Scientific Computing · **indirect**

[source](https://doi.org/10.1137/s1064827503426693) · no local copy (no open-access copy found)

Practical Bayesian calibration with field data and discrepancy; implementation detail for VV-002.

### VV-011 — Learning about physical parameters: the importance of model discrepancy

Brynjarsdóttir & OʼHagan · 2014 · Inverse Problems · **direct**

[source](https://doi.org/10.1088/0266-5611/30/11/114007) · no local copy (download failed) · [open-access copy to fetch in a browser](https://iopscience.iop.org/article/10.1088/0266-5611/30/11/114007/pdf)

Shows calibrated parameters are wrong unless discrepancy is modelled with prior knowledge; a warning for tyre and aero calibration.

### VV-012 — How Many Random Seeds? Statistical Power Analysis in Deep Reinforcement Learning Experiments

Colas et al. · 2018 · arXiv.org · **direct**

[source](https://arxiv.org/abs/1806.08295) · [arXiv:1806.08295](https://arxiv.org/abs/1806.08295) · local PDF: [`papers/13_validation_statistics_claims/VV-012_Colas2018_how-many-random-seeds-statistical-power-analysis-i.pdf`](../../../papers/13_validation_statistics_claims/VV-012_Colas2018_how-many-random-seeds-statistical-power-analysis-i.pdf)

Power analysis for choosing seed counts; directly applicable to sizing paired-seed search campaigns.

### VV-013 — Deep Reinforcement Learning that Matters

Henderson et al. · 2018 · AAAI Conference on Artificial Intelligence · **indirect**

[source](https://arxiv.org/abs/1709.06560) · [arXiv:1709.06560](https://arxiv.org/abs/1709.06560) · local PDF: [`papers/13_validation_statistics_claims/VV-013_Henderson2018_deep-reinforcement-learning-that-matters.pdf`](../../../papers/13_validation_statistics_claims/VV-013_Henderson2018_deep-reinforcement-learning-that-matters.pdf)

Shows seeds, implementations and hyperparameters can flip conclusions; motivates full replay metadata.

### VV-014 — Statistical Comparisons of Classifiers over Multiple Data Sets

— · 2006 · **indirect**

[source](https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf) · local PDF: [`papers/13_validation_statistics_claims/VV-014_Anon2006_statistical-comparisons-of-classifiers-over-multip.pdf`](../../../papers/13_validation_statistics_claims/VV-014_Anon2006_statistical-comparisons-of-classifiers-over-multip.pdf)

Non-parametric tests for comparing algorithms across many tasks; applicable to comparing search methods across circuits.

### VV-015 — Time for a Change: a Tutorial for Comparing Multiple Classifiers Through Bayesian Analysis

Benavoli et al. · 2017 · Journal of machine learning research · **indirect**

[source](https://arxiv.org/abs/1606.04316) · [arXiv:1606.04316](https://arxiv.org/abs/1606.04316) · local PDF: [`papers/13_validation_statistics_claims/VV-015_Benavoli2017_time-for-a-change-a-tutorial-for-comparing-multipl.pdf`](../../../papers/13_validation_statistics_claims/VV-015_Benavoli2017_time-for-a-change-a-tutorial-for-comparing-multipl.pdf)

Bayesian comparison with a region of practical equivalence; a way to say 'no practical difference' rather than 'not significant'.

### VV-016 — Benchmarking in Optimization: Best Practice and Open Issues

Bartz-Beielstein et al. · 2020 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2007.03488) · [arXiv:2007.03488](https://arxiv.org/abs/2007.03488) · local PDF: [`papers/13_validation_statistics_claims/VV-016_Beielstein2020_benchmarking-in-optimization-best-practice-and-ope.pdf`](../../../papers/13_validation_statistics_claims/VV-016_Beielstein2020_benchmarking-in-optimization-best-practice-and-ope.pdf)

Community best practice for benchmarking optimisers (budgets, baselines, reporting); a checklist for our campaign protocols.

### VV-017 — COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting

Hansen et al. · 2021 · Optim. Methods Softw. · **indirect**

[source](https://arxiv.org/abs/1603.08785) · [arXiv:1603.08785](https://arxiv.org/abs/1603.08785) · local PDF: [`papers/13_validation_statistics_claims/VV-017_Hansen2021_coco-a-platform-for-comparing-continuous-optimizer.pdf`](../../../papers/13_validation_statistics_claims/VV-017_Hansen2021_coco-a-platform-for-comparing-continuous-optimizer.pdf)

Budget-based anytime performance comparison of optimisers; a model for reporting quality versus evaluations.

### VV-018 — The preregistration revolution

Nosek et al. · 2018 · Proceedings of the National Academy of Sciences · **direct**

[source](https://doi.org/10.1073/pnas.1708274114) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.ncbi.nlm.nih.gov/pmc/articles/5856500)

Case for preregistering hypotheses and analyses; the rationale behind the project's frozen protocols before campaigns.

### VV-019 — Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)

Pineau et al. · 2021 · Journal of machine learning research · **indirect**

[source](https://arxiv.org/abs/2003.12206) · [arXiv:2003.12206](https://arxiv.org/abs/2003.12206) · local PDF: [`papers/13_validation_statistics_claims/VV-019_Pineau2021_improving-reproducibility-in-machine-learning-rese.pdf`](../../../papers/13_validation_statistics_claims/VV-019_Pineau2021_improving-reproducibility-in-machine-learning-rese.pdf)

Reproducibility checklist and findings; complements the replay metadata requirement.

### VV-020 — Troubling Trends in Machine Learning Scholarship

Lipton & Steinhardt · 2018 · Queue · **indirect**

[source](https://arxiv.org/abs/1807.03341) · [arXiv:1807.03341](https://arxiv.org/abs/1807.03341) · local PDF: [`papers/13_validation_statistics_claims/VV-020_Lipton2018_troubling-trends-in-machine-learning-scholarship.pdf`](../../../papers/13_validation_statistics_claims/VV-020_Lipton2018_troubling-trends-in-machine-learning-scholarship.pdf)

Catalogues overclaiming, speculation presented as explanation and ablation gaps; a reviewer's checklist for our own reports.

### VV-021 — The Surprising Creativity of Digital Evolution: A Collection of Anecdotes from the Evolutionary Computation and Artificial Life Research Communities

Lehman et al. · 2020 · Artificial Life · **direct**

[source](https://arxiv.org/abs/1803.03453) · [arXiv:1803.03453](https://arxiv.org/abs/1803.03453) · local PDF: [`papers/13_validation_statistics_claims/VV-021_Lehman2020_the-surprising-creativity-of-digital-evolution-a-c.pdf`](../../../papers/13_validation_statistics_claims/VV-021_Lehman2020_the-surprising-creativity-of-digital-evolution-a-c.pdf)

Dozens of cases where evolution exploited simulator bugs and loopholes; the evidence behind treating numerical exploits as an alternative explanation.

### VV-022 — Concrete Problems in AI Safety

Amodei et al. · 2016 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/1606.06565) · [arXiv:1606.06565](https://arxiv.org/abs/1606.06565) · local PDF: [`papers/13_validation_statistics_claims/VV-022_Amodei2016_concrete-problems-in-ai-safety.pdf`](../../../papers/13_validation_statistics_claims/VV-022_Amodei2016_concrete-problems-in-ai-safety.pdf)

Defines reward hacking and side effects; vocabulary for objective loopholes in design search.

### VV-023 — Defining and Characterizing Reward Hacking

Skalse et al. · 2022 · Advances in Neural Information Processing Systems 35 · **indirect**

[source](https://arxiv.org/abs/2209.13085) · [arXiv:2209.13085](https://arxiv.org/abs/2209.13085) · local PDF: [`papers/13_validation_statistics_claims/VV-023_Skalse2022_defining-and-characterizing-reward-hacking.pdf`](../../../papers/13_validation_statistics_claims/VV-023_Skalse2022_defining-and-characterizing-reward-hacking.pdf)

Formal definition of when a proxy objective is hackable; relevant to Level-0 race time as a proxy for real race time.

### VV-024 — Leakage and the reproducibility crisis in machine-learning-based science

Kapoor & Narayanan · 2023 · arXiv.org · **direct**

[source](https://arxiv.org/abs/2207.07048) · [arXiv:2207.07048](https://arxiv.org/abs/2207.07048) · local PDF: [`papers/13_validation_statistics_claims/VV-024_Kapoor2023_leakage-and-the-reproducibility-crisis-in-machine.pdf`](../../../papers/13_validation_statistics_claims/VV-024_Kapoor2023_leakage-and-the-reproducibility-crisis-in-machine.pdf)

Taxonomy of data leakage that inflates results; applicable to held-out tracks and surrogate training data.

### VV-025 — The garden of forking paths: Why multiple comparisons can be a problem, even when there is no fishing expedition or p-hacking and the research hypothesis was posited ahead of time

Watson · 2013 · New Directions in Travel Writing Studies · **indirect**

[source](https://doi.org/10.1057/9781137457257.0008) · local PDF: [`papers/13_validation_statistics_claims/VV-025_Watson2013_the-garden-of-forking-paths-why-multiple-compariso.pdf`](../../../papers/13_validation_statistics_claims/VV-025_Watson2013_the-garden-of-forking-paths-why-multiple-compariso.pdf)

Data-dependent analysis choices inflate false positives even without intent; supports freezing analyses before results.

### VV-026 — The ASA Statement on p-Values: Context, Process, and Purpose

Wasserstein & Lazar · 2016 · The American Statistician · **indirect**

[source](https://doi.org/10.1080/00031305.2016.1154108) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.tandfonline.com/doi/pdf/10.1080/00031305.2016.1154108?needAccess=true&role=button)

What p-values do and do not mean; relevant to reporting the non-significant campaign comparisons honestly.

### VV-027 — Noise and the reality gap: The use of simulation in evolutionary robotics

Jakobi et al. · 1995 · Lecture Notes in Computer Science · **direct**

[source](https://doi.org/10.1007/3-540-59496-5_337) · no local copy (no open-access copy found)

Adding the right noise to simulation to stop evolution exploiting simulator artefacts; an early reality-gap remedy.

### VV-028 — Robot Learning from Randomized Simulations: A Review

Muratore et al. · 2022 · Frontiers in Robotics and AI · **indirect**

[source](https://arxiv.org/abs/2111.00956) · [arXiv:2111.00956](https://arxiv.org/abs/2111.00956) · local PDF: [`papers/13_validation_statistics_claims/VV-028_Muratore2022_robot-learning-from-randomized-simulations-a-revie.pdf`](../../../papers/13_validation_statistics_claims/VV-028_Muratore2022_robot-learning-from-randomized-simulations-a-revie.pdf)

Reviews domain randomisation for sim-to-real; relevant to robustness across uncertain parameters.

### VV-029 — Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World

Tobin et al. · 2017 · IEEE/RJS International Conference on Intelligent RObots and Systems · **indirect**

[source](https://arxiv.org/abs/1703.06907) · [arXiv:1703.06907](https://arxiv.org/abs/1703.06907) · local PDF: [`papers/13_validation_statistics_claims/VV-029_Tobin2017_domain-randomization-for-transferring-deep-neural.pdf`](../../../papers/13_validation_statistics_claims/VV-029_Tobin2017_domain-randomization-for-transferring-deep-neural.pdf)

Randomising simulator parameters to transfer to reality; a robustness tactic for held-out conditions.

### VV-030 — Estimating the reproducibility of psychological science

Collaboration · 2015 · Science · **indirect**

[source](https://doi.org/10.1126/science.aac4716) · no local copy (download failed) · [open-access copy to fetch in a browser](https://research.tilburguniversity.edu/en/publications/4b1e6c37-3ee2-414b-b790-66024d631d4a)

Large replication effort showing weaker effects on replication; background for expecting shrinkage when promoted candidates are re-run.

### VV-031 — A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification

Angelopoulos & Bates · 2021 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2107.07511) · [arXiv:2107.07511](https://arxiv.org/abs/2107.07511) · local PDF: [`papers/13_validation_statistics_claims/VV-031_Angelopoulos2021_a-gentle-introduction-to-conformal-prediction-and.pdf`](../../../papers/13_validation_statistics_claims/VV-031_Angelopoulos2021_a-gentle-introduction-to-conformal-prediction-and.pdf)

Distribution-free prediction intervals for any surrogate; a simple way to bound surrogate error in promotion decisions.

### VV-032 — SALib: An open-source Python library for Sensitivity Analysis

Herman & Usher · 2017 · The Journal of Open Source Software · **indirect**

[source](https://doi.org/10.21105/joss.00097) · local PDF: [`papers/13_validation_statistics_claims/VV-032_Herman2017_salib-an-open-source-python-library-for-sensitivit.pdf`](../../../papers/13_validation_statistics_claims/VV-032_Herman2017_salib-an-open-source-python-library-for-sensitivit.pdf)

Global sensitivity analysis tooling (Sobol, Morris); for finding which parameters drive race-time rankings.


## Autonomous racing control, learned drivers, real telemetry and race strategy

Controllers and learned drivers that can drive each candidate near its limit, public real-car racing data, model identification from track data, and race-level strategy simulation. A weak driver makes good mechanics look bad, so driver quality is part of fairness.

### AR-001 — Outracing champion Gran Turismo drivers with deep reinforcement learning

Wurman et al. · 2022 · Nature · **indirect** · Work 102 catalog P40

[source](https://doi.org/10.1038/s41586-021-04357-7) · local PDF: [`papers/14_autonomous_racing_strategy/AR-001_Wurman2022_outracing-champion-gran-turismo-drivers-with-deep.pdf`](../../../papers/14_autonomous_racing_strategy/AR-001_Wurman2022_outracing-champion-gran-turismo-drivers-with-deep.pdf)

Learned driver beating top humans in a high-fidelity game; a method for strong per-design drivers, not physical validation.

### AR-002 — Optimization-Based Autonomous Racing of 1:43 Scale RC Cars

Liniger et al. · 2015 · arXiv.org · **indirect** · Work 102 catalog P41

[source](https://arxiv.org/abs/1711.07300) · [arXiv:1711.07300](https://arxiv.org/abs/1711.07300) · local PDF: [`papers/14_autonomous_racing_strategy/AR-002_Liniger2015_optimization-based-autonomous-racing-of-1-43-scale.pdf`](../../../papers/14_autonomous_racing_strategy/AR-002_Liniger2015_optimization-based-autonomous-racing-of-1-43-scale.pdf)

Model predictive contouring control for racing; an implementable controller baseline with explicit horizon and actuator limits.

### AR-003 — Analyzing the Impact of Simulation Fidelity on the Evaluation of Autonomous Driving Motion Control

Sagmeister et al. · 2024 · 2024 IEEE Intelligent Vehicles Symposium (IV) · **direct** · Work 102 catalog P42

[source](https://arxiv.org/abs/2602.07984) · [arXiv:2602.07984](https://arxiv.org/abs/2602.07984) · local PDF: [`papers/14_autonomous_racing_strategy/AR-003_Sagmeister2024_analyzing-the-impact-of-simulation-fidelity-on-the.pdf`](../../../papers/14_autonomous_racing_strategy/AR-003_Sagmeister2024_analyzing-the-impact-of-simulation-fidelity-on-the.pdf)

Ablates simulation fidelity against real autonomous-racing telemetry; the template for testing H4 fidelity survival.

### AR-004 — Autonomous Racing using Learning Model Predictive Control

Rosolia et al. · 2016 · American Control Conference · **indirect** · Work 102 catalog P62

[source](https://arxiv.org/abs/1610.06534) · [arXiv:1610.06534](https://arxiv.org/abs/1610.06534) · local PDF: [`papers/14_autonomous_racing_strategy/AR-004_Rosolia2016_autonomous-racing-using-learning-model-predictive.pdf`](../../../papers/14_autonomous_racing_strategy/AR-004_Rosolia2016_autonomous-racing-using-learning-model-predictive.pdf)

Iterative learning MPC improves lap time from previous laps; a controller that approaches each vehicle's limit.

### AR-005 — Autonomous Vehicles on the Edge: A Survey on Autonomous Vehicle Racing

Betz et al. · 2022 · IEEE Open Journal of Intelligent Transportation Systems · **indirect**

[source](https://arxiv.org/abs/2202.07008) · [arXiv:2202.07008](https://arxiv.org/abs/2202.07008) · local PDF: [`papers/14_autonomous_racing_strategy/AR-005_Betz2022_autonomous-vehicles-on-the-edge-a-survey-on-autono.pdf`](../../../papers/14_autonomous_racing_strategy/AR-005_Betz2022_autonomous-vehicles-on-the-edge-a-survey-on-autono.pdf)

Survey of perception, planning, control and simulation in autonomous racing; a map of tools and datasets.

### AR-006 — Indy Autonomous Challenge - Autonomous Race Cars at the Handling Limits

Wischnewski et al. · 2022 · arXiv.org · **data/findings**

[source](https://arxiv.org/abs/2202.03807) · [arXiv:2202.03807](https://arxiv.org/abs/2202.03807) · local PDF: [`papers/14_autonomous_racing_strategy/AR-006_Wischnewski2022_indy-autonomous-challenge-autonomous-race-cars-at.pdf`](../../../papers/14_autonomous_racing_strategy/AR-006_Wischnewski2022_indy-autonomous-challenge-autonomous-race-cars-at.pdf)

Full-scale autonomous racing at the handling limit with real vehicle behaviour; a reference for model-reality gaps at speed.

### AR-007 — TUM Autonomous Motorsport: An Autonomous Racing Software for the Indy Autonomous Challenge

Betz et al. · 2023 · J. Field Robotics · **indirect**

[source](https://arxiv.org/abs/2205.15979) · [arXiv:2205.15979](https://arxiv.org/abs/2205.15979) · local PDF: [`papers/14_autonomous_racing_strategy/AR-007_Betz2023_tum-autonomous-motorsport-an-autonomous-racing-sof.pdf`](../../../papers/14_autonomous_racing_strategy/AR-007_Betz2023_tum-autonomous-motorsport-an-autonomous-racing-sof.pdf)

Complete open autonomous racing stack with planning and control; reusable components for a driver baseline.

### AR-008 — RACECAR -- The Dataset for High-Speed Autonomous Racing

Kulkarni et al. · 2023 · IEEE/RJS International Conference on Intelligent RObots and Systems · **data/findings**

[source](https://arxiv.org/abs/2306.03252) · [arXiv:2306.03252](https://arxiv.org/abs/2306.03252) · local PDF: [`papers/14_autonomous_racing_strategy/AR-008_Kulkarni2023_racecar-the-dataset-for-high-speed-autonomous-raci.pdf`](../../../papers/14_autonomous_racing_strategy/AR-008_Kulkarni2023_racecar-the-dataset-for-high-speed-autonomous-raci.pdf)

Open multi-sensor data from full-scale autonomous Indy cars up to 273 km/h including banked tracks; real data for vehicle-model validation.

### AR-009 — AMZ Driverless: The Full Autonomous Racing System

Kabzan et al. · 2020 · J. Field Robotics · **indirect**

[source](https://arxiv.org/abs/1905.05150) · [arXiv:1905.05150](https://arxiv.org/abs/1905.05150) · local PDF: [`papers/14_autonomous_racing_strategy/AR-009_Kabzan2020_amz-driverless-the-full-autonomous-racing-system.pdf`](../../../papers/14_autonomous_racing_strategy/AR-009_Kabzan2020_amz-driverless-the-full-autonomous-racing-system.pdf)

Complete Formula Student driverless system with vehicle models and MPC; a well-documented reference implementation.

### AR-010 — Learning-Based Model Predictive Control for Autonomous Racing

Kabzan et al. · 2019 · IEEE Robotics and Automation Letters · **indirect**

[source](https://doi.org/10.1109/lra.2019.2926677) · no local copy (download failed) · [open-access copy to fetch in a browser](http://hdl.handle.net/20.500.11850/351561)

Gaussian-process correction of a nominal vehicle model inside MPC; a pattern for model-discrepancy learning in the driver.

### AR-011 — Super-Human Performance in Gran Turismo Sport Using Deep Reinforcement Learning

Fuchs et al. · 2021 · IEEE Robotics and Automation Letters · **indirect**

[source](https://arxiv.org/abs/2008.07971) · [arXiv:2008.07971](https://arxiv.org/abs/2008.07971) · local PDF: [`papers/14_autonomous_racing_strategy/AR-011_Fuchs2021_super-human-performance-in-gran-turismo-sport-usin.pdf`](../../../papers/14_autonomous_racing_strategy/AR-011_Fuchs2021_super-human-performance-in-gran-turismo-sport-usin.pdf)

RL driver reaching super-human lap times in time trials; a learned-driver baseline method.

### AR-012 — Reaching the Limit in Autonomous Racing: Optimal Control versus Reinforcement Learning

Song et al. · 2023 · Science Robotics · **direct**

[source](https://arxiv.org/abs/2310.10943) · [arXiv:2310.10943](https://arxiv.org/abs/2310.10943) · local PDF: [`papers/14_autonomous_racing_strategy/AR-012_Song2023_reaching-the-limit-in-autonomous-racing-optimal-co.pdf`](../../../papers/14_autonomous_racing_strategy/AR-012_Song2023_reaching-the-limit-in-autonomous-racing-optimal-co.pdf)

Compares optimal control and RL for drone racing at the limit; evidence for choosing driver methods under model mismatch.

### AR-013 — Champion-level drone racing using deep reinforcement learning

Kaufmann et al. · 2023 · Nature · **indirect**

[source](https://doi.org/10.1038/s41586-023-06419-4) · local PDF: [`papers/14_autonomous_racing_strategy/AR-013_Kaufmann2023_champion-level-drone-racing-using-deep-reinforceme.pdf`](../../../papers/14_autonomous_racing_strategy/AR-013_Kaufmann2023_champion-level-drone-racing-using-deep-reinforceme.pdf)

Learned policy beating human champions in the real world with residual models from real data; an example of closing the sim-to-real gap.

### AR-014 — Application of Monte Carlo Methods to Consider Probabilistic Effects in a Race Simulation for Circuit Motorsport

Heilmeier et al. · 2020 · Applied Sciences · **direct**

[source](https://doi.org/10.3390/app10124229) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.mdpi.com/2076-3417/10/12/4229/pdf?version=1597915201)

Race simulation with probabilistic events (safety cars, failures) via Monte Carlo; relevant to total race time rather than one lap.

### AR-015 — Virtual Strategy Engineer: Using Artificial Neural Networks for Making Race Strategy Decisions in Circuit Motorsport

Heilmeier et al. · 2020 · Applied Sciences · **indirect**

[source](https://doi.org/10.3390/app10217805) · no local copy (download failed) · [open-access copy to fetch in a browser](https://www.mdpi.com/2076-3417/10/21/7805/pdf)

Learned pit and compound strategy decisions in a race simulation; strategy is part of total race time.

### AR-016 — A Race Simulation for Strategy Decisions in Circuit Motorsports

Heilmeier et al. · 2018 · 2018 21st International Conference on Intelligent Transportation Systems (ITSC) · **direct**

[source](https://doi.org/10.1109/itsc.2018.8570012) · no local copy (no open-access copy found)

Lap-by-lap race simulation with tyre degradation and fuel mass; a public model of race-length (not lap-length) time.

### AR-017 — Towards Learning-Based Formula 1 Race Strategies

Fieni et al. · 2025 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2512.21570) · [arXiv:2512.21570](https://arxiv.org/abs/2512.21570) · local PDF: [`papers/14_autonomous_racing_strategy/AR-017_Fieni2025_towards-learning-based-formula-1-race-strategies.pdf`](../../../papers/14_autonomous_racing_strategy/AR-017_Fieni2025_towards-learning-based-formula-1-race-strategies.pdf)

Learning-based F1 strategy; recent context for race-level decision making.

### AR-018 — Game Theory in Formula 1: From Physical to Strategic Interactions

Fieni et al. · 2025 · European Journal of Control · **indirect**

[source](https://arxiv.org/abs/2503.05421) · [arXiv:2503.05421](https://arxiv.org/abs/2503.05421) · local PDF: [`papers/14_autonomous_racing_strategy/AR-018_Fieni2025_game-theory-in-formula-1-from-physical-to-strategi.pdf`](../../../papers/14_autonomous_racing_strategy/AR-018_Fieni2025_game-theory-in-formula-1-from-physical-to-strategi.pdf)

Game-theoretic view of F1 interactions; relevant only if multi-car races enter the environment.

### AR-019 — Opponent State Inference Under Partial Observability: An HMM-POMDP Framework for 2026 Formula 1 Energy Strategy

Kleisarchaki · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2603.01290) · [arXiv:2603.01290](https://arxiv.org/abs/2603.01290) · local PDF: [`papers/14_autonomous_racing_strategy/AR-019_Kleisarchaki2026_opponent-state-inference-under-partial-observabili.pdf`](../../../papers/14_autonomous_racing_strategy/AR-019_Kleisarchaki2026_opponent-state-inference-under-partial-observabili.pdf)

Models 2026-regulation energy strategy including Override Mode; context for the regulation profile our race contract pins.

### AR-020 — Bridging RL and MPC for mixed-integer optimal control with application to Formula 1 race strategies

Wüthrich et al. · 2026 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2604.00826) · [arXiv:2604.00826](https://arxiv.org/abs/2604.00826) · local PDF: [`papers/14_autonomous_racing_strategy/AR-020_Wuthrich2026_bridging-rl-and-mpc-for-mixed-integer-optimal-cont.pdf`](../../../papers/14_autonomous_racing_strategy/AR-020_Wuthrich2026_bridging-rl-and-mpc-for-mixed-integer-optimal-cont.pdf)

Combines RL and MPC for mixed-integer race strategy; relevant to discrete strategy choices.

### AR-021 — Mission Performance: Automatic and Adaptive Race Pace Progression for Autonomous Racing

Lambertini et al. · 2026 · arXiv · **indirect**

[source](https://arxiv.org/abs/2609.12292) · [arXiv:2609.12292](https://arxiv.org/abs/2609.12292) · local PDF: [`papers/14_autonomous_racing_strategy/AR-021_Lambertini2026_mission-performance-automatic-and-adaptive-race-pa.pdf`](../../../papers/14_autonomous_racing_strategy/AR-021_Lambertini2026_mission-performance-automatic-and-adaptive-race-pa.pdf)

Adaptive pace progression towards the limit; relevant to safely finding each candidate's achievable pace.

### AR-022 — Learning-Based On-Track System Identification for Scaled Autonomous Racing in Under a Minute

Dikici et al. · 2024 · IEEE Robotics and Automation Letters · **direct**

[source](https://arxiv.org/abs/2411.17508) · [arXiv:2411.17508](https://arxiv.org/abs/2411.17508) · local PDF: [`papers/14_autonomous_racing_strategy/AR-022_Dikici2024_learning-based-on-track-system-identification-for.pdf`](../../../papers/14_autonomous_racing_strategy/AR-022_Dikici2024_learning-based-on-track-system-identification-for.pdf)

Identifies tyre/vehicle models from about 30 s of driving data; a fast calibration route for physical correlation.

### AR-023 — Deep Dynamics: Vehicle Dynamics Modeling with a Physics-Informed Neural Network for Autonomous Racing

Chrosniak et al. · 2024 · IEEE Robotics and Automation Letters · **indirect**

[source](https://arxiv.org/abs/2312.04374) · [arXiv:2312.04374](https://arxiv.org/abs/2312.04374) · local PDF: [`papers/14_autonomous_racing_strategy/AR-023_Chrosniak2024_deep-dynamics-vehicle-dynamics-modeling-with-a-phy.pdf`](../../../papers/14_autonomous_racing_strategy/AR-023_Chrosniak2024_deep-dynamics-vehicle-dynamics-modeling-with-a-phy.pdf)

Physics-informed network that estimates interpretable vehicle parameters from data; a hybrid model-identification option.

### AR-024 — F1TENTH: An Open-source Evaluation Environment for Continuous Control and Reinforcement Learning

— · 2020 · **indirect**

[source](https://proceedings.mlr.press/v123/o-kelly20a/o-kelly20a.pdf) · local PDF: [`papers/14_autonomous_racing_strategy/AR-024_Anon2020_f1tenth-an-open-source-evaluation-environment-for.pdf`](../../../papers/14_autonomous_racing_strategy/AR-024_Anon2020_f1tenth-an-open-source-evaluation-environment-for.pdf)

Open scaled-racing evaluation environment with physical cars; a low-cost physical testbed idea.

### AR-025 — Real-Time Adaptive Velocity Optimization for Autonomous Electric Cars at the Limits of Handling

Herrmann et al. · 2021 · IEEE Transactions on Intelligent Vehicles · **indirect**

[source](https://doi.org/10.1109/tiv.2020.3047858) · [arXiv:2012.13586](https://arxiv.org/abs/2012.13586) · local PDF: [`papers/14_autonomous_racing_strategy/AR-025_Herrmann2021_real-time-adaptive-velocity-optimization-for-auton.pdf`](../../../papers/14_autonomous_racing_strategy/AR-025_Herrmann2021_real-time-adaptive-velocity-optimization-for-auton.pdf)

Real-time velocity planning with energy and friction limits on an electric racecar; a driver component for energy-limited races.

### AR-026 — Efficient Trajectory Optimization for Autonomous Racing via Formula-1 Data-Driven Initialization

Shehadeh et al. · 2026 · arXiv.org · **data/findings**

[source](https://arxiv.org/abs/2603.07126) · [arXiv:2603.07126](https://arxiv.org/abs/2603.07126) · local PDF: [`papers/14_autonomous_racing_strategy/AR-026_Shehadeh2026_efficient-trajectory-optimization-for-autonomous-r.pdf`](../../../papers/14_autonomous_racing_strategy/AR-026_Shehadeh2026_efficient-trajectory-optimization-for-autonomous-r.pdf)

Uses real Formula 1 trajectory data to initialise racing-line optimisation; a source of public F1 line data and a warm-start method.

### AR-027 — Unifying F1TENTH Autonomous Racing: Survey, Methods and Benchmarks

Evans et al. · 2024 · arXiv.org · **indirect**

[source](https://arxiv.org/abs/2402.18558) · [arXiv:2402.18558](https://arxiv.org/abs/2402.18558) · local PDF: [`papers/14_autonomous_racing_strategy/AR-027_Evans2024_unifying-f1tenth-autonomous-racing-survey-methods.pdf`](../../../papers/14_autonomous_racing_strategy/AR-027_Evans2024_unifying-f1tenth-autonomous-racing-survey-methods.pdf)

Benchmarks of racing planners and controllers on a common platform; a reference for fair controller comparisons.


## Computational design synthesis, functional representation, assembly synthesis and novelty measurement

Engineering-design research on generating architectures from functions with grammars, decomposing structures into joined parts, and measuring whether a design is actually novel. Relevant to typed interfaces, the physical interface graph, part resolution and the project's definition of a discovery.

### DS-001 — Computational Synthesis of Product Architectures Based on Object-Oriented Graph Grammars

Helms & Shea · 2012 · Journal of Mechanical Design · **direct**

[source](https://doi.org/10.1115/1.4005592) · no local copy (no open-access copy found)

Object-oriented graph grammars over function-behaviour-structure models, validated on hybrid powertrain synthesis; the closest engineering-design precedent to our typed topology genome.

### DS-002 — A framework for computational design synthesis based on graph-grammars and function-behavior-structure

Helms et al. · 2009 · Volume 8: 14th Design for Manufacturing and the Life Cycle Conference; 6th Symposium on International Design and Design Education; 21st International Conference on Design Theory and Methodology, Parts A and B · **direct**

[source](https://doi.org/10.1115/detc2009-86851) · no local copy (download failed) · [open-access copy to fetch in a browser](http://mediatum.ub.tum.de/node?id=1155306)

The framework paper behind DS-001; defines how functional requirements drive grammar-based architecture generation.

### DS-003 — Comparing Strategies for Topologic and Parametric Rule Application in Automated Computational Design Synthesis

Königseder & Shea · 2016 · Journal of Mechanical Design · **direct**

[source](https://doi.org/10.1115/1.4031714) · no local copy (no open-access copy found)

Compares how topological and parametric grammar rules should be interleaved in search; directly relevant to mutation scheduling.

### DS-004 — Computer-Based Design Synthesis Research: An Overview

Chakrabarti et al. · 2011 · Journal of Computing and Information Science in Engineering · **indirect**

[source](https://doi.org/10.1115/1.3593409) · no local copy (download failed) · [open-access copy to fetch in a browser](http://mediatum.ub.tum.de/node?id=1161039)

Overview of computational design synthesis methods and their evaluation; places the project within prior synthesis research.

### DS-005 — A Framework for Computational Design Synthesis: Model and Applications

Cagan et al. · 2005 · Journal of Computing and Information Science in Engineering · **indirect**

[source](https://doi.org/10.1115/1.2013289) · no local copy (no open-access copy found)

Representation-generation-evaluation-guidance model of design synthesis; a vocabulary for separating our generator from evaluators.

### DS-006 — A functional basis for engineering design: Reconciling and evolving previous efforts

Hirtz et al. · 2002 · Research in Engineering Design · **direct**

[source](https://doi.org/10.1007/s00163-001-0008-3) · no local copy (no open-access copy found)

Standard taxonomy of functions and flows (material, energy, signal); a basis for typed functional interfaces independent of form.

### DS-007 — Development of a Functional Basis for Design

Stone & Wood · 2000 · Journal of Mechanical Design · **indirect**

[source](https://doi.org/10.1115/1.1289637) · no local copy (no open-access copy found)

The first functional-basis vocabulary; background for DS-006.

### DS-008 — Design prototypes: a knowledge representation schema for design

— · 1990 · **indirect**

[source](https://aaai.org/ojs/index.php/aimagazine/article/view/854) · no local copy (no open-access copy found)

Function-behaviour-structure framing; separates what a part does from how it is built, as our discovery criteria require.

### DS-009 — Automated synthesis of electromechanical design configurations from empirical analysis of function to form mapping

Kurtoglu & Campbell · 2009 · Journal of Engineering Design · **indirect**

[source](https://doi.org/10.1080/09544820701546165) · local PDF: [`papers/15_design_synthesis_novelty/DS-009_Kurtoglu2009_automated-synthesis-of-electromechanical-design-co.pdf`](../../../papers/15_design_synthesis_novelty/DS-009_Kurtoglu2009_automated-synthesis-of-electromechanical-design-co.pdf)

Learns function-to-component mappings from real products to synthesise configurations; a data-driven grammar source.

### DS-010 — Metrics for measuring ideation effectiveness

Shah et al. · 2003 · Design Studies · **direct**

[source](https://doi.org/10.1016/s0142-694x(02)00034-0) · no local copy (no open-access copy found)

Novelty, variety, quality and quantity metrics for design ideas; operational definitions for measuring novelty of generated architectures.

### DS-011 — Assessing design creativity

Sarkar & Chakrabarti · 2011 · Design Studies · **indirect**

[source](https://doi.org/10.1016/j.destud.2011.01.002) · no local copy (no open-access copy found)

Combines novelty and usefulness into a creativity measure; relevant to separating novel-but-useless from useful discoveries.

### DS-012 — Measuring technological novelty with patent-based indicators

Verhoeven et al. · 2016 · Research Policy · **indirect**

[source](https://doi.org/10.1016/j.respol.2015.11.010) · local PDF: [`papers/15_design_synthesis_novelty/DS-012_Verhoeven2016_measuring-technological-novelty-with-patent-based.pdf`](../../../papers/15_design_synthesis_novelty/DS-012_Verhoeven2016_measuring-technological-novelty-with-patent-based.pdf)

Patent-based measures of new combinations and new functions; an external reference for what counts as a technology-level novelty.

### DS-013 — Decomposition-Based Assembly Synthesis of Space Frame Structures Using Joint Library

Lyu & Saitou · 2005 · Volume 1: 30th Design Automation Conference · **direct**

[source](https://doi.org/10.1115/detc2004-57301) · no local copy (no open-access copy found)

Decomposes a frame into parts and chooses joints from a library under structural and manufacturing objectives; the same problem as part resolution with joint systems (Works 140-142).

### DS-014 — Decomposition-Based Assembly Synthesis Based on Structural Considerations

Yetis & Saitou · 2002 · Journal of Mechanical Design · **direct**

[source](https://doi.org/10.1115/1.1519276) · no local copy (no open-access copy found)

Earlier decomposition-based assembly synthesis driven by stiffness; method basis for DS-013.

### DS-015 — Multi-component topology and material orientation design of composite structures (MTO-C)

Zhou et al. · 2018 · Computer Methods in Applied Mechanics and Engineering · **direct**

[source](https://doi.org/10.1016/j.cma.2018.07.039) · no local copy (no open-access copy found)

Simultaneously optimises structural topology and its decomposition into manufacturable composite components; closes the gap between topology and part count.

### DS-016 — Patterns in System Architecture Decisions

Selva et al. · 2016 · Systems Engineering · **indirect**

[source](https://doi.org/10.1002/sys.21370) · no local copy (no open-access copy found)

Classifies architecture decisions (assigning, partitioning, connecting) into patterns with search formulations; a formal view of vehicle-architecture choices.

### DS-017 — Generative Transformers for Design Concept Generation

Zhu & Luo · 2023 · Journal of Computing and Information Science in Engineering · **indirect**

[source](https://arxiv.org/abs/2211.03468) · [arXiv:2211.03468](https://arxiv.org/abs/2211.03468) · local PDF: [`papers/15_design_synthesis_novelty/DS-017_Zhu2023_generative-transformers-for-design-concept-generat.pdf`](../../../papers/15_design_synthesis_novelty/DS-017_Zhu2023_generative-transformers-for-design-concept-generat.pdf)

Transformer-based concept generation from design knowledge; a text-level proposal route before geometry.


## Open-access papers to download by hand

A free copy of each paper below exists, but its host refused scripted downloads (mostly Cloudflare-style bot checks at MDPI, ACM, PNAS, Royal Society, IEEE and some university repositories), and that check was not bypassed. Open the link in a browser, save the PDF into one folder, then run `python scripts/research/build_paper_library.py --ingest <folder>`. Naming a file `<ID>.pdf` (for example `OE-003.pdf`) makes the match explicit; the title check still applies.

| ID | Title | Open in a browser |
| --- | --- | --- |
| OE-003 | RoboGrammar: Graph Grammar for Terrain-Optimized Robot Design | [dl.acm.org](https://dl.acm.org/doi/pdf/10.1145/3414685.3417831) |
| OE-018 | Morphological change in machines accelerates the evolution of robust behavior | [www.ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/pmc/articles/3029735) |
| OE-019 | A scalable pipeline for designing reconfigurable organisms | [doi.org](https://doi.org/10.1073/pnas.1910837117) |
| OE-043 | Evolving three-dimensional objects with a generative encoding inspired by developmental biology | [doi.org](https://doi.org/10.7551/978-0-262-29714-1-ch024) |
| QD-031 | Nonlinear information fusion algorithms for data-efficient multi-fidelity modelling | [www.ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/pmc/articles/5332612) |
| CAD-024 | BrepDiff: Single-stage B-rep Diffusion Model | [doi.org](https://doi.org/10.1145/3721238.3730698) |
| CAD-030 | Hierarchical CADNet: Learning from B-Reps for Machining Feature Recognition | [www.sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0010448522000240/pdf) |
| ST-002 | A 99 line topology optimization code written in Matlab | [orbit.dtu.dk](http://orbit.dtu.dk/en/publications/a-99-line-topology-optimization-code-written-in-matlab(b0794468-93a9-4cca-87b3-b4224938859a).html) |
| ST-005 | Topology optimization approaches: A comparative review | [orbit.dtu.dk](http://orbit.dtu.dk/en/publications/topology-optimization-approaches(f861e156-422e-4bb0-a0ad-d378322003f9).html) |
| ST-010 | A Review of Topology Optimisation for Fluid-Based Problems | [www.mdpi.com](https://www.mdpi.com/2311-5521/5/1/29/pdf) |
| ST-013 | Tetrahedral Meshing in the Wild | [dl.acm.org](https://dl.acm.org/doi/pdf/10.1145/3197517.3201353) |
| SI-004 | MuJoCo: A physics engine for model-based control | [homes.cs.washington.edu](https://homes.cs.washington.edu/~todorov/papers/TodorovIROS12.pdf) |
| SI-008 | The Pinocchio C++ library: A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives | [hal.laas.fr](https://hal.laas.fr/hal-01866228v2/file/19-sii-pinocchio.pdf) |
| SI-016 | The Functional Mockup Interface for Tool independent Exchange of Simulation Models | [www.ep.liu.se](http://www.ep.liu.se/ecp/063/013/ecp11063013.pdf) |
| LT-006 | Minimum curvature trajectory planning and control for an autonomous race car | [mediatum.ub.tum.de](http://mediatum.ub.tum.de/node?id=1509975) |
| LT-009 | Lap time optimisation of a racing go-kart | [eprints.soton.ac.uk](https://eprints.soton.ac.uk/385883/2/Lap%2520time%2520optimisation%2520of%2520a%2520racing%2520go-kart%2520%2528corrected%2520proof%2529.pdf) |
| LT-011 | A free-trajectory quasi-steady-state optimal-control method for minimum lap-time of race vehicles | [hdl.handle.net](http://hdl.handle.net/11577/3297111) |
| LT-012 | A three-dimensional free-trajectory quasi-steady-state optimal-control method for minimum-lap-time of race vehicles | [hdl.handle.net](http://hdl.handle.net/11577/3375385) |
| LT-018 | On minimum time vehicle manoeuvring: the theoretical optimal lap | [core.ac.uk](https://core.ac.uk/download/pdf/138004.pdf) |
| LT-019 | Minimum-lap-time optimisation and simulation | [hdl.handle.net](http://hdl.handle.net/11577/3389257) |
| LT-020 | Comparison of direct and indirect methods for minimum lap time optimal control problems | [iris.unitn.it](https://iris.unitn.it/bitstream/11572/211730/4/2_PDFsam_2018dir_vs_indirpreprint.pdf) |
| LT-021 | Optimal control of motorsport differentials | [www.tandfonline.com](https://www.tandfonline.com/doi/pdf/10.1080/00423114.2015.1093150?needAccess=true) |
| LT-022 | A Convex Optimization Framework for Minimum Lap Time Design and Control of Electric Race Cars | [research.tue.nl](https://research.tue.nl/en/publications/98d6f349-dcae-447b-86cc-8d61e15b7107) |
| LT-028 | The kinematic bicycle model: A consistent model for planning feasible trajectories for autonomous vehicles? | [polytechnique.hal.science](https://polytechnique.hal.science/hal-01520869) |
| LT-030 | Simultaneous Optimisation of Vehicle Design and Control for Improving Vehicle Performance and Energy Efficiency Using an Open Source Minimum Lap Time Simulation Framework | [www.mdpi.com](https://www.mdpi.com/2032-6653/15/8/366/pdf?version=1724141770) |
| EN-001 | Optimal control of Formula One car energy recovery systems | [www.anilvrao.com](https://www.anilvrao.com/Publications/JournalPublications/F-1-Optimal-Control-Energy-Recovery.pdf) |
| EN-002 | Optimal energy management for formula-E cars with regulatory limits and thermal constraints | [dspace.lib.cranfield.ac.uk](https://dspace.lib.cranfield.ac.uk/bitstream/1826/15797/1/Optimal_energy_management_for_formula-E_cars_with_regulatory_limits_and_thermal_constraints-2020.pdf) |
| EN-005 | Time-optimal gearshift and energy management strategies for a hybrid electric race car | [www.sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0306261920314288/pdf) |
| EN-006 | Time-optimal low-level control and gearshift strategies for the formula 1 hybrid electric powertrain | [www.mdpi.com](https://www.mdpi.com/1996-1073/14/1/171/pdf?version=1609831608) |
| EN-014 | Review of Optimization Strategies for System-Level Design in Hybrid Electric Vehicles | [research.tue.nl](https://research.tue.nl/en/publications/69ba1672-e399-42f9-a7f4-f3633784ffb8) |
| EN-018 | Review of parameterisation and a novel database (LiionDB) for continuum Li-ion battery models | [iopscience.iop.org](https://iopscience.iop.org/article/10.1088/2516-1083/ac692c/pdf) |
| EN-024 | Modeling of Galvanostatic Charge and Discharge of the Lithium/Polymer/Insertion Cell | [iopscience.iop.org](https://iopscience.iop.org/article/10.1149/1.2221597/pdf) |
| EN-026 | Overview of current development in electrical energy storage technologies and the application potential in power system operation | [www.sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0306261914010290/pdf) |
| EN-028 | A Review of Flywheel Energy Storage System Technologies and Their Applications | [www.mdpi.com](https://www.mdpi.com/2076-3417/7/3/286/pdf?version=1489660272) |
| EN-029 | A Comprehensive Review on Supercapacitor Applications and Developments | [www.mdpi.com](https://www.mdpi.com/1996-1073/15/3/674/pdf?version=1642493431) |
| TY-003 | An improved Magic Formula/Swift tyre model that can handle inflation pressure changes | [pure.tue.nl](https://pure.tue.nl/ws/files/3139490/Metis245615.pdf) |
| TY-007 | Theory of rubber friction and contact mechanics | [juser.fz-juelich.de](http://juser.fz-juelich.de/record/42969/files/6009.pdf) |
| TY-016 | Estimation of tire-road friction coefficient and its application in chassis control systems | [doi.org](https://doi.org/10.1080/21642583.2014.985804) |
| AE-003 | DAFoam: An Open-Source Adjoint Framework for Multidisciplinary Design Optimization with OpenFOAM | [arc.aiaa.org](https://arc.aiaa.org/doi/pdf/10.2514/1.J058853) |
| AE-014 | The effects of simplifications on isolated wheel aerodynamics | [digitalcommons.calpoly.edu](https://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1151&context=aero_fac) |
| AE-015 | CFD Investigation of the Effect of the Salient Flow Features in the Wake of a Generic Open-Wheel Race Car | [nrl.northumbria.ac.uk](http://nrl.northumbria.ac.uk/id/eprint/25043/1/SAE%202015-01-1539_PrePublication_Dominy-Newbon.pdf) |
| AE-020 | Learning Three-dimensional Flow for Interactive Aerodynamic Design | [zenodo.org](https://zenodo.org/record/3495498) |
| TH-003 | Evolution and Modern Approaches for Thermal Analysis of Electrical Machines | [iris.polito.it](https://iris.polito.it/bitstream/11583/1938008/1/1938008.pdf) |
| MA-002 | Commentary: The Materials Project: A materials genome approach to accelerating materials innovation | [aip.scitation.org](https://aip.scitation.org/doi/pdf/10.1063/1.4812323) |
| MA-009 | A survey of research in the application of tolerance analysis to the design of mechanical assemblies | [adcats.et.byu.edu](http://adcats.et.byu.edu/WWW/RESEARCH/../Publication/91-1/DesRes_w_figs.PDF) |
| MA-011 | Design for additive manufacturing: Trends, opportunities, considerations, and constraints | [www.sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0007850616301913) |
| MA-013 | Artificial Intelligence Driving Materials Discovery? Perspective on the Article: Scaling Deep Learning for Materials Discovery | [doi.org](https://doi.org/10.1021/acs.chemmater.4c00643) |
| VV-001 | Verification and Validation in Computational Fluid Dynamics | [www.osti.gov](https://www.osti.gov/servlets/purl/793406) |
| VV-004 | Code Verification by the Method of Manufactured Solutions | [www.osti.gov](https://www.osti.gov/servlets/purl/759450) |
| VV-006 | Procedure for Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications | [asmedigitalcollection.asme.org](https://asmedigitalcollection.asme.org/fluidsengineering/article-pdf/130/7/078001/5491455/078001_1.pdf) |
| VV-009 | Verification and validation of simulation models | [repository.lib.ncsu.edu](http://repository.lib.ncsu.edu/bitstream/1840.4/5093/1/1994_0012.pdf) |
| VV-011 | Learning about physical parameters: the importance of model discrepancy | [iopscience.iop.org](https://iopscience.iop.org/article/10.1088/0266-5611/30/11/114007/pdf) |
| VV-018 | The preregistration revolution | [www.ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov/pmc/articles/5856500) |
| VV-026 | The ASA Statement on p-Values: Context, Process, and Purpose | [www.tandfonline.com](https://www.tandfonline.com/doi/pdf/10.1080/00031305.2016.1154108?needAccess=true&role=button) |
| VV-030 | Estimating the reproducibility of psychological science | [research.tilburguniversity.edu](https://research.tilburguniversity.edu/en/publications/4b1e6c37-3ee2-414b-b790-66024d631d4a) |
| AR-010 | Learning-Based Model Predictive Control for Autonomous Racing | [hdl.handle.net](http://hdl.handle.net/20.500.11850/351561) |
| AR-014 | Application of Monte Carlo Methods to Consider Probabilistic Effects in a Race Simulation for Circuit Motorsport | [www.mdpi.com](https://www.mdpi.com/2076-3417/10/12/4229/pdf?version=1597915201) |
| AR-015 | Virtual Strategy Engineer: Using Artificial Neural Networks for Making Race Strategy Decisions in Circuit Motorsport | [www.mdpi.com](https://www.mdpi.com/2076-3417/10/21/7805/pdf) |
| DS-002 | A framework for computational design synthesis based on graph-grammars and function-behavior-structure | [mediatum.ub.tum.de](http://mediatum.ub.tum.de/node?id=1155306) |
| DS-004 | Computer-Based Design Synthesis Research: An Overview | [mediatum.ub.tum.de](http://mediatum.ub.tum.de/node?id=1161039) |
