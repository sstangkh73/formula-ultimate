# SI-020: Energy conservation and power bonds in co-simulations: non-iterative adaptive step size control and error estimation

English source: `SI-020_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Severin Sadjina, Lars T. Kyllingstad, Stian Skjong, E. Pedersen |
| ปี | 2017 |
| แหล่งตีพิมพ์ | Engineering computations |
| DOI | Not recorded |
| arXiv | 1602.06434 |
| ระเบียน canonical | [https://arxiv.org/abs/1602.06434](https://arxiv.org/abs/1602.06434) |
| หัวข้อในคลัง | โครงสร้างพื้นฐาน simulation และ differentiable physics |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/06_simulation_infrastructure/SI-020_Sadjina2017_energy-conservation-and-power-bonds-in-co-simulati.pdf) |
| SHA-256 ของต้นฉบับ | `bb2e17ce18e507768e371000c81175481dacf7398b0edb5d7f455cb24384c7f1` |
| coverage ของ full text | 14/14 หน้า (100.00%); สกัดได้ 10,076 คำ |

## คำถามวิจัย

residual ของกำลังที่แลกเปลี่ยนจะใช้เป็น error estimate และตัวควบคุม macro step แบบไม่ iterate สำหรับ co-simulation ได้หรือไม่?

## วิธีและหลักฐาน

ECCO คำนวณ residual power/energy จาก power bond ที่ interface ของ subsystem และปรับ macro step โดยไม่ rollback หรือเข้าถึงภายใน subsystem ทดสอบกับ quarter-car co-simulation แบบ linear/nonlinear (หน้า 1, 5, 8-11)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ใน linear benchmark ที่รายงาน adaptive step จาก residual energy ลด residual energy ประมาณ 90% และการแบ่ง subsystem อีกแบบให้ error สูงกว่า แสดงว่า coupling topology มีผล (หน้า 10-11)
- **การตีความของผู้ทบทวน:** error signal สังเกตได้อย่างอิสระที่ interface ไม่ได้สร้างจากการใส่เครื่องหมายลบให้ input ที่กำหนด ตรงกับความต้องการหลักฐาน transferred energy ของโครงการ
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** error signal สังเกตได้อย่างอิสระที่ interface ไม่ได้สร้างจากการใส่เครื่องหมายลบให้ input ที่กำหนด ตรงกับความต้องการหลักฐาน transferred energy ของโครงการ โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ข้อผูก global error สมมติ coupling ที่ไม่มี algebraic loop และหลักฐานมาจาก quarter-car benchmark การเลือก tolerance กับการแบ่ง subsystem ยังเฉพาะ application การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **error signal สังเกตได้อย่างอิสระที่ interface ไม่ได้สร้างจากการใส่เครื่องหมายลบให้ input ที่กำหนด ตรงกับความต้องการหลักฐาน transferred energy ของโครงการ** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **simulation coupling contract, evaluator applicability registry และ solver-failure ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | simulation coupling contract, evaluator applicability registry และ solver-failure ledger |
| การเปลี่ยนแปลงที่เสนอ | ติดเครื่องมือที่ทุก coupling bond ของ Work 123 เพื่อวัด effort/flow และ residual energy เทียบ macro step คงที่กับ ECCO adaptive และไม่เลื่อนเมื่อ residual-energy reduction ไม่สัมพันธ์กับ state/output error อิสระ |
| experiment และ control | benchmark กับกรณี analytical และ independent solver ข้าม time step, mesh, ช่วง stiffness/contact และ hardware พร้อมวัด error, conservation, stability และ cost |
| หลักฐานผ่านและล้มเหลว | admit เฉพาะ candidate class ที่ error/stability อยู่ใน envelope ที่ลงทะเบียน และคง gradient/solver failure เป็นผลที่สังเกตได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 14 หน้า, 58,688 ตัวอักษร, 10,076 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 14/14
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 5, 8, 9, 10, 11, 12 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
