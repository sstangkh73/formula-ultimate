# QD-009: Abandoning Objectives: Evolution Through the Search for Novelty Alone

English source: `QD-009_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Joel Lehman, Kenneth O. Stanley |
| ปี | 2011 |
| แหล่งตีพิมพ์ | Evolutionary Computation |
| DOI | 10.1162/evco_a_00025 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.1162/evco_a_00025](https://doi.org/10.1162/evco_a_00025) |
| หัวข้อในคลัง | quality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/03_search_qd_multifidelity/QD-009_Lehman2011_abandoning-objectives-evolution-through-the-search.pdf) |
| SHA-256 ของต้นฉบับ | `de1e27262b4c10b6d20fae064bb4531e925e86162c5be0e1f4f511da9f2b184a` |
| coverage ของ full text | 39/39 หน้า (100.00%); สกัดได้ 18,147 คำ |

## คำถามวิจัย

งาน Abandoning Objectives: Evolution Through the Search for Novelty Alone แลกเปลี่ยน quality, diversity, evaluation cost และ fidelity error ใน adaptive search อย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา optimization/search, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, discussion, introduction และคำเทคนิคที่พบบ่อย ได้แก่ search, novelty, objective, maze, evolution, neat, tness, evolutionary วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **novelty search หลุดจากวัตถุประสงค์ที่หลอกลวงได้ เกี่ยวข้องเมื่อเวลาแข่งเพียงอย่างเดียวทำให้การค้นหาติดอยู่กับ layout แบบเดิม**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** novelty search หลุดจากวัตถุประสงค์ที่หลอกลวงได้ เกี่ยวข้องเมื่อเวลาแข่งเพียงอย่างเดียวทำให้การค้นหาติดอยู่กับ layout แบบเดิม
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'novelty search หลุดจากวัตถุประสงค์ที่หลอกลวงได้ เกี่ยวข้องเมื่อเวลาแข่งเพียงอย่างเดียวทำให้การค้นหาติดอยู่กับ layout แบบเดิม' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'novelty search หลุดจากวัตถุประสงค์ที่หลอกลวงได้ เกี่ยวข้องเมื่อเวลาแข่งเพียงอย่างเดียวทำให้การค้นหาติดอยู่กับ layout แบบเดิม' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ข้อสรุป QD ขึ้นกับ descriptor geometry, archive resolution, งบประเมิน และ proxy fidelity คะแนน archive อย่างเดียวไม่ใช่คุณค่าของรถ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **novelty search หลุดจากวัตถุประสงค์ที่หลอกลวงได้ เกี่ยวข้องเมื่อเวลาแข่งเพียงอย่างเดียวทำให้การค้นหาติดอยู่กับ layout แบบเดิม** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'novelty search หลุดจากวัตถุประสงค์ที่หลอกลวงได้ เกี่ยวข้องเมื่อเวลาแข่งเพียงอย่างเดียวทำให้การค้นหาติดอยู่กับ layout แบบเดิม' ใน target ที่ระบุด้านล่าง |
| experiment และ control | เทียบกฎค้นหาจาก paper กับ objective optimization, random search และ MAP-Elites โดยจับคู่ proposal, seed, งบ wall/CPU/GPU และ high-fidelity audit แบบ stratified |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่ม feasible coverage หรือ held-out quality พร้อม confidence interval และไม่มี proxy false-negative rate ที่ยอมรับไม่ได้ ผล fidelity สูงที่ยังไม่ทราบคงเป็น `not_estimable` |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 39 หน้า, 114,939 ตัวอักษร, 18,147 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 39/39
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 5, 6, 7, 8, 9 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, discussion, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
