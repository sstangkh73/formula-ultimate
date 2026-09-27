# OE-013: Evolving Neural Networks through Augmenting Topologies

English source: `OE-013_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Kenneth O. Stanley, Risto Miikkulainen |
| ปี | 2002 |
| แหล่งตีพิมพ์ | Evolutionary Computation |
| DOI | 10.1162/106365602320169811 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.1162/106365602320169811](https://doi.org/10.1162/106365602320169811) |
| หัวข้อในคลัง | การออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/01_open_ended_codesign/OE-013_Stanley2002_evolving-neural-networks-through-augmenting-topolo.pdf) |
| SHA-256 ของต้นฉบับ | `9653947f63d9dc2fc06760b7cac8a82fbf37cbbcda01dc1f6adf12fc6954b4c3` |
| coverage ของ full text | 30/30 หน้า (100.00%); สกัดได้ 14,984 คำ |

## คำถามวิจัย

งาน Evolving Neural Networks through Augmenting Topologies ค้นหา รักษา หรือประเมิน morphology ร่วมกับ control อย่างไร และทำให้เกิด bias แบบใด?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา optimization/search, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction และคำเทคนิคที่พบบ่อย ได้แก่ neat, networks, species, population, structure, different, number, neural วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **NEAT: historical marking, speciation และการเพิ่มความซับซ้อนสำหรับวิวัฒนาการ topology กราฟ เป็นคำตอบมาตรฐานของการผสมข้าม topology ที่ต่างกัน (Work 094)**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** NEAT: historical marking, speciation และการเพิ่มความซับซ้อนสำหรับวิวัฒนาการ topology กราฟ เป็นคำตอบมาตรฐานของการผสมข้าม topology ที่ต่างกัน (Work 094)
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'NEAT: historical marking, speciation และการเพิ่มความซับซ้อนสำหรับวิวัฒนาการ topology กราฟ เป็นคำตอบมาตรฐานของการผสมข้าม topology ที่ต่างกัน (Work 094)' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'NEAT: historical marking, speciation และการเพิ่มความซับซ้อนสำหรับวิวัฒนาการ topology กราฟ เป็นคำตอบมาตรฐานของการผสมข้าม topology ที่ต่างกัน (Work 094)' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล morphology ไวต่อ encoding, การจัดงบฝึก controller, task distribution และสมมติฐาน simulator มาก ความสำเร็จเสมือนไม่ถ่ายโอนไปรถแข่งโดยไม่มี physical correlation การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **NEAT: historical marking, speciation และการเพิ่มความซับซ้อนสำหรับวิวัฒนาการ topology กราฟ เป็นคำตอบมาตรฐานของการผสมข้าม topology ที่ต่างกัน (Work 094)** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'NEAT: historical marking, speciation และการเพิ่มความซับซ้อนสำหรับวิวัฒนาการ topology กราฟ เป็นคำตอบมาตรฐานของการผสมข้าม topology ที่ต่างกัน (Work 094)' ใน target ที่ระบุด้านล่าง |
| experiment และ control | รัน operator หรือกฎจัดสรรที่ได้จาก paper เทียบ evolution/QD และ fixed-topology control ที่ optimize แล้ว โดยจับคู่ seed, compute รวม, งบฝึก controller และสนาม held-out |
| หลักฐานผ่านและล้มเหลว | ยอมรับเมื่อ feasible archive coverage หรือผลงานสนาม held-out ดีขึ้นโดยไม่เพิ่มแบบ invalid, controller under-training หรือ evaluator disagreement มิฉะนั้นปฏิเสธการถ่ายโอน |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 30 หน้า, 93,188 ตัวอักษร, 14,984 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 30/30
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 4, 5, 11, 13, 14, 16 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
