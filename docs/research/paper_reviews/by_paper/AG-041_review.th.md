# AG-041: Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents

English source: `AG-041_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Shuo Ren, Pu Jian, Zhen-Jiang Ren, Chun-Lin Leng, Can Xie, Jia-Jun Zhang |
| ปี | 2025 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2503.24047 |
| ระเบียน canonical | [https://arxiv.org/abs/2503.24047](https://arxiv.org/abs/2503.24047) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-041_Ren2025_towards-scientific-intelligence-a-survey-of-llm-ba.pdf) |
| SHA-256 ของต้นฉบับ | `0091c33932764e85c269746f813dd78582bc524f48d8a890ee1bbb1fea06865f` |
| coverage ของ full text | 68/68 หน้า (100.00%); สกัดได้ 42,626 คำ |

## คำถามวิจัย

agent หรือ generative method ใน Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, discussion, introduction, methods, results และคำเทคนิคที่พบบ่อย ได้แก่ scientific, agents, arxiv, reasoning, agent, research, zhang, knowledge วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **survey ของ LLM scientific agent เป็นบริบทสำหรับวางตำแหน่ง agent ค้นพบทางวิศวกรรม**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** survey ของ LLM scientific agent เป็นบริบทสำหรับวางตำแหน่ง agent ค้นพบทางวิศวกรรม
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'survey ของ LLM scientific agent เป็นบริบทสำหรับวางตำแหน่ง agent ค้นพบทางวิศวกรรม' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'survey ของ LLM scientific agent เป็นบริบทสำหรับวางตำแหน่ง agent ค้นพบทางวิศวกรรม' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **survey ของ LLM scientific agent เป็นบริบทสำหรับวางตำแหน่ง agent ค้นพบทางวิศวกรรม** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'survey ของ LLM scientific agent เป็นบริบทสำหรับวางตำแหน่ง agent ค้นพบทางวิศวกรรม' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 68 หน้า, 302,319 ตัวอักษร, 42,626 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 68/68
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 7, 9, 10, 11, 14, 17, 19, 23 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, discussion, introduction, methods, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
