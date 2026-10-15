# VV-017: COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting

English source: `VV-017_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Nikolaus Hansen, A. Auger, R. Ros, Olaf Mersmann, T. Tušar, D. Brockhoff |
| ปี | 2021 |
| แหล่งตีพิมพ์ | Optim. Methods Softw. |
| DOI | Not recorded |
| arXiv | 1603.08785 |
| ระเบียน canonical | [https://arxiv.org/abs/1603.08785](https://arxiv.org/abs/1603.08785) |
| หัวข้อในคลัง | verification, validation, uncertainty, สถิติ และ claim |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/13_validation_statistics_claims/VV-017_Hansen2021_coco-a-platform-for-comparing-continuous-optimizer.pdf) |
| SHA-256 ของต้นฉบับ | `c37521aa07b2cd5b6f1af8d05112e4b0d8a4e192fc6fc7064c6954e41c591eff` |
| coverage ของ full text | 29/29 หน้า (100.00%); สกัดได้ 15,418 คำ |

## คำถามวิจัย

งาน COCO: A Platform for Comparing Continuous Optimizers in a Black-Box Setting แก้ปัญหา verification, validation, uncertainty, สถิติ หรือ claim failure ใด และต้องใช้วินัยหลักฐานอะไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ coco, target, benchmarking, function, data, solver, functions, optimization วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **การเปรียบเทียบสมรรถนะ optimizer ตามงบแบบ anytime เป็นแบบการรายงานคุณภาพเทียบกับจำนวนการประเมิน**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** การเปรียบเทียบสมรรถนะ optimizer ตามงบแบบ anytime เป็นแบบการรายงานคุณภาพเทียบกับจำนวนการประเมิน
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'การเปรียบเทียบสมรรถนะ optimizer ตามงบแบบ anytime เป็นแบบการรายงานคุณภาพเทียบกับจำนวนการประเมิน' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'การเปรียบเทียบสมรรถนะ optimizer ตามงบแบบ anytime เป็นแบบการรายงานคุณภาพเทียบกับจำนวนการประเมิน' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

วิธีเหล่านี้เพิ่มวินัย claim แต่ไม่สร้างข้อมูลกายภาพหรือ model validity ที่ขาด ความถูกต้องทางสถิติช่วย evaluator ที่ใช้ผิดโดเมนไม่ได้ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **การเปรียบเทียบสมรรถนะ optimizer ตามงบแบบ anytime เป็นแบบการรายงานคุณภาพเทียบกับจำนวนการประเมิน** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'การเปรียบเทียบสมรรถนะ optimizer ตามงบแบบ anytime เป็นแบบการรายงานคุณภาพเทียบกับจำนวนการประเมิน' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้ check จาก paper กับ known-positive, negative control ที่หักล้างได้, seed/refinement ซ้ำ และการแยก calibration/holdout แล้ว audit wording ของ claim กับผล |
| หลักฐานผ่านและล้มเหลว | ต้องมี error/uncertainty bound ที่กำหนดล่วงหน้า, ปฏิเสธหลักฐาน invalid ถูก, inference คำนึง multiplicity, provenance deterministic และไม่มี retrospective repair |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 29 หน้า, 90,975 ตัวอักษร, 15,418 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 29/29
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 5, 6, 9, 11 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
