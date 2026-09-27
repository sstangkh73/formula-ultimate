# รายงานสังเคราะห์ paper ทั้งคลังสำหรับ Formula Ultimate

English source: `FULL_LIBRARY_SYNTHESIS_2026-09-28.md`

วันที่อ่าน: 2026-09-28 (Asia/Bangkok)

## ขอบเขตและวิธี

รายงานนี้ครอบคลุม PDF ทุกฉบับที่มีอยู่ใน `papers/` ณ เวลาสกัด: **261 ฉบับ, 6,280 หน้า, ประมาณ 3,503,351 คำที่สกัดได้** อ่าน full text ทีละหน้าและสร้าง reading manifest ที่ผูก source path, SHA-256, page coverage, section cue และ evidence-cue page จากนั้นสังเคราะห์ผลตาม 15 หัวข้อของคลัง

ใช้ระดับความลึกสองชั้น: paper ที่มีผลต่อการตัดสินใจสูง 15 ฉบับได้รับ deep review ที่ระบุวิธี ตัวเลข ผล ข้อจำกัด เลขหน้า และ proposal เฉพาะ ส่วนอีก 246 ฉบับได้รับ full-text transfer record ที่ผูกข้อค้นพบที่คัดสรรกับ target, experiment/control และเกณฑ์ผ่าน/ล้มเหลวเฉพาะหัวข้อ จึงไม่ควรอ่าน record ชั้นหลังว่าเทียบเท่า critical replication

ข้อจำกัดสำคัญ: การอ่าน paper ไม่ใช่การ replicate ผล การคำนวณหรือการทดลองของผู้เขียนยังไม่ได้รันซ้ำ และผลจาก simulation/benchmark/review ไม่ถูกยกระดับเป็น physical validation ของ Formula Ultimate

PDF 6 ฉบับมี text coverage ต่ำกว่า 95% จึง render และตรวจหน้าที่มีข้อความน้อย พบว่าเป็นหน้าภาพล้วน (field CFD, ตารางภาพ geometry, diagram หรือภาพชุดข้อมูล) หรือหน้าท้ายว่าง ไม่ใช่เนื้อความสแกนที่อ่านตกหล่น และไม่มี PDF ใดถูกจัดว่าเป็นสแกนที่อ่านไม่ได้

## ข้อสรุปรวม

1. งานทั้งหมดสนับสนุนให้ Formula Ultimate คงเป้าหมายแบบ open-ended แต่ **ต้องเปิดกว้างภายใน constraint และ evidence gate ที่ชัด** ไม่ใช่ปล่อย generator ไม่มีขอบเขต
2. ประเด็นร่วมที่แรงที่สุดคือ **representation, evaluator และ budget เป็นส่วนหนึ่งของผลการค้นพบ** ไม่ใช่รายละเอียด implementation ที่ละเลยได้
3. geometry ที่ดูใหม่ต้องผ่านลำดับ: สร้างได้จริง -> มี causal physical response -> ทำงานใน assembly/vehicle -> ดีกว่า baseline ที่ optimize อย่างยุติธรรม -> รอด higher fidelity/holdout -> จึงพิจารณาความใหม่ภายนอก
4. ช่องว่างเร่งด่วนที่สุดยังตรงกับ roadmap ปัจจุบัน: tyre/contact transient, aero field, energy/thermal endurance, independently recovered structural evidence, tolerance/fatigue และ coupled whole-vehicle replay
5. AI agent และ generative model ควรเพิ่มอัตราการเสนอและซ่อม artifact แต่ห้ามเป็นผู้ตัดสินความถูกต้องของ artifact ที่ตัวเองสร้าง
6. QD/multifidelity เหมาะกับโจทย์ แต่ต้องมี descriptor versioning, uncertainty, false-negative audit, resource ledger และ untouched holdout
7. ข้อมูลสาธารณะใช้ calibrate, pretrain และตรวจ pipeline ได้ แต่ต้องประกาศ domain shift และกันข้อมูลโครงการไว้ทดสอบอิสระ
8. งานแข่งอัตโนมัติชี้ว่าต้องมี controller baseline ที่แข็งแรง มิฉะนั้นอาจให้เครดิตรูปร่างรถกับความต่างของ controller

## ลำดับการปรับปรุงที่เสนอ

1. **ทำ evaluator ให้เชื่อถือได้ก่อนเพิ่ม search:** ปิดช่องว่าง field equilibrium/contact/tyre/aero/thermal-energy และบันทึก invalid/numerical failure เป็นผล
2. **เชื่อม transient ทั้งรถ:** รวม vehicle, tyre, aero, energy, brake, thermal และ controller ใน objective เวลารวมการแข่งขัน พร้อม finish gate
3. **ทำ search ให้ยุติธรรม:** matched seed/compute/evaluator access, controller-allocation fairness, fixed-topology optimized baselines และ resource accounting
4. **ทำ multifidelity promotion ให้ตรวจสอบได้:** uncertainty envelope, discrepancy model, stratified audit และ independent replay
5. **เพิ่ม evidence จากของจริงตามลำดับ:** specimen -> connection/subsystem -> assembly -> vehicle โดยห้ามข้ามระดับด้วย claim จาก simulation
6. **แยก claim สี่ชนิด:** geometric novelty, causal functional difference, performance superiority และ external technology novelty

## OE: การค้นพบแบบ open-ended การออกแบบเชิงวิวัฒนาการ และการออกแบบรูปร่างร่วมกับการควบคุม

**ขอบเขต:** งานที่ค้นหาโครงสร้างร่างกาย/topology ร่วมกับพฤติกรรม หรือศึกษาว่าอะไรทำให้การค้นหาการออกแบบแบบ open-ended ได้ผล ใกล้กับวัตถุประสงค์การค้นพบของโครงการที่สุด แต่ไม่มีงานใดยืนยันรถแข่งได้

**สิ่งที่พบข้าม paper**
- topology ของร่างกาย การเรียนรู้ตัวควบคุม และความยากของสภาพแวดล้อมมีปฏิสัมพันธ์กัน การประเมินร่างใหม่ด้วยตัวควบคุมที่ยังฝึกไม่พอจะคัดทิ้ง morphology ที่อาจมีประโยชน์อย่างเป็นระบบ
- generative encoding, graph grammar และ differentiable refinement มี search bias ต่างกัน ไม่มี representation ใดเป็นกลาง จึงต้อง audit coverage ของ representation ด้วย
- งานตัวอย่างที่แข็งแรงที่สุดปิด sim-to-real loop บางส่วนด้วยการผลิตหรือทดสอบจริง ความใหม่ในโลกเสมือนอย่างเดียวไม่ใช่ claim การค้นพบเทคโนโลยี

**สิ่งที่น่าสนใจ**

- [OE-002](by_paper/OE-002_review.th.md): ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0
- [OE-016](by_paper/OE-016_review.th.md): paper แยก controller-adaptation lag เป็น selection bias: ลูกที่โครงสร้างมีศักยภาพอาจดูแย่เพียงเพราะรับ controller ที่เฉพาะกับ parent มา (หน้า 5)
- [OE-029](by_paper/OE-029_review.th.md): วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ

ชุด 33 ฉบับมี evidence profile หลักคือ การศึกษา optimization/search (29), หลักฐานเชิงประจักษ์/การทดลอง (24), การศึกษา control/learning (23), หลักฐาน simulation/เชิงตัวเลข (14), หลักฐานการทดสอบกายภาพ (8), ชุดข้อมูล/benchmark (8), งานทบทวน/สังเคราะห์ (2), หลักฐานคณิตศาสตร์/เชิงรูปนัย (2) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- เพิ่มความยุติธรรมในการจัดสรรการฝึกตัวควบคุมและการปกป้อง morphology ใหม่ในตัวจัดตารางค้นหาของ Work 124
- เปรียบเทียบ representation แบบ direct, generative, graph และ continuous refinement ด้วยงบคำนวณและสิทธิ์เข้าถึง evaluator เท่ากัน
- บังคับใช้ physical-correlation gate จาก Works 131-133 ก่อนเลื่อน morphology ที่ไม่ธรรมดาออกจากระดับ simulation

**รายงานรายฉบับและข้อค้นพบหลัก**
- [OE-001: Evolving Virtual Creatures](by_paper/OE-001_review.th.md) — ตัวอย่างต้นแบบของการวิวัฒนาการกราฟร่างกายพร้อมตัวควบคุม งาน typed genome และ topology mutation (Works 093-094) สืบทอดแนวคิดนี้
- [OE-002: Automatic design and manufacture of robotic lifeforms](by_paper/OE-002_review.th.md) — ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0
- [OE-004: Evolution Gym: A Large-Scale Benchmark for Evolving Soft Robots](by_paper/OE-004_review.th.md) — benchmark การออกแบบร่วมที่กำหนดงานและงบคำนวณคงที่ ใช้เป็นแบบวินัยการเปรียบเทียบ GRID/RANDOM/EVOLUTION/QD อย่างยุติธรรม
- [OE-005: Neural Graph Evolution: Towards Efficient Automatic Robot Design](by_paper/OE-005_review.th.md) — นำตัวควบคุมแบบ graph network กลับมาใช้ข้ามการกลายพันธุ์ของรูปร่างเพื่อลดต้นทุนฝึกใหม่ เกี่ยวข้องเมื่อทุก topology ต้องมีผู้ขับที่ปรับแล้วของตัวเอง
- [OE-006: Embodied Intelligence via Learning and Evolution](by_paper/OE-006_review.th.md) — แสดงว่าความซับซ้อนของสภาพแวดล้อมกำหนดรูปร่างที่วิวัฒนาการได้ (DERL) เป็นทั้งหลักฐานและวิธีทดสอบ H3 ข้ามสภาพสนามแข่ง
- [OE-007: DiffAqua: A Differentiable Computational Design Pipeline for Soft Underwater Swimmers with Shape Interpolation](by_paper/OE-007_review.th.md) — การออกแบบรูปทรงร่วมกับการควบคุมแบบ differentiable เป็นแบบสำหรับการปรับละเอียดด้วย gradient ภายใน topology ที่ผ่านแล้ว ไม่ใช่การเปลี่ยน topology
- [OE-008: Multi-Objective Graph Heuristic Search for Terrestrial Robot Design](by_paper/OE-008_review.th.md) — การค้นหาการออกแบบแบบกราฟไม่ต่อเนื่องภายใต้วัตถุประสงค์ที่ขัดกัน เป็นตัวเทียบสำหรับเวลาแข่ง พลังงาน มวล และความน่าเชื่อถือแบบหลายวัตถุประสงค์ (H2)
- [OE-009: Racing a Wheeled Quadruped: Active Load Transfer Mitigation via Model Predictive Control](by_paper/OE-009_review.th.md) — การแข่งจริงของสถาปัตยกรรมจุดสัมผัสพื้นที่ไม่ธรรมดา ได้เวลาต่อรอบดีขึ้นจากกลไกขาแบบ active เป็นงานตีพิมพ์ที่ใกล้กับรูปร่างรถแข่งที่ไม่ใช่รถยนต์มากที่สุด
- [OE-010: Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions](by_paper/OE-010_review.th.md) — วิวัฒนาการสภาพแวดล้อมร่วมกับคำตอบ ใช้ทำสนามแบบ curriculum ได้ โดยสนามประเมินแบบ held-out ต้องคงที่
- [OE-011: Enhanced POET: Open-Ended Reinforcement Learning through Unbounded Invention of Learning Challenges and their Solutions](by_paper/OE-011_review.th.md) — เพิ่มตัววัดความใหม่ที่ไม่ผูกกับโดเมนและการถ่ายโอนระหว่างคู่สภาพแวดล้อม-คำตอบ เกี่ยวข้องกับการวัดความใหม่ของสภาพแวดล้อมอย่างซื่อตรง
- [OE-012: Reality-assisted evolution of soft robots through large-scale physical experimentation: a review](by_paper/OE-012_review.th.md) — ทบทวนการนำการทดลองจริงเข้าไปในวงวิวัฒนาการ ให้ข้อมูลกับโปรแกรม physical correlation (Works 131-133)
- [OE-013: Evolving Neural Networks through Augmenting Topologies](by_paper/OE-013_review.th.md) — NEAT: historical marking, speciation และการเพิ่มความซับซ้อนสำหรับวิวัฒนาการ topology กราฟ เป็นคำตอบมาตรฐานของการผสมข้าม topology ที่ต่างกัน (Work 094)
- [OE-016: Scalable Co-Optimization of Morphology and Control in Embodied Machines](by_paper/OE-016_review.th.md) — **deep review** — เมื่อปกป้อง morphology ค่า fitness เฉลี่ยเพิ่มจาก 18.715 ที่ generation 0 เป็น 22.916 ที่ generation 5,000 (p < 0.001) ส่วนการปกป้องทางเลือกไม่ดีกว่าแบบไม่ปกป้อง (p = 0.240) และแย่กว่า morphology protection อย่างมีนัยสำคัญ (p = 1.211e-4) (หน้า 4)
- [OE-017: Environmental influence on the evolution of morphological complexity in machines](by_paper/OE-017_review.th.md) — วัดว่าสภาพแวดล้อมกำหนดความซับซ้อนของรูปร่างที่วิวัฒนาการได้อย่างไร เป็นแหล่งวิธีโดยตรงสำหรับ H3
- [OE-020: Efficient automatic design of robots](by_paper/OE-020_review.th.md) — การออกแบบทั้งร่างด้วย gradient ได้ภายในไม่กี่วินาทีแล้วสร้างจริง เป็นเกณฑ์ว่าการค้นหา topology เร็วได้แค่ไหนเมื่อมีฟิสิกส์แบบ differentiable
- [OE-021: Reinforcement Learning for Improving Agent Design](by_paper/OE-021_review.th.md) — เรียนรู้พารามิเตอร์ร่างกายร่วมกับ policy และแสดงว่าตัว optimizer ใช้ความอิสระของร่างกายแบบไม่คาดคิด เป็นคำเตือนสำหรับการตรวจวัตถุประสงค์ของเรา
- [OE-022: Jointly Learning to Construct and Control Agents using Deep Reinforcement Learning](by_paper/OE-022_review.th.md) — policy ที่ขึ้นกับการออกแบบใช้ร่วมกันทั้งการกระจายของแบบ เป็นวิธีเฉลี่ยต้นทุนการปรับผู้ขับข้ามรถหลายแบบ
- [OE-023: Data-efficient Co-Adaptation of Morphology and Behaviour with Deep Reinforcement Learning](by_paper/OE-023_review.th.md) — ใช้ value function ที่เรียนรู้ประเมินแบบใหม่โดยไม่ต้องรันเต็ม เกี่ยวข้องกับการคัดกรองราคาถูกก่อนการแข่ง Level-0
- [OE-024: Transform2Act: Learning a Transform-and-Control Policy for Efficient Agent Design](by_paper/OE-024_review.th.md) — policy ที่แก้กราฟร่างกายก่อนแล้วจึงควบคุม เป็นทางเลือกแทนการกลายพันธุ์ topology เชิงวิวัฒนาการที่ควรเทียบที่งบเท่ากัน
- [OE-025: An End-to-End Differentiable Framework for Contact-Aware Robot Design](by_paper/OE-025_review.th.md) — การออกแบบที่คำนึงถึงการสัมผัสแบบ differentiable ด้วย cage deformation เกี่ยวข้องกับ ground interaction และเรขาคณิตที่ขับด้วยการสัมผัส
- [OE-026: SoftZoo: A Soft Robot Co-design Benchmark For Locomotion In Diverse Environments](by_paper/OE-026_review.th.md) — benchmark การออกแบบร่วมข้ามหลายสภาพแวดล้อม เป็นแบบการรันการค้นหาเดียวข้ามหลายสภาพสนามแล้วเทียบความเฉพาะ
- [OE-027: Evolution and learning in differentiable robots](by_paper/OE-027_review.th.md) — รวมวิวัฒนาการร่างกายกับการเรียนรู้ตัวควบคุมด้วย gradient ในสเกลใหญ่ ให้ข้อมูลเรื่องการแบ่งการค้นหาไม่ต่อเนื่องกับการปรับละเอียดต่อเนื่อง
- [OE-028: Co-optimising Robot Morphology and Controller in a Simulated Open-Ended Environment](by_paper/OE-028_review.th.md) — การปรับรูปร่างและตัวควบคุมร่วมกันภายใต้สภาพแวดล้อมแบบ POET แสดงปฏิสัมพันธ์ระหว่างการสร้างสภาพแวดล้อมกับการค้นหาร่างกาย
- [OE-029: An Empirical Study on the Computation Budget of Co-Optimization of Robot Design and Control in Simulation](by_paper/OE-029_review.th.md) — วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ
- [OE-030: Convergent Functions, Divergent Forms](by_paper/OE-030_review.th.md) — ศึกษาว่ารูปทรงต่างกันไปถึงหน้าที่เดียวกันได้อย่างไรในการค้นหารูปร่าง เกี่ยวข้องกับการแยกความใหม่ทางรูปลักษณ์ออกจากความใหม่ทางหน้าที่
- [OE-031: Embodied Co-Design for Rapidly Evolving Agents](by_paper/OE-031_review.th.md) — survey ล่าสุดของการออกแบบรูปร่างร่วมกับการควบคุม ตั้งแต่สิ่งมีชีวิตเสมือนถึงหุ่นยนต์จริง เป็นแผนที่วิธีและปัญหาที่ยังเปิดอยู่
- [OE-032: Shaping the Evolutionary Dynamics of Robot Morphology via Adaptive Control Learning](by_paper/OE-032_review.th.md) — ความเร็วการเรียนรู้ของตัวควบคุมกำหนดว่ารูปร่างใดอยู่รอด เกี่ยวข้องกับ bias จากการจัดสรรตัวควบคุมในการค้นหาของเรา
- [OE-033: Shape Your Body: Value Gradients for Multi-Embodiment Robot Design](by_paper/OE-033_review.th.md) — ใช้ gradient ของ value จาก policy หลายร่างเพื่อปรับการออกแบบร่างกาย เป็นตัวเทียบฝั่งการออกแบบต่อเนื่อง
- [OE-034: Seeking Quality Diversity in Evolutionary Co-design of Morphology and Control of Soft Tensegrity Modular Robots](by_paper/OE-034_review.th.md) — quality diversity กับการออกแบบรูปร่าง/การควบคุมร่วม เป็นตัวอย่างก่อนหน้าของ executable morphology archive (Work 099)
- [OE-035: Open-Endedness is Essential for Artificial Superhuman Intelligence](by_paper/OE-035_review.th.md) — นิยาม open-endedness ว่าเป็นความใหม่บวกกับความเรียนรู้ได้สำหรับผู้สังเกต เป็นนิยามที่ใช้ได้สำหรับความหมายของ claim การค้นพบของเรา
- [OE-038: Design Mining Interacting Wind Turbines](by_paper/OE-038_review.th.md) — วิวัฒนาการแบบที่ประเมินด้วยการพิมพ์ 3 มิติและอุโมงค์ลมร่วมกับ surrogate เป็นตัวอย่างการประเมินทางกายภาพในวง
- [OE-039: Keep Rollin' - Whole-Body Motion Control and Planning for Wheeled Quadrupedal Robots](by_paper/OE-039_review.th.md) — การควบคุมการเคลื่อนที่แบบล้อ-ขาผสม แสดงว่าจุดสัมผัสพื้นแบบไม่ธรรมดาต้องการอะไรจากการควบคุม
- [OE-040: Automated Antenna Design with Evolutionary Algorithms](by_paper/OE-040_review.th.md) — เสาอากาศ ST5 ของ NASA ที่ได้จากวิวัฒนาการและขึ้นบินจริง เป็นกรณีหายากที่การออกแบบฮาร์ดแวร์แปลกตาผ่านการรับรองจริง

## AG: LLM และ AI agent สำหรับการออกแบบทางวิศวกรรม โค้ด CAD และการจำลอง

**ขอบเขต:** agent และแบบจำลองเชิงกำเนิดที่เสนอการออกแบบทางวิศวกรรม เขียนโปรแกรม CAD หรือสั่ง solver รวมถึงงานเรื่องการประเมินระบบเหล่านี้ เกี่ยวข้องเพราะผู้ออกแบบของ Formula Ultimate เป็น agent ที่เขียน CadQuery และถูกตัดสินโดยตัวประเมินอิสระ

**สิ่งที่พบข้าม paper**
- LLM agent มีประโยชน์สูงสุดในฐานะตัวเสนอแบบ สร้างโค้ด และจัด workflow เมื่อจับคู่กับ verifier ที่รันได้ ภาษาที่ดูน่าเชื่อไม่ใช่หลักฐานวิศวกรรม
- benchmark CAD และ CAE พบซ้ำ ๆ ว่าความดูสมจริงหรือการใช้เครื่องมือสำเร็จไม่เท่ากับความถูกต้องเชิงหน้าที่ เรขาคณิต หรือ multiphysics
- archive, reflection และการสร้าง candidate เพิ่มตอนทดสอบช่วย search ได้ แต่ evaluation leakage และการตัดสินตัวเองอาจสร้างภาพความก้าวหน้าปลอม

**สิ่งที่น่าสนใจ**

- [AG-003](by_paper/AG-003_review.th.md): coding agent เชิงวิวัฒนาการที่มีฐานข้อมูลโปรแกรมแบบ MAP-Elites และคะแนนที่เครื่องตรวจได้ รวมถึงผลด้านวงจรฮาร์ดแวร์ เป็นสถาปัตยกรรมอ้างอิงของ design agent ของเรา
- [AG-004](by_paper/AG-004_review.th.md): ตั้งคำถามว่าผลดีที่รายงานของการค้นหาเชิงวิวัฒนาการด้วย LLM ยังอยู่หรือไม่เมื่อใช้ baseline และงบที่ยุติธรรม สนับสนุนกฎการพยายามหักล้างและการจับคู่งบของเราโดยตรง
- [AG-026](by_paper/AG-026_review.th.md): โปรแกรมที่สร้างอาจรันได้และตรงรูป nominal หนึ่งจุด แต่ encode ความสัมพันธ์พารามิเตอร์ผิด ทำให้ตระกูล structural response เบี่ยงออก (หน้า 5)

ชุด 43 ฉบับมี evidence profile หลักคือ หลักฐานเชิงประจักษ์/การทดลอง (34), ชุดข้อมูล/benchmark (32), หลักฐาน simulation/เชิงตัวเลข (26), หลักฐานการทดสอบกายภาพ (21), การศึกษา optimization/search (12), งานทบทวน/สังเคราะห์ (11), หลักฐานคณิตศาสตร์/เชิงรูปนัย (10), การศึกษา control/learning (7) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- ไม่ให้ agent มีอำนาจตัดสิน admission: agent เสนอ artifact ได้ แต่ gate ด้าน geometry, physics, provenance และ test ที่ deterministic เป็นผู้ตัดสิน
- เพิ่มชุดงาน CAD/CAE ที่มี hidden negative control การตรวจ artifact จริง และการระบุตำแหน่งความล้มเหลว แทนการให้คะแนนด้วยภาษาธรรมชาติ
- บันทึก prompt, เวอร์ชันเครื่องมือ, retry, ค่า token/compute และผล verifier ใน experiment ledger

**รายงานรายฉบับและข้อค้นพบหลัก**
- [AG-001: Evolution through Large Models](by_paper/AG-001_review.th.md) — LLM เป็นตัวกลายพันธุ์ภายใน MAP-Elites สร้างรูปร่าง Sodarace ที่เคลื่อนที่ได้ในรูปโค้ด เป็นแม่แบบที่ใกล้ที่สุดของ LLM ที่กลายพันธุ์โปรแกรม CadQuery ของรถ
- [AG-002: Mathematical discoveries from program search with large language models](by_paper/AG-002_review.th.md) — FunSearch จับคู่ LLM ผู้เสนอกับตัวประเมินอัตโนมัติที่เชื่อถือได้ การแยกการสร้างออกจากการประเมินตรงกับกฎตัวประเมินอิสระของเรา
- [AG-003: AlphaEvolve: A coding agent for scientific and algorithmic discovery](by_paper/AG-003_review.th.md) — coding agent เชิงวิวัฒนาการที่มีฐานข้อมูลโปรแกรมแบบ MAP-Elites และคะแนนที่เครื่องตรวจได้ รวมถึงผลด้านวงจรฮาร์ดแวร์ เป็นสถาปัตยกรรมอ้างอิงของ design agent ของเรา
- [AG-004: Evolution or Illusion? Rethinking Evaluation in LLM Evolutionary Search](by_paper/AG-004_review.th.md) — ตั้งคำถามว่าผลดีที่รายงานของการค้นหาเชิงวิวัฒนาการด้วย LLM ยังอยู่หรือไม่เมื่อใช้ baseline และงบที่ยุติธรรม สนับสนุนกฎการพยายามหักล้างและการจับคู่งบของเราโดยตรง
- [AG-005: The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery](by_paper/AG-005_review.th.md) — วงจรวิจัยอัตโนมัติครบวง มีประโยชน์หลักจากรูปแบบความล้มเหลวที่บันทึกไว้ (อ้างเกินจริง การรีวิวอ่อน) ซึ่งระดับหลักฐานของเราออกแบบมาเพื่อกันไว้
- [AG-006: How Can Large Language Models Help Humans in Design and Manufacturing?](by_paper/AG-006_review.th.md) — ทดสอบ LLM อย่างเป็นระบบตั้งแต่สร้าง CAD ประเมินสมรรถนะ optimize จนถึงการผลิต แสดงว่าแบบจำลองภาษาล้มเหลวตรงไหนในเรขาคณิตและฟิสิกส์
- [AG-007: Large Language Model Agent as a Mechanical Designer](by_paper/AG-007_review.th.md) — LLM agent ปรับแบบโครงถักด้วยผลจาก FEM และเทียบกับ NSGA-II ที่จำนวนการประเมินเท่ากัน เป็นทั้งวิธีและตัวเทียบความยุติธรรมโดยตรง
- [AG-008: An LLM-enabled Multi-Agent Autonomous Mechatronics Design Framework](by_paper/AG-008_review.th.md) — การออกแบบต้นแบบแมคคาทรอนิกส์จริงด้วยหลาย agent ข้ามโดเมนกล อิเล็กทรอนิกส์ และซอฟต์แวร์ เทียบได้กับไปป์ไลน์ part-to-vehicle หลายโดเมนของเรา
- [AG-009: Physics-in-the-Loop: A Hybrid Agentic Architecture for Validated CAD Engineering Design](by_paper/AG-009_review.th.md) — CAD agent แบบสร้าง-จำลอง-ปรับ ที่ใช้เครื่องมือฟิสิกส์ที่ตรวจสอบแล้วในวงแทนการดูภาพ เป็นรูปแบบเดียวกับวง CadQuery สู่ตัวประเมินของเรา
- [AG-010: Engineering.ai: A Platform for Teams of AI Engineers in Computational Design](by_paper/AG-010_review.th.md) — LLM agent ที่รัน CAD, meshing, การจำลองหลายสาขา และ optimization ในวงปิด เป็นระบบที่เทียบกันได้สำหรับทำ benchmark
- [AG-011: Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback](by_paper/AG-011_review.th.md) — ใช้ผล FEA เป็นสัญญาณป้อนกลับให้ agent ที่เขียน CAD เกี่ยวข้องโดยตรงกับ geometry-structural coupling (Works 082, 138)
- [AG-012: FEABench: Evaluating Language Models on Multiphysics Reasoning Ability](by_paper/AG-012_review.th.md) — benchmark ของ LLM agent ที่ใช้โปรแกรม finite element ตั้งแต่ต้นจนจบ เป็นมาตรวัดว่าเชื่อ agent ในการตั้งค่า solver ได้แค่ไหน
- [AG-013: FEM-Bench: A Structured Scientific Reasoning Benchmark](by_paper/AG-013_review.th.md) — งานเขียนโค้ด FEM ระดับบัณฑิตศึกษาพร้อมการตรวจอัตโนมัติ ใช้ทดสอบ agent ที่เขียนโค้ด element หรือ solver ของเรา
- [AG-014: What Do CAE Simulation Agents Really Need Beyond a Generic Harness?](by_paper/AG-014_review.th.md) — วิเคราะห์ว่า CAE agent ต้องการเครื่องมืออะไรนอกเหนือจาก harness เขียนโค้ดทั่วไป ให้ข้อมูลการออกแบบ interface เครื่องมือ CAD/solver
- [AG-015: VFEAgent: A Multimodal Agent Framework for End-to-End Automated Finite Element Analysis](by_paper/AG-015_review.th.md) — agent ที่ใช้ภาพช่วยตั้งค่า FEA พร้อม benchmark ที่ผู้เชี่ยวชาญให้คะแนนรวมถึง topology optimization เป็นตัวเทียบของการประเมินโครงสร้างอัตโนมัติ
- [AG-016: MechAgents: Large language model multi-agent collaborations can solve mechanics problems, generate new data, and integrate knowledge](by_paper/AG-016_review.th.md) — LLM หลาย agent เขียนและตรวจโค้ด elasticity บน FEniCS แสดงประโยชน์และข้อจำกัดของการแก้ไขตัวเอง
- [AG-017: Large Language and Text-to-3D Models for Engineering Design Optimization](by_paper/AG-017_review.th.md) — รูปทรงรถจาก text-to-3D ที่ optimize แรงต้านจาก CFD ในวงวิวัฒนาการ เกี่ยวข้องโดยตรงกับการสร้างตัวถังที่ให้คะแนนด้วยอากาศพลศาสตร์
- [AG-018: Drag-guided diffusion models for vehicle image generation](by_paper/AG-018_review.th.md) — นำทางแบบจำลองเชิงกำเนิดด้วย surrogate ของแรงต้าน แสดงความเสี่ยงที่การนำทางด้วย surrogate จะให้รางวัลกับความผิดพลาดของ surrogate
- [AG-019: Text-to-CadQuery: A New Paradigm for CAD Generation with Scalable Large Model Capabilities](by_paper/AG-019_review.th.md) — ฝึก LLM ให้เขียน CadQuery โดยตรง เป็นภาษา CAD เดียวกับที่ agent ของเราเขียน มีชุดข้อมูลและสถิติข้อผิดพลาดที่นำมาใช้ได้
- [AG-020: CAD-Recode: Reverse Engineering CAD Code from Point Clouds](by_paper/AG-020_review.th.md) — กู้โปรแกรม CadQuery จาก point cloud พร้อมคลัง CadQuery สังเคราะห์ขนาดใหญ่ เป็นข้อมูลที่ใช้ได้และเป็นการตรวจจากเรขาคณิตกลับเป็นโค้ด
- [AG-021: Generating CAD Code with Vision-Language Models for 3D Designs](by_paper/AG-021_review.th.md) — CADCodeVerify: แบบจำลองเรนเดอร์ผล CAD ของตัวเองแล้วตรวจเอง เป็นการตรวจเบื้องต้นราคาถูกก่อน geometry witness อิสระของเรา
- [AG-022: CADDesigner: Conceptual CAD Model Generation with a General-Purpose Agent](by_paper/AG-022_review.th.md) — agent อเนกประสงค์ที่ให้ข้อวินิจฉัยเป็นโครงสร้างเมื่อสคริปต์ CAD ล้มเหลว เกี่ยวข้องกับการแปลงข้อผิดพลาดของ kernel เป็นข้อมูลป้อนกลับที่ซ่อมได้
- [AG-023: Towards High-Fidelity CAD Generation via LLM-Driven Program Generation and Text-Based B-Rep Primitive Grounding](by_paper/AG-023_review.th.md) — FutureCAD: LLM เขียน CadQuery และผูกการอ้างอิงเข้ากับ primitive ของ B-rep แก้ปัญหาการเลือก face/edge ที่เปราะบางใน CAD ที่สร้างขึ้น
- [AG-024: Clarify Before You Draw: Proactive Agents for Robust Text-to-CAD Generation](by_paper/AG-024_review.th.md) — agent ที่ถามให้ชัดก่อนวาดเมื่อคำขอ CAD ไม่ครบ เกี่ยวข้องกับข้อกำหนด interface แบบมีชนิดสำหรับชิ้นส่วนที่สร้าง
- [AG-025: Test-Time Scaling for CAD Generation via Verifier-Free Consensus Selection](by_paper/AG-025_review.th.md) — เลือกโปรแกรม CAD จากหลายตัวอย่างด้วยฉันทามติ เป็นตัวกรองราคาถูก แต่ฉันทามติไม่ใช่การตรวจทางฟิสิกส์
- [AG-026: CADEngBench: It Looks Like CAD, but Does It Work? Evaluating Parametric Design, Assembly Reasoning, and Physics Simulation](by_paper/AG-026_review.th.md) — **deep review** — การแก้ CAD ที่ให้มาง่ายกว่าการสร้างใหม่มาก แต่ complex edit และ matched linear-static FEA ยังยาก โมเดล assembly มักหาบริเวณถูกแต่หา joint/mating entity ที่บันทึกไว้ไม่ถูก และไม่มีโมเดลใดนำทุกขั้นประเมิน (หน้า 1, 5, 22-23)
- [AG-027: Automated Design Optimization via Strategic Search with Large Language Models](by_paper/AG-027_review.th.md) — การค้นหาเชิงกลยุทธ์ที่นำโดย LLM สำหรับ optimize การออกแบบ เป็นตัวเทียบของการเสนอค่าพารามิเตอร์โดย LLM
- [AG-028: Generative Reliability-Based Design Optimization Using In-Context Learning Capabilities of Large Language Models](by_paper/AG-028_review.th.md) — การสร้างแบบด้วย in-context learning ของ LLM ภายใต้ข้อจำกัดความน่าเชื่อถือ เกี่ยวข้องกับ gate ที่คำนึงถึงความไม่แน่นอน
- [AG-029: From Concept to Manufacturing: Evaluating Vision-Language Models for Engineering Design](by_paper/AG-029_review.th.md) — ประเมิน vision-language model อย่างกว้างในงานออกแบบวิศวกรรม บันทึกว่าตรงไหนเชื่อไม่ได้
- [AG-030: Deep Generative Models in Engineering Design: A Review](by_paper/AG-030_review.th.md) — ทบทวนแบบจำลองเชิงกำเนิดในการออกแบบวิศวกรรม รวมถึงช่องว่างด้านความถูกต้องและสมรรถนะ เป็นแผนที่วิธีสำหรับการเสนอเรขาคณิต
- [AG-031: Beyond Statistical Similarity: Rethinking Metrics for Deep Generative Models in Engineering Design](by_paper/AG-031_review.th.md) — เสนอว่าแบบที่สร้างต้องวัดด้วยการผ่านข้อจำกัด สมรรถนะ และความใหม่ ไม่ใช่ความคล้ายกับข้อมูล สอดคล้องกับเกณฑ์การค้นพบของเรา
- [AG-032: Constraining Generative Models for Engineering Design with Negative Data](by_paper/AG-032_review.th.md) — ฝึกด้วยตัวอย่างที่ไม่ผ่านเพื่อให้ตัวสร้างอยู่ในข้อจำกัด บันทึกการปฏิเสธของเราคือข้อมูลเชิงลบแบบนี้พอดี
- [AG-033: BIKED: A Dataset for Computational Bicycle Design with Machine Learning Benchmarks](by_paper/AG-033_review.th.md) — ชุดข้อมูลการออกแบบยานพาหนะแบบพารามิเตอร์พร้อมป้ายกำกับโครงสร้างและสมรรถนะ เป็นตัวอย่างสาธารณะของข้อมูลการออกแบบยานพาหนะที่มีการตรวจความถูกต้อง
- [AG-034: The impact of AI on engineering design procedures for dynamical systems](by_paper/AG-034_review.th.md) — อภิปรายว่า AI เปลี่ยนกระบวนการออกแบบระบบพลวัตอย่างไร รวมถึงภาระการตรวจสอบ
- [AG-035: Eureka: Human-Level Reward Design via Coding Large Language Models](by_paper/AG-035_review.th.md) — LLM เขียนโค้ดรางวัลสำหรับงานควบคุม เป็นข้อเตือนว่าวัตถุประสงค์ที่ agent เขียนต้องถูกตรึงและตรวจก่อนค้นหา
- [AG-036: RoboMorph: Evolving Robot Morphology using Large Language Models](by_paper/AG-036_review.th.md) — การค้นหาเชิงวิวัฒนาการของรูปร่างหุ่นยนต์แบบโมดูลที่ขับด้วย LLM เป็นคู่เทียบโดยตรงของการกลายพันธุ์ topology ที่นำโดย LLM
- [AG-037: Text2Robot: Evolutionary Robot Design from Text Descriptions](by_paper/AG-037_review.th.md) — จากข้อความสู่หุ่นยนต์ขาที่วิวัฒนาการแล้วสร้างจริง แสดงข้อจำกัดการผลิตที่ต้องมีเพื่อให้ร่างที่สร้างขึ้นสร้างได้จริง
- [AG-038: Large Language Models as Optimizers](by_paper/AG-038_review.th.md) — OPRO: LLM เสนอคำตอบจากประวัติที่มีคะแนน เป็น baseline ของพฤติกรรม LLM ในบทบาท optimizer
- [AG-039: CodeEvolve: an open-source evolutionary framework for algorithmic discovery and optimization](by_paper/AG-039_review.th.md) — framework แบบ AlphaEvolve ที่เป็น open source เป็นตัวอ้างอิงที่รันได้ของการค้นหาเชิงวิวัฒนาการด้วย LLM
- [AG-040: OMNI: Open-endedness via Models of human Notions of Interestingness](by_paper/AG-040_review.th.md) — ใช้ foundation model ตัดสินว่างานใดน่าสนใจ เกี่ยวข้องกับการตัดสินว่ากลไกใหม่ใดควรได้งบประเมิน
- [AG-041: Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents](by_paper/AG-041_review.th.md) — survey ของ LLM scientific agent เป็นบริบทสำหรับวางตำแหน่ง agent ค้นพบทางวิศวกรรม
- [AG-042: LLEMA: Evolutionary Search with LLMs for Multi-Objective Materials Discovery](by_paper/AG-042_review.th.md) — การค้นหาเชิงวิวัฒนาการที่นำโดย LLM ด้านวัสดุ โครงการจำกัดตัวเองไว้ที่วัสดุในแค็ตตาล็อก จึงเป็นบริบทมากกว่าวิธีที่จะนำมาใช้
- [AG-043: Physical Design using Differentiable Learned Simulators](by_paper/AG-043_review.th.md) — optimize การออกแบบผ่านตัวจำลองแบบ graph network ที่เรียนรู้ (airfoil เครื่องมือของไหล) แสดงทั้งความเร็วและความเสี่ยงที่จะถูกใช้ช่องโหว่ของ surrogate

## QD: Quality diversity อัลกอริทึมค้นหา surrogate และ multifidelity

**ขอบเขต:** อัลกอริทึมสำหรับใช้งบประเมินกับผู้สมัครที่หลากหลาย คุณภาพสูง และน่าเชื่อถือ: MAP-Elites และสายต่อยอด novelty search, evolution strategy, Bayesian และ multifidelity optimization และความถ่ายโอนได้จากจำลองสู่ของจริง

**สิ่งที่พบข้าม paper**
- วิธี QD แยกการหาคำตอบดีที่สุดหนึ่งแบบออกจากการส่องให้เห็นหลาย niche ที่มีคุณภาพ ตัวเลือก descriptor เป็นตัวกำหนดว่าความหลากหลายแบบใดมองเห็นได้
- surrogate และ multifidelity ลดการประเมินราคาแพงได้ต่อเมื่อระบุ uncertainty, fidelity discrepancy และ false-negative audit ชัดเจน
- novelty ช่วยเปิด stepping stone ได้ แต่ novelty ที่ไม่มี feasibility และ external-task holdout ไม่ยืนยันการค้นพบที่มีประโยชน์

**สิ่งที่น่าสนใจ**

- [QD-001](by_paper/QD-001_review.th.md): MAP-Elites: เก็บแบบที่ดีที่สุดต่อหนึ่งช่องพฤติกรรม เป็นอัลกอริทึมพื้นฐานของ executable morphology archive (Work 099)
- [QD-003](by_paper/QD-003_review.th.md): นอกจากลด evaluation แล้ว SAIL เปิดเผย encoding bias โดยแผนที่แสดงบริเวณที่ encoding สร้างได้และบริเวณที่ surrogate เรียนง่ายหรือยาก (discussion หน้า 25-26)
- [QD-005](by_paper/QD-005_review.th.md): เอกสารอ้างอิงของการรวมแบบจำลองถูกและแพงโดยไม่เชื่อแบบถูก เป็นรากฐานของบันได fidelity และการตรวจการเลื่อนระดับ

ชุด 31 ฉบับมี evidence profile หลักคือ หลักฐานเชิงประจักษ์/การทดลอง (24), การศึกษา optimization/search (22), หลักฐาน simulation/เชิงตัวเลข (15), ชุดข้อมูล/benchmark (14), การศึกษา control/learning (12), หลักฐานการทดสอบกายภาพ (7), งานทบทวน/สังเคราะห์ (6), หลักฐานคณิตศาสตร์/เชิงรูปนัย (5) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- ใช้ archive ที่ version descriptor และรายงาน archive coverage, QD score, feasible coverage และ descriptor occupancy แยกกัน
- ใช้การเลื่อน fidelity ที่ลงทะเบียนล่วงหน้า พร้อม stratified proxy audit และผล `not_estimable` สำหรับ label fidelity สูงที่ยังไม่ทราบ
- จับคู่งบ QD, objective optimization, random search และ fixed-topology baseline ข้าม seed

**รายงานรายฉบับและข้อค้นพบหลัก**
- [QD-001: Illuminating search spaces by mapping elites](by_paper/QD-001_review.th.md) — MAP-Elites: เก็บแบบที่ดีที่สุดต่อหนึ่งช่องพฤติกรรม เป็นอัลกอริทึมพื้นฐานของ executable morphology archive (Work 099)
- [QD-002: Quality Diversity: A New Frontier for Evolutionary Computation](by_paper/QD-002_review.th.md) — นิยาม quality diversity และแยก coverage, novelty และ quality เป็นศัพท์สำหรับสัญญา design diversity (Work 090)
- [QD-003: Data-Efficient Design Exploration through Surrogate-Assisted Illumination](by_paper/QD-003_review.th.md) — **deep review** — paper รายงานแบบที่หลากหลายและคุณภาพสูงหลายร้อยแบบด้วยจำนวน evaluation ต่ำกว่า MAP-Elites หรือ CMA-ES หลายลำดับขนาดในงาน 2 มิติ และสร้าง illumination map คุณภาพสูงในงาน 3 มิติ (หน้า 1) การสุ่มด้วย UCB เพิ่มความแม่นบริเวณ high-fitness เมื่อเทียบการสุ่มสม่ำเสมอหรือดู variance อย่างเดียว (หน้า 13)
- [QD-004: Covariance Matrix Adaptation MAP-Annealing](by_paper/QD-004_review.th.md) — CMA-MAE ปรับปรุงการค้นหา QD แบบต่อเนื่อง เป็น baseline พารามิเตอร์ต่อเนื่องที่แข็งกว่าเมื่อ MAP-Elites พื้นฐานใช้ได้แล้ว
- [QD-005: Survey of multifidelity methods in uncertainty propagation, inference, and optimization](by_paper/QD-005_review.th.md) — เอกสารอ้างอิงของการรวมแบบจำลองถูกและแพงโดยไม่เชื่อแบบถูก เป็นรากฐานของบันได fidelity และการตรวจการเลื่อนระดับ
- [QD-006: Multi-fidelity Bayesian Optimisation with Continuous Approximations](by_paper/QD-006_review.th.md) — BOCA เลือกทั้งผู้สมัครและ fidelity ตามต้นทุน เกี่ยวข้องเมื่อขนาด mesh หรือ time step เป็น fidelity ที่ควบคุมได้
- [QD-007: Crossing the Reality Gap: a Short Introduction to the Transferability Approach](by_paper/QD-007_review.th.md) — เรียนรู้ว่าพฤติกรรมจำลองใดถ่ายโอนสู่ของจริงได้และ optimize ความถ่ายโอนได้ เป็นแบบสำหรับการคัดเลือกที่คำนึงถึงการเลื่อนระดับ
- [QD-009: Abandoning Objectives: Evolution Through the Search for Novelty Alone](by_paper/QD-009_review.th.md) — novelty search หลุดจากวัตถุประสงค์ที่หลอกลวงได้ เกี่ยวข้องเมื่อเวลาแข่งเพียงอย่างเดียวทำให้การค้นหาติดอยู่กับ layout แบบเดิม
- [QD-011: Using Centroidal Voronoi Tessellations to Scale Up the Multidimensional Archive of Phenotypic Elites Algorithm](by_paper/QD-011_review.th.md) — CVT-MAP-Elites คงขนาดคลังในพื้นที่ descriptor หลายมิติ จำเป็นเมื่อ descriptor ของรถเพิ่มขึ้น
- [QD-012: Covariance Matrix Adaptation for the Rapid Illumination of Behavior Space](by_paper/QD-012_review.th.md) — CMA-ME: emitter แบบ CMA-ES ภายใน MAP-Elites เป็นตัวเทียบ QD มาตรฐาน
- [QD-013: pyribs: A Bare-Bones Python Library for Quality Diversity Optimization](by_paper/QD-013_review.th.md) — ไลบรารี QD อ้างอิงที่มี archive และ emitter เป็นการ implement ที่ทดสอบแล้วสำหรับตรวจทานโค้ด archive ของเรา
- [QD-014: Accelerated Quality-Diversity through Massive Parallelism](by_paper/QD-014_review.th.md) — QDax: QD บน accelerator ด้วย batch ใหญ่ เกี่ยวข้องกับการเทียบบัญชีการคำนวณระหว่างขนาด batch กับจำนวนการประเมิน
- [QD-015: Multi-Objective Quality Diversity Optimization](by_paper/QD-015_review.th.md) — MOME เก็บ Pareto front ต่อช่อง เหมาะกับการแลกเปลี่ยนเวลาแข่ง/พลังงาน/มวล/ความน่าเชื่อถือของ H2 ภายในคลังที่หลากหลาย
- [QD-016: Quality Diversity for Multi-task Optimization](by_paper/QD-016_review.th.md) — การค้นหาเดียวแก้หลายงานที่เกี่ยวข้องโดยแบ่งปัน elite ตรงกับการค้นหาการออกแบบเดียวข้ามหลายสภาพสนามแข่ง
- [QD-017: Multi-Task Multi-Behavior MAP-Elites](by_paper/QD-017_review.th.md) — ขยาย QD หลายงานให้มีพฤติกรรมหลากหลายต่องาน เกี่ยวข้องกับคลังที่เฉพาะตามสภาพแวดล้อม (H3)
- [QD-018: BOP-Elites, a Bayesian Optimisation algorithm for Quality-Diversity search](by_paper/QD-018_review.th.md) — Bayesian optimization สำหรับ QD ที่ใช้การประเมินน้อยมาก เกี่ยวข้องเมื่อการประเมินแต่ละครั้งคือการรัน CFD หรือ FE
- [QD-019: Designing Air Flow with Surrogate-assisted Phenotypic Niching](by_paper/QD-019_review.th.md) — QD ที่ใช้ surrogate ช่วยสำหรับการออกแบบการไหลของอากาศด้วย phenotypic niching เป็นวิธีโดยตรงสำหรับเรขาคณิต aero/การระบายความร้อนที่หลากหลาย
- [QD-020: Prototype Discovery using Quality-Diversity](by_paper/QD-020_review.th.md) — จัดกลุ่มคลัง QD เป็นต้นแบบให้มนุษย์ตรวจ ใช้สรุปว่าตระกูลสถาปัตยกรรมใดเกิดขึ้น
- [QD-021: Robots that can adapt like animals](by_paper/QD-021_review.th.md) — คลัง MAP-Elites ที่คำนวณไว้ถูกนำกลับมาใช้ฟื้นตัวเร็วหลังเสียหาย เป็นแบบการใช้คลังซ้ำเมื่อสภาพเสื่อมลง
- [QD-022: Open-ended search for environments and adapted agents using MAP-Elites](by_paper/QD-022_review.th.md) — MAP-Elites บนสภาพแวดล้อมและ agent ร่วมกัน เกี่ยวข้องกับ curriculum ของสนามและสภาพ
- [QD-023: The CMA Evolution Strategy: A Tutorial](by_paper/QD-023_review.th.md) — tutorial CMA-ES ที่เชื่อถือได้ เป็น optimizer ต่อเนื่องค่าเริ่มต้นสำหรับ baseline topology คงที่ที่ปรับแล้ว
- [QD-025: Practical Bayesian Optimization of Machine Learning Algorithms](by_paper/QD-025_review.th.md) — Bayesian optimization ด้วย Gaussian process แบบใช้งานจริงรวมถึง acquisition ที่คำนึงต้นทุน เป็น baseline สำหรับการปรับพารามิเตอร์ที่แพง
- [QD-026: A Tutorial on Bayesian Optimization](by_paper/QD-026_review.th.md) — tutorial ที่ชัดเจนของ Bayesian optimization รวมถึงกรณี multi-fidelity และมีสัญญาณรบกวน
- [QD-027: Scalable Global Optimization via Local Bayesian Optimization](by_paper/QD-027_review.th.md) — TuRBO Bayesian optimization แบบ trust region สำหรับมิติสูง เป็น baseline ที่แข็งสำหรับปรับรถแบบเดิม
- [QD-028: Bayesian Optimization of Combinatorial Structures](by_paper/QD-028_review.th.md) — BOCS จัดการตัวแปรออกแบบแบบไม่ต่อเนื่องเชิงการจัด เกี่ยวข้องกับการเลือก topology แบบไม่ต่อเนื่อง
- [QD-029: Multi-fidelity optimization via surrogate modelling](by_paper/QD-029_review.th.md) — optimization แบบ multi-fidelity ด้วย co-kriging พร้อมตัวอย่างอากาศพลศาสตร์ เป็นสูตรทางวิศวกรรมแบบคลาสสิก
- [QD-032: A composite neural network that learns from multi-fidelity data: Application to function approximation and inverse PDE problems](by_paper/QD-032_review.th.md) — แบบจำลองโครงข่ายประสาท multi-fidelity เป็นทางเลือกแทน Gaussian process เมื่อข้อมูลมาก
- [QD-033: Efficient Global Optimization of Expensive Black-Box Functions](by_paper/QD-033_review.th.md) — EGO และ expected improvement เป็นรากฐานของ optimization ด้วย surrogate สำหรับการจำลองที่แพง
- [QD-034: Dominated Novelty Search: Rethinking Local Competition in Quality-Diversity](by_paper/QD-034_review.th.md) — แทน archive แบบตารางด้วยการแปลงค่า fitness ตามการแข่งขัน เป็นทางเลือก QD ที่ไม่ต้องใช้ archive สำหรับพื้นที่ descriptor ไร้ขอบเขต
- [QD-035: Aerodynamic Design Exploration through Surrogate-Assisted Illumination](by_paper/QD-035_review.th.md) — paper ด้านอากาศพลศาสตร์ของ SAIL ใช้ CFD ของ airfoil 2 มิติ ใกล้ที่สุดกับการค้นหาพื้นผิว aero ที่หลากหลาย
- [QD-036: Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations](by_paper/QD-036_review.th.md) — physics-informed neural network เป็นตระกูล surrogate ที่ฝังสมการควบคุม เกี่ยวข้องเมื่อข้อมูลมีน้อย

## CAD: การแทนค่า การสร้าง และชุดข้อมูลของ CAD, B-rep และการประกอบ

**ขอบเขต:** วิธีแทนค่า เรียนรู้ และสร้าง solid model ลำดับการสร้าง ข้อต่อ และการประกอบ รวมถึงชุดข้อมูล CAD สาธารณะ เกี่ยวข้องกับ grammar B-rep แบบพารามิเตอร์/อิสระ semantic geometry witness, joint kernel และงาน part resolution (Works 078-096, 135-142)

**สิ่งที่พบข้าม paper**
- การสร้าง CAD ต้องรักษา construction semantics, topology, constraint และความแก้ไขได้ ความคล้ายของภาพหรือระยะ point cloud มองไม่เห็น defect เชิงหน้าที่
- การเรียนรู้ B-rep และ assembly ต้องใช้ความสัมพันธ์ face-edge-loop และ mating ที่ชัดเจน ไม่ใช่เรขาคณิตไร้ลำดับอย่างเดียว
- generation ที่มี execution/verifier ช่วยเพิ่ม validity แต่ไม่แทนหลักฐาน tolerance, interference, material หรือ load path

**สิ่งที่น่าสนใจ**

- [CAD-003](by_paper/CAD-003_review.th.md): เรียนรู้บน topology face/edge/coedge ของ B-rep โดยตรง เป็นตัวเลือก descriptor สำหรับวัดความหลากหลายที่มีความหมายทางกล
- [CAD-013](by_paper/CAD-013_review.th.md): equivalent label ทำให้ความแม่นที่วัดเพิ่มมาก (หน้า 22) แสดงว่า evaluation assembly ต้องแยก geometric equivalence จริงออกจากการยอม joint ผิด
- [CAD-018](by_paper/CAD-018_review.th.md): เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา

ชุด 30 ฉบับมี evidence profile หลักคือ ชุดข้อมูล/benchmark (29), หลักฐานเชิงประจักษ์/การทดลอง (22), หลักฐานการทดสอบกายภาพ (9), การศึกษา optimization/search (8), การศึกษา control/learning (8), หลักฐาน simulation/เชิงตัวเลข (6), งานทบทวน/สังเคราะห์ (5), หลักฐานคณิตศาสตร์/เชิงรูปนัย (1), การศึกษาเชิงเทคนิค/วิธีวิทยา (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- ขยาย geometry-general evaluator ของ Work 138 ด้วยการตรวจ semantic topology, constraint, editability และ assembly mate
- รักษา revision identity จาก geometry ไป mesh ไป reduced model และวัด discrepancy ของ adapter ทุกจุด
- ให้คะแนน CAD ที่สร้างจากงานฟิสิกส์และการผลิต ไม่ใช่ความคล้ายของภาพ render

**รายงานรายฉบับและข้อค้นพบหลัก**
- [CAD-001: DeepCAD: A Deep Generative Network for Computer-Aided Design Models](by_paper/CAD-001_review.th.md) — สร้างลำดับ sketch-and-extrude เป็นการแทนค่าสำหรับเสนอแบบ ผลที่ได้ยังต้องผ่าน gate ทางเดินแรงและกระบวนการผลิตของเรา
- [CAD-002: Text2CAD: Generating Sequential CAD Models from Beginner-to-Expert Level Text Prompts](by_paper/CAD-002_review.th.md) — จากข้อความสู่ลำดับ CAD โดยแบ่งระดับคำสั่ง เป็นข้อมูลและการประเมินอ้างอิงของการเสนอเรขาคณิตจากภาษา
- [CAD-003: BRepNet: A topological message passing system for solid models](by_paper/CAD-003_review.th.md) — เรียนรู้บน topology face/edge/coedge ของ B-rep โดยตรง เป็นตัวเลือก descriptor สำหรับวัดความหลากหลายที่มีความหมายทางกล
- [CAD-004: Fusion 360 Gallery: A Dataset and Environment for Programmatic CAD Construction from Human Design Sequences](by_paper/CAD-004_review.th.md) — ลำดับการสร้าง CAD โดยมนุษย์พร้อมสภาพแวดล้อมการสร้างใหม่ เป็นข้อมูลสำหรับเรียนรู้ prior ของการสร้างชิ้นส่วนที่สมจริง
- [CAD-005: DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation](by_paper/CAD-005_review.th.md) — การแทนรูปทรงแบบ signed distance โดยนัย เป็นทางเลือกของพื้นผิวตัวถังที่เรียบ แต่มีภาระเรื่อง meshing และพิกัดของ feature
- [CAD-006: ABC: A Big CAD Model Dataset For Geometric Deep Learning](by_paper/CAD-006_review.th.md) — แบบ B-rep หนึ่งล้านชิ้นพร้อมเส้นโค้งและพื้นผิวพารามิเตอร์ เป็นแหล่ง benchmark สำหรับทดสอบความทนทานของ geometry kernel
- [CAD-007: UV-Net: Learning from Boundary Representations](by_paper/CAD-007_review.th.md) — สุ่มตัวอย่าง face และ edge ของ B-rep บนโดเมน UV เพื่อเรียนรู้ เป็นตัวเข้ารหัส B-rep ที่ใช้ได้จริงสำหรับ surrogate บนเรขาคณิตต้นฉบับ
- [CAD-008: SolidGen: An Autoregressive Model for Direct B-rep Synthesis](by_paper/CAD-008_review.th.md) — สังเคราะห์ B-rep โดยตรงด้วย indexed boundary representation แสดงวิธีสร้าง topology ที่ถูกต้องโดยไม่มีประวัติการสร้าง
- [CAD-009: SkexGen: Autoregressive Generation of CAD Construction Sequences with Disentangled Codebooks](by_paper/CAD-009_review.th.md) — แยกรหัส topology และเรขาคณิตในลำดับ CAD เกี่ยวข้องกับการแยกการเลือกโครงสร้างออกจากมิติใน genome
- [CAD-010: Hierarchical Neural Coding for Controllable CAD Model Generation](by_paper/CAD-010_review.th.md) — รหัสเชิงลำดับชั้นของ loop, profile และ solid ทำให้แก้บางส่วนได้แบบควบคุม คล้ายการกลายพันธุ์เฉพาะที่ของชิ้นส่วน
- [CAD-011: BrepGen: A B-rep Generative Diffusion Model with Structured Latent Geometry](by_paper/CAD-011_review.th.md) — diffusion บนต้นไม้ B-rep แฝงที่มีโครงสร้าง รวมพื้นผิวอิสระ เป็นตัวเลือกตัวสร้าง solid อิสระ (Work 092)
- [CAD-012: ComplexGen: CAD Reconstruction by B-Rep Chain Complex Generation](by_paper/CAD-012_review.th.md) — สร้าง B-rep ใหม่เป็น chain complex พร้อมข้อจำกัดเชิง topology ชัดเจน เกี่ยวข้องกับการตรวจความสอดคล้องของ topology
- [CAD-013: JoinABLe: Learning Bottom-up Assembly of Parametric CAD Joints](by_paper/CAD-013_review.th.md) — **deep review** — ความแม่น joint-axis ที่รายงานคือ 79.53% ใกล้ผลมนุษย์ 80% และสูงกว่า baseline ที่ทดสอบ (หน้า 1) งาน joint ที่มีรูทำได้ดีกว่า โดย edge length และ entity type สำคัญ ส่วน face area อาจลดผล (ภาคผล หน้า 22-25)
- [CAD-014: AutoMate: A Dataset and Learning Approach for Automatic Mating of CAD Assemblies](by_paper/CAD-014_review.th.md) — ชุดข้อมูลขนาดใหญ่ของ mate ใน CAD จริงและตัวทำนาย mate บน B-rep เป็นข้อมูลสำหรับทดสอบว่า interface ที่สร้างคล้าย mate ทางกลจริงหรือไม่
- [CAD-015: Assemble Them All: Physics-Based Planning for Generalizable Assembly by Disassembly](by_paper/CAD-015_review.th.md) — การวางแผนถอดประกอบด้วยฟิสิกส์พิสูจน์ว่าประกอบได้จริง เป็น gate ความสามารถในการสร้างสำหรับรถหลายชิ้นส่วนที่สร้างขึ้น
- [CAD-016: ASAP: Automated Sequence Planning for Complex Robotic Assembly with Physical Feasibility](by_paper/CAD-016_review.th.md) — การวางแผนลำดับการประกอบพร้อมการตรวจแรงโน้มถ่วงและเสถียรภาพ เกี่ยวข้องกับการส่งมอบการผลิต (Work 130)
- [CAD-017: Geometric Deep Learning for Computer-Aided Design: A Survey](by_paper/CAD-017_review.th.md) — survey การเรียนรู้บนข้อมูล CAD (B-rep ลำดับ การประกอบ) เป็นแผนที่วิธีและชุดข้อมูลที่มีอยู่
- [CAD-018: Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations](by_paper/CAD-018_review.th.md) — เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา
- [CAD-019: TG-Diff: Coupling Discrete Topology Diffusion and Topology-conditioned Geometry Diffusions for B-Rep Generation](by_paper/CAD-019_review.th.md) — สร้าง topology ของ B-rep ก่อนแล้วจึงเรขาคณิต สะท้อนการแบ่ง topology แล้วจึงมิติใน genome ของเรา
- [CAD-020: HiFi-BRep: High-Fidelity Latent Representation for Robust B-Rep Generation](by_paper/CAD-020_review.th.md) — มุ่งความทนทานของ B-rep ที่สร้าง (ปิดสนิท solid ที่ถูกต้อง) เกี่ยวข้องกับ constructive validity gate (Work 095)
- [CAD-021: CADENA: Stepwise CAD Reverse Engineering](by_paper/CAD-021_review.th.md) — กู้ CAD ที่แก้ได้ทีละขั้นจากเรขาคณิต ใช้แปลง mesh หรือ field ที่วิวัฒนาการได้กลับเป็นชิ้นส่วนที่แก้ได้
- [CAD-022: HoLa: B-Rep Generation using a Holistic Latent Representation](by_paper/CAD-022_review.th.md) — พื้นที่แฝงเดียวสำหรับเรขาคณิตและ topology ของ B-rep เป็นงานต่อจาก BrepGen สำหรับเสนอ solid อิสระ
- [CAD-023: AutoBrep: Autoregressive B-Rep Generation with Unified Topology and Geometry](by_paper/CAD-023_review.th.md) — การสร้าง B-rep แบบ autoregressive ด้วย token รวม topology และเรขาคณิต เป็นตัวสร้างทางเลือกที่ควบคุมระดับลำดับได้
- [CAD-025: DTGBrepGen: A Novel B-rep Generative Model through Decoupling Topology and Geometry](by_paper/CAD-025_review.th.md) — แยกการสร้าง topology กับเรขาคณิตของ B-rep อีกหนึ่งข้อมูลเรื่องความถูกต้องเทียบกับความหลากหลาย
- [CAD-026: CAD-MLLM: Unifying Multimodality-Conditioned CAD Generation With MLLM](by_paper/CAD-026_review.th.md) — การสร้าง CAD ที่มีเงื่อนไขหลายรูปแบบ (ข้อความ ภาพ point cloud) เกี่ยวข้องกับการกำหนดเงื่อนไขการเสนอชิ้นส่วนด้วยเรขาคณิตของ interface
- [CAD-027: FlexCAD: Unified and Versatile Controllable CAD Generation with Fine-tuned Large Language Models](by_paper/CAD-027_review.th.md) — การแก้ CAD แบบควบคุมได้ด้วย LLM ในหลายระดับลำดับชั้น คล้ายตัวกลายพันธุ์เชิงลำดับชั้น
- [CAD-028: GenCAD: Image-Conditioned Computer-Aided Design Generation with Transformer-Based Contrastive Representation and Diffusion Priors](by_paper/CAD-028_review.th.md) — การสร้างโปรแกรม CAD จากภาพ เป็นอีกเส้นทางการเสนอแบบที่ยังต้องผ่าน gate ทางกายภาพ
- [CAD-029: Self-Supervised Representation Learning for CAD](by_paper/CAD-029_review.th.md) — embedding ของ B-rep แบบ self-supervised ที่ไม่ต้องใช้ป้ายกำกับ เป็น descriptor ที่ใช้ได้เมื่อข้อมูลวิศวกรรมที่มีป้ายกำกับมีน้อย
- [CAD-033: KDH-CAD: Knowledge-data hybrid CAD learning under data scarcity](by_paper/CAD-033_review.th.md) — รวมความรู้ทางวิศวกรรมกับข้อมูล CAD ที่มีน้อย เกี่ยวข้องเพราะข้อมูลชิ้นส่วนรถมีน้อยและเป็นกรรมสิทธิ์
- [CAD-034: MatchMaker: Automated Asset Generation for Robotic Assembly](by_paper/CAD-034_review.th.md) — สร้างคู่ชิ้นส่วนที่ประกบกันพร้อมระยะเผื่อสำหรับการประกอบ เกี่ยวข้องกับการสร้างระยะเผื่อและ fit ของ interface

## ST: Topology optimization, meshing, finite element, contact และตัวเลขของการพัง

**ขอบเขต:** วิธีที่เปลี่ยนเรขาคณิตที่ผ่านแล้วเป็น field ที่แก้แล้วและสถานะการพัง: structural topology optimization, meshing ทรงสี่หน้าที่ทนทาน ปัญหาตรวจสอบ element, contact แบบมีแรงเสียดทาน แบบจำลองการแตกและความล้า การทบทวนของ Work 102 จัดให้การประเมินจากเรขาคณิตสู่ field แบบอิสระเป็นช่องว่างอันดับแรก

**สิ่งที่พบข้าม paper**
- ความน่าเชื่อถือเชิงโครงสร้างขึ้นกับ equilibrium, discretization, constitutive assumption, contact treatment และ convergence ไม่ใช่ค่า stress เดี่ยว
- topology optimization สร้างการวางวัสดุที่มีประโยชน์ได้ แต่ filter, length scale, ข้อจำกัดการผลิต และ mesh dependence กำหนดผลอย่างมาก
- วิธี contact ที่น่าเชื่อถือถือ penetration, friction, solver failure และ non-convergence เป็นผลที่สังเกตได้

**สิ่งที่น่าสนใจ**

- [ST-011](by_paper/ST-011_review.th.md): ตัวสร้าง mesh ของ geometry-mesh bridge (Work 110) ควรอ่านคู่กับเอกสารก่อนเชื่อการตั้งค่าคุณภาพ mesh
- [ST-015](by_paper/ST-015_review.th.md): paper ถือ missed collision และ linearized constraint ที่ infeasible เป็น numerical failure แทนการซ่อนด้วย non-physical fail-safe (หน้า 5, 7)
- [ST-016](by_paper/ST-016_review.th.md): ขยาย IPC ไปยัง mesh โค้งอันดับสูง เกี่ยวข้องเมื่อใช้ mesh ที่ตรงกับ CAD

ชุด 9 ฉบับมี evidence profile หลักคือ หลักฐาน simulation/เชิงตัวเลข (9), ชุดข้อมูล/benchmark (6), การศึกษา optimization/search (3), หลักฐานคณิตศาสตร์/เชิงรูปนัย (2), หลักฐานการทดสอบกายภาพ (2), การศึกษา control/learning (2), งานทบทวน/สังเคราะห์ (1), หลักฐานเชิงประจักษ์/การทดลอง (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- เลื่อนเฉพาะ field solution ที่มี reaction ที่กู้คืนอย่างอิสระ residual history ตำแหน่งพัง และ refinement อย่างน้อยสามระดับที่ลงทะเบียนไว้
- เพิ่ม taxonomy ของ contact/mesh failure และห้าม geometry healing เปลี่ยน candidate identity อย่างเงียบ ๆ
- นำ manufacturing length scale และ uncertainty เข้า structural search ไม่ใช่ใส่หลัง optimize

**รายงานรายฉบับและข้อค้นพบหลัก**
- [ST-003: Efficient topology optimization in MATLAB using 88 lines of code](by_paper/ST-003_review.th.md) — รุ่นต่อจากโค้ด 99 บรรทัดที่เร็วกว่าและมี filter เป็นการ implement อ้างอิงที่ใช้ได้จริงสำหรับ baseline โครงสร้าง 2 มิติ
- [ST-004: Giga-voxel computational morphogenesis for structural design](by_paper/ST-004_review.th.md) — topology optimization ของปีกเครื่องบินทั้งปีกที่ความละเอียดพันล้าน voxel ค้นพบโครงสร้างภายในที่ไม่ธรรมดา ใกล้ที่สุดกับการค้นพบทั้งชิ้นส่วนด้านโครงสร้าง
- [ST-008: An efficient 3D topology optimization code written in Matlab](by_paper/ST-008_review.th.md) — โค้ด topology optimization 3 มิติที่กระชับ เป็น baseline โครงสร้าง 3 มิติสำหรับเทียบระดับชิ้นส่วน
- [ST-009: Current and future trends in topology optimization for additive manufacturing](by_paper/ST-009_review.th.md) — ทบทวนข้อจำกัดการผลิต (overhang ขนาด feature ต่ำสุด support) ใน topology optimization เป็นข้อมูลเข้าของภาษาการผลิต
- [ST-011: Gmsh: A 3-D finite element mesh generator with built-in pre- and post-processing facilities](by_paper/ST-011_review.th.md) — ตัวสร้าง mesh ของ geometry-mesh bridge (Work 110) ควรอ่านคู่กับเอกสารก่อนเชื่อการตั้งค่าคุณภาพ mesh
- [ST-012: Fast Tetrahedral Meshing in the Wild](by_paper/ST-012_review.th.md) — fTetWild สร้าง mesh จาก triangle soup ที่ไม่สมบูรณ์ได้อย่างทนทาน เป็นทางสำรองเมื่อ CAD ที่สร้างไม่สะอาดพอสำหรับ meshing จาก CAD
- [ST-015: Incremental Potential Contact: Intersection- and Inversion-free, Large-Deformation Dynamics](by_paper/ST-015_review.th.md) — **deep review** — วิธีให้ trajectory ที่ไม่ทะลุและไม่ inversion ในตัวอย่างที่รายงาน และแยก tolerance ของ dynamics กับ surface conformation ได้ (หน้า 1) ในกรณี mat เมื่อเพิ่ม resolution จำนวน contact/iteration/memory เพิ่มใกล้เชิงเส้น และเวลาสูงกว่าเชิงเส้นเล็กน้อย (หน้า 16)
- [ST-016: High-Order Incremental Potential Contact for Elastodynamic Simulation on Curved Meshes](by_paper/ST-016_review.th.md) — ขยาย IPC ไปยัง mesh โค้งอันดับสูง เกี่ยวข้องเมื่อใช้ mesh ที่ตรงกับ CAD
- [ST-018: Affine Body Dynamics: Fast, Stable & Intersection-free Simulation of Stiff Materials](by_paper/ST-018_review.th.md) — วัตถุแข็งเกร็งแบบ affine deformation พร้อม contact แบบ IPC เป็นทางเลือกที่เร็วสำหรับการประกอบหลายชิ้น

## SI: โครงสร้างพื้นฐานการจำลอง optimal control และ MDO การเชื่อมโยง และ integrator

**ขอบเขต:** engine solver และภาษาแบบจำลองที่โครงการอาจนำมาใช้หรือใช้ตรวจทาน: multibody dynamics การจำลองแบบ differentiable การเชื่อมโยง co-simulation การจำลองแบบ energy port ไม่มีทิศเหตุ integrator ที่รักษาโครงสร้าง และ solver nonlinear programming ที่ใช้กับปัญหาเวลาต่ำสุด

**สิ่งที่พบข้าม paper**
- simulator แบบ differentiable และ GPU ที่เร็วทำให้ co-design ขนาดใหญ่เป็นไปได้ แต่การมี gradient ไม่ใช่หลักฐานว่า model ใช้ได้กับโจทย์
- contact, deformable, rigid body และ multiphysics มีรูปแบบความล้มเหลวเชิงตัวเลขและภาระ validation ต่างกัน
- benchmark simulator มีความหมายเมื่อเปิดเผย hardware, tolerance, time-step sensitivity และ trade-off ระหว่างความแม่นกับต้นทุน

**สิ่งที่น่าสนใจ**

- [SI-001](by_paper/SI-001_review.th.md): ภาษาการจำลองแบบ differentiable เป็นเส้นทางสู่การปรับละเอียดด้วย gradient ภายใน topology ที่ผ่านแล้ว โดย gradient ไม่ได้พิสูจน์ความแม่นยำ
- [SI-006](by_paper/SI-006_review.th.md): การเชื่อม multiphysics แบบแบ่งส่วน (ของไหล-โครงสร้าง ความร้อนร่วม) พร้อมการเร่งการลู่เข้า เกี่ยวข้องกับงาน thermal-solid แบบเชื่อมโยง (Work 115)
- [SI-020](by_paper/SI-020_review.th.md): error signal สังเกตได้อย่างอิสระที่ interface ไม่ได้สร้างจากการใส่เครื่องหมายลบให้ input ที่กำหนด ตรงกับความต้องการหลักฐาน transferred energy ของโครงการ

ชุด 12 ฉบับมี evidence profile หลักคือ หลักฐาน simulation/เชิงตัวเลข (8), การศึกษา control/learning (6), การศึกษา optimization/search (5), หลักฐานคณิตศาสตร์/เชิงรูปนัย (5), หลักฐานการทดสอบกายภาพ (4), หลักฐานเชิงประจักษ์/การทดลอง (4), งานทบทวน/สังเคราะห์ (2), ชุดข้อมูล/benchmark (2) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- สร้าง evaluator applicability record ต่อ candidate class และบันทึก solver/gradient failure เป็นผลระดับแรกใน ledger
- benchmark runtime พร้อม solution error, conservation residual และ stability ข้าม time-step/mesh refinement
- ใช้ differentiable solver ปรับละเอียดเฉพาะในโดเมนที่ validate แล้ว และคง discrete topology search ภายนอกโดเมนนั้น

**รายงานรายฉบับและข้อค้นพบหลัก**
- [SI-001: DiffTaichi: Differentiable Programming for Physical Simulation](by_paper/SI-001_review.th.md) — ภาษาการจำลองแบบ differentiable เป็นเส้นทางสู่การปรับละเอียดด้วย gradient ภายใน topology ที่ผ่านแล้ว โดย gradient ไม่ได้พิสูจน์ความแม่นยำ
- [SI-005: OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization](by_paper/SI-005_review.th.md) — การจัดการการวิเคราะห์แบบเชื่อมโยงพร้อมอนุพันธ์ เป็นแบบสำหรับการเชื่อมการออกแบบ/การควบคุม/พลังงาน/โครงสร้าง
- [SI-006: preCICE v2: A sustainable and user-friendly coupling library](by_paper/SI-006_review.th.md) — การเชื่อม multiphysics แบบแบ่งส่วน (ของไหล-โครงสร้าง ความร้อนร่วม) พร้อมการเร่งการลู่เข้า เกี่ยวข้องกับงาน thermal-solid แบบเชื่อมโยง (Work 115)
- [SI-007: DOLFINx: The next generation FEniCS problem solving environment](by_paper/SI-007_review.th.md) — สภาพแวดล้อม finite element แบบเปิด เป็น solver อิสระตัวเลือกสำหรับการประเมินเรขาคณิตทั่วไป (Work 138)
- [SI-009: Brax: A Differentiable Physics Engine for Large Scale Rigid Body Simulation](by_paper/SI-009_review.th.md) — ฟิสิกส์บน accelerator แบบขนานจำนวนมาก เกี่ยวข้องกับบัญชีการคำนวณเมื่อเทียบอัลกอริทึมค้นหาด้วยเวลาจริง
- [SI-010: Dojo: A Differentiable Physics Engine for Robotics](by_paper/SI-010_review.th.md) — contact แบบ differentiable ด้วย interior-point complementarity เป็นทางเลือก gradient ผ่าน contact สำหรับ ground interaction
- [SI-011: A pressure field model for fast, robust approximation of net contact force and moment between nominally rigid objects](by_paper/SI-011_review.th.md) — contact แบบ hydroelastic ที่ให้ความดันกระจายแทนแรงจุด เกี่ยวข้องกับ contact patch ของจุดสัมผัสพื้นแบบใดก็ได้
- [SI-012: Discrete mechanics and variational integrators](by_paper/SI-012_review.th.md) — integrator ที่รักษาโครงสร้างโดยมีความคลาดเคลื่อนพลังงานมีขอบเขต เป็นทฤษฎีเบื้องหลังการถือ residual พลังงานเป็นผลลัพธ์ที่สังเกตได้
- [SI-017: CasADi: a software framework for nonlinear optimization and optimal control](by_paper/SI-017_review.th.md) — เครื่องมือเปิดมาตรฐานสำหรับปัญหาเวลาต่อรอบต่ำสุดแบบ direct collocation จำเป็นสำหรับ baseline ผู้ขับที่ optimize แล้ว
- [SI-018: On the implementation of an interior-point filter line-search algorithm for large-scale nonlinear programming](by_paper/SI-018_review.th.md) — IPOPT เป็น solver NLP ที่งานเวลาต่อรอบต่ำสุดส่วนใหญ่ใช้ ควรรู้พฤติกรรมการลู่เข้าก่อนเชื่อผลรอบ
- [SI-020: Energy conservation and power bonds in co-simulations: non-iterative adaptive step size control and error estimation](by_paper/SI-020_review.th.md) — **deep review** — ใน linear benchmark ที่รายงาน adaptive step จาก residual energy ลด residual energy ประมาณ 90% และการแบ่ง subsystem อีกแบบให้ error สูงกว่า แสดงว่า coupling topology มีผล (หน้า 10-11)
- [SI-021: Co-simulation: State of the art](by_paper/SI-021_review.th.md) — survey การจัดการ ความเสถียร และความแม่นยำของ co-simulation เป็นพื้นหลังของการเชื่อมแบบจำลองระบบย่อยจำนวนมาก

## LT: Optimal control เวลาต่อรอบต่ำสุด พลวัตยานยนต์ สนามแข่ง และการ optimize การออกแบบร่วมกับการควบคุม

**ขอบเขต:** วิธีขับรถแข่งอย่างเหมาะที่สุด และวิธี optimize พารามิเตอร์การออกแบบร่วมกับการขับนั้น เป็นฝั่งตัวประเมินของโครงการ รถที่ไม่ธรรมดาจะถูกตัดสินอย่างยุติธรรมได้ก็ต่อเมื่อมีผู้ขับที่ optimize แล้วบนสนามเชิงพื้นที่

**สิ่งที่พบข้าม paper**
- การ optimize เวลาต่อรอบต่ำสุดเชื่อม state ของรถ control path constraint ขีดจำกัดยาง และข้อจำกัด power/energy ค่าสูงสุดแยกส่วนใช้แทนได้ไม่ดี
- การปรับ design และ control พร้อมกันเปลี่ยน hardware ที่เหมาะ เพราะตัวควบคุมใช้ประโยชน์หรือเปิดเผย trade-off ของชิ้นส่วน
- numerical transcription, scaling, initialization และการบังคับ constraint มีผลโดยตรงต่อความน่าเชื่อถือของรอบที่คำนวณ

**สิ่งที่น่าสนใจ**

- [LT-001](by_paper/LT-001_review.th.md): การควบคุมเวลาต่อรอบต่ำสุดโดยให้พารามิเตอร์รถเป็นตัวแปร optimize เป็นแม่แบบของความยุติธรรมระหว่างการออกแบบกับผู้ขับ
- [LT-005](by_paper/LT-005_review.th.md): aero กับ suspension optimize เป็น peak metric แยกกันไม่ได้ เพราะ controller เปลี่ยน ride/roll ตลอด lap และเลื่อน operating point ของ aero
- [LT-032](by_paper/LT-032_review.th.md): การ optimize เวลาต่อรอบแบบเส้นแข่งอิสระที่มีประสิทธิภาพล่าสุด เกี่ยวข้องกับต้นทุนการให้ผู้ขับที่ optimize แล้วแก่ทุกผู้สมัคร

ชุด 11 ฉบับมี evidence profile หลักคือ การศึกษา control/learning (11), หลักฐาน simulation/เชิงตัวเลข (7), หลักฐานเชิงประจักษ์/การทดลอง (6), การศึกษา optimization/search (1), หลักฐานคณิตศาสตร์/เชิงรูปนัย (1), หลักฐานการทดสอบกายภาพ (1), ชุดข้อมูล/benchmark (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- แทนคะแนน subsystem ที่แยกกันด้วยวัตถุประสงค์ lap transient แบบ coupled ที่รักษาข้อจำกัดยาง พลังงาน ความร้อน เบรก และเสถียรภาพ
- audit feasibility ของ optimal control ด้วยการ replay control ใน forward simulation ที่ตั้งค่าอย่างอิสระ
- เทียบ co-design กับ fixed-topology baseline ที่ optimize แล้วภายใต้สนาม energy profile seed และ compute เดียวกัน

**รายงานรายฉบับและข้อค้นพบหลัก**
- [LT-001: Optimal control for a Formula One car with variable parameters](by_paper/LT-001_review.th.md) — การควบคุมเวลาต่อรอบต่ำสุดโดยให้พารามิเตอร์รถเป็นตัวแปร optimize เป็นแม่แบบของความยุติธรรมระหว่างการออกแบบกับผู้ขับ
- [LT-002: Optimal control of a Formula One car on a three-dimensional track-part 1: track modeling and identification](by_paper/LT-002_review.th.md) — สร้างและระบุ ribbon ของสนาม 3 มิติ (ความโค้ง ความสูง ความเอียง) จากข้อมูล เป็นคู่มือการแทนที่สนามสังเคราะห์ของเรา
- [LT-004: Minimum time optimal control simulation of a GP2 race car](by_paper/LT-004_review.th.md) — รถ 14 DOF ยางไม่เชิงเส้น aero ตามความสูงตัวถัง และเทียบกับ telemetry เป็นเป้าหมายแบบจำลองเชื่อมโยงสาธารณะที่ใกล้ที่สุด
- [LT-005: Optimizing the aero-suspension interactions in a Formula One car](by_paper/LT-005_review.th.md) — **deep review** — surrogate error สูงสุดที่รายงานคือ 0.147 mm สำหรับ front ride height และ 0.038° สำหรับ roll บน mesh ที่ทดสอบ เมื่อรวม sensitivity ของ aero ต่อ steer/sideslip เวลาต่อรอบเพิ่มเป็น 83.45 s และ ride height ต่ำที่ความเร็วสูงเพิ่ม downforce ขณะที่ roll ลดมัน (หน้า 6, 11)
- [LT-010: A Curvilinear Abscissa Approach for the Lap Time Optimization of Racing Vehicles](by_paper/LT-010_review.th.md) — สูตรพิกัดเชิงเส้นโค้งที่ solver เวลาต่อรอบยุคใหม่ส่วนใหญ่ใช้ จำเป็นสำหรับตั้งพลวัตที่อิงกับสนามของเรา
- [LT-013: Online Time-Optimal Trajectory Planning on Three-Dimensional Race Tracks](by_paper/LT-013_review.th.md) — การวางแผนเวลาต่ำสุดแบบมวลจุดบนสนาม 3 มิติพร้อมโค้ดเปิด เป็นขั้น fidelity ต่ำราคาถูกของบันได
- [LT-015: GripMap: An Efficient, Spatially Resolved Constraint Framework for Offline and Online Trajectory Planning in Autonomous Racing](by_paper/LT-015_review.th.md) — ข้อจำกัดการยึดเกาะที่แยกตามตำแหน่งสำหรับการวางแผน เป็นโครงสร้างข้อมูลของการยึดเกาะที่ขึ้นกับตำแหน่งบนสนาม
- [LT-023: Minimum-lap-time Control Strategies for All-wheel Drive Electric Race Cars via Convex Optimization](by_paper/LT-023_review.th.md) — ขีดจำกัดการยึดเกาะรายยางกับการขับเคลื่อนสี่ล้อในสูตรรอบแบบ convex เกี่ยวข้องกับการจัดสรรแรงบิดรายล้อ
- [LT-024: Time-optimal Design and Control of Electric Race Cars Equipped with Multi-speed Transmissions](by_paper/LT-024_review.th.md) — เปรียบเทียบเกียร์คงที่ CVT และหลายสปีดพร้อมการควบคุมที่ optimize ร่วม เป็นการประเมินการเลือกสถาปัตยกรรมอย่างยุติธรรม
- [LT-025: Time-optimal Control Strategies for Electric Race Cars with Different Transmission Technologies](by_paper/LT-025_review.th.md) — การเปรียบเทียบเทคโนโลยีเกียร์ภายใต้การควบคุมเวลาต่ำสุดรุ่นก่อน เป็นงานก่อนหน้าของการเทียบสถาปัตยกรรมที่ความพยายามควบคุมเท่ากัน
- [LT-032: A Sequential Convex Programming Approach to Free-trajectory Minimum-lap-time Optimization of Racing Cars](by_paper/LT-032_review.th.md) — การ optimize เวลาต่อรอบแบบเส้นแข่งอิสระที่มีประสิทธิภาพล่าสุด เกี่ยวข้องกับต้นทุนการให้ผู้ขับที่ optimize แล้วแก่ทุกผู้สมัคร

## EN: การจัดการพลังงานในการแข่ง สถาปัตยกรรม powertrain และแหล่งเก็บพลังงาน

**ขอบเขต:** กลยุทธ์การแข่งที่พลังงานจำกัด การควบคุม powertrain ไฮบริดและไฟฟ้า การสังเคราะห์ topology ของ powertrain และแบบจำลองกับข้อมูลวัดของแบตเตอรี่ flywheel และ supercapacitor สนับสนุนสัญญาการแข่งที่พลังงานต้องพกไป typed energy graph และ onboard energy realization (Work 120)

**สิ่งที่พบข้าม paper**
- พลังงานที่ใช้แข่งได้จริงถูกจำกัดด้วย power limit, efficiency map, อุณหภูมิ, state of charge, degradation และมวล containment ไม่ใช่ joule nominal อย่างเดียว
- การจัดการพลังงานที่เหมาะขึ้นกับ trajectory และเชื่อมกับเวลาต่อรอบ thermal state และขนาดชิ้นส่วน
- การเปรียบเทียบที่เท่าเทียมต้องรวม carrier, conversion, cooling และ recovery พร้อม loss ที่สังเกตได้

**สิ่งที่น่าสนใจ**

- [EN-012](by_paper/EN-012_review.th.md): paper ไม่ได้แสดงการกลับอันดับ architecture แบบทั่วไป แต่แสดงเส้นแบ่ง fidelity ที่แคบกว่า: model ง่ายอาจพอสำหรับ sizing แต่ไม่พอสำหรับตีความ trajectory การควบคุมพลังงานที่ optimize
- [EN-016](by_paper/EN-016_review.th.md): co-design ของชิ้นส่วนขับเคลื่อนไฟฟ้าและการควบคุม เป็นวิธีกำหนดขนาดชิ้นส่วนภายใน topology ที่เลือก
- [EN-030](by_paper/EN-030_review.th.md): กลยุทธ์พลังงานไฮบริดเชิงสุ่มที่คำนึงถึงคู่แข่ง เกี่ยวข้องหากเวลาแข่งขึ้นกับปฏิสัมพันธ์ ไม่ใช่รถคันเดียว

ชุด 15 ฉบับมี evidence profile หลักคือ การศึกษา control/learning (9), หลักฐาน simulation/เชิงตัวเลข (6), หลักฐานคณิตศาสตร์/เชิงรูปนัย (6), หลักฐานเชิงประจักษ์/การทดลอง (5), ชุดข้อมูล/benchmark (3), งานทบทวน/สังเคราะห์ (3), การศึกษาเชิงเทคนิค/วิธีวิทยา (2), หลักฐานการทดสอบกายภาพ (2) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- เพิ่ม storage state และ converter map ที่มีขอบเขต power, temperature, degradation และ failure ใน Work 120
- ให้ race-energy profile รวม containment, auxiliary, cooling และ provenance ของ recovery
- optimize การจัดการพลังงานร่วมกับ trajectory และ sizing แล้ว replay สมดุลทั้งหมดอย่างอิสระ

**รายงานรายฉบับและข้อค้นพบหลัก**
- [EN-007: Low-level Online Control of the Formula 1 Power Unit with Feedforward Cylinder Deactivation](by_paper/EN-007_review.th.md) — การควบคุม power unit F1 แบบออนไลน์ แสดงข้อจำกัดเวลาจริงของกลยุทธ์พลังงาน
- [EN-009: Maximum-distance Race Strategies for a Fully Electric Endurance Race Car](by_paper/EN-009_review.th.md) — กลยุทธ์ endurance ภายใต้พลังงานคงที่พร้อมการตัดสินใจเข้าพิท เกี่ยวข้องกับการจัดงบพลังงานตลอดการแข่ง
- [EN-010: Optimal Endurance Race Strategies for a Fully Electric Race Car under Thermal Constraints](by_paper/EN-010_review.th.md) — เพิ่มขีดจำกัดความร้อนของแบตเตอรี่และมอเตอร์ในกลยุทธ์ endurance เป็นการเชื่อม gate ความร้อนกับพลังงานของเราโดยตรง
- [EN-011: Human-in-the-loop Energy and Thermal Management for Electric Racing Cars through Optimization-based Control](by_paper/EN-011_review.th.md) — คำแนะนำด้านพลังงานและความร้อนจากการ optimize ส่งให้ผู้ขับมนุษย์ เกี่ยวข้องกับการที่ผู้ขับจริงทำตามกลยุทธ์ที่เหมาะที่สุด
- [EN-012: Battery model impact on time-optimal co-design for electric racing cars: review and application](by_paper/EN-012_review.th.md) — **deep review** — model ง่ายให้ผล battery sizing สอดคล้องกัน ส่วน model ละเอียดจำเป็นเมื่อต้องการศึกษาวิวัฒนาการตัวแปร control ที่น่าเชื่อถือ ใน model ละเอียด ความต่างเวลาแข่งระหว่าง 24 กับ 25 cell ขนานแทบไม่มี และ convex relaxation อาจให้ profile ตัวแปรพลังงานที่ไม่เป็นกายภาพ (หน้า 1-2, 9, 11)
- [EN-013: Minimum Race-Time Planning-Strategy for an Autonomous Electric Racecar](by_paper/EN-013_review.th.md) — การวางแผนพลังงานและความร้อนตลอดการแข่งของรถแข่งไฟฟ้าพร้อมเครื่องมือเปิด เป็นการ implement อ้างอิงสาธารณะ
- [EN-016: Joint Design and Control of Electric Vehicle Propulsion Systems](by_paper/EN-016_review.th.md) — co-design ของชิ้นส่วนขับเคลื่อนไฟฟ้าและการควบคุม เป็นวิธีกำหนดขนาดชิ้นส่วนภายใน topology ที่เลือก
- [EN-017: Python Battery Mathematical Modelling (PyBaMM)](by_paper/EN-017_review.th.md) — แพ็กเกจแบบจำลองแบตเตอรี่ที่มีสำเนาอยู่แล้วใน private/materials/sources เป็นเอกสารอ้างอิงของแบบจำลองและชุดพารามิเตอร์
- [EN-019: Development of Experimental Techniques for Parameterization of Multi-scale Lithium-ion Battery Models](by_paper/EN-019_review.th.md) — ชุดพารามิเตอร์ที่วัดจากเซลล์ LG M50 (PyBaMM Chen2020) เป็นข้อมูลเซลล์จริงที่ใช้กับแบบจำลองแบตเตอรี่บนรถได้
- [EN-020: An asymptotic derivation of a single particle model with electrolyte](by_paper/EN-020_review.th.md) — หา SPMe เป็นการลดรูปแบบควบคุมได้ของแบบจำลอง DFN เป็นขั้นแบตเตอรี่ fidelity ต่ำที่มีหลักการ
- [EN-021: Lithium-ion battery degradation: how to model it](by_paper/EN-021_review.th.md) — กลไกการเสื่อมที่เชื่อมกันใน PyBaMM เกี่ยวข้องหากแหล่งพลังงานเสื่อมตลอด stint หรือฤดูกาล
- [EN-022: A continuum of physics-based lithium-ion battery models reviewed](by_paper/EN-022_review.th.md) — ทบทวนลำดับชั้นของแบบจำลองเซลล์เชิงฟิสิกส์ เป็นแผนที่การเลือก fidelity ของแบตเตอรี่ต่อ gate
- [EN-023: Parameterization of a Physico-Chemical Model of a Lithium-Ion Battery: I. Determination of Parameters](by_paper/EN-023_review.th.md) — พารามิเตอร์ที่วัดจากเซลล์ Kokam (PyBaMM Ecker2015) เป็นชุดข้อมูลวัดชุดที่สองสำหรับตรวจทานแบบจำลองแบตเตอรี่
- [EN-025: A non-academic perspective on the future of lithium-based batteries](by_paper/EN-025_review.th.md) — ตัวเลขจากภาคอุตสาหกรรมเรื่องความหนาแน่นพลังงานเซลล์และต้นทุนที่ทำได้ เป็นขอบเขตที่สมจริงของผู้สมัครแหล่งเก็บพลังงาน
- [EN-030: Competitors-Aware Stochastic Lap Strategy Optimisation for Race Hybrid Vehicles](by_paper/EN-030_review.th.md) — กลยุทธ์พลังงานไฮบริดเชิงสุ่มที่คำนึงถึงคู่แข่ง เกี่ยวข้องหากเวลาแข่งขึ้นกับปฏิสัมพันธ์ ไม่ใช่รถคันเดียว

## TY: ยาง แรงเสียดทานของยาง และการระบุพารามิเตอร์ยาง

**ขอบเขต:** แบบจำลองแรงยาง พฤติกรรม transient และความร้อน การสึกและการเสื่อม ฟิสิกส์แรงเสียดทานของยาง และการระบุพารามิเตอร์จากข้อมูลทดสอบหรือสนาม ยาง/contact เป็นช่องว่างระดับ A ในการทบทวนของ Work 102 ขณะที่ kernel ปัจจุบันใช้ friction envelope และเส้นทาง slip แบบ tanh

**สิ่งที่พบข้าม paper**
- แรงยางขึ้นกับ combined slip, normal load, camber, pressure, temperature, wear, speed และสภาพถนน friction circle คงที่เป็นเพียง approximation ที่มีขอบเขต
- transient relaxation และ load transfer สำคัญในการขับแข่ง จึงอาจจัดอันดับแบบผิดหากใช้เฉพาะ steady-state map
- model identification และ uncertainty เป็นหัวใจ เพราะพารามิเตอร์ยางขึ้นกับสภาวะและวัดยาก

**สิ่งที่น่าสนใจ**

- [TY-006](by_paper/TY-006_review.th.md): วิธีที่ FSAE TTC วัดและแจกจ่ายข้อมูลยาง เป็นแหล่งข้อมูลยางแข่งจริงที่เข้าถึงได้ง่ายที่สุดสำหรับขอใช้
- [TY-011](by_paper/TY-011_review.th.md): การทดลองเชื่อมการออกแบบ manoeuvre กับ uncertainty เพราะการขับทั่วไปที่ทำได้ง่ายอาจไม่กระตุ้นพารามิเตอร์ที่ racing controller ต้องใช้
- [TY-012](by_paper/TY-012_review.th.md): การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง

ชุด 5 ฉบับมี evidence profile หลักคือ งานทบทวน/สังเคราะห์ (4), การศึกษา control/learning (4), หลักฐานการทดสอบกายภาพ (3), หลักฐานเชิงประจักษ์/การทดลอง (1), หลักฐาน simulation/เชิงตัวเลข (1), การศึกษา optimization/search (1), ชุดข้อมูล/benchmark (1), หลักฐานคณิตศาสตร์/เชิงรูปนัย (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- ยกระดับ ground-interaction contract เป็นแรง combined-slip แบบ transient พร้อม load, temperature, wear และ validity envelope
- calibrate กับข้อมูลที่ประกาศและส่งต่อ uncertainty ของยางไปยังเวลาต่อรอบกับ safety margin
- คง model ง่ายปัจจุบันไว้เป็น low-fidelity gate เท่านั้นและ audit promotion error

**รายงานรายฉบับและข้อค้นพบหลัก**
- [TY-006: The Formula SAE Tire Test Consortium-Tire Testing and Data Handling](by_paper/TY-006_review.th.md) — วิธีที่ FSAE TTC วัดและแจกจ่ายข้อมูลยาง เป็นแหล่งข้อมูลยางแข่งจริงที่เข้าถึงได้ง่ายที่สุดสำหรับขอใช้
- [TY-010: Tire Modeling and Friction Estimation](by_paper/TY-010_review.th.md) — วิทยานิพนธ์เรื่องแบบจำลองยางแบบ brush และการประมาณแรงเสียดทาน เป็นฐานทางฟิสิกส์ของพฤติกรรม combined slip
- [TY-011: Bayesian Optimization-based Tire Parameter and Uncertainty Estimation for Real-World Data](by_paper/TY-011_review.th.md) — **deep review** — วิธีประมาณ distribution ของพารามิเตอร์แทน best fit จุดเดียวและแสดงว่า excitation มีผลต่อความแม่น งานยังพบว่าการ identify เฉพาะพารามิเตอร์ยางอาจแย่กว่าการ identify model เต็ม เตือนว่าห้ามถือพารามิเตอร์รถอื่นว่ารู้แน่ (หน้า 2-3)
- [TY-012: A State-Space Approach to Modeling Tire Degradation in Formula 1 Racing](by_paper/TY-012_review.th.md) — การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง
- [TY-013: Extended Pacejka Tire Model for Enhanced Vehicle](by_paper/TY-013_review.th.md) — ขยายแบบจำลอง Pacejka ด้วยผลเพิ่มเติมสำหรับการจำลองรถ เป็นตัวเทียบของการขยายแบบจำลองยาง

## AE: อากาศพลศาสตร์ การตรวจสอบ CFD ชุดข้อมูล aero และ neural surrogate

**ขอบเขต:** กลไกอากาศพลศาสตร์ของรถแข่ง (ground effect ล้อ wake) กรณี CFD ที่ยึดกับการทดลอง การ optimize รูปทรงแบบ adjoint ชุดข้อมูล CFD ยานยนต์แบบเปิด และ neural surrogate พร้อมข้อจำกัดนอกการกระจายข้อมูล aero เป็นช่องว่างระดับ A/B เพราะยังไม่มีเส้นทางจากเรขาคณิตสู่แผนที่ aero ที่ตรวจสอบแล้ว

**สิ่งที่พบข้าม paper**
- อากาศพลศาสตร์รถขึ้นกับ geometry, attitude, wheel, ground และสภาวะการไหล ค่าสัมประสิทธิ์เดี่ยวซ่อน spatial load และการเลื่อน balance
- ชุดข้อมูล CFD และการทดลองแบบเปิดช่วย surrogate และ validation ได้ แต่โดเมน geometry กับ Reynolds number จำกัดการถ่ายโอน
- shape optimization ต้องพิจารณา drag, downforce, balance, cooling flow, sensitivity และ uncertainty ร่วมกัน ไม่ใช่สัมประสิทธิ์เดียว

**สิ่งที่น่าสนใจ**

- [AE-002](by_paper/AE-002_review.th.md): field resolution ต่ำที่ดูสมจริงอาจให้แนวโน้ม load ผิด จึงต้องตรวจ resolution และ averaging-time sensitivity ไม่ใช่ coefficient ภาพเดียว
- [AE-007](by_paper/AE-007_review.th.md): benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้
- [AE-024](by_paper/AE-024_review.th.md): วัดความล้มเหลวและการปรับตัวของ surrogate กับตระกูลรถใหม่ เกี่ยวข้องโดยตรงเพราะสถาปัตยกรรมใหม่อยู่นอกการกระจายข้อมูล

ชุด 22 ฉบับมี evidence profile หลักคือ หลักฐาน simulation/เชิงตัวเลข (20), ชุดข้อมูล/benchmark (18), หลักฐานเชิงประจักษ์/การทดลอง (17), หลักฐานการทดสอบกายภาพ (8), การศึกษา optimization/search (7), งานทบทวน/สังเคราะห์ (5), การศึกษา control/learning (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- เพิ่ม field/surface aero ที่มาจาก geometry พร้อม sweep ride height, yaw, wheel และ ground effect ใน Work 121 และ coupled vehicle model
- ใช้ public dataset ตรวจ pipeline และ pretrain แล้วกัน geometry/condition ของโครงการเป็น holdout อิสระ
- เลื่อน aero surrogate เมื่อมี uncertainty และ audit ด้วย CFD/การทดลองเป็นระยะเท่านั้น

**รายงานรายฉบับและข้อค้นพบหลัก**
- [AE-002: Spectral/hp element simulation of flow past a Formula One front wing: validation against experiments](by_paper/AE-002_review.th.md) — **deep review** — กรณี order 3 มี resolution ไม่พอ กรณี order 5 ตรงการทดลองด้าน reattachment/flow feature ดีที่สุด ให้ downforce สูงกว่า order 4 อยู่ 4.5% และ lift เสถียรเฉพาะช่วงท้ายของ averaging window (หน้า 8, 16)
- [AE-004: Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design](by_paper/AE-004_review.th.md) — ชุด CFD และการออกแบบ adjoint แบบเปิด เป็น solver ตัวที่สองที่อิสระสำหรับตรวจทาน aero
- [AE-005: DrivAerNet: A Parametric Car Dataset for Data-Driven Aerodynamic Design and Prediction](by_paper/AE-005_review.th.md) — ผล CFD รถแบบพารามิเตอร์หลายพันชุด เป็นข้อมูลฝึก/ตรวจสอบ surrogate แรงต้าน จำกัดที่รูปทรงรถถนน
- [AE-006: DrivAerNet++: A Large-Scale Multimodal Car Dataset with Computational Fluid Dynamics Simulations and Deep Learning Benchmarks](by_paper/AE-006_review.th.md) — กรณี CFD รถหลายรูปแบบกว่า 8,000 กรณีพร้อม benchmark เป็นชุดข้อมูล aero ยานยนต์แบบเปิดที่ใหญ่ที่สุด
- [AE-007: CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics](by_paper/AE-007_review.th.md) — benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้
- [AE-008: DrivAerML: High-Fidelity Computational Fluid Dynamics Dataset for Road-Car External Aerodynamics](by_paper/AE-008_review.th.md) — DrivAer 500 แบบด้วย hybrid RANS-LES ที่ 160 ล้าน cell สัญญาอนุญาตเปิด เป็นข้อมูลอ้างอิง fidelity สูงสำหรับตรวจสอบ surrogate
- [AE-009: AhmedML: High-Fidelity Computational Fluid Dynamics Dataset for Incompressible, Low-Speed Bluff Body Aerodynamics](by_paper/AE-009_review.th.md) — Ahmed body 500 แบบด้วย hybrid RANS-LES เป็น benchmark วัตถุทื่อที่ง่ายกว่าสำหรับทดสอบไปป์ไลน์ aero
- [AE-010: WindsorML: High-Fidelity Computational Fluid Dynamics Dataset For Automotive Aerodynamics](by_paper/AE-010_review.th.md) — LES แบบ wall-modelled ของ Windsor body หลายแบบ (CC-BY-SA) เป็นข้อมูล fidelity สูงแบบเปิดที่รวมผลใกล้พื้น
- [AE-011: Ground Effect Aerodynamics of Race Cars](by_paper/AE-011_review.th.md) — ทบทวนปีก diffuser และล้อใน ground effect พร้อมข้อมูลการทดลอง เป็นฟิสิกส์ของ downforce ที่ขึ้นกับความสูงตัวถัง
- [AE-016: AB-UPT: Scaling Neural CFD Surrogates for High-Fidelity Automotive Aerodynamics Simulations via Anchored-Branched Universal Physics Transformers](by_paper/AE-016_review.th.md) — ขยาย neural surrogate ไปยัง field รถ fidelity สูงเต็มคัน เป็นสถาปัตยกรรม surrogate ตัวเลือก พร้อมข้อควรระวังนอกการกระจายข้อมูล
- [AE-017: Transolver: A Fast Transformer Solver for PDEs on General Geometries](by_paper/AE-017_review.th.md) — transformer แบบ physics-attention สำหรับ PDE บน mesh ใดก็ได้รวมถึงอากาศพลศาสตร์รถ เป็นผู้สมัคร surrogate สำหรับเรขาคณิตทั่วไป
- [AE-018: Geometry-Informed Neural Operator for Large-Scale 3D PDEs](by_paper/AE-018_review.th.md) — GINO ทำนายความดันบนผิวรถจากเรขาคณิต เป็นผล neural operator ด้าน aero รถยุคแรกที่ควรทำซ้ำ
- [AE-019: Learning Mesh-Based Simulation with Graph Networks](by_paper/AE-019_review.th.md) — MeshGraphNets เรียนรู้ฟิสิกส์บน mesh รวมถึงอากาศพลศาสตร์ เป็นฐานของ surrogate เรขาคณิตทั่วไปหลายตัว
- [AE-021: Surrogate Modeling of Car Drag Coefficient with Depth and Normal Renderings](by_paper/AE-021_review.th.md) — surrogate แรงต้านจากภาพพร้อมชุดข้อมูล CFD รถขนาดใหญ่ เป็น surrogate คัดกรองราคาถูกสำหรับเทียบกับ surrogate แบบ field
- [AE-022: Faster by Design: Interactive Aerodynamics via Neural Surrogates Trained on Expert-Validated CFD](by_paper/AE-022_review.th.md) — neural surrogate ที่ฝึกบน CFD รถแข่งที่ผู้เชี่ยวชาญตรวจแล้ว (รวมถึงรถ LMP2) เป็นการศึกษา surrogate รถแข่งที่ใกล้ที่สุด
- [AE-023: Multi-Granularity Conformal Prediction for Reliable Neural-Operator Automotive Aerodynamic Surrogates](by_paper/AE-023_review.th.md) — ขอบเขตความไม่แน่นอนแบบ conformal สำหรับ surrogate aero เป็นวิธีแนบ error bar ที่สอบเทียบแล้วให้การเลื่อนระดับที่ใช้ surrogate
- [AE-024: Adapting Automotive Aerodynamics Surrogates to New Vehicle Families via Transfer Learning](by_paper/AE-024_review.th.md) — วัดความล้มเหลวและการปรับตัวของ surrogate กับตระกูลรถใหม่ เกี่ยวข้องโดยตรงเพราะสถาปัตยกรรมใหม่อยู่นอกการกระจายข้อมูล
- [AE-025: Towards a Foundation-Model Paradigm for Aerodynamic Prediction in Three-dimensional Design](by_paper/AE-025_review.th.md) — แนวทาง foundation model สำหรับการทำนาย aero 3 มิติ เป็นบริบทของ surrogate เรขาคณิตทั่วไป
- [AE-026: SMART: Scalable Mesh-free Aerodynamic Simulations from Raw Geometries using a Transformer-based Surrogate Model](by_paper/AE-026_review.th.md) — surrogate ที่ไม่ต้องใช้ mesh จากเรขาคณิตดิบ ข้ามขั้น meshing สำหรับการคัดกรองขั้นแรก
- [AE-027: AirfRANS: High Fidelity Computational Fluid Dynamics Dataset for Approximating Reynolds-Averaged Navier-Stokes Solutions](by_paper/AE-027_review.th.md) — ชุดข้อมูล RANS ของ airfoil พร้อมตัวชี้วัดความสอดคล้องทางฟิสิกส์ เกี่ยวข้องกับ surrogate ของชิ้นปีกและการประเมินความสอดคล้องทางฟิสิกส์
- [AE-028: Adjoint methods for car aerodynamics](by_paper/AE-028_review.th.md) — การ optimize รูปทรงและ topology ด้าน aero ของรถแบบ adjoint ในอุตสาหกรรม เป็นวิธีปรับ aero เฉพาะที่ของตัวถังที่ผ่านแล้ว
- [AE-033: Fourier Neural Operator for Parametric Partial Differential Equations](by_paper/AE-033_review.th.md) — neural operator ที่เรียนรู้การแปลงคำตอบของ PDE เป็นสถาปัตยกรรมฐานของ surrogate การไหลหลายตัว

## TH: การจัดการความร้อน การเกิดความร้อน และการออกแบบการระบายความร้อน

**ขอบเขต:** แบบจำลองการเกิดความร้อนและเครือข่ายความร้อนของแบตเตอรี่และเครื่องจักรไฟฟ้า และการออกแบบการระบายความร้อนระดับเรขาคณิต สนับสนุนงานฟิสิกส์ความร้อนแบบ lumped, thermal-solid แบบเชื่อมโยง และ flow/heat exchange (Works 014, 115, 121)

**สิ่งที่พบข้าม paper**
- ขีดจำกัดความร้อนเกิดจาก heat generation, storage, transfer, coolant/airflow และ control แบบ transient อุณหภูมิ lumped คงที่ไม่ยืนยันความทนทานตลอดการแข่ง
- อุปกรณ์ระบายความร้อนมีต้นทุนมวล ปริมาตร pressure loss parasitic power และโอกาสทาง aero จึงต้องเชื่อม thermal design กับ objective ของรถ
- reduced thermal model ต้องมี envelope ที่ calibrate และเลื่อน fidelity เมื่อ candidate ออกจาก envelope

**สิ่งที่น่าสนใจ**

- [TH-001](by_paper/TH-001_review.th.md): อุณหภูมิปลายเท่ากันไม่แปลว่ากลไกความร้อนภายในเท่ากัน การตรวจแค่อุณหภูมิสุดท้ายจึงซ่อน provenance ของแหล่งความร้อนที่ผิดได้
- [TH-004](by_paper/TH-004_review.th.md): topology optimization การถ่ายเทความร้อนร่วม 3 มิติเต็มรูปแบบที่ได้ heat sink ไม่คุ้นตา เป็นงานก่อนหน้าของเรขาคณิตระบายความร้อนที่ค้นพบ

ชุด 2 ฉบับมี evidence profile หลักคือ หลักฐานเชิงประจักษ์/การทดลอง (1), หลักฐานคณิตศาสตร์/เชิงรูปนัย (1), หลักฐาน simulation/เชิงตัวเลข (1), การศึกษา optimization/search (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- เชื่อม thermal-solid และ flow-heat ของ Work 115/121 กับ storage, converter, brake, aero duct และ finish gate ตลอด stint
- ติดตาม provenance ของแหล่งความร้อน พลังงานสะสม boundary flux กำลังปั๊ม coolant และความร้อนที่ระบายเป็นสมดุลเดียว
- เพิ่มกรณี thermal soak, หลายรอบต่อเนื่อง, อากาศร้อน, ทางไหลอุดตัน และ pump/fan failure

**รายงานรายฉบับและข้อค้นพบหลัก**
- [TH-001: A General Energy Balance for Battery Systems](by_paper/TH-001_review.th.md) — **deep review** — สองกลไกไปถึงอุณหภูมิ adiabatic-reversible สุดท้ายเท่ากันได้แต่มีประวัติ heat generation และจุดเปลี่ยน slope ต่างกัน สมดุลแบบ reaction เดียวที่ใช้ทั่วไปใช้ได้เมื่อ phase change, mixing และ simultaneous reaction ไม่มีนัยสำคัญเท่านั้น (ผล/สรุป หน้า 7-9)
- [TH-004: Large scale three-dimensional topology optimisation of heat sinks cooled by natural convection](by_paper/TH-004_review.th.md) — topology optimization การถ่ายเทความร้อนร่วม 3 มิติเต็มรูปแบบที่ได้ heat sink ไม่คุ้นตา เป็นงานก่อนหน้าของเรขาคณิตระบายความร้อนที่ค้นพบ

## MA: วัสดุ ข้อมูลวัสดุ ตัวยึดและข้อต่อ โครงสร้างรับการชน การผลิต และพิกัดความเผื่อ

**ขอบเขต:** แหล่งที่มาของพฤติกรรมวัสดุและข้อต่อจริง และการที่การผลิตกับพิกัดความเผื่อจำกัดการออกแบบ โครงการเลือกเฉพาะวัสดุในแค็ตตาล็อก (ไม่ออกแบบส่วนผสมใหม่) และค่าวัสดุจริงอยู่ใน private/ ตามนโยบายข้อมูลวัสดุ

**สิ่งที่พบข้าม paper**
- สมรรถนะวัสดุและข้อต่อขึ้นกับ process, orientation, surface, temperature, tolerance และ load history ค่า scalar จาก handbook ไม่ใช่ constitutive law สากล
- fatigue และ reliability ต้องใช้ distribution, damage accumulation และ failure mode ไม่ใช่ static factor of safety อย่างเดียว
- manufacturing feasibility ต้องผูกกับกระบวนการและแผนตรวจที่ประกาศ

**สิ่งที่น่าสนใจ**

- [MA-003](by_paper/MA-003_review.th.md): paper model ความเชื่อมโยง process-structure-property ไม่ใช่ composition อย่างเดียว ตรงกับกฎโครงการว่าค่าวัสดุขึ้นกับประวัติการผลิต
- [MA-012](by_paper/MA-012_review.th.md): claim การค้นพบขนาดใหญ่ของ GNoME ใช้คู่กับ MA-013 เป็นกรณีศึกษาของการโต้แย้ง claim การค้นพบ

ชุด 2 ฉบับมี evidence profile หลักคือ ชุดข้อมูล/benchmark (2), หลักฐานเชิงประจักษ์/การทดลอง (2), หลักฐาน simulation/เชิงตัวเลข (2), หลักฐานคณิตศาสตร์/เชิงรูปนัย (1), งานทบทวน/สังเคราะห์ (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- ใช้ material-data policy กับ constitutive lookup ทุกครั้ง และคงสภาวะที่ไม่มีข้อมูลเป็น unknown ชัดเจน
- ขยาย Works 113/114/116/130 ด้วย preload, contact, tolerance, thermal, fatigue และ failure envelope เฉพาะ process
- เพิ่ม specimen และ assembly correlation ก่อนถ่ายโอน model วัสดุ/ข้อต่อไปยังรถเต็มคัน

**รายงานรายฉบับและข้อค้นพบหลัก**
- [MA-003: Exploration of data science techniques to predict fatigue strength of steel from composition and processing parameters](by_paper/MA-003_review.th.md) — **deep review** — หลาย model ได้ R2 ประมาณ 0.98 และ error ที่รายงานต่ำกว่า 4% ดีกว่างานก่อนและช่วยจัดอันดับ composition/process variable ที่ทำนายได้ (หน้า 1, 13-15)
- [MA-012: Scaling deep learning for materials discovery](by_paper/MA-012_review.th.md) — claim การค้นพบขนาดใหญ่ของ GNoME ใช้คู่กับ MA-013 เป็นกรณีศึกษาของการโต้แย้ง claim การค้นพบ

## VV: Verification, validation, การสอบเทียบ สถิติ การทำซ้ำได้ และวินัยในการอ้างผล

**ขอบเขต:** วิธีแสดงว่า solver แก้สมการของตัวเองได้ถูก วิธีแสดงว่าแบบจำลองทำนายความจริงได้ วิธีเปรียบเทียบวิธีค้นหาเชิงสุ่มอย่างซื่อตรง และวิธีที่ optimizer ใช้ช่องโหว่ของวัตถุประสงค์และตัวจำลอง เป็นรากฐานของระดับหลักฐาน fidelity gate และวินัยการรีวิวใน AGENTS.md

**สิ่งที่พบข้าม paper**
- verification ถามว่าแก้สมการถูกหรือไม่ ส่วน validation ถามว่าสมการแทนโลกจริงสำหรับ intended use ได้หรือไม่ การผ่าน software test ไม่แทนทั้งสองอย่าง
- uncertainty, sensitivity, convergence, การแยก calibration/validation และการควบคุม multiplicity กำหนดความแข็งแรงของ claim
- adaptive search และการใช้ benchmark ซ้ำสร้าง selection bias จึงต้องมี untouched holdout และหลักฐานแบบ append-only

**สิ่งที่น่าสนใจ**

- [VV-008](by_paper/VV-008_review.th.md): code อาจ verify แล้วแต่ model ใช้ไม่ได้กับ application และการตรงการทดลองหนึ่ง tier ไม่ได้ validate การทำนายระบบเต็มโดยอัตโนมัติ
- [VV-012](by_paper/VV-012_review.th.md): การวิเคราะห์ power สำหรับเลือกจำนวน seed ใช้ได้โดยตรงกับการกำหนดขนาดแคมเปญค้นหาแบบ paired seed
- [VV-024](by_paper/VV-024_review.th.md): อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate

ชุด 20 ฉบับมี evidence profile หลักคือ หลักฐานเชิงประจักษ์/การทดลอง (15), ชุดข้อมูล/benchmark (13), หลักฐานการทดสอบกายภาพ (10), งานทบทวน/สังเคราะห์ (9), หลักฐาน simulation/เชิงตัวเลข (9), การศึกษา control/learning (7), การศึกษา optimization/search (6), หลักฐานคณิตศาสตร์/เชิงรูปนัย (5), การศึกษาเชิงเทคนิค/วิธีวิทยา (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- ทำ Validation Strategy ให้เป็น evidence gate เฉพาะโดเมนที่รันได้ พร้อม intended-use statement ที่ trace ได้
- บังคับ convergence, sensitivity/UQ, การแยก calibration/holdout, inference ที่คำนึง multiplicity และ negative control ในงาน admitted ทุกชิ้น
- ใช้ claim template ที่ผูกข้อสรุปกับ candidate, evaluator, dataset, fidelity และ uncertainty identity

**รายงานรายฉบับและข้อค้นพบหลัก**
- [VV-002: Bayesian calibration of computer models](by_paper/VV-002_review.th.md) — การสอบเทียบของ Kennedy-O'Hagan ที่มีเทอมความคลาดเคลื่อนของแบบจำลองชัดเจน เป็นแผนการสอบเทียบระบบย่อยกับการวัด
- [VV-003: Deep Reinforcement Learning at the Edge of the Statistical Precipice](by_paper/VV-003_review.th.md) — การประมาณช่วงและค่ารวมที่ทนทานสำหรับการเทียบที่มีจำนวนรันน้อย เป็นมาตรฐานการรายงานของแคมเปญค้นหาที่จำนวน seed จำกัด
- [VV-008: Verification, validation, and predictive capability in computational engineering and physics](by_paper/VV-008_review.th.md) — **deep review** — verification ประเมินความแม่นในการแก้ computational model ส่วน validation ประเมินความตรงกับโลกทดลองสำหรับ intended use ต้องแยก numerical error, experimental uncertainty และ model discrepancy และการทำนายนอก validation database ใช้ inference ที่อ่อนกว่า (หน้า 3-4, 14, 21)
- [VV-012: How Many Random Seeds? Statistical Power Analysis in Deep Reinforcement Learning Experiments](by_paper/VV-012_review.th.md) — การวิเคราะห์ power สำหรับเลือกจำนวน seed ใช้ได้โดยตรงกับการกำหนดขนาดแคมเปญค้นหาแบบ paired seed
- [VV-013: Deep Reinforcement Learning that Matters](by_paper/VV-013_review.th.md) — แสดงว่า seed การ implement และ hyperparameter พลิกข้อสรุปได้ เป็นเหตุผลของ metadata การ replay ครบถ้วน
- [VV-014: Statistical Comparisons of Classifiers over Multiple Data Sets](by_paper/VV-014_review.th.md) — การทดสอบแบบไม่อิงพารามิเตอร์สำหรับเทียบอัลกอริทึมข้ามหลายงาน ใช้กับการเทียบวิธีค้นหาข้ามหลายสนามได้
- [VV-015: Time for a Change: a Tutorial for Comparing Multiple Classifiers Through Bayesian Analysis](by_paper/VV-015_review.th.md) — การเปรียบเทียบแบบ Bayesian ที่มีช่วงความเท่ากันเชิงปฏิบัติ เป็นวิธีบอกว่า 'ไม่ต่างในทางปฏิบัติ' แทน 'ไม่มีนัยสำคัญ'
- [VV-016: Benchmarking in Optimization: Best Practice and Open Issues](by_paper/VV-016_review.th.md) — แนวปฏิบัติที่ดีของชุมชนในการ benchmark optimizer (งบ baseline การรายงาน) เป็น checklist ของระเบียบแคมเปญเรา
- [VV-017: COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting](by_paper/VV-017_review.th.md) — การเปรียบเทียบสมรรถนะ optimizer ตามงบแบบ anytime เป็นแบบการรายงานคุณภาพเทียบกับจำนวนการประเมิน
- [VV-019: Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)](by_paper/VV-019_review.th.md) — checklist และข้อค้นพบด้านการทำซ้ำได้ เสริมข้อกำหนด metadata การ replay
- [VV-020: Troubling Trends in Machine Learning Scholarship](by_paper/VV-020_review.th.md) — รวบรวมการอ้างเกินจริง การคาดเดาที่นำเสนอเป็นคำอธิบาย และช่องว่างของ ablation เป็น checklist ผู้รีวิวสำหรับรายงานของเราเอง
- [VV-021: The Surprising Creativity of Digital Evolution: A Collection of Anecdotes from the Evolutionary Computation and Artificial Life Research Communities](by_paper/VV-021_review.th.md) — หลายสิบกรณีที่วิวัฒนาการใช้บั๊กของตัวจำลองและช่องโหว่ เป็นหลักฐานเบื้องหลังการถือว่าการใช้ช่องโหว่เชิงตัวเลขเป็นคำอธิบายทางเลือก
- [VV-022: Concrete Problems in AI Safety](by_paper/VV-022_review.th.md) — นิยาม reward hacking และผลข้างเคียง เป็นศัพท์ของช่องโหว่วัตถุประสงค์ในการค้นหาการออกแบบ
- [VV-023: Defining and Characterizing Reward Hacking](by_paper/VV-023_review.th.md) — นิยามเชิงรูปนัยว่าเมื่อใดวัตถุประสงค์แทนถูกใช้ช่องโหว่ได้ เกี่ยวข้องกับเวลาแข่ง Level-0 ในฐานะตัวแทนเวลาแข่งจริง
- [VV-024: Leakage and the reproducibility crisis in machine-learning-based science](by_paper/VV-024_review.th.md) — อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate
- [VV-025: The garden of forking paths: Why multiple comparisons can be a problem, even when there is no fishing expedition or p-hacking and the research hypothesis was posited ahead of time](by_paper/VV-025_review.th.md) — การเลือกการวิเคราะห์ตามข้อมูลเพิ่ม false positive แม้ไม่ตั้งใจ สนับสนุนการตรึงการวิเคราะห์ก่อนเห็นผล
- [VV-028: Robot Learning from Randomized Simulations: A Review](by_paper/VV-028_review.th.md) — ทบทวน domain randomization สำหรับ sim-to-real เกี่ยวข้องกับความทนทานข้ามพารามิเตอร์ที่ไม่แน่นอน
- [VV-029: Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](by_paper/VV-029_review.th.md) — สุ่มพารามิเตอร์ตัวจำลองเพื่อถ่ายโอนสู่ความจริง เป็นกลยุทธ์ความทนทานสำหรับเงื่อนไข held-out
- [VV-031: A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](by_paper/VV-031_review.th.md) — ช่วงการทำนายที่ไม่ขึ้นกับการกระจายสำหรับ surrogate ใด ๆ เป็นวิธีง่ายในการจำกัดความคลาดเคลื่อนของ surrogate ในการตัดสินเลื่อนระดับ
- [VV-032: SALib: An open-source Python library for Sensitivity Analysis](by_paper/VV-032_review.th.md) — เครื่องมือวิเคราะห์ความไวแบบ global (Sobol, Morris) สำหรับหาว่าพารามิเตอร์ใดขับการจัดอันดับเวลาแข่ง

## AR: การควบคุมการแข่งอัตโนมัติ ผู้ขับที่เรียนรู้ telemetry จริง และกลยุทธ์การแข่ง

**ขอบเขต:** ตัวควบคุมและผู้ขับที่เรียนรู้ซึ่งขับผู้สมัครแต่ละคันใกล้ขีดจำกัดได้ ข้อมูลการแข่งรถจริงแบบสาธารณะ การระบุแบบจำลองจากข้อมูลสนาม และการจำลองกลยุทธ์ระดับการแข่ง ผู้ขับที่อ่อนทำให้กลไกที่ดีดูแย่ ดังนั้นคุณภาพผู้ขับเป็นส่วนหนึ่งของความยุติธรรม

**สิ่งที่พบข้าม paper**
- สมรรถนะการแข่งต้องเชื่อม perception, state estimation, prediction, planning, control, system identification และ safety ไว้ด้วยกันที่ขีดจำกัด
- MPC และ learning เสริมกันได้เมื่อส่วนที่เรียนรู้เปิดเผย uncertainty และยังบังคับ hard constraint ได้
- ระบบในสนามจริงแสดงว่า latency, localization fault, คู่แข่ง, grip ที่เปลี่ยน และ operational safety สำคัญกว่า simulation อุดมคติ

**สิ่งที่น่าสนใจ**

- [AR-003](by_paper/AR-003_review.th.md): paper ท้าทายสมมติฐานโดยตรงว่า model ที่ 'ดีกว่า' โดยรวมจะรักษาอันดับ controller หรือพฤติกรรม error แบบ closed loop
- [AR-012](by_paper/AR-012_review.th.md): เปรียบเทียบ optimal control กับ RL สำหรับการแข่งโดรนที่ขีดจำกัด เป็นหลักฐานสำหรับการเลือกวิธีผู้ขับเมื่อแบบจำลองไม่ตรง
- [AR-022](by_paper/AR-022_review.th.md): ระบุแบบจำลองยาง/รถจากข้อมูลขับประมาณ 30 วินาที เป็นเส้นทางการสอบเทียบที่เร็วสำหรับ physical correlation

ชุด 23 ฉบับมี evidence profile หลักคือ ชุดข้อมูล/benchmark (17), การศึกษา control/learning (16), หลักฐานเชิงประจักษ์/การทดลอง (11), หลักฐานการทดสอบกายภาพ (11), หลักฐาน simulation/เชิงตัวเลข (9), การศึกษา optimization/search (4), งานทบทวน/สังเคราะห์ (4), หลักฐานคณิตศาสตร์/เชิงรูปนัย (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- ใช้ autonomous racing stack ที่ optimize แล้วเป็น controller baseline ที่ยุติธรรมก่อนให้เครดิต morphology ของรถ
- เพิ่ม online identification, prediction ที่รู้ uncertainty, การฉีด latency/fault และสถานการณ์คู่แข่งใน held-out evaluation
- ให้การตัดสินใจเชิงกลยุทธ์อยู่ในบัญชีพลังงาน ยาง ความร้อน และ safety เดียวกับการออกแบบรถ

**รายงานรายฉบับและข้อค้นพบหลัก**
- [AR-001: Outracing champion Gran Turismo drivers with deep reinforcement learning](by_paper/AR-001_review.th.md) — ผู้ขับที่เรียนรู้ชนะมนุษย์ระดับสูงสุดในเกม fidelity สูง เป็นวิธีสร้างผู้ขับที่แข็งต่อแต่ละแบบ ไม่ใช่การยืนยันทางกายภาพ
- [AR-002: Optimization-Based Autonomous Racing of 1:43 Scale RC Cars](by_paper/AR-002_review.th.md) — model predictive contouring control สำหรับการแข่ง เป็น baseline ตัวควบคุมที่ implement ได้พร้อมขอบฟ้าและขีดจำกัด actuator ชัดเจน
- [AR-003: Analyzing the Impact of Simulation Fidelity on the Evaluation of Autonomous Driving Motion Control](by_paper/AR-003_review.th.md) — **deep review** — maximum lateral error อย่างเดียวทิ้งโครงสร้าง error สำคัญ และการ retune baseline ให้ approximation ดีขึ้นอาจทำ lateral-error disparity แย่ลงมาก (หน้า 5-6) ดังนั้น model fidelity กับ fidelity ของการประเมิน controller ไม่ได้เพิ่มตามกันเสมอ
- [AR-004: Autonomous Racing using Learning Model Predictive Control](by_paper/AR-004_review.th.md) — MPC ที่เรียนรู้ซ้ำจากรอบก่อนหน้าเพื่อลดเวลาต่อรอบ เป็นตัวควบคุมที่เข้าใกล้ขีดจำกัดของรถแต่ละคัน
- [AR-005: Autonomous Vehicles on the Edge: A Survey on Autonomous Vehicle Racing](by_paper/AR-005_review.th.md) — survey การรับรู้ การวางแผน การควบคุม และการจำลองในการแข่งอัตโนมัติ เป็นแผนที่เครื่องมือและชุดข้อมูล
- [AR-006: Indy Autonomous Challenge - Autonomous Race Cars at the Handling Limits](by_paper/AR-006_review.th.md) — การแข่งอัตโนมัติเต็มสเกลที่ขีดจำกัดการควบคุมพร้อมพฤติกรรมรถจริง เป็นเอกสารอ้างอิงของช่องว่างแบบจำลอง-ความจริงที่ความเร็วสูง
- [AR-007: TUM Autonomous Motorsport: An Autonomous Racing Software for the Indy Autonomous Challenge](by_paper/AR-007_review.th.md) — ชุดซอฟต์แวร์การแข่งอัตโนมัติแบบเปิดครบวงรวมการวางแผนและการควบคุม เป็นชิ้นส่วนที่นำมาใช้กับ baseline ผู้ขับได้
- [AR-008: RACECAR -- The Dataset for High-Speed Autonomous Racing](by_paper/AR-008_review.th.md) — ข้อมูลหลายเซนเซอร์แบบเปิดจากรถ Indy อัตโนมัติเต็มสเกลถึง 273 km/h รวมสนามเอียง เป็นข้อมูลจริงสำหรับตรวจสอบแบบจำลองรถ
- [AR-009: AMZ Driverless: The Full Autonomous Racing System](by_paper/AR-009_review.th.md) — ระบบไร้คนขับ Formula Student ครบวงพร้อมแบบจำลองรถและ MPC เป็นการ implement อ้างอิงที่มีเอกสารดี
- [AR-011: Super-Human Performance in Gran Turismo Sport Using Deep Reinforcement Learning](by_paper/AR-011_review.th.md) — ผู้ขับ RL ที่ทำเวลาต่อรอบเหนือมนุษย์ใน time trial เป็นวิธี baseline ของผู้ขับที่เรียนรู้
- [AR-012: Reaching the Limit in Autonomous Racing: Optimal Control versus Reinforcement Learning](by_paper/AR-012_review.th.md) — เปรียบเทียบ optimal control กับ RL สำหรับการแข่งโดรนที่ขีดจำกัด เป็นหลักฐานสำหรับการเลือกวิธีผู้ขับเมื่อแบบจำลองไม่ตรง
- [AR-013: Champion-level drone racing using deep reinforcement learning](by_paper/AR-013_review.th.md) — policy ที่เรียนรู้ชนะแชมป์มนุษย์ในโลกจริงโดยใช้แบบจำลอง residual จากข้อมูลจริง เป็นตัวอย่างการปิดช่องว่างจากจำลองสู่ของจริง
- [AR-017: Towards Learning-Based Formula 1 Race Strategies](by_paper/AR-017_review.th.md) — กลยุทธ์ F1 แบบเรียนรู้ เป็นบริบทล่าสุดของการตัดสินใจระดับการแข่ง
- [AR-018: Game Theory in Formula 1: From Physical to Strategic Interactions](by_paper/AR-018_review.th.md) — มุมมองทฤษฎีเกมของปฏิสัมพันธ์ใน F1 เกี่ยวข้องเฉพาะเมื่อการแข่งหลายคันเข้ามาในสภาพแวดล้อม
- [AR-019: Opponent State Inference Under Partial Observability: An HMM-POMDP Framework for 2026 Formula 1 Energy Strategy](by_paper/AR-019_review.th.md) — จำลองกลยุทธ์พลังงานตามติกาปี 2026 รวมถึง Override Mode เป็นบริบทของโปรไฟล์ติกาที่สัญญาการแข่งของเราตรึงไว้
- [AR-020: Bridging RL and MPC for mixed-integer optimal control with application to Formula 1 race strategies](by_paper/AR-020_review.th.md) — รวม RL กับ MPC สำหรับกลยุทธ์การแข่งแบบ mixed-integer เกี่ยวข้องกับการเลือกกลยุทธ์แบบไม่ต่อเนื่อง
- [AR-021: Mission Performance: Automatic and Adaptive Race Pace Progression for Autonomous Racing](by_paper/AR-021_review.th.md) — การเพิ่มจังหวะความเร็วแบบปรับตัวสู่ขีดจำกัด เกี่ยวข้องกับการหาจังหวะที่ทำได้ของผู้สมัครแต่ละคันอย่างปลอดภัย
- [AR-022: Learning-Based On-Track System Identification for Scaled Autonomous Racing in Under a Minute](by_paper/AR-022_review.th.md) — ระบุแบบจำลองยาง/รถจากข้อมูลขับประมาณ 30 วินาที เป็นเส้นทางการสอบเทียบที่เร็วสำหรับ physical correlation
- [AR-023: Deep Dynamics: Vehicle Dynamics Modeling with a Physics-Informed Neural Network for Autonomous Racing](by_paper/AR-023_review.th.md) — โครงข่ายที่มีฟิสิกส์กำกับซึ่งประมาณพารามิเตอร์รถที่ตีความได้จากข้อมูล เป็นทางเลือกการระบุแบบจำลองแบบผสม
- [AR-024: F1TENTH: An Open-source Evaluation Environment for Continuous Control and Reinforcement Learning](by_paper/AR-024_review.th.md) — สภาพแวดล้อมประเมินการแข่งแบบย่อส่วนที่เปิดพร้อมรถจริง เป็นแนวคิดแท่นทดสอบจริงราคาถูก
- [AR-025: Real-Time Adaptive Velocity Optimization for Autonomous Electric Cars at the Limits of Handling](by_paper/AR-025_review.th.md) — การวางแผนความเร็วแบบเวลาจริงที่มีขีดจำกัดพลังงานและแรงเสียดทานบนรถแข่งไฟฟ้า เป็นชิ้นส่วนผู้ขับสำหรับการแข่งที่พลังงานจำกัด
- [AR-026: Efficient Trajectory Optimization for Autonomous Racing via Formula-1 Data-Driven Initialization](by_paper/AR-026_review.th.md) — ใช้ข้อมูลเส้นทาง Formula 1 จริงเป็นค่าเริ่มต้นของการ optimize เส้นแข่ง เป็นแหล่งข้อมูลเส้นแข่ง F1 สาธารณะและวิธี warm start
- [AR-027: Unifying F1TENTH Autonomous Racing: Survey, Methods and Benchmarks](by_paper/AR-027_review.th.md) — benchmark ตัววางแผนและตัวควบคุมการแข่งบนแพลตฟอร์มเดียวกัน เป็นแหล่งอ้างอิงของการเทียบตัวควบคุมอย่างยุติธรรม

## DS: การสังเคราะห์การออกแบบเชิงคำนวณ การแทนค่าเชิงหน้าที่ การสังเคราะห์การประกอบ และการวัดความใหม่

**ขอบเขต:** งานวิจัยการออกแบบวิศวกรรมเรื่องการสร้างสถาปัตยกรรมจากหน้าที่ด้วย grammar การแยกโครงสร้างเป็นชิ้นส่วนที่ต่อกัน และการวัดว่าการออกแบบใหม่จริงหรือไม่ เกี่ยวข้องกับ typed interface, physical interface graph, part resolution และนิยามการค้นพบของโครงการ

**สิ่งที่พบข้าม paper**
- function-to-form mapping และ generative model เพิ่มจำนวน concept ได้ แต่ความหลากหลายที่สร้างไม่เท่ากับความมีประโยชน์หรือความใหม่โดยอัตโนมัติ
- novelty มีหลายความหมาย: ความใหม่ทางภาพ โครงสร้าง หน้าที่ เทคโนโลยี และ prior art ต้องใช้หลักฐานต่างกัน
- metric การออกแบบต้องแยก quantity, quality, variety และ novelty และยึดกับแหล่งอ้างอิงภายนอก

**สิ่งที่น่าสนใจ**

- [DS-009](by_paper/DS-009_review.th.md): เรียนรู้การจับคู่จากหน้าที่สู่ชิ้นส่วนจากผลิตภัณฑ์จริงเพื่อสังเคราะห์โครงร่าง เป็นแหล่ง grammar ที่ขับด้วยข้อมูล
- [DS-012](by_paper/DS-012_review.th.md): paper แสดงว่าคะแนน novelty เดียวไม่พอ แบบหนึ่งอาจใช้ความรู้ต้นทางแปลกใหม่แต่ไม่เพิ่มหน้าที่ หรือเพิ่มหน้าที่จากต้นทางคุ้นเคย
- [DS-017](by_paper/DS-017_review.th.md): การสร้างแนวคิดการออกแบบด้วย transformer จากความรู้การออกแบบ เป็นเส้นทางเสนอแบบระดับข้อความก่อนเรขาคณิต

ชุด 3 ฉบับมี evidence profile หลักคือ หลักฐานเชิงประจักษ์/การทดลอง (3), งานทบทวน/สังเคราะห์ (2), ชุดข้อมูล/benchmark (2), การศึกษา control/learning (2), หลักฐาน simulation/เชิงตัวเลข (1), หลักฐานคณิตศาสตร์/เชิงรูปนัย (1) ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง

**ควรปรับปรุงส่วนใดในงานเรา**
- แยกรายงาน Formula Ultimate เป็น geometric novelty, causal functional difference, performance benefit และ external technology novelty
- ค้น prior art หลัง candidate มีหลักฐาน causal function และ performance ที่ยุติธรรมแล้ว
- ใช้คำอธิบาย function-flow และ physical interface ช่วยค้นหา ไม่ใช้เป็นหลักฐานว่า hardware มีอยู่จริง

**รายงานรายฉบับและข้อค้นพบหลัก**
- [DS-009: Automated synthesis of electromechanical design configurations from empirical analysis of function to form mapping](by_paper/DS-009_review.th.md) — เรียนรู้การจับคู่จากหน้าที่สู่ชิ้นส่วนจากผลิตภัณฑ์จริงเพื่อสังเคราะห์โครงร่าง เป็นแหล่ง grammar ที่ขับด้วยข้อมูล
- [DS-012: Measuring technological novelty with patent-based indicators](by_paper/DS-012_review.th.md) — **deep review** — new functionality กับ new origins มีความสัมพันธ์แต่ให้ข้อมูลต่างกัน correlation ระหว่าง indicator คนละมิติโดยทั่วไปไม่เกิน 0.3 และ indicator ระดับ IPC4 มีความสัมพันธ์บวกอย่างมีนัยสำคัญกับโอกาสเป็น breakthrough (หน้า 2, 11-12)
- [DS-017: Generative Transformers for Design Concept Generation](by_paper/DS-017_review.th.md) — การสร้างแนวคิดการออกแบบด้วย transformer จากความรู้การออกแบบ เป็นเส้นทางเสนอแบบระดับข้อความก่อนเรขาคณิต

## ข้อจำกัดของรายงาน

- คลังนี้ครอบคลุมเฉพาะ PDF ที่อยู่ใน `papers/` ณ วันที่อ่าน ไม่ใช่ systematic review ที่ค้นครบทุกฐานข้อมูล
- section detection เป็นตัวช่วยนำทางและพลาด heading ที่จัดรูปแบบไม่ปกติได้ แต่ coverage และคำรวมคำนวณจากทุกหน้า
- รายงานรายฉบับเป็นการอ่านเชิงถ่ายโอนสู่โครงการ ไม่แทน critical replication หรือการประเมินคุณภาพทางสถิติเต็มรูปแบบ
