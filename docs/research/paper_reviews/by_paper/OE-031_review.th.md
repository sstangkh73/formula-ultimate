# OE-031: Embodied Co-Design for Rapidly Evolving Agents

English source: `OE-031_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Yuxing Wang, Zhiyu Chen, Tian-Tian Zhang, Qi-Yue Yin, Yongzhe Chang, Zhiheng Li, Liang Wang, Xueqian Wang |
| ปี | 2025 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2512.04770 |
| ระเบียน canonical | [https://arxiv.org/abs/2512.04770](https://arxiv.org/abs/2512.04770) |
| หัวข้อในคลัง | การออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/01_open_ended_codesign/OE-031_Wang2025_embodied-co-design-for-rapidly-evolving-agents.pdf) |
| SHA-256 ของต้นฉบับ | `1e8500347aa68157bee55fa83d1db4307d0674c6cea2a03648ad717a1da1e961` |
| coverage ของ full text | 29/29 หน้า (100.00%); สกัดได้ 29,429 คำ |

## คำถามวิจัย

งาน Embodied Co-Design for Rapidly Evolving Agents ค้นหา รักษา หรือประเมิน morphology ร่วมกับ control อย่างไร และทำให้เกิด bias แบบใด?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, การศึกษา optimization/search, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ methods และคำเทคนิคที่พบบ่อย ได้แก่ robot, task, conf, learning, inproc, design, control, simulation วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **survey ล่าสุดของการออกแบบรูปร่างร่วมกับการควบคุม ตั้งแต่สิ่งมีชีวิตเสมือนถึงหุ่นยนต์จริง เป็นแผนที่วิธีและปัญหาที่ยังเปิดอยู่**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** survey ล่าสุดของการออกแบบรูปร่างร่วมกับการควบคุม ตั้งแต่สิ่งมีชีวิตเสมือนถึงหุ่นยนต์จริง เป็นแผนที่วิธีและปัญหาที่ยังเปิดอยู่
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'survey ล่าสุดของการออกแบบรูปร่างร่วมกับการควบคุม ตั้งแต่สิ่งมีชีวิตเสมือนถึงหุ่นยนต์จริง เป็นแผนที่วิธีและปัญหาที่ยังเปิดอยู่' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'survey ล่าสุดของการออกแบบรูปร่างร่วมกับการควบคุม ตั้งแต่สิ่งมีชีวิตเสมือนถึงหุ่นยนต์จริง เป็นแผนที่วิธีและปัญหาที่ยังเปิดอยู่' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล morphology ไวต่อ encoding, การจัดงบฝึก controller, task distribution และสมมติฐาน simulator มาก ความสำเร็จเสมือนไม่ถ่ายโอนไปรถแข่งโดยไม่มี physical correlation การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **survey ล่าสุดของการออกแบบรูปร่างร่วมกับการควบคุม ตั้งแต่สิ่งมีชีวิตเสมือนถึงหุ่นยนต์จริง เป็นแผนที่วิธีและปัญหาที่ยังเปิดอยู่** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'survey ล่าสุดของการออกแบบรูปร่างร่วมกับการควบคุม ตั้งแต่สิ่งมีชีวิตเสมือนถึงหุ่นยนต์จริง เป็นแผนที่วิธีและปัญหาที่ยังเปิดอยู่' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | รัน operator หรือกฎจัดสรรที่ได้จาก paper เทียบ evolution/QD และ fixed-topology control ที่ optimize แล้ว โดยจับคู่ seed, compute รวม, งบฝึก controller และสนาม held-out |
| หลักฐานผ่านและล้มเหลว | ยอมรับเมื่อ feasible archive coverage หรือผลงานสนาม held-out ดีขึ้นโดยไม่เพิ่มแบบ invalid, controller under-training หรือ evaluator disagreement มิฉะนั้นปฏิเสธการถ่ายโอน |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 29 หน้า, 198,453 ตัวอักษร, 29,429 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 29/29
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 5, 6, 9, 11, 12 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: methods
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
