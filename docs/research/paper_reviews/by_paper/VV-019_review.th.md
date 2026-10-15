# VV-019: Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)

English source: `VV-019_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Joelle Pineau, Philippe Vincent-Lamarre, Koustuv Sinha, V. Larivière, A. Beygelzimer, Florence d'Alché-Buc, E. Fox, H. Larochelle |
| ปี | 2021 |
| แหล่งตีพิมพ์ | Journal of machine learning research |
| DOI | Not recorded |
| arXiv | 2003.12206 |
| ระเบียน canonical | [https://arxiv.org/abs/2003.12206](https://arxiv.org/abs/2003.12206) |
| หัวข้อในคลัง | verification, validation, uncertainty, สถิติ และ claim |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/13_validation_statistics_claims/VV-019_Pineau2021_improving-reproducibility-in-machine-learning-rese.pdf) |
| SHA-256 ของต้นฉบับ | `0ea62d8ae3eede31d18faedf4246d59f9c07346df59b4ca99407ef4323d2307f` |
| coverage ของ full text | 22/22 หน้า (100.00%); สกัดได้ 7,806 คำ |

## คำถามวิจัย

งาน Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program) แก้ปัญหา verification, validation, uncertainty, สถิติ หรือ claim failure ใด และต้องใช้วินัยหลักฐานอะไร?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, การศึกษา optimization/search** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ reproducibility, code, research, neurips, learning, machine, checklist, papers วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **checklist และข้อค้นพบด้านการทำซ้ำได้ เสริมข้อกำหนด metadata การ replay**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** checklist และข้อค้นพบด้านการทำซ้ำได้ เสริมข้อกำหนด metadata การ replay
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'checklist และข้อค้นพบด้านการทำซ้ำได้ เสริมข้อกำหนด metadata การ replay' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'checklist และข้อค้นพบด้านการทำซ้ำได้ เสริมข้อกำหนด metadata การ replay' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อverification, validation, uncertainty, สถิติ และ claim โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

วิธีเหล่านี้เพิ่มวินัย claim แต่ไม่สร้างข้อมูลกายภาพหรือ model validity ที่ขาด ความถูกต้องทางสถิติช่วย evaluator ที่ใช้ผิดโดเมนไม่ได้ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **checklist และข้อค้นพบด้านการทำซ้ำได้ เสริมข้อกำหนด metadata การ replay** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'checklist และข้อค้นพบด้านการทำซ้ำได้ เสริมข้อกำหนด metadata การ replay' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ใช้ check จาก paper กับ known-positive, negative control ที่หักล้างได้, seed/refinement ซ้ำ และการแยก calibration/holdout แล้ว audit wording ของ claim กับผล |
| หลักฐานผ่านและล้มเหลว | ต้องมี error/uncertainty bound ที่กำหนดล่วงหน้า, ปฏิเสธหลักฐาน invalid ถูก, inference คำนึง multiplicity, provenance deterministic และไม่มี retrospective repair |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 22 หน้า, 50,128 ตัวอักษร, 7,806 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 22/22
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 6, 7, 14 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
