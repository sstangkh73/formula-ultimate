# VV-032: SALib: An open-source Python library for Sensitivity Analysis

English source: `VV-032_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Jon Herman, Will Usher |
| ปี | 2017 |
| แหล่งตีพิมพ์ | The Journal of Open Source Software |
| DOI | 10.21105/joss.00097 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.21105/joss.00097](https://doi.org/10.21105/joss.00097) |
| หัวข้อในคลัง | verification, validation, uncertainty, สถิติ และ claim |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/13_validation_statistics_claims/VV-032_Herman2017_salib-an-open-source-python-library-for-sensitivit.pdf) |
| SHA-256 ของต้นฉบับ | `702455103000c4988ffa5b80079a40011a5edaaee90785df8ee598ace2741d2a` |
| coverage ของ full text | 2/2 หน้า (100.00%); สกัดได้ 638 คำ |

## คำถามวิจัย

งาน SALib: An open-source Python library for Sensitivity Analysis แก้ปัญหา verification, validation, uncertainty, สถิติ หรือ claim failure ใด และต้องใช้วินัยหลักฐานอะไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **การศึกษาเชิงเทคนิค/วิธีวิทยา** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ sensitivity, analysis, saltelli, global, andrea, salib, model, sobol วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **เครื่องมือวิเคราะห์ความไวแบบ global (Sobol, Morris) สำหรับหาว่าพารามิเตอร์ใดขับการจัดอันดับเวลาแข่ง**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** เครื่องมือวิเคราะห์ความไวแบบ global (Sobol, Morris) สำหรับหาว่าพารามิเตอร์ใดขับการจัดอันดับเวลาแข่ง
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'เครื่องมือวิเคราะห์ความไวแบบ global (Sobol, Morris) สำหรับหาว่าพารามิเตอร์ใดขับการจัดอันดับเวลาแข่ง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'เครื่องมือวิเคราะห์ความไวแบบ global (Sobol, Morris) สำหรับหาว่าพารามิเตอร์ใดขับการจัดอันดับเวลาแข่ง' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

วิธีเหล่านี้เพิ่มวินัย claim แต่ไม่สร้างข้อมูลกายภาพหรือ model validity ที่ขาด ความถูกต้องทางสถิติช่วย evaluator ที่ใช้ผิดโดเมนไม่ได้ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **เครื่องมือวิเคราะห์ความไวแบบ global (Sobol, Morris) สำหรับหาว่าพารามิเตอร์ใดขับการจัดอันดับเวลาแข่ง** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'เครื่องมือวิเคราะห์ความไวแบบ global (Sobol, Morris) สำหรับหาว่าพารามิเตอร์ใดขับการจัดอันดับเวลาแข่ง' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้ check จาก paper กับ known-positive, negative control ที่หักล้างได้, seed/refinement ซ้ำ และการแยก calibration/holdout แล้ว audit wording ของ claim กับผล |
| หลักฐานผ่านและล้มเหลว | ต้องมี error/uncertainty bound ที่กำหนดล่วงหน้า, ปฏิเสธหลักฐาน invalid ถูก, inference คำนึง multiplicity, provenance deterministic และไม่มี retrospective repair |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 2 หน้า, 4,125 ตัวอักษร, 638 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 2/2
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
