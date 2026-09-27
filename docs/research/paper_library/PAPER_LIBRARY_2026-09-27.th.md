# คลัง paper ของ Formula Ultimate — 2026-09-27

ต้นฉบับภาษาอังกฤษ: `PAPER_LIBRARY_2026-09-27.md`

คลัง paper ของ Work 145 ที่เกี่ยวข้องกับ Formula Ultimate ทางตรง (วัตถุประสงค์หรือวิธีแบบเดียวกัน) ทางอ้อม (วิธีที่โครงการนำมาใช้ได้) หรือผ่านข้อมูลและผลการค้นพบที่โครงการใช้ได้ ต่อยอดจากแค็ตตาล็อก Work 102 (`../RELATED_WORK_CATALOG_2026-09-05.th.md`, P01-P62) paper เหล่านั้นปรากฏที่นี่พร้อมหมายเลข P

## วิธีอ่านแค็ตตาล็อกนี้

- **ความสัมพันธ์** `ตรง`: วัตถุประสงค์หรือวิธีแบบเดียวกับโครงการ `อ้อม`: วิธี เครื่องมือ หรือข้อโต้แย้งที่โครงการนำมาใช้ได้ `ข้อมูล/ผลที่ใช้ได้`: ข้อมูลวัด ชุดข้อมูล หรือผลเชิงปริมาณที่โครงการใช้ได้
- **ตัวตน** paper จะถูกบันทึกเฉพาะเมื่อยืนยันชื่อเรื่องกับ metadata ของ arXiv, Crossref หรือ Semantic Scholar แล้ว และพบคำในชื่อเรื่องที่คัดสรรบนหน้าแรกของ PDF ตัวระบุที่จำมาถือเป็นเพียงคำใบ้ ไม่ใช่ข้อเท็จจริง
- **สำเนาในเครื่อง** PDF อยู่ใน `papers/<category>/` ซึ่งถูก git-ignore เพราะ paper ส่วนใหญ่ แม้เป็น open access ก็อาจเผยแพร่ซ้ำภายใต้สัญญาอนุญาต CC BY 4.0 ของ repository นี้ไม่ได้ commit เฉพาะ metadata ส่วน SHA-256 ขนาด และ URL ต้นทางของทุกไฟล์อยู่ใน `manifest_v1.json`
- **ไม่มีสำเนาในเครื่อง** บันทึกเป็น `ไม่พบสำเนา open access` (ไม่มีแหล่งใดระบุว่ามีสำเนาฟรี ให้ขอผ่านห้องสมุด), `ดาวน์โหลดไม่สำเร็จ` (มีสำเนาฟรีแต่เซิร์ฟเวอร์ปฏิเสธการดาวน์โหลดด้วยสคริปต์ ส่วนใหญ่เป็นการตรวจ bot แบบ Cloudflare ซึ่งไม่ได้พยายามข้าม) หรือ `ยืนยันตัวตนไม่ได้` paper กลุ่มที่สองแสดงไว้ท้ายเอกสารพร้อมลิงก์ให้เปิดในเบราว์เซอร์ บันทึกไฟล์ไว้ในโฟลเดอร์ใดก็ได้แล้วนำเข้าคลังด้วย `python scripts/research/build_paper_library.py --ingest <folder>` ซึ่งใช้การตรวจชื่อเรื่องแบบเดียวกัน
- **หมายเหตุความเกี่ยวข้อง** เป็นการประเมินจากบทคัดย่อและเนื้อหาที่ทราบ ไม่ใช่ผลจากการอ่านทุก paper เต็มฉบับ และไม่ใช่การอ้างว่าวิธีนั้นใช้ได้กับโครงการนี้ การค้นที่ไม่พบคู่แข่งไม่ใช่หลักฐานของความใหม่

สร้างใหม่ด้วย `python scripts/research/build_paper_library.py --download`

| หมวด | จำนวน | ตรง | อ้อม | ข้อมูล | มี PDF |
| --- | ---: | ---: | ---: | ---: | ---: |
| การค้นพบแบบ open-ended การออกแบบเชิงวิวัฒนาการ และการออกแบบรูปร่างร่วมกับการควบคุม | 43 | 15 | 28 | 0 | 33 |
| LLM และ AI agent สำหรับการออกแบบทางวิศวกรรม โค้ด CAD และการจำลอง | 43 | 15 | 27 | 1 | 43 |
| Quality diversity อัลกอริทึมค้นหา surrogate และ multifidelity | 36 | 12 | 24 | 0 | 31 |
| การแทนค่า การสร้าง และชุดข้อมูลของ CAD, B-rep และการประกอบ | 34 | 4 | 27 | 3 | 30 |
| Topology optimization, meshing, finite element, contact และตัวเลขของการพัง | 24 | 7 | 17 | 0 | 9 |
| โครงสร้างพื้นฐานการจำลอง optimal control และ MDO การเชื่อมโยง และ integrator | 21 | 5 | 16 | 0 | 12 |
| Optimal control เวลาต่อรอบต่ำสุด พลวัตยานยนต์ สนามแข่ง และการ optimize การออกแบบร่วมกับการควบคุม | 32 | 19 | 12 | 1 | 11 |
| การจัดการพลังงานในการแข่ง สถาปัตยกรรม powertrain และแหล่งเก็บพลังงาน | 31 | 15 | 8 | 8 | 15 |
| ยาง แรงเสียดทานของยาง และการระบุพารามิเตอร์ยาง | 17 | 7 | 7 | 3 | 5 |
| อากาศพลศาสตร์ การตรวจสอบ CFD ชุดข้อมูล aero และ neural surrogate | 33 | 7 | 15 | 11 | 22 |
| การจัดการความร้อน การเกิดความร้อน และการออกแบบการระบายความร้อน | 6 | 3 | 3 | 0 | 2 |
| วัสดุ ข้อมูลวัสดุ ตัวยึดและข้อต่อ โครงสร้างรับการชน การผลิต และพิกัดความเผื่อ | 15 | 7 | 4 | 4 | 2 |
| Verification, validation, การสอบเทียบ สถิติ การทำซ้ำได้ และวินัยในการอ้างผล | 32 | 14 | 18 | 0 | 20 |
| การควบคุมการแข่งอัตโนมัติ ผู้ขับที่เรียนรู้ telemetry จริง และกลยุทธ์การแข่ง | 27 | 5 | 19 | 3 | 23 |
| การสังเคราะห์การออกแบบเชิงคำนวณ การแทนค่าเชิงหน้าที่ การสังเคราะห์การประกอบ และการวัดความใหม่ | 17 | 8 | 9 | 0 | 3 |
| **รวม** | **411** | **143** | **234** | **34** | **261** |

ดาวน์โหลดแล้ว: **261** · ไม่พบสำเนา open access: **90** · ยืนยันตัวตนไม่ได้: **0** · ดาวน์โหลดไม่สำเร็จ: **60**

## การค้นพบแบบ open-ended การออกแบบเชิงวิวัฒนาการ และการออกแบบรูปร่างร่วมกับการควบคุม

งานที่ค้นหาโครงสร้างร่างกาย/topology ร่วมกับพฤติกรรม หรือศึกษาว่าอะไรทำให้การค้นหาการออกแบบแบบ open-ended ได้ผล ใกล้กับวัตถุประสงค์การค้นพบของโครงการที่สุด แต่ไม่มีงานใดยืนยันรถแข่งได้

### OE-001 — Evolving Virtual Creatures

Sims · 1994 · Proceedings of the 21st annual conference on Computer graphics and interactive techniques - SIGGRAPH '94 · **ตรง** · แค็ตตาล็อก Work 102 P01

[แหล่ง](https://doi.org/10.1145/192161.192167) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-001_Sims1994_evolving-virtual-creatures.pdf`](../../../papers/01_open_ended_codesign/OE-001_Sims1994_evolving-virtual-creatures.pdf)

ตัวอย่างต้นแบบของการวิวัฒนาการกราฟร่างกายพร้อมตัวควบคุม งาน typed genome และ topology mutation (Works 093-094) สืบทอดแนวคิดนี้

### OE-002 — Automatic design and manufacture of robotic lifeforms

Lipson & Pollack · 2000 · Nature · **ตรง** · แค็ตตาล็อก Work 102 P02

[แหล่ง](https://doi.org/10.1038/35023115) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-002_Lipson2000_automatic-design-and-manufacture-of-robotic-lifefo.pdf`](../../../papers/01_open_ended_codesign/OE-002_Lipson2000_automatic-design-and-manufacture-of-robotic-lifefo.pdf)

ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0

### OE-003 — RoboGrammar: Graph Grammar for Terrain-Optimized Robot Design

Zhao et al. · 2020 · ACM Transactions on Graphics · **ตรง** · แค็ตตาล็อก Work 102 P03

[แหล่ง](https://doi.org/10.1145/3414685.3417831) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://dl.acm.org/doi/pdf/10.1145/3414685.3417831)

graph grammar ร่วมกับการปรับตัวควบคุมรายแบบบนหลายภูมิประเทศ เทียบได้โดยตรงกับ constrained component grammar และสมมติฐาน H3 เรื่องความเฉพาะตามสภาพแวดล้อม

### OE-004 — Evolution Gym: A Large-Scale Benchmark for Evolving Soft Robots

Bhatia et al. · 2021 · Neural Information Processing Systems · **อ้อม** · แค็ตตาล็อก Work 102 P04

[แหล่ง](https://arxiv.org/abs/2201.09863) · [arXiv:2201.09863](https://arxiv.org/abs/2201.09863) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-004_Bhatia2021_evolution-gym-a-large-scale-benchmark-for-evolving.pdf`](../../../papers/01_open_ended_codesign/OE-004_Bhatia2021_evolution-gym-a-large-scale-benchmark-for-evolving.pdf)

benchmark การออกแบบร่วมที่กำหนดงานและงบคำนวณคงที่ ใช้เป็นแบบวินัยการเปรียบเทียบ GRID/RANDOM/EVOLUTION/QD อย่างยุติธรรม

### OE-005 — Neural Graph Evolution: Towards Efficient Automatic Robot Design

Wang et al. · 2019 · International Conference on Learning Representations · **อ้อม** · แค็ตตาล็อก Work 102 P05

[แหล่ง](https://arxiv.org/abs/1906.05370) · [arXiv:1906.05370](https://arxiv.org/abs/1906.05370) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-005_Wang2019_neural-graph-evolution-towards-efficient-automatic.pdf`](../../../papers/01_open_ended_codesign/OE-005_Wang2019_neural-graph-evolution-towards-efficient-automatic.pdf)

นำตัวควบคุมแบบ graph network กลับมาใช้ข้ามการกลายพันธุ์ของรูปร่างเพื่อลดต้นทุนฝึกใหม่ เกี่ยวข้องเมื่อทุก topology ต้องมีผู้ขับที่ปรับแล้วของตัวเอง

### OE-006 — Embodied Intelligence via Learning and Evolution

Gupta et al. · 2021 · Nature Communications · **ตรง** · แค็ตตาล็อก Work 102 P06

[แหล่ง](https://arxiv.org/abs/2102.02202) · [arXiv:2102.02202](https://arxiv.org/abs/2102.02202) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-006_Gupta2021_embodied-intelligence-via-learning-and-evolution.pdf`](../../../papers/01_open_ended_codesign/OE-006_Gupta2021_embodied-intelligence-via-learning-and-evolution.pdf)

แสดงว่าความซับซ้อนของสภาพแวดล้อมกำหนดรูปร่างที่วิวัฒนาการได้ (DERL) เป็นทั้งหลักฐานและวิธีทดสอบ H3 ข้ามสภาพสนามแข่ง

### OE-007 — DiffAqua: A Differentiable Computational Design Pipeline for Soft Underwater Swimmers with Shape Interpolation

Ma et al. · 2021 · ACM Transactions on Graphics · **อ้อม** · แค็ตตาล็อก Work 102 P07

[แหล่ง](https://arxiv.org/abs/2104.00837) · [arXiv:2104.00837](https://arxiv.org/abs/2104.00837) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-007_Ma2021_diffaqua-a-differentiable-computational-design-pip.pdf`](../../../papers/01_open_ended_codesign/OE-007_Ma2021_diffaqua-a-differentiable-computational-design-pip.pdf)

การออกแบบรูปทรงร่วมกับการควบคุมแบบ differentiable เป็นแบบสำหรับการปรับละเอียดด้วย gradient ภายใน topology ที่ผ่านแล้ว ไม่ใช่การเปลี่ยน topology

### OE-008 — Multi-Objective Graph Heuristic Search for Terrestrial Robot Design

Xu et al. · 2021 · IEEE International Conference on Robotics and Automation · **ตรง** · แค็ตตาล็อก Work 102 P09

[แหล่ง](https://arxiv.org/abs/2107.05858) · [arXiv:2107.05858](https://arxiv.org/abs/2107.05858) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-008_Xu2021_multi-objective-graph-heuristic-search-for-terrest.pdf`](../../../papers/01_open_ended_codesign/OE-008_Xu2021_multi-objective-graph-heuristic-search-for-terrest.pdf)

การค้นหาการออกแบบแบบกราฟไม่ต่อเนื่องภายใต้วัตถุประสงค์ที่ขัดกัน เป็นตัวเทียบสำหรับเวลาแข่ง พลังงาน มวล และความน่าเชื่อถือแบบหลายวัตถุประสงค์ (H2)

### OE-009 — Racing a Wheeled Quadruped: Active Load Transfer Mitigation via Model Predictive Control

Eisman et al. · 2026 · arXiv.org · **ตรง** · แค็ตตาล็อก Work 102 P10

[แหล่ง](https://arxiv.org/abs/2606.26313) · [arXiv:2606.26313](https://arxiv.org/abs/2606.26313) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-009_Eisman2026_racing-a-wheeled-quadruped-active-load-transfer-mi.pdf`](../../../papers/01_open_ended_codesign/OE-009_Eisman2026_racing-a-wheeled-quadruped-active-load-transfer-mi.pdf)

การแข่งจริงของสถาปัตยกรรมจุดสัมผัสพื้นที่ไม่ธรรมดา ได้เวลาต่อรอบดีขึ้นจากกลไกขาแบบ active เป็นงานตีพิมพ์ที่ใกล้กับรูปร่างรถแข่งที่ไม่ใช่รถยนต์มากที่สุด

### OE-010 — Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions

Wang et al. · 2019 · arXiv.org · **อ้อม** · แค็ตตาล็อก Work 102 P18

[แหล่ง](https://arxiv.org/abs/1901.01753) · [arXiv:1901.01753](https://arxiv.org/abs/1901.01753) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-010_Wang2019_paired-open-ended-trailblazer-poet-endlessly-gener.pdf`](../../../papers/01_open_ended_codesign/OE-010_Wang2019_paired-open-ended-trailblazer-poet-endlessly-gener.pdf)

วิวัฒนาการสภาพแวดล้อมร่วมกับคำตอบ ใช้ทำสนามแบบ curriculum ได้ โดยสนามประเมินแบบ held-out ต้องคงที่

### OE-011 — Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions

Wang et al. · 2020 · International Conference on Machine Learning · **อ้อม** · แค็ตตาล็อก Work 102 P19

[แหล่ง](https://arxiv.org/abs/2003.08536) · [arXiv:2003.08536](https://arxiv.org/abs/2003.08536) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-011_Wang2020_enhanced-poet-open-ended-reinforcement-learning-th.pdf`](../../../papers/01_open_ended_codesign/OE-011_Wang2020_enhanced-poet-open-ended-reinforcement-learning-th.pdf)

เพิ่มตัววัดความใหม่ที่ไม่ผูกกับโดเมนและการถ่ายโอนระหว่างคู่สภาพแวดล้อม-คำตอบ เกี่ยวข้องกับการวัดความใหม่ของสภาพแวดล้อมอย่างซื่อตรง

### OE-012 — Reality-assisted evolution of soft robots through large-scale physical experimentation: a review

Howison et al. · 2020 · Artificial Life · **อ้อม** · แค็ตตาล็อก Work 102 P20

[แหล่ง](https://arxiv.org/abs/2009.13960) · [arXiv:2009.13960](https://arxiv.org/abs/2009.13960) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-012_Howison2020_reality-assisted-evolution-of-soft-robots-through.pdf`](../../../papers/01_open_ended_codesign/OE-012_Howison2020_reality-assisted-evolution-of-soft-robots-through.pdf)

ทบทวนการนำการทดลองจริงเข้าไปในวงวิวัฒนาการ ให้ข้อมูลกับโปรแกรม physical correlation (Works 131-133)

### OE-013 — Evolving Neural Networks through Augmenting Topologies

Stanley & Miikkulainen · 2002 · Evolutionary Computation · **ตรง**

[แหล่ง](https://doi.org/10.1162/106365602320169811) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-013_Stanley2002_evolving-neural-networks-through-augmenting-topolo.pdf`](../../../papers/01_open_ended_codesign/OE-013_Stanley2002_evolving-neural-networks-through-augmenting-topolo.pdf)

NEAT: historical marking, speciation และการเพิ่มความซับซ้อนสำหรับวิวัฒนาการ topology กราฟ เป็นคำตอบมาตรฐานของการผสมข้าม topology ที่ต่างกัน (Work 094)

### OE-014 — Compositional pattern producing networks: A novel abstraction of development

Stanley · 2007 · Genetic Programming and Evolvable Machines · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s10710-007-9028-8) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การเข้ารหัสเชิงกำเนิด CPPN สำหรับเรขาคณิตที่มีความสม่ำเสมอและสมมาตร เป็นตัวเลือกการแทนค่าสำหรับ spatial material field (Works 108-111)

### OE-015 — Unshackling evolution: evolving soft robots with multiple materials and a powerful generative encoding

Cheney et al. · 2013 · Proceedings of the 15th annual conference on Genetic and evolutionary computation · **อ้อม**

[แหล่ง](https://doi.org/10.1145/2463372.2463404) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ร่างกาย voxel หลายวัสดุที่เข้ารหัสด้วย CPPN ดีกว่าการเข้ารหัสตรง เป็นหลักฐานสนับสนุนการเข้ารหัสเชิงกำเนิดในการค้นหาการกระจายวัสดุ

### OE-016 — Scalable Co-Optimization of Morphology and Control in Embodied Machines

Cheney et al. · 2018 · Journal of the Royal Society Interface · **ตรง**

[แหล่ง](https://arxiv.org/abs/1706.06133) · [arXiv:1706.06133](https://arxiv.org/abs/1706.06133) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-016_Cheney2018_scalable-co-optimization-of-morphology-and-control.pdf`](../../../papers/01_open_ended_codesign/OE-016_Cheney2018_scalable-co-optimization-of-morphology-and-control.pdf)

แสดงว่านวัตกรรมทางรูปร่างถูกทิ้งเพราะตัวควบคุมยังไม่ปรับตาม และเสนอการปกป้อง เป็นรูปแบบความล้มเหลวที่ทราบแล้วของการค้นหาแบบร่วมระหว่างการออกแบบกับผู้ขับ

### OE-017 — Environmental influence on the evolution of morphological complexity in machines

Auerbach & Bongard · 2014 · PLoS Computational Biology · **ตรง**

[แหล่ง](https://doi.org/10.1371/journal.pcbi.1003399) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-017_Auerbach2014_environmental-influence-on-the-evolution-of-morpho.pdf`](../../../papers/01_open_ended_codesign/OE-017_Auerbach2014_environmental-influence-on-the-evolution-of-morpho.pdf)

วัดว่าสภาพแวดล้อมกำหนดความซับซ้อนของรูปร่างที่วิวัฒนาการได้อย่างไร เป็นแหล่งวิธีโดยตรงสำหรับ H3

### OE-018 — Morphological change in machines accelerates the evolution of robust behavior

Bongard · 2011 · Proceedings of the National Academy of Sciences · **อ้อม**

[แหล่ง](https://doi.org/10.1073/pnas.1015390108) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.ncbi.nlm.nih.gov/pmc/articles/3029735)

การเปลี่ยนร่างกายระหว่างวิวัฒนาการเพิ่มความทนทานของพฤติกรรม เกี่ยวข้องกับความทนทานต่อสนามแข่ง held-out (Work 128)

### OE-019 — A scalable pipeline for designing reconfigurable organisms

Kriegman et al. · 2020 · Proceedings of the National Academy of Sciences · **ตรง**

[แหล่ง](https://doi.org/10.1073/pnas.1910837117) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://doi.org/10.1073/pnas.1910837117)

การออกแบบที่วิวัฒนาการได้ถูกกรองความทนทานจากจำลองสู่ของจริงแล้วจึงสร้างและทดสอบ เป็นตัวอย่างจริงของบันไดหลักฐานจาก generated ถึงทดสอบจริง

### OE-020 — Efficient automatic design of robots

Matthews et al. · 2023 · Proceedings of the National Academy of Sciences · **ตรง**

[แหล่ง](https://doi.org/10.1073/pnas.2305180120) · [arXiv:2306.03263](https://arxiv.org/abs/2306.03263) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-020_Matthews2023_efficient-automatic-design-of-robots.pdf`](../../../papers/01_open_ended_codesign/OE-020_Matthews2023_efficient-automatic-design-of-robots.pdf)

การออกแบบทั้งร่างด้วย gradient ได้ภายในไม่กี่วินาทีแล้วสร้างจริง เป็นเกณฑ์ว่าการค้นหา topology เร็วได้แค่ไหนเมื่อมีฟิสิกส์แบบ differentiable

### OE-021 — Reinforcement Learning for Improving Agent Design

Ha · 2019 · Artificial Life · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1810.03779) · [arXiv:1810.03779](https://arxiv.org/abs/1810.03779) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-021_Ha2019_reinforcement-learning-for-improving-agent-design.pdf`](../../../papers/01_open_ended_codesign/OE-021_Ha2019_reinforcement-learning-for-improving-agent-design.pdf)

เรียนรู้พารามิเตอร์ร่างกายร่วมกับ policy และแสดงว่าตัว optimizer ใช้ความอิสระของร่างกายแบบไม่คาดคิด เป็นคำเตือนสำหรับการตรวจวัตถุประสงค์ของเรา

### OE-022 — Jointly Learning to Construct and Control Agents using Deep Reinforcement Learning

Schaff et al. · 2019 · IEEE International Conference on Robotics and Automation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1801.01432) · [arXiv:1801.01432](https://arxiv.org/abs/1801.01432) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-022_Schaff2019_jointly-learning-to-construct-and-control-agents-u.pdf`](../../../papers/01_open_ended_codesign/OE-022_Schaff2019_jointly-learning-to-construct-and-control-agents-u.pdf)

policy ที่ขึ้นกับการออกแบบใช้ร่วมกันทั้งการกระจายของแบบ เป็นวิธีเฉลี่ยต้นทุนการปรับผู้ขับข้ามรถหลายแบบ

### OE-023 — Data-efficient Co-Adaptation of Morphology and Behaviour with Deep Reinforcement Learning

Luck et al. · 2019 · Conference on Robot Learning · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1911.06832) · [arXiv:1911.06832](https://arxiv.org/abs/1911.06832) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-023_Luck2019_data-efficient-co-adaptation-of-morphology-and-beh.pdf`](../../../papers/01_open_ended_codesign/OE-023_Luck2019_data-efficient-co-adaptation-of-morphology-and-beh.pdf)

ใช้ value function ที่เรียนรู้ประเมินแบบใหม่โดยไม่ต้องรันเต็ม เกี่ยวข้องกับการคัดกรองราคาถูกก่อนการแข่ง Level-0

### OE-024 — Transform2Act: Learning a Transform-and-Control Policy for Efficient Agent Design

Yuan et al. · 2022 · International Conference on Learning Representations · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2110.03659) · [arXiv:2110.03659](https://arxiv.org/abs/2110.03659) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-024_Yuan2022_transform2act-learning-a-transform-and-control-pol.pdf`](../../../papers/01_open_ended_codesign/OE-024_Yuan2022_transform2act-learning-a-transform-and-control-pol.pdf)

policy ที่แก้กราฟร่างกายก่อนแล้วจึงควบคุม เป็นทางเลือกแทนการกลายพันธุ์ topology เชิงวิวัฒนาการที่ควรเทียบที่งบเท่ากัน

### OE-025 — An End-to-End Differentiable Framework for Contact-Aware Robot Design

Xu et al. · 2021 · Robotics: Science and Systems Conference · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2107.07501) · [arXiv:2107.07501](https://arxiv.org/abs/2107.07501) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-025_Xu2021_an-end-to-end-differentiable-framework-for-contact.pdf`](../../../papers/01_open_ended_codesign/OE-025_Xu2021_an-end-to-end-differentiable-framework-for-contact.pdf)

การออกแบบที่คำนึงถึงการสัมผัสแบบ differentiable ด้วย cage deformation เกี่ยวข้องกับ ground interaction และเรขาคณิตที่ขับด้วยการสัมผัส

### OE-026 — SoftZoo: A Soft Robot Co-design Benchmark For Locomotion In Diverse Environments

Wang et al. · 2023 · International Conference on Learning Representations · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2303.09555) · [arXiv:2303.09555](https://arxiv.org/abs/2303.09555) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-026_Wang2023_softzoo-a-soft-robot-co-design-benchmark-for-locom.pdf`](../../../papers/01_open_ended_codesign/OE-026_Wang2023_softzoo-a-soft-robot-co-design-benchmark-for-locom.pdf)

benchmark การออกแบบร่วมข้ามหลายสภาพแวดล้อม เป็นแบบการรันการค้นหาเดียวข้ามหลายสภาพสนามแล้วเทียบความเฉพาะ

### OE-027 — Evolution and learning in differentiable robots

Strgar et al. · 2024 · Robotics: Science and Systems Conference · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2405.14712) · [arXiv:2405.14712](https://arxiv.org/abs/2405.14712) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-027_Strgar2024_evolution-and-learning-in-differentiable-robots.pdf`](../../../papers/01_open_ended_codesign/OE-027_Strgar2024_evolution-and-learning-in-differentiable-robots.pdf)

รวมวิวัฒนาการร่างกายกับการเรียนรู้ตัวควบคุมด้วย gradient ในสเกลใหญ่ ให้ข้อมูลเรื่องการแบ่งการค้นหาไม่ต่อเนื่องกับการปรับละเอียดต่อเนื่อง

### OE-028 — Co-optimising Robot Morphology and Controller in a Simulated Open-Ended Environment

Stensby et al. · 2021 · EvoApplications · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2104.03062) · [arXiv:2104.03062](https://arxiv.org/abs/2104.03062) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-028_Stensby2021_co-optimising-robot-morphology-and-controller-in-a.pdf`](../../../papers/01_open_ended_codesign/OE-028_Stensby2021_co-optimising-robot-morphology-and-controller-in-a.pdf)

การปรับรูปร่างและตัวควบคุมร่วมกันภายใต้สภาพแวดล้อมแบบ POET แสดงปฏิสัมพันธ์ระหว่างการสร้างสภาพแวดล้อมกับการค้นหาร่างกาย

### OE-029 — An Empirical Study on the Computation Budget of Co-Optimization of Robot Design and Control in Simulation

Arza et al. · 2024 · arXiv · **ตรง**

[แหล่ง](https://arxiv.org/abs/2409.08621) · [arXiv:2409.08621](https://arxiv.org/abs/2409.08621) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-029_Arza2024_an-empirical-study-on-the-computation-budget-of-co.pdf`](../../../papers/01_open_ended_codesign/OE-029_Arza2024_an-empirical-study-on-the-computation-budget-of-co.pdf)

วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ

### OE-030 — Convergent Functions, Divergent Forms

Jeon et al. · 2025 · Neural Information Processing Systems · **ตรง**

[แหล่ง](https://arxiv.org/abs/2505.21665) · [arXiv:2505.21665](https://arxiv.org/abs/2505.21665) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-030_Jeon2025_convergent-functions-divergent-forms.pdf`](../../../papers/01_open_ended_codesign/OE-030_Jeon2025_convergent-functions-divergent-forms.pdf)

ศึกษาว่ารูปทรงต่างกันไปถึงหน้าที่เดียวกันได้อย่างไรในการค้นหารูปร่าง เกี่ยวข้องกับการแยกความใหม่ทางรูปลักษณ์ออกจากความใหม่ทางหน้าที่

### OE-031 — Embodied Co-Design for Rapidly Evolving Agents

Wang et al. · 2025 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2512.04770) · [arXiv:2512.04770](https://arxiv.org/abs/2512.04770) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-031_Wang2025_embodied-co-design-for-rapidly-evolving-agents.pdf`](../../../papers/01_open_ended_codesign/OE-031_Wang2025_embodied-co-design-for-rapidly-evolving-agents.pdf)

survey ล่าสุดของการออกแบบรูปร่างร่วมกับการควบคุม ตั้งแต่สิ่งมีชีวิตเสมือนถึงหุ่นยนต์จริง เป็นแผนที่วิธีและปัญหาที่ยังเปิดอยู่

### OE-032 — Shaping the Evolutionary Dynamics of Robot Morphology via Adaptive Control Learning

Song et al. · 2026 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2608.23100) · [arXiv:2608.23100](https://arxiv.org/abs/2608.23100) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-032_Song2026_shaping-the-evolutionary-dynamics-of-robot-morphol.pdf`](../../../papers/01_open_ended_codesign/OE-032_Song2026_shaping-the-evolutionary-dynamics-of-robot-morphol.pdf)

ความเร็วการเรียนรู้ของตัวควบคุมกำหนดว่ารูปร่างใดอยู่รอด เกี่ยวข้องกับ bias จากการจัดสรรตัวควบคุมในการค้นหาของเรา

### OE-033 — Shape Your Body: Value Gradients for Multi-Embodiment Robot Design

Bohlinger & Peters · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2606.00702) · [arXiv:2606.00702](https://arxiv.org/abs/2606.00702) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-033_Bohlinger2026_shape-your-body-value-gradients-for-multi-embodime.pdf`](../../../papers/01_open_ended_codesign/OE-033_Bohlinger2026_shape-your-body-value-gradients-for-multi-embodime.pdf)

ใช้ gradient ของ value จาก policy หลายร่างเพื่อปรับการออกแบบร่างกาย เป็นตัวเทียบฝั่งการออกแบบต่อเนื่อง

### OE-034 — Seeking Quality Diversity in Evolutionary Co-design of Morphology and Control of Soft Tensegrity Modular Robots

Zardini et al. · 2021 · Annual Conference on Genetic and Evolutionary Computation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2104.12175) · [arXiv:2104.12175](https://arxiv.org/abs/2104.12175) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-034_Zardini2021_seeking-quality-diversity-in-evolutionary-co-desig.pdf`](../../../papers/01_open_ended_codesign/OE-034_Zardini2021_seeking-quality-diversity-in-evolutionary-co-desig.pdf)

quality diversity กับการออกแบบรูปร่าง/การควบคุมร่วม เป็นตัวอย่างก่อนหน้าของ executable morphology archive (Work 099)

### OE-035 — Open-Endedness is Essential for Artificial Superhuman Intelligence

Hughes et al. · 2024 · International Conference on Machine Learning · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2406.04268) · [arXiv:2406.04268](https://arxiv.org/abs/2406.04268) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-035_Hughes2024_open-endedness-is-essential-for-artificial-superhu.pdf`](../../../papers/01_open_ended_codesign/OE-035_Hughes2024_open-endedness-is-essential-for-artificial-superhu.pdf)

นิยาม open-endedness ว่าเป็นความใหม่บวกกับความเรียนรู้ได้สำหรับผู้สังเกต เป็นนิยามที่ใช้ได้สำหรับความหมายของ claim การค้นพบของเรา

### OE-036 — Why Open-Endedness Matters

Stanley · 2019 · Artificial Life · **อ้อม**

[แหล่ง](https://doi.org/10.1162/artl_a_00294) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

อธิบายว่าทำไมการค้นหาแบบ open-ended สำคัญเกินกว่าการ optimize เป็นบริบทของกรอบใน research charter

### OE-037 — Minimal Criterion Coevolution: A New Approach to Open-Ended Search

Brant & Stanley · 2017 · Proceedings of the Genetic and Evolutionary Computation Conference · **อ้อม**

[แหล่ง](https://doi.org/10.1145/3071178.3071186) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แทนวัตถุประสงค์ด้วยเกณฑ์ขั้นต่ำของการอยู่รอด คล้ายกับ feasibility gate ที่เป็นแรงคัดเลือกเพียงอย่างเดียว

### OE-038 — Design Mining Interacting Wind Turbines

Preen & Bull · 2016 · Evolutionary Computation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1410.0547) · [arXiv:1410.0547](https://arxiv.org/abs/1410.0547) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-038_Preen2016_design-mining-interacting-wind-turbines.pdf`](../../../papers/01_open_ended_codesign/OE-038_Preen2016_design-mining-interacting-wind-turbines.pdf)

วิวัฒนาการแบบที่ประเมินด้วยการพิมพ์ 3 มิติและอุโมงค์ลมร่วมกับ surrogate เป็นตัวอย่างการประเมินทางกายภาพในวง

### OE-039 — Keep Rollin' - Whole-Body Motion Control and Planning for Wheeled Quadrupedal Robots

Bjelonic et al. · 2019 · IEEE Robotics and Automation Letters · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1809.03557) · [arXiv:1809.03557](https://arxiv.org/abs/1809.03557) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-039_Bjelonic2019_keep-rollin-whole-body-motion-control-and-planning.pdf`](../../../papers/01_open_ended_codesign/OE-039_Bjelonic2019_keep-rollin-whole-body-motion-control-and-planning.pdf)

การควบคุมการเคลื่อนที่แบบล้อ-ขาผสม แสดงว่าจุดสัมผัสพื้นแบบไม่ธรรมดาต้องการอะไรจากการควบคุม

### OE-040 — Automated Antenna Design with Evolutionary Algorithms

Hornby et al. · 2006 · Space 2006 · **ตรง**

[แหล่ง](https://doi.org/10.2514/6.2006-7242) · มี PDF ในเครื่อง: [`papers/01_open_ended_codesign/OE-040_Hornby2006_automated-antenna-design-with-evolutionary-algorit.pdf`](../../../papers/01_open_ended_codesign/OE-040_Hornby2006_automated-antenna-design-with-evolutionary-algorit.pdf)

เสาอากาศ ST5 ของ NASA ที่ได้จากวิวัฒนาการและขึ้นบินจริง เป็นกรณีหายากที่การออกแบบฮาร์ดแวร์แปลกตาผ่านการรับรองจริง

### OE-041 — Toward a unified and automated design methodology for multi-domain dynamic systems using bond graphs and genetic programming

Seo et al. · 2003 · Mechatronics · **ตรง**

[แหล่ง](https://doi.org/10.1016/s0957-4158(03)00006-0) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

วิวัฒนาการ topology และพารามิเตอร์ของ bond graph ระบบหลายโดเมน เป็นงานก่อนหน้าที่ใกล้กับการค้นหา powertrain แบบ typed energy graph ของเรามากที่สุด

### OE-042 — Automated design of both the topology and sizing of analog electrical circuits using genetic programming

Koza et al. · 1996 · Artificial Intelligence in Design ’96 · **อ้อม**

[แหล่ง](https://doi.org/10.1007/978-94-009-0279-4_9) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

genetic programming ค้นพบ topology ของวงจรพร้อมค่าชิ้นส่วน เป็นผลคลาสสิกของการค้นพบ topology พร้อมขนาด

### OE-043 — Evolving three-dimensional objects with a generative encoding inspired by developmental biology

— · 2011 · ECAL 2011: The 11th European Conference on Artificial Life · **อ้อม**

[แหล่ง](https://doi.org/10.7551/978-0-262-29714-1-ch024) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://doi.org/10.7551/978-0-262-29714-1-ch024)

การเข้ารหัสเชิงกำเนิดที่สร้างวัตถุ 3 มิติที่พิมพ์ได้ เกี่ยวข้องกับ freeform solid grammar (Work 092)


## LLM และ AI agent สำหรับการออกแบบทางวิศวกรรม โค้ด CAD และการจำลอง

agent และแบบจำลองเชิงกำเนิดที่เสนอการออกแบบทางวิศวกรรม เขียนโปรแกรม CAD หรือสั่ง solver รวมถึงงานเรื่องการประเมินระบบเหล่านี้ เกี่ยวข้องเพราะผู้ออกแบบของ Formula Ultimate เป็น agent ที่เขียน CadQuery และถูกตัดสินโดยตัวประเมินอิสระ

### AG-001 — Evolution through Large Models

Lehman et al. · 2022 · arXiv · **ตรง**

[แหล่ง](https://arxiv.org/abs/2206.08896) · [arXiv:2206.08896](https://arxiv.org/abs/2206.08896) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-001_Lehman2022_evolution-through-large-models.pdf`](../../../papers/02_ai_agents_engineering/AG-001_Lehman2022_evolution-through-large-models.pdf)

LLM เป็นตัวกลายพันธุ์ภายใน MAP-Elites สร้างรูปร่าง Sodarace ที่เคลื่อนที่ได้ในรูปโค้ด เป็นแม่แบบที่ใกล้ที่สุดของ LLM ที่กลายพันธุ์โปรแกรม CadQuery ของรถ

### AG-002 — Mathematical discoveries from program search with large language models

Romera-Paredes et al. · 2024 · Nature · **ตรง**

[แหล่ง](https://doi.org/10.1038/s41586-023-06924-6) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-002_Paredes2024_mathematical-discoveries-from-program-search-with.pdf`](../../../papers/02_ai_agents_engineering/AG-002_Paredes2024_mathematical-discoveries-from-program-search-with.pdf)

FunSearch จับคู่ LLM ผู้เสนอกับตัวประเมินอัตโนมัติที่เชื่อถือได้ การแยกการสร้างออกจากการประเมินตรงกับกฎตัวประเมินอิสระของเรา

### AG-003 — AlphaEvolve: A coding agent for scientific and algorithmic discovery

Novikov et al. · 2025 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2506.13131) · [arXiv:2506.13131](https://arxiv.org/abs/2506.13131) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-003_Novikov2025_alphaevolve-a-coding-agent-for-scientific-and-algo.pdf`](../../../papers/02_ai_agents_engineering/AG-003_Novikov2025_alphaevolve-a-coding-agent-for-scientific-and-algo.pdf)

coding agent เชิงวิวัฒนาการที่มีฐานข้อมูลโปรแกรมแบบ MAP-Elites และคะแนนที่เครื่องตรวจได้ รวมถึงผลด้านวงจรฮาร์ดแวร์ เป็นสถาปัตยกรรมอ้างอิงของ design agent ของเรา

### AG-004 — Evolution or Illusion? Rethinking Evaluation in LLM Evolutionary Search

Oved et al. · 2026 · arXiv · **ตรง**

[แหล่ง](https://arxiv.org/abs/2609.19799) · [arXiv:2609.19799](https://arxiv.org/abs/2609.19799) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-004_Oved2026_evolution-or-illusion-rethinking-evaluation-in-llm.pdf`](../../../papers/02_ai_agents_engineering/AG-004_Oved2026_evolution-or-illusion-rethinking-evaluation-in-llm.pdf)

ตั้งคำถามว่าผลดีที่รายงานของการค้นหาเชิงวิวัฒนาการด้วย LLM ยังอยู่หรือไม่เมื่อใช้ baseline และงบที่ยุติธรรม สนับสนุนกฎการพยายามหักล้างและการจับคู่งบของเราโดยตรง

### AG-005 — The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery

Lu et al. · 2024 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2408.06292) · [arXiv:2408.06292](https://arxiv.org/abs/2408.06292) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-005_Lu2024_the-ai-scientist-towards-fully-automated-open-ende.pdf`](../../../papers/02_ai_agents_engineering/AG-005_Lu2024_the-ai-scientist-towards-fully-automated-open-ende.pdf)

วงจรวิจัยอัตโนมัติครบวง มีประโยชน์หลักจากรูปแบบความล้มเหลวที่บันทึกไว้ (อ้างเกินจริง การรีวิวอ่อน) ซึ่งระดับหลักฐานของเราออกแบบมาเพื่อกันไว้

### AG-006 — How Can Large Language Models Help Humans in Design and Manufacturing?

Makatura et al. · 2023 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2307.14377) · [arXiv:2307.14377](https://arxiv.org/abs/2307.14377) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-006_Makatura2023_how-can-large-language-models-help-humans-in-desig.pdf`](../../../papers/02_ai_agents_engineering/AG-006_Makatura2023_how-can-large-language-models-help-humans-in-desig.pdf)

ทดสอบ LLM อย่างเป็นระบบตั้งแต่สร้าง CAD ประเมินสมรรถนะ optimize จนถึงการผลิต แสดงว่าแบบจำลองภาษาล้มเหลวตรงไหนในเรขาคณิตและฟิสิกส์

### AG-007 — Large Language Model Agent as a Mechanical Designer

Jadhav & Farimani · 2024 · Journal of engineering design · **ตรง**

[แหล่ง](https://arxiv.org/abs/2404.17525) · [arXiv:2404.17525](https://arxiv.org/abs/2404.17525) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-007_Jadhav2024_large-language-model-agent-as-a-mechanical-designe.pdf`](../../../papers/02_ai_agents_engineering/AG-007_Jadhav2024_large-language-model-agent-as-a-mechanical-designe.pdf)

LLM agent ปรับแบบโครงถักด้วยผลจาก FEM และเทียบกับ NSGA-II ที่จำนวนการประเมินเท่ากัน เป็นทั้งวิธีและตัวเทียบความยุติธรรมโดยตรง

### AG-008 — An LLM-enabled Multi-Agent Autonomous Mechatronics Design Framework

Wang et al. · 2025 · 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW) · **ตรง**

[แหล่ง](https://arxiv.org/abs/2504.14681) · [arXiv:2504.14681](https://arxiv.org/abs/2504.14681) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-008_Wang2025_an-llm-enabled-multi-agent-autonomous-mechatronics.pdf`](../../../papers/02_ai_agents_engineering/AG-008_Wang2025_an-llm-enabled-multi-agent-autonomous-mechatronics.pdf)

การออกแบบต้นแบบแมคคาทรอนิกส์จริงด้วยหลาย agent ข้ามโดเมนกล อิเล็กทรอนิกส์ และซอฟต์แวร์ เทียบได้กับไปป์ไลน์ part-to-vehicle หลายโดเมนของเรา

### AG-009 — Physics-in-the-Loop: A Hybrid Agentic Architecture for Validated CAD Engineering Design

Berger et al. · 2026 · Proceedings of the Thirty-Fifth International Joint Conference on Artificial Intelligence · **ตรง**

[แหล่ง](https://arxiv.org/abs/2605.19717) · [arXiv:2605.19717](https://arxiv.org/abs/2605.19717) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-009_Berger2026_physics-in-the-loop-a-hybrid-agentic-architecture.pdf`](../../../papers/02_ai_agents_engineering/AG-009_Berger2026_physics-in-the-loop-a-hybrid-agentic-architecture.pdf)

CAD agent แบบสร้าง-จำลอง-ปรับ ที่ใช้เครื่องมือฟิสิกส์ที่ตรวจสอบแล้วในวงแทนการดูภาพ เป็นรูปแบบเดียวกับวง CadQuery สู่ตัวประเมินของเรา

### AG-010 — Engineering.ai: A Platform for Teams of AI Engineers in Computational Design

Xu et al. · 2025 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2511.00122) · [arXiv:2511.00122](https://arxiv.org/abs/2511.00122) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-010_Xu2025_engineering-ai-a-platform-for-teams-of-ai-engineer.pdf`](../../../papers/02_ai_agents_engineering/AG-010_Xu2025_engineering-ai-a-platform-for-teams-of-ai-engineer.pdf)

LLM agent ที่รัน CAD, meshing, การจำลองหลายสาขา และ optimization ในวงปิด เป็นระบบที่เทียบกันได้สำหรับทำ benchmark

### AG-011 — Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback

Son et al. · 2026 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2605.17448) · [arXiv:2605.17448](https://arxiv.org/abs/2605.17448) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-011_Son2026_self-improving-cad-generation-agents-with-finite-e.pdf`](../../../papers/02_ai_agents_engineering/AG-011_Son2026_self-improving-cad-generation-agents-with-finite-e.pdf)

ใช้ผล FEA เป็นสัญญาณป้อนกลับให้ agent ที่เขียน CAD เกี่ยวข้องโดยตรงกับ geometry-structural coupling (Works 082, 138)

### AG-012 — FEABench: Evaluating Language Models on Multiphysics Reasoning Ability

Mudur et al. · 2025 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2504.06260) · [arXiv:2504.06260](https://arxiv.org/abs/2504.06260) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-012_Mudur2025_feabench-evaluating-language-models-on-multiphysic.pdf`](../../../papers/02_ai_agents_engineering/AG-012_Mudur2025_feabench-evaluating-language-models-on-multiphysic.pdf)

benchmark ของ LLM agent ที่ใช้โปรแกรม finite element ตั้งแต่ต้นจนจบ เป็นมาตรวัดว่าเชื่อ agent ในการตั้งค่า solver ได้แค่ไหน

### AG-013 — FEM-Bench: A Structured Scientific Reasoning Benchmark

Mohammadzadeh et al. · 2025 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2512.20732) · [arXiv:2512.20732](https://arxiv.org/abs/2512.20732) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-013_Mohammadzadeh2025_fem-bench-a-structured-scientific-reasoning-benchm.pdf`](../../../papers/02_ai_agents_engineering/AG-013_Mohammadzadeh2025_fem-bench-a-structured-scientific-reasoning-benchm.pdf)

งานเขียนโค้ด FEM ระดับบัณฑิตศึกษาพร้อมการตรวจอัตโนมัติ ใช้ทดสอบ agent ที่เขียนโค้ด element หรือ solver ของเรา

### AG-014 — What Do CAE Simulation Agents Really Need Beyond a Generic Harness?

Shi & Zhang · 2026 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2609.03718) · [arXiv:2609.03718](https://arxiv.org/abs/2609.03718) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-014_Shi2026_what-do-cae-simulation-agents-really-need-beyond-a.pdf`](../../../papers/02_ai_agents_engineering/AG-014_Shi2026_what-do-cae-simulation-agents-really-need-beyond-a.pdf)

วิเคราะห์ว่า CAE agent ต้องการเครื่องมืออะไรนอกเหนือจาก harness เขียนโค้ดทั่วไป ให้ข้อมูลการออกแบบ interface เครื่องมือ CAD/solver

### AG-015 — VFEAgent: A Multimodal Agent Framework for End-to-End Automated Finite Element Analysis

Zhang et al. · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2605.28978) · [arXiv:2605.28978](https://arxiv.org/abs/2605.28978) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-015_Zhang2026_vfeagent-a-multimodal-agent-framework-for-end-to-e.pdf`](../../../papers/02_ai_agents_engineering/AG-015_Zhang2026_vfeagent-a-multimodal-agent-framework-for-end-to-e.pdf)

agent ที่ใช้ภาพช่วยตั้งค่า FEA พร้อม benchmark ที่ผู้เชี่ยวชาญให้คะแนนรวมถึง topology optimization เป็นตัวเทียบของการประเมินโครงสร้างอัตโนมัติ

### AG-016 — MechAgents: Large language model multi-agent collaborations can solve mechanics problems, generate new data, and integrate knowledge

Ni & Buehler · 2024 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2311.08166) · [arXiv:2311.08166](https://arxiv.org/abs/2311.08166) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-016_Ni2024_mechagents-large-language-model-multi-agent-collab.pdf`](../../../papers/02_ai_agents_engineering/AG-016_Ni2024_mechagents-large-language-model-multi-agent-collab.pdf)

LLM หลาย agent เขียนและตรวจโค้ด elasticity บน FEniCS แสดงประโยชน์และข้อจำกัดของการแก้ไขตัวเอง

### AG-017 — Large Language and Text-to-3D Models for Engineering Design Optimization

Rios et al. · 2023 · IEEE Symposium Series on Computational Intelligence · **ตรง**

[แหล่ง](https://arxiv.org/abs/2307.01230) · [arXiv:2307.01230](https://arxiv.org/abs/2307.01230) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-017_Rios2023_large-language-and-text-to-3d-models-for-engineeri.pdf`](../../../papers/02_ai_agents_engineering/AG-017_Rios2023_large-language-and-text-to-3d-models-for-engineeri.pdf)

รูปทรงรถจาก text-to-3D ที่ optimize แรงต้านจาก CFD ในวงวิวัฒนาการ เกี่ยวข้องโดยตรงกับการสร้างตัวถังที่ให้คะแนนด้วยอากาศพลศาสตร์

### AG-018 — Drag-guided diffusion models for vehicle image generation

Aréchiga et al. · 2023 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2306.09935) · [arXiv:2306.09935](https://arxiv.org/abs/2306.09935) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-018_Arechiga2023_drag-guided-diffusion-models-for-vehicle-image-gen.pdf`](../../../papers/02_ai_agents_engineering/AG-018_Arechiga2023_drag-guided-diffusion-models-for-vehicle-image-gen.pdf)

นำทางแบบจำลองเชิงกำเนิดด้วย surrogate ของแรงต้าน แสดงความเสี่ยงที่การนำทางด้วย surrogate จะให้รางวัลกับความผิดพลาดของ surrogate

### AG-019 — Text-to-CadQuery: A New Paradigm for CAD Generation with Scalable Large Model Capabilities

Xie & Ju · 2025 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2505.06507) · [arXiv:2505.06507](https://arxiv.org/abs/2505.06507) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-019_Xie2025_text-to-cadquery-a-new-paradigm-for-cad-generation.pdf`](../../../papers/02_ai_agents_engineering/AG-019_Xie2025_text-to-cadquery-a-new-paradigm-for-cad-generation.pdf)

ฝึก LLM ให้เขียน CadQuery โดยตรง เป็นภาษา CAD เดียวกับที่ agent ของเราเขียน มีชุดข้อมูลและสถิติข้อผิดพลาดที่นำมาใช้ได้

### AG-020 — CAD-Recode: Reverse Engineering CAD Code from Point Clouds

Rukhovich et al. · 2024 · IEEE International Conference on Computer Vision · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2412.14042) · [arXiv:2412.14042](https://arxiv.org/abs/2412.14042) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-020_Rukhovich2024_cad-recode-reverse-engineering-cad-code-from-point.pdf`](../../../papers/02_ai_agents_engineering/AG-020_Rukhovich2024_cad-recode-reverse-engineering-cad-code-from-point.pdf)

กู้โปรแกรม CadQuery จาก point cloud พร้อมคลัง CadQuery สังเคราะห์ขนาดใหญ่ เป็นข้อมูลที่ใช้ได้และเป็นการตรวจจากเรขาคณิตกลับเป็นโค้ด

### AG-021 — Generating CAD Code with Vision-Language Models for 3D Designs

Alrashedy et al. · 2024 · International Conference on Learning Representations · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2410.05340) · [arXiv:2410.05340](https://arxiv.org/abs/2410.05340) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-021_Alrashedy2024_generating-cad-code-with-vision-language-models-fo.pdf`](../../../papers/02_ai_agents_engineering/AG-021_Alrashedy2024_generating-cad-code-with-vision-language-models-fo.pdf)

CADCodeVerify: แบบจำลองเรนเดอร์ผล CAD ของตัวเองแล้วตรวจเอง เป็นการตรวจเบื้องต้นราคาถูกก่อน geometry witness อิสระของเรา

### AG-022 — CADDesigner: Conceptual CAD Model Generation with a General-Purpose Agent

Fan et al. · 2025 · Comput. Aided Des. · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2508.01031) · [arXiv:2508.01031](https://arxiv.org/abs/2508.01031) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-022_Fan2025_caddesigner-conceptual-cad-model-generation-with-a.pdf`](../../../papers/02_ai_agents_engineering/AG-022_Fan2025_caddesigner-conceptual-cad-model-generation-with-a.pdf)

agent อเนกประสงค์ที่ให้ข้อวินิจฉัยเป็นโครงสร้างเมื่อสคริปต์ CAD ล้มเหลว เกี่ยวข้องกับการแปลงข้อผิดพลาดของ kernel เป็นข้อมูลป้อนกลับที่ซ่อมได้

### AG-023 — Towards High-Fidelity CAD Generation via LLM-Driven Program Generation and Text-Based B-Rep Primitive Grounding

Li et al. · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2603.11831) · [arXiv:2603.11831](https://arxiv.org/abs/2603.11831) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-023_Li2026_towards-high-fidelity-cad-generation-via-llm-drive.pdf`](../../../papers/02_ai_agents_engineering/AG-023_Li2026_towards-high-fidelity-cad-generation-via-llm-drive.pdf)

FutureCAD: LLM เขียน CadQuery และผูกการอ้างอิงเข้ากับ primitive ของ B-rep แก้ปัญหาการเลือก face/edge ที่เปราะบางใน CAD ที่สร้างขึ้น

### AG-024 — Clarify Before You Draw: Proactive Agents for Robust Text-to-CAD Generation

Yuan et al. · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2602.03045) · [arXiv:2602.03045](https://arxiv.org/abs/2602.03045) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-024_Yuan2026_clarify-before-you-draw-proactive-agents-for-robus.pdf`](../../../papers/02_ai_agents_engineering/AG-024_Yuan2026_clarify-before-you-draw-proactive-agents-for-robus.pdf)

agent ที่ถามให้ชัดก่อนวาดเมื่อคำขอ CAD ไม่ครบ เกี่ยวข้องกับข้อกำหนด interface แบบมีชนิดสำหรับชิ้นส่วนที่สร้าง

### AG-025 — Test-Time Scaling for CAD Generation via Verifier-Free Consensus Selection

Haag et al. · 2026 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2608.09706) · [arXiv:2608.09706](https://arxiv.org/abs/2608.09706) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-025_Haag2026_test-time-scaling-for-cad-generation-via-verifier.pdf`](../../../papers/02_ai_agents_engineering/AG-025_Haag2026_test-time-scaling-for-cad-generation-via-verifier.pdf)

เลือกโปรแกรม CAD จากหลายตัวอย่างด้วยฉันทามติ เป็นตัวกรองราคาถูก แต่ฉันทามติไม่ใช่การตรวจทางฟิสิกส์

### AG-026 — CADEngBench: It Looks Like CAD, but Does It Work? Evaluating Parametric Design, Assembly Reasoning, and Physics Simulation

Singh et al. · 2026 · arXiv · **ตรง**

[แหล่ง](https://arxiv.org/abs/2608.09296) · [arXiv:2608.09296](https://arxiv.org/abs/2608.09296) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-026_Singh2026_cadengbench-it-looks-like-cad-but-does-it-work-eva.pdf`](../../../papers/02_ai_agents_engineering/AG-026_Singh2026_cadengbench-it-looks-like-cad-but-does-it-work-eva.pdf)

benchmark ที่ให้คะแนน CAD ที่สร้างจากการประกอบและฟิสิกส์ ไม่ใช่รูปลักษณ์ เป็นหลักการเดียวกับกฎเรขาคณิตเป็น input เชิงเหตุของเรา

### AG-027 — Automated Design Optimization via Strategic Search with Large Language Models

Carreon et al. · 2025 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2511.22651) · [arXiv:2511.22651](https://arxiv.org/abs/2511.22651) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-027_Carreon2025_automated-design-optimization-via-strategic-search.pdf`](../../../papers/02_ai_agents_engineering/AG-027_Carreon2025_automated-design-optimization-via-strategic-search.pdf)

การค้นหาเชิงกลยุทธ์ที่นำโดย LLM สำหรับ optimize การออกแบบ เป็นตัวเทียบของการเสนอค่าพารามิเตอร์โดย LLM

### AG-028 — Generative Reliability-Based Design Optimization Using In-Context Learning Capabilities of Large Language Models

Jiang et al. · 2025 · Journal of Mechanical Design · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2503.22401) · [arXiv:2503.22401](https://arxiv.org/abs/2503.22401) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-028_Jiang2025_generative-reliability-based-design-optimization-u.pdf`](../../../papers/02_ai_agents_engineering/AG-028_Jiang2025_generative-reliability-based-design-optimization-u.pdf)

การสร้างแบบด้วย in-context learning ของ LLM ภายใต้ข้อจำกัดความน่าเชื่อถือ เกี่ยวข้องกับ gate ที่คำนึงถึงความไม่แน่นอน

### AG-029 — From Concept to Manufacturing: Evaluating Vision-Language Models for Engineering Design

Picard et al. · 2023 · Artificial Intelligence Review · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2311.12668) · [arXiv:2311.12668](https://arxiv.org/abs/2311.12668) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-029_Picard2023_from-concept-to-manufacturing-evaluating-vision-la.pdf`](../../../papers/02_ai_agents_engineering/AG-029_Picard2023_from-concept-to-manufacturing-evaluating-vision-la.pdf)

ประเมิน vision-language model อย่างกว้างในงานออกแบบวิศวกรรม บันทึกว่าตรงไหนเชื่อไม่ได้

### AG-030 — Deep Generative Models in Engineering Design: A Review

Regenwetter et al. · 2022 · Journal of Mechanical Design · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2110.10863) · [arXiv:2110.10863](https://arxiv.org/abs/2110.10863) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-030_Regenwetter2022_deep-generative-models-in-engineering-design-a-rev.pdf`](../../../papers/02_ai_agents_engineering/AG-030_Regenwetter2022_deep-generative-models-in-engineering-design-a-rev.pdf)

ทบทวนแบบจำลองเชิงกำเนิดในการออกแบบวิศวกรรม รวมถึงช่องว่างด้านความถูกต้องและสมรรถนะ เป็นแผนที่วิธีสำหรับการเสนอเรขาคณิต

### AG-031 — Beyond Statistical Similarity: Rethinking Metrics for Deep Generative Models in Engineering Design

Regenwetter et al. · 2023 · Comput. Aided Des. · **ตรง**

[แหล่ง](https://arxiv.org/abs/2302.02913) · [arXiv:2302.02913](https://arxiv.org/abs/2302.02913) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-031_Regenwetter2023_beyond-statistical-similarity-rethinking-metrics-f.pdf`](../../../papers/02_ai_agents_engineering/AG-031_Regenwetter2023_beyond-statistical-similarity-rethinking-metrics-f.pdf)

เสนอว่าแบบที่สร้างต้องวัดด้วยการผ่านข้อจำกัด สมรรถนะ และความใหม่ ไม่ใช่ความคล้ายกับข้อมูล สอดคล้องกับเกณฑ์การค้นพบของเรา

### AG-032 — Constraining Generative Models for Engineering Design with Negative Data

Giannone et al. · 2023 · Trans. Mach. Learn. Res. · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2306.15166) · [arXiv:2306.15166](https://arxiv.org/abs/2306.15166) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-032_Giannone2023_constraining-generative-models-for-engineering-des.pdf`](../../../papers/02_ai_agents_engineering/AG-032_Giannone2023_constraining-generative-models-for-engineering-des.pdf)

ฝึกด้วยตัวอย่างที่ไม่ผ่านเพื่อให้ตัวสร้างอยู่ในข้อจำกัด บันทึกการปฏิเสธของเราคือข้อมูลเชิงลบแบบนี้พอดี

### AG-033 — BIKED: A Dataset for Computational Bicycle Design with Machine Learning Benchmarks

Regenwetter et al. · 2022 · Journal of Mechanical Design · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1115/1.4052585) · [arXiv:2103.05844](https://arxiv.org/abs/2103.05844) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-033_Regenwetter2022_biked-a-dataset-for-computational-bicycle-design-w.pdf`](../../../papers/02_ai_agents_engineering/AG-033_Regenwetter2022_biked-a-dataset-for-computational-bicycle-design-w.pdf)

ชุดข้อมูลการออกแบบยานพาหนะแบบพารามิเตอร์พร้อมป้ายกำกับโครงสร้างและสมรรถนะ เป็นตัวอย่างสาธารณะของข้อมูลการออกแบบยานพาหนะที่มีการตรวจความถูกต้อง

### AG-034 — The impact of AI on engineering design procedures for dynamical systems

Payrebrune et al. · 2024 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2412.12230) · [arXiv:2412.12230](https://arxiv.org/abs/2412.12230) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-034_Payrebrune2024_the-impact-of-ai-on-engineering-design-procedures.pdf`](../../../papers/02_ai_agents_engineering/AG-034_Payrebrune2024_the-impact-of-ai-on-engineering-design-procedures.pdf)

อภิปรายว่า AI เปลี่ยนกระบวนการออกแบบระบบพลวัตอย่างไร รวมถึงภาระการตรวจสอบ

### AG-035 — Eureka: Human-Level Reward Design via Coding Large Language Models

Ma et al. · 2023 · International Conference on Learning Representations · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2310.12931) · [arXiv:2310.12931](https://arxiv.org/abs/2310.12931) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-035_Ma2023_eureka-human-level-reward-design-via-coding-large.pdf`](../../../papers/02_ai_agents_engineering/AG-035_Ma2023_eureka-human-level-reward-design-via-coding-large.pdf)

LLM เขียนโค้ดรางวัลสำหรับงานควบคุม เป็นข้อเตือนว่าวัตถุประสงค์ที่ agent เขียนต้องถูกตรึงและตรวจก่อนค้นหา

### AG-036 — RoboMorph: Evolving Robot Morphology using Large Language Models

Qiu et al. · 2024 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2407.08626) · [arXiv:2407.08626](https://arxiv.org/abs/2407.08626) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-036_Qiu2024_robomorph-evolving-robot-morphology-using-large-la.pdf`](../../../papers/02_ai_agents_engineering/AG-036_Qiu2024_robomorph-evolving-robot-morphology-using-large-la.pdf)

การค้นหาเชิงวิวัฒนาการของรูปร่างหุ่นยนต์แบบโมดูลที่ขับด้วย LLM เป็นคู่เทียบโดยตรงของการกลายพันธุ์ topology ที่นำโดย LLM

### AG-037 — Text2Robot: Evolutionary Robot Design from Text Descriptions

Ringel et al. · 2024 · IEEE International Conference on Robotics and Automation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2406.19963) · [arXiv:2406.19963](https://arxiv.org/abs/2406.19963) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-037_Ringel2024_text2robot-evolutionary-robot-design-from-text-des.pdf`](../../../papers/02_ai_agents_engineering/AG-037_Ringel2024_text2robot-evolutionary-robot-design-from-text-des.pdf)

จากข้อความสู่หุ่นยนต์ขาที่วิวัฒนาการแล้วสร้างจริง แสดงข้อจำกัดการผลิตที่ต้องมีเพื่อให้ร่างที่สร้างขึ้นสร้างได้จริง

### AG-038 — Large Language Models as Optimizers

Yang et al. · 2023 · International Conference on Learning Representations · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2309.03409) · [arXiv:2309.03409](https://arxiv.org/abs/2309.03409) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-038_Yang2023_large-language-models-as-optimizers.pdf`](../../../papers/02_ai_agents_engineering/AG-038_Yang2023_large-language-models-as-optimizers.pdf)

OPRO: LLM เสนอคำตอบจากประวัติที่มีคะแนน เป็น baseline ของพฤติกรรม LLM ในบทบาท optimizer

### AG-039 — CodeEvolve: an open-source evolutionary framework for algorithmic discovery and optimization

Assumpção et al. · 2025 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2510.14150) · [arXiv:2510.14150](https://arxiv.org/abs/2510.14150) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-039_Assumpcao2025_codeevolve-an-open-source-evolutionary-framework-f.pdf`](../../../papers/02_ai_agents_engineering/AG-039_Assumpcao2025_codeevolve-an-open-source-evolutionary-framework-f.pdf)

framework แบบ AlphaEvolve ที่เป็น open source เป็นตัวอ้างอิงที่รันได้ของการค้นหาเชิงวิวัฒนาการด้วย LLM

### AG-040 — OMNI: Open-endedness via Models of human Notions of Interestingness

Zhang et al. · 2023 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2306.01711) · [arXiv:2306.01711](https://arxiv.org/abs/2306.01711) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-040_Zhang2023_omni-open-endedness-via-models-of-human-notions-of.pdf`](../../../papers/02_ai_agents_engineering/AG-040_Zhang2023_omni-open-endedness-via-models-of-human-notions-of.pdf)

ใช้ foundation model ตัดสินว่างานใดน่าสนใจ เกี่ยวข้องกับการตัดสินว่ากลไกใหม่ใดควรได้งบประเมิน

### AG-041 — Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents

Ren et al. · 2025 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2503.24047) · [arXiv:2503.24047](https://arxiv.org/abs/2503.24047) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-041_Ren2025_towards-scientific-intelligence-a-survey-of-llm-ba.pdf`](../../../papers/02_ai_agents_engineering/AG-041_Ren2025_towards-scientific-intelligence-a-survey-of-llm-ba.pdf)

survey ของ LLM scientific agent เป็นบริบทสำหรับวางตำแหน่ง agent ค้นพบทางวิศวกรรม

### AG-042 — LLEMA: Evolutionary Search with LLMs for Multi-Objective Materials Discovery

Abhyankar et al. · 2025 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2510.22503) · [arXiv:2510.22503](https://arxiv.org/abs/2510.22503) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-042_Abhyankar2025_llema-evolutionary-search-with-llms-for-multi-obje.pdf`](../../../papers/02_ai_agents_engineering/AG-042_Abhyankar2025_llema-evolutionary-search-with-llms-for-multi-obje.pdf)

การค้นหาเชิงวิวัฒนาการที่นำโดย LLM ด้านวัสดุ โครงการจำกัดตัวเองไว้ที่วัสดุในแค็ตตาล็อก จึงเป็นบริบทมากกว่าวิธีที่จะนำมาใช้

### AG-043 — Physical Design using Differentiable Learned Simulators

Allen et al. · 2022 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2202.00728) · [arXiv:2202.00728](https://arxiv.org/abs/2202.00728) · มี PDF ในเครื่อง: [`papers/02_ai_agents_engineering/AG-043_Allen2022_physical-design-using-differentiable-learned-simul.pdf`](../../../papers/02_ai_agents_engineering/AG-043_Allen2022_physical-design-using-differentiable-learned-simul.pdf)

optimize การออกแบบผ่านตัวจำลองแบบ graph network ที่เรียนรู้ (airfoil เครื่องมือของไหล) แสดงทั้งความเร็วและความเสี่ยงที่จะถูกใช้ช่องโหว่ของ surrogate


## Quality diversity อัลกอริทึมค้นหา surrogate และ multifidelity

อัลกอริทึมสำหรับใช้งบประเมินกับผู้สมัครที่หลากหลาย คุณภาพสูง และน่าเชื่อถือ: MAP-Elites และสายต่อยอด novelty search, evolution strategy, Bayesian และ multifidelity optimization และความถ่ายโอนได้จากจำลองสู่ของจริง

### QD-001 — Illuminating search spaces by mapping elites

Mouret & Clune · 2015 · arXiv.org · **ตรง** · แค็ตตาล็อก Work 102 P11

[แหล่ง](https://arxiv.org/abs/1504.04909) · [arXiv:1504.04909](https://arxiv.org/abs/1504.04909) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-001_Mouret2015_illuminating-search-spaces-by-mapping-elites.pdf`](../../../papers/03_search_qd_multifidelity/QD-001_Mouret2015_illuminating-search-spaces-by-mapping-elites.pdf)

MAP-Elites: เก็บแบบที่ดีที่สุดต่อหนึ่งช่องพฤติกรรม เป็นอัลกอริทึมพื้นฐานของ executable morphology archive (Work 099)

### QD-002 — Quality Diversity: A New Frontier for Evolutionary Computation

Pugh et al. · 2016 · Frontiers in Robotics and AI · **อ้อม** · แค็ตตาล็อก Work 102 P12

[แหล่ง](https://doi.org/10.3389/frobt.2016.00040) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-002_Pugh2016_quality-diversity-a-new-frontier-for-evolutionary.pdf`](../../../papers/03_search_qd_multifidelity/QD-002_Pugh2016_quality-diversity-a-new-frontier-for-evolutionary.pdf)

นิยาม quality diversity และแยก coverage, novelty และ quality เป็นศัพท์สำหรับสัญญา design diversity (Work 090)

### QD-003 — Data-Efficient Design Exploration through Surrogate-Assisted Illumination

Gaier et al. · 2018 · Evolutionary Computation · **ตรง** · แค็ตตาล็อก Work 102 P13

[แหล่ง](https://arxiv.org/abs/1806.05865) · [arXiv:1806.05865](https://arxiv.org/abs/1806.05865) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-003_Gaier2018_data-efficient-design-exploration-through-surrogat.pdf`](../../../papers/03_search_qd_multifidelity/QD-003_Gaier2018_data-efficient-design-exploration-through-surrogat.pdf)

SAIL รวม surrogate แบบ Gaussian process กับ MAP-Elites บนรูปทรงอากาศพลศาสตร์ เป็นวิธีโดยตรงสำหรับ illumination ที่ตัวประเมินแพง

### QD-004 — Covariance Matrix Adaptation MAP-Annealing

Fontaine & Nikolaidis · 2022 · Annual Conference on Genetic and Evolutionary Computation · **อ้อม** · แค็ตตาล็อก Work 102 P14

[แหล่ง](https://arxiv.org/abs/2205.10752) · [arXiv:2205.10752](https://arxiv.org/abs/2205.10752) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-004_Fontaine2022_covariance-matrix-adaptation-map-annealing.pdf`](../../../papers/03_search_qd_multifidelity/QD-004_Fontaine2022_covariance-matrix-adaptation-map-annealing.pdf)

CMA-MAE ปรับปรุงการค้นหา QD แบบต่อเนื่อง เป็น baseline พารามิเตอร์ต่อเนื่องที่แข็งกว่าเมื่อ MAP-Elites พื้นฐานใช้ได้แล้ว

### QD-005 — Survey of multifidelity methods in uncertainty propagation, inference, and optimization

Peherstorfer et al. · 2018 · SIAM Review · **ตรง** · แค็ตตาล็อก Work 102 P15

[แหล่ง](https://arxiv.org/abs/1806.10761) · [arXiv:1806.10761](https://arxiv.org/abs/1806.10761) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-005_Peherstorfer2018_survey-of-multifidelity-methods-in-uncertainty-pro.pdf`](../../../papers/03_search_qd_multifidelity/QD-005_Peherstorfer2018_survey-of-multifidelity-methods-in-uncertainty-pro.pdf)

เอกสารอ้างอิงของการรวมแบบจำลองถูกและแพงโดยไม่เชื่อแบบถูก เป็นรากฐานของบันได fidelity และการตรวจการเลื่อนระดับ

### QD-006 — Multi-fidelity Bayesian Optimisation with Continuous Approximations

Kandasamy et al. · 2017 · International Conference on Machine Learning · **อ้อม** · แค็ตตาล็อก Work 102 P16

[แหล่ง](https://arxiv.org/abs/1703.06240) · [arXiv:1703.06240](https://arxiv.org/abs/1703.06240) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-006_Kandasamy2017_multi-fidelity-bayesian-optimisation-with-continuo.pdf`](../../../papers/03_search_qd_multifidelity/QD-006_Kandasamy2017_multi-fidelity-bayesian-optimisation-with-continuo.pdf)

BOCA เลือกทั้งผู้สมัครและ fidelity ตามต้นทุน เกี่ยวข้องเมื่อขนาด mesh หรือ time step เป็น fidelity ที่ควบคุมได้

### QD-007 — Crossing the Reality Gap: a Short Introduction to the Transferability Approach

Mouret et al. · 2013 · arXiv.org · **ตรง** · แค็ตตาล็อก Work 102 P17

[แหล่ง](https://arxiv.org/abs/1307.1870) · [arXiv:1307.1870](https://arxiv.org/abs/1307.1870) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-007_Mouret2013_crossing-the-reality-gap-a-short-introduction-to-t.pdf`](../../../papers/03_search_qd_multifidelity/QD-007_Mouret2013_crossing-the-reality-gap-a-short-introduction-to-t.pdf)

เรียนรู้ว่าพฤติกรรมจำลองใดถ่ายโอนสู่ของจริงได้และ optimize ความถ่ายโอนได้ เป็นแบบสำหรับการคัดเลือกที่คำนึงถึงการเลื่อนระดับ

### QD-008 — The Transferability Approach: Crossing the Reality Gap in Evolutionary Robotics

Koos et al. · 2013 · IEEE Transactions on Evolutionary Computation · **ตรง**

[แหล่ง](https://doi.org/10.1109/tevc.2012.2185849) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ฉบับวารสารเต็มของ transferability approach พร้อมการทดลอง เป็นหลักฐานเบื้องหลัง QD-007

### QD-009 — Abandoning Objectives: Evolution Through the Search for Novelty Alone

Lehman & Stanley · 2011 · Evolutionary Computation · **ตรง**

[แหล่ง](https://doi.org/10.1162/evco_a_00025) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-009_Lehman2011_abandoning-objectives-evolution-through-the-search.pdf`](../../../papers/03_search_qd_multifidelity/QD-009_Lehman2011_abandoning-objectives-evolution-through-the-search.pdf)

novelty search หลุดจากวัตถุประสงค์ที่หลอกลวงได้ เกี่ยวข้องเมื่อเวลาแข่งเพียงอย่างเดียวทำให้การค้นหาติดอยู่กับ layout แบบเดิม

### QD-010 — Evolving a diversity of virtual creatures through novelty search and local competition

Lehman & Stanley · 2011 · Proceedings of the 13th annual conference on Genetic and evolutionary computation · **ตรง**

[แหล่ง](https://doi.org/10.1145/2001576.2001606) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

novelty search กับการแข่งขันเฉพาะที่บนรูปร่าง เป็นงานก่อนหน้าโดยตรงของคลังรถที่หลากหลายแต่ยังแข่งขันได้

### QD-011 — Using Centroidal Voronoi Tessellations to Scale Up the Multidimensional Archive of Phenotypic Elites Algorithm

Vassiliades et al. · 2018 · IEEE Transactions on Evolutionary Computation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1610.05729) · [arXiv:1610.05729](https://arxiv.org/abs/1610.05729) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-011_Vassiliades2018_using-centroidal-voronoi-tessellations-to-scale-up.pdf`](../../../papers/03_search_qd_multifidelity/QD-011_Vassiliades2018_using-centroidal-voronoi-tessellations-to-scale-up.pdf)

CVT-MAP-Elites คงขนาดคลังในพื้นที่ descriptor หลายมิติ จำเป็นเมื่อ descriptor ของรถเพิ่มขึ้น

### QD-012 — Covariance Matrix Adaptation for the Rapid Illumination of Behavior Space

Fontaine et al. · 2020 · Annual Conference on Genetic and Evolutionary Computation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1912.02400) · [arXiv:1912.02400](https://arxiv.org/abs/1912.02400) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-012_Fontaine2020_covariance-matrix-adaptation-for-the-rapid-illumin.pdf`](../../../papers/03_search_qd_multifidelity/QD-012_Fontaine2020_covariance-matrix-adaptation-for-the-rapid-illumin.pdf)

CMA-ME: emitter แบบ CMA-ES ภายใน MAP-Elites เป็นตัวเทียบ QD มาตรฐาน

### QD-013 — pyribs: A Bare-Bones Python Library for Quality Diversity Optimization

Tjanaka et al. · 2023 · Annual Conference on Genetic and Evolutionary Computation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2303.00191) · [arXiv:2303.00191](https://arxiv.org/abs/2303.00191) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-013_Tjanaka2023_pyribs-a-bare-bones-python-library-for-quality-div.pdf`](../../../papers/03_search_qd_multifidelity/QD-013_Tjanaka2023_pyribs-a-bare-bones-python-library-for-quality-div.pdf)

ไลบรารี QD อ้างอิงที่มี archive และ emitter เป็นการ implement ที่ทดสอบแล้วสำหรับตรวจทานโค้ด archive ของเรา

### QD-014 — Accelerated Quality-Diversity through Massive Parallelism

Lim et al. · 2023 · Trans. Mach. Learn. Res. · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2202.01258) · [arXiv:2202.01258](https://arxiv.org/abs/2202.01258) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-014_Lim2023_accelerated-quality-diversity-through-massive-para.pdf`](../../../papers/03_search_qd_multifidelity/QD-014_Lim2023_accelerated-quality-diversity-through-massive-para.pdf)

QDax: QD บน accelerator ด้วย batch ใหญ่ เกี่ยวข้องกับการเทียบบัญชีการคำนวณระหว่างขนาด batch กับจำนวนการประเมิน

### QD-015 — Multi-Objective Quality Diversity Optimization

Pierrot et al. · 2022 · Annual Conference on Genetic and Evolutionary Computation · **ตรง**

[แหล่ง](https://arxiv.org/abs/2202.03057) · [arXiv:2202.03057](https://arxiv.org/abs/2202.03057) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-015_Pierrot2022_multi-objective-quality-diversity-optimization.pdf`](../../../papers/03_search_qd_multifidelity/QD-015_Pierrot2022_multi-objective-quality-diversity-optimization.pdf)

MOME เก็บ Pareto front ต่อช่อง เหมาะกับการแลกเปลี่ยนเวลาแข่ง/พลังงาน/มวล/ความน่าเชื่อถือของ H2 ภายในคลังที่หลากหลาย

### QD-016 — Quality Diversity for Multi-task Optimization

Mouret & Maguire · 2020 · Annual Conference on Genetic and Evolutionary Computation · **ตรง**

[แหล่ง](https://arxiv.org/abs/2003.04407) · [arXiv:2003.04407](https://arxiv.org/abs/2003.04407) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-016_Mouret2020_quality-diversity-for-multi-task-optimization.pdf`](../../../papers/03_search_qd_multifidelity/QD-016_Mouret2020_quality-diversity-for-multi-task-optimization.pdf)

การค้นหาเดียวแก้หลายงานที่เกี่ยวข้องโดยแบ่งปัน elite ตรงกับการค้นหาการออกแบบเดียวข้ามหลายสภาพสนามแข่ง

### QD-017 — Multi-Task Multi-Behavior MAP-Elites

Anne & Mouret · 2023 · GECCO Companion · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2305.01264) · [arXiv:2305.01264](https://arxiv.org/abs/2305.01264) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-017_Anne2023_multi-task-multi-behavior-map-elites.pdf`](../../../papers/03_search_qd_multifidelity/QD-017_Anne2023_multi-task-multi-behavior-map-elites.pdf)

ขยาย QD หลายงานให้มีพฤติกรรมหลากหลายต่องาน เกี่ยวข้องกับคลังที่เฉพาะตามสภาพแวดล้อม (H3)

### QD-018 — BOP-Elites, a Bayesian Optimisation algorithm for Quality-Diversity search

Kent & Branke · 2020 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2005.04320) · [arXiv:2005.04320](https://arxiv.org/abs/2005.04320) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-018_Kent2020_bop-elites-a-bayesian-optimisation-algorithm-for-q.pdf`](../../../papers/03_search_qd_multifidelity/QD-018_Kent2020_bop-elites-a-bayesian-optimisation-algorithm-for-q.pdf)

Bayesian optimization สำหรับ QD ที่ใช้การประเมินน้อยมาก เกี่ยวข้องเมื่อการประเมินแต่ละครั้งคือการรัน CFD หรือ FE

### QD-019 — Designing Air Flow with Surrogate-assisted Phenotypic Niching

Hagg et al. · 2020 · Lecture Notes in Computer Science · **ตรง**

[แหล่ง](https://doi.org/10.1007/978-3-030-58112-1_10) · [arXiv:2105.04256](https://arxiv.org/abs/2105.04256) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-019_Hagg2020_designing-air-flow-with-surrogate-assisted-phenoty.pdf`](../../../papers/03_search_qd_multifidelity/QD-019_Hagg2020_designing-air-flow-with-surrogate-assisted-phenoty.pdf)

QD ที่ใช้ surrogate ช่วยสำหรับการออกแบบการไหลของอากาศด้วย phenotypic niching เป็นวิธีโดยตรงสำหรับเรขาคณิต aero/การระบายความร้อนที่หลากหลาย

### QD-020 — Prototype Discovery using Quality-Diversity

Hagg et al. · 2018 · Lecture Notes in Computer Science · **อ้อม**

[แหล่ง](https://doi.org/10.1007/978-3-319-99253-2_40) · [arXiv:1807.09488](https://arxiv.org/abs/1807.09488) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-020_Hagg2018_prototype-discovery-using-quality-diversity.pdf`](../../../papers/03_search_qd_multifidelity/QD-020_Hagg2018_prototype-discovery-using-quality-diversity.pdf)

จัดกลุ่มคลัง QD เป็นต้นแบบให้มนุษย์ตรวจ ใช้สรุปว่าตระกูลสถาปัตยกรรมใดเกิดขึ้น

### QD-021 — Robots that can adapt like animals

Cully et al. · 2015 · Nature · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1407.3501) · [arXiv:1407.3501](https://arxiv.org/abs/1407.3501) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-021_Cully2015_robots-that-can-adapt-like-animals.pdf`](../../../papers/03_search_qd_multifidelity/QD-021_Cully2015_robots-that-can-adapt-like-animals.pdf)

คลัง MAP-Elites ที่คำนวณไว้ถูกนำกลับมาใช้ฟื้นตัวเร็วหลังเสียหาย เป็นแบบการใช้คลังซ้ำเมื่อสภาพเสื่อมลง

### QD-022 — Open-ended search for environments and adapted agents using MAP-Elites

Norstein et al. · 2023 · EvoApplications · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2305.01153) · [arXiv:2305.01153](https://arxiv.org/abs/2305.01153) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-022_Norstein2023_open-ended-search-for-environments-and-adapted-age.pdf`](../../../papers/03_search_qd_multifidelity/QD-022_Norstein2023_open-ended-search-for-environments-and-adapted-age.pdf)

MAP-Elites บนสภาพแวดล้อมและ agent ร่วมกัน เกี่ยวข้องกับ curriculum ของสนามและสภาพ

### QD-023 — The CMA Evolution Strategy: A Tutorial

Hansen · 2016 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1604.00772) · [arXiv:1604.00772](https://arxiv.org/abs/1604.00772) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-023_Hansen2016_the-cma-evolution-strategy-a-tutorial.pdf`](../../../papers/03_search_qd_multifidelity/QD-023_Hansen2016_the-cma-evolution-strategy-a-tutorial.pdf)

tutorial CMA-ES ที่เชื่อถือได้ เป็น optimizer ต่อเนื่องค่าเริ่มต้นสำหรับ baseline topology คงที่ที่ปรับแล้ว

### QD-024 — A fast and elitist multiobjective genetic algorithm: NSGA-II

Deb et al. · 2002 · IEEE Transactions on Evolutionary Computation · **อ้อม**

[แหล่ง](https://doi.org/10.1109/4235.996017) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

NSGA-II เป็น baseline หลายวัตถุประสงค์มาตรฐานที่วิธีค้นหาใหม่ควรถูกเทียบด้วย

### QD-025 — Practical Bayesian Optimization of Machine Learning Algorithms

Snoek et al. · 2012 · Neural Information Processing Systems · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1206.2944) · [arXiv:1206.2944](https://arxiv.org/abs/1206.2944) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-025_Snoek2012_practical-bayesian-optimization-of-machine-learnin.pdf`](../../../papers/03_search_qd_multifidelity/QD-025_Snoek2012_practical-bayesian-optimization-of-machine-learnin.pdf)

Bayesian optimization ด้วย Gaussian process แบบใช้งานจริงรวมถึง acquisition ที่คำนึงต้นทุน เป็น baseline สำหรับการปรับพารามิเตอร์ที่แพง

### QD-026 — A Tutorial on Bayesian Optimization

Frazier · 2018 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1807.02811) · [arXiv:1807.02811](https://arxiv.org/abs/1807.02811) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-026_Frazier2018_a-tutorial-on-bayesian-optimization.pdf`](../../../papers/03_search_qd_multifidelity/QD-026_Frazier2018_a-tutorial-on-bayesian-optimization.pdf)

tutorial ที่ชัดเจนของ Bayesian optimization รวมถึงกรณี multi-fidelity และมีสัญญาณรบกวน

### QD-027 — Scalable Global Optimization via Local Bayesian Optimization

Eriksson et al. · 2019 · Neural Information Processing Systems · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1910.01739) · [arXiv:1910.01739](https://arxiv.org/abs/1910.01739) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-027_Eriksson2019_scalable-global-optimization-via-local-bayesian-op.pdf`](../../../papers/03_search_qd_multifidelity/QD-027_Eriksson2019_scalable-global-optimization-via-local-bayesian-op.pdf)

TuRBO Bayesian optimization แบบ trust region สำหรับมิติสูง เป็น baseline ที่แข็งสำหรับปรับรถแบบเดิม

### QD-028 — Bayesian Optimization of Combinatorial Structures

Baptista & Poloczek · 2018 · International Conference on Machine Learning · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1806.08838) · [arXiv:1806.08838](https://arxiv.org/abs/1806.08838) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-028_Baptista2018_bayesian-optimization-of-combinatorial-structures.pdf`](../../../papers/03_search_qd_multifidelity/QD-028_Baptista2018_bayesian-optimization-of-combinatorial-structures.pdf)

BOCS จัดการตัวแปรออกแบบแบบไม่ต่อเนื่องเชิงการจัด เกี่ยวข้องกับการเลือก topology แบบไม่ต่อเนื่อง

### QD-029 — Multi-fidelity optimization via surrogate modelling

Forrester et al. · 2007 · Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences · **ตรง**

[แหล่ง](https://doi.org/10.1098/rspa.2007.1900) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-029_Forrester2007_multi-fidelity-optimization-via-surrogate-modellin.pdf`](../../../papers/03_search_qd_multifidelity/QD-029_Forrester2007_multi-fidelity-optimization-via-surrogate-modellin.pdf)

optimization แบบ multi-fidelity ด้วย co-kriging พร้อมตัวอย่างอากาศพลศาสตร์ เป็นสูตรทางวิศวกรรมแบบคลาสสิก

### QD-030 — Predicting the output from a complex computer code when fast approximations are available

Kennedy · 2000 · Biometrika · **อ้อม**

[แหล่ง](https://doi.org/10.1093/biomet/87.1.1) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แบบจำลอง Gaussian process multi-fidelity แบบ autoregressive เป็นฐานทางสถิติของ co-kriging ข้ามระดับ fidelity

### QD-031 — Nonlinear information fusion algorithms for data-efficient multi-fidelity modelling

Perdikaris et al. · 2017 · Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences · **อ้อม**

[แหล่ง](https://doi.org/10.1098/rspa.2016.0751) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.ncbi.nlm.nih.gov/pmc/articles/5332612)

Gaussian process multi-fidelity แบบไม่เชิงเส้นสำหรับกรณีแบบถูกและแบบแพงไม่ตรงกันแบบไม่เชิงเส้น เช่น Level 0 กับแบบละเอียด

### QD-032 — A composite neural network that learns from multi-fidelity data: Application to function approximation and inverse PDE problems

Meng & Karniadakis · 2020 · Journal of Computational Physics · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1903.00104) · [arXiv:1903.00104](https://arxiv.org/abs/1903.00104) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-032_Meng2020_a-composite-neural-network-that-learns-from-multi.pdf`](../../../papers/03_search_qd_multifidelity/QD-032_Meng2020_a-composite-neural-network-that-learns-from-multi.pdf)

แบบจำลองโครงข่ายประสาท multi-fidelity เป็นทางเลือกแทน Gaussian process เมื่อข้อมูลมาก

### QD-033 — Efficient Global Optimization of Expensive Black-Box Functions

Jones et al. · 1998 · Journal of Global Optimization · **อ้อม**

[แหล่ง](https://doi.org/10.1023/a:1008306431147) · [arXiv:2211.00162](https://arxiv.org/abs/2211.00162) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-033_Jones1998_efficient-global-optimization-of-expensive-black-b.pdf`](../../../papers/03_search_qd_multifidelity/QD-033_Jones1998_efficient-global-optimization-of-expensive-black-b.pdf)

EGO และ expected improvement เป็นรากฐานของ optimization ด้วย surrogate สำหรับการจำลองที่แพง

### QD-034 — Dominated Novelty Search: Rethinking Local Competition in Quality-Diversity

Bahlous-Boldi et al. · 2025 · Proceedings of the Genetic and Evolutionary Computation Conference · **อ้อม**

[แหล่ง](https://doi.org/10.1145/3712256.3726310) · [arXiv:2502.00593](https://arxiv.org/abs/2502.00593) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-034_Boldi2025_dominated-novelty-search-rethinking-local-competit.pdf`](../../../papers/03_search_qd_multifidelity/QD-034_Boldi2025_dominated-novelty-search-rethinking-local-competit.pdf)

แทน archive แบบตารางด้วยการแปลงค่า fitness ตามการแข่งขัน เป็นทางเลือก QD ที่ไม่ต้องใช้ archive สำหรับพื้นที่ descriptor ไร้ขอบเขต

### QD-035 — Aerodynamic Design Exploration through Surrogate-Assisted Illumination

Gaier et al. · 2017 · 18th AIAA/ISSMO Multidisciplinary Analysis and Optimization Conference · **ตรง**

[แหล่ง](https://doi.org/10.2514/6.2017-3330) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-035_Gaier2017_aerodynamic-design-exploration-through-surrogate-a.pdf`](../../../papers/03_search_qd_multifidelity/QD-035_Gaier2017_aerodynamic-design-exploration-through-surrogate-a.pdf)

paper ด้านอากาศพลศาสตร์ของ SAIL ใช้ CFD ของ airfoil 2 มิติ ใกล้ที่สุดกับการค้นหาพื้นผิว aero ที่หลากหลาย

### QD-036 — Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations

Raissi et al. · 2017 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1711.10561) · [arXiv:1711.10561](https://arxiv.org/abs/1711.10561) · มี PDF ในเครื่อง: [`papers/03_search_qd_multifidelity/QD-036_Raissi2017_physics-informed-deep-learning-part-i-data-driven.pdf`](../../../papers/03_search_qd_multifidelity/QD-036_Raissi2017_physics-informed-deep-learning-part-i-data-driven.pdf)

physics-informed neural network เป็นตระกูล surrogate ที่ฝังสมการควบคุม เกี่ยวข้องเมื่อข้อมูลมีน้อย


## การแทนค่า การสร้าง และชุดข้อมูลของ CAD, B-rep และการประกอบ

วิธีแทนค่า เรียนรู้ และสร้าง solid model ลำดับการสร้าง ข้อต่อ และการประกอบ รวมถึงชุดข้อมูล CAD สาธารณะ เกี่ยวข้องกับ grammar B-rep แบบพารามิเตอร์/อิสระ semantic geometry witness, joint kernel และงาน part resolution (Works 078-096, 135-142)

### CAD-001 — DeepCAD: A Deep Generative Network for Computer-Aided Design Models

Wu et al. · 2021 · IEEE International Conference on Computer Vision · **อ้อม** · แค็ตตาล็อก Work 102 P21

[แหล่ง](https://arxiv.org/abs/2105.09492) · [arXiv:2105.09492](https://arxiv.org/abs/2105.09492) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-001_Wu2021_deepcad-a-deep-generative-network-for-computer-aid.pdf`](../../../papers/04_cad_brep_assembly/CAD-001_Wu2021_deepcad-a-deep-generative-network-for-computer-aid.pdf)

สร้างลำดับ sketch-and-extrude เป็นการแทนค่าสำหรับเสนอแบบ ผลที่ได้ยังต้องผ่าน gate ทางเดินแรงและกระบวนการผลิตของเรา

### CAD-002 — Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts

Khan et al. · 2024 · arXiv.org · **อ้อม** · แค็ตตาล็อก Work 102 P22

[แหล่ง](https://arxiv.org/abs/2409.17106) · [arXiv:2409.17106](https://arxiv.org/abs/2409.17106) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-002_Khan2024_text2cad-generating-sequential-cad-models-from-beg.pdf`](../../../papers/04_cad_brep_assembly/CAD-002_Khan2024_text2cad-generating-sequential-cad-models-from-beg.pdf)

จากข้อความสู่ลำดับ CAD โดยแบ่งระดับคำสั่ง เป็นข้อมูลและการประเมินอ้างอิงของการเสนอเรขาคณิตจากภาษา

### CAD-003 — BRepNet: A topological message passing system for solid models

Lambourne et al. · 2021 · Computer Vision and Pattern Recognition · **อ้อม** · แค็ตตาล็อก Work 102 P23

[แหล่ง](https://arxiv.org/abs/2104.00706) · [arXiv:2104.00706](https://arxiv.org/abs/2104.00706) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-003_Lambourne2021_brepnet-a-topological-message-passing-system-for-s.pdf`](../../../papers/04_cad_brep_assembly/CAD-003_Lambourne2021_brepnet-a-topological-message-passing-system-for-s.pdf)

เรียนรู้บน topology face/edge/coedge ของ B-rep โดยตรง เป็นตัวเลือก descriptor สำหรับวัดความหลากหลายที่มีความหมายทางกล

### CAD-004 — Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences

Willis et al. · 2021 · ACM Transactions on Graphics · **ข้อมูล/ผลที่ใช้ได้** · แค็ตตาล็อก Work 102 P24

[แหล่ง](https://arxiv.org/abs/2010.02392) · [arXiv:2010.02392](https://arxiv.org/abs/2010.02392) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-004_Willis2021_fusion-360-gallery-a-dataset-and-environment-for-p.pdf`](../../../papers/04_cad_brep_assembly/CAD-004_Willis2021_fusion-360-gallery-a-dataset-and-environment-for-p.pdf)

ลำดับการสร้าง CAD โดยมนุษย์พร้อมสภาพแวดล้อมการสร้างใหม่ เป็นข้อมูลสำหรับเรียนรู้ prior ของการสร้างชิ้นส่วนที่สมจริง

### CAD-005 — DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation

Park et al. · 2019 · Computer Vision and Pattern Recognition · **อ้อม** · แค็ตตาล็อก Work 102 P25

[แหล่ง](https://arxiv.org/abs/1901.05103) · [arXiv:1901.05103](https://arxiv.org/abs/1901.05103) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-005_Park2019_deepsdf-learning-continuous-signed-distance-functi.pdf`](../../../papers/04_cad_brep_assembly/CAD-005_Park2019_deepsdf-learning-continuous-signed-distance-functi.pdf)

การแทนรูปทรงแบบ signed distance โดยนัย เป็นทางเลือกของพื้นผิวตัวถังที่เรียบ แต่มีภาระเรื่อง meshing และพิกัดของ feature

### CAD-006 — ABC: A Big CAD Model Dataset For Geometric Deep Learning

Koch et al. · 2019 · Computer Vision and Pattern Recognition · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/1812.06216) · [arXiv:1812.06216](https://arxiv.org/abs/1812.06216) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-006_Koch2019_abc-a-big-cad-model-dataset-for-geometric-deep-lea.pdf`](../../../papers/04_cad_brep_assembly/CAD-006_Koch2019_abc-a-big-cad-model-dataset-for-geometric-deep-lea.pdf)

แบบ B-rep หนึ่งล้านชิ้นพร้อมเส้นโค้งและพื้นผิวพารามิเตอร์ เป็นแหล่ง benchmark สำหรับทดสอบความทนทานของ geometry kernel

### CAD-007 — UV-Net: Learning from Boundary Representations

Jayaraman et al. · 2021 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2006.10211) · [arXiv:2006.10211](https://arxiv.org/abs/2006.10211) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-007_Jayaraman2021_uv-net-learning-from-boundary-representations.pdf`](../../../papers/04_cad_brep_assembly/CAD-007_Jayaraman2021_uv-net-learning-from-boundary-representations.pdf)

สุ่มตัวอย่าง face และ edge ของ B-rep บนโดเมน UV เพื่อเรียนรู้ เป็นตัวเข้ารหัส B-rep ที่ใช้ได้จริงสำหรับ surrogate บนเรขาคณิตต้นฉบับ

### CAD-008 — SolidGen: An Autoregressive Model for Direct B-rep Synthesis

Jayaraman et al. · 2023 · Trans. Mach. Learn. Res. · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2203.13944) · [arXiv:2203.13944](https://arxiv.org/abs/2203.13944) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-008_Jayaraman2023_solidgen-an-autoregressive-model-for-direct-b-rep.pdf`](../../../papers/04_cad_brep_assembly/CAD-008_Jayaraman2023_solidgen-an-autoregressive-model-for-direct-b-rep.pdf)

สังเคราะห์ B-rep โดยตรงด้วย indexed boundary representation แสดงวิธีสร้าง topology ที่ถูกต้องโดยไม่มีประวัติการสร้าง

### CAD-009 — SkexGen: Autoregressive Generation of CAD Construction Sequences with Disentangled Codebooks

Xu et al. · 2022 · International Conference on Machine Learning · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2207.04632) · [arXiv:2207.04632](https://arxiv.org/abs/2207.04632) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-009_Xu2022_skexgen-autoregressive-generation-of-cad-construct.pdf`](../../../papers/04_cad_brep_assembly/CAD-009_Xu2022_skexgen-autoregressive-generation-of-cad-construct.pdf)

แยกรหัส topology และเรขาคณิตในลำดับ CAD เกี่ยวข้องกับการแยกการเลือกโครงสร้างออกจากมิติใน genome

### CAD-010 — Hierarchical Neural Coding for Controllable CAD Model Generation

Xu et al. · 2023 · International Conference on Machine Learning · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2307.00149) · [arXiv:2307.00149](https://arxiv.org/abs/2307.00149) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-010_Xu2023_hierarchical-neural-coding-for-controllable-cad-mo.pdf`](../../../papers/04_cad_brep_assembly/CAD-010_Xu2023_hierarchical-neural-coding-for-controllable-cad-mo.pdf)

รหัสเชิงลำดับชั้นของ loop, profile และ solid ทำให้แก้บางส่วนได้แบบควบคุม คล้ายการกลายพันธุ์เฉพาะที่ของชิ้นส่วน

### CAD-011 — BrepGen: A B-rep Generative Diffusion Model with Structured Latent Geometry

Xu et al. · 2024 · ACM Transactions on Graphics · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2401.15563) · [arXiv:2401.15563](https://arxiv.org/abs/2401.15563) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-011_Xu2024_brepgen-a-b-rep-generative-diffusion-model-with-st.pdf`](../../../papers/04_cad_brep_assembly/CAD-011_Xu2024_brepgen-a-b-rep-generative-diffusion-model-with-st.pdf)

diffusion บนต้นไม้ B-rep แฝงที่มีโครงสร้าง รวมพื้นผิวอิสระ เป็นตัวเลือกตัวสร้าง solid อิสระ (Work 092)

### CAD-012 — ComplexGen: CAD Reconstruction by B-Rep Chain Complex Generation

Guo et al. · 2022 · ACM Transactions on Graphics · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2205.14573) · [arXiv:2205.14573](https://arxiv.org/abs/2205.14573) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-012_Guo2022_complexgen-cad-reconstruction-by-b-rep-chain-compl.pdf`](../../../papers/04_cad_brep_assembly/CAD-012_Guo2022_complexgen-cad-reconstruction-by-b-rep-chain-compl.pdf)

สร้าง B-rep ใหม่เป็น chain complex พร้อมข้อจำกัดเชิง topology ชัดเจน เกี่ยวข้องกับการตรวจความสอดคล้องของ topology

### CAD-013 — JoinABLe: Learning Bottom-up Assembly of Parametric CAD Joints

Willis et al. · 2022 · Computer Vision and Pattern Recognition · **ตรง**

[แหล่ง](https://arxiv.org/abs/2111.12772) · [arXiv:2111.12772](https://arxiv.org/abs/2111.12772) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-013_Willis2022_joinable-learning-bottom-up-assembly-of-parametric.pdf`](../../../papers/04_cad_brep_assembly/CAD-013_Willis2022_joinable-learning-bottom-up-assembly-of-parametric.pdf)

ทำนายข้อต่อระหว่างชิ้นส่วนจากเรขาคณิต B-rep พร้อมชุดข้อมูล assembly/joint ของ Fusion 360 เกี่ยวข้องโดยตรงกับ joint kernel และ part resolution

### CAD-014 — AutoMate: A Dataset and Learning Approach for Automatic Mating of CAD Assemblies

Jones et al. · 2021 · ACM Transactions on Graphics · **ตรง**

[แหล่ง](https://arxiv.org/abs/2105.12238) · [arXiv:2105.12238](https://arxiv.org/abs/2105.12238) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-014_Jones2021_automate-a-dataset-and-learning-approach-for-autom.pdf`](../../../papers/04_cad_brep_assembly/CAD-014_Jones2021_automate-a-dataset-and-learning-approach-for-autom.pdf)

ชุดข้อมูลขนาดใหญ่ของ mate ใน CAD จริงและตัวทำนาย mate บน B-rep เป็นข้อมูลสำหรับทดสอบว่า interface ที่สร้างคล้าย mate ทางกลจริงหรือไม่

### CAD-015 — Assemble Them All: Physics-Based Planning for Generalizable Assembly by Disassembly

Tian et al. · 2022 · ACM Transactions on Graphics · **ตรง**

[แหล่ง](https://doi.org/10.1145/3550454.3555525) · [arXiv:2211.03977](https://arxiv.org/abs/2211.03977) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-015_Tian2022_assemble-them-all-physics-based-planning-for-gener.pdf`](../../../papers/04_cad_brep_assembly/CAD-015_Tian2022_assemble-them-all-physics-based-planning-for-gener.pdf)

การวางแผนถอดประกอบด้วยฟิสิกส์พิสูจน์ว่าประกอบได้จริง เป็น gate ความสามารถในการสร้างสำหรับรถหลายชิ้นส่วนที่สร้างขึ้น

### CAD-016 — ASAP: Automated Sequence Planning for Complex Robotic Assembly with Physical Feasibility

Tian et al. · 2024 · IEEE International Conference on Robotics and Automation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2309.16909) · [arXiv:2309.16909](https://arxiv.org/abs/2309.16909) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-016_Tian2024_asap-automated-sequence-planning-for-complex-robot.pdf`](../../../papers/04_cad_brep_assembly/CAD-016_Tian2024_asap-automated-sequence-planning-for-complex-robot.pdf)

การวางแผนลำดับการประกอบพร้อมการตรวจแรงโน้มถ่วงและเสถียรภาพ เกี่ยวข้องกับการส่งมอบการผลิต (Work 130)

### CAD-017 — Geometric Deep Learning for Computer-Aided Design: A Survey

Heidari & Iosifidis · 2024 · IEEE Access · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2402.17695) · [arXiv:2402.17695](https://arxiv.org/abs/2402.17695) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-017_Heidari2024_geometric-deep-learning-for-computer-aided-design.pdf`](../../../papers/04_cad_brep_assembly/CAD-017_Heidari2024_geometric-deep-learning-for-computer-aided-design.pdf)

survey การเรียนรู้บนข้อมูล CAD (B-rep ลำดับ การประกอบ) เป็นแผนที่วิธีและชุดข้อมูลที่มีอยู่

### CAD-018 — Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations

Jiang et al. · 2026 · arXiv · **ตรง**

[แหล่ง](https://arxiv.org/abs/2609.11573) · [arXiv:2609.11573](https://arxiv.org/abs/2609.11573) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-018_Jiang2026_learn-the-solid-not-the-file-canonical-inputs-for.pdf`](../../../papers/04_cad_brep_assembly/CAD-018_Jiang2026_learn-the-solid-not-the-file-canonical-inputs-for.pdf)

เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา

### CAD-019 — TG-Diff: Coupling Discrete Topology Diffusion and Topology-conditioned Geometry Diffusions for B-Rep Generation

Sun et al. · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2607.21928) · [arXiv:2607.21928](https://arxiv.org/abs/2607.21928) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-019_Sun2026_tg-diff-coupling-discrete-topology-diffusion-and-t.pdf`](../../../papers/04_cad_brep_assembly/CAD-019_Sun2026_tg-diff-coupling-discrete-topology-diffusion-and-t.pdf)

สร้าง topology ของ B-rep ก่อนแล้วจึงเรขาคณิต สะท้อนการแบ่ง topology แล้วจึงมิติใน genome ของเรา

### CAD-020 — HiFi-BRep: High-Fidelity Latent Representation for Robust B-Rep Generation

Hou et al. · 2026 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2608.16485) · [arXiv:2608.16485](https://arxiv.org/abs/2608.16485) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-020_Hou2026_hifi-brep-high-fidelity-latent-representation-for.pdf`](../../../papers/04_cad_brep_assembly/CAD-020_Hou2026_hifi-brep-high-fidelity-latent-representation-for.pdf)

มุ่งความทนทานของ B-rep ที่สร้าง (ปิดสนิท solid ที่ถูกต้อง) เกี่ยวข้องกับ constructive validity gate (Work 095)

### CAD-021 — CADENA: Stepwise CAD Reverse Engineering

Kabisov et al. · 2026 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2608.00799) · [arXiv:2608.00799](https://arxiv.org/abs/2608.00799) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-021_Kabisov2026_cadena-stepwise-cad-reverse-engineering.pdf`](../../../papers/04_cad_brep_assembly/CAD-021_Kabisov2026_cadena-stepwise-cad-reverse-engineering.pdf)

กู้ CAD ที่แก้ได้ทีละขั้นจากเรขาคณิต ใช้แปลง mesh หรือ field ที่วิวัฒนาการได้กลับเป็นชิ้นส่วนที่แก้ได้

### CAD-022 — HoLa: B-Rep Generation using a Holistic Latent Representation

Liu et al. · 2025 · ACM Transactions on Graphics · **อ้อม**

[แหล่ง](https://doi.org/10.1145/3730842) · [arXiv:2504.14257](https://arxiv.org/abs/2504.14257) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-022_Liu2025_hola-b-rep-generation-using-a-holistic-latent-repr.pdf`](../../../papers/04_cad_brep_assembly/CAD-022_Liu2025_hola-b-rep-generation-using-a-holistic-latent-repr.pdf)

พื้นที่แฝงเดียวสำหรับเรขาคณิตและ topology ของ B-rep เป็นงานต่อจาก BrepGen สำหรับเสนอ solid อิสระ

### CAD-023 — AutoBrep: Autoregressive B-Rep Generation with Unified Topology and Geometry

Xu et al. · 2025 · Proceedings of the SIGGRAPH Asia 2025 Conference Papers · **อ้อม**

[แหล่ง](https://doi.org/10.1145/3757377.3763814) · [arXiv:2512.03018](https://arxiv.org/abs/2512.03018) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-023_Xu2025_autobrep-autoregressive-b-rep-generation-with-unif.pdf`](../../../papers/04_cad_brep_assembly/CAD-023_Xu2025_autobrep-autoregressive-b-rep-generation-with-unif.pdf)

การสร้าง B-rep แบบ autoregressive ด้วย token รวม topology และเรขาคณิต เป็นตัวสร้างทางเลือกที่ควบคุมระดับลำดับได้

### CAD-024 — BrepDiff: Single-stage B-rep Diffusion Model

Lee et al. · 2025 · Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers · **อ้อม**

[แหล่ง](https://doi.org/10.1145/3721238.3730698) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://doi.org/10.1145/3721238.3730698)

diffusion ขั้นเดียวสำหรับ B-rep เป็นตัวสร้างที่ง่ายกว่าสำหรับเทียบอัตราความถูกต้อง

### CAD-025 — DTGBrepGen: A Novel B-rep Generative Model through Decoupling Topology and Geometry

Li et al. · 2025 · 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) · **อ้อม**

[แหล่ง](https://doi.org/10.1109/cvpr52734.2025.01997) · [arXiv:2503.13110](https://arxiv.org/abs/2503.13110) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-025_Li2025_dtgbrepgen-a-novel-b-rep-generative-model-through.pdf`](../../../papers/04_cad_brep_assembly/CAD-025_Li2025_dtgbrepgen-a-novel-b-rep-generative-model-through.pdf)

แยกการสร้าง topology กับเรขาคณิตของ B-rep อีกหนึ่งข้อมูลเรื่องความถูกต้องเทียบกับความหลากหลาย

### CAD-026 — CAD-MLLM: Unifying Multimodality-Conditioned CAD Generation With MLLM

Xu et al. · 2024 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2411.04954) · [arXiv:2411.04954](https://arxiv.org/abs/2411.04954) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-026_Xu2024_cad-mllm-unifying-multimodality-conditioned-cad-ge.pdf`](../../../papers/04_cad_brep_assembly/CAD-026_Xu2024_cad-mllm-unifying-multimodality-conditioned-cad-ge.pdf)

การสร้าง CAD ที่มีเงื่อนไขหลายรูปแบบ (ข้อความ ภาพ point cloud) เกี่ยวข้องกับการกำหนดเงื่อนไขการเสนอชิ้นส่วนด้วยเรขาคณิตของ interface

### CAD-027 — FlexCAD: Unified and Versatile Controllable CAD Generation with Fine-tuned Large Language Models

Zhang et al. · 2024 · International Conference on Learning Representations · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2411.05823) · [arXiv:2411.05823](https://arxiv.org/abs/2411.05823) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-027_Zhang2024_flexcad-unified-and-versatile-controllable-cad-gen.pdf`](../../../papers/04_cad_brep_assembly/CAD-027_Zhang2024_flexcad-unified-and-versatile-controllable-cad-gen.pdf)

การแก้ CAD แบบควบคุมได้ด้วย LLM ในหลายระดับลำดับชั้น คล้ายตัวกลายพันธุ์เชิงลำดับชั้น

### CAD-028 — GenCAD: Image-Conditioned Computer-Aided Design Generation with Transformer-Based Contrastive Representation and Diffusion Priors

Alam & Ahmed · 2024 · Trans. Mach. Learn. Res. · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2409.16294) · [arXiv:2409.16294](https://arxiv.org/abs/2409.16294) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-028_Alam2024_gencad-image-conditioned-computer-aided-design-gen.pdf`](../../../papers/04_cad_brep_assembly/CAD-028_Alam2024_gencad-image-conditioned-computer-aided-design-gen.pdf)

การสร้างโปรแกรม CAD จากภาพ เป็นอีกเส้นทางการเสนอแบบที่ยังต้องผ่าน gate ทางกายภาพ

### CAD-029 — Self-Supervised Representation Learning for CAD

Jones et al. · 2023 · 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) · **อ้อม**

[แหล่ง](https://doi.org/10.1109/cvpr52729.2023.02043) · [arXiv:2210.10807](https://arxiv.org/abs/2210.10807) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-029_Jones2023_self-supervised-representation-learning-for-cad.pdf`](../../../papers/04_cad_brep_assembly/CAD-029_Jones2023_self-supervised-representation-learning-for-cad.pdf)

embedding ของ B-rep แบบ self-supervised ที่ไม่ต้องใช้ป้ายกำกับ เป็น descriptor ที่ใช้ได้เมื่อข้อมูลวิศวกรรมที่มีป้ายกำกับมีน้อย

### CAD-030 — Hierarchical CADNet: Learning from B-Reps for Machining Feature Recognition

Colligan et al. · 2022 · Computer-Aided Design · **อ้อม**

[แหล่ง](https://doi.org/10.1016/j.cad.2022.103226) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.sciencedirect.com/science/article/pii/S0010448522000240/pdf)

รู้จำ machining feature บน B-rep เป็นเส้นทางสู่การตรวจความสามารถในการผลิตอัตโนมัติใน constructive validity gate

### CAD-031 — Graph representation of 3D CAD models for machining feature recognition with deep learning

Cao et al. · 2020 · Volume 11A: 46th Design Automation Conference (DAC) · **อ้อม**

[แหล่ง](https://doi.org/10.1115/detc2020-22355) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เสนอการเข้ารหัสแบบกราฟและชุดข้อมูล machining feature สังเคราะห์ (MFCAD) เป็นข้อมูลสำหรับตัวจำแนกความสามารถในการผลิต

### CAD-032 — LINKS: A dataset of a hundred million planar linkage mechanisms for data-driven kinematic design

Nobari et al. · 2022 · Volume 3A: 48th Design Automation Conference (DAC) · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1115/detc2022-89798) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ชุดข้อมูล linkage ระนาบหนึ่งร้อยล้านชุดพร้อม coupler curve เป็นข้อมูลและวิธีสำหรับสังเคราะห์ linkage และ motion ratio (Work 075)

### CAD-033 — KDH-CAD: Knowledge-data hybrid CAD learning under data scarcity

Gao et al. · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2606.01702) · [arXiv:2606.01702](https://arxiv.org/abs/2606.01702) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-033_Gao2026_kdh-cad-knowledge-data-hybrid-cad-learning-under-d.pdf`](../../../papers/04_cad_brep_assembly/CAD-033_Gao2026_kdh-cad-knowledge-data-hybrid-cad-learning-under-d.pdf)

รวมความรู้ทางวิศวกรรมกับข้อมูล CAD ที่มีน้อย เกี่ยวข้องเพราะข้อมูลชิ้นส่วนรถมีน้อยและเป็นกรรมสิทธิ์

### CAD-034 — MatchMaker: Automated Asset Generation for Robotic Assembly

Wang et al. · 2025 · IEEE International Conference on Robotics and Automation · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2503.05887) · [arXiv:2503.05887](https://arxiv.org/abs/2503.05887) · มี PDF ในเครื่อง: [`papers/04_cad_brep_assembly/CAD-034_Wang2025_matchmaker-automated-asset-generation-for-robotic.pdf`](../../../papers/04_cad_brep_assembly/CAD-034_Wang2025_matchmaker-automated-asset-generation-for-robotic.pdf)

สร้างคู่ชิ้นส่วนที่ประกบกันพร้อมระยะเผื่อสำหรับการประกอบ เกี่ยวข้องกับการสร้างระยะเผื่อและ fit ของ interface


## Topology optimization, meshing, finite element, contact และตัวเลขของการพัง

วิธีที่เปลี่ยนเรขาคณิตที่ผ่านแล้วเป็น field ที่แก้แล้วและสถานะการพัง: structural topology optimization, meshing ทรงสี่หน้าที่ทนทาน ปัญหาตรวจสอบ element, contact แบบมีแรงเสียดทาน แบบจำลองการแตกและความล้า การทบทวนของ Work 102 จัดให้การประเมินจากเรขาคณิตสู่ field แบบอิสระเป็นช่องว่างอันดับแรก

### ST-001 — Generating optimal topologies in structural design using a homogenization method

Bendsøe & Kikuchi · 1988 · Computer Methods in Applied Mechanics and Engineering · **ตรง** · แค็ตตาล็อก Work 102 P26

[แหล่ง](https://doi.org/10.1016/0045-7825(88)90086-2) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

paper ต้นกำเนิดของ structural topology optimization เป็นงานก่อนหน้าที่มีข้อจำกัดทางฟิสิกส์ของการปล่อยให้ทางเดินแรงเกิดขึ้นเอง

### ST-002 — A 99 line topology optimization code written in Matlab

Sigmund · 2001 · Structural and Multidisciplinary Optimization · **อ้อม** · แค็ตตาล็อก Work 102 P27

[แหล่ง](https://doi.org/10.1007/s001580050176) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://orbit.dtu.dk/en/publications/a-99-line-topology-optimization-code-written-in-matlab(b0794468-93a9-4cca-87b3-b4224938859a).html)

baseline compliance แบบ SIMP ที่กระชับ เป็นวิธีง่ายแต่แข็งที่การค้นหาโครงสร้างอิสระใด ๆ ควรทำได้ดีกว่าหรือเท่ากัน

### ST-003 — Efficient topology optimization in MATLAB using 88 lines of code

Andreassen et al. · 2011 · Structural and Multidisciplinary Optimization · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s00158-010-0594-7) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-003_Andreassen2011_efficient-topology-optimization-in-matlab-using-88.pdf`](../../../papers/05_structures_meshing_contact/ST-003_Andreassen2011_efficient-topology-optimization-in-matlab-using-88.pdf)

รุ่นต่อจากโค้ด 99 บรรทัดที่เร็วกว่าและมี filter เป็นการ implement อ้างอิงที่ใช้ได้จริงสำหรับ baseline โครงสร้าง 2 มิติ

### ST-004 — Giga-voxel computational morphogenesis for structural design

Aage et al. · 2017 · Nature · **ตรง**

[แหล่ง](https://doi.org/10.1038/nature23911) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-004_Aage2017_giga-voxel-computational-morphogenesis-for-structu.pdf`](../../../papers/05_structures_meshing_contact/ST-004_Aage2017_giga-voxel-computational-morphogenesis-for-structu.pdf)

topology optimization ของปีกเครื่องบินทั้งปีกที่ความละเอียดพันล้าน voxel ค้นพบโครงสร้างภายในที่ไม่ธรรมดา ใกล้ที่สุดกับการค้นพบทั้งชิ้นส่วนด้านโครงสร้าง

### ST-005 — Topology optimization approaches: A comparative review

Sigmund & Maute · 2013 · Structural and Multidisciplinary Optimization · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s00158-013-0978-6) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://orbit.dtu.dk/en/publications/topology-optimization-approaches(f861e156-422e-4bb0-a0ad-d378322003f9).html)

เปรียบเทียบ topology optimization แบบ density, level-set, phase-field และเชิงวิวัฒนาการ ช่วยตัดสินว่าแบบใดเหมาะกับ gate ใด

### ST-006 — Material interpolation schemes in topology optimization

Bendsøe & Sigmund · 1999 · Archive of Applied Mechanics (Ingenieur Archiv) · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s004190050248) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ให้เหตุผลทางฟิสิกส์ของการลงโทษแบบ SIMP เกี่ยวข้องกับ spatial material-void field (Work 108)

### ST-007 — Level-set methods for structural topology optimization: a review

Dijk et al. · 2013 · Structural and Multidisciplinary Optimization · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s00158-013-0912-y) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ขอบเขตแบบ level-set ให้เรขาคณิตคมที่แปลงเป็น CAD ได้ เกี่ยวข้องกับการแปลง field ที่ optimize แล้วเป็น B-rep

### ST-008 — An efficient 3D topology optimization code written in Matlab

Liu & Tovar · 2014 · Structural and Multidisciplinary Optimization · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s00158-014-1107-x) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-008_Liu2014_an-efficient-3d-topology-optimization-code-written.pdf`](../../../papers/05_structures_meshing_contact/ST-008_Liu2014_an-efficient-3d-topology-optimization-code-written.pdf)

โค้ด topology optimization 3 มิติที่กระชับ เป็น baseline โครงสร้าง 3 มิติสำหรับเทียบระดับชิ้นส่วน

### ST-009 — Current and future trends in topology optimization for additive manufacturing

Liu et al. · 2018 · Structural and Multidisciplinary Optimization · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s00158-018-1994-3) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-009_Liu2018_current-and-future-trends-in-topology-optimization.pdf`](../../../papers/05_structures_meshing_contact/ST-009_Liu2018_current-and-future-trends-in-topology-optimization.pdf)

ทบทวนข้อจำกัดการผลิต (overhang ขนาด feature ต่ำสุด support) ใน topology optimization เป็นข้อมูลเข้าของภาษาการผลิต

### ST-010 — A Review of Topology Optimisation for Fluid-Based Problems

Alexandersen & Andreasen · 2020 · Fluids · **อ้อม**

[แหล่ง](https://doi.org/10.3390/fluids5010029) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.mdpi.com/2311-5521/5/1/29/pdf)

ทบทวน topology optimization ของการไหลและการถ่ายเทความร้อนร่วม เกี่ยวข้องกับท่อและตัวแลกเปลี่ยนความร้อน (Work 121)

### ST-011 — Gmsh: A 3-D finite element mesh generator with built-in pre- and post-processing facilities

Geuzaine & Remacle · 2009 · International Journal for Numerical Methods in Engineering · **ตรง** · แค็ตตาล็อก Work 102 P28

[แหล่ง](https://doi.org/10.1002/nme.2579) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-011_Geuzaine2009_gmsh-a-3-d-finite-element-mesh-generator-with-buil.pdf`](../../../papers/05_structures_meshing_contact/ST-011_Geuzaine2009_gmsh-a-3-d-finite-element-mesh-generator-with-buil.pdf)

ตัวสร้าง mesh ของ geometry-mesh bridge (Work 110) ควรอ่านคู่กับเอกสารก่อนเชื่อการตั้งค่าคุณภาพ mesh

### ST-012 — Fast Tetrahedral Meshing in the Wild

Hu et al. · 2020 · ACM Transactions on Graphics · **ตรง**

[แหล่ง](https://arxiv.org/abs/1908.03581) · [arXiv:1908.03581](https://arxiv.org/abs/1908.03581) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-012_Hu2020_fast-tetrahedral-meshing-in-the-wild.pdf`](../../../papers/05_structures_meshing_contact/ST-012_Hu2020_fast-tetrahedral-meshing-in-the-wild.pdf)

fTetWild สร้าง mesh จาก triangle soup ที่ไม่สมบูรณ์ได้อย่างทนทาน เป็นทางสำรองเมื่อ CAD ที่สร้างไม่สะอาดพอสำหรับ meshing จาก CAD

### ST-013 — Tetrahedral Meshing in the Wild

Hu et al. · 2018 · ACM Transactions on Graphics · **อ้อม**

[แหล่ง](https://doi.org/10.1145/3197517.3201353) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://dl.acm.org/doi/pdf/10.1145/3197517.3201353)

TetWild: การสร้างทรงสี่หน้าที่ทนทานด้วย envelope เป็นวิธีเบื้องหลัง ST-012 พร้อมการรับประกัน

### ST-014 — TetGen, a Delaunay-Based Quality Tetrahedral Mesh Generator

Si · 2015 · ACM Transactions on Mathematical Software · **อ้อม**

[แหล่ง](https://doi.org/10.1145/2629697) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การสร้าง mesh ทรงสี่หน้าแบบ constrained Delaunay พร้อมขอบเขตคุณภาพ เป็นตัวสร้าง mesh อิสระสำหรับตรวจความไวต่อ mesh

### ST-015 — Incremental Potential Contact: Intersection- and Inversion-free, Large-Deformation Dynamics

Li et al. · 2020 · ACM Transactions on Graphics · **ตรง** · แค็ตตาล็อก Work 102 P29

[แหล่ง](https://doi.org/10.1145/3386569.3392425) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-015_Li2020_incremental-potential-contact-intersection-and-inv.pdf`](../../../papers/05_structures_meshing_contact/ST-015_Li2020_incremental-potential-contact-intersection-and-inv.pdf)

contact แบบมีแรงเสียดทานที่รับประกันการไม่ทะลุสำหรับการเสียรูปมาก เป็นวิธีตัวเลือกสำหรับ moving contact assembly (Work 114)

### ST-016 — High-Order Incremental Potential Contact for Elastodynamic Simulation on Curved Meshes

Ferguson et al. · 2023 · International Conference on Computer Graphics and Interactive Techniques · **อ้อม** · แค็ตตาล็อก Work 102 P30

[แหล่ง](https://arxiv.org/abs/2205.13727) · [arXiv:2205.13727](https://arxiv.org/abs/2205.13727) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-016_Ferguson2023_high-order-incremental-potential-contact-for-elast.pdf`](../../../papers/05_structures_meshing_contact/ST-016_Ferguson2023_high-order-incremental-potential-contact-for-elast.pdf)

ขยาย IPC ไปยัง mesh โค้งอันดับสูง เกี่ยวข้องเมื่อใช้ mesh ที่ตรงกับ CAD

### ST-017 — Intersection-free Rigid Body Dynamics

Ferguson et al. · 2021 · ACM Transactions on Graphics · **อ้อม**

[แหล่ง](https://doi.org/10.1145/3450626.3459802) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

IPC สำหรับวัตถุแข็งพร้อมวิถีโค้ง เกี่ยวข้องกับ contact ของข้อต่อแข็งและตัวยึดโดยไม่ทะลุ

### ST-018 — Affine Body Dynamics: Fast, Stable & Intersection-free Simulation of Stiff Materials

Lan et al. · 2022 · ACM Transactions on Graphics · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2201.10022) · [arXiv:2201.10022](https://arxiv.org/abs/2201.10022) · มี PDF ในเครื่อง: [`papers/05_structures_meshing_contact/ST-018_Lan2022_affine-body-dynamics-fast-stable-intersection-free.pdf`](../../../papers/05_structures_meshing_contact/ST-018_Lan2022_affine-body-dynamics-fast-stable-intersection-free.pdf)

วัตถุแข็งเกร็งแบบ affine deformation พร้อม contact แบบ IPC เป็นทางเลือกที่เร็วสำหรับการประกอบหลายชิ้น

### ST-019 — A proposed standard set of problems to test finite element accuracy

Macneal & Harder · 1985 · Finite Elements in Analysis and Design · **ตรง**

[แหล่ง](https://doi.org/10.1016/0168-874x(85)90003-4) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การทดสอบ patch และการบิดเบี้ยวของ element ของ MacNeal-Harder เป็นปัญหาตรวจสอบมาตรฐานสำหรับ element ที่เรา implement (Work 041)

### ST-020 — A review on phase-field models of brittle fracture and a new fast hybrid formulation

Ambati et al. · 2015 · Computational Mechanics · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s00466-014-1109-y) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ทบทวนแบบจำลองการแตกแบบ phase-field พร้อมสูตรผสมที่เร็ว เป็นเส้นทางจากการเริ่มแตก (Work 043) สู่การลามของรอยแตก

### ST-021 — Cumulative fatigue damage and life prediction theories: a survey of the state of the art for homogeneous materials

Fatemi & Yang · 1998 · International Journal of Fatigue · **ตรง**

[แหล่ง](https://doi.org/10.1016/s0142-1123(97)00081-9) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

สำรวจทางเลือกของกฎ Miner และความคลาดเคลื่อนภายใต้แอมพลิจูดแปรผัน กำหนดขอบเขตของ gate อายุความล้า (Work 044) โดยตรง

### ST-022 — Cumulative Damage in Fatigue

Wilkins · 1945 · Colloquium on Fatigue / Colloque de Fatigue / Kolloquium über Ermüdungsfestigkeit · **อ้อม**

[แหล่ง](https://doi.org/10.1007/978-3-642-99854-6_35) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

กฎความเสียหายเชิงเส้นของ Miner เป็นสมมติฐานเบื้องหลังการคิดความล้าแบบง่าย ควรอ้างพร้อมข้อจำกัดที่ทราบว่าไม่ปลอดภัยเสมอ

### ST-023 — A Critical Analysis of Crack Propagation Laws

Paris & Erdogan · 1963 · Journal of Basic Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1115/1.3656900) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

กฎการโตของรอยแตกของ Paris-Erdogan เป็นฐานของแนวทาง damage tolerance แทน safe-life

### ST-024 — An implicit time-stepping scheme for rigid body dynamics with inelastic collisions and coulomb friction

STEWART & TRINKLE · 1996 · International Journal for Numerical Methods in Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1002/(sici)1097-0207(19960815)39:15<2673::aid-nme972>3.0.co;2-i) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การก้าวเวลาแบบ complementarity ของ Stewart-Trinkle สำหรับ contact ที่มีแรงเสียดทาน เป็นสูตรคลาสสิกเบื้องหลัง solver contact แข็งหลายตัว


## โครงสร้างพื้นฐานการจำลอง optimal control และ MDO การเชื่อมโยง และ integrator

engine solver และภาษาแบบจำลองที่โครงการอาจนำมาใช้หรือใช้ตรวจทาน: multibody dynamics การจำลองแบบ differentiable การเชื่อมโยง co-simulation การจำลองแบบ energy port ไม่มีทิศเหตุ integrator ที่รักษาโครงสร้าง และ solver nonlinear programming ที่ใช้กับปัญหาเวลาต่ำสุด

### SI-001 — DiffTaichi: Differentiable Programming for Physical Simulation

Hu et al. · 2020 · International Conference on Learning Representations · **อ้อม** · แค็ตตาล็อก Work 102 P08

[แหล่ง](https://arxiv.org/abs/1910.00935) · [arXiv:1910.00935](https://arxiv.org/abs/1910.00935) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-001_Hu2020_difftaichi-differentiable-programming-for-physical.pdf`](../../../papers/06_simulation_infrastructure/SI-001_Hu2020_difftaichi-differentiable-programming-for-physical.pdf)

ภาษาการจำลองแบบ differentiable เป็นเส้นทางสู่การปรับละเอียดด้วย gradient ภายใน topology ที่ผ่านแล้ว โดย gradient ไม่ได้พิสูจน์ความแม่นยำ

### SI-002 — Chrono: An Open Source Multi-physics Dynamics Engine

Tasora et al. · 2016 · Lecture Notes in Computer Science · **อ้อม** · แค็ตตาล็อก Work 102 P54

[แหล่ง](https://doi.org/10.1007/978-3-319-40361-8_2) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

engine multibody และ contact แบบเปิด เป็น backend อิสระตัวเลือกสำหรับตรวจทานพลวัตของรถ

### SI-003 — Chrono::Vehicle: template-based ground vehicle modelling and simulation

Serban et al. · 2019 · International Journal of Vehicle Performance · **ตรง** · แค็ตตาล็อก Work 102 P55

[แหล่ง](https://doi.org/10.1504/ijvp.2019.097096) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แบบจำลองรถแบบ template ใน engine เปิด เป็นเส้นทางสาธารณะที่ใช้ได้จริงที่สุดสู่ baseline แบบเดิมที่ทำซ้ำได้

### SI-004 — MuJoCo: A physics engine for model-based control

Todorov et al. · 2012 · 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems · **อ้อม** · แค็ตตาล็อก Work 102 P56

[แหล่ง](https://doi.org/10.1109/iros.2012.6386109) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://homes.cs.washington.edu/~todorov/papers/TodorovIROS12.pdf)

พลวัตที่มี contact มากและเร็วสำหรับการเรียนรู้การควบคุม ใช้ฝึก policy ผู้ขับได้ แต่ไม่ใช่หลักฐานยางหรือ aero ที่สอบเทียบแล้ว

### SI-005 — OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization

Gray et al. · 2019 · Structural and Multidisciplinary Optimization · **อ้อม** · แค็ตตาล็อก Work 102 P57

[แหล่ง](https://doi.org/10.1007/s00158-019-02211-z) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-005_Gray2019_openmdao-an-open-source-framework-for-multidiscipl.pdf`](../../../papers/06_simulation_infrastructure/SI-005_Gray2019_openmdao-an-open-source-framework-for-multidiscipl.pdf)

การจัดการการวิเคราะห์แบบเชื่อมโยงพร้อมอนุพันธ์ เป็นแบบสำหรับการเชื่อมการออกแบบ/การควบคุม/พลังงาน/โครงสร้าง

### SI-006 — preCICE v2: A sustainable and user-friendly coupling library

Chourdakis et al. · 2022 · Open Research Europe · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2109.14470) · [arXiv:2109.14470](https://arxiv.org/abs/2109.14470) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-006_Chourdakis2022_precice-v2-a-sustainable-and-user-friendly-couplin.pdf`](../../../papers/06_simulation_infrastructure/SI-006_Chourdakis2022_precice-v2-a-sustainable-and-user-friendly-couplin.pdf)

การเชื่อม multiphysics แบบแบ่งส่วน (ของไหล-โครงสร้าง ความร้อนร่วม) พร้อมการเร่งการลู่เข้า เกี่ยวข้องกับงาน thermal-solid แบบเชื่อมโยง (Work 115)

### SI-007 — DOLFINx: The next generation FEniCS problem solving environment

— · 2023 · **อ้อม**

[แหล่ง](https://zenodo.org/records/10447666/files/main.pdf?download=1) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-007_Anon2023_dolfinx-the-next-generation-fenics-problem-solving.pdf`](../../../papers/06_simulation_infrastructure/SI-007_Anon2023_dolfinx-the-next-generation-fenics-problem-solving.pdf)

สภาพแวดล้อม finite element แบบเปิด เป็น solver อิสระตัวเลือกสำหรับการประเมินเรขาคณิตทั่วไป (Work 138)

### SI-008 — The Pinocchio C++ library: A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives

Carpentier et al. · 2019 · 2019 IEEE/SICE International Symposium on System Integration (SII) · **อ้อม**

[แหล่ง](https://doi.org/10.1109/sii.2019.8700380) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://hal.laas.fr/hal-01866228v2/file/19-sii-pinocchio.pdf)

พลวัตวัตถุแข็งพร้อมอนุพันธ์เชิงวิเคราะห์ ใช้กับจลนศาสตร์ linkage และระบบกันสะเทือนที่ต้องการ gradient

### SI-009 — Brax: A Differentiable Physics Engine for Large Scale Rigid Body Simulation

Freeman et al. · 2021 · NeurIPS Datasets and Benchmarks · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2106.13281) · [arXiv:2106.13281](https://arxiv.org/abs/2106.13281) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-009_Freeman2021_brax-a-differentiable-physics-engine-for-large-sca.pdf`](../../../papers/06_simulation_infrastructure/SI-009_Freeman2021_brax-a-differentiable-physics-engine-for-large-sca.pdf)

ฟิสิกส์บน accelerator แบบขนานจำนวนมาก เกี่ยวข้องกับบัญชีการคำนวณเมื่อเทียบอัลกอริทึมค้นหาด้วยเวลาจริง

### SI-010 — Dojo: A Differentiable Physics Engine for Robotics

Howell et al. · 2022 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2203.00806) · [arXiv:2203.00806](https://arxiv.org/abs/2203.00806) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-010_Howell2022_dojo-a-differentiable-physics-engine-for-robotics.pdf`](../../../papers/06_simulation_infrastructure/SI-010_Howell2022_dojo-a-differentiable-physics-engine-for-robotics.pdf)

contact แบบ differentiable ด้วย interior-point complementarity เป็นทางเลือก gradient ผ่าน contact สำหรับ ground interaction

### SI-011 — A pressure field model for fast, robust approximation of net contact force and moment between nominally rigid objects

Elandt et al. · 2019 · IEEE/RJS International Conference on Intelligent RObots and Systems · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1904.11433) · [arXiv:1904.11433](https://arxiv.org/abs/1904.11433) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-011_Elandt2019_a-pressure-field-model-for-fast-robust-approximati.pdf`](../../../papers/06_simulation_infrastructure/SI-011_Elandt2019_a-pressure-field-model-for-fast-robust-approximati.pdf)

contact แบบ hydroelastic ที่ให้ความดันกระจายแทนแรงจุด เกี่ยวข้องกับ contact patch ของจุดสัมผัสพื้นแบบใดก็ได้

### SI-012 — Discrete mechanics and variational integrators

Marsden & West · 2001 · Acta Numerica · **ตรง**

[แหล่ง](https://doi.org/10.1017/s096249290100006x) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-012_Marsden2001_discrete-mechanics-and-variational-integrators.pdf`](../../../papers/06_simulation_infrastructure/SI-012_Marsden2001_discrete-mechanics-and-variational-integrators.pdf)

integrator ที่รักษาโครงสร้างโดยมีความคลาดเคลื่อนพลังงานมีขอบเขต เป็นทฤษฎีเบื้องหลังการถือ residual พลังงานเป็นผลลัพธ์ที่สังเกตได้

### SI-013 — Port-Hamiltonian Systems Theory: An Introductory Overview

Schaft & Jeltsema · 2014 · **ตรง**

[แหล่ง](https://doi.org/10.1561/9781601987877) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

รูปแบบ energy port ที่การเชื่อมต่ออนุรักษ์กำลังโดยโครงสร้าง เป็นฐานที่เข้มงวดของ typed energy graph และการตรวจการอนุรักษ์ (Works 012-013)

### SI-014 — Physical system modeling with Modelica

Mattsson et al. · 1998 · Control Engineering Practice · **อ้อม**

[แหล่ง](https://doi.org/10.1016/S0967-0661(98)00047-1) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การจำลองชิ้นส่วนแบบสมการที่ไม่มีทิศเหตุพร้อม connector ที่มีชนิด เป็นการออกแบบ port ทางกายภาพแบบมีชนิดที่เป็นที่ยอมรับ

### SI-015 — Bond-graph modeling

Machado & Cunha · 2007 · An Introduction to Bond Graph Modeling with Applications · **อ้อม**

[แหล่ง](https://doi.org/10.1201/9781003057741-2) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

tutorial ของ bond graph สำหรับการไหลของพลังงานหลายโดเมน เป็นสัญกรณ์กระชับสำหรับตรวจการเชื่อมต่อที่อนุรักษ์กำลัง

### SI-016 — The Functional Mockup Interface for Tool independent Exchange of Simulation Models

Blochwitz et al. · 2011 · Linköping Electronic Conference Proceedings · **อ้อม**

[แหล่ง](https://doi.org/10.3384/ecp11063105) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://www.ep.liu.se/ecp/063/013/ecp11063013.pdf)

มาตรฐาน co-simulation FMI เกี่ยวข้องหากเชื่อมแบบจำลองระบบย่อยจากเครื่องมืออื่นเข้ากับการจำลองการแข่ง

### SI-017 — CasADi: a software framework for nonlinear optimization and optimal control

Andersson et al. · 2019 · Mathematical Programming Computation · **ตรง**

[แหล่ง](https://doi.org/10.1007/s12532-018-0139-4) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-017_Andersson2019_casadi-a-software-framework-for-nonlinear-optimiza.pdf`](../../../papers/06_simulation_infrastructure/SI-017_Andersson2019_casadi-a-software-framework-for-nonlinear-optimiza.pdf)

เครื่องมือเปิดมาตรฐานสำหรับปัญหาเวลาต่อรอบต่ำสุดแบบ direct collocation จำเป็นสำหรับ baseline ผู้ขับที่ optimize แล้ว

### SI-018 — On the implementation of an interior-point filter line-search algorithm for large-scale nonlinear programming

Wächter & Biegler · 2006 · Mathematical Programming · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s10107-004-0559-y) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-018_Wachter2006_on-the-implementation-of-an-interior-point-filter.pdf`](../../../papers/06_simulation_infrastructure/SI-018_Wachter2006_on-the-implementation-of-an-interior-point-filter.pdf)

IPOPT เป็น solver NLP ที่งานเวลาต่อรอบต่ำสุดส่วนใหญ่ใช้ ควรรู้พฤติกรรมการลู่เข้าก่อนเชื่อผลรอบ

### SI-019 — GPOPS-II: A MATLAB Software for Solving Multiple-Phase Optimal Control Problems Using hp-Adaptive Gaussian Quadrature Collocation Methods and Sparse Nonlinear Programming

Patterson & Rao · 2014 · ACM Transactions on Mathematical Software · **อ้อม**

[แหล่ง](https://doi.org/10.1145/2558904) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

collocation แบบ hp-adaptive ที่ใช้ใน paper optimal control F1 ของ Limebeer อธิบายการปรับ mesh ของงานเหล่านั้น

### SI-020 — Energy conservation and power bonds in co-simulations: non-iterative adaptive step size control and error estimation

Sadjina et al. · 2017 · Engineering computations · **ตรง**

[แหล่ง](https://arxiv.org/abs/1602.06434) · [arXiv:1602.06434](https://arxiv.org/abs/1602.06434) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-020_Sadjina2017_energy-conservation-and-power-bonds-in-co-simulati.pdf`](../../../papers/06_simulation_infrastructure/SI-020_Sadjina2017_energy-conservation-and-power-bonds-in-co-simulati.pdf)

วัด residual พลังงานที่ power bond ของ co-simulation และใช้ควบคุมขนาดก้าว เกี่ยวข้องโดยตรงกับ residual การอนุรักษ์ที่สังเกตได้ในก้าวการแข่งแบบเชื่อมโยง

### SI-021 — Co-simulation: State of the art

Gomes et al. · 2018 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1702.00686) · [arXiv:1702.00686](https://arxiv.org/abs/1702.00686) · มี PDF ในเครื่อง: [`papers/06_simulation_infrastructure/SI-021_Gomes2018_co-simulation-state-of-the-art.pdf`](../../../papers/06_simulation_infrastructure/SI-021_Gomes2018_co-simulation-state-of-the-art.pdf)

survey การจัดการ ความเสถียร และความแม่นยำของ co-simulation เป็นพื้นหลังของการเชื่อมแบบจำลองระบบย่อยจำนวนมาก


## Optimal control เวลาต่อรอบต่ำสุด พลวัตยานยนต์ สนามแข่ง และการ optimize การออกแบบร่วมกับการควบคุม

วิธีขับรถแข่งอย่างเหมาะที่สุด และวิธี optimize พารามิเตอร์การออกแบบร่วมกับการขับนั้น เป็นฝั่งตัวประเมินของโครงการ รถที่ไม่ธรรมดาจะถูกตัดสินอย่างยุติธรรมได้ก็ต่อเมื่อมีผู้ขับที่ optimize แล้วบนสนามเชิงพื้นที่

### LT-001 — Optimal control for a Formula One car with variable parameters

Perantoni & Limebeer · 2014 · Vehicle System Dynamics · **ตรง** · แค็ตตาล็อก Work 102 P31

[แหล่ง](https://doi.org/10.1080/00423114.2014.889315) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-001_Perantoni2014_optimal-control-for-a-formula-one-car-with-variabl.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-001_Perantoni2014_optimal-control-for-a-formula-one-car-with-variabl.pdf)

การควบคุมเวลาต่อรอบต่ำสุดโดยให้พารามิเตอร์รถเป็นตัวแปร optimize เป็นแม่แบบของความยุติธรรมระหว่างการออกแบบกับผู้ขับ

### LT-002 — Optimal control of a Formula One car on a three-dimensional track-part 1: track modeling and identification

Perantoni & Limebeer · 2015 · Journal of Dynamic Systems, Measurement, and Control · **ตรง** · แค็ตตาล็อก Work 102 P32

[แหล่ง](https://doi.org/10.1115/1.4028253) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-002_Perantoni2015_optimal-control-of-a-formula-one-car-on-a-three-di.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-002_Perantoni2015_optimal-control-of-a-formula-one-car-on-a-three-di.pdf)

สร้างและระบุ ribbon ของสนาม 3 มิติ (ความโค้ง ความสูง ความเอียง) จากข้อมูล เป็นคู่มือการแทนที่สนามสังเคราะห์ของเรา

### LT-003 — Optimal Control of a Formula One Car on a Three-Dimensional Track - Part 2: Optimal Control

Limebeer & Perantoni · 2015 · Journal of Dynamic Systems, Measurement, and Control · **ตรง** · แค็ตตาล็อก Work 102 P33

[แหล่ง](https://doi.org/10.1115/1.4029466) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แก้ปัญหาเวลาต่อรอบต่ำสุดบนสนาม 3 มิติ และแสดงผลของเรขาคณิต 3 มิติต่อเวลาต่อรอบ

### LT-004 — Minimum time optimal control simulation of a GP2 race car

Bianco et al. · 2018 · Proceedings of the Institution of Mechanical Engineers, Part D: Journal of Automobile Engineering · **ตรง** · แค็ตตาล็อก Work 102 P34

[แหล่ง](https://doi.org/10.1177/0954407017728158) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-004_Bianco2018_minimum-time-optimal-control-simulation-of-a-gp2-r.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-004_Bianco2018_minimum-time-optimal-control-simulation-of-a-gp2-r.pdf)

รถ 14 DOF ยางไม่เชิงเส้น aero ตามความสูงตัวถัง และเทียบกับ telemetry เป็นเป้าหมายแบบจำลองเชื่อมโยงสาธารณะที่ใกล้ที่สุด

### LT-005 — Optimizing the aero-suspension interactions in a Formula One car

Masouleh & Limebeer · 2016 · IEEE Transactions on Control Systems Technology · **ตรง** · แค็ตตาล็อก Work 102 P35

[แหล่ง](https://doi.org/10.1109/tcst.2015.2475396) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-005_Masouleh2016_optimizing-the-aero-suspension-interactions-in-a-f.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-005_Masouleh2016_optimizing-the-aero-suspension-interactions-in-a-f.pdf)

optimize เรขาคณิตระบบกันสะเทือนและ aero ที่ขึ้นกับความสูงตัวถังร่วมกัน เป็น benchmark ของ aero-chassis coupling (Work 024)

### LT-006 — Minimum curvature trajectory planning and control for an autonomous race car

Heilmeier et al. · 2020 · Vehicle System Dynamics · **อ้อม** · แค็ตตาล็อก Work 102 P39

[แหล่ง](https://doi.org/10.1080/00423114.2019.1631455) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://mediatum.ub.tum.de/node?id=1509975)

การ optimize เส้นแข่งที่ใช้ได้จริงพร้อมโค้ดและข้อมูลสนามแบบเปิด เป็นเส้นแข่ง baseline ที่เร็ว ไม่ใช่เส้นเวลาต่ำสุด

### LT-007 — Time-optimal control of the race car: a numerical method to emulate the ideal driver

Kelly & Sharp · 2010 · Vehicle System Dynamics · **ตรง**

[แหล่ง](https://doi.org/10.1080/00423110903514236) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การเลียนแบบผู้ขับเวลาต่ำสุดแบบ transient เป็นสูตรผู้ขับที่เหมาะที่สุดยุคแรกสำหรับเทียบกับวิธี steady-state

### LT-008 — Vehicle dynamics applications of optimal control theory

Sharp & Peng · 2011 · Vehicle System Dynamics · **อ้อม**

[แหล่ง](https://doi.org/10.1080/00423114.2011.586707) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ทบทวน optimal control ในพลวัตยานยนต์ เป็นแนวทางการเลือกแบบจำลองผู้ขับที่ fidelity ต่างกัน

### LT-009 — Lap time optimisation of a racing go-kart

Lot & Bianco · 2016 · Vehicle System Dynamics · **อ้อม**

[แหล่ง](https://doi.org/10.1080/00423114.2015.1125514) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://eprints.soton.ac.uk/385883/2/Lap%2520time%2520optimisation%2520of%2520a%2520racing%2520go-kart%2520%2528corrected%2520proof%2529.pdf)

เวลาต่อรอบต่ำสุดของรถที่ไม่มีเฟืองท้ายหรือระบบกันสะเทือน เป็นหลักฐานว่าวิธีนี้ใช้กับแชสซีที่ไม่ธรรมดาได้

### LT-010 — A Curvilinear Abscissa Approach for the Lap Time Optimization of Racing Vehicles

Lot & Biral · 2014 · IFAC Proceedings Volumes · **อ้อม**

[แหล่ง](https://doi.org/10.3182/20140824-6-za-1003.00868) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-010_Lot2014_a-curvilinear-abscissa-approach-for-the-lap-time-o.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-010_Lot2014_a-curvilinear-abscissa-approach-for-the-lap-time-o.pdf)

สูตรพิกัดเชิงเส้นโค้งที่ solver เวลาต่อรอบยุคใหม่ส่วนใหญ่ใช้ จำเป็นสำหรับตั้งพลวัตที่อิงกับสนามของเรา

### LT-011 — A free-trajectory quasi-steady-state optimal-control method for minimum lap-time of race vehicles

Veneri & Massaro · 2020 · Vehicle System Dynamics · **ตรง**

[แหล่ง](https://doi.org/10.1080/00423114.2019.1608364) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://hdl.handle.net/11577/3297111)

optimal control แบบกึ่งคงตัวที่เส้นแข่งเป็นอิสระและใช้แผนที่ g-g เร็วพอจะประเมินรถหลายแบบ

### LT-012 — A three-dimensional free-trajectory quasi-steady-state optimal-control method for minimum-lap-time of race vehicles

Lovato & Massaro · 2022 · Vehicle System Dynamics · **ตรง**

[แหล่ง](https://doi.org/10.1080/00423114.2021.1878242) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://hdl.handle.net/11577/3375385)

ขยาย LT-011 สู่สนาม 3 มิติด้วยแผนภาพ g-g-g เป็นตัวประเมินที่เร็วซึ่งเข้ากับ 3D circuit corridor ของเรา (Work 010)

### LT-013 — Online Time-Optimal Trajectory Planning on Three-Dimensional Race Tracks

Rowold et al. · 2023 · 2023 IEEE Intelligent Vehicles Symposium (IV) · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2304.10954) · [arXiv:2304.10954](https://arxiv.org/abs/2304.10954) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-013_Rowold2023_online-time-optimal-trajectory-planning-on-three-d.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-013_Rowold2023_online-time-optimal-trajectory-planning-on-three-d.pdf)

การวางแผนเวลาต่ำสุดแบบมวลจุดบนสนาม 3 มิติพร้อมโค้ดเปิด เป็นขั้น fidelity ต่ำราคาถูกของบันได

### LT-014 — Time-optimal trajectory planning for a race car considering variable tyre-road friction coefficients

Christ et al. · 2021 · Vehicle System Dynamics · **อ้อม**

[แหล่ง](https://doi.org/10.1080/00423114.2019.1704804) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แรงเสียดทานที่แปรตามตำแหน่งในการวางแผนเวลาต่ำสุด เกี่ยวข้องกับความไม่แน่นอนของผิวสนาม

### LT-015 — GripMap: An Efficient, Spatially Resolved Constraint Framework for Offline and Online Trajectory Planning in Autonomous Racing

Werner et al. · 2025 · 2025 IEEE Intelligent Vehicles Symposium (IV) · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2504.12115) · [arXiv:2504.12115](https://arxiv.org/abs/2504.12115) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-015_Werner2025_gripmap-an-efficient-spatially-resolved-constraint.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-015_Werner2025_gripmap-an-efficient-spatially-resolved-constraint.pdf)

ข้อจำกัดการยึดเกาะที่แยกตามตำแหน่งสำหรับการวางแผน เป็นโครงสร้างข้อมูลของการยึดเกาะที่ขึ้นกับตำแหน่งบนสนาม

### LT-016 — A quasi steady state approach to race car lap simulation in order to understand the effects of racing line and centre of gravity location

Brayshaw & Harrison · 2005 · Proceedings of the Institution of Mechanical Engineers, Part D: Journal of Automobile Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1243/095440705x11211) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การจำลองรอบแบบกึ่งคงตัวที่ศึกษาผลของจุดศูนย์ถ่วง เป็นเอกสารคลาสสิกของแบบจำลองรอบ fidelity ต่ำ

### LT-017 — Lap Time Simulation: Comparison of Steady State, Quasi-Static and Transient Racing Car Cornering Strategies

Siegler et al. · 2000 · SAE Technical Paper Series · **ตรง**

[แหล่ง](https://doi.org/10.4271/2000-01-3563) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เปรียบเทียบ fidelity ของการจำลองรอบโดยตรง เป็นหลักฐานว่าเมื่อใดการจัดอันดับแบบ steady-state ต่างจากแบบ transient (H4)

### LT-018 — On minimum time vehicle manoeuvring: the theoretical optimal lap

— · 2000 · **ตรง**

[แหล่ง](https://dspace.lib.cranfield.ac.uk/handle/1826/1091) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://core.ac.uk/download/pdf/138004.pdf)

วิทยานิพนธ์ของ Casanova ที่แก้รอบที่เหมาะที่สุดแบบ transient เต็มรูปแบบและศึกษาความไวต่อพารามิเตอร์รถ

### LT-019 — Minimum-lap-time optimisation and simulation

Massaro & Limebeer · 2021 · Vehicle System Dynamics · **อ้อม**

[แหล่ง](https://doi.org/10.1080/00423114.2021.1910718) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://hdl.handle.net/11577/3389257)

ทบทวนวิธีเวลาต่อรอบต่ำสุดล่าสุดโดยผู้เชี่ยวชาญ เป็นแนวทางการเลือกสูตรและ solver

### LT-020 — Comparison of direct and indirect methods for minimum lap time optimal control problems

Bianco et al. · 2019 · Vehicle System Dynamics · **อ้อม**

[แหล่ง](https://doi.org/10.1080/00423114.2018.1480048) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://iris.unitn.it/bitstream/11572/211730/4/2_PDFsam_2018dir_vs_indirpreprint.pdf)

เปรียบเทียบการแก้ปัญหารอบเดียวกันด้วยวิธีตรงและอ้อม เป็นหลักฐานเรื่องความต่างของเวลาต่อรอบที่เกิดจาก solver

### LT-021 — Optimal control of motorsport differentials

Tremlett et al. · 2015 · Vehicle System Dynamics · **ตรง**

[แหล่ง](https://doi.org/10.1080/00423114.2015.1093150) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.tandfonline.com/doi/pdf/10.1080/00423114.2015.1093150?needAccess=true)

optimize พฤติกรรมเฟืองท้ายเพื่อเวลาต่อรอบต่ำสุด เกี่ยวข้องกับพลวัตเฟืองท้ายและล้ออิสระ (Works 070-071)

### LT-022 — A Convex Optimization Framework for Minimum Lap Time Design and Control of Electric Race Cars

Borsboom et al. · 2021 · IEEE Transactions on Vehicular Technology · **ตรง**

[แหล่ง](https://doi.org/10.1109/tvt.2021.3093164) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://research.tue.nl/en/publications/98d6f349-dcae-447b-86cc-8d61e15b7107)

กำหนดขนาด powertrain ไฟฟ้าและคำนวณกลยุทธ์เวลาต่อรอบต่ำสุดร่วมกันด้วย convex optimization เป็นวิธี co-optimization ของการออกแบบ/การควบคุมโดยตรง

### LT-023 — Minimum-lap-time Control Strategies for All-wheel Drive Electric Race Cars via Convex Optimization

Broere et al. · 2022 · European Control Conference · **ตรง**

[แหล่ง](https://arxiv.org/abs/2111.04650) · [arXiv:2111.04650](https://arxiv.org/abs/2111.04650) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-023_Broere2022_minimum-lap-time-control-strategies-for-all-wheel.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-023_Broere2022_minimum-lap-time-control-strategies-for-all-wheel.pdf)

ขีดจำกัดการยึดเกาะรายยางกับการขับเคลื่อนสี่ล้อในสูตรรอบแบบ convex เกี่ยวข้องกับการจัดสรรแรงบิดรายล้อ

### LT-024 — Time-optimal Design and Control of Electric Race Cars Equipped with Multi-speed Transmissions

Cartignij & Salazar · 2023 · Vehicle Power and Propulsion Conference · **ตรง**

[แหล่ง](https://arxiv.org/abs/2311.03545) · [arXiv:2311.03545](https://arxiv.org/abs/2311.03545) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-024_Cartignij2023_time-optimal-design-and-control-of-electric-race-c.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-024_Cartignij2023_time-optimal-design-and-control-of-electric-race-c.pdf)

เปรียบเทียบเกียร์คงที่ CVT และหลายสปีดพร้อมการควบคุมที่ optimize ร่วม เป็นการประเมินการเลือกสถาปัตยกรรมอย่างยุติธรรม

### LT-025 — Time-optimal Control Strategies for Electric Race Cars with Different Transmission Technologies

Borsboom et al. · 2020 · Vehicle Power and Propulsion Conference · **ตรง**

[แหล่ง](https://arxiv.org/abs/2005.07592) · [arXiv:2005.07592](https://arxiv.org/abs/2005.07592) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-025_Borsboom2020_time-optimal-control-strategies-for-electric-race.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-025_Borsboom2020_time-optimal-control-strategies-for-electric-race.pdf)

การเปรียบเทียบเทคโนโลยีเกียร์ภายใต้การควบคุมเวลาต่ำสุดรุ่นก่อน เป็นงานก่อนหน้าของการเทียบสถาปัตยกรรมที่ความพยายามควบคุมเท่ากัน

### LT-026 — Joint Optimisation of Active Aerodynamics and Electric Energy Deployment for Minimum Lap Time in 2026 Formula One

Saxena · 2026 · **ตรง**

[แหล่ง](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7045379) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

จัดตารางโหมดปีกขยับได้ปี 2026 ร่วมกับการปล่อยและเก็บพลังงานไฟฟ้าด้วย direct collocation ใช้ปีกติกาเดียวกับสัญญาการแข่งของเรา

### LT-027 — Kinematic and dynamic vehicle models for autonomous driving control design

Kong et al. · 2015 · 2015 IEEE Intelligent Vehicles Symposium (IV) · **อ้อม**

[แหล่ง](https://doi.org/10.1109/ivs.2015.7225830) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เปรียบเทียบแบบจำลองจักรยานเชิงจลนศาสตร์และเชิงพลวัตกับข้อมูล เป็นตัวอย่างบันได fidelity ขนาดเล็ก

### LT-028 — The kinematic bicycle model: A consistent model for planning feasible trajectories for autonomous vehicles?

Polack et al. · 2017 · 2017 IEEE Intelligent Vehicles Symposium (IV) · **อ้อม**

[แหล่ง](https://doi.org/10.1109/ivs.2017.7995816) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://polytechnique.hal.science/hal-01520869)

แสดงว่าเมื่อใดแบบจำลองจักรยานเชิงจลนศาสตร์ไม่สอดคล้องกับฟิสิกส์ เป็นข้อเตือนสำหรับ gate fidelity ต่ำ

### LT-029 — A quasi-steady-state minimum lap time simulation of race motorcycles using experimental data

Biniewicz & Pyrz · 2023 · Vehicle System Dynamics · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1080/00423114.2023.2170256) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การจำลองรอบแบบกึ่งคงตัวเทียบกับข้อมูลวัดของรถจักรยานยนต์ เป็นตัวอย่างการตรวจสอบแบบจำลองรอบกับ telemetry

### LT-030 — Simultaneous Optimisation of Vehicle Design and Control for Improving Vehicle Performance and Energy Efficiency Using an Open Source Minimum Lap Time Simulation Framework

Elbal et al. · 2024 · World Electric Vehicle Journal · **ตรง**

[แหล่ง](https://doi.org/10.3390/wevj15080366) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.mdpi.com/2032-6653/15/8/366/pdf?version=1724141770)

framework เวลาต่อรอบต่ำสุดแบบ open source ที่ optimize พารามิเตอร์การออกแบบ การกระจายแรงบิดแบบ active aero แบบ active และการปล่อยพลังงานร่วมกัน เป็น baseline co-optimization ที่ทำซ้ำได้

### LT-031 — Optimising the Performance of a Formula One Car Using a Genetic Algorithm

Wloch & Bentley · 2004 · Lecture Notes in Computer Science · **ตรง**

[แหล่ง](https://doi.org/10.1007/978-3-540-30217-9_71) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

genetic algorithm ปรับพารามิเตอร์ setup 66 ตัวของรถ F1 ภายในเกมจำลองการแข่ง เป็นผลยุคแรกของการออกแบบเชิงวิวัฒนาการในตัวจำลองพร้อมข้อควรระวังเรื่องการขึ้นกับตัวจำลอง

### LT-032 — A Sequential Convex Programming Approach to Free-trajectory Minimum-lap-time Optimization of Racing Cars

Eshof et al. · 2025 · arXiv · **ตรง**

[แหล่ง](https://arxiv.org/abs/2511.13522) · [arXiv:2511.13522](https://arxiv.org/abs/2511.13522) · มี PDF ในเครื่อง: [`papers/07_lap_time_vehicle_dynamics/LT-032_Eshof2025_a-sequential-convex-programming-approach-to-free-t.pdf`](../../../papers/07_lap_time_vehicle_dynamics/LT-032_Eshof2025_a-sequential-convex-programming-approach-to-free-t.pdf)

การ optimize เวลาต่อรอบแบบเส้นแข่งอิสระที่มีประสิทธิภาพล่าสุด เกี่ยวข้องกับต้นทุนการให้ผู้ขับที่ optimize แล้วแก่ทุกผู้สมัคร


## การจัดการพลังงานในการแข่ง สถาปัตยกรรม powertrain และแหล่งเก็บพลังงาน

กลยุทธ์การแข่งที่พลังงานจำกัด การควบคุม powertrain ไฮบริดและไฟฟ้า การสังเคราะห์ topology ของ powertrain และแบบจำลองกับข้อมูลวัดของแบตเตอรี่ flywheel และ supercapacitor สนับสนุนสัญญาการแข่งที่พลังงานต้องพกไป typed energy graph และ onboard energy realization (Work 120)

### EN-001 — Optimal control of Formula One car energy recovery systems

Limebeer et al. · 2014 · International Journal of Control · **ตรง** · แค็ตตาล็อก Work 102 P36

[แหล่ง](https://doi.org/10.1080/00207179.2014.900705) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.anilvrao.com/Publications/JournalPublications/F-1-Optimal-Control-Energy-Recovery.pdf)

การขับเวลาต่ำสุดร่วมกับการจัดตาราง ERS เป็นสูตรของการแข่งที่พลังงานจำกัดและมีการกู้คืนพลังงาน

### EN-002 — Optimal energy management for formula-E cars with regulatory limits and thermal constraints

Liu et al. · 2020 · Applied Energy · **ตรง** · แค็ตตาล็อก Work 102 P37

[แหล่ง](https://doi.org/10.1016/j.apenergy.2020.115805) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://dspace.lib.cranfield.ac.uk/bitstream/1826/15797/1/Optimal_energy_management_for_formula-E_cars_with_regulatory_limits_and_thermal_constraints-2020.pdf)

ขีดจำกัดพลังงานและอุณหภูมิแบตเตอรี่ที่กำหนดการควบคุมตลอดการแข่ง เป็นการเชื่อมพลังงานกับความร้อนตลอด stint

### EN-003 — Time-optimal Control Strategies for a Hybrid Electric Race Car

Ebbesen et al. · 2018 · IEEE Transactions on Control Systems Technology · **ตรง**

[แหล่ง](https://doi.org/10.1109/tcst.2017.2661824) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การจัดการพลังงานเวลาต่ำสุดแบบ convex ของไฮบริดแบบ F1 เป็นตระกูลวิธีหลักของกลยุทธ์เชื้อเพลิงร่วมไฟฟ้า

### EN-004 — Time-Optimal Control Policy for a Hybrid Electric Race Car

Salazar et al. · 2017 · IEEE Transactions on Control Systems Technology · **ตรง**

[แหล่ง](https://doi.org/10.1109/tcst.2016.2642830) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

หาโครงสร้างของนโยบายพลังงานไฮบริดเวลาต่ำสุด ใช้ตรวจความสมเหตุสมผลของกลยุทธ์ที่เรียนรู้หรือค้นหามา

### EN-005 — Time-optimal gearshift and energy management strategies for a hybrid electric race car

Duhr et al. · 2021 · Applied Energy · **ตรง**

[แหล่ง](https://doi.org/10.1016/j.apenergy.2020.115980) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.sciencedirect.com/science/article/pii/S0306261920314288/pdf)

เพิ่มการเลือกเกียร์ในการจัดการพลังงานไฮบริด มีโครงสร้าง mixed-integer คล้ายการเลือกสถาปัตยกรรมแบบไม่ต่อเนื่อง

### EN-006 — Time-optimal low-level control and gearshift strategies for the formula 1 hybrid electric powertrain

Balerna et al. · 2020 · Energies · **ตรง**

[แหล่ง](https://doi.org/10.3390/en14010171) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.mdpi.com/1996-1073/14/1/171/pdf?version=1609831608)

การควบคุมระดับล่างของ power unit F1 รวมถึง turbocharger และ MGU-H เป็นรายละเอียดสำหรับ baseline ไฮบริดแบบเดิม

### EN-007 — Low-level Online Control of the Formula 1 Power Unit with Feedforward Cylinder Deactivation

Neumann et al. · 2023 · IEEE Transactions on Vehicular Technology · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2303.00372) · [arXiv:2303.00372](https://arxiv.org/abs/2303.00372) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-007_Neumann2023_low-level-online-control-of-the-formula-1-power-un.pdf`](../../../papers/08_energy_powertrain/EN-007_Neumann2023_low-level-online-control-of-the-formula-1-power-un.pdf)

การควบคุม power unit F1 แบบออนไลน์ แสดงข้อจำกัดเวลาจริงของกลยุทธ์พลังงาน

### EN-008 — Time-optimal Energy Management of the Formula 1 Power Unit with Active Battery Path Constraints

Duhr et al. · 2021 · 2021 European Control Conference (ECC) · **ตรง**

[แหล่ง](https://doi.org/10.23919/ecc54610.2021.9655192) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

บังคับข้อจำกัดเส้นทางแบตเตอรี่ในการจัดการพลังงาน F1 เวลาต่ำสุด เกี่ยวข้องกับขีดจำกัด state of charge ในสัญญาการแข่ง

### EN-009 — Maximum-distance Race Strategies for a Fully Electric Endurance Race Car

Kampen et al. · 2022 · European Journal of Control · **ตรง**

[แหล่ง](https://arxiv.org/abs/2111.05784) · [arXiv:2111.05784](https://arxiv.org/abs/2111.05784) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-009_Kampen2022_maximum-distance-race-strategies-for-a-fully-elect.pdf`](../../../papers/08_energy_powertrain/EN-009_Kampen2022_maximum-distance-race-strategies-for-a-fully-elect.pdf)

กลยุทธ์ endurance ภายใต้พลังงานคงที่พร้อมการตัดสินใจเข้าพิท เกี่ยวข้องกับการจัดงบพลังงานตลอดการแข่ง

### EN-010 — Optimal Endurance Race Strategies for a Fully Electric Race Car under Thermal Constraints

Kampen et al. · 2023 · IEEE Transactions on Control Systems Technology · **ตรง**

[แหล่ง](https://arxiv.org/abs/2301.08060) · [arXiv:2301.08060](https://arxiv.org/abs/2301.08060) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-010_Kampen2023_optimal-endurance-race-strategies-for-a-fully-elec.pdf`](../../../papers/08_energy_powertrain/EN-010_Kampen2023_optimal-endurance-race-strategies-for-a-fully-elec.pdf)

เพิ่มขีดจำกัดความร้อนของแบตเตอรี่และมอเตอร์ในกลยุทธ์ endurance เป็นการเชื่อม gate ความร้อนกับพลังงานของเราโดยตรง

### EN-011 — Human-in-the-loop Energy and Thermal Management for Electric Racing Cars through Optimization-based Control

Eshof et al. · 2024 · European Journal of Control · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2412.15379) · [arXiv:2412.15379](https://arxiv.org/abs/2412.15379) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-011_Eshof2024_human-in-the-loop-energy-and-thermal-management-fo.pdf`](../../../papers/08_energy_powertrain/EN-011_Eshof2024_human-in-the-loop-energy-and-thermal-management-fo.pdf)

คำแนะนำด้านพลังงานและความร้อนจากการ optimize ส่งให้ผู้ขับมนุษย์ เกี่ยวข้องกับการที่ผู้ขับจริงทำตามกลยุทธ์ที่เหมาะที่สุด

### EN-012 — Battery model impact on time-optimal co-design for electric racing cars: review and application

Riva et al. · 2023 · IEEE Transactions on Transportation Electrification · **ตรง**

[แหล่ง](https://arxiv.org/abs/2312.17003) · [arXiv:2312.17003](https://arxiv.org/abs/2312.17003) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-012_Riva2023_battery-model-impact-on-time-optimal-co-design-for.pdf`](../../../papers/08_energy_powertrain/EN-012_Riva2023_battery-model-impact-on-time-optimal-co-design-for.pdf)

แสดงว่าการเลือกแบบจำลองแบตเตอรี่เปลี่ยนผล co-design เป็นหลักฐานโดยตรงว่า fidelity ของแหล่งเก็บพลังงานพลิกอันดับสถาปัตยกรรมได้ (H4)

### EN-013 — Minimum Race-Time Planning-Strategy for an Autonomous Electric Racecar

Herrmann et al. · 2020 · 2020 IEEE 23rd International Conference on Intelligent Transportation Systems (ITSC) · **ตรง**

[แหล่ง](https://arxiv.org/abs/2005.07127) · [arXiv:2005.07127](https://arxiv.org/abs/2005.07127) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-013_Herrmann2020_minimum-race-time-planning-strategy-for-an-autonom.pdf`](../../../papers/08_energy_powertrain/EN-013_Herrmann2020_minimum-race-time-planning-strategy-for-an-autonom.pdf)

การวางแผนพลังงานและความร้อนตลอดการแข่งของรถแข่งไฟฟ้าพร้อมเครื่องมือเปิด เป็นการ implement อ้างอิงสาธารณะ

### EN-014 — Review of Optimization Strategies for System-Level Design in Hybrid Electric Vehicles

Silvas et al. · 2017 · IEEE Transactions on Vehicular Technology · **ตรง**

[แหล่ง](https://doi.org/10.1109/tvt.2016.2547897) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://research.tue.nl/en/publications/69ba1672-e399-42f9-a7f4-f3633784ffb8)

จำแนก co-design ของ topology เทคโนโลยี ขนาด และการควบคุมของไฮบริด เป็นศัพท์สำหรับการค้นหา topology ของ powertrain ของเรา

### EN-015 — Topology Generation for Hybrid Electric Vehicle Architecture Design

Bayrak et al. · 2016 · Journal of Mechanical Design · **ตรง**

[แหล่ง](https://doi.org/10.1115/1.4033656) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แจกแจง topology ของ powertrain ไฮบริดที่เป็นไปได้จากชิ้นส่วนและกฎการเชื่อม เทียบได้โดยตรงกับการสร้าง topology แบบ typed graph

### EN-016 — Joint Design and Control of Electric Vehicle Propulsion Systems

Verbruggen et al. · 2020 · 2020 European Control Conference (ECC) · **ตรง**

[แหล่ง](https://doi.org/10.23919/ecc51009.2020.9143869) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-016_Verbruggen2020_joint-design-and-control-of-electric-vehicle-propu.pdf`](../../../papers/08_energy_powertrain/EN-016_Verbruggen2020_joint-design-and-control-of-electric-vehicle-propu.pdf)

co-design ของชิ้นส่วนขับเคลื่อนไฟฟ้าและการควบคุม เป็นวิธีกำหนดขนาดชิ้นส่วนภายใน topology ที่เลือก

### EN-017 — Python Battery Mathematical Modelling (PyBaMM)

Sulzer et al. · 2021 · Journal of Open Research Software · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.5334/jors.309) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-017_Sulzer2021_python-battery-mathematical-modelling-pybamm.pdf`](../../../papers/08_energy_powertrain/EN-017_Sulzer2021_python-battery-mathematical-modelling-pybamm.pdf)

แพ็กเกจแบบจำลองแบตเตอรี่ที่มีสำเนาอยู่แล้วใน private/materials/sources เป็นเอกสารอ้างอิงของแบบจำลองและชุดพารามิเตอร์

### EN-018 — Review of parameterisation and a novel database (LiionDB) for continuum Li-ion battery models

Wang et al. · 2022 · Progress in Energy · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1088/2516-1083/ac692c) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://iopscience.iop.org/article/10.1088/2516-1083/ac692c/pdf)

พารามิเตอร์จากงานวิจัยที่คัดสรรสำหรับแบบจำลองเซลล์เชิงฟิสิกส์ เป็น paper เบื้องหลังแหล่ง liiondb ส่วนตัวและฟิลด์ที่มา

### EN-019 — Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models

Chen et al. · 2020 · Journal of The Electrochemical Society · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1149/1945-7111/ab9050) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-019_Chen2020_development-of-experimental-techniques-for-paramet.pdf`](../../../papers/08_energy_powertrain/EN-019_Chen2020_development-of-experimental-techniques-for-paramet.pdf)

ชุดพารามิเตอร์ที่วัดจากเซลล์ LG M50 (PyBaMM Chen2020) เป็นข้อมูลเซลล์จริงที่ใช้กับแบบจำลองแบตเตอรี่บนรถได้

### EN-020 — An asymptotic derivation of a single particle model with electrolyte

Marquis et al. · 2019 · Journal of the Electrochemical Society · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1905.12553) · [arXiv:1905.12553](https://arxiv.org/abs/1905.12553) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-020_Marquis2019_an-asymptotic-derivation-of-a-single-particle-mode.pdf`](../../../papers/08_energy_powertrain/EN-020_Marquis2019_an-asymptotic-derivation-of-a-single-particle-mode.pdf)

หา SPMe เป็นการลดรูปแบบควบคุมได้ของแบบจำลอง DFN เป็นขั้นแบตเตอรี่ fidelity ต่ำที่มีหลักการ

### EN-021 — Lithium-ion battery degradation: how to model it

O’Kane et al. · 2022 · Physical Chemistry, Chemical Physics - PCCP · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2112.02037) · [arXiv:2112.02037](https://arxiv.org/abs/2112.02037) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-021_Kane2022_lithium-ion-battery-degradation-how-to-model-it.pdf`](../../../papers/08_energy_powertrain/EN-021_Kane2022_lithium-ion-battery-degradation-how-to-model-it.pdf)

กลไกการเสื่อมที่เชื่อมกันใน PyBaMM เกี่ยวข้องหากแหล่งพลังงานเสื่อมตลอด stint หรือฤดูกาล

### EN-022 — A continuum of physics-based lithium-ion battery models reviewed

Planella et al. · 2022 · Progress in Energy · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2203.16091) · [arXiv:2203.16091](https://arxiv.org/abs/2203.16091) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-022_Planella2022_a-continuum-of-physics-based-lithium-ion-battery-m.pdf`](../../../papers/08_energy_powertrain/EN-022_Planella2022_a-continuum-of-physics-based-lithium-ion-battery-m.pdf)

ทบทวนลำดับชั้นของแบบจำลองเซลล์เชิงฟิสิกส์ เป็นแผนที่การเลือก fidelity ของแบตเตอรี่ต่อ gate

### EN-023 — Parameterization of a Physico-Chemical Model of a Lithium-Ion Battery: I. Determination of Parameters

Ecker et al. · 2015 · Journal of The Electrochemical Society · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1149/2.0551509jes) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-023_Ecker2015_parameterization-of-a-physico-chemical-model-of-a.pdf`](../../../papers/08_energy_powertrain/EN-023_Ecker2015_parameterization-of-a-physico-chemical-model-of-a.pdf)

พารามิเตอร์ที่วัดจากเซลล์ Kokam (PyBaMM Ecker2015) เป็นชุดข้อมูลวัดชุดที่สองสำหรับตรวจทานแบบจำลองแบตเตอรี่

### EN-024 — Modeling of Galvanostatic Charge and Discharge of the Lithium/Polymer/Insertion Cell

Doyle et al. · 1993 · Journal of The Electrochemical Society · **อ้อม**

[แหล่ง](https://doi.org/10.1149/1.2221597) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://iopscience.iop.org/article/10.1149/1.2221597/pdf)

แบบจำลอง Doyle-Fuller-Newman เป็นแบบจำลองเซลล์เชิงฟิสิกส์อ้างอิงที่แบบลดรูปทั้งหมดถูกเทียบด้วย

### EN-025 — A non-academic perspective on the future of lithium-based batteries

Frith et al. · 2023 · Nature Communications · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1038/s41467-023-35933-2) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-025_Frith2023_a-non-academic-perspective-on-the-future-of-lithiu.pdf`](../../../papers/08_energy_powertrain/EN-025_Frith2023_a-non-academic-perspective-on-the-future-of-lithiu.pdf)

ตัวเลขจากภาคอุตสาหกรรมเรื่องความหนาแน่นพลังงานเซลล์และต้นทุนที่ทำได้ เป็นขอบเขตที่สมจริงของผู้สมัครแหล่งเก็บพลังงาน

### EN-026 — Overview of current development in electrical energy storage technologies and the application potential in power system operation

Luo et al. · 2015 · Applied Energy · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1016/j.apenergy.2014.09.081) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.sciencedirect.com/science/article/pii/S0306261914010290/pdf)

ตารางความหนาแน่นพลังงานและกำลัง ประสิทธิภาพ และอายุใช้งานข้ามเทคโนโลยีการเก็บพลังงาน เป็นข้อมูลเข้าของโปรไฟล์พลังงานที่เป็นกลางทางเทคโนโลยี

### EN-027 — Theory of Ragone plots

Christen & Carlen · 2000 · Journal of Power Sources · **ตรง**

[แหล่ง](https://doi.org/10.1016/s0378-7753(00)00474-2) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

หาเส้นแลกเปลี่ยนพลังงานกับกำลังของอุปกรณ์เก็บพลังงาน เป็นกรอบเปรียบเทียบที่ถูกต้องของแบตเตอรี่ flywheel และ supercapacitor ภายใต้งบพลังงานเดียว

### EN-028 — A Review of Flywheel Energy Storage System Technologies and Their Applications

Amiryar & Pullen · 2017 · Applied Sciences · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.3390/app7030286) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.mdpi.com/2076-3417/7/3/286/pdf?version=1489660272)

ข้อมูลพลังงาน กำลัง และการสูญเสียของ flywheel รวมถึง KERS ในมอเตอร์สปอร์ต เป็นข้อมูลเข้าของผู้สมัครแหล่งเก็บพลังงานเชิงกล

### EN-029 — A Comprehensive Review on Supercapacitor Applications and Developments

Şahin et al. · 2022 · Energies · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.3390/en15030674) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.mdpi.com/1996-1073/15/3/674/pdf?version=1642493431)

ข้อมูลสมรรถนะและการใช้งาน supercapacitor เป็นข้อมูลเข้าของผู้สมัครแหล่งเก็บที่กำลังสูงแต่พลังงานต่ำ

### EN-030 — Competitors-Aware Stochastic Lap Strategy Optimisation for Race Hybrid Vehicles

Paparusso et al. · 2022 · IEEE Transactions on Vehicular Technology · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2203.00084) · [arXiv:2203.00084](https://arxiv.org/abs/2203.00084) · มี PDF ในเครื่อง: [`papers/08_energy_powertrain/EN-030_Paparusso2022_competitors-aware-stochastic-lap-strategy-optimisa.pdf`](../../../papers/08_energy_powertrain/EN-030_Paparusso2022_competitors-aware-stochastic-lap-strategy-optimisa.pdf)

กลยุทธ์พลังงานไฮบริดเชิงสุ่มที่คำนึงถึงคู่แข่ง เกี่ยวข้องหากเวลาแข่งขึ้นกับปฏิสัมพันธ์ ไม่ใช่รถคันเดียว

### EN-031 — Modern Electrical Machine Design Optimization: Techniques, Trends, and Best Practices

Bramerdorfer et al. · 2018 · IEEE Transactions on Industrial Electronics · **อ้อม**

[แหล่ง](https://doi.org/10.1109/tie.2018.2801805) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ทบทวนแนวปฏิบัติการ optimize การออกแบบเครื่องจักรไฟฟ้า เป็นแนวทางการกำหนดขนาดหรือสร้างมอเตอร์เป็นชิ้นส่วน


## ยาง แรงเสียดทานของยาง และการระบุพารามิเตอร์ยาง

แบบจำลองแรงยาง พฤติกรรม transient และความร้อน การสึกและการเสื่อม ฟิสิกส์แรงเสียดทานของยาง และการระบุพารามิเตอร์จากข้อมูลทดสอบหรือสนาม ยาง/contact เป็นช่องว่างระดับ A ในการทบทวนของ Work 102 ขณะที่ kernel ปัจจุบันใช้ friction envelope และเส้นทาง slip แบบ tanh

### TY-001 — Tyre Modelling for Use in Vehicle Dynamics Studies

Bakker et al. · 1987 · SAE Technical Paper Series · **ตรง** · แค็ตตาล็อก Work 102 P43

[แหล่ง](https://doi.org/10.4271/870421) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

Magic Formula ฉบับแรก เป็นแบบจำลองแรงแบบ steady-state ที่จะแทน friction envelope ค่าคงที่

### TY-002 — Magic Formula Tyre Model with Transient Properties

PACEJKA & BESSELINK · 1997 · Vehicle System Dynamics · **ตรง** · แค็ตตาล็อก Work 102 P44

[แหล่ง](https://doi.org/10.1080/00423119708969658) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เพิ่ม transient แบบ relaxation length ให้ Magic Formula จำเป็นสำหรับการขับแบบ transient ใกล้ขีดจำกัด

### TY-003 — An improved Magic Formula/Swift tyre model that can handle inflation pressure changes

Besselink et al. · 2010 · Vehicle System Dynamics · **ตรง** · แค็ตตาล็อก Work 102 P45

[แหล่ง](https://doi.org/10.1080/00423111003748088) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://pure.tue.nl/ws/files/3139490/Metis245615.pdf)

Magic Formula ที่ขึ้นกับความดันลมยาง (ฐานของ MF 6.1) กำหนดขอบเขตการใช้ได้ของสัมประสิทธิ์ยาง

### TY-004 — TRT: thermo racing tyre a physical model to predict the tyre temperature distribution

Farroni et al. · 2014 · Meccanica · **ตรง** · แค็ตตาล็อก Work 102 P46

[แหล่ง](https://doi.org/10.1007/s11012-013-9821-9) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แบบจำลองความร้อนของยางแข่งเชิงฟิสิกส์ที่เทียบกับ telemetry เป็นสถาปัตยกรรมของ state อุณหภูมิยาง

### TY-005 — Optimal tyre usage for a Formula One car

Tremlett & Limebeer · 2016 · Vehicle System Dynamics · **ตรง** · แค็ตตาล็อก Work 102 P38

[แหล่ง](https://doi.org/10.1080/00423114.2016.1213861) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เชื่อมสถานะความร้อนและการสึกของยางเข้ากับการควบคุมเวลาต่ำสุดตลอด stint เป็นปัญหายางตลอดการแข่ง

### TY-006 — The Formula SAE Tire Test Consortium-Tire Testing and Data Handling

Kasprzak & Gentz · 2006 · SAE Technical Paper Series · **ข้อมูล/ผลที่ใช้ได้** · แค็ตตาล็อก Work 102 P61

[แหล่ง](https://doi.org/10.4271/2006-01-3606) · มี PDF ในเครื่อง: [`papers/09_tyres_friction/TY-006_Kasprzak2006_the-formula-sae-tire-test-consortium-tire-testing.pdf`](../../../papers/09_tyres_friction/TY-006_Kasprzak2006_the-formula-sae-tire-test-consortium-tire-testing.pdf)

วิธีที่ FSAE TTC วัดและแจกจ่ายข้อมูลยาง เป็นแหล่งข้อมูลยางแข่งจริงที่เข้าถึงได้ง่ายที่สุดสำหรับขอใช้

### TY-007 — Theory of rubber friction and contact mechanics

Persson · 2001 · The Journal of Chemical Physics · **อ้อม**

[แหล่ง](https://doi.org/10.1063/1.1388626) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://juser.fz-juelich.de/record/42969/files/6009.pdf)

ทฤษฎีแรงเสียดทานยางแบบ viscoelastic บนผิวขรุขระของ Persson เป็นฟิสิกส์เบื้องหลังการยึดเกาะที่ขึ้นกับความเร็ว อุณหภูมิ และพื้นผิวถนน

### TY-008 — Rubber friction on road surfaces: Experiment and theory for low sliding speeds

Lorenz et al. · 2015 · The Journal of Chemical Physics · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1063/1.4919221) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แรงเสียดทานยางบนผิวถนนที่วัดได้เทียบกับทฤษฎี เป็นข้อมูลว่าแรงเสียดทานจากหลักการพื้นฐานเชื่อได้แค่ไหน

### TY-009 — TMeasy - The Handling Tire Model for All Driving Situations

— · 2013 · **อ้อม**

ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แบบจำลองยางกึ่งฟิสิกส์ที่มีพารามิเตอร์น้อยและตีความได้ เป็นทางเลือก fidelity กลางเมื่อไม่มีข้อมูล Magic Formula ครบ

### TY-010 — Tire Modeling and Friction Estimation

— · 2007 · **อ้อม**

[แหล่ง](https://lucris.lub.lu.se/ws/files/4401399/27004.pdf) · มี PDF ในเครื่อง: [`papers/09_tyres_friction/TY-010_Anon2007_tire-modeling-and-friction-estimation.pdf`](../../../papers/09_tyres_friction/TY-010_Anon2007_tire-modeling-and-friction-estimation.pdf)

วิทยานิพนธ์เรื่องแบบจำลองยางแบบ brush และการประมาณแรงเสียดทาน เป็นฐานทางฟิสิกส์ของพฤติกรรม combined slip

### TY-011 — Bayesian Optimization-based Tire Parameter and Uncertainty Estimation for Real-World Data

Goblirsch et al. · 2025 · 2025 IEEE Intelligent Vehicles Symposium (IV) · **ตรง**

[แหล่ง](https://arxiv.org/abs/2504.20863) · [arXiv:2504.20863](https://arxiv.org/abs/2504.20863) · มี PDF ในเครื่อง: [`papers/09_tyres_friction/TY-011_Goblirsch2025_bayesian-optimization-based-tire-parameter-and-unc.pdf`](../../../papers/09_tyres_friction/TY-011_Goblirsch2025_bayesian-optimization-based-tire-parameter-and-unc.pdf)

ระบุพารามิเตอร์ยางพร้อมความไม่แน่นอนจากข้อมูลรถจริง เกี่ยวข้องโดยตรงกับการสอบเทียบยางพร้อมระบุความไม่แน่นอน

### TY-012 — A State-Space Approach to Modeling Tire Degradation in Formula 1 Racing

Cappello & Hoegh · 2025 · Journal of Sports Analytics · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/2512.00640) · [arXiv:2512.00640](https://arxiv.org/abs/2512.00640) · มี PDF ในเครื่อง: [`papers/09_tyres_friction/TY-012_Cappello2025_a-state-space-approach-to-modeling-tire-degradatio.pdf`](../../../papers/09_tyres_friction/TY-012_Cappello2025_a-state-space-approach-to-modeling-tire-degradatio.pdf)

การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง

### TY-013 — Extended Pacejka Tire Model for Enhanced Vehicle

Singh & Sivaramakrishnan · 2023 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2305.18422) · [arXiv:2305.18422](https://arxiv.org/abs/2305.18422) · มี PDF ในเครื่อง: [`papers/09_tyres_friction/TY-013_Singh2023_extended-pacejka-tire-model-for-enhanced-vehicle.pdf`](../../../papers/09_tyres_friction/TY-013_Singh2023_extended-pacejka-tire-model-for-enhanced-vehicle.pdf)

ขยายแบบจำลอง Pacejka ด้วยผลเพิ่มเติมสำหรับการจำลองรถ เป็นตัวเทียบของการขยายแบบจำลองยาง

### TY-014 — TRIP-ID: A tool for a smart and interactive identification of Magic Formula tyre model parameters from experimental data acquired on track

Farroni et al. · 2019 · Mechanical Systems and Signal Processing · **อ้อม**

[แหล่ง](https://doi.org/10.1016/j.ymssp.2017.07.025) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ระบุพารามิเตอร์ Magic Formula จากข้อมูลบนสนามแทนแท่นทดสอบ เป็นเส้นทางที่ใช้ได้จริงเมื่อไม่มีข้อมูลแท่นทดสอบ

### TY-015 — Tyre wear model: Validation and sensitivity analysis

Braghin et al. · 2006 · Meccanica · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s11012-005-1058-9) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แบบจำลองการสึกของยางเชิงฟิสิกส์พร้อมการตรวจสอบ เป็นจุดเริ่มของ state การสึกตลอดการแข่ง

### TY-016 — Estimation of tire-road friction coefficient and its application in chassis control systems

Singh & Taheri · 2015 · Systems Science &amp; Control Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1080/21642583.2014.985804) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://doi.org/10.1080/21642583.2014.985804)

ทบทวนการประมาณสัมประสิทธิ์แรงเสียดทานยาง-ถนน เกี่ยวข้องกับขอบเขตความไม่แน่นอนของแรงเสียดทานบนสนาม held-out

### TY-017 — Tire multiphysical modeling for the analysis of thermal and wear sensitivity on vehicle objective dynamics and racing performances

Farroni & Sakhnevych · 2022 · Simulation Modelling Practice and Theory · **ตรง**

[แหล่ง](https://doi.org/10.1016/j.simpat.2022.102517) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เชื่อมแบบจำลองความร้อนและการสึกของยางกับพลวัตรถและสมรรถนะต่อรอบ เป็นตัวประเมินยางหลายฟิสิกส์ที่โครงการยังขาด


## อากาศพลศาสตร์ การตรวจสอบ CFD ชุดข้อมูล aero และ neural surrogate

กลไกอากาศพลศาสตร์ของรถแข่ง (ground effect ล้อ wake) กรณี CFD ที่ยึดกับการทดลอง การ optimize รูปทรงแบบ adjoint ชุดข้อมูล CFD ยานยนต์แบบเปิด และ neural surrogate พร้อมข้อจำกัดนอกการกระจายข้อมูล aero เป็นช่องว่างระดับ A/B เพราะยังไม่มีเส้นทางจากเรขาคณิตสู่แผนที่ aero ที่ตรวจสอบแล้ว

### AE-001 — Aerodynamics of Race Cars

Katz · 2006 · Annual Review of Fluid Mechanics · **ตรง** · แค็ตตาล็อก Work 102 P47

[แหล่ง](https://doi.org/10.1146/annurev.fluid.38.050304.092016) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ทบทวนกลไก aero ของรถแข่ง ground effect และปฏิสัมพันธ์ระหว่างชิ้นส่วน บอกว่าแบบจำลอง aero ต้องจับผลเชิงเหตุใดบ้าง

### AE-002 — Spectral/hp element simulation of flow past a Formula One front wing: validation against experiments

Buscariolo et al. · 2019 · Journal of Wind Engineering and Industrial Aerodynamics · **ข้อมูล/ผลที่ใช้ได้** · แค็ตตาล็อก Work 102 P48

[แหล่ง](https://arxiv.org/abs/1909.06701) · [arXiv:1909.06701](https://arxiv.org/abs/1909.06701) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-002_Buscariolo2019_spectral-hp-element-simulation-of-flow-past-a-form.pdf`](../../../papers/10_aerodynamics/AE-002_Buscariolo2019_spectral-hp-element-simulation-of-flow-past-a-form.pdf)

กรณี CFD ปีกหน้า F1 ที่ตรวจสอบกับการทดลองแล้ว เป็น benchmark สาธารณะสำหรับตรวจ solver aero ก่อนใช้กับทั้งคัน

### AE-003 — DAFoam: An Open-Source Adjoint Framework for Multidisciplinary Design Optimization with OpenFOAM

He et al. · 2020 · AIAA Journal · **อ้อม** · แค็ตตาล็อก Work 102 P49

[แหล่ง](https://doi.org/10.2514/1.j058853) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://arc.aiaa.org/doi/pdf/10.2514/1.J058853)

gradient CFD แบบ adjoint สำหรับ optimize รูปทรงบน OpenFOAM เป็นเครื่องมือปรับ aero เฉพาะที่ภายใน topology ที่ผ่านแล้ว

### AE-004 — Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design

Palacios et al. · 2013 · 51st AIAA Aerospace Sciences Meeting including the New Horizons Forum and Aerospace Exposition · **อ้อม** · แค็ตตาล็อก Work 102 P50

[แหล่ง](https://doi.org/10.2514/6.2013-287) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-004_Palacios2013_stanford-university-unstructured-su2-an-open-sourc.pdf`](../../../papers/10_aerodynamics/AE-004_Palacios2013_stanford-university-unstructured-su2-an-open-sourc.pdf)

ชุด CFD และการออกแบบ adjoint แบบเปิด เป็น solver ตัวที่สองที่อิสระสำหรับตรวจทาน aero

### AE-005 — DrivAerNet: A Parametric Car Dataset for Data-Driven Aerodynamic Design and Prediction

Elrefaie et al. · 2024 · Design Automation Conference · **ข้อมูล/ผลที่ใช้ได้** · แค็ตตาล็อก Work 102 P51

[แหล่ง](https://arxiv.org/abs/2403.08055) · [arXiv:2403.08055](https://arxiv.org/abs/2403.08055) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-005_Elrefaie2024_drivaernet-a-parametric-car-dataset-for-data-drive.pdf`](../../../papers/10_aerodynamics/AE-005_Elrefaie2024_drivaernet-a-parametric-car-dataset-for-data-drive.pdf)

ผล CFD รถแบบพารามิเตอร์หลายพันชุด เป็นข้อมูลฝึก/ตรวจสอบ surrogate แรงต้าน จำกัดที่รูปทรงรถถนน

### AE-006 — DrivAerNet++: A Large-Scale Multimodal Car Dataset with Computational Fluid Dynamics Simulations and Deep Learning Benchmarks

Elrefaie et al. · 2024 · Neural Information Processing Systems · **ข้อมูล/ผลที่ใช้ได้** · แค็ตตาล็อก Work 102 P52

[แหล่ง](https://arxiv.org/abs/2406.09624) · [arXiv:2406.09624](https://arxiv.org/abs/2406.09624) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-006_Elrefaie2024_drivaernet-a-large-scale-multimodal-car-dataset-wi.pdf`](../../../papers/10_aerodynamics/AE-006_Elrefaie2024_drivaernet-a-large-scale-multimodal-car-dataset-wi.pdf)

กรณี CFD รถหลายรูปแบบกว่า 8,000 กรณีพร้อม benchmark เป็นชุดข้อมูล aero ยานยนต์แบบเปิดที่ใหญ่ที่สุด

### AE-007 — CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics

Elrefaie et al. · 2025 · arXiv.org · **ตรง** · แค็ตตาล็อก Work 102 P53

[แหล่ง](https://arxiv.org/abs/2512.07847) · [arXiv:2512.07847](https://arxiv.org/abs/2512.07847) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-007_Elrefaie2025_carbench-a-comprehensive-benchmark-for-neural-surr.pdf`](../../../papers/10_aerodynamics/AE-007_Elrefaie2025_carbench-a-comprehensive-benchmark-for-neural-surr.pdf)

benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้

### AE-008 — DrivAerML: High-Fidelity Computational Fluid Dynamics Dataset for Road-Car External Aerodynamics

Ashton et al. · 2024 · arXiv.org · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/2408.11969) · [arXiv:2408.11969](https://arxiv.org/abs/2408.11969) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-008_Ashton2024_drivaerml-high-fidelity-computational-fluid-dynami.pdf`](../../../papers/10_aerodynamics/AE-008_Ashton2024_drivaerml-high-fidelity-computational-fluid-dynami.pdf)

DrivAer 500 แบบด้วย hybrid RANS-LES ที่ 160 ล้าน cell สัญญาอนุญาตเปิด เป็นข้อมูลอ้างอิง fidelity สูงสำหรับตรวจสอบ surrogate

### AE-009 — AhmedML: High-Fidelity Computational Fluid Dynamics Dataset for Incompressible, Low-Speed Bluff Body Aerodynamics

Ashton et al. · 2024 · arXiv.org · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/2407.20801) · [arXiv:2407.20801](https://arxiv.org/abs/2407.20801) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-009_Ashton2024_ahmedml-high-fidelity-computational-fluid-dynamics.pdf`](../../../papers/10_aerodynamics/AE-009_Ashton2024_ahmedml-high-fidelity-computational-fluid-dynamics.pdf)

Ahmed body 500 แบบด้วย hybrid RANS-LES เป็น benchmark วัตถุทื่อที่ง่ายกว่าสำหรับทดสอบไปป์ไลน์ aero

### AE-010 — WindsorML: High-Fidelity Computational Fluid Dynamics Dataset For Automotive Aerodynamics

Ashton et al. · 2024 · Neural Information Processing Systems · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/2407.19320) · [arXiv:2407.19320](https://arxiv.org/abs/2407.19320) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-010_Ashton2024_windsorml-high-fidelity-computational-fluid-dynami.pdf`](../../../papers/10_aerodynamics/AE-010_Ashton2024_windsorml-high-fidelity-computational-fluid-dynami.pdf)

LES แบบ wall-modelled ของ Windsor body หลายแบบ (CC-BY-SA) เป็นข้อมูล fidelity สูงแบบเปิดที่รวมผลใกล้พื้น

### AE-011 — Ground Effect Aerodynamics of Race Cars

Zhang et al. · 2006 · Applied Mechanics Reviews · **ตรง**

[แหล่ง](https://doi.org/10.1115/1.2110263) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-011_Zhang2006_ground-effect-aerodynamics-of-race-cars.pdf`](../../../papers/10_aerodynamics/AE-011_Zhang2006_ground-effect-aerodynamics-of-race-cars.pdf)

ทบทวนปีก diffuser และล้อใน ground effect พร้อมข้อมูลการทดลอง เป็นฟิสิกส์ของ downforce ที่ขึ้นกับความสูงตัวถัง

### AE-012 — Aerodynamics of a single element wing in ground effect

Zerihan & Zhang · 2000 · 38th Aerospace Sciences Meeting and Exhibit · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.2514/6.2000-650) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ผลวัดในอุโมงค์ลมของปีกกลับหัวตามระยะจากพื้น รวมถึงแรงที่ลดลงเมื่อใกล้พื้นมาก เป็นข้อมูลตรวจสอบแบบจำลอง ground effect

### AE-013 — A Computational Study of the Flow Around an Isolated Wheel in Contact With the Ground

McManus & Zhang · 2006 · Journal of Fluids Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1115/1.2175158) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

CFD ของล้อหมุนบนพื้นเทียบกับการทดลอง เกี่ยวข้องกับจุดสัมผัสพื้นที่เปิดโล่ง

### AE-014 — The effects of simplifications on isolated wheel aerodynamics

Diasinos et al. · 2015 · Journal of Wind Engineering and Industrial Aerodynamics · **อ้อม**

[แหล่ง](https://doi.org/10.1016/j.jweia.2015.08.004) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1151&context=aero_fac)

วัดว่าการลดรายละเอียดเรขาคณิตเปลี่ยน aero ของล้ออย่างไร เป็นแนวทางว่าเส้นทางเรขาคณิตสู่ aero ต้องเก็บรายละเอียดใด

### AE-015 — CFD Investigation of the Effect of the Salient Flow Features in the Wake of a Generic Open-Wheel Race Car

Newbon et al. · 2017 · SAE International Journal of Passenger Cars - Mechanical Systems · **อ้อม**

[แหล่ง](https://doi.org/10.4271/2015-01-1539) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://nrl.northumbria.ac.uk/id/eprint/25043/1/SAE%202015-01-1539_PrePublication_Dominy-Newbon.pdf)

โครงสร้าง wake ของรถล้อเปิดและผลต่อรถที่ตามหลัง เกี่ยวข้องในภายหลังหากการจราจรและ wake เข้ามาในสภาพการแข่ง

### AE-016 — AB-UPT: Scaling Neural CFD Surrogates for High-Fidelity Automotive Aerodynamics Simulations via Anchored-Branched Universal Physics Transformers

Alkin et al. · 2025 · Trans. Mach. Learn. Res. · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2502.09692) · [arXiv:2502.09692](https://arxiv.org/abs/2502.09692) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-016_Alkin2025_ab-upt-scaling-neural-cfd-surrogates-for-high-fide.pdf`](../../../papers/10_aerodynamics/AE-016_Alkin2025_ab-upt-scaling-neural-cfd-surrogates-for-high-fide.pdf)

ขยาย neural surrogate ไปยัง field รถ fidelity สูงเต็มคัน เป็นสถาปัตยกรรม surrogate ตัวเลือก พร้อมข้อควรระวังนอกการกระจายข้อมูล

### AE-017 — Transolver: A Fast Transformer Solver for PDEs on General Geometries

Wu et al. · 2024 · International Conference on Machine Learning · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2402.02366) · [arXiv:2402.02366](https://arxiv.org/abs/2402.02366) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-017_Wu2024_transolver-a-fast-transformer-solver-for-pdes-on-g.pdf`](../../../papers/10_aerodynamics/AE-017_Wu2024_transolver-a-fast-transformer-solver-for-pdes-on-g.pdf)

transformer แบบ physics-attention สำหรับ PDE บน mesh ใดก็ได้รวมถึงอากาศพลศาสตร์รถ เป็นผู้สมัคร surrogate สำหรับเรขาคณิตทั่วไป

### AE-018 — Geometry-Informed Neural Operator for Large-Scale 3D PDEs

Li et al. · 2023 · Neural Information Processing Systems · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2309.00583) · [arXiv:2309.00583](https://arxiv.org/abs/2309.00583) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-018_Li2023_geometry-informed-neural-operator-for-large-scale.pdf`](../../../papers/10_aerodynamics/AE-018_Li2023_geometry-informed-neural-operator-for-large-scale.pdf)

GINO ทำนายความดันบนผิวรถจากเรขาคณิต เป็นผล neural operator ด้าน aero รถยุคแรกที่ควรทำซ้ำ

### AE-019 — Learning Mesh-Based Simulation with Graph Networks

Pfaff et al. · 2021 · International Conference on Learning Representations · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2010.03409) · [arXiv:2010.03409](https://arxiv.org/abs/2010.03409) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-019_Pfaff2021_learning-mesh-based-simulation-with-graph-networks.pdf`](../../../papers/10_aerodynamics/AE-019_Pfaff2021_learning-mesh-based-simulation-with-graph-networks.pdf)

MeshGraphNets เรียนรู้ฟิสิกส์บน mesh รวมถึงอากาศพลศาสตร์ เป็นฐานของ surrogate เรขาคณิตทั่วไปหลายตัว

### AE-020 — Learning Three-dimensional Flow for Interactive Aerodynamic Design

Umetani & Bickel · 2018 · ACM Transactions on Graphics · **อ้อม**

[แหล่ง](https://doi.org/10.1145/3197517.3201325) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://zenodo.org/record/3495498)

การทำนายการไหล 3 มิติและแรงต้านที่เรียนรู้สำหรับออกแบบรูปทรงรถแบบโต้ตอบ เป็นตัวอย่างยุคแรกของ surrogate ในวงการออกแบบ

### AE-021 — Surrogate Modeling of Car Drag Coefficient with Depth and Normal Renderings

Song et al. · 2023 · Design Automation Conference · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2306.06110) · [arXiv:2306.06110](https://arxiv.org/abs/2306.06110) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-021_Song2023_surrogate-modeling-of-car-drag-coefficient-with-de.pdf`](../../../papers/10_aerodynamics/AE-021_Song2023_surrogate-modeling-of-car-drag-coefficient-with-de.pdf)

surrogate แรงต้านจากภาพพร้อมชุดข้อมูล CFD รถขนาดใหญ่ เป็น surrogate คัดกรองราคาถูกสำหรับเทียบกับ surrogate แบบ field

### AE-022 — Faster by Design: Interactive Aerodynamics via Neural Surrogates Trained on Expert-Validated CFD

Thumiger et al. · 2026 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2604.18491) · [arXiv:2604.18491](https://arxiv.org/abs/2604.18491) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-022_Thumiger2026_faster-by-design-interactive-aerodynamics-via-neur.pdf`](../../../papers/10_aerodynamics/AE-022_Thumiger2026_faster-by-design-interactive-aerodynamics-via-neur.pdf)

neural surrogate ที่ฝึกบน CFD รถแข่งที่ผู้เชี่ยวชาญตรวจแล้ว (รวมถึงรถ LMP2) เป็นการศึกษา surrogate รถแข่งที่ใกล้ที่สุด

### AE-023 — Multi-Granularity Conformal Prediction for Reliable Neural-Operator Automotive Aerodynamic Surrogates

Jia et al. · 2026 · arXiv · **ตรง**

[แหล่ง](https://arxiv.org/abs/2607.17297) · [arXiv:2607.17297](https://arxiv.org/abs/2607.17297) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-023_Jia2026_multi-granularity-conformal-prediction-for-reliabl.pdf`](../../../papers/10_aerodynamics/AE-023_Jia2026_multi-granularity-conformal-prediction-for-reliabl.pdf)

ขอบเขตความไม่แน่นอนแบบ conformal สำหรับ surrogate aero เป็นวิธีแนบ error bar ที่สอบเทียบแล้วให้การเลื่อนระดับที่ใช้ surrogate

### AE-024 — Adapting Automotive Aerodynamics Surrogates to New Vehicle Families via Transfer Learning

Keum & Warey · 2026 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2605.27968) · [arXiv:2605.27968](https://arxiv.org/abs/2605.27968) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-024_Keum2026_adapting-automotive-aerodynamics-surrogates-to-new.pdf`](../../../papers/10_aerodynamics/AE-024_Keum2026_adapting-automotive-aerodynamics-surrogates-to-new.pdf)

วัดความล้มเหลวและการปรับตัวของ surrogate กับตระกูลรถใหม่ เกี่ยวข้องโดยตรงเพราะสถาปัตยกรรมใหม่อยู่นอกการกระจายข้อมูล

### AE-025 — Towards a Foundation-Model Paradigm for Aerodynamic Prediction in Three-dimensional Design

Yang et al. · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2604.18062) · [arXiv:2604.18062](https://arxiv.org/abs/2604.18062) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-025_Yang2026_towards-a-foundation-model-paradigm-for-aerodynami.pdf`](../../../papers/10_aerodynamics/AE-025_Yang2026_towards-a-foundation-model-paradigm-for-aerodynami.pdf)

แนวทาง foundation model สำหรับการทำนาย aero 3 มิติ เป็นบริบทของ surrogate เรขาคณิตทั่วไป

### AE-026 — SMART: Scalable Mesh-free Aerodynamic Simulations from Raw Geometries using a Transformer-based Surrogate Model

Hagnberger & Niepert · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2601.18707) · [arXiv:2601.18707](https://arxiv.org/abs/2601.18707) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-026_Hagnberger2026_smart-scalable-mesh-free-aerodynamic-simulations-f.pdf`](../../../papers/10_aerodynamics/AE-026_Hagnberger2026_smart-scalable-mesh-free-aerodynamic-simulations-f.pdf)

surrogate ที่ไม่ต้องใช้ mesh จากเรขาคณิตดิบ ข้ามขั้น meshing สำหรับการคัดกรองขั้นแรก

### AE-027 — AirfRANS: High Fidelity Computational Fluid Dynamics Dataset for Approximating Reynolds-Averaged Navier-Stokes Solutions

Bonnet et al. · 2022 · Neural Information Processing Systems · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/2212.07564) · [arXiv:2212.07564](https://arxiv.org/abs/2212.07564) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-027_Bonnet2022_airfrans-high-fidelity-computational-fluid-dynamic.pdf`](../../../papers/10_aerodynamics/AE-027_Bonnet2022_airfrans-high-fidelity-computational-fluid-dynamic.pdf)

ชุดข้อมูล RANS ของ airfoil พร้อมตัวชี้วัดความสอดคล้องทางฟิสิกส์ เกี่ยวข้องกับ surrogate ของชิ้นปีกและการประเมินความสอดคล้องทางฟิสิกส์

### AE-028 — Adjoint methods for car aerodynamics

Othmer · 2014 · Journal of Mathematics in Industry · **ตรง**

[แหล่ง](https://doi.org/10.1186/2190-5983-4-6) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-028_Othmer2014_adjoint-methods-for-car-aerodynamics.pdf`](../../../papers/10_aerodynamics/AE-028_Othmer2014_adjoint-methods-for-car-aerodynamics.pdf)

การ optimize รูปทรงและ topology ด้าน aero ของรถแบบ adjoint ในอุตสาหกรรม เป็นวิธีปรับ aero เฉพาะที่ของตัวถังที่ผ่านแล้ว

### AE-029 — Introduction of a New Realistic Generic Car Model for Aerodynamic Investigations

Heft et al. · 2012 · SAE Technical Paper Series · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.4271/2012-01-0168) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เรขาคณิตอ้างอิง DrivAer และข้อมูลการทดลอง เป็นฐานของ DrivAerNet/DrivAerML

### AE-030 — Some Salient Features Of The Time-Averaged Ground Vehicle Wake

Ahmed et al. · 1984 · SAE Technical Paper Series · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.4271/840300) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การทดลอง Ahmed body พร้อมแรงต้านตามมุมลาด เป็นกรณีตรวจสอบคลาสสิกของ CFD wake ยานพาหนะ

### AE-031 — Improved two-equation k-omega turbulence models for aerodynamic flows

Menter · 1992 · 23rd Fluid Dynamics, Plasmadynamics, and Lasers Conference · **อ้อม**

[แหล่ง](https://doi.org/10.2514/6.1993-2906) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

รายงานแบบจำลอง SST ของ Menter เป็นแบบจำลองความปั่นป่วนที่ RANS รถแข่งส่วนใหญ่ใช้ พร้อมข้อจำกัดที่ทราบในการแยกตัวของการไหล

### AE-032 — Experimental study of the vortex system generated by a Formula 1 front wing

— · 2006 · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://spiral.imperial.ac.uk/entities/publication/001dea4e-b1e9-490a-8daf-cc80fd398e38) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

วิทยานิพนธ์ที่วัด vortex ของปีกหน้า F1 อย่างละเอียด เป็นข้อมูลการทดลองสำหรับตรวจสอบการทำนาย wake ของปีก

### AE-033 — Fourier Neural Operator for Parametric Partial Differential Equations

Li et al. · 2021 · International Conference on Learning Representations · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2010.08895) · [arXiv:2010.08895](https://arxiv.org/abs/2010.08895) · มี PDF ในเครื่อง: [`papers/10_aerodynamics/AE-033_Li2021_fourier-neural-operator-for-parametric-partial-dif.pdf`](../../../papers/10_aerodynamics/AE-033_Li2021_fourier-neural-operator-for-parametric-partial-dif.pdf)

neural operator ที่เรียนรู้การแปลงคำตอบของ PDE เป็นสถาปัตยกรรมฐานของ surrogate การไหลหลายตัว


## การจัดการความร้อน การเกิดความร้อน และการออกแบบการระบายความร้อน

แบบจำลองการเกิดความร้อนและเครือข่ายความร้อนของแบตเตอรี่และเครื่องจักรไฟฟ้า และการออกแบบการระบายความร้อนระดับเรขาคณิต สนับสนุนงานฟิสิกส์ความร้อนแบบ lumped, thermal-solid แบบเชื่อมโยง และ flow/heat exchange (Works 014, 115, 121)

### TH-001 — A General Energy Balance for Battery Systems

Bernardi et al. · 1985 · Journal of The Electrochemical Society · **ตรง**

[แหล่ง](https://doi.org/10.1149/1.2113792) · มี PDF ในเครื่อง: [`papers/11_thermal_cooling/TH-001_Bernardi1985_a-general-energy-balance-for-battery-systems.pdf`](../../../papers/11_thermal_cooling/TH-001_Bernardi1985_a-general-energy-balance-for-battery-systems.pdf)

สมการการเกิดความร้อนของแบตเตอรี่ของ Bernardi (ความร้อนไม่ผันกลับบวกความร้อนเชิง entropy) เป็นเทอมแหล่งของ state ความร้อนแบตเตอรี่ใด ๆ

### TH-002 — Lumped-parameter electro-thermal model for cylindrical batteries

Lin et al. · 2014 · Journal of Power Sources · **ตรง**

[แหล่ง](https://doi.org/10.1016/j.jpowsour.2014.01.097) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แบบจำลองความร้อนสองสถานะแกน/ผิวที่ระบุจากข้อมูล เป็น fidelity ที่เหมาะกับอุณหภูมิแบตเตอรี่ตลอดการแข่ง

### TH-003 — Evolution and Modern Approaches for Thermal Analysis of Electrical Machines

Boglietti et al. · 2009 · IEEE Transactions on Industrial Electronics · **ตรง**

[แหล่ง](https://doi.org/10.1109/tie.2008.2011622) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://iris.polito.it/bitstream/11583/1938008/1/1938008.pdf)

ทบทวนเครือข่ายความร้อนแบบ lumped และ CFD ของเครื่องจักรไฟฟ้า เป็นฐานของการลดกำลังมอเตอร์ในแบบจำลอง powertrain

### TH-004 — Large scale three-dimensional topology optimisation of heat sinks cooled by natural convection

Alexandersen et al. · 2016 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1508.04596) · [arXiv:1508.04596](https://arxiv.org/abs/1508.04596) · มี PDF ในเครื่อง: [`papers/11_thermal_cooling/TH-004_Alexandersen2016_large-scale-three-dimensional-topology-optimisatio.pdf`](../../../papers/11_thermal_cooling/TH-004_Alexandersen2016_large-scale-three-dimensional-topology-optimisatio.pdf)

topology optimization การถ่ายเทความร้อนร่วม 3 มิติเต็มรูปแบบที่ได้ heat sink ไม่คุ้นตา เป็นงานก่อนหน้าของเรขาคณิตระบายความร้อนที่ค้นพบ

### TH-005 — A review about the engineering design of optimal heat transfer systems using topology optimization

Dbouk · 2017 · Applied Thermal Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1016/j.applthermaleng.2016.10.134) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ทบทวน topology optimization ของอุปกรณ์ถ่ายเทความร้อน เป็นแผนที่วิธีสำหรับการค้นพบเส้นทางระบายความร้อน

### TH-006 — Analysis of heat conduction in a disk brake system

Talati & Jalalifar · 2009 · Heat and Mass Transfer · **อ้อม**

[แหล่ง](https://doi.org/10.1007/s00231-009-0476-y) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การนำความร้อนแบบ transient ในจานเบรก เกี่ยวข้องกับขีดจำกัดความร้อนของเบรกและพลังงานที่เบรกเสียดทานสลายไป


## วัสดุ ข้อมูลวัสดุ ตัวยึดและข้อต่อ โครงสร้างรับการชน การผลิต และพิกัดความเผื่อ

แหล่งที่มาของพฤติกรรมวัสดุและข้อต่อจริง และการที่การผลิตกับพิกัดความเผื่อจำกัดการออกแบบ โครงการเลือกเฉพาะวัสดุในแค็ตตาล็อก (ไม่ออกแบบส่วนผสมใหม่) และค่าวัสดุจริงอยู่ใน private/ ตามนโยบายข้อมูลวัสดุ

### MA-001 — On the engineering properties of materials

— · 1989 · **ตรง**

ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แผนภูมิสมบัติวัสดุและดัชนีสมรรถนะของ Ashby เป็นวิธีที่มีหลักการในการเลือกวัสดุในแค็ตตาล็อกตามหน้าที่

### MA-002 — Commentary: The Materials Project: A materials genome approach to accelerating materials innovation

Jain et al. · 2013 · APL Materials · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1063/1.4812323) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://aip.scitation.org/doi/pdf/10.1063/1.4812323)

ฐานข้อมูลวัสดุที่คำนวณแบบเปิด เป็นบริบทและแหล่งที่อาจใช้สำหรับสมบัติระดับธาตุ ไม่ใช่ค่าที่ยอมให้ทางวิศวกรรม

### MA-003 — Exploration of data science techniques to predict fatigue strength of steel from composition and processing parameters

Agrawal et al. · 2014 · Integrating Materials and Manufacturing Innovation · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1186/2193-9772-3-8) · มี PDF ในเครื่อง: [`papers/12_materials_joints_manufacturing/MA-003_Agrawal2014_exploration-of-data-science-techniques-to-predict.pdf`](../../../papers/12_materials_joints_manufacturing/MA-003_Agrawal2014_exploration-of-data-science-techniques-to-predict.pdf)

ใช้ชุดข้อมูลความล้าของเหล็กจาก NIMS พร้อมส่วนผสมและกระบวนการ เป็นแหล่งข้อมูลความล้าแบบเปิดและตัวอย่างข้อจำกัดของข้อมูล

### MA-004 — New Criteria for Self-Loosening of Fasteners Under Vibration

Junker · 1969 · SAE Technical Paper Series · **ตรง**

[แหล่ง](https://doi.org/10.4271/690055) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

กลไกการคลายตัวจากการสั่นตามขวางของ Junker เป็นฟิสิกส์ที่ gate ข้อต่อสลักเกลียวต้องจัดการ

### MA-005 — Three-dimensional finite element analysis of tightening and loosening mechanism of threaded fastener

Izumi et al. · 2005 · Engineering Failure Analysis · **ตรง**

[แหล่ง](https://doi.org/10.1016/j.engfailanal.2004.09.009) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

FE 3 มิติของการสัมผัสเกลียวระหว่างขันและคลาย เป็นเอกสารอ้างอิงการตรวจสอบของ detailed connection contact (Work 113)

### MA-006 — Composite materials technology in formula 1 motor racing

— · 2008 · **ข้อมูล/ผลที่ใช้ได้**

ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

อธิบายโครงสร้างคอมโพสิต กระบวนการ และการพังใน F1 จากวิศวกรของทีม เป็นบริบทของสมมติฐานชิ้นส่วนคอมโพสิต

### MA-007 — Repair of composite structures on Formula 1 race cars

Savage & Oxley · 2010 · Engineering Failure Analysis · **อ้อม**

[แหล่ง](https://doi.org/10.1016/j.engfailanal.2008.11.006) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ความเสียหายและการซ่อมชิ้นส่วนคอมโพสิต F1 เกี่ยวข้องกับสมมติฐานความน่าเชื่อถือและ damage tolerance

### MA-008 — Crash Simulation of an F1 Racing Car Front Impact Structure

— · 2009 · **ตรง**

ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การจำลองการชนแบบ explicit ของจมูกคอมโพสิต F1 เทียบกับการทดสอบรับรอง เป็นแม่แบบของ gate การชนในอนาคต

### MA-009 — A survey of research in the application of tolerance analysis to the design of mechanical assemblies

Chase & Parkinson · 1991 · Research in Engineering Design · **ตรง**

[แหล่ง](https://doi.org/10.1007/bf01580066) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://adcats.et.byu.edu/WWW/RESEARCH/../Publication/91-1/DesRes_w_figs.PDF)

การสะสมพิกัดความเผื่อแบบกรณีเลวร้ายที่สุดเทียบกับเชิงสถิติในการประกอบ เป็นฐานวิธีของ manufacturing tolerance handoff (Work 130)

### MA-010 — A comprehensive review of tolerancing research

Hong & Chang · 2002 · International Journal of Production Research · **อ้อม**

[แหล่ง](https://doi.org/10.1080/00207540210128242) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ทบทวนกว้างเรื่องการแทน การวิเคราะห์ และการสังเคราะห์พิกัดความเผื่อ เป็นบริบทของเรขาคณิตที่คำนึงถึงพิกัดความเผื่อ

### MA-011 — Design for additive manufacturing: Trends, opportunities, considerations, and constraints

Thompson et al. · 2016 · CIRP Annals · **อ้อม**

[แหล่ง](https://doi.org/10.1016/j.cirp.2016.05.004) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.sciencedirect.com/science/article/pii/S0007850616301913)

ข้อจำกัดและโอกาสของการผลิตแบบเติมเนื้อ เป็นข้อมูลเข้าของภาษาการผลิตที่ประกาศไว้

### MA-012 — Scaling deep learning for materials discovery

Merchant et al. · 2023 · Nature · **ตรง**

[แหล่ง](https://doi.org/10.1038/s41586-023-06735-9) · มี PDF ในเครื่อง: [`papers/12_materials_joints_manufacturing/MA-012_Merchant2023_scaling-deep-learning-for-materials-discovery.pdf`](../../../papers/12_materials_joints_manufacturing/MA-012_Merchant2023_scaling-deep-learning-for-materials-discovery.pdf)

claim การค้นพบขนาดใหญ่ของ GNoME ใช้คู่กับ MA-013 เป็นกรณีศึกษาของการโต้แย้ง claim การค้นพบ

### MA-013 — Artificial Intelligence Driving Materials Discovery? Perspective on the Article: Scaling Deep Learning for Materials Discovery

Cheetham & Seshadri · 2024 · Chemistry of Materials · **ตรง**

[แหล่ง](https://doi.org/10.1021/acs.chemmater.4c00643) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://doi.org/10.1021/acs.chemmater.4c00643)

บทวิจารณ์ที่แสดงว่าวัสดุที่ 'ค้นพบ' จำนวนมากไม่ใหม่ ไม่มีประโยชน์ หรือไม่น่าเชื่อ เป็นแบบของการแยก generated, validated และ discovered ของเรา

### MA-014 — A statistical distribution function of wide applicability

Weibull · 1951 · Journal of Applied Mechanics · **อ้อม**

[แหล่ง](https://doi.org/10.1115/1.4010337) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การกระจายแบบ Weibull สำหรับการกระจายของความแข็งแรง เกี่ยวข้องกับการพังเชิงความน่าจะเป็นของชิ้นส่วนเปราะและคอมโพสิต

### MA-015 — A comparison of the predictive capabilities of current failure theories for composite laminates, judged against experimental evidence

Hinton et al. · 2002 · Composites Science and Technology · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://doi.org/10.1016/s0266-3538(02)00125-2) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

World-Wide Failure Exercise: ทฤษฎีการพังของคอมโพสิตถูกให้คะแนนแบบปิดตาเทียบกับการทดลอง เป็นหลักฐานว่าการทำนายการพังของคอมโพสิตไม่แน่นอนเพียงใด


## Verification, validation, การสอบเทียบ สถิติ การทำซ้ำได้ และวินัยในการอ้างผล

วิธีแสดงว่า solver แก้สมการของตัวเองได้ถูก วิธีแสดงว่าแบบจำลองทำนายความจริงได้ วิธีเปรียบเทียบวิธีค้นหาเชิงสุ่มอย่างซื่อตรง และวิธีที่ optimizer ใช้ช่องโหว่ของวัตถุประสงค์และตัวจำลอง เป็นรากฐานของระดับหลักฐาน fidelity gate และวินัยการรีวิวใน AGENTS.md

### VV-001 — Verification and Validation in Computational Fluid Dynamics

OBERKAMPF & TRUCANO · 2002 · **ตรง** · แค็ตตาล็อก Work 102 P59

[แหล่ง](https://doi.org/10.2172/793406) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.osti.gov/servlets/purl/793406)

แยก verification (แก้สมการถูก) ออกจาก validation (สมการถูก) เป็นรากฐานของภาษาระดับหลักฐานของโครงการ

### VV-002 — Bayesian calibration of computer models

Kennedy & O'Hagan · 2001 · Journal of the Royal Statistical Society Series B: Statistical Methodology · **ตรง** · แค็ตตาล็อก Work 102 P58

[แหล่ง](https://doi.org/10.1111/1467-9868.00294) · [arXiv:2006.07546](https://arxiv.org/abs/2006.07546) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-002_Kennedy2001_bayesian-calibration-of-computer-models.pdf`](../../../papers/13_validation_statistics_claims/VV-002_Kennedy2001_bayesian-calibration-of-computer-models.pdf)

การสอบเทียบของ Kennedy-O'Hagan ที่มีเทอมความคลาดเคลื่อนของแบบจำลองชัดเจน เป็นแผนการสอบเทียบระบบย่อยกับการวัด

### VV-003 — Deep Reinforcement Learning at the Edge of the Statistical Precipice

Agarwal et al. · 2021 · Neural Information Processing Systems · **ตรง** · แค็ตตาล็อก Work 102 P60

[แหล่ง](https://arxiv.org/abs/2108.13264) · [arXiv:2108.13264](https://arxiv.org/abs/2108.13264) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-003_Agarwal2021_deep-reinforcement-learning-at-the-edge-of-the-sta.pdf`](../../../papers/13_validation_statistics_claims/VV-003_Agarwal2021_deep-reinforcement-learning-at-the-edge-of-the-sta.pdf)

การประมาณช่วงและค่ารวมที่ทนทานสำหรับการเทียบที่มีจำนวนรันน้อย เป็นมาตรฐานการรายงานของแคมเปญค้นหาที่จำนวน seed จำกัด

### VV-004 — Code Verification by the Method of Manufactured Solutions

SALARI & KNUPP · 2000 · **ตรง**

[แหล่ง](https://doi.org/10.2172/759450) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.osti.gov/servlets/purl/759450)

manufactured solution สำหรับตรวจอันดับความแม่นยำของโค้ด PDE เป็นวิธีตรวจ solver อย่างอิสระ (Work 138)

### VV-005 — A comprehensive framework for verification, validation, and uncertainty quantification in scientific computing

Roy & Oberkampf · 2011 · Computer Methods in Applied Mechanics and Engineering · **ตรง**

[แหล่ง](https://doi.org/10.1016/j.cma.2011.03.016) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

กรอบ VVUQ ครบวงจรรวมถึงความไม่แน่นอนเชิงตัวเลข ข้อมูลเข้า และรูปแบบแบบจำลอง เป็นโครงสร้างของหลักฐานการเลื่อน fidelity

### VV-006 — Procedure for Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications

Celik et al. · 2008 · Journal of Fluids Engineering · **ตรง**

[แหล่ง](https://doi.org/10.1115/1.2960953) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://asmedigitalcollection.asme.org/fluidsengineering/article-pdf/130/7/078001/5491455/078001_1.pdf)

ขั้นตอน grid convergence index ที่ใช้การปรับละเอียดสามระดับ เป็นกฎการรายงาน claim การลู่เข้าของ mesh

### VV-007 — Perspective: A Method for Uniform Reporting of Grid Refinement Studies

Roache · 1994 · Journal of Fluids Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1115/1.2910291) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

grid convergence index ต้นฉบับของ Roache เป็นพื้นหลังของ VV-006

### VV-008 — Verification, validation, and predictive capability in computational engineering and physics

Oberkampf et al. · 2004 · Applied Mechanics Reviews · **ตรง**

[แหล่ง](https://doi.org/10.1115/1.1767847) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-008_Oberkampf2004_verification-validation-and-predictive-capability.pdf`](../../../papers/13_validation_statistics_claims/VV-008_Oberkampf2004_verification-validation-and-predictive-capability.pdf)

นิยามความสามารถในการทำนายนอกเงื่อนไขที่ตรวจสอบแล้ว เกี่ยวข้องกับการขยายผลไปยังสถาปัตยกรรมใหม่

### VV-009 — Verification and validation of simulation models

Sargent · 2010 · Proceedings of the 2010 Winter Simulation Conference · **อ้อม**

[แหล่ง](https://doi.org/10.1109/wsc.2010.5679166) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://repository.lib.ncsu.edu/bitstream/1840.4/5093/1/1994_0012.pdf)

เทคนิค validation เชิงปฏิบัติของแบบจำลองการจำลอง เป็นการตรวจที่ใช้ได้จริงกับการจำลองการแข่งเอง

### VV-010 — Combining field data and computer simulations for calibration and prediction

Higdon et al. · 2004 · SIAM Journal on Scientific Computing · **อ้อม**

[แหล่ง](https://doi.org/10.1137/s1064827503426693) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การสอบเทียบแบบ Bayesian ที่ใช้ได้จริงกับข้อมูลภาคสนามและความคลาดเคลื่อน เป็นรายละเอียดการ implement ของ VV-002

### VV-011 — Learning about physical parameters: the importance of model discrepancy

Brynjarsdóttir & OʼHagan · 2014 · Inverse Problems · **ตรง**

[แหล่ง](https://doi.org/10.1088/0266-5611/30/11/114007) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://iopscience.iop.org/article/10.1088/0266-5611/30/11/114007/pdf)

แสดงว่าพารามิเตอร์ที่สอบเทียบจะผิดหากไม่จำลองความคลาดเคลื่อนด้วยความรู้ก่อนหน้า เป็นคำเตือนสำหรับการสอบเทียบยางและ aero

### VV-012 — How Many Random Seeds? Statistical Power Analysis in Deep Reinforcement Learning Experiments

Colas et al. · 2018 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/1806.08295) · [arXiv:1806.08295](https://arxiv.org/abs/1806.08295) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-012_Colas2018_how-many-random-seeds-statistical-power-analysis-i.pdf`](../../../papers/13_validation_statistics_claims/VV-012_Colas2018_how-many-random-seeds-statistical-power-analysis-i.pdf)

การวิเคราะห์ power สำหรับเลือกจำนวน seed ใช้ได้โดยตรงกับการกำหนดขนาดแคมเปญค้นหาแบบ paired seed

### VV-013 — Deep Reinforcement Learning that Matters

Henderson et al. · 2018 · AAAI Conference on Artificial Intelligence · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1709.06560) · [arXiv:1709.06560](https://arxiv.org/abs/1709.06560) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-013_Henderson2018_deep-reinforcement-learning-that-matters.pdf`](../../../papers/13_validation_statistics_claims/VV-013_Henderson2018_deep-reinforcement-learning-that-matters.pdf)

แสดงว่า seed การ implement และ hyperparameter พลิกข้อสรุปได้ เป็นเหตุผลของ metadata การ replay ครบถ้วน

### VV-014 — Statistical Comparisons of Classifiers over Multiple Data Sets

— · 2006 · **อ้อม**

[แหล่ง](https://www.jmlr.org/papers/volume7/demsar06a/demsar06a.pdf) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-014_Anon2006_statistical-comparisons-of-classifiers-over-multip.pdf`](../../../papers/13_validation_statistics_claims/VV-014_Anon2006_statistical-comparisons-of-classifiers-over-multip.pdf)

การทดสอบแบบไม่อิงพารามิเตอร์สำหรับเทียบอัลกอริทึมข้ามหลายงาน ใช้กับการเทียบวิธีค้นหาข้ามหลายสนามได้

### VV-015 — Time for a Change: a Tutorial for Comparing Multiple Classifiers Through Bayesian Analysis

Benavoli et al. · 2017 · Journal of machine learning research · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1606.04316) · [arXiv:1606.04316](https://arxiv.org/abs/1606.04316) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-015_Benavoli2017_time-for-a-change-a-tutorial-for-comparing-multipl.pdf`](../../../papers/13_validation_statistics_claims/VV-015_Benavoli2017_time-for-a-change-a-tutorial-for-comparing-multipl.pdf)

การเปรียบเทียบแบบ Bayesian ที่มีช่วงความเท่ากันเชิงปฏิบัติ เป็นวิธีบอกว่า 'ไม่ต่างในทางปฏิบัติ' แทน 'ไม่มีนัยสำคัญ'

### VV-016 — Benchmarking in Optimization: Best Practice and Open Issues

Bartz-Beielstein et al. · 2020 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2007.03488) · [arXiv:2007.03488](https://arxiv.org/abs/2007.03488) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-016_Beielstein2020_benchmarking-in-optimization-best-practice-and-ope.pdf`](../../../papers/13_validation_statistics_claims/VV-016_Beielstein2020_benchmarking-in-optimization-best-practice-and-ope.pdf)

แนวปฏิบัติที่ดีของชุมชนในการ benchmark optimizer (งบ baseline การรายงาน) เป็น checklist ของระเบียบแคมเปญเรา

### VV-017 — COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting

Hansen et al. · 2021 · Optim. Methods Softw. · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1603.08785) · [arXiv:1603.08785](https://arxiv.org/abs/1603.08785) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-017_Hansen2021_coco-a-platform-for-comparing-continuous-optimizer.pdf`](../../../papers/13_validation_statistics_claims/VV-017_Hansen2021_coco-a-platform-for-comparing-continuous-optimizer.pdf)

การเปรียบเทียบสมรรถนะ optimizer ตามงบแบบ anytime เป็นแบบการรายงานคุณภาพเทียบกับจำนวนการประเมิน

### VV-018 — The preregistration revolution

Nosek et al. · 2018 · Proceedings of the National Academy of Sciences · **ตรง**

[แหล่ง](https://doi.org/10.1073/pnas.1708274114) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.ncbi.nlm.nih.gov/pmc/articles/5856500)

เหตุผลของการลงทะเบียนสมมติฐานและการวิเคราะห์ล่วงหน้า เป็นเหตุผลเบื้องหลังระเบียบที่ตรึงไว้ก่อนแคมเปญของโครงการ

### VV-019 — Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)

Pineau et al. · 2021 · Journal of machine learning research · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2003.12206) · [arXiv:2003.12206](https://arxiv.org/abs/2003.12206) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-019_Pineau2021_improving-reproducibility-in-machine-learning-rese.pdf`](../../../papers/13_validation_statistics_claims/VV-019_Pineau2021_improving-reproducibility-in-machine-learning-rese.pdf)

checklist และข้อค้นพบด้านการทำซ้ำได้ เสริมข้อกำหนด metadata การ replay

### VV-020 — Troubling Trends in Machine Learning Scholarship

Lipton & Steinhardt · 2018 · Queue · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1807.03341) · [arXiv:1807.03341](https://arxiv.org/abs/1807.03341) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-020_Lipton2018_troubling-trends-in-machine-learning-scholarship.pdf`](../../../papers/13_validation_statistics_claims/VV-020_Lipton2018_troubling-trends-in-machine-learning-scholarship.pdf)

รวบรวมการอ้างเกินจริง การคาดเดาที่นำเสนอเป็นคำอธิบาย และช่องว่างของ ablation เป็น checklist ผู้รีวิวสำหรับรายงานของเราเอง

### VV-021 — The Surprising Creativity of Digital Evolution: A Collection of Anecdotes from the Evolutionary Computation and Artificial Life Research Communities

Lehman et al. · 2020 · Artificial Life · **ตรง**

[แหล่ง](https://arxiv.org/abs/1803.03453) · [arXiv:1803.03453](https://arxiv.org/abs/1803.03453) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-021_Lehman2020_the-surprising-creativity-of-digital-evolution-a-c.pdf`](../../../papers/13_validation_statistics_claims/VV-021_Lehman2020_the-surprising-creativity-of-digital-evolution-a-c.pdf)

หลายสิบกรณีที่วิวัฒนาการใช้บั๊กของตัวจำลองและช่องโหว่ เป็นหลักฐานเบื้องหลังการถือว่าการใช้ช่องโหว่เชิงตัวเลขเป็นคำอธิบายทางเลือก

### VV-022 — Concrete Problems in AI Safety

Amodei et al. · 2016 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1606.06565) · [arXiv:1606.06565](https://arxiv.org/abs/1606.06565) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-022_Amodei2016_concrete-problems-in-ai-safety.pdf`](../../../papers/13_validation_statistics_claims/VV-022_Amodei2016_concrete-problems-in-ai-safety.pdf)

นิยาม reward hacking และผลข้างเคียง เป็นศัพท์ของช่องโหว่วัตถุประสงค์ในการค้นหาการออกแบบ

### VV-023 — Defining and Characterizing Reward Hacking

Skalse et al. · 2022 · Advances in Neural Information Processing Systems 35 · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2209.13085) · [arXiv:2209.13085](https://arxiv.org/abs/2209.13085) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-023_Skalse2022_defining-and-characterizing-reward-hacking.pdf`](../../../papers/13_validation_statistics_claims/VV-023_Skalse2022_defining-and-characterizing-reward-hacking.pdf)

นิยามเชิงรูปนัยว่าเมื่อใดวัตถุประสงค์แทนถูกใช้ช่องโหว่ได้ เกี่ยวข้องกับเวลาแข่ง Level-0 ในฐานะตัวแทนเวลาแข่งจริง

### VV-024 — Leakage and the reproducibility crisis in machine-learning-based science

Kapoor & Narayanan · 2023 · arXiv.org · **ตรง**

[แหล่ง](https://arxiv.org/abs/2207.07048) · [arXiv:2207.07048](https://arxiv.org/abs/2207.07048) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-024_Kapoor2023_leakage-and-the-reproducibility-crisis-in-machine.pdf`](../../../papers/13_validation_statistics_claims/VV-024_Kapoor2023_leakage-and-the-reproducibility-crisis-in-machine.pdf)

อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate

### VV-025 — The garden of forking paths: Why multiple comparisons can be a problem, even when there is no fishing expedition or p-hacking and the research hypothesis was posited ahead of time

Watson · 2013 · New Directions in Travel Writing Studies · **อ้อม**

[แหล่ง](https://doi.org/10.1057/9781137457257.0008) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-025_Watson2013_the-garden-of-forking-paths-why-multiple-compariso.pdf`](../../../papers/13_validation_statistics_claims/VV-025_Watson2013_the-garden-of-forking-paths-why-multiple-compariso.pdf)

การเลือกการวิเคราะห์ตามข้อมูลเพิ่ม false positive แม้ไม่ตั้งใจ สนับสนุนการตรึงการวิเคราะห์ก่อนเห็นผล

### VV-026 — The ASA Statement on p-Values: Context, Process, and Purpose

Wasserstein & Lazar · 2016 · The American Statistician · **อ้อม**

[แหล่ง](https://doi.org/10.1080/00031305.2016.1154108) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.tandfonline.com/doi/pdf/10.1080/00031305.2016.1154108?needAccess=true&role=button)

p-value หมายถึงอะไรและไม่ได้หมายถึงอะไร เกี่ยวข้องกับการรายงานผลเทียบแคมเปญที่ไม่มีนัยสำคัญอย่างซื่อตรง

### VV-027 — Noise and the reality gap: The use of simulation in evolutionary robotics

Jakobi et al. · 1995 · Lecture Notes in Computer Science · **ตรง**

[แหล่ง](https://doi.org/10.1007/3-540-59496-5_337) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เพิ่มสัญญาณรบกวนที่เหมาะสมในการจำลองเพื่อไม่ให้วิวัฒนาการใช้สิ่งแปลกปลอมของตัวจำลอง เป็นวิธีแก้ reality gap ยุคแรก

### VV-028 — Robot Learning from Randomized Simulations: A Review

Muratore et al. · 2022 · Frontiers in Robotics and AI · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2111.00956) · [arXiv:2111.00956](https://arxiv.org/abs/2111.00956) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-028_Muratore2022_robot-learning-from-randomized-simulations-a-revie.pdf`](../../../papers/13_validation_statistics_claims/VV-028_Muratore2022_robot-learning-from-randomized-simulations-a-revie.pdf)

ทบทวน domain randomization สำหรับ sim-to-real เกี่ยวข้องกับความทนทานข้ามพารามิเตอร์ที่ไม่แน่นอน

### VV-029 — Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World

Tobin et al. · 2017 · IEEE/RJS International Conference on Intelligent RObots and Systems · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1703.06907) · [arXiv:1703.06907](https://arxiv.org/abs/1703.06907) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-029_Tobin2017_domain-randomization-for-transferring-deep-neural.pdf`](../../../papers/13_validation_statistics_claims/VV-029_Tobin2017_domain-randomization-for-transferring-deep-neural.pdf)

สุ่มพารามิเตอร์ตัวจำลองเพื่อถ่ายโอนสู่ความจริง เป็นกลยุทธ์ความทนทานสำหรับเงื่อนไข held-out

### VV-030 — Estimating the reproducibility of psychological science

Collaboration · 2015 · Science · **อ้อม**

[แหล่ง](https://doi.org/10.1126/science.aac4716) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://research.tilburguniversity.edu/en/publications/4b1e6c37-3ee2-414b-b790-66024d631d4a)

ความพยายามทำซ้ำขนาดใหญ่ที่แสดงว่าผลอ่อนลงเมื่อทำซ้ำ เป็นพื้นหลังของการคาดว่าผลจะหดเมื่อรันผู้สมัครที่เลื่อนระดับอีกครั้ง

### VV-031 — A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification

Angelopoulos & Bates · 2021 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2107.07511) · [arXiv:2107.07511](https://arxiv.org/abs/2107.07511) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-031_Angelopoulos2021_a-gentle-introduction-to-conformal-prediction-and.pdf`](../../../papers/13_validation_statistics_claims/VV-031_Angelopoulos2021_a-gentle-introduction-to-conformal-prediction-and.pdf)

ช่วงการทำนายที่ไม่ขึ้นกับการกระจายสำหรับ surrogate ใด ๆ เป็นวิธีง่ายในการจำกัดความคลาดเคลื่อนของ surrogate ในการตัดสินเลื่อนระดับ

### VV-032 — SALib: An open-source Python library for Sensitivity Analysis

Herman & Usher · 2017 · The Journal of Open Source Software · **อ้อม**

[แหล่ง](https://doi.org/10.21105/joss.00097) · มี PDF ในเครื่อง: [`papers/13_validation_statistics_claims/VV-032_Herman2017_salib-an-open-source-python-library-for-sensitivit.pdf`](../../../papers/13_validation_statistics_claims/VV-032_Herman2017_salib-an-open-source-python-library-for-sensitivit.pdf)

เครื่องมือวิเคราะห์ความไวแบบ global (Sobol, Morris) สำหรับหาว่าพารามิเตอร์ใดขับการจัดอันดับเวลาแข่ง


## การควบคุมการแข่งอัตโนมัติ ผู้ขับที่เรียนรู้ telemetry จริง และกลยุทธ์การแข่ง

ตัวควบคุมและผู้ขับที่เรียนรู้ซึ่งขับผู้สมัครแต่ละคันใกล้ขีดจำกัดได้ ข้อมูลการแข่งรถจริงแบบสาธารณะ การระบุแบบจำลองจากข้อมูลสนาม และการจำลองกลยุทธ์ระดับการแข่ง ผู้ขับที่อ่อนทำให้กลไกที่ดีดูแย่ ดังนั้นคุณภาพผู้ขับเป็นส่วนหนึ่งของความยุติธรรม

### AR-001 — Outracing champion Gran Turismo drivers with deep reinforcement learning

Wurman et al. · 2022 · Nature · **อ้อม** · แค็ตตาล็อก Work 102 P40

[แหล่ง](https://doi.org/10.1038/s41586-021-04357-7) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-001_Wurman2022_outracing-champion-gran-turismo-drivers-with-deep.pdf`](../../../papers/14_autonomous_racing_strategy/AR-001_Wurman2022_outracing-champion-gran-turismo-drivers-with-deep.pdf)

ผู้ขับที่เรียนรู้ชนะมนุษย์ระดับสูงสุดในเกม fidelity สูง เป็นวิธีสร้างผู้ขับที่แข็งต่อแต่ละแบบ ไม่ใช่การยืนยันทางกายภาพ

### AR-002 — Optimization-Based Autonomous Racing of 1:43 Scale RC Cars

Liniger et al. · 2015 · arXiv.org · **อ้อม** · แค็ตตาล็อก Work 102 P41

[แหล่ง](https://arxiv.org/abs/1711.07300) · [arXiv:1711.07300](https://arxiv.org/abs/1711.07300) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-002_Liniger2015_optimization-based-autonomous-racing-of-1-43-scale.pdf`](../../../papers/14_autonomous_racing_strategy/AR-002_Liniger2015_optimization-based-autonomous-racing-of-1-43-scale.pdf)

model predictive contouring control สำหรับการแข่ง เป็น baseline ตัวควบคุมที่ implement ได้พร้อมขอบฟ้าและขีดจำกัด actuator ชัดเจน

### AR-003 — Analyzing the Impact of Simulation Fidelity on the Evaluation of Autonomous Driving Motion Control

Sagmeister et al. · 2024 · 2024 IEEE Intelligent Vehicles Symposium (IV) · **ตรง** · แค็ตตาล็อก Work 102 P42

[แหล่ง](https://arxiv.org/abs/2602.07984) · [arXiv:2602.07984](https://arxiv.org/abs/2602.07984) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-003_Sagmeister2024_analyzing-the-impact-of-simulation-fidelity-on-the.pdf`](../../../papers/14_autonomous_racing_strategy/AR-003_Sagmeister2024_analyzing-the-impact-of-simulation-fidelity-on-the.pdf)

ตัด fidelity ของการจำลองทีละส่วนเทียบกับ telemetry การแข่งอัตโนมัติจริง เป็นแม่แบบของการทดสอบ H4

### AR-004 — Autonomous Racing using Learning Model Predictive Control

Rosolia et al. · 2016 · American Control Conference · **อ้อม** · แค็ตตาล็อก Work 102 P62

[แหล่ง](https://arxiv.org/abs/1610.06534) · [arXiv:1610.06534](https://arxiv.org/abs/1610.06534) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-004_Rosolia2016_autonomous-racing-using-learning-model-predictive.pdf`](../../../papers/14_autonomous_racing_strategy/AR-004_Rosolia2016_autonomous-racing-using-learning-model-predictive.pdf)

MPC ที่เรียนรู้ซ้ำจากรอบก่อนหน้าเพื่อลดเวลาต่อรอบ เป็นตัวควบคุมที่เข้าใกล้ขีดจำกัดของรถแต่ละคัน

### AR-005 — Autonomous Vehicles on the Edge: A Survey on Autonomous Vehicle Racing

Betz et al. · 2022 · IEEE Open Journal of Intelligent Transportation Systems · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2202.07008) · [arXiv:2202.07008](https://arxiv.org/abs/2202.07008) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-005_Betz2022_autonomous-vehicles-on-the-edge-a-survey-on-autono.pdf`](../../../papers/14_autonomous_racing_strategy/AR-005_Betz2022_autonomous-vehicles-on-the-edge-a-survey-on-autono.pdf)

survey การรับรู้ การวางแผน การควบคุม และการจำลองในการแข่งอัตโนมัติ เป็นแผนที่เครื่องมือและชุดข้อมูล

### AR-006 — Indy Autonomous Challenge - Autonomous Race Cars at the Handling Limits

Wischnewski et al. · 2022 · arXiv.org · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/2202.03807) · [arXiv:2202.03807](https://arxiv.org/abs/2202.03807) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-006_Wischnewski2022_indy-autonomous-challenge-autonomous-race-cars-at.pdf`](../../../papers/14_autonomous_racing_strategy/AR-006_Wischnewski2022_indy-autonomous-challenge-autonomous-race-cars-at.pdf)

การแข่งอัตโนมัติเต็มสเกลที่ขีดจำกัดการควบคุมพร้อมพฤติกรรมรถจริง เป็นเอกสารอ้างอิงของช่องว่างแบบจำลอง-ความจริงที่ความเร็วสูง

### AR-007 — TUM Autonomous Motorsport: An Autonomous Racing Software for the Indy Autonomous Challenge

Betz et al. · 2023 · J. Field Robotics · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2205.15979) · [arXiv:2205.15979](https://arxiv.org/abs/2205.15979) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-007_Betz2023_tum-autonomous-motorsport-an-autonomous-racing-sof.pdf`](../../../papers/14_autonomous_racing_strategy/AR-007_Betz2023_tum-autonomous-motorsport-an-autonomous-racing-sof.pdf)

ชุดซอฟต์แวร์การแข่งอัตโนมัติแบบเปิดครบวงรวมการวางแผนและการควบคุม เป็นชิ้นส่วนที่นำมาใช้กับ baseline ผู้ขับได้

### AR-008 — RACECAR -- The Dataset for High-Speed Autonomous Racing

Kulkarni et al. · 2023 · IEEE/RJS International Conference on Intelligent RObots and Systems · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/2306.03252) · [arXiv:2306.03252](https://arxiv.org/abs/2306.03252) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-008_Kulkarni2023_racecar-the-dataset-for-high-speed-autonomous-raci.pdf`](../../../papers/14_autonomous_racing_strategy/AR-008_Kulkarni2023_racecar-the-dataset-for-high-speed-autonomous-raci.pdf)

ข้อมูลหลายเซนเซอร์แบบเปิดจากรถ Indy อัตโนมัติเต็มสเกลถึง 273 km/h รวมสนามเอียง เป็นข้อมูลจริงสำหรับตรวจสอบแบบจำลองรถ

### AR-009 — AMZ Driverless: The Full Autonomous Racing System

Kabzan et al. · 2020 · J. Field Robotics · **อ้อม**

[แหล่ง](https://arxiv.org/abs/1905.05150) · [arXiv:1905.05150](https://arxiv.org/abs/1905.05150) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-009_Kabzan2020_amz-driverless-the-full-autonomous-racing-system.pdf`](../../../papers/14_autonomous_racing_strategy/AR-009_Kabzan2020_amz-driverless-the-full-autonomous-racing-system.pdf)

ระบบไร้คนขับ Formula Student ครบวงพร้อมแบบจำลองรถและ MPC เป็นการ implement อ้างอิงที่มีเอกสารดี

### AR-010 — Learning-Based Model Predictive Control for Autonomous Racing

Kabzan et al. · 2019 · IEEE Robotics and Automation Letters · **อ้อม**

[แหล่ง](https://doi.org/10.1109/lra.2019.2926677) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://hdl.handle.net/20.500.11850/351561)

การแก้แบบจำลองรถด้วย Gaussian process ภายใน MPC เป็นแบบการเรียนรู้ความคลาดเคลื่อนของแบบจำลองในผู้ขับ

### AR-011 — Super-Human Performance in Gran Turismo Sport Using Deep Reinforcement Learning

Fuchs et al. · 2021 · IEEE Robotics and Automation Letters · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2008.07971) · [arXiv:2008.07971](https://arxiv.org/abs/2008.07971) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-011_Fuchs2021_super-human-performance-in-gran-turismo-sport-usin.pdf`](../../../papers/14_autonomous_racing_strategy/AR-011_Fuchs2021_super-human-performance-in-gran-turismo-sport-usin.pdf)

ผู้ขับ RL ที่ทำเวลาต่อรอบเหนือมนุษย์ใน time trial เป็นวิธี baseline ของผู้ขับที่เรียนรู้

### AR-012 — Reaching the Limit in Autonomous Racing: Optimal Control versus Reinforcement Learning

Song et al. · 2023 · Science Robotics · **ตรง**

[แหล่ง](https://arxiv.org/abs/2310.10943) · [arXiv:2310.10943](https://arxiv.org/abs/2310.10943) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-012_Song2023_reaching-the-limit-in-autonomous-racing-optimal-co.pdf`](../../../papers/14_autonomous_racing_strategy/AR-012_Song2023_reaching-the-limit-in-autonomous-racing-optimal-co.pdf)

เปรียบเทียบ optimal control กับ RL สำหรับการแข่งโดรนที่ขีดจำกัด เป็นหลักฐานสำหรับการเลือกวิธีผู้ขับเมื่อแบบจำลองไม่ตรง

### AR-013 — Champion-level drone racing using deep reinforcement learning

Kaufmann et al. · 2023 · Nature · **อ้อม**

[แหล่ง](https://doi.org/10.1038/s41586-023-06419-4) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-013_Kaufmann2023_champion-level-drone-racing-using-deep-reinforceme.pdf`](../../../papers/14_autonomous_racing_strategy/AR-013_Kaufmann2023_champion-level-drone-racing-using-deep-reinforceme.pdf)

policy ที่เรียนรู้ชนะแชมป์มนุษย์ในโลกจริงโดยใช้แบบจำลอง residual จากข้อมูลจริง เป็นตัวอย่างการปิดช่องว่างจากจำลองสู่ของจริง

### AR-014 — Application of Monte Carlo Methods to Consider Probabilistic Effects in a Race Simulation for Circuit Motorsport

Heilmeier et al. · 2020 · Applied Sciences · **ตรง**

[แหล่ง](https://doi.org/10.3390/app10124229) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.mdpi.com/2076-3417/10/12/4229/pdf?version=1597915201)

การจำลองการแข่งที่มีเหตุการณ์เชิงความน่าจะเป็น (safety car ความเสียหาย) ด้วย Monte Carlo เกี่ยวข้องกับเวลาแข่งรวมแทนเวลาหนึ่งรอบ

### AR-015 — Virtual Strategy Engineer: Using Artificial Neural Networks for Making Race Strategy Decisions in Circuit Motorsport

Heilmeier et al. · 2020 · Applied Sciences · **อ้อม**

[แหล่ง](https://doi.org/10.3390/app10217805) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](https://www.mdpi.com/2076-3417/10/21/7805/pdf)

การตัดสินใจกลยุทธ์พิทและชนิดยางที่เรียนรู้ในการจำลองการแข่ง กลยุทธ์เป็นส่วนหนึ่งของเวลาแข่งรวม

### AR-016 — A Race Simulation for Strategy Decisions in Circuit Motorsports

Heilmeier et al. · 2018 · 2018 21st International Conference on Intelligent Transportation Systems (ITSC) · **ตรง**

[แหล่ง](https://doi.org/10.1109/itsc.2018.8570012) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การจำลองการแข่งทีละรอบพร้อมการเสื่อมของยางและมวลเชื้อเพลิง เป็นแบบจำลองสาธารณะของเวลาระยะการแข่ง (ไม่ใช่ระยะรอบ)

### AR-017 — Towards Learning-Based Formula 1 Race Strategies

Fieni et al. · 2025 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2512.21570) · [arXiv:2512.21570](https://arxiv.org/abs/2512.21570) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-017_Fieni2025_towards-learning-based-formula-1-race-strategies.pdf`](../../../papers/14_autonomous_racing_strategy/AR-017_Fieni2025_towards-learning-based-formula-1-race-strategies.pdf)

กลยุทธ์ F1 แบบเรียนรู้ เป็นบริบทล่าสุดของการตัดสินใจระดับการแข่ง

### AR-018 — Game Theory in Formula 1: From Physical to Strategic Interactions

Fieni et al. · 2025 · European Journal of Control · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2503.05421) · [arXiv:2503.05421](https://arxiv.org/abs/2503.05421) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-018_Fieni2025_game-theory-in-formula-1-from-physical-to-strategi.pdf`](../../../papers/14_autonomous_racing_strategy/AR-018_Fieni2025_game-theory-in-formula-1-from-physical-to-strategi.pdf)

มุมมองทฤษฎีเกมของปฏิสัมพันธ์ใน F1 เกี่ยวข้องเฉพาะเมื่อการแข่งหลายคันเข้ามาในสภาพแวดล้อม

### AR-019 — Opponent State Inference Under Partial Observability: An HMM-POMDP Framework for 2026 Formula 1 Energy Strategy

Kleisarchaki · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2603.01290) · [arXiv:2603.01290](https://arxiv.org/abs/2603.01290) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-019_Kleisarchaki2026_opponent-state-inference-under-partial-observabili.pdf`](../../../papers/14_autonomous_racing_strategy/AR-019_Kleisarchaki2026_opponent-state-inference-under-partial-observabili.pdf)

จำลองกลยุทธ์พลังงานตามติกาปี 2026 รวมถึง Override Mode เป็นบริบทของโปรไฟล์ติกาที่สัญญาการแข่งของเราตรึงไว้

### AR-020 — Bridging RL and MPC for mixed-integer optimal control with application to Formula 1 race strategies

Wüthrich et al. · 2026 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2604.00826) · [arXiv:2604.00826](https://arxiv.org/abs/2604.00826) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-020_Wuthrich2026_bridging-rl-and-mpc-for-mixed-integer-optimal-cont.pdf`](../../../papers/14_autonomous_racing_strategy/AR-020_Wuthrich2026_bridging-rl-and-mpc-for-mixed-integer-optimal-cont.pdf)

รวม RL กับ MPC สำหรับกลยุทธ์การแข่งแบบ mixed-integer เกี่ยวข้องกับการเลือกกลยุทธ์แบบไม่ต่อเนื่อง

### AR-021 — Mission Performance: Automatic and Adaptive Race Pace Progression for Autonomous Racing

Lambertini et al. · 2026 · arXiv · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2609.12292) · [arXiv:2609.12292](https://arxiv.org/abs/2609.12292) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-021_Lambertini2026_mission-performance-automatic-and-adaptive-race-pa.pdf`](../../../papers/14_autonomous_racing_strategy/AR-021_Lambertini2026_mission-performance-automatic-and-adaptive-race-pa.pdf)

การเพิ่มจังหวะความเร็วแบบปรับตัวสู่ขีดจำกัด เกี่ยวข้องกับการหาจังหวะที่ทำได้ของผู้สมัครแต่ละคันอย่างปลอดภัย

### AR-022 — Learning-Based On-Track System Identification for Scaled Autonomous Racing in Under a Minute

Dikici et al. · 2024 · IEEE Robotics and Automation Letters · **ตรง**

[แหล่ง](https://arxiv.org/abs/2411.17508) · [arXiv:2411.17508](https://arxiv.org/abs/2411.17508) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-022_Dikici2024_learning-based-on-track-system-identification-for.pdf`](../../../papers/14_autonomous_racing_strategy/AR-022_Dikici2024_learning-based-on-track-system-identification-for.pdf)

ระบุแบบจำลองยาง/รถจากข้อมูลขับประมาณ 30 วินาที เป็นเส้นทางการสอบเทียบที่เร็วสำหรับ physical correlation

### AR-023 — Deep Dynamics: Vehicle Dynamics Modeling with a Physics-Informed Neural Network for Autonomous Racing

Chrosniak et al. · 2024 · IEEE Robotics and Automation Letters · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2312.04374) · [arXiv:2312.04374](https://arxiv.org/abs/2312.04374) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-023_Chrosniak2024_deep-dynamics-vehicle-dynamics-modeling-with-a-phy.pdf`](../../../papers/14_autonomous_racing_strategy/AR-023_Chrosniak2024_deep-dynamics-vehicle-dynamics-modeling-with-a-phy.pdf)

โครงข่ายที่มีฟิสิกส์กำกับซึ่งประมาณพารามิเตอร์รถที่ตีความได้จากข้อมูล เป็นทางเลือกการระบุแบบจำลองแบบผสม

### AR-024 — F1TENTH: An Open-source Evaluation Environment for Continuous Control and Reinforcement Learning

— · 2020 · **อ้อม**

[แหล่ง](https://proceedings.mlr.press/v123/o-kelly20a/o-kelly20a.pdf) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-024_Anon2020_f1tenth-an-open-source-evaluation-environment-for.pdf`](../../../papers/14_autonomous_racing_strategy/AR-024_Anon2020_f1tenth-an-open-source-evaluation-environment-for.pdf)

สภาพแวดล้อมประเมินการแข่งแบบย่อส่วนที่เปิดพร้อมรถจริง เป็นแนวคิดแท่นทดสอบจริงราคาถูก

### AR-025 — Real-Time Adaptive Velocity Optimization for Autonomous Electric Cars at the Limits of Handling

Herrmann et al. · 2021 · IEEE Transactions on Intelligent Vehicles · **อ้อม**

[แหล่ง](https://doi.org/10.1109/tiv.2020.3047858) · [arXiv:2012.13586](https://arxiv.org/abs/2012.13586) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-025_Herrmann2021_real-time-adaptive-velocity-optimization-for-auton.pdf`](../../../papers/14_autonomous_racing_strategy/AR-025_Herrmann2021_real-time-adaptive-velocity-optimization-for-auton.pdf)

การวางแผนความเร็วแบบเวลาจริงที่มีขีดจำกัดพลังงานและแรงเสียดทานบนรถแข่งไฟฟ้า เป็นชิ้นส่วนผู้ขับสำหรับการแข่งที่พลังงานจำกัด

### AR-026 — Efficient Trajectory Optimization for Autonomous Racing via Formula-1 Data-Driven Initialization

Shehadeh et al. · 2026 · arXiv.org · **ข้อมูล/ผลที่ใช้ได้**

[แหล่ง](https://arxiv.org/abs/2603.07126) · [arXiv:2603.07126](https://arxiv.org/abs/2603.07126) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-026_Shehadeh2026_efficient-trajectory-optimization-for-autonomous-r.pdf`](../../../papers/14_autonomous_racing_strategy/AR-026_Shehadeh2026_efficient-trajectory-optimization-for-autonomous-r.pdf)

ใช้ข้อมูลเส้นทาง Formula 1 จริงเป็นค่าเริ่มต้นของการ optimize เส้นแข่ง เป็นแหล่งข้อมูลเส้นแข่ง F1 สาธารณะและวิธี warm start

### AR-027 — Unifying F1TENTH Autonomous Racing: Survey, Methods and Benchmarks

Evans et al. · 2024 · arXiv.org · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2402.18558) · [arXiv:2402.18558](https://arxiv.org/abs/2402.18558) · มี PDF ในเครื่อง: [`papers/14_autonomous_racing_strategy/AR-027_Evans2024_unifying-f1tenth-autonomous-racing-survey-methods.pdf`](../../../papers/14_autonomous_racing_strategy/AR-027_Evans2024_unifying-f1tenth-autonomous-racing-survey-methods.pdf)

benchmark ตัววางแผนและตัวควบคุมการแข่งบนแพลตฟอร์มเดียวกัน เป็นแหล่งอ้างอิงของการเทียบตัวควบคุมอย่างยุติธรรม


## การสังเคราะห์การออกแบบเชิงคำนวณ การแทนค่าเชิงหน้าที่ การสังเคราะห์การประกอบ และการวัดความใหม่

งานวิจัยการออกแบบวิศวกรรมเรื่องการสร้างสถาปัตยกรรมจากหน้าที่ด้วย grammar การแยกโครงสร้างเป็นชิ้นส่วนที่ต่อกัน และการวัดว่าการออกแบบใหม่จริงหรือไม่ เกี่ยวข้องกับ typed interface, physical interface graph, part resolution และนิยามการค้นพบของโครงการ

### DS-001 — Computational Synthesis of Product Architectures Based on Object-Oriented Graph Grammars

Helms & Shea · 2012 · Journal of Mechanical Design · **ตรง**

[แหล่ง](https://doi.org/10.1115/1.4005592) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

graph grammar เชิงวัตถุบนแบบจำลอง function-behaviour-structure ตรวจสอบด้วยการสังเคราะห์ powertrain ไฮบริด เป็นงานก่อนหน้าด้านการออกแบบวิศวกรรมที่ใกล้กับ typed topology genome ของเรามากที่สุด

### DS-002 — A framework for computational design synthesis based on graph-grammars and function-behavior-structure

Helms et al. · 2009 · Volume 8: 14th Design for Manufacturing and the Life Cycle Conference; 6th Symposium on International Design and Design Education; 21st International Conference on Design Theory and Methodology, Parts A and B · **ตรง**

[แหล่ง](https://doi.org/10.1115/detc2009-86851) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://mediatum.ub.tum.de/node?id=1155306)

paper กรอบงานเบื้องหลัง DS-001 นิยามว่าข้อกำหนดเชิงหน้าที่ขับการสร้างสถาปัตยกรรมด้วย grammar อย่างไร

### DS-003 — Comparing Strategies for Topologic and Parametric Rule Application in Automated Computational Design Synthesis

Königseder & Shea · 2016 · Journal of Mechanical Design · **ตรง**

[แหล่ง](https://doi.org/10.1115/1.4031714) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

เปรียบเทียบว่ากฎ grammar เชิง topology และเชิงพารามิเตอร์ควรสลับกันอย่างไรในการค้นหา เกี่ยวข้องโดยตรงกับการจัดตารางการกลายพันธุ์

### DS-004 — Computer-Based Design Synthesis Research: An Overview

Chakrabarti et al. · 2011 · Journal of Computing and Information Science in Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1115/1.3593409) · ไม่มีสำเนาในเครื่อง (ดาวน์โหลดไม่สำเร็จ) · [สำเนา open access ให้ดาวน์โหลดผ่านเบราว์เซอร์](http://mediatum.ub.tum.de/node?id=1161039)

ภาพรวมของวิธีสังเคราะห์การออกแบบเชิงคำนวณและการประเมิน วางตำแหน่งโครงการในงานวิจัยการสังเคราะห์ที่ผ่านมา

### DS-005 — A Framework for Computational Design Synthesis: Model and Applications

Cagan et al. · 2005 · Journal of Computing and Information Science in Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1115/1.2013289) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แบบจำลองการสังเคราะห์การออกแบบแบบ representation-generation-evaluation-guidance เป็นศัพท์สำหรับแยกตัวสร้างออกจากตัวประเมินของเรา

### DS-006 — A functional basis for engineering design: Reconciling and evolving previous efforts

Hirtz et al. · 2002 · Research in Engineering Design · **ตรง**

[แหล่ง](https://doi.org/10.1007/s00163-001-0008-3) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

อนุกรมวิธานมาตรฐานของหน้าที่และการไหล (วัสดุ พลังงาน สัญญาณ) เป็นฐานของ interface เชิงหน้าที่แบบมีชนิดที่ไม่ขึ้นกับรูปทรง

### DS-007 — Development of a Functional Basis for Design

Stone & Wood · 2000 · Journal of Mechanical Design · **อ้อม**

[แหล่ง](https://doi.org/10.1115/1.1289637) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

คำศัพท์ functional basis ฉบับแรก เป็นพื้นหลังของ DS-006

### DS-008 — Design prototypes: a knowledge representation schema for design

— · 1990 · **อ้อม**

[แหล่ง](https://aaai.org/ojs/index.php/aimagazine/article/view/854) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

กรอบ function-behaviour-structure แยกสิ่งที่ชิ้นส่วนทำออกจากวิธีที่สร้าง ตามที่เกณฑ์การค้นพบของเราต้องการ

### DS-009 — Automated synthesis of electromechanical design configurations from empirical analysis of function to form mapping

Kurtoglu & Campbell · 2009 · Journal of Engineering Design · **อ้อม**

[แหล่ง](https://doi.org/10.1080/09544820701546165) · มี PDF ในเครื่อง: [`papers/15_design_synthesis_novelty/DS-009_Kurtoglu2009_automated-synthesis-of-electromechanical-design-co.pdf`](../../../papers/15_design_synthesis_novelty/DS-009_Kurtoglu2009_automated-synthesis-of-electromechanical-design-co.pdf)

เรียนรู้การจับคู่จากหน้าที่สู่ชิ้นส่วนจากผลิตภัณฑ์จริงเพื่อสังเคราะห์โครงร่าง เป็นแหล่ง grammar ที่ขับด้วยข้อมูล

### DS-010 — Metrics for measuring ideation effectiveness

Shah et al. · 2003 · Design Studies · **ตรง**

[แหล่ง](https://doi.org/10.1016/s0142-694x(02)00034-0) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

ตัวชี้วัด novelty, variety, quality และ quantity ของแนวคิดการออกแบบ เป็นนิยามเชิงปฏิบัติสำหรับวัดความใหม่ของสถาปัตยกรรมที่สร้างขึ้น

### DS-011 — Assessing design creativity

Sarkar & Chakrabarti · 2011 · Design Studies · **อ้อม**

[แหล่ง](https://doi.org/10.1016/j.destud.2011.01.002) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

รวมความใหม่และประโยชน์เป็นตัววัดความสร้างสรรค์ เกี่ยวข้องกับการแยกสิ่งใหม่แต่ไร้ประโยชน์ออกจากการค้นพบที่มีประโยชน์

### DS-012 — Measuring technological novelty with patent-based indicators

Verhoeven et al. · 2016 · Research Policy · **อ้อม**

[แหล่ง](https://doi.org/10.1016/j.respol.2015.11.010) · มี PDF ในเครื่อง: [`papers/15_design_synthesis_novelty/DS-012_Verhoeven2016_measuring-technological-novelty-with-patent-based.pdf`](../../../papers/15_design_synthesis_novelty/DS-012_Verhoeven2016_measuring-technological-novelty-with-patent-based.pdf)

ตัววัดจากสิทธิบัตรของการผสมใหม่และหน้าที่ใหม่ เป็นแหล่งอ้างอิงภายนอกว่าอะไรนับเป็นความใหม่ระดับเทคโนโลยี

### DS-013 — Decomposition-Based Assembly Synthesis of Space Frame Structures Using Joint Library

Lyu & Saitou · 2005 · Volume 1: 30th Design Automation Conference · **ตรง**

[แหล่ง](https://doi.org/10.1115/detc2004-57301) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

แยกเฟรมเป็นชิ้นส่วนและเลือกข้อต่อจากคลังภายใต้วัตถุประสงค์ด้านโครงสร้างและการผลิต เป็นปัญหาเดียวกับ part resolution พร้อมระบบข้อต่อ (Works 140-142)

### DS-014 — Decomposition-Based Assembly Synthesis Based on Structural Considerations

Yetis & Saitou · 2002 · Journal of Mechanical Design · **ตรง**

[แหล่ง](https://doi.org/10.1115/1.1519276) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

การสังเคราะห์การประกอบแบบแยกส่วนที่ขับด้วยความแข็งเกร็งรุ่นก่อน เป็นฐานวิธีของ DS-013

### DS-015 — Multi-component topology and material orientation design of composite structures (MTO-C)

Zhou et al. · 2018 · Computer Methods in Applied Mechanics and Engineering · **ตรง**

[แหล่ง](https://doi.org/10.1016/j.cma.2018.07.039) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

optimize topology ของโครงสร้างพร้อมการแยกเป็นชิ้นส่วนคอมโพสิตที่ผลิตได้ในคราวเดียว ปิดช่องว่างระหว่าง topology กับจำนวนชิ้นส่วน

### DS-016 — Patterns in System Architecture Decisions

Selva et al. · 2016 · Systems Engineering · **อ้อม**

[แหล่ง](https://doi.org/10.1002/sys.21370) · ไม่มีสำเนาในเครื่อง (ไม่พบสำเนา open access)

จำแนกการตัดสินใจเชิงสถาปัตยกรรม (การกำหนด การแบ่ง การเชื่อม) เป็นแบบแผนพร้อมสูตรการค้นหา เป็นมุมมองเชิงรูปนัยของการเลือกสถาปัตยกรรมรถ

### DS-017 — Generative Transformers for Design Concept Generation

Zhu & Luo · 2023 · Journal of Computing and Information Science in Engineering · **อ้อม**

[แหล่ง](https://arxiv.org/abs/2211.03468) · [arXiv:2211.03468](https://arxiv.org/abs/2211.03468) · มี PDF ในเครื่อง: [`papers/15_design_synthesis_novelty/DS-017_Zhu2023_generative-transformers-for-design-concept-generat.pdf`](../../../papers/15_design_synthesis_novelty/DS-017_Zhu2023_generative-transformers-for-design-concept-generat.pdf)

การสร้างแนวคิดการออกแบบด้วย transformer จากความรู้การออกแบบ เป็นเส้นทางเสนอแบบระดับข้อความก่อนเรขาคณิต


## paper open access ที่ต้องดาวน์โหลดด้วยมือ

paper แต่ละชิ้นด้านล่างมีสำเนาฟรี แต่เซิร์ฟเวอร์ปฏิเสธการดาวน์โหลดด้วยสคริปต์ (ส่วนใหญ่เป็นการตรวจ bot แบบ Cloudflare ที่ MDPI, ACM, PNAS, Royal Society, IEEE และคลังของบางมหาวิทยาลัย) และไม่ได้พยายามข้ามการตรวจนั้น ให้เปิดลิงก์ในเบราว์เซอร์ บันทึก PDF ไว้ในโฟลเดอร์เดียวกัน แล้วรัน `python scripts/research/build_paper_library.py --ingest <folder>` การตั้งชื่อไฟล์เป็น `<ID>.pdf` (เช่น `OE-003.pdf`) ทำให้จับคู่ได้ชัดเจน โดยยังมีการตรวจชื่อเรื่องเหมือนเดิม

| ID | ชื่อเรื่อง | เปิดในเบราว์เซอร์ |
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
