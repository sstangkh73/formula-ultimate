# VV-002: Bayesian calibration of computer models

English source: `VV-002_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Marc C. Kennedy, Anthony O'Hagan |
| ปี | 2001 |
| แหล่งตีพิมพ์ | Journal of the Royal Statistical Society Series B: Statistical Methodology |
| DOI | 10.1111/1467-9868.00294 |
| arXiv | 2006.07546 |
| ระเบียน canonical | [https://doi.org/10.1111/1467-9868.00294](https://doi.org/10.1111/1467-9868.00294) |
| หัวข้อในคลัง | verification, validation, uncertainty, สถิติ และ claim |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/13_validation_statistics_claims/VV-002_Kennedy2001_bayesian-calibration-of-computer-models.pdf) |
| SHA-256 ของต้นฉบับ | `2db6986205016745464e5797462899313397dba6c7ab12c98a5f9841a471d873` |
| coverage ของ full text | 25/25 หน้า (100.00%); สกัดได้ 10,256 คำ |

## คำถามวิจัย

งาน Bayesian calibration of computer models แก้ปัญหา verification, validation, uncertainty, สถิติ หรือ claim failure ใด และต้องใช้วินัยหลักฐานอะไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, introduction และคำเทคนิคที่พบบ่อย ได้แก่ calibration, model, posterior, latent, data, parameters, runs, failures วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **การสอบเทียบของ Kennedy-O'Hagan ที่มีเทอมความคลาดเคลื่อนของแบบจำลองชัดเจน เป็นแผนการสอบเทียบระบบย่อยกับการวัด**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** การสอบเทียบของ Kennedy-O'Hagan ที่มีเทอมความคลาดเคลื่อนของแบบจำลองชัดเจน เป็นแผนการสอบเทียบระบบย่อยกับการวัด
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'การสอบเทียบของ Kennedy-O'Hagan ที่มีเทอมความคลาดเคลื่อนของแบบจำลองชัดเจน เป็นแผนการสอบเทียบระบบย่อยกับการวัด' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'การสอบเทียบของ Kennedy-O'Hagan ที่มีเทอมความคลาดเคลื่อนของแบบจำลองชัดเจน เป็นแผนการสอบเทียบระบบย่อยกับการวัด' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

วิธีเหล่านี้เพิ่มวินัย claim แต่ไม่สร้างข้อมูลกายภาพหรือ model validity ที่ขาด ความถูกต้องทางสถิติช่วย evaluator ที่ใช้ผิดโดเมนไม่ได้ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **การสอบเทียบของ Kennedy-O'Hagan ที่มีเทอมความคลาดเคลื่อนของแบบจำลองชัดเจน เป็นแผนการสอบเทียบระบบย่อยกับการวัด** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'การสอบเทียบของ Kennedy-O'Hagan ที่มีเทอมความคลาดเคลื่อนของแบบจำลองชัดเจน เป็นแผนการสอบเทียบระบบย่อยกับการวัด' ใน target ที่ระบุด้านล่าง |
| experiment และ control | ใช้ check จาก paper กับ known-positive, negative control ที่หักล้างได้, seed/refinement ซ้ำ และการแยก calibration/holdout แล้ว audit wording ของ claim กับผล |
| หลักฐานผ่านและล้มเหลว | ต้องมี error/uncertainty bound ที่กำหนดล่วงหน้า, ปฏิเสธหลักฐาน invalid ถูก, inference คำนึง multiplicity, provenance deterministic และไม่มี retrospective repair |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 25 หน้า, 63,307 ตัวอักษร, 10,256 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 25/25
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 5, 14, 16, 17, 19 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, introduction
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
