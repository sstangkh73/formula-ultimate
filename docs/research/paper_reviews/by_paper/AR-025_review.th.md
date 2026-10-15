# AR-025: Real-Time Adaptive Velocity Optimization for Autonomous Electric Cars at the Limits of Handling

English source: `AR-025_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Thomas Herrmann, Alexander Wischnewski, Leonhard Hermansdorfer, Johannes Betz, Markus Lienkamp |
| ปี | 2021 |
| แหล่งตีพิมพ์ | IEEE Transactions on Intelligent Vehicles |
| DOI | 10.1109/tiv.2020.3047858 |
| arXiv | 2012.13586 |
| ระเบียน canonical | [https://doi.org/10.1109/tiv.2020.3047858](https://doi.org/10.1109/tiv.2020.3047858) |
| หัวข้อในคลัง | การควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/14_autonomous_racing_strategy/AR-025_Herrmann2021_real-time-adaptive-velocity-optimization-for-auton.pdf) |
| SHA-256 ของต้นฉบับ | `1a41bb54b79ca4e09aa1f8a5327bdbf50acbccdac3c9604f2f22f38f7b501ead` |
| coverage ของ full text | 13/13 หน้า (100.00%); สกัดได้ 11,640 คำ |

## คำถามวิจัย

งาน Real-Time Adaptive Velocity Optimization for Autonomous Electric Cars at the Limits of Handling รวม perception, estimation, planning, control, identification หรือ strategy ของการแข่งที่ขีดจำกัดอย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ ไม่พบ heading ที่เชื่อถือได้ และคำเทคนิคที่พบบ่อย ได้แก่ optimization, velocity, sglo, acceleration, race, vehicle, path, limits วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **การวางแผนความเร็วแบบเวลาจริงที่มีขีดจำกัดพลังงานและแรงเสียดทานบนรถแข่งไฟฟ้า เป็นชิ้นส่วนผู้ขับสำหรับการแข่งที่พลังงานจำกัด**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** การวางแผนความเร็วแบบเวลาจริงที่มีขีดจำกัดพลังงานและแรงเสียดทานบนรถแข่งไฟฟ้า เป็นชิ้นส่วนผู้ขับสำหรับการแข่งที่พลังงานจำกัด
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'การวางแผนความเร็วแบบเวลาจริงที่มีขีดจำกัดพลังงานและแรงเสียดทานบนรถแข่งไฟฟ้า เป็นชิ้นส่วนผู้ขับสำหรับการแข่งที่พลังงานจำกัด' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'การวางแผนความเร็วแบบเวลาจริงที่มีขีดจำกัดพลังงานและแรงเสียดทานบนรถแข่งไฟฟ้า เป็นชิ้นส่วนผู้ขับสำหรับการแข่งที่พลังงานจำกัด' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล controller เฉพาะ stack, vehicle, sensor, latency, opponent, track และ safety policy การชนะใน simulator ไม่ใช่หลักฐานสนามจริงหรือ morphology การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **การวางแผนความเร็วแบบเวลาจริงที่มีขีดจำกัดพลังงานและแรงเสียดทานบนรถแข่งไฟฟ้า เป็นชิ้นส่วนผู้ขับสำหรับการแข่งที่พลังงานจำกัด** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'การวางแผนความเร็วแบบเวลาจริงที่มีขีดจำกัดพลังงานและแรงเสียดทานบนรถแข่งไฟฟ้า เป็นชิ้นส่วนผู้ขับสำหรับการแข่งที่พลังงานจำกัด' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | เทียบ MPC, learning และ hybrid baseline บนรถ/สนามเดียวกัน พร้อม latency, localization fault, grip shift, คู่แข่ง, energy/thermal limit และ safety constraint |
| หลักฐานผ่านและล้มเหลว | ต้องได้เวลาหรือ completion บน held-out ดีขึ้นซ้ำได้โดยไม่เพิ่ม safety violation, constraint breach หรือความได้เปรียบจาก vehicle model และแยกผล controller/morphology |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 13 หน้า, 69,706 ตัวอักษร, 11,640 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 13/13
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 5, 8 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
