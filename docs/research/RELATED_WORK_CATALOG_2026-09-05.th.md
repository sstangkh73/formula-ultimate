# แค็ตตาล็อกงานที่เกี่ยวข้องกับ Formula Ultimate — 2026-09-05

ต้นฉบับภาษาอังกฤษ: `RELATED_WORK_CATALOG_2026-09-05.md`

มี **62 งานวิชาการ (P01–P62)** และ **8 แหล่งอุตสาหกรรม/เครื่องมือ (I01–I08)** อ่านข้อสรุปและลำดับพัฒนาใน [รายงานประเมิน](../reports/LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.th.md)

## ขอบเขตและวิธีคัดเลือก

สำรวจแบบกว้างโดยเน้นแหล่งปฐมภูมิถึง 2026-09-05: สำนักพิมพ์ arXiv คลังมหาวิทยาลัย เว็บไซต์ผู้วิจัย โค้ดผู้พัฒนา และเว็บไซต์ทีม/ผู้ขายโดยตรง ค้นทั้งงานที่ทำสิ่งใกล้กันและงานที่ให้วิธีเติมช่องว่างของเรา นี่ไม่ใช่ systematic review และไม่รับรองว่าครบทุกงานที่มีอยู่ ไม่ได้นับ preprint กับฉบับตีพิมพ์ของงานเดียวกันซ้ำ งานต่อยอดที่มีเนื้อหาแยกนับแยกและระบุความเกี่ยวข้องไว้

รหัสการอ่าน: **E** = อ่านบางส่วนของเนื้อหาเต็มหรือเอกสารเทคนิค รวมถึงข้อจำกัด; **A** = อ่านบทคัดย่อ/คำอธิบายงานจากแหล่งปฐมภูมิ (บางแห่งผ่านดัชนีค้นหา); **M** = ตรวจบรรณานุกรม/ตัวโครงการเป็นหลัก ยังไม่ประเมินวิธีทั้งบทความ ไม่มีรหัสใดหมายความว่าได้ทำซ้ำงานแล้ว ไม่ได้อ่านทุกบทความเต็มฉบับ ไม่ได้รันโค้ดภายนอกหรือดาวน์โหลดชุดข้อมูลขนาดใหญ่

ลำดับอ่าน **First / Next / Later** เป็นข้อเสนอสำหรับสถานะโครงการปัจจุบัน ไม่ใช่การจัดอันดับคุณภาพวารสาร แต่ละแถวแยกสิ่งที่นำมาใช้ได้ออกจากสิ่งที่งานนั้นยังพิสูจน์ให้เราไม่ได้ ชื่อบทความเก็บภาษาต้นฉบับเพื่อค้นต่อได้ตรง

ตัวอย่างคำค้นที่ใช้: `robot morphology controller co-design graph grammar`, `quality diversity surrogate assisted illumination`, `multifidelity optimization`, `CAD generation BRep graph`, `Formula One minimum lap time three-dimensional track`, `aero suspension optimization`, `tyre thermal transient Magic Formula`, `simulation fidelity autonomous racing telemetry`, `CFD front wing experimental validation`, `DrivAerNet CarBench`, `F1 simulator correlation Mercedes McLaren Ferrari` และชื่อบทความที่ตามจากรายการอ้างอิง

ข้อจำกัดการเข้าถึง: บางหน้า Taylor & Francis/ScienceDirect และ PDF ผู้เขียนตอบ 403 หรือดึงข้อมูลไม่ได้ จึงใช้บทคัดย่อปฐมภูมิที่ค้นได้หรือสำเนามหาวิทยาลัยแทน และลดระดับการอ่านเมื่อไม่มีเนื้อหาวิธีเพียงพอ P28/P29/P54 เป็น M ไม่ใช่การรับรอง solver; P38 มีข้อจำกัดเข้าหน้าสำนักพิมพ์โดยตรง ปีบนเว็บอาจเป็นปีอัปโหลด: P30 คือ SIGGRAPH 2023 (preprint 2022), P42 คือ IEEE IV 2024 (ฝาก arXiv 2026), P10 รับ AVEC 2026 ซึ่งกำหนดประชุม 2026-09-07 ถึง 2026-09-11 ยังไม่ถึงวันประชุม ณ วันทบทวน ไม่อ้างว่าผลรายงานปี 2026 ผ่านการทำซ้ำอิสระแล้ว

## การค้นหารูปร่างร่วมกับตัวควบคุม

### P01 — Evolving Virtual Creatures

Sims · 1994 · SIGGRAPH · **Next · E** · [แหล่งปฐมภูมิ](https://www.karlsims.com/papers/siggraph94.pdf)

วิวัฒนาการกราฟร่างกายกับตัวควบคุมร่วมกัน เป็นรากฐานของการค้นหารูปร่าง แต่การเคลื่อนที่ในโลกจำลองยังไม่ใช่การยืนยันรถแข่งจริง

### P02 — Automatic design and manufacture of robotic lifeforms

Lipson & Pollack · 2000 · Nature · **Next · A** · [แหล่งปฐมภูมิ](https://web.mit.edu/people/hlipson/papers/design.pdf)

เชื่อมร่างกายที่วิวัฒนาการกับหุ่นยนต์ที่ผลิตจริง ใช้วางด่านผลิตและทดสอบในอนาคต โดยกลไกและโจทย์ที่สาธิตยังมีขอบเขตจำกัด

### P03 — RoboGrammar: Graph Grammar for Terrain-Optimized Robot Design

Zhao et al. · 2020 · ACM TOG · **First · A** · [แหล่งปฐมภูมิ](https://people.csail.mit.edu/jiex/papers/robogrammar/index.html)

ใช้ไวยากรณ์กราฟและการประเมินตัวควบคุมค้นหาแบบที่มีความหมายทางกล นำวิธีตรวจกราฟและจัดงบฝึกมาปรับใช้ได้ แต่กฎชิ้นส่วนยังจำกัดพื้นที่ค้นหา

### P04 — Evolution Gym: A Large-Scale Benchmark for Evolving Soft Robots

Bhatia et al. · 2021 · NeurIPS; arXiv 2022 · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2201.09863)

เป็น benchmark ร่วมสำหรับรูปร่างและตัวควบคุม ช่วยเปรียบเทียบอัลกอริทึมอย่างเป็นธรรม นำระเบียบการทดลองมาใช้ได้ แต่ฟิสิกส์ voxel 2D ไม่ใช่หลักฐานรถแข่ง 3D

### P05 — Neural Graph Evolution: Towards Efficient Automatic Robot Design

Wang et al. · 2019 · arXiv · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1906.05370)

ถ่ายทอดความรู้ตัวควบคุมบนกราฟเมื่อรูปร่างเปลี่ยน ช่วยศึกษาแนวทางลดการฝึกซ้ำ แต่ต้องวัดประโยชน์ใหม่ภายใต้งบของเรา

### P06 — Embodied Intelligence via Learning and Evolution

Gupta et al. · 2021 · arXiv · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2102.02202)

ศึกษาวิวัฒนาการร่วมกับการเรียนรู้หลายสภาพแวดล้อม ใช้ทดสอบว่ากลไกที่ค้นพบยังฝึกให้ใช้งานข้ามสนามได้หรือไม่ โดยการผลิตได้จริงต้องตรวจแยก

### P07 — DiffAqua: A Differentiable Computational Design Pipeline for Soft Underwater Swimmers with Shape Interpolation

Ma et al. · 2021 · ACM TOG · **Later · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2104.00837)

สาธิตการหารูปร่างและตัวควบคุมร่วมกันด้วยอนุพันธ์ แต่การแทรกรูปร่างและสมมติฐานวัตถุนิ่มใต้น้ำไม่ครอบคลุม topology รถแข่งอิสระ

### P08 — DiffTaichi: Differentiable Programming for Physical Simulation

Hu et al. · 2020 · ICLR; preprint 2019 · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1910.00935)

เป็นเครื่องมือจำลองที่หาอนุพันธ์ได้ เหมาะศึกษาการปรับค่าต่อเนื่องภายใน topology ที่ผ่านด่านแล้ว อนุพันธ์ไม่ได้รับรองความตรงทางฟิสิกส์หรือ contact ที่เรียบ

### P09 — Multi-Objective Graph Heuristic Search for Terrestrial Robot Design

Xu et al. · 2021 · ICRA · **First · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2107.05858)

ค้นหาแบบหุ่นยนต์ไม่ต่อเนื่องภายใต้หลายเป้าหมาย เหมาะกับการศึกษาข้อแลกเปลี่ยนของกลไกและสมรรถนะ โดยคงวัตถุประสงค์การแข่งขันและข้อจำกัดของโครงการ

### P10 — Racing a Wheeled Quadruped: Active Load Transfer Mitigation via Model Predictive Control

Eisman et al. · 2026 · arXiv; accepted AVEC 2026 · **First · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2606.26313)

ทดลองแข่งหุ่นยนต์สี่ขาติดล้อจริง เชื่อมกลไกขาแบบ active กับการถ่ายน้ำหนักและเวลารอบ ใกล้แนวคิดยานพาหนะนอกกรอบ แต่ใช้หุ่นยนต์ที่กำหนดมาแล้ว ไม่ได้ค้นหา topology เอง

## ความหลากหลายของแบบ หลายระดับความละเอียด และการถ่ายทอดสู่โลกจริง

### P11 — Illuminating search spaces by mapping elites

Mouret & Clune · 2015 · arXiv · **First · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1504.04909)

MAP-Elites เก็บแบบที่ดีในแต่ละช่องคุณลักษณะ ตรงกับ Work 099 แต่ความหลากหลายของ descriptor อาจยังเป็นกลไกที่เทียบเท่ากัน

### P12 — Quality Diversity: A New Frontier for Evolutionary Computation

Pugh, Soros & Stanley · 2016 · Frontiers · **Next · A** · [แหล่งปฐมภูมิ](https://doi.org/10.3389/frobt.2016.00040)

อธิบายแนวคิดและการประเมิน quality-diversity ใช้แยกความครอบคลุม ความใหม่ และคุณภาพ จำนวนแบบมากขึ้นไม่ได้แปลว่าค้นพบสิ่งที่ดีกว่าทางฟิสิกส์เสมอ

### P13 — Data-Efficient Design Exploration through Surrogate-Assisted Illumination

Gaier, Asteroth & Mouret · 2018 · arXiv · **First · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1806.05865)

ผสาน surrogate กับการค้นหาแบบหลากหลาย มีตัวอย่างออกแบบอากาศพลศาสตร์ เหมาะกับ evaluator ราคาแพง แต่ต้องตรวจแบบเด่นและแบบที่ surrogate คัดทิ้งผิด

### P14 — Covariance Matrix Adaptation MAP-Annealing

Fontaine & Nikolaidis · 2022 · arXiv · **Later · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2205.10752)

พัฒนาการค้นหา quality-diversity ในพื้นที่ต่อเนื่อง ควรเทียบหลัง MAP-Elites พื้นฐาน การปรับในพื้นที่พารามิเตอร์ไม่ได้สร้างตัวแทน topology ทั่วไปให้เอง

### P15 — Survey of multifidelity methods in uncertainty propagation, inference, and optimization

Peherstorfer, Willcox & Gunzburger · 2018 · SIAM Review · **First · E** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1806.10761)

อธิบายการใช้โมเดลราคาถูกและแพงร่วมกัน เป็นฐาน Work 098 เรื่องความคลาดเคลื่อน การเลื่อนด่าน และการคิดต้นทุน ชื่อระดับ fidelity ต้องมีหลักฐานความสัมพันธ์รองรับ

### P16 — Multi-fidelity Bayesian Optimisation with Continuous Approximations

Kandasamy et al. · 2017 · ICML · **Next · A** · [แหล่งปฐมภูมิ](https://proceedings.mlr.press/v70/kandasamy17a.html)

BOCA เลือกทั้งแบบและระดับ fidelity โดยคิดต้นทุน เหมาะเมื่อควบคุม fidelity ได้ แต่ความสัมพันธ์ที่สมมติอาจใช้ไม่ได้ข้ามการเปลี่ยน topology

### P17 — Crossing the Reality Gap: a Short Introduction to the Transferability Approach

Mouret, Koos & Doncieux · 2013 · arXiv · **First · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1307.1870)

สร้างโมเดลว่าพฤติกรรมจำลองถ่ายทอดสู่โลกจริงได้เพียงใด ใช้ประกอบด่านยอมรับแบบด้วยข้อมูลจริง การเห็นตรงกันระหว่างซิมอย่างเดียวยังไม่พอ

### P18 — Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions

Wang et al. · 2019 · arXiv · **Later · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1901.01753)

วิวัฒนาการโจทย์และคำตอบร่วมกัน อาจใช้สร้างสนามฝึกในอนาคต แต่ต้องตรึงสนามประเมินลับไว้เพื่อไม่ให้เกณฑ์ชนะเปลี่ยนตามการค้นหา

### P19 — Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions

Wang et al. · 2020 · arXiv · **Later · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2003.08536)

ขยายการสร้างโจทย์และถ่ายทอดคำตอบ เหมาะกับหลักสูตรฝึกมากกว่าการยืนยันกลไกในขั้นปัจจุบัน ต้องแยกงบสภาพแวดล้อมกับงบตัวควบคุม

### P20 — Reality-assisted evolution of soft robots through large-scale physical experimentation: a review

Howison et al. · 2020 · accepted-manuscript preprint · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2009.13960)

ทบทวนการนำการทดลองจริงเข้าไปในวิวัฒนาการแบบ ใช้วางระบบทดสอบชิ้นส่วนอัตโนมัติในอนาคต แต่ข้อมูลหุ่นยนต์นิ่มไม่ใช่ข้อมูลวัสดุรถแข่ง

## CAD, topology, mesh และ contact

### P21 — DeepCAD: A Deep Generative Network for Computer-Aided Design Models

Wu, Xiao & Zheng · 2021 · ICCV · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2105.09492)

สร้างลำดับคำสั่ง CAD ใช้เป็นตัวเสนอแบบได้ แต่ CAD ที่ถูกไวยากรณ์ยังต้องผ่านการตรวจการเชื่อมต่อ เส้นทางแรง กระบวนการผลิต และสมรรถนะ

### P22 — Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts

Khan et al. · 2024 · arXiv / NeurIPS · **Later · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2409.17106)

แปลงข้อความเป็นลำดับ CAD อาจใช้ตั้งต้นแบบหรือช่วยเขียนแบบ ความสมเหตุสมผลของภาษาไม่ใช่กลศาสตร์ ชื่อใน proceedings ใช้ 'Designs' แทน 'Models'

### P23 — BRepNet: A topological message passing system for solid models

Lambourne et al. · 2021 · CVPR · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2104.00706)

เรียนรู้บน topology ของผิวขอบ solid ใช้สร้าง descriptor และรู้จำ feature ได้ แต่ embedding ต้องตรวจความไม่ขึ้นกับการแทนข้อมูลและกรณีผิดพลาด

### P24 — Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences

Willis et al. · 2021 · ACM TOG; preprint 2020 · **Next · E** · [แหล่งปฐมภูมิ](https://www.research.autodesk.com/publications/fusion-360-gallery/)

มีข้อมูลลำดับการสร้าง CAD โดยมนุษย์ การอภิปรายการสร้างรูปกลับสนับสนุนการตรวจหน้าที่ของ feature เพราะรูปซ้อนทับกันมากก็ยังอาจขาด feature เล็กที่จำเป็น

### P25 — DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation

Park et al. · 2019 · CVPR · **Later · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1901.05103)

แทนพื้นผิวแบบ implicit ต่อเนื่อง เป็นทางเลือกสำหรับพื้นที่ค้นหา แต่การแปลงเป็น solid ปิด ความคลาดเคลื่อน feature และความหมายด้านการผลิตยังต้องทำเพิ่ม

### P26 — Generating optimal topologies in structural design using a homogenization method

Bendsøe & Kikuchi · 1988 · CMAME · **Next · A** · [แหล่งปฐมภูมิ](https://www.sciencedirect.com/science/article/pii/0045782588900862)

เป็นรากฐาน topology optimization ของโครงสร้างภายใต้ฟิสิกส์ ใช้เป็น baseline ของโครงรับแรงเฉพาะส่วน ผลลัพธ์ขึ้นกับกรณีแรงและวัสดุที่กำหนด

### P27 — A 99 line topology optimization code written in Matlab

Sigmund · 2001 · Structural and Multidisciplinary Optimization · **Next · A** · [แหล่งปฐมภูมิ](https://www.topopt.mek.dtu.dk/apps-and-software/a-99-line-topology-optimization-code-written-in-matlab)

เป็น baseline การลด compliance ที่กะทัดรัดและตรวจเข้าใจได้ ใช้เทียบการค้นหากับวิธีพื้นฐานที่มีประสิทธิภาพ แต่ไม่ใช่ evaluator รถทั้งคัน

### P28 — Gmsh: a three-dimensional finite element mesh generator with built-in pre- and post-processing facilities

Geuzaine & Remacle · 2009 · IJNME · **First · M** · [แหล่งปฐมภูมิ](https://orbi.uliege.be/handle/2268/22742?locale=en)

เป็นฐานการสร้าง mesh สำหรับเส้นทาง CAD สู่ elements จริง รอบนี้ตรวจข้อมูลบรรณานุกรมแล้ว ก่อนเลือกใช้ต้องอ่านเอกสารและทำ benchmark ซ้ำ

### P29 — Incremental Potential Contact: Intersection- and Inversion-free, Large-Deformation Dynamics

Li et al. · 2020 · ACM TOG · **Next · M** · [แหล่งปฐมภูมิ](https://github.com/ipc-sim/IPC)

ตรวจตัว implementation อ้างอิงและข้อมูลบทความด้าน nonlinear contact แล้ว เป็นทางเลือกในอนาคต การไม่ทะลุกันเชิงตัวเลขไม่ได้สอบเทียบแรงเสียดทานหรือความเสียหาย

### P30 — High-Order Incremental Potential Contact for Elastodynamic Simulation on Curved Meshes

Ferguson et al. · 2023 · SIGGRAPH; preprint 2022 · **Later · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2205.13727)

เชื่อม curved elements ลำดับสูงกับ contact ที่ทนทาน เหมาะหลังเส้นทาง mesh CAD พื้นฐานทำงานได้ การรับประกันทางคณิตศาสตร์ไม่ได้ยืนยันว่าวัสดุตรงของจริง

## พลศาสตร์การแข่งขัน สนาม และ optimal control

### P31 — Optimal control for a Formula One car with variable parameters

Perantoni & Limebeer · 2014 · Vehicle System Dynamics · **First · A** · [แหล่งปฐมภูมิ](https://ora.ox.ac.uk/objects/uuid%3Ace1a7106-0a2c-41af-8449-41541220809f)

ผสานพารามิเตอร์รถกับการขับให้ใช้เวลาต่ำสุด เป็นงานอ้างอิงตรงสำหรับความเป็นธรรมของการออกแบบและตัวควบคุม สมมติฐาน F1 ในอดีตไม่ใช่ข้อจำกัดรถของเรา

### P32 — Optimal control of a Formula One car on a three-dimensional track-part 1: track modeling and identification

Perantoni & Limebeer · 2015 · ASME JDSMC · **First · A** · [แหล่งปฐมภูมิ](https://ora.ox.ac.uk/objects/uuid%3A3a7cfbe2-facf-479f-9208-089b1b22b2ae)

สร้างและระบุแบบจำลองสนาม 3D ใช้เปลี่ยนระดับความต้องการสนามแบบจัดอันดับเป็นความโค้ง ความสูง และการเอียงตามตำแหน่ง โดยคุณภาพข้อมูลต้นทางยังสำคัญ

### P33 — Optimal Control of a Formula One Car on a Three-Dimensional Track - Part 2: Optimal Control

Limebeer & Perantoni · 2015 · ASME JDSMC · **Next · A** · [แหล่งปฐมภูมิ](https://pure.uj.ac.za/en/publications/optimal-control-of-a-formula-one-car-on-a-three-dimensional-track-3/)

ใช้ optimal control บนสนาม 3D อ่านร่วม P32 เพื่อทดสอบการเชื่อมสนามและพลศาสตร์ ผล optimization ยังขึ้นกับความถูกต้องของโมเดลที่ป้อน

### P34 — Minimum time optimal control simulation of a GP2 race car

Dal Bianco, Lot & Gadola · 2018 issue; online 2017 · VSD · **First · E** · [แหล่งปฐมภูมิ](https://eprints.soton.ac.uk/417133/)

ใช้รถ transient 14-DOF ยางไม่เชิงเส้น และแอโรตาม ride height เทียบ telemetry เป็นเป้าหมายเชื่อมโมเดลที่จับต้องได้ แต่ข้อมูลและค่าที่สอบเทียบ GP2 ไม่ถ่ายทอดมาโดยอัตโนมัติ

### P35 — Optimizing the aero-suspension interactions in a Formula One car

Imani Masouleh & Limebeer · 2016 issue; online 2015 · IEEE TCST · **First · A** · [แหล่งปฐมภูมิ](https://ora.ox.ac.uk/objects/uuid%3A856dd2b0-3df9-4daa-a4f7-9462dc7cd2f8)

ศึกษา geometry ช่วงล่างกับแอโรภายใน optimization ใช้วาง benchmark ride height/downforce/การถ่ายน้ำหนักร่วมกัน โดยโครงช่วงล่าง F1 ที่กำหนดเป็นเพียง baseline

### P36 — Optimal control of Formula One car energy recovery systems

Limebeer, Perantoni & Rao · 2014 · International Journal of Control · **Next · E** · [แหล่งปฐมภูมิ](https://www.anilvrao.com/Publications/JournalPublications/F-1-Optimal-Control-Energy-Recovery.pdf)

จัดสรรการกู้คืนพลังงานร่วมกับการขับเวลาต่ำสุด นำรูปแบบโจทย์ optimal control มาใช้ได้ แต่เพดานกำลังและพลังงานตามกติกาเก่าไม่ใช่กฎปัจจุบัน

### P37 — Optimal energy management for formula-E cars with regulatory limits and thermal constraints

Liu, Fotouhi & Auger · 2020 · Applied Energy · **First · A** · [แหล่งปฐมภูมิ](https://dspace.lib.cranfield.ac.uk/bitstream/1826/15797/1/Optimal_energy_management_for_formula-E_cars_with_regulatory_limits_and_thermal_constraints-2020.pdf)

อุณหภูมิแบตเตอรี่และขีดจำกัดพลังงานเปลี่ยนการควบคุมที่เหมาะสม ใช้วางการเชื่อมพลังงาน/ความร้อนตลอดช่วงแข่ง ผลเทียบรถแต่ละรุ่นในซิมไม่ใช่การวัดระบบของเรา

### P38 — Optimal tyre usage for a Formula One car

Tremlett & Limebeer · 2016 · Vehicle System Dynamics · **First · A** · [แหล่งปฐมภูมิ](https://www.tandfonline.com/doi/abs/10.1080/00423114.2016.1213861)

เชื่อมสภาพยางกับการตัดสินใจตลอดช่วงแข่ง เกี่ยวข้องมากกว่าเวลารอบเดียว รอบนี้อ่านบทคัดย่อที่จัดทำดัชนีจากสำนักพิมพ์ การเปิดหน้าตรงถูกจำกัด

### P39 — Minimum curvature trajectory planning and control for an autonomous race car

Heilmeier et al. · 2020 issue; online 2019 · VSD · **Next · A** · [แหล่งปฐมภูมิ](https://www.tandfonline.com/doi/abs/10.1080/00423114.2019.1631455)

มีวิธีวางเส้นทางและควบคุมรถพร้อมเส้นทางไปยังโค้ดผู้วิจัย เหมาะเป็น baseline เริ่มต้น แต่ความโค้งต่ำสุดไม่เท่ากับเวลารอบต่ำสุด

### P40 — Outracing champion Gran Turismo drivers with deep reinforcement learning

Wurman et al. · 2022 · Nature · **Later · E** · [แหล่งปฐมภูมิ](https://www.nature.com/articles/s41586-021-04357-7)

แสดงตัวควบคุมแข่งที่เรียนรู้ได้ดีในเกม ใช้ศึกษาเทคนิคควบคุมได้ แต่ไม่ได้ยืนยันความตรงของโมเดล F1 จริงหรือการค้นหารูปร่างยานพาหนะ

### P41 — Optimization-Based Autonomous Racing of 1:43 Scale RC Cars

Liniger, Domahidi & Morari · 2015 issue; arXiv 2017 · OCA · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1711.07300)

มี model predictive contouring control สำหรับ baseline ที่ลงมือทำได้ สเกลและสภาพยางต่างกัน ต้องเทียบงบตัวควบคุมกับขีดจำกัด actuator อย่างชัดเจน

### P42 — Analyzing the Impact of Simulation Fidelity on the Evaluation of Autonomous Driving Motion Control

Sagmeister et al. · IEEE IV 2024; arXiv deposit 2026 · **First · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2602.07984)

เปรียบเทียบโมเดลหลาย fidelity กับ telemetry รถแข่งอัตโนมัติจริง เป็นแบบอย่างการตัดโมดูลทดสอบใกล้ขีดจำกัดการยึดเกาะ ปีฝาก arXiv 2026 ไม่ใช่ปีตีพิมพ์ครั้งแรก

## ยางและความร้อนของยาง

### P43 — Tyre Modelling for Use in Vehicle Dynamics Studies

Bakker, Nyborg & Pacejka · 1987 · SAE 870421 · **First · A** · [แหล่งปฐมภูมิ](https://saemobilus.sae.org/papers/tyre-modelling-use-vehicle-dynamics-studies-870421)

เป็นฐานความสัมพันธ์แรงยางที่ fit จากข้อมูล ใช้เริ่ม tyre map จากการวัด สมการไม่มีค่าสัมประสิทธิ์ให้เอง และการ fit steady-state แบบแยกแรงไม่ครอบคลุม combined slip transient ทั้งหมด

### P44 — Magic Formula Tyre Model with Transient Properties

Pacejka & Besselink · 1997 · Vehicle System Dynamics · **First · A** · [แหล่งปฐมภูมิ](https://www.tandfonline.com/doi/abs/10.1080/00423119708969658)

เพิ่มพฤติกรรมยาง transient ในกรอบ Magic Formula เหมาะกับ relaxation และความต้องการแรงร่วม ต้องระบุพารามิเตอร์จากการวัดในเงื่อนไขที่เกี่ยวข้อง

### P45 — An improved Magic Formula/Swift tyre model that can handle inflation pressure changes

Besselink, Schmeitz & Pacejka · 2010 · VSD · **Next · A** · [แหล่งปฐมภูมิ](https://pure.tue.nl/ws/files/3139490/Metis245615.pdf)

ขยายโมเดลยางให้รองรับแรงดันและผลเกี่ยวข้อง ใช้กำหนดขอบเขตแรงดัน/camber ที่โมเดลใช้ได้ พารามิเตอร์ที่เพิ่มต้องมีข้อมูล ไม่ใช่เพิ่มรายละเอียดด้วยการเดา

### P46 — TRT: thermo racing tyre a physical model to predict the tyre temperature distribution

Farroni et al. · 2014 issue; online 2013 · Meccanica · **Next · E** · [แหล่งปฐมภูมิ](https://link.springer.com/article/10.1007/s11012-013-9821-9)

จำลองการกระจายความร้อนยางและเทียบ telemetry สนาม ใช้ศึกษาโครงโมเดลความร้อนได้ แต่ข้อมูลใช้งานที่ปกปิดทำให้ไม่ใช่ชุดสอบเทียบ F1 แบบเปิด

## อากาศพลศาสตร์และ surrogate ที่เรียนรู้

### P47 — Aerodynamics of Race Cars

Katz · 2006 · Annual Review of Fluid Mechanics · **Next · A** · [แหล่งปฐมภูมิ](https://www.annualreviews.org/content/journals/10.1146/annurev.fluid.38.050304.092016)

ทบทวนกลไกอากาศพลศาสตร์รถแข่งและ ground effect ใช้เลือกการทดสอบเหตุและผลกับปฏิสัมพันธ์ แต่บททบทวนไม่ได้ให้แผนที่แอโรที่ยืนยันแล้วสำหรับ geometry ใหม่

### P48 — Spectral/hp element simulation of flow past a Formula One front wing: validation against experiments

Buscariolo et al. · 2019 · arXiv · **First · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1909.06701)

มี benchmark CFD ปีกหน้าที่อ้างอิงการทดลอง เหมาะตรวจแอโรเฉพาะส่วนก่อนกล่าวอ้างรถทั้งคัน ปีกที่ตรวจแล้วไม่ได้ทำให้รถทั้งคันผ่าน

### P49 — DAFoam: An Open-Source Adjoint Framework for Multidisciplinary Design Optimization with OpenFOAM

He et al. · 2020 · AIAA Journal · **Next · A** · [แหล่งปฐมภูมิ](https://mdolab.engin.umich.edu/bibliography/He2020b)

ใช้ adjoint CFD ในการปรับแบบ เป็นทางเลือกปรับรูปร่างแอโรเฉพาะที่ โดยยังต้องตรวจ mesh turbulence เงื่อนไขขอบเขต และอนุพันธ์ adjoint

### P50 — Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design

Palacios et al. · 2013 · AIAA · **Next · A** · [แหล่งปฐมภูมิ](https://su2code.github.io/documents/SU2_AIAA_ASM2013.pdf)

เป็นกรอบ solver แบบเปิดสำหรับหลายฟิสิกส์และการออกแบบ ควรประเมินเป็น backend ด้วย benchmark เดียวกัน การติดตั้ง solver ไม่ใช่หลักฐานความแม่นยำ

### P51 — DrivAerNet: A Parametric Car Dataset for Data-Driven Aerodynamic Design and Prediction

Elrefaie et al. · 2024 · arXiv · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2403.08055)

ข้อมูล CFD รถถนนเชิงพารามิเตอร์ช่วยทดลอง aero surrogate ใช้ศึกษา data pipeline ได้ แต่การกระจาย geometry ไม่ครอบคลุมรถแข่งรูปแบบอิสระ

### P52 — DrivAerNet++: A Large-Scale Multimodal Car Dataset with Computational Fluid Dynamics Simulations and Deep Learning Benchmarks

Elrefaie et al. · 2024 · NeurIPS · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2406.09624)

เป็นชุดข้อมูลรถหลายรูปแบบที่ขยายขึ้นพร้อม benchmark ทำนาย เป็นงานต่อจาก P51 ไม่ใช่การทดลองจริงซ้ำอย่างอิสระ labels จาก CFD ยังมีอคติของ solver/โมเดล

### P53 — CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics

Elrefaie et al. · 2025 preprint; revised 2026-08-20 · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2512.07847)

เปรียบเทียบความแม่น ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate ใช้เป็นรูปแบบประเมินได้ แต่ใช้ DrivAerNet++ เดิมและไม่รับรอง topology ใหม่นอกการกระจาย

## โครงสร้างซิมและการยืนยันทางวิทยาศาสตร์

### P54 — Chrono: An Open Source Multi-physics Dynamics Engine

Tasora et al. · 2016 · LNCS · **Next · M** · [แหล่งปฐมภูมิ](https://projectchrono.org/faq/)

บรรณานุกรมทางการของโครงการยืนยันบทความเอนจินนี้ เป็นตัวเลือก backend พลศาสตร์ทั่วไป ต้องตรวจความเหมาะสมกับ benchmark ไม่ถือว่าชื่อเอนจินรับรอง fidelity

### P55 — Chrono::Vehicle: template-based ground vehicle modelling and simulation

Serban, Taylor, Negrut & Tasora · 2019 · IJVP · **First · A** · [แหล่งปฐมภูมิ](https://www.inderscience.com/info/inarticle.php?artid=97096)

การจำลองรถ multibody แบบแยกโมดูลเป็นเส้นทางเปรียบเทียบสาธารณะที่ครบขึ้น ใช้ template เป็น baseline ควบคุม พร้อมคงการสร้าง topology อิสระไว้ต้นทาง

### P56 — MuJoCo: A physics engine for model-based control

Todorov, Erez & Tassa · 2012 · IROS · **Next · A** · [แหล่งปฐมภูมิ](https://homes.cs.washington.edu/~todorov/papers/TodorovIROS12.pdf)

พลศาสตร์ contact ที่คำนวณได้รวดเร็วช่วยเทียบการฝึกตัวควบคุม แต่ contact หุ่นยนต์ทั่วไปใช้แทนยางแข่ง แอโร หรือความเสียหายวัสดุที่สอบเทียบแล้วไม่ได้

### P57 — OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization

Gray et al. · 2019 · Structural and Multidisciplinary Optimization · **Next · E** · [แหล่งปฐมภูมิ](https://link.springer.com/article/10.1007/s00158-019-02211-z)

จัดระเบียบการวิเคราะห์ที่เชื่อมกันและอนุพันธ์ ใช้ศึกษาโครงเชื่อมการออกแบบ/ควบคุม/พลังงาน/โครงสร้างได้ แต่ framework ไม่ได้เติมฟิสิกส์ที่ขาดให้เอง

### P58 — Bayesian calibration of computer models

Kennedy & O'Hagan · 2001 · JRSS B · **First · A** · [แหล่งปฐมภูมิ](https://rss.onlinelibrary.wiley.com/doi/pdf/10.1111/1467-9868.00294)

แยกความไม่แน่นอนของการสอบเทียบจากความคลาดเคลื่อนของตัวโมเดล ใช้วางแผนข้อมูลจริงได้ แต่สองส่วนอาจแยกไม่ออกหากการทดลองให้ข้อมูลไม่พอ

### P59 — Verification and validation in computational fluid dynamics

Oberkampf & Trucano · 2002 · Progress in Aerospace Sciences · **First · E** · [แหล่งปฐมภูมิ](https://www.sciencedirect.com/science/article/pii/S0376042102000052)

แยกการแก้สมการได้ถูกต้องออกจากการตรงกับการทดลอง เป็นฐานการวัด residual อิสระ การศึกษา convergence และภาษาระดับหลักฐาน

### P60 — Deep Reinforcement Learning at the Edge of the Statistical Precipice

Agarwal et al. · 2021 · NeurIPS · **First · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/2108.13264)

แสดงปัญหาการเปรียบเทียบจากรันน้อยและการรายงานความไม่แน่นอน ใช้กับ seed ช่วงความเชื่อมั่น และสถิติที่ทนทาน แต่ไม่ได้พิสูจน์ว่าอัลกอริทึมของเราชนะ

### P61 — The Formula SAE Tire Test Consortium-Tire Testing and Data Handling

Kasprzak & Gentz · 2006 · SAE 2006-01-3606 · **Next · A** · [แหล่งปฐมภูมิ](https://saemobilus.sae.org/papers/formula-sae-tire-test-consortium-tire-testing-data-handling-2006-01-3606)

อธิบายการร่วมทดสอบยางและจัดข้อมูล ใช้วางการเก็บข้อมูลทดลองได้ แต่สิทธิ์เข้าถึง consortium และความเหมาะสมของยางต้องตรวจแยก

### P62 — Autonomous Racing using Learning Model Predictive Control

Rosolia, Carvalho & Borrelli · 2016 · arXiv · **Next · A** · [แหล่งปฐมภูมิ](https://arxiv.org/abs/1610.06534)

ใช้ประสบการณ์แข่งก่อนหน้าปรับ predictive control เป็นคู่เทียบการเรียนรู้ตัวควบคุมได้ ความปลอดภัยและการพัฒนาขึ้นอยู่กับสมมติฐานและระบบที่จำลอง

## แหล่งอุตสาหกรรมและเครื่องมือ — ไม่รวมใน 62 papers

### I01 — Mercedes — How Does F1 Simulation Work?

Team article; historical 2020 context · [แหล่งโดยตรง](https://www.mercedesamgf1.com/news/how-does-f1-simulation-work)

อธิบาย computer simulation, driver-in-loop และการเทียบกับสนาม/รถจริง เป็นหลักฐานกระบวนการ ไม่ได้เปิดเพดานความผิดพลาดเชิงตัวเลข

### I02 — McLaren — The secrets of the sim

Team article; historical public description · [แหล่งโดยตรง](https://www.mclaren.com/racing/latest-news/mclarenracing/article/secrets-formula-1-simulator/)

อธิบายการเตรียมซิมและจับคู่สภาพรถ/สนาม สนับสนุนความจำเป็นของการเชื่อมระบบ แต่ไม่เปิดโมเดลภายในที่เป็นกรรมสิทธิ์

### I03 — Dynisma — Ferrari simulator completion

Supplier announcement; 2021-07-07 · [แหล่งโดยตรง](https://www.dynisma.com/news/dynisma-completes-scuderia-ferrari-mission-winnows-new-simulator)

ยืนยันซิมคนขับเฉพาะสำหรับ Ferrari คำกล่าวเรื่อง bandwidth/latency เกี่ยวกับการตอบสนองฮาร์ดแวร์ ไม่ใช่ความแม่นของโมเดลรถทั้งคัน

### I04 — rFpro — Terrain Server

Supplier product description; accessed 2026-09-05 · [แหล่งโดยตรง](https://rfpro.com/simulation-software/terrain-server/)

ระบุรายละเอียดผิวทางแนวราบ 1 cm แนวดิ่ง 1 mm และอัตราป้อนข้อมูลสูงสุด 5 kHz เป็นสเปกข้อมูลผิวทาง ไม่ใช่ความผิดพลาดเวลารอบ F1 หรืออัตรา solver ทั้งระบบ

### I05 — Formula 1 / Rob Smedley — What is correlation?

Official F1 explanation; 2019 · [แหล่งโดยตรง](https://www.formula1.com/en/latest/article/smedley-what-is-correlation.3gcOwCLuQ7rxk4bNeBKf1p)

อธิบายการจับคู่ผลซิมกับรถจริง สนับสนุนการแยกด่าน correlation โดยไม่ได้ให้เกณฑ์ความแม่นสากลของ F1

### I06 — Fastest-lap

Author-maintained open-source project · [แหล่งโดยตรง](https://github.com/juanmanzanero/fastest-lap)

มี optimization เวลารอบต่ำสุดและตัวอย่างรถแบบเปิด เหมาะทำซ้ำเป็น baseline แต่ตัวอย่าง F1 แบบเปิดไม่ใช่ซิมภายในทีม

### I07 — MFeval — Equation source

Implementation author's documentation · [แหล่งโดยตรง](https://mfeval.wordpress.com/equation-source/)

อธิบายแหล่งสมการและการแก้สมการ Magic Formula ใช้ตรวจ implementation ข้ามกันได้ สมการแยกจากค่าสัมประสิทธิ์ยางที่ต้องวัดหรือมีสิทธิ์ใช้งาน

### I08 — Milliken Research — FSAE Tire Test Consortium

Data-owner information · [แหล่งโดยตรง](https://www.millikenresearch.com/fsaettc.html)

เป็นช่องทางศึกษาสิทธิ์ข้อมูลยางและแนวปฏิบัติทดสอบ รอบนี้ไม่ได้เข้าถึง ซื้อ หรือรับสิทธิ์ข้อมูล และไม่ถือว่ายางเทียบเท่า F1
