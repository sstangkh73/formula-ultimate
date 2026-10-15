# SI-021: Co-simulation: State of the art

English source: `SI-021_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | C. Gomes, Casper Thule, David Broman, P. Larsen, H. Vangheluwe |
| ปี | 2018 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 1702.00686 |
| ระเบียน canonical | [https://arxiv.org/abs/1702.00686](https://arxiv.org/abs/1702.00686) |
| หัวข้อในคลัง | โครงสร้างพื้นฐาน simulation และ differentiable physics |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/06_simulation_infrastructure/SI-021_Gomes2018_co-simulation-state-of-the-art.pdf) |
| SHA-256 ของต้นฉบับ | `5ce85c761a65389ca10448f701514e0a5f8596e0c14815972d4ad7b0316be438` |
| coverage ของ full text | 157/157 หน้า (100.00%); สกัดได้ 47,789 คำ |

## คำถามวิจัย

ความสามารถด้าน simulation, coupling, differentiation หรือ optimal control ใน Co-simulation: State of the art แม่นและเสถียรพอสำหรับ evaluator ของ Formula Ultimate หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, หลักฐาน simulation/เชิงตัวเลข, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, discussion, introduction, methods, results และคำเทคนิคที่พบบ่อย ได้แก่ co-simulation, simulation, time, model, unit, step, system, systems วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **survey การจัดการ ความเสถียร และความแม่นยำของ co-simulation เป็นพื้นหลังของการเชื่อมแบบจำลองระบบย่อยจำนวนมาก**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** survey การจัดการ ความเสถียร และความแม่นยำของ co-simulation เป็นพื้นหลังของการเชื่อมแบบจำลองระบบย่อยจำนวนมาก
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'survey การจัดการ ความเสถียร และความแม่นยำของ co-simulation เป็นพื้นหลังของการเชื่อมแบบจำลองระบบย่อยจำนวนมาก' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อโครงสร้างพื้นฐาน simulation และ differentiable physics
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'survey การจัดการ ความเสถียร และความแม่นยำของ co-simulation เป็นพื้นหลังของการเชื่อมแบบจำลองระบบย่อยจำนวนมาก' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อโครงสร้างพื้นฐาน simulation และ differentiable physics โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ความเร็ว differentiability หรือ API ที่สะดวกไม่ยืนยัน model-form validity, conservation, contact correctness หรือ coupling stability การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **survey การจัดการ ความเสถียร และความแม่นยำของ co-simulation เป็นพื้นหลังของการเชื่อมแบบจำลองระบบย่อยจำนวนมาก** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **simulation coupling contract, evaluator applicability registry และ solver-failure ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | simulation coupling contract, evaluator applicability registry และ solver-failure ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'survey การจัดการ ความเสถียร และความแม่นยำของ co-simulation เป็นพื้นหลังของการเชื่อมแบบจำลองระบบย่อยจำนวนมาก' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | benchmark กับกรณี analytical และ independent solver ข้าม time step, mesh, ช่วง stiffness/contact และ hardware พร้อมวัด error, conservation, stability และ cost |
| หลักฐานผ่านและล้มเหลว | admit เฉพาะ candidate class ที่ error/stability อยู่ใน envelope ที่ลงทะเบียน และคง gradient/solver failure เป็นผลที่สังเกตได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 157 หน้า, 303,080 ตัวอักษร, 47,789 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 157/157
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 28, 30, 33, 34, 36, 45, 55, 84 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, discussion, introduction, methods, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
