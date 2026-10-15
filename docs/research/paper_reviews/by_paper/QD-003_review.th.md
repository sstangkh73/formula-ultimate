# QD-003: Data-Efficient Design Exploration through Surrogate-Assisted Illumination

English source: `QD-003_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Adam Gaier, A. Asteroth, Jean-Baptiste Mouret |
| ปี | 2018 |
| แหล่งตีพิมพ์ | Evolutionary Computation |
| DOI | Not recorded |
| arXiv | 1806.05865 |
| ระเบียน canonical | [https://arxiv.org/abs/1806.05865](https://arxiv.org/abs/1806.05865) |
| หัวข้อในคลัง | quality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/03_search_qd_multifidelity/QD-003_Gaier2018_data-efficient-design-exploration-through-surrogat.pdf) |
| SHA-256 ของต้นฉบับ | `85ecbc13345539cd4b1ef7322499b70108b8f38b603a532509b08b37ea589d19` |
| coverage ของ full text | 30/30 หน้า (100.00%); สกัดได้ 14,513 คำ |

## คำถามวิจัย

surrogate-assisted illumination จะทำแผนที่ niche การออกแบบคุณภาพสูงหลายแบบด้วย expensive evaluation น้อยกว่า MAP-Elites หรือการหา optimum เดี่ยวได้หรือไม่?

## วิธีและหลักฐาน

SAIL รวม Gaussian-process surrogate, upper-confidence-bound acquisition map และ MAP-Elites ทดสอบกับ airfoil 2 มิติแล้วขยายไปงานออกแบบ aero 3 มิติที่ flow simulation มีราคาแพง (หน้า 1-2, 8, 13)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** paper รายงานแบบที่หลากหลายและคุณภาพสูงหลายร้อยแบบด้วยจำนวน evaluation ต่ำกว่า MAP-Elites หรือ CMA-ES หลายลำดับขนาดในงาน 2 มิติ และสร้าง illumination map คุณภาพสูงในงาน 3 มิติ (หน้า 1) การสุ่มด้วย UCB เพิ่มความแม่นบริเวณ high-fitness เมื่อเทียบการสุ่มสม่ำเสมอหรือดู variance อย่างเดียว (หน้า 13)
- **การตีความของผู้ทบทวน:** นอกจากลด evaluation แล้ว SAIL เปิดเผย encoding bias โดยแผนที่แสดงบริเวณที่ encoding สร้างได้และบริเวณที่ surrogate เรียนง่ายหรือยาก (discussion หน้า 25-26)
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** นอกจากลด evaluation แล้ว SAIL เปิดเผย encoding bias โดยแผนที่แสดงบริเวณที่ encoding สร้างได้และบริเวณที่ surrogate เรียนง่ายหรือยาก (discussion หน้า 25-26) โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ประโยชน์ขึ้นกับ behavioral feature, ความเหมาะของ Gaussian process, acquisition policy และการสุ่ม expensive truth งาน 3 มิติมีต้นทุนสูงจนไม่ได้ทำ learning curve ละเอียดเท่ากรณี airfoil (หน้า 19) การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **นอกจากลด evaluation แล้ว SAIL เปิดเผย encoding bias โดยแผนที่แสดงบริเวณที่ encoding สร้างได้และบริเวณที่ surrogate เรียนง่ายหรือยาก (discussion หน้า 25-26)** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion |
| การเปลี่ยนแปลงที่เสนอ | เพิ่มแขน SAIL ใน benchmark การค้นหาโดยให้งบ high-fidelity call เท่ากับ MAP-Elites audit surrogate error แยก archive cell และต้องเพิ่ม held-out feasible coverage ไม่ใช่ predicted QD score อย่างเดียว |
| experiment และ control | เทียบกฎค้นหาจาก paper กับ objective optimization, random search และ MAP-Elites โดยจับคู่ proposal, seed, งบ wall/CPU/GPU และ high-fidelity audit แบบ stratified |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่ม feasible coverage หรือ held-out quality พร้อม confidence interval และไม่มี proxy false-negative rate ที่ยอมรับไม่ได้ ผล fidelity สูงที่ยังไม่ทราบคงเป็น `not_estimable` |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 30 หน้า, 91,245 ตัวอักษร, 14,513 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 30/30
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 6, 8, 13, 19, 21, 24 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, discussion, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
