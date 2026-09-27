# VV-024: Leakage and the reproducibility crisis in machine-learning-based science

English source: `VV-024_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Sayash Kapoor, Arvind Narayanan |
| ปี | 2023 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2207.07048 |
| ระเบียน canonical | [https://arxiv.org/abs/2207.07048](https://arxiv.org/abs/2207.07048) |
| หัวข้อในคลัง | verification, validation, uncertainty, สถิติ และ claim |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/13_validation_statistics_claims/VV-024_Kapoor2023_leakage-and-the-reproducibility-crisis-in-machine.pdf) |
| SHA-256 ของต้นฉบับ | `c433bceda841ca09fe2fd7ddf857fc0818fdf98553e62e54a37cc394c6f70c42` |
| coverage ของ full text | 29/29 หน้า (100.00%); สกัดได้ 21,107 คำ |

## คำถามวิจัย

งาน Leakage and the reproducibility crisis in machine-learning-based science แก้ปัญหา verification, validation, uncertainty, สถิติ หรือ claim failure ใด และต้องใช้วินัยหลักฐานอะไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, ชุดข้อมูล/benchmark, หลักฐาน simulation/เชิงตัวเลข, การศึกษา control/learning** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ data, model, leakage, test, performance, models, science, reproducibility วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

วิธีเหล่านี้เพิ่มวินัย claim แต่ไม่สร้างข้อมูลกายภาพหรือ model validity ที่ขาด ความถูกต้องทางสถิติช่วย evaluator ที่ใช้ผิดโดเมนไม่ได้ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'อนุกรมวิธานของ data leakage ที่ทำให้ผลดูดีเกินจริง ใช้กับสนาม held-out และข้อมูลฝึก surrogate' ใน target ที่ระบุด้านล่าง |
| experiment และ control | ใช้ check จาก paper กับ known-positive, negative control ที่หักล้างได้, seed/refinement ซ้ำ และการแยก calibration/holdout แล้ว audit wording ของ claim กับผล |
| หลักฐานผ่านและล้มเหลว | ต้องมี error/uncertainty bound ที่กำหนดล่วงหน้า, ปฏิเสธหลักฐาน invalid ถูก, inference คำนึง multiplicity, provenance deterministic และไม่มี retrospective repair |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 29 หน้า, 129,981 ตัวอักษร, 21,107 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 29/29
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 5, 6, 8, 9, 12, 20, 22, 24 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
