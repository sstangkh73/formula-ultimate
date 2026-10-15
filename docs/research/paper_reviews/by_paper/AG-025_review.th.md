# AG-025: Test-Time Scaling for CAD Generation via Verifier-Free Consensus Selection

English source: `AG-025_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Aaron Haag, Altay Kacan, Bertram Fuchs, Oliver Lohse |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv |
| DOI | Not recorded |
| arXiv | 2608.09706 |
| ระเบียน canonical | [https://arxiv.org/abs/2608.09706](https://arxiv.org/abs/2608.09706) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-025_Haag2026_test-time-scaling-for-cad-generation-via-verifier.pdf) |
| SHA-256 ของต้นฉบับ | `b5e96f2859f7493f7d390423fd27d7bcb517915239b240ab046fc77f26c04ccd` |
| coverage ของ full text | 10/10 หน้า (100.00%); สกัดได้ 5,706 คำ |

## คำถามวิจัย

agent หรือ generative method ใน Test-Time Scaling for CAD Generation via Verifier-Free Consensus Selection สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction, methods, results และคำเทคนิคที่พบบ่อย ได้แก่ consensus, selection, arxiv, candidate, models, candidates, generation, model วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **เลือกโปรแกรม CAD จากหลายตัวอย่างด้วยฉันทามติ เป็นตัวกรองราคาถูก แต่ฉันทามติไม่ใช่การตรวจทางฟิสิกส์**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** เลือกโปรแกรม CAD จากหลายตัวอย่างด้วยฉันทามติ เป็นตัวกรองราคาถูก แต่ฉันทามติไม่ใช่การตรวจทางฟิสิกส์
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'เลือกโปรแกรม CAD จากหลายตัวอย่างด้วยฉันทามติ เป็นตัวกรองราคาถูก แต่ฉันทามติไม่ใช่การตรวจทางฟิสิกส์' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'เลือกโปรแกรม CAD จากหลายตัวอย่างด้วยฉันทามติ เป็นตัวกรองราคาถูก แต่ฉันทามติไม่ใช่การตรวจทางฟิสิกส์' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **เลือกโปรแกรม CAD จากหลายตัวอย่างด้วยฉันทามติ เป็นตัวกรองราคาถูก แต่ฉันทามติไม่ใช่การตรวจทางฟิสิกส์** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'เลือกโปรแกรม CAD จากหลายตัวอย่างด้วยฉันทามติ เป็นตัวกรองราคาถูก แต่ฉันทามติไม่ใช่การตรวจทางฟิสิกส์' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 10 หน้า, 36,243 ตัวอักษร, 5,706 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 10/10
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 4, 5, 6, 7 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction, methods, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
