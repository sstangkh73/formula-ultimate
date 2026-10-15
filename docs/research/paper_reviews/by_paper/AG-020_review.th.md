# AG-020: CAD-Recode: Reverse Engineering CAD Code from Point Clouds

English source: `AG-020_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | D. Rukhovich, Elona Dupont, Dimitrios Mallis, K. Cherenkova, Anis Kacem, Djamila Aouada |
| ปี | 2024 |
| แหล่งตีพิมพ์ | IEEE International Conference on Computer Vision |
| DOI | Not recorded |
| arXiv | 2412.14042 |
| ระเบียน canonical | [https://arxiv.org/abs/2412.14042](https://arxiv.org/abs/2412.14042) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-020_Rukhovich2024_cad-recode-reverse-engineering-cad-code-from-point.pdf) |
| SHA-256 ของต้นฉบับ | `979e38357c87401dcd71a3b4bca5e57d0ae14eeb9404a93234527d09bcfc0727` |
| coverage ของ full text | 22/22 หน้า (100.00%); สกัดได้ 14,547 คำ |

## คำถามวิจัย

agent หรือ generative method ใน CAD-Recode: Reverse Engineering CAD Code from Point Clouds สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ segment, code, point, model, cad-recode, dataset, cloud, cadquery วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **กู้โปรแกรม CadQuery จาก point cloud พร้อมคลัง CadQuery สังเคราะห์ขนาดใหญ่ เป็นข้อมูลที่ใช้ได้และเป็นการตรวจจากเรขาคณิตกลับเป็นโค้ด**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** กู้โปรแกรม CadQuery จาก point cloud พร้อมคลัง CadQuery สังเคราะห์ขนาดใหญ่ เป็นข้อมูลที่ใช้ได้และเป็นการตรวจจากเรขาคณิตกลับเป็นโค้ด
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'กู้โปรแกรม CadQuery จาก point cloud พร้อมคลัง CadQuery สังเคราะห์ขนาดใหญ่ เป็นข้อมูลที่ใช้ได้และเป็นการตรวจจากเรขาคณิตกลับเป็นโค้ด' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'กู้โปรแกรม CadQuery จาก point cloud พร้อมคลัง CadQuery สังเคราะห์ขนาดใหญ่ เป็นข้อมูลที่ใช้ได้และเป็นการตรวจจากเรขาคณิตกลับเป็นโค้ด' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **กู้โปรแกรม CadQuery จาก point cloud พร้อมคลัง CadQuery สังเคราะห์ขนาดใหญ่ เป็นข้อมูลที่ใช้ได้และเป็นการตรวจจากเรขาคณิตกลับเป็นโค้ด** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'กู้โปรแกรม CadQuery จาก point cloud พร้อมคลัง CadQuery สังเคราะห์ขนาดใหญ่ เป็นข้อมูลที่ใช้ได้และเป็นการตรวจจากเรขาคณิตกลับเป็นโค้ด' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 22 หน้า, 89,150 ตัวอักษร, 14,547 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 22/22
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 4, 6, 7, 10, 11 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
