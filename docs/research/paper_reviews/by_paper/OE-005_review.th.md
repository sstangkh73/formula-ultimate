# OE-005: Neural Graph Evolution: Towards Efficient Automatic Robot Design

English source: `OE-005_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Tingwu Wang, Yuhao Zhou, S. Fidler, Jimmy Ba |
| ปี | 2019 |
| แหล่งตีพิมพ์ | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 1906.05370 |
| ระเบียน canonical | [https://arxiv.org/abs/1906.05370](https://arxiv.org/abs/1906.05370) |
| หัวข้อในคลัง | การออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/01_open_ended_codesign/OE-005_Wang2019_neural-graph-evolution-towards-efficient-automatic.pdf) |
| SHA-256 ของต้นฉบับ | `267dbde264760f353cfb3d63d162a814f581a44a17896f7e9c4bcdb3dc1b2166` |
| coverage ของ full text | 17/17 หน้า (100.00%); สกัดได้ 9,300 คำ |

## คำถามวิจัย

งาน Neural Graph Evolution: Towards Efficient Automatic Robot Design ค้นหา รักษา หรือประเมิน morphology ร่วมกับ control อย่างไร และทำให้เกิด bias แบบใด?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข, การศึกษา optimization/search, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, methods และคำเทคนิคที่พบบ่อย ได้แก่ graph, species, search, model, policy, generation, neural, design วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **นำตัวควบคุมแบบ graph network กลับมาใช้ข้ามการกลายพันธุ์ของรูปร่างเพื่อลดต้นทุนฝึกใหม่ เกี่ยวข้องเมื่อทุก topology ต้องมีผู้ขับที่ปรับแล้วของตัวเอง**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** นำตัวควบคุมแบบ graph network กลับมาใช้ข้ามการกลายพันธุ์ของรูปร่างเพื่อลดต้นทุนฝึกใหม่ เกี่ยวข้องเมื่อทุก topology ต้องมีผู้ขับที่ปรับแล้วของตัวเอง
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'นำตัวควบคุมแบบ graph network กลับมาใช้ข้ามการกลายพันธุ์ของรูปร่างเพื่อลดต้นทุนฝึกใหม่ เกี่ยวข้องเมื่อทุก topology ต้องมีผู้ขับที่ปรับแล้วของตัวเอง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'นำตัวควบคุมแบบ graph network กลับมาใช้ข้ามการกลายพันธุ์ของรูปร่างเพื่อลดต้นทุนฝึกใหม่ เกี่ยวข้องเมื่อทุก topology ต้องมีผู้ขับที่ปรับแล้วของตัวเอง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล morphology ไวต่อ encoding, การจัดงบฝึก controller, task distribution และสมมติฐาน simulator มาก ความสำเร็จเสมือนไม่ถ่ายโอนไปรถแข่งโดยไม่มี physical correlation การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **นำตัวควบคุมแบบ graph network กลับมาใช้ข้ามการกลายพันธุ์ของรูปร่างเพื่อลดต้นทุนฝึกใหม่ เกี่ยวข้องเมื่อทุก topology ต้องมีผู้ขับที่ปรับแล้วของตัวเอง** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'นำตัวควบคุมแบบ graph network กลับมาใช้ข้ามการกลายพันธุ์ของรูปร่างเพื่อลดต้นทุนฝึกใหม่ เกี่ยวข้องเมื่อทุก topology ต้องมีผู้ขับที่ปรับแล้วของตัวเอง' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | รัน operator หรือกฎจัดสรรที่ได้จาก paper เทียบ evolution/QD และ fixed-topology control ที่ optimize แล้ว โดยจับคู่ seed, compute รวม, งบฝึก controller และสนาม held-out |
| หลักฐานผ่านและล้มเหลว | ยอมรับเมื่อ feasible archive coverage หรือผลงานสนาม held-out ดีขึ้นโดยไม่เพิ่มแบบ invalid, controller under-training หรือ evaluator disagreement มิฉะนั้นปฏิเสธการถ่ายโอน |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 17 หน้า, 53,909 ตัวอักษร, 9,300 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 17/17
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 6, 7, 8, 9 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, methods
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
