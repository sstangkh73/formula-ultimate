# AE-010: WindsorML: High-Fidelity Computational Fluid Dynamics Dataset For Automotive Aerodynamics

English source: `AE-010_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Neil Ashton, Jordan B. Angel, A. Ghate, G. Kenway, M. Wong, C. Kiris, Astrid Walle, Danielle C. Maddix, G. Page |
| ปี | 2024 |
| แหล่งตีพิมพ์ | Neural Information Processing Systems |
| DOI | Not recorded |
| arXiv | 2407.19320 |
| ระเบียน canonical | [https://arxiv.org/abs/2407.19320](https://arxiv.org/abs/2407.19320) |
| หัวข้อในคลัง | อากาศพลศาสตร์และข้อมูล aerodynamic |
| ความสัมพันธ์กับโครงการ | `data` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/10_aerodynamics/AE-010_Ashton2024_windsorml-high-fidelity-computational-fluid-dynami.pdf) |
| SHA-256 ของต้นฉบับ | `6c2c5b3118718f1f129b78cad2a4f351e66bdfab39004fc15cd322c897dbac64` |
| coverage ของ full text | 35/39 หน้า (89.74%); สกัดได้ 11,517 คำ |

## คำถามวิจัย

งาน WindsorML: High-Fidelity Computational Fluid Dynamics Dataset For Automotive Aerodynamics ยืนยันกลไก aerodynamic, dataset, solver หรือ surrogate ใด และในโดเมน geometry/flow ใด?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction และคำเทคนิคที่พบบ่อย ได้แก่ dataset, data, coefficient, geometry, body, windsor, velocity, drag วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **LES แบบ wall-modelled ของ Windsor body หลายแบบ (CC-BY-SA) เป็นข้อมูล fidelity สูงแบบเปิดที่รวมผลใกล้พื้น**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** LES แบบ wall-modelled ของ Windsor body หลายแบบ (CC-BY-SA) เป็นข้อมูล fidelity สูงแบบเปิดที่รวมผลใกล้พื้น
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'LES แบบ wall-modelled ของ Windsor body หลายแบบ (CC-BY-SA) เป็นข้อมูล fidelity สูงแบบเปิดที่รวมผลใกล้พื้น' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้ออากาศพลศาสตร์และข้อมูล aerodynamic
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'LES แบบ wall-modelled ของ Windsor body หลายแบบ (CC-BY-SA) เป็นข้อมูล fidelity สูงแบบเปิดที่รวมผลใกล้พื้น' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้ออากาศพลศาสตร์และข้อมูล aerodynamic โดยเป็นความเชื่อมโยงชนิด `data` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ข้อสรุป aero ผูกกับตระกูล geometry, Reynolds number, turbulence/ground/wheel treatment, mesh และข้อมูล validation การถ่ายโอนจากรถถนนหรือทรงมาตรฐานมีขอบเขต การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **LES แบบ wall-modelled ของ Windsor body หลายแบบ (CC-BY-SA) เป็นข้อมูล fidelity สูงแบบเปิดที่รวมผลใกล้พื้น** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-flow-heat path ของ Work 121, aero-field evaluator และ surrogate promotion audit** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-flow-heat path ของ Work 121, aero-field evaluator และ surrogate promotion audit |
| การเปลี่ยนแปลงที่เสนอ | ลงทะเบียนชุดข้อมูล/benchmark ที่เกี่ยวกับ 'LES แบบ wall-modelled ของ Windsor body หลายแบบ (CC-BY-SA) เป็นข้อมูล fidelity สูงแบบเปิดที่รวมผลใกล้พื้น' พร้อม licence, domain, split และ leakage control แล้วใช้เฉพาะ calibration, pretraining หรือ independent test ตามที่ลงทะเบียน |
| experiment และ control | ประเมิน geometry เดียวกันข้าม ride height, yaw, wheel/ground treatment, Reynolds number และ cooling flow แล้วเทียบ surrogate/CFD กับ independent CFD และการทดลองที่มี |
| หลักฐานผ่านและล้มเหลว | ต้องมี error ของ force, moment, balance, surface field และ uncertainty มีขอบเขตบน geometry held-out และไม่คัดทิ้งรูปทรงไม่คุ้นอย่างเป็นระบบ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 39 หน้า, 70,759 ตัวอักษร, 11,517 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 35/39
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 4, 7, 9, 16, 17, 21 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
