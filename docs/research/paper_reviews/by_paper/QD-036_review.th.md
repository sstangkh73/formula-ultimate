# QD-036: Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations

English source: `QD-036_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | M. Raissi, P. Perdikaris, G. Karniadakis |
| ปี | 2017 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 1711.10561 |
| ระเบียน canonical | [https://arxiv.org/abs/1711.10561](https://arxiv.org/abs/1711.10561) |
| หัวข้อในคลัง | quality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/03_search_qd_multifidelity/QD-036_Raissi2017_physics-informed-deep-learning-part-i-data-driven.pdf) |
| SHA-256 ของต้นฉบับ | `2a8db6776a110a4f36bd1e36af79cf31a2e74baa5af8f7ee3d9286a75fdc400d` |
| coverage ของ full text | 22/22 หน้า (100.00%); สกัดได้ 7,184 คำ |

## คำถามวิจัย

งาน Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations แลกเปลี่ยน quality, diversity, evaluation cost และ fidelity error ใน adaptive search อย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐานคณิตศาสตร์/เชิงรูปนัย, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ equation, neural, data, solution, network, number, time, e-03 วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **physics-informed neural network เป็นตระกูล surrogate ที่ฝังสมการควบคุม เกี่ยวข้องเมื่อข้อมูลมีน้อย**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** physics-informed neural network เป็นตระกูล surrogate ที่ฝังสมการควบคุม เกี่ยวข้องเมื่อข้อมูลมีน้อย
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'physics-informed neural network เป็นตระกูล surrogate ที่ฝังสมการควบคุม เกี่ยวข้องเมื่อข้อมูลมีน้อย' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'physics-informed neural network เป็นตระกูล surrogate ที่ฝังสมการควบคุม เกี่ยวข้องเมื่อข้อมูลมีน้อย' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อquality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ข้อสรุป QD ขึ้นกับ descriptor geometry, archive resolution, งบประเมิน และ proxy fidelity คะแนน archive อย่างเดียวไม่ใช่คุณค่าของรถ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **physics-informed neural network เป็นตระกูล surrogate ที่ฝังสมการควบคุม เกี่ยวข้องเมื่อข้อมูลมีน้อย** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'physics-informed neural network เป็นตระกูล surrogate ที่ฝังสมการควบคุม เกี่ยวข้องเมื่อข้อมูลมีน้อย' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | เทียบกฎค้นหาจาก paper กับ objective optimization, random search และ MAP-Elites โดยจับคู่ proposal, seed, งบ wall/CPU/GPU และ high-fidelity audit แบบ stratified |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่ม feasible coverage หรือ held-out quality พร้อม confidence interval และไม่มี proxy false-negative rate ที่ยอมรับไม่ได้ ผล fidelity สูงที่ยังไม่ทราบคงเป็น `not_estimable` |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 22 หน้า, 40,217 ตัวอักษร, 7,184 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 22/22
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 7, 8, 9, 11, 12, 14 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
