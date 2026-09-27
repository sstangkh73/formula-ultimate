# SI-017: CasADi: a software framework for nonlinear optimization and optimal control

English source: `SI-017_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Joel A. E. Andersson, Joris Gillis, Greg Horn, James B. Rawlings, Moritz Diehl |
| ปี | 2019 |
| แหล่งตีพิมพ์ | Mathematical Programming Computation |
| DOI | 10.1007/s12532-018-0139-4 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.1007/s12532-018-0139-4](https://doi.org/10.1007/s12532-018-0139-4) |
| หัวข้อในคลัง | โครงสร้างพื้นฐาน simulation และ differentiable physics |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/06_simulation_infrastructure/SI-017_Andersson2019_casadi-a-software-framework-for-nonlinear-optimiza.pdf) |
| SHA-256 ของต้นฉบับ | `55106413bd7b129b173b32fac5007de604031a3296df731cd9a37bfc4c214239` |
| coverage ของ full text | 33/33 หน้า (100.00%); สกัดได้ 16,702 คำ |

## คำถามวิจัย

ความสามารถด้าน simulation, coupling, differentiation หรือ optimal control ใน CasADi: a software framework for nonlinear optimization and optimal control แม่นและเสถียรพอสำหรับ evaluator ของ Formula Ultimate หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ introduction และคำเทคนิคที่พบบ่อย ได้แก่ control, casadi, optimization, function, nonlinear, optimal, problems, page วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **เครื่องมือเปิดมาตรฐานสำหรับปัญหาเวลาต่อรอบต่ำสุดแบบ direct collocation จำเป็นสำหรับ baseline ผู้ขับที่ optimize แล้ว**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** เครื่องมือเปิดมาตรฐานสำหรับปัญหาเวลาต่อรอบต่ำสุดแบบ direct collocation จำเป็นสำหรับ baseline ผู้ขับที่ optimize แล้ว
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'เครื่องมือเปิดมาตรฐานสำหรับปัญหาเวลาต่อรอบต่ำสุดแบบ direct collocation จำเป็นสำหรับ baseline ผู้ขับที่ optimize แล้ว' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อโครงสร้างพื้นฐาน simulation และ differentiable physics
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'เครื่องมือเปิดมาตรฐานสำหรับปัญหาเวลาต่อรอบต่ำสุดแบบ direct collocation จำเป็นสำหรับ baseline ผู้ขับที่ optimize แล้ว' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อโครงสร้างพื้นฐาน simulation และ differentiable physics โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ความเร็ว differentiability หรือ API ที่สะดวกไม่ยืนยัน model-form validity, conservation, contact correctness หรือ coupling stability การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **เครื่องมือเปิดมาตรฐานสำหรับปัญหาเวลาต่อรอบต่ำสุดแบบ direct collocation จำเป็นสำหรับ baseline ผู้ขับที่ optimize แล้ว** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **simulation coupling contract, evaluator applicability registry และ solver-failure ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | simulation coupling contract, evaluator applicability registry และ solver-failure ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'เครื่องมือเปิดมาตรฐานสำหรับปัญหาเวลาต่อรอบต่ำสุดแบบ direct collocation จำเป็นสำหรับ baseline ผู้ขับที่ optimize แล้ว' ใน target ที่ระบุด้านล่าง |
| experiment และ control | benchmark กับกรณี analytical และ independent solver ข้าม time step, mesh, ช่วง stiffness/contact และ hardware พร้อมวัด error, conservation, stability และ cost |
| หลักฐานผ่านและล้มเหลว | admit เฉพาะ candidate class ที่ error/stability อยู่ใน envelope ที่ลงทะเบียน และคง gradient/solver failure เป็นผลที่สังเกตได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 33 หน้า, 94,129 ตัวอักษร, 16,702 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 33/33
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 10, 13, 16, 18, 20, 22 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
