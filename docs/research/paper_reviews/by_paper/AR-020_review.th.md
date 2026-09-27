# AR-020: Bridging RL and MPC for mixed-integer optimal control with application to Formula 1 race strategies

English source: `AR-020_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Joschua Wüthrich, Romir Damle, Giona Fieni, M. Zeilinger, C. Onder, Andrea Carron |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2604.00826 |
| ระเบียน canonical | [https://arxiv.org/abs/2604.00826](https://arxiv.org/abs/2604.00826) |
| หัวข้อในคลัง | การควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/14_autonomous_racing_strategy/AR-020_Wuthrich2026_bridging-rl-and-mpc-for-mixed-integer-optimal-cont.pdf) |
| SHA-256 ของต้นฉบับ | `ae93eb9f850808f67d51a5d1f9ead026ba77b11ccd1543a834d8d039aea53ee8` |
| coverage ของ full text | 8/8 หน้า (100.00%); สกัดได้ 7,312 คำ |

## คำถามวิจัย

งาน Bridging RL and MPC for mixed-integer optimal control with application to Formula 1 race strategies รวม perception, estimation, planning, control, identification หรือ strategy ของการแข่งที่ขีดจำกัดอย่างไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ ไม่พบ heading ที่เชื่อถือได้ และคำเทคนิคที่พบบ่อย ได้แก่ hybrid, cost, control, discrete, time, continuous, race, action วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **รวม RL กับ MPC สำหรับกลยุทธ์การแข่งแบบ mixed-integer เกี่ยวข้องกับการเลือกกลยุทธ์แบบไม่ต่อเนื่อง**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** รวม RL กับ MPC สำหรับกลยุทธ์การแข่งแบบ mixed-integer เกี่ยวข้องกับการเลือกกลยุทธ์แบบไม่ต่อเนื่อง
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'รวม RL กับ MPC สำหรับกลยุทธ์การแข่งแบบ mixed-integer เกี่ยวข้องกับการเลือกกลยุทธ์แบบไม่ต่อเนื่อง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'รวม RL กับ MPC สำหรับกลยุทธ์การแข่งแบบ mixed-integer เกี่ยวข้องกับการเลือกกลยุทธ์แบบไม่ต่อเนื่อง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล controller เฉพาะ stack, vehicle, sensor, latency, opponent, track และ safety policy การชนะใน simulator ไม่ใช่หลักฐานสนามจริงหรือ morphology การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **รวม RL กับ MPC สำหรับกลยุทธ์การแข่งแบบ mixed-integer เกี่ยวข้องกับการเลือกกลยุทธ์แบบไม่ต่อเนื่อง** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'รวม RL กับ MPC สำหรับกลยุทธ์การแข่งแบบ mixed-integer เกี่ยวข้องกับการเลือกกลยุทธ์แบบไม่ต่อเนื่อง' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | เทียบ MPC, learning และ hybrid baseline บนรถ/สนามเดียวกัน พร้อม latency, localization fault, grip shift, คู่แข่ง, energy/thermal limit และ safety constraint |
| หลักฐานผ่านและล้มเหลว | ต้องได้เวลาหรือ completion บน held-out ดีขึ้นซ้ำได้โดยไม่เพิ่ม safety violation, constraint breach หรือความได้เปรียบจาก vehicle model และแยกผล controller/morphology |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 8 หน้า, 44,410 ตัวอักษร, 7,312 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 8/8
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 5, 6, 7 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
