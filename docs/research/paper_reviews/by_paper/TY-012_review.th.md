# TY-012: A State-Space Approach to Modeling Tire Degradation in Formula 1 Racing

English source: `TY-012_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Cole Cappello, A. Hoegh |
| ปี | 2025 |
| แหล่งตีพิมพ์ | Journal of Sports Analytics |
| DOI | Not recorded |
| arXiv | 2512.00640 |
| ระเบียน canonical | [https://arxiv.org/abs/2512.00640](https://arxiv.org/abs/2512.00640) |
| หัวข้อในคลัง | ยาง แรงเสียดทาน และการสัมผัสถนน |
| ความสัมพันธ์กับโครงการ | `data` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/09_tyres_friction/TY-012_Cappello2025_a-state-space-approach-to-modeling-tire-degradatio.pdf) |
| SHA-256 ของต้นฉบับ | `ecacae600f48f42f4b9c51586b5e4784901f05def46737fb96e1188187ed7c7e` |
| coverage ของ full text | 18/18 หน้า (100.00%); สกัดได้ 6,059 คำ |

## คำถามวิจัย

งาน A State-Space Approach to Modeling Tire Degradation in Formula 1 Racing ระบุ state และ operating condition ของ tyre/contact ใด และรองรับการทำนายการแข่งแบบ transient ได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานคณิตศาสตร์/เชิงรูปนัย** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction, results และคำเทคนิคที่พบบ่อย ได้แก่ degradation, model, tire, tires, time, race, models, times วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อยาง แรงเสียดทาน และการสัมผัสถนน
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อยาง แรงเสียดทาน และการสัมผัสถนน โดยเป็นความเชื่อมโยงชนิด `data` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

พารามิเตอร์และข้อสรุปยางขึ้นกับ condition, construction และ dataset curve ที่ fit แล้วนอก envelope load/temperature/wear ยังไม่ validate การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ground-interaction contract, tyre-state estimator และการส่งต่อ uncertainty ไปยัง lap/safety** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ground-interaction contract, tyre-state estimator และการส่งต่อ uncertainty ไปยัง lap/safety |
| การเปลี่ยนแปลงที่เสนอ | ลงทะเบียนชุดข้อมูล/benchmark ที่เกี่ยวกับ 'การเสื่อมของยางแบบ state-space เชิง Bayesian ที่ประมาณจากเวลาต่อรอบ F1 จริงปี 2025 เป็นอัตราการเสื่อมจากข้อมูลสำหรับจำลองระยะการแข่ง' พร้อม licence, domain, split และ leakage control แล้วใช้เฉพาะ calibration, pretraining หรือ independent test ตามที่ลงทะเบียน |
| experiment และ control | fit และ validate กับ manoeuvre แยกข้าม combined slip, load, camber, pressure, temperature, wear, speed และสภาพถนน แล้วเทียบ low-fidelity model ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ต้องมี force/moment และ temperature/wear error มีขอบเขตบน manoeuvre held-out และทำ lap replay ดีขึ้นโดยไม่ซ่อน extrapolation นอก tyre envelope |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 18 หน้า, 35,225 ตัวอักษร, 6,059 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 18/18
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 5, 6, 7, 14, 17 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
