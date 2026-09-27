# CAD-013: JoinABLe: Learning Bottom-up Assembly of Parametric CAD Joints

English source: `CAD-013_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Karl D. D. Willis, P. Jayaraman, Hang Chu, Yunsheng Tian, Yifei Li, Daniele Grandi, Aditya Sanghi, Linh-Tam Tran, J. Lambourne, Armando Solar-Lezama, W. Matusik |
| ปี | 2022 |
| แหล่งตีพิมพ์ | Computer Vision and Pattern Recognition |
| DOI | Not recorded |
| arXiv | 2111.12772 |
| ระเบียน canonical | [https://arxiv.org/abs/2111.12772](https://arxiv.org/abs/2111.12772) |
| หัวข้อในคลัง | CAD, B-rep, assembly และการสร้างเรขาคณิต |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/04_cad_brep_assembly/CAD-013_Willis2022_joinable-learning-bottom-up-assembly-of-parametric.pdf) |
| SHA-256 ของต้นฉบับ | `1a4f6b4944b07a43ef4489363cf619437a54c9ec6f5362e2a997a62210381485` |
| coverage ของ full text | 30/31 หน้า (96.77%); สกัดได้ 18,587 คำ |

## คำถามวิจัย

การเรียนรู้บนกราฟ B-rep จะกู้ joint axis และ pose จาก weak supervision ใน parametric CAD assembly ทั่วไปได้หรือไม่?

## วิธีและหลักฐาน

JoinABLe encode face/edge ของ B-rep เป็นกราฟ ทำนายคู่ entity ของ joint axis และค้น joint pose ใช้ weak label จาก Fusion 360 Gallery assembly dataset และเทียบ geometric baseline หลายแบบ (หน้า 1, 22-28)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ความแม่น joint-axis ที่รายงานคือ 79.53% ใกล้ผลมนุษย์ 80% และสูงกว่า baseline ที่ทดสอบ (หน้า 1) งาน joint ที่มีรูทำได้ดีกว่า โดย edge length และ entity type สำคัญ ส่วน face area อาจลดผล (ภาคผล หน้า 22-25)
- **การตีความของผู้ทบทวน:** equivalent label ทำให้ความแม่นที่วัดเพิ่มมาก (หน้า 22) แสดงว่า evaluation assembly ต้องแยก geometric equivalence จริงออกจากการยอม joint ผิด
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** equivalent label ทำให้ความแม่นที่วัดเพิ่มมาก (หน้า 22) แสดงว่า evaluation assembly ต้องแยก geometric equivalence จริงออกจากการยอม joint ผิด โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

วิธีทำนาย joint จาก regularity ของ dataset และทำงานง่ายกว่ากับ interface แบบรู ไม่พิสูจน์ load transfer, tolerance, motion ที่ไม่ชน, รายละเอียดตัวยึด หรือ manufacturing feasibility การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **equivalent label ทำให้ความแม่นที่วัดเพิ่มมาก (หน้า 22) แสดงว่า evaluation assembly ต้องแยก geometric equivalence จริงออกจากการยอม joint ผิด** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140 |
| การเปลี่ยนแปลงที่เสนอ | ใช้ JoinABLe เป็น proposal baseline ใน Work 140 แต่ต้องผ่าน exact face/edge grounding, DOF ที่ประกาศ, motion probe, interference และ load-path check ก่อนรับ joint |
| experiment และ control | ประเมิน representation จาก paper บน solid/assembly ที่ซ่อนด้วยการตรวจ topology, watertightness, constraint/editability, mass property, mate, interference, meshing และ load path |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่มอัตรา artifact ผ่านเชิงหน้าที่ที่งบสร้างเท่ากัน โดยไม่เพิ่ม topology corruption, mate invalid หรือ geometry-to-mesh discrepancy |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 31 หน้า, 111,462 ตัวอักษร, 18,587 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 30/31
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 6, 7, 8, 13, 22, 24 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
