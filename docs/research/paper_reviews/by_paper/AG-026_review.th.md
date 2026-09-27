# AG-026: CADEngBench: It Looks Like CAD, but Does It Work? Evaluating Parametric Design, Assembly Reasoning, and Physics Simulation

English source: `AG-026_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Harmanjot Singh, Abhra Dubey, Jorge Alejandro Amador Herrera |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv |
| DOI | Not recorded |
| arXiv | 2608.09296 |
| ระเบียน canonical | [https://arxiv.org/abs/2608.09296](https://arxiv.org/abs/2608.09296) |
| หัวข้อในคลัง | AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์ |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/02_ai_agents_engineering/AG-026_Singh2026_cadengbench-it-looks-like-cad-but-does-it-work-eva.pdf) |
| SHA-256 ของต้นฉบับ | `8856c68ecf3f1cbc1aae0ac4e7b3ba9fc453925e959e009a89a65128ddcff30f` |
| coverage ของ full text | 27/27 หน้า (100.00%); สกัดได้ 13,971 คำ |

## คำถามวิจัย

โมเดลที่สร้างข้อความ/โค้ดผลิต CAD ที่ยัง valid ภายใต้ parameter edit, engineering check, matched FEA และการรัน assembly joint ได้หรือไม่?

## วิธีและหลักฐาน

CADEngBench-P ใช้ชิ้นส่วน parametric 300 ชิ้นในโจทย์ zero-to-CAD และ functional edit รวม 600 งาน ส่วน CADEngBench-A ใช้ body pair 150 คู่ตรวจ joint retrieval, entity grounding, frame prediction และ kinematic verification โดยเทียบโมเดล multimodal ที่เขียนโค้ดได้ 8 ตัว (หน้า 1)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** การแก้ CAD ที่ให้มาง่ายกว่าการสร้างใหม่มาก แต่ complex edit และ matched linear-static FEA ยังยาก โมเดล assembly มักหาบริเวณถูกแต่หา joint/mating entity ที่บันทึกไว้ไม่ถูก และไม่มีโมเดลใดนำทุกขั้นประเมิน (หน้า 1, 5, 22-23)
- **การตีความของผู้ทบทวน:** โปรแกรมที่สร้างอาจรันได้และตรงรูป nominal หนึ่งจุด แต่ encode ความสัมพันธ์พารามิเตอร์ผิด ทำให้ตระกูล structural response เบี่ยงออก (หน้า 5)
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** โปรแกรมที่สร้างอาจรันได้และตรงรูป nominal หนึ่งจุด แต่ encode ความสัมพันธ์พารามิเตอร์ผิด ทำให้ตระกูล structural response เบี่ยงออก (หน้า 5) โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

benchmark ใช้กฎ DFM ที่ประกาศ, CalculiX linear-static FEA และ assembly relation ที่บันทึกไว้ ยังไม่ครอบคลุม nonlinear material/contact, fatigue, tolerance stack หรือหน้าที่รถเต็มคัน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **โปรแกรมที่สร้างอาจรันได้และตรงรูป nominal หนึ่งจุด แต่ encode ความสัมพันธ์พารามิเตอร์ผิด ทำให้ตระกูล structural response เบี่ยงออก (หน้า 5)** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger |
| การเปลี่ยนแปลงที่เสนอ | เพิ่ม hidden test สำหรับ parametric family, matched FEA, exact mate และ motion probe ใน agent verifier และนับ end-to-end fail เมื่อขั้น geometry หรือ joint grounding ก่อนหน้าล้มเหลว |
| experiment และ control | ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 27 หน้า, 97,218 ตัวอักษร, 13,971 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 27/27
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 5, 7, 12, 16 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
