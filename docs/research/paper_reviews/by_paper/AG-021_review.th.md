# AG-021: Generating CAD Code with Vision-Language Models for 3D Designs

English source: `AG-021_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Kamel Alrashedy, Pradyumna Tambwekar, Z. Zaidi, Megan Langwasser, Wei Xu, Matthew C. Gombolay |
| ปี | 2024 |
| แหล่งตีพิมพ์ | International Conference on Learning Representations |
| DOI | Not recorded |
| arXiv | 2410.05340 |
| ระเบียน canonical | [https://arxiv.org/abs/2410.05340](https://arxiv.org/abs/2410.05340) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-021_Alrashedy2024_generating-cad-code-with-vision-language-models-fo.pdf) |
| SHA-256 ของต้นฉบับ | `f3e88746a0739c925efde8dbc80e20f947bb4a88bfdeab08f1e3a7cdbac6e056` |
| coverage ของ full text | 27/27 หน้า (100.00%); สกัดได้ 12,303 คำ |

## คำถามวิจัย

agent หรือ generative method ใน Generating CAD Code with Vision-Language Models for 3D Designs สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ code, object, generated, cadcodeverify, feedback, objects, geometric, generation วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **CADCodeVerify: แบบจำลองเรนเดอร์ผล CAD ของตัวเองแล้วตรวจเอง เป็นการตรวจเบื้องต้นราคาถูกก่อน geometry witness อิสระของเรา**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** CADCodeVerify: แบบจำลองเรนเดอร์ผล CAD ของตัวเองแล้วตรวจเอง เป็นการตรวจเบื้องต้นราคาถูกก่อน geometry witness อิสระของเรา
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'CADCodeVerify: แบบจำลองเรนเดอร์ผล CAD ของตัวเองแล้วตรวจเอง เป็นการตรวจเบื้องต้นราคาถูกก่อน geometry witness อิสระของเรา' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'CADCodeVerify: แบบจำลองเรนเดอร์ผล CAD ของตัวเองแล้วตรวจเอง เป็นการตรวจเบื้องต้นราคาถูกก่อน geometry witness อิสระของเรา' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **CADCodeVerify: แบบจำลองเรนเดอร์ผล CAD ของตัวเองแล้วตรวจเอง เป็นการตรวจเบื้องต้นราคาถูกก่อน geometry witness อิสระของเรา** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'CADCodeVerify: แบบจำลองเรนเดอร์ผล CAD ของตัวเองแล้วตรวจเอง เป็นการตรวจเบื้องต้นราคาถูกก่อน geometry witness อิสระของเรา' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 27 หน้า, 72,751 ตัวอักษร, 12,303 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 27/27
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 6, 8, 9, 10, 16 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
