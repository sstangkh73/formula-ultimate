# QD-029: Multi-fidelity optimization via surrogate modelling

English source: `QD-029_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Alexander I.J Forrester, András Sóbester, Andy J Keane |
| ปี | 2007 |
| แหล่งตีพิมพ์ | Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences |
| DOI | 10.1098/rspa.2007.1900 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.1098/rspa.2007.1900](https://doi.org/10.1098/rspa.2007.1900) |
| หัวข้อในคลัง | quality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/03_search_qd_multifidelity/QD-029_Forrester2007_multi-fidelity-optimization-via-surrogate-modellin.pdf) |
| SHA-256 ของต้นฉบับ | `c6344012576da38d6c014bb51ee90e561d88020e4c9488eecd003f7483aec89f` |
| coverage ของ full text | 19/19 หน้า (100.00%); สกัดได้ 8,679 คำ |

## คำถามวิจัย

งาน Multi-fidelity optimization via surrogate modelling แลกเปลี่ยน quality, diversity, evaluation cost และ fidelity error ใน adaptive search อย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข, หลักฐานคณิตศาสตร์/เชิงรูปนัย** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ ไม่พบ heading ที่เชื่อถือได้ และคำเทคนิคที่พบบ่อย ได้แก่ data, co-kriging, model, points, function, optimization, error, kriging วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **optimization แบบ multi-fidelity ด้วย co-kriging พร้อมตัวอย่างอากาศพลศาสตร์ เป็นสูตรทางวิศวกรรมแบบคลาสสิก**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** optimization แบบ multi-fidelity ด้วย co-kriging พร้อมตัวอย่างอากาศพลศาสตร์ เป็นสูตรทางวิศวกรรมแบบคลาสสิก
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'optimization แบบ multi-fidelity ด้วย co-kriging พร้อมตัวอย่างอากาศพลศาสตร์ เป็นสูตรทางวิศวกรรมแบบคลาสสิก' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'optimization แบบ multi-fidelity ด้วย co-kriging พร้อมตัวอย่างอากาศพลศาสตร์ เป็นสูตรทางวิศวกรรมแบบคลาสสิก' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ข้อสรุป QD ขึ้นกับ descriptor geometry, archive resolution, งบประเมิน และ proxy fidelity คะแนน archive อย่างเดียวไม่ใช่คุณค่าของรถ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **optimization แบบ multi-fidelity ด้วย co-kriging พร้อมตัวอย่างอากาศพลศาสตร์ เป็นสูตรทางวิศวกรรมแบบคลาสสิก** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'optimization แบบ multi-fidelity ด้วย co-kriging พร้อมตัวอย่างอากาศพลศาสตร์ เป็นสูตรทางวิศวกรรมแบบคลาสสิก' ใน target ที่ระบุด้านล่าง |
| experiment และ control | เทียบกฎค้นหาจาก paper กับ objective optimization, random search และ MAP-Elites โดยจับคู่ proposal, seed, งบ wall/CPU/GPU และ high-fidelity audit แบบ stratified |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่ม feasible coverage หรือ held-out quality พร้อม confidence interval และไม่มี proxy false-negative rate ที่ยอมรับไม่ได้ ผล fidelity สูงที่ยังไม่ทราบคงเป็น `not_estimable` |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 19 หน้า, 47,633 ตัวอักษร, 8,679 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 19/19
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 6, 9, 10, 11, 12, 15, 16 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
