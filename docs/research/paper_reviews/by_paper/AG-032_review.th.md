# AG-032: Constraining Generative Models for Engineering Design with Negative Data

English source: `AG-032_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Giorgio Giannone, Lyle Regenwetter, Akash Srivastava, D. Gutfreund, Faez Ahmed |
| ปี | 2023 |
| แหล่งตีพิมพ์ | Trans. Mach. Learn. Res. |
| DOI | Not recorded |
| arXiv | 2306.15166 |
| ระเบียน canonical | [https://arxiv.org/abs/2306.15166](https://arxiv.org/abs/2306.15166) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-032_Giannone2023_constraining-generative-models-for-engineering-des.pdf) |
| SHA-256 ของต้นฉบับ | `6f829566eba3823d227d5d333e92b85e6cb51c1dc6ee8e65d7103d8da6dcad4e` |
| coverage ของ full text | 38/38 หน้า (100.00%); สกัดได้ 16,417 คำ |

## คำถามวิจัย

agent หรือ generative method ใน Constraining Generative Models for Engineering Design with Negative Data สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐานคณิตศาสตร์/เชิงรูปนัย** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction, methods และคำเทคนิคที่พบบ่อย ได้แก่ models, data, generative, negative, design, model, engineering, gan-mdd วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **ฝึกด้วยตัวอย่างที่ไม่ผ่านเพื่อให้ตัวสร้างอยู่ในข้อจำกัด บันทึกการปฏิเสธของเราคือข้อมูลเชิงลบแบบนี้พอดี**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** ฝึกด้วยตัวอย่างที่ไม่ผ่านเพื่อให้ตัวสร้างอยู่ในข้อจำกัด บันทึกการปฏิเสธของเราคือข้อมูลเชิงลบแบบนี้พอดี
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'ฝึกด้วยตัวอย่างที่ไม่ผ่านเพื่อให้ตัวสร้างอยู่ในข้อจำกัด บันทึกการปฏิเสธของเราคือข้อมูลเชิงลบแบบนี้พอดี' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'ฝึกด้วยตัวอย่างที่ไม่ผ่านเพื่อให้ตัวสร้างอยู่ในข้อจำกัด บันทึกการปฏิเสธของเราคือข้อมูลเชิงลบแบบนี้พอดี' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อAI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **ฝึกด้วยตัวอย่างที่ไม่ผ่านเพื่อให้ตัวสร้างอยู่ในข้อจำกัด บันทึกการปฏิเสธของเราคือข้อมูลเชิงลบแบบนี้พอดี** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'ฝึกด้วยตัวอย่างที่ไม่ผ่านเพื่อให้ตัวสร้างอยู่ในข้อจำกัด บันทึกการปฏิเสธของเราคือข้อมูลเชิงลบแบบนี้พอดี' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 38 หน้า, 103,782 ตัวอักษร, 16,417 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 38/38
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 4, 5, 6, 8, 11, 12 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction, methods
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
