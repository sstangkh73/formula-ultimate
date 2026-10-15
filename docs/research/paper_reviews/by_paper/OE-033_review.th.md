# OE-033: Shape Your Body: Value Gradients for Multi-Embodiment Robot Design

English source: `OE-033_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Nico Bohlinger, Jan Peters |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2606.00702 |
| ระเบียน canonical | [https://arxiv.org/abs/2606.00702](https://arxiv.org/abs/2606.00702) |
| หัวข้อในคลัง | การออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/01_open_ended_codesign/OE-033_Bohlinger2026_shape-your-body-value-gradients-for-multi-embodime.pdf) |
| SHA-256 ของต้นฉบับ | `00e8f5b45b88da847c66c97bd2a506b39c7cc697b74a77fb9dbab3d8f3cb3cb1` |
| coverage ของ full text | 27/27 หน้า (100.00%); สกัดได้ 11,760 คำ |

## คำถามวิจัย

งาน Shape Your Body: Value Gradients for Multi-Embodiment Robot Design ค้นหา รักษา หรือประเมิน morphology ร่วมกับ control อย่างไร และทำให้เกิด bias แบบใด?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, การศึกษา optimization/search, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ conclusion, introduction, limitations, results และคำเทคนิคที่พบบ่อย ได้แก่ design, robot, value, policy, learning, training, critic, designs วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **ใช้ gradient ของ value จาก policy หลายร่างเพื่อปรับการออกแบบร่างกาย เป็นตัวเทียบฝั่งการออกแบบต่อเนื่อง**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ใช้ gradient ของ value จาก policy หลายร่างเพื่อปรับการออกแบบร่างกาย เป็นตัวเทียบฝั่งการออกแบบต่อเนื่อง
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'ใช้ gradient ของ value จาก policy หลายร่างเพื่อปรับการออกแบบร่างกาย เป็นตัวเทียบฝั่งการออกแบบต่อเนื่อง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'ใช้ gradient ของ value จาก policy หลายร่างเพื่อปรับการออกแบบร่างกาย เป็นตัวเทียบฝั่งการออกแบบต่อเนื่อง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อการออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผล morphology ไวต่อ encoding, การจัดงบฝึก controller, task distribution และสมมติฐาน simulator มาก ความสำเร็จเสมือนไม่ถ่ายโอนไปรถแข่งโดยไม่มี physical correlation การตรวจ heading แบบอัตโนมัติ **พบ** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **ใช้ gradient ของ value จาก policy หลายร่างเพื่อปรับการออกแบบร่างกาย เป็นตัวเทียบฝั่งการออกแบบต่อเนื่อง** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'ใช้ gradient ของ value จาก policy หลายร่างเพื่อปรับการออกแบบร่างกาย เป็นตัวเทียบฝั่งการออกแบบต่อเนื่อง' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | รัน operator หรือกฎจัดสรรที่ได้จาก paper เทียบ evolution/QD และ fixed-topology control ที่ optimize แล้ว โดยจับคู่ seed, compute รวม, งบฝึก controller และสนาม held-out |
| หลักฐานผ่านและล้มเหลว | ยอมรับเมื่อ feasible archive coverage หรือผลงานสนาม held-out ดีขึ้นโดยไม่เพิ่มแบบ invalid, controller under-training หรือ evaluator disagreement มิฉะนั้นปฏิเสธการถ่ายโอน |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 27 หน้า, 71,539 ตัวอักษร, 11,760 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 27/27
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 6, 7, 8, 19, 22 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: conclusion, introduction, limitations, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
