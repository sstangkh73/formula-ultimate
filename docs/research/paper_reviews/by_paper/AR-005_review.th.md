# AR-005: Autonomous Vehicles on the Edge: A Survey on Autonomous Vehicle Racing

English source: `AR-005_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Johannes Betz, Hongrui Zheng, Alexander Liniger, Ugo Rosolia, Phillip Karle, Madhur Behl, V. Krovi, Rahul Mangharam |
| ปี | 2022 |
| แหล่งตีพิมพ์ | IEEE Open Journal of Intelligent Transportation Systems |
| DOI | Not recorded |
| arXiv | 2202.07008 |
| ระเบียน canonical | [https://arxiv.org/abs/2202.07008](https://arxiv.org/abs/2202.07008) |
| หัวข้อในคลัง | การควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/14_autonomous_racing_strategy/AR-005_Betz2022_autonomous-vehicles-on-the-edge-a-survey-on-autono.pdf) |
| SHA-256 ของต้นฉบับ | `d85e0429fc7b4b44e19f3b320eede56b86a68b3734910bef24d1192d7da84ee4` |
| coverage ของ full text | 29/29 หน้า (100.00%); สกัดได้ 29,646 คำ |

## คำถามวิจัย

งาน Autonomous Vehicles on the Edge: A Survey on Autonomous Vehicle Racing รวม perception, estimation, planning, control, identification หรือ strategy ของการแข่งที่ขีดจำกัดอย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ ไม่พบ heading ที่เชื่อถือได้ และคำเทคนิคที่พบบ่อย ได้แก่ autonomous, control, vehicle, racing, available, online, https, ieee วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **survey การรับรู้ การวางแผน การควบคุม และการจำลองในการแข่งอัตโนมัติ เป็นแผนที่เครื่องมือและชุดข้อมูล**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** survey การรับรู้ การวางแผน การควบคุม และการจำลองในการแข่งอัตโนมัติ เป็นแผนที่เครื่องมือและชุดข้อมูล
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'survey การรับรู้ การวางแผน การควบคุม และการจำลองในการแข่งอัตโนมัติ เป็นแผนที่เครื่องมือและชุดข้อมูล' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'survey การรับรู้ การวางแผน การควบคุม และการจำลองในการแข่งอัตโนมัติ เป็นแผนที่เครื่องมือและชุดข้อมูล' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล controller เฉพาะ stack, vehicle, sensor, latency, opponent, track และ safety policy การชนะใน simulator ไม่ใช่หลักฐานสนามจริงหรือ morphology การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **survey การรับรู้ การวางแผน การควบคุม และการจำลองในการแข่งอัตโนมัติ เป็นแผนที่เครื่องมือและชุดข้อมูล** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'survey การรับรู้ การวางแผน การควบคุม และการจำลองในการแข่งอัตโนมัติ เป็นแผนที่เครื่องมือและชุดข้อมูล' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | เทียบ MPC, learning และ hybrid baseline บนรถ/สนามเดียวกัน พร้อม latency, localization fault, grip shift, คู่แข่ง, energy/thermal limit และ safety constraint |
| หลักฐานผ่านและล้มเหลว | ต้องได้เวลาหรือ completion บน held-out ดีขึ้นซ้ำได้โดยไม่เพิ่ม safety violation, constraint breach หรือความได้เปรียบจาก vehicle model และแยกผล controller/morphology |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 29 หน้า, 189,240 ตัวอักษร, 29,646 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 29/29
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 5, 8, 9, 10 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
