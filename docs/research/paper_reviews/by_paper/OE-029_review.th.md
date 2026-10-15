# OE-029: An Empirical Study on the Computation Budget of Co-Optimization of Robot Design and Control in Simulation

English source: `OE-029_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Etor Arza, Frank Veenstra, T. Nygaard, Kyrre Glette |
| ปี | 2024 |
| แหล่งตีพิมพ์ | arXiv |
| DOI | Not recorded |
| arXiv | 2409.08621 |
| ระเบียน canonical | [https://arxiv.org/abs/2409.08621](https://arxiv.org/abs/2409.08621) |
| หัวข้อในคลัง | การออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/01_open_ended_codesign/OE-029_Arza2024_an-empirical-study-on-the-computation-budget-of-co.pdf) |
| SHA-256 ของต้นฉบับ | `692767090d0cbbae61219741368aa1b0080916189498a1aa0225de9f39665765` |
| coverage ของ full text | 14/14 หน้า (100.00%); สกัดได้ 7,113 คำ |

## คำถามวิจัย

งาน An Empirical Study on the Computation Budget of Co-Optimization of Robot Design and Control in Simulation ค้นหา รักษา หรือประเมิน morphology ร่วมกับ control อย่างไร และทำให้เกิด bias แบบใด?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction และคำเทคนิคที่พบบ่อย ได้แก่ design, budget, controller, co-optimization, control, computation, best, complexity วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล morphology ไวต่อ encoding, การจัดงบฝึก controller, task distribution และสมมติฐาน simulator มาก ความสำเร็จเสมือนไม่ถ่ายโอนไปรถแข่งโดยไม่มี physical correlation การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'วัดว่าการแบ่งงบคำนวณระหว่างการออกแบบกับการควบคุมเปลี่ยนผลการปรับร่วมอย่างไร เกี่ยวข้องโดยตรงกับกฎความยุติธรรมที่จับคู่งบ' ใน target ที่ระบุด้านล่าง |
| experiment และ control | รัน operator หรือกฎจัดสรรที่ได้จาก paper เทียบ evolution/QD และ fixed-topology control ที่ optimize แล้ว โดยจับคู่ seed, compute รวม, งบฝึก controller และสนาม held-out |
| หลักฐานผ่านและล้มเหลว | ยอมรับเมื่อ feasible archive coverage หรือผลงานสนาม held-out ดีขึ้นโดยไม่เพิ่มแบบ invalid, controller under-training หรือ evaluator disagreement มิฉะนั้นปฏิเสธการถ่ายโอน |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 14 หน้า, 44,420 ตัวอักษร, 7,113 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 14/14
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 7, 9, 11 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
