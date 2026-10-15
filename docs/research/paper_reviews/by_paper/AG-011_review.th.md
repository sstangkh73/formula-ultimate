# AG-011: Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback

English source: `AG-011_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Guijin Son, Jehyun Park, Seyeon Park, Sunghee Ahn, Youngjae Yu |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2605.17448 |
| ระเบียน canonical | [https://arxiv.org/abs/2605.17448](https://arxiv.org/abs/2605.17448) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-011_Son2026_self-improving-cad-generation-agents-with-finite-e.pdf) |
| SHA-256 ของต้นฉบับ | `b793a594ff8ad1bee86b1b37e964d4f572f2953e124bbbbd24650238bbc58eba` |
| coverage ของ full text | 33/33 หน้า (100.00%); สกัดได้ 14,144 คำ |

## คำถามวิจัย

agent หรือ generative method ใน Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction, results และคำเทคนิคที่พบบ่อย ได้แก่ pass, design, feedback, engineering, https, gpt-5, page, brief วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **ใช้ผล FEA เป็นสัญญาณป้อนกลับให้ agent ที่เขียน CAD เกี่ยวข้องโดยตรงกับ geometry-structural coupling (Works 082, 138)**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ใช้ผล FEA เป็นสัญญาณป้อนกลับให้ agent ที่เขียน CAD เกี่ยวข้องโดยตรงกับ geometry-structural coupling (Works 082, 138)
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'ใช้ผล FEA เป็นสัญญาณป้อนกลับให้ agent ที่เขียน CAD เกี่ยวข้องโดยตรงกับ geometry-structural coupling (Works 082, 138)' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'ใช้ผล FEA เป็นสัญญาณป้อนกลับให้ agent ที่เขียน CAD เกี่ยวข้องโดยตรงกับ geometry-structural coupling (Works 082, 138)' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **ใช้ผล FEA เป็นสัญญาณป้อนกลับให้ agent ที่เขียน CAD เกี่ยวข้องโดยตรงกับ geometry-structural coupling (Works 082, 138)** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'ใช้ผล FEA เป็นสัญญาณป้อนกลับให้ agent ที่เขียน CAD เกี่ยวข้องโดยตรงกับ geometry-structural coupling (Works 082, 138)' ใน target ที่ระบุด้านล่าง |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 33 หน้า, 88,556 ตัวอักษร, 14,144 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 33/33
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 6, 8, 9, 13, 14, 16, 23 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
