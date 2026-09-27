# LT-024: Time-optimal Design and Control of Electric Race Cars Equipped with Multi-speed Transmissions

English source: `LT-024_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Camiel Cartignij, Mauro Salazar |
| ปี | 2023 |
| แหล่งตีพิมพ์ | Vehicle Power and Propulsion Conference |
| DOI | Not recorded |
| arXiv | 2311.03545 |
| ระเบียน canonical | [https://arxiv.org/abs/2311.03545](https://arxiv.org/abs/2311.03545) |
| หัวข้อในคลัง | เวลาต่อรอบต่ำสุดและการออกแบบรถ/การควบคุมร่วม |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/07_lap_time_vehicle_dynamics/LT-024_Cartignij2023_time-optimal-design-and-control-of-electric-race-c.pdf) |
| SHA-256 ของต้นฉบับ | `840b73c28b9d0902631db5366a01969d9131fc6effec5ba06cf9be0bc29ea5e3` |
| coverage ของ full text | 4/4 หน้า (100.00%); สกัดได้ 3,588 คำ |

## คำถามวิจัย

งาน Time-optimal Design and Control of Electric Race Cars Equipped with Multi-speed Transmissions ตั้งและแก้ปัญหา minimum lap time หรือ vehicle design/control แบบ coupled อย่างไร และตรวจ feasibility อย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ ไม่พบ heading ที่เชื่อถือได้ และคำเทคนิคที่พบบ่อย ได้แก่ control, problem, optimization, design, electric, race, algorithm, time วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **เปรียบเทียบเกียร์คงที่ CVT และหลายสปีดพร้อมการควบคุมที่ optimize ร่วม เป็นการประเมินการเลือกสถาปัตยกรรมอย่างยุติธรรม**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** เปรียบเทียบเกียร์คงที่ CVT และหลายสปีดพร้อมการควบคุมที่ optimize ร่วม เป็นการประเมินการเลือกสถาปัตยกรรมอย่างยุติธรรม
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'เปรียบเทียบเกียร์คงที่ CVT และหลายสปีดพร้อมการควบคุมที่ optimize ร่วม เป็นการประเมินการเลือกสถาปัตยกรรมอย่างยุติธรรม' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อเวลาต่อรอบต่ำสุดและการออกแบบรถ/การควบคุมร่วม
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'เปรียบเทียบเกียร์คงที่ CVT และหลายสปีดพร้อมการควบคุมที่ optimize ร่วม เป็นการประเมินการเลือกสถาปัตยกรรมอย่างยุติธรรม' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อเวลาต่อรอบต่ำสุดและการออกแบบรถ/การควบคุมร่วม โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผลเวลาต่อรอบขึ้นกับ vehicle model, tyre/aero map, track, constraint, initialization, scaling และ transcription การที่ optimizer converge อย่างเดียวไม่ใช่ feasibility การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **เปรียบเทียบเกียร์คงที่ CVT และหลายสปีดพร้อมการควบคุมที่ optimize ร่วม เป็นการประเมินการเลือกสถาปัตยกรรมอย่างยุติธรรม** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **integrated transient lap evaluator, optimal-control transcription และ independent forward replay** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | integrated transient lap evaluator, optimal-control transcription และ independent forward replay |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'เปรียบเทียบเกียร์คงที่ CVT และหลายสปีดพร้อมการควบคุมที่ optimize ร่วม เป็นการประเมินการเลือกสถาปัตยกรรมอย่างยุติธรรม' ใน target ที่ระบุด้านล่าง |
| experiment และ control | แก้และ replay โจทย์สนามเดียวกันด้วยข้อจำกัด tyre, aero, energy, thermal, actuator และ path เดียวกัน พร้อมเทียบ transcription และ fixed-topology baseline ที่ optimize แล้ว |
| หลักฐานผ่านและล้มเหลว | ต้องผ่าน forward-replay feasibility, state/control defect ต่ำ, สมดุลพลังงาน, finish completion และเวลาที่ดีขึ้นซ้ำได้เกิน numerical tolerance |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 4 หน้า, 21,350 ตัวอักษร, 3,588 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 4/4
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
