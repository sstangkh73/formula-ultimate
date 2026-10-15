# QD-007: Crossing the Reality Gap: a Short Introduction to the Transferability Approach

English source: `QD-007_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Jean-Baptiste Mouret, S. Koos, S. Doncieux |
| ปี | 2013 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 1307.1870 |
| ระเบียน canonical | [https://arxiv.org/abs/1307.1870](https://arxiv.org/abs/1307.1870) |
| หัวข้อในคลัง | quality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/03_search_qd_multifidelity/QD-007_Mouret2013_crossing-the-reality-gap-a-short-introduction-to-t.pdf) |
| SHA-256 ของต้นฉบับ | `344a21c3537663269783f1b9d5a4e1309802f20ac5b73609c28c293d10b0db38` |
| coverage ของ full text | 5/5 หน้า (100.00%); สกัดได้ 4,381 คำ |

## คำถามวิจัย

งาน Crossing the Reality Gap: a Short Introduction to the Transferability Approach แลกเปลี่ยน quality, diversity, evaluation cost และ fidelity error ใน adaptive search อย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา optimization/search, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ conclusion, introduction, methods และคำเทคนิคที่พบบ่อย ได้แก่ simulation, reality, transferability, tness, robot, solutions, function, optimization วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **เรียนรู้ว่าพฤติกรรมจำลองใดถ่ายโอนสู่ของจริงได้และ optimize ความถ่ายโอนได้ เป็นแบบสำหรับการคัดเลือกที่คำนึงถึงการเลื่อนระดับ**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** เรียนรู้ว่าพฤติกรรมจำลองใดถ่ายโอนสู่ของจริงได้และ optimize ความถ่ายโอนได้ เป็นแบบสำหรับการคัดเลือกที่คำนึงถึงการเลื่อนระดับ
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'เรียนรู้ว่าพฤติกรรมจำลองใดถ่ายโอนสู่ของจริงได้และ optimize ความถ่ายโอนได้ เป็นแบบสำหรับการคัดเลือกที่คำนึงถึงการเลื่อนระดับ' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'เรียนรู้ว่าพฤติกรรมจำลองใดถ่ายโอนสู่ของจริงได้และ optimize ความถ่ายโอนได้ เป็นแบบสำหรับการคัดเลือกที่คำนึงถึงการเลื่อนระดับ' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ข้อสรุป QD ขึ้นกับ descriptor geometry, archive resolution, งบประเมิน และ proxy fidelity คะแนน archive อย่างเดียวไม่ใช่คุณค่าของรถ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **เรียนรู้ว่าพฤติกรรมจำลองใดถ่ายโอนสู่ของจริงได้และ optimize ความถ่ายโอนได้ เป็นแบบสำหรับการคัดเลือกที่คำนึงถึงการเลื่อนระดับ** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'เรียนรู้ว่าพฤติกรรมจำลองใดถ่ายโอนสู่ของจริงได้และ optimize ความถ่ายโอนได้ เป็นแบบสำหรับการคัดเลือกที่คำนึงถึงการเลื่อนระดับ' ใน target ที่ระบุด้านล่าง |
| experiment และ control | เทียบกฎค้นหาจาก paper กับ objective optimization, random search และ MAP-Elites โดยจับคู่ proposal, seed, งบ wall/CPU/GPU และ high-fidelity audit แบบ stratified |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่ม feasible coverage หรือ held-out quality พร้อม confidence interval และไม่มี proxy false-negative rate ที่ยอมรับไม่ได้ ผล fidelity สูงที่ยังไม่ทราบคงเป็น `not_estimable` |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 5 หน้า, 26,805 ตัวอักษร, 4,381 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 5/5
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 5 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: conclusion, introduction, methods
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
