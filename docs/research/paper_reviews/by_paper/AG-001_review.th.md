# AG-001: Evolution through Large Models

English source: `AG-001_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | J. Lehman, Jonathan Gordon, Shawn Jain, Kamal Ndousse, Cathy Yeh, Kenneth O. Stanley |
| ปี | 2022 |
| แหล่งตีพิมพ์ | arXiv |
| DOI | Not recorded |
| arXiv | 2206.08896 |
| ระเบียน canonical | [https://arxiv.org/abs/2206.08896](https://arxiv.org/abs/2206.08896) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-001_Lehman2022_evolution-through-large-models.pdf) |
| SHA-256 ของต้นฉบับ | `16cbbfb8d37e593ce462b7083bff625c992072d98fb16d92965cfd55f8347f8b` |
| coverage ของ full text | 58/58 หน้า (100.00%); สกัดได้ 20,435 คำ |

## คำถามวิจัย

agent หรือ generative method ใน Evolution through Large Models สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา optimization/search, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction และคำเทคนิคที่พบบ่อย ได้แก่ model, models, seed, stage, code, page, performance, mutation วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **LLM เป็นตัวกลายพันธุ์ภายใน MAP-Elites สร้างรูปร่าง Sodarace ที่เคลื่อนที่ได้ในรูปโค้ด เป็นแม่แบบที่ใกล้ที่สุดของ LLM ที่กลายพันธุ์โปรแกรม CadQuery ของรถ**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** LLM เป็นตัวกลายพันธุ์ภายใน MAP-Elites สร้างรูปร่าง Sodarace ที่เคลื่อนที่ได้ในรูปโค้ด เป็นแม่แบบที่ใกล้ที่สุดของ LLM ที่กลายพันธุ์โปรแกรม CadQuery ของรถ
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'LLM เป็นตัวกลายพันธุ์ภายใน MAP-Elites สร้างรูปร่าง Sodarace ที่เคลื่อนที่ได้ในรูปโค้ด เป็นแม่แบบที่ใกล้ที่สุดของ LLM ที่กลายพันธุ์โปรแกรม CadQuery ของรถ' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'LLM เป็นตัวกลายพันธุ์ภายใน MAP-Elites สร้างรูปร่าง Sodarace ที่เคลื่อนที่ได้ในรูปโค้ด เป็นแม่แบบที่ใกล้ที่สุดของ LLM ที่กลายพันธุ์โปรแกรม CadQuery ของรถ' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **LLM เป็นตัวกลายพันธุ์ภายใน MAP-Elites สร้างรูปร่าง Sodarace ที่เคลื่อนที่ได้ในรูปโค้ด เป็นแม่แบบที่ใกล้ที่สุดของ LLM ที่กลายพันธุ์โปรแกรม CadQuery ของรถ** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'LLM เป็นตัวกลายพันธุ์ภายใน MAP-Elites สร้างรูปร่าง Sodarace ที่เคลื่อนที่ได้ในรูปโค้ด เป็นแม่แบบที่ใกล้ที่สุดของ LLM ที่กลายพันธุ์โปรแกรม CadQuery ของรถ' ใน target ที่ระบุด้านล่าง |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 58 หน้า, 124,175 ตัวอักษร, 20,435 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 58/58
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 7, 12, 14, 18, 20, 21, 23, 24 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
