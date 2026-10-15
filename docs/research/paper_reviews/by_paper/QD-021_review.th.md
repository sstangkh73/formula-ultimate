# QD-021: Robots that can adapt like animals

English source: `QD-021_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Antoine Cully, J. Clune, Danesh Tarapore, Jean-Baptiste Mouret |
| ปี | 2015 |
| แหล่งตีพิมพ์ | Nature |
| DOI | Not recorded |
| arXiv | 1407.3501 |
| ระเบียน canonical | [https://arxiv.org/abs/1407.3501](https://arxiv.org/abs/1407.3501) |
| หัวข้อในคลัง | quality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/03_search_qd_multifidelity/QD-021_Cully2015_robots-that-can-adapt-like-animals.pdf) |
| SHA-256 ของต้นฉบับ | `ff088dfdb1a7d96a2edc85aa2ab8e4995498a025289be947582c057c3b22a99b` |
| coverage ของ full text | 26/26 หน้า (100.00%); สกัดได้ 22,354 คำ |

## คำถามวิจัย

งาน Robots that can adapt like animals แลกเปลี่ยน quality, diversity, evaluation cost และ fidelity error ใน adaptive search อย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา optimization/search, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ methods และคำเทคนิคที่พบบ่อย ได้แก่ robot, performance, algorithm, behavior, space, behavioral, behavior-performance, trial วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **คลัง MAP-Elites ที่คำนวณไว้ถูกนำกลับมาใช้ฟื้นตัวเร็วหลังเสียหาย เป็นแบบการใช้คลังซ้ำเมื่อสภาพเสื่อมลง**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** คลัง MAP-Elites ที่คำนวณไว้ถูกนำกลับมาใช้ฟื้นตัวเร็วหลังเสียหาย เป็นแบบการใช้คลังซ้ำเมื่อสภาพเสื่อมลง
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'คลัง MAP-Elites ที่คำนวณไว้ถูกนำกลับมาใช้ฟื้นตัวเร็วหลังเสียหาย เป็นแบบการใช้คลังซ้ำเมื่อสภาพเสื่อมลง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'คลัง MAP-Elites ที่คำนวณไว้ถูกนำกลับมาใช้ฟื้นตัวเร็วหลังเสียหาย เป็นแบบการใช้คลังซ้ำเมื่อสภาพเสื่อมลง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ข้อสรุป QD ขึ้นกับ descriptor geometry, archive resolution, งบประเมิน และ proxy fidelity คะแนน archive อย่างเดียวไม่ใช่คุณค่าของรถ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **คลัง MAP-Elites ที่คำนวณไว้ถูกนำกลับมาใช้ฟื้นตัวเร็วหลังเสียหาย เป็นแบบการใช้คลังซ้ำเมื่อสภาพเสื่อมลง** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'คลัง MAP-Elites ที่คำนวณไว้ถูกนำกลับมาใช้ฟื้นตัวเร็วหลังเสียหาย เป็นแบบการใช้คลังซ้ำเมื่อสภาพเสื่อมลง' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | เทียบกฎค้นหาจาก paper กับ objective optimization, random search และ MAP-Elites โดยจับคู่ proposal, seed, งบ wall/CPU/GPU และ high-fidelity audit แบบ stratified |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่ม feasible coverage หรือ held-out quality พร้อม confidence interval และไม่มี proxy false-negative rate ที่ยอมรับไม่ได้ ผล fidelity สูงที่ยังไม่ทราบคงเป็น `not_estimable` |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 26 หน้า, 133,348 ตัวอักษร, 22,354 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 26/26
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 7, 9, 13, 15 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: methods
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
