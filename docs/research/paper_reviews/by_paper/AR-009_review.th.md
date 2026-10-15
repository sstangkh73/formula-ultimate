# AR-009: AMZ Driverless: The Full Autonomous Racing System

English source: `AR-009_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Juraj Kabzan, M. I. Valls, Victor Reijgwart, Hubertus Franciscus Cornelis Hendrikx, Claas Ehmke, Manish Prajapat, Andreas Bühler, N. Gosala, Mehak Gupta, R. Sivanesan, Ankit Dhall, Eugenio Chisari, Napat Karnchanachari, Sonja Brits, Manuel Dangel, Inkyu Sa, Renaud Dubé, A. Gawel, Mark Pfeiffer, Alexander Liniger, J. Lygeros, R. Siegwart |
| ปี | 2020 |
| แหล่งตีพิมพ์ | J. Field Robotics |
| DOI | Not recorded |
| arXiv | 1905.05150 |
| ระเบียน canonical | [https://arxiv.org/abs/1905.05150](https://arxiv.org/abs/1905.05150) |
| หัวข้อในคลัง | การควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/14_autonomous_racing_strategy/AR-009_Kabzan2020_amz-driverless-the-full-autonomous-racing-system.pdf) |
| SHA-256 ของต้นฉบับ | `9827d916c735ff865147218933e7f153c94933031e66a1393de25f9f50f5a6ca` |
| coverage ของ full text | 40/40 หน้า (100.00%); สกัดได้ 19,235 คำ |

## คำถามวิจัย

งาน AMZ Driverless: The Full Autonomous Racing System รวม perception, estimation, planning, control, identification หรือ strategy ของการแข่งที่ขีดจำกัดอย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction และคำเทคนิคที่พบบ่อย ได้แก่ cones, cone, figure, model, track, system, used, estimation วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **ระบบไร้คนขับ Formula Student ครบวงพร้อมแบบจำลองรถและ MPC เป็นการ implement อ้างอิงที่มีเอกสารดี**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ระบบไร้คนขับ Formula Student ครบวงพร้อมแบบจำลองรถและ MPC เป็นการ implement อ้างอิงที่มีเอกสารดี
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'ระบบไร้คนขับ Formula Student ครบวงพร้อมแบบจำลองรถและ MPC เป็นการ implement อ้างอิงที่มีเอกสารดี' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'ระบบไร้คนขับ Formula Student ครบวงพร้อมแบบจำลองรถและ MPC เป็นการ implement อ้างอิงที่มีเอกสารดี' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล controller เฉพาะ stack, vehicle, sensor, latency, opponent, track และ safety policy การชนะใน simulator ไม่ใช่หลักฐานสนามจริงหรือ morphology การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **ระบบไร้คนขับ Formula Student ครบวงพร้อมแบบจำลองรถและ MPC เป็นการ implement อ้างอิงที่มีเอกสารดี** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'ระบบไร้คนขับ Formula Student ครบวงพร้อมแบบจำลองรถและ MPC เป็นการ implement อ้างอิงที่มีเอกสารดี' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | เทียบ MPC, learning และ hybrid baseline บนรถ/สนามเดียวกัน พร้อม latency, localization fault, grip shift, คู่แข่ง, energy/thermal limit และ safety constraint |
| หลักฐานผ่านและล้มเหลว | ต้องได้เวลาหรือ completion บน held-out ดีขึ้นซ้ำได้โดยไม่เพิ่ม safety violation, constraint breach หรือความได้เปรียบจาก vehicle model และแยกผล controller/morphology |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 40 หน้า, 114,436 ตัวอักษร, 19,235 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 40/40
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 4, 8, 11, 13, 16, 18, 19 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
