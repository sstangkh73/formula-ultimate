# AG-023: Towards High-Fidelity CAD Generation via LLM-Driven Program Generation and Text-Based B-Rep Primitive Grounding

English source: `AG-023_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Jiahao Li, Qingwang Zhang, Qiuyue Chen, Guozhan Qiu, Yunzhong Lou, Xiangdong Zhou |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2603.11831 |
| ระเบียน canonical | [https://arxiv.org/abs/2603.11831](https://arxiv.org/abs/2603.11831) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-023_Li2026_towards-high-fidelity-cad-generation-via-llm-drive.pdf) |
| SHA-256 ของต้นฉบับ | `07bcd526f6e1729b22caa70e6207a9c93db5b046f47ef4775a4ce30bd1288736` |
| coverage ของ full text | 13/13 หน้า (100.00%); สกัดได้ 9,152 คำ |

## คำถามวิจัย

agent หรือ generative method ใน Towards High-Fidelity CAD Generation via LLM-Driven Program Generation and Text-Based B-Rep Primitive Grounding สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, methods และคำเทคนิคที่พบบ่อย ได้แก่ b-rep, generation, models, primitive, primitives, dataset, geometric, model วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **FutureCAD: LLM เขียน CadQuery และผูกการอ้างอิงเข้ากับ primitive ของ B-rep แก้ปัญหาการเลือก face/edge ที่เปราะบางใน CAD ที่สร้างขึ้น**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** FutureCAD: LLM เขียน CadQuery และผูกการอ้างอิงเข้ากับ primitive ของ B-rep แก้ปัญหาการเลือก face/edge ที่เปราะบางใน CAD ที่สร้างขึ้น
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'FutureCAD: LLM เขียน CadQuery และผูกการอ้างอิงเข้ากับ primitive ของ B-rep แก้ปัญหาการเลือก face/edge ที่เปราะบางใน CAD ที่สร้างขึ้น' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'FutureCAD: LLM เขียน CadQuery และผูกการอ้างอิงเข้ากับ primitive ของ B-rep แก้ปัญหาการเลือก face/edge ที่เปราะบางใน CAD ที่สร้างขึ้น' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **FutureCAD: LLM เขียน CadQuery และผูกการอ้างอิงเข้ากับ primitive ของ B-rep แก้ปัญหาการเลือก face/edge ที่เปราะบางใน CAD ที่สร้างขึ้น** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'FutureCAD: LLM เขียน CadQuery และผูกการอ้างอิงเข้ากับ primitive ของ B-rep แก้ปัญหาการเลือก face/edge ที่เปราะบางใน CAD ที่สร้างขึ้น' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 13 หน้า, 58,971 ตัวอักษร, 9,152 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 13/13
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 6, 7, 8, 11, 13 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, methods
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
