# OE-002: Automatic design and manufacture of robotic lifeforms

English source: `OE-002_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Hod Lipson, Jordan B. Pollack |
| ปี | 2000 |
| แหล่งตีพิมพ์ | Nature |
| DOI | 10.1038/35023115 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.1038/35023115](https://doi.org/10.1038/35023115) |
| หัวข้อในคลัง | การออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/01_open_ended_codesign/OE-002_Lipson2000_automatic-design-and-manufacture-of-robotic-lifefo.pdf) |
| SHA-256 ของต้นฉบับ | `1dab1d4fe2b10ef8deef95c6ebd58777bc9f5216444eeedc9ffaac7b21c04a38` |
| coverage ของ full text | 14/15 หน้า (93.33%); สกัดได้ 4,293 คำ |

## คำถามวิจัย

งาน Automatic design and manufacture of robotic lifeforms ค้นหา รักษา หรือประเมิน morphology ร่วมกับ control อย่างไร และทำให้เกิด bias แบบใด?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ methods และคำเทคนิคที่พบบ่อย ได้แก่ evolutionary, artificial, design, physical, control, process, page, robots วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล morphology ไวต่อ encoding, การจัดงบฝึก controller, task distribution และสมมติฐาน simulator มาก ความสำเร็จเสมือนไม่ถ่ายโอนไปรถแข่งโดยไม่มี physical correlation การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'ปิดวงจรจากการออกแบบที่วิวัฒนาการได้ไปสู่เครื่องจักรที่ผลิตและทดสอบจริง เป็นแม่แบบของ gate สร้างและทดสอบจริงหลังการค้นหา Level-0' ใน target ที่ระบุด้านล่าง |
| experiment และ control | รัน operator หรือกฎจัดสรรที่ได้จาก paper เทียบ evolution/QD และ fixed-topology control ที่ optimize แล้ว โดยจับคู่ seed, compute รวม, งบฝึก controller และสนาม held-out |
| หลักฐานผ่านและล้มเหลว | ยอมรับเมื่อ feasible archive coverage หรือผลงานสนาม held-out ดีขึ้นโดยไม่เพิ่มแบบ invalid, controller under-training หรือ evaluator disagreement มิฉะนั้นปฏิเสธการถ่ายโอน |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 15 หน้า, 28,177 ตัวอักษร, 4,293 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 14/15
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 6, 7, 8, 10 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: methods
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
