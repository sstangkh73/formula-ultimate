# AR-002: Optimization-Based Autonomous Racing of 1:43 Scale RC Cars

English source: `AR-002_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Alexander Liniger, A. Domahidi, M. Morari |
| ปี | 2015 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 1711.07300 |
| ระเบียน canonical | [https://arxiv.org/abs/1711.07300](https://arxiv.org/abs/1711.07300) |
| หัวข้อในคลัง | การควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/14_autonomous_racing_strategy/AR-002_Liniger2015_optimization-based-autonomous-racing-of-1-43-scale.pdf) |
| SHA-256 ของต้นฉบับ | `bb5d2330f57ab2b703429d12471854e14136787bfb232b7577e1310791c6103c` |
| coverage ของ full text | 20/20 หน้า (100.00%); สกัดได้ 11,975 คำ |

## คำถามวิจัย

งาน Optimization-Based Autonomous Racing of 1:43 Scale RC Cars รวม perception, estimation, planning, control, identification หรือ strategy ของการแข่งที่ขีดจำกัดอย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข, หลักฐานคณิตศาสตร์/เชิงรูปนัย, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ control, path, model, time, controller, problem, horizon, trajectory วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **model predictive contouring control สำหรับการแข่ง เป็น baseline ตัวควบคุมที่ implement ได้พร้อมขอบฟ้าและขีดจำกัด actuator ชัดเจน**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** model predictive contouring control สำหรับการแข่ง เป็น baseline ตัวควบคุมที่ implement ได้พร้อมขอบฟ้าและขีดจำกัด actuator ชัดเจน
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'model predictive contouring control สำหรับการแข่ง เป็น baseline ตัวควบคุมที่ implement ได้พร้อมขอบฟ้าและขีดจำกัด actuator ชัดเจน' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'model predictive contouring control สำหรับการแข่ง เป็น baseline ตัวควบคุมที่ implement ได้พร้อมขอบฟ้าและขีดจำกัด actuator ชัดเจน' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล controller เฉพาะ stack, vehicle, sensor, latency, opponent, track และ safety policy การชนะใน simulator ไม่ใช่หลักฐานสนามจริงหรือ morphology การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **model predictive contouring control สำหรับการแข่ง เป็น baseline ตัวควบคุมที่ implement ได้พร้อมขอบฟ้าและขีดจำกัด actuator ชัดเจน** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'model predictive contouring control สำหรับการแข่ง เป็น baseline ตัวควบคุมที่ implement ได้พร้อมขอบฟ้าและขีดจำกัด actuator ชัดเจน' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | เทียบ MPC, learning และ hybrid baseline บนรถ/สนามเดียวกัน พร้อม latency, localization fault, grip shift, คู่แข่ง, energy/thermal limit และ safety constraint |
| หลักฐานผ่านและล้มเหลว | ต้องได้เวลาหรือ completion บน held-out ดีขึ้นซ้ำได้โดยไม่เพิ่ม safety violation, constraint breach หรือความได้เปรียบจาก vehicle model และแยกผล controller/morphology |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 20 หน้า, 68,772 ตัวอักษร, 11,975 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 20/20
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 10, 11, 15, 16, 18 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
