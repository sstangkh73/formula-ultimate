# SI-010: Dojo: A Differentiable Physics Engine for Robotics

English source: `SI-010_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Taylor A. Howell, Simon Le Cleac'h, Jan Brudigam, Qianzhong Chen, Jian-Kai Sun, J. Kolter, Mac Schwager, Zachary Manchester |
| ปี | 2022 |
| แหล่งตีพิมพ์ | arXiv |
| DOI | Not recorded |
| arXiv | 2203.00806 |
| ระเบียน canonical | [https://arxiv.org/abs/2203.00806](https://arxiv.org/abs/2203.00806) |
| หัวข้อในคลัง | โครงสร้างพื้นฐาน simulation และ differentiable physics |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/06_simulation_infrastructure/SI-010_Howell2022_dojo-a-differentiable-physics-engine-for-robotics.pdf) |
| SHA-256 ของต้นฉบับ | `729928039c101eba82d02ddfe215d7d19e592414bff32f690014be9f3e071bf7` |
| coverage ของ full text | 18/18 หน้า (100.00%); สกัดได้ 13,906 คำ |

## คำถามวิจัย

ความสามารถด้าน simulation, coupling, differentiation หรือ optimal control ใน Dojo: A Differentiable Physics Engine for Robotics แม่นและเสถียรพอสำหรับ evaluator ของ Formula Ultimate หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐาน simulation/เชิงตัวเลข, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ ไม่พบ heading ที่เชื่อถือได้ และคำเทคนิคที่พบบ่อย ได้แก่ dojo, contact, simulation, gradients, optimization, dynamics, robotics, solver วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **contact แบบ differentiable ด้วย interior-point complementarity เป็นทางเลือก gradient ผ่าน contact สำหรับ ground interaction**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** contact แบบ differentiable ด้วย interior-point complementarity เป็นทางเลือก gradient ผ่าน contact สำหรับ ground interaction
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'contact แบบ differentiable ด้วย interior-point complementarity เป็นทางเลือก gradient ผ่าน contact สำหรับ ground interaction' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อโครงสร้างพื้นฐาน simulation และ differentiable physics
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'contact แบบ differentiable ด้วย interior-point complementarity เป็นทางเลือก gradient ผ่าน contact สำหรับ ground interaction' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อโครงสร้างพื้นฐาน simulation และ differentiable physics โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ความเร็ว differentiability หรือ API ที่สะดวกไม่ยืนยัน model-form validity, conservation, contact correctness หรือ coupling stability การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **contact แบบ differentiable ด้วย interior-point complementarity เป็นทางเลือก gradient ผ่าน contact สำหรับ ground interaction** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **simulation coupling contract, evaluator applicability registry และ solver-failure ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | simulation coupling contract, evaluator applicability registry และ solver-failure ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'contact แบบ differentiable ด้วย interior-point complementarity เป็นทางเลือก gradient ผ่าน contact สำหรับ ground interaction' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | benchmark กับกรณี analytical และ independent solver ข้าม time step, mesh, ช่วง stiffness/contact และ hardware พร้อมวัด error, conservation, stability และ cost |
| หลักฐานผ่านและล้มเหลว | admit เฉพาะ candidate class ที่ error/stability อยู่ใน envelope ที่ลงทะเบียน และคง gradient/solver failure เป็นผลที่สังเกตได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 18 หน้า, 86,101 ตัวอักษร, 13,906 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 18/18
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 5, 6, 7, 9 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
