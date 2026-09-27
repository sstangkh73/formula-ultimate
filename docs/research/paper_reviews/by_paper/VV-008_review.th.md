# VV-008: Verification, validation, and predictive capability in computational engineering and physics

English source: `VV-008_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | William L Oberkampf, Timothy G Trucano, Charles Hirsch |
| ปี | 2004 |
| แหล่งตีพิมพ์ | Applied Mechanics Reviews |
| DOI | 10.1115/1.1767847 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.1115/1.1767847](https://doi.org/10.1115/1.1767847) |
| หัวข้อในคลัง | verification, validation, uncertainty, สถิติ และ claim |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/13_validation_statistics_claims/VV-008_Oberkampf2004_verification-validation-and-predictive-capability.pdf) |
| SHA-256 ของต้นฉบับ | `74df43945adc818c7718587e71058b31124b7d8255ee9b3e7f21e6bfaeaeca25` |
| coverage ของ full text | 92/92 หน้า (100.00%); สกัดได้ 42,720 คำ |

## คำถามวิจัย

ควรสร้างความเชื่อมั่นในการทำนายเชิงคำนวณอย่างไรโดยแยก code/solution verification ออกจาก validation กับการทดลอง?

## วิธีและหลักฐาน

บทความมุมมองวิศวกรรม 92 หน้าสังเคราะห์ V&V: PIRT, code/calculation verification, grid convergence, validation hierarchy, experimental uncertainty, quantitative comparison และ inference จาก validation domain ไป prediction (หน้า 14, 21, 34, 48)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** verification ประเมินความแม่นในการแก้ computational model ส่วน validation ประเมินความตรงกับโลกทดลองสำหรับ intended use ต้องแยก numerical error, experimental uncertainty และ model discrepancy และการทำนายนอก validation database ใช้ inference ที่อ่อนกว่า (หน้า 3-4, 14, 21)
- **การตีความของผู้ทบทวน:** code อาจ verify แล้วแต่ model ใช้ไม่ได้กับ application และการตรงการทดลองหนึ่ง tier ไม่ได้ validate การทำนายระบบเต็มโดยอัตโนมัติ
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** code อาจ verify แล้วแต่ model ใช้ไม่ได้กับ application และการตรงการทดลองหนึ่ง tier ไม่ได้ validate การทำนายระบบเต็มโดยอัตโนมัติ โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

เป็น framework/มุมมอง ไม่ใช่หลักฐาน validation ของ solver Formula Ultimate ต้องแปลงเป็น threshold, experiment และ intended-use domain เฉพาะ evaluator ฟิสิกส์แต่ละตัว การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **code อาจ verify แล้วแต่ model ใช้ไม่ได้กับ application และการตรงการทดลองหนึ่ง tier ไม่ได้ validate การทำนายระบบเต็มโดยอัตโนมัติ** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate |
| การเปลี่ยนแปลงที่เสนอ | เพิ่ม block intended-use/V&V ใน evaluator identity ทุกตัว: governing model, code-verification case, refinement evidence, validation tier/data, discrepancy/uncertainty, applicability domain และภาษาที่ห้าม claim |
| experiment และ control | ใช้ check จาก paper กับ known-positive, negative control ที่หักล้างได้, seed/refinement ซ้ำ และการแยก calibration/holdout แล้ว audit wording ของ claim กับผล |
| หลักฐานผ่านและล้มเหลว | ต้องมี error/uncertainty bound ที่กำหนดล่วงหน้า, ปฏิเสธหลักฐาน invalid ถูก, inference คำนึง multiplicity, provenance deterministic และไม่มี retrospective repair |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 92 หน้า, 280,341 ตัวอักษร, 42,720 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 92/92
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 12, 14, 17, 21, 26, 29, 34, 35 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
