# AG-019: Text-to-CadQuery: A New Paradigm for CAD Generation with Scalable Large Model Capabilities

English source: `AG-019_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Haoyang Xie, Feng Ju |
| ปี | 2025 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2505.06507 |
| ระเบียน canonical | [https://arxiv.org/abs/2505.06507](https://arxiv.org/abs/2505.06507) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-019_Xie2025_text-to-cadquery-a-new-paradigm-for-cad-generation.pdf) |
| SHA-256 ของต้นฉบับ | `b78f5a28edb4fc9468c0605bd90863b59094d4598d6a1daad273151b62639acc` |
| coverage ของ full text | 18/18 หน้า (100.00%); สกัดได้ 9,072 คำ |

## คำถามวิจัย

agent หรือ generative method ใน Text-to-CadQuery: A New Paradigm for CAD Generation with Scalable Large Model Capabilities สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction, limitations, methods และคำเทคนิคที่พบบ่อย ได้แก่ models, cadquery, model, arxiv, language, command, code, point วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **ฝึก LLM ให้เขียน CadQuery โดยตรง เป็นภาษา CAD เดียวกับที่ agent ของเราเขียน มีชุดข้อมูลและสถิติข้อผิดพลาดที่นำมาใช้ได้**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ฝึก LLM ให้เขียน CadQuery โดยตรง เป็นภาษา CAD เดียวกับที่ agent ของเราเขียน มีชุดข้อมูลและสถิติข้อผิดพลาดที่นำมาใช้ได้
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'ฝึก LLM ให้เขียน CadQuery โดยตรง เป็นภาษา CAD เดียวกับที่ agent ของเราเขียน มีชุดข้อมูลและสถิติข้อผิดพลาดที่นำมาใช้ได้' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'ฝึก LLM ให้เขียน CadQuery โดยตรง เป็นภาษา CAD เดียวกับที่ agent ของเราเขียน มีชุดข้อมูลและสถิติข้อผิดพลาดที่นำมาใช้ได้' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **พบ** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **ฝึก LLM ให้เขียน CadQuery โดยตรง เป็นภาษา CAD เดียวกับที่ agent ของเราเขียน มีชุดข้อมูลและสถิติข้อผิดพลาดที่นำมาใช้ได้** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'ฝึก LLM ให้เขียน CadQuery โดยตรง เป็นภาษา CAD เดียวกับที่ agent ของเราเขียน มีชุดข้อมูลและสถิติข้อผิดพลาดที่นำมาใช้ได้' ใน target ที่ระบุด้านล่าง |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 18 หน้า, 56,342 ตัวอักษร, 9,072 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 18/18
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 4, 5, 6, 7, 9, 17 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction, limitations, methods
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
