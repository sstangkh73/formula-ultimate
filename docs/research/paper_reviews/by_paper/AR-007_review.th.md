# AR-007: TUM Autonomous Motorsport: An Autonomous Racing Software for the Indy Autonomous Challenge

English source: `AR-007_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Johannes Betz, Tobias Betz, F. Fent, Maximilian Geisslinger, Alexander Heilmeier, Leonhard Hermansdorfer, T. Herrmann, Sebastian Huch, Phillip Karle, M. Lienkamp, B. Lohmann, Felix Nobis, Levent Ogretmen, Matthias Rowold, Florian Sauerbeck, Tim Stahl, Rainer Trauth, Frederik Werner, Alexander Wischnewski |
| ปี | 2023 |
| แหล่งตีพิมพ์ | J. Field Robotics |
| DOI | Not recorded |
| arXiv | 2205.15979 |
| ระเบียน canonical | [https://arxiv.org/abs/2205.15979](https://arxiv.org/abs/2205.15979) |
| หัวข้อในคลัง | การควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/14_autonomous_racing_strategy/AR-007_Betz2023_tum-autonomous-motorsport-an-autonomous-racing-sof.pdf) |
| SHA-256 ของต้นฉบับ | `92c1b50e8cf6f71dde574a9b08dd30ac6fd3f27e3d0039bf92e1432c867d6f92` |
| coverage ของ full text | 27/27 หน้า (100.00%); สกัดได้ 23,556 คำ |

## คำถามวิจัย

งาน TUM Autonomous Motorsport: An Autonomous Racing Software for the Indy Autonomous Challenge รวม perception, estimation, planning, control, identification หรือ strategy ของการแข่งที่ขีดจำกัดอย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐาน simulation/เชิงตัวเลข, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ vehicle, autonomous, software, wiley, race, object, racing, based วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **ชุดซอฟต์แวร์การแข่งอัตโนมัติแบบเปิดครบวงรวมการวางแผนและการควบคุม เป็นชิ้นส่วนที่นำมาใช้กับ baseline ผู้ขับได้**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ชุดซอฟต์แวร์การแข่งอัตโนมัติแบบเปิดครบวงรวมการวางแผนและการควบคุม เป็นชิ้นส่วนที่นำมาใช้กับ baseline ผู้ขับได้
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'ชุดซอฟต์แวร์การแข่งอัตโนมัติแบบเปิดครบวงรวมการวางแผนและการควบคุม เป็นชิ้นส่วนที่นำมาใช้กับ baseline ผู้ขับได้' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'ชุดซอฟต์แวร์การแข่งอัตโนมัติแบบเปิดครบวงรวมการวางแผนและการควบคุม เป็นชิ้นส่วนที่นำมาใช้กับ baseline ผู้ขับได้' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล controller เฉพาะ stack, vehicle, sensor, latency, opponent, track และ safety policy การชนะใน simulator ไม่ใช่หลักฐานสนามจริงหรือ morphology การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **ชุดซอฟต์แวร์การแข่งอัตโนมัติแบบเปิดครบวงรวมการวางแผนและการควบคุม เป็นชิ้นส่วนที่นำมาใช้กับ baseline ผู้ขับได้** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'ชุดซอฟต์แวร์การแข่งอัตโนมัติแบบเปิดครบวงรวมการวางแผนและการควบคุม เป็นชิ้นส่วนที่นำมาใช้กับ baseline ผู้ขับได้' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | เทียบ MPC, learning และ hybrid baseline บนรถ/สนามเดียวกัน พร้อม latency, localization fault, grip shift, คู่แข่ง, energy/thermal limit และ safety constraint |
| หลักฐานผ่านและล้มเหลว | ต้องได้เวลาหรือ completion บน held-out ดีขึ้นซ้ำได้โดยไม่เพิ่ม safety violation, constraint breach หรือความได้เปรียบจาก vehicle model และแยกผล controller/morphology |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 27 หน้า, 146,876 ตัวอักษร, 23,556 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 27/27
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 7, 8, 10, 14, 18, 19, 20 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
