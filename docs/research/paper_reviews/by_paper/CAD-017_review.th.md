# CAD-017: Geometric Deep Learning for Computer-Aided Design: A Survey

English source: `CAD-017_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Negar Heidari, A. Iosifidis |
| ปี | 2024 |
| แหล่งตีพิมพ์ | IEEE Access |
| DOI | Not recorded |
| arXiv | 2402.17695 |
| ระเบียน canonical | [https://arxiv.org/abs/2402.17695](https://arxiv.org/abs/2402.17695) |
| หัวข้อในคลัง | CAD, B-rep, assembly และการสร้างเรขาคณิต |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/04_cad_brep_assembly/CAD-017_Heidari2024_geometric-deep-learning-for-computer-aided-design.pdf) |
| SHA-256 ของต้นฉบับ | `4ffd28c88c3e7f80a2412d6d0bc45b4b075521acc7c48dbbcac9637daa6851d0` |
| coverage ของ full text | 28/28 หน้า (100.00%); สกัดได้ 26,272 คำ |

## คำถามวิจัย

งาน Geometric Deep Learning for Computer-Aided Design: A Survey แทนหรือสร้าง CAD topology, geometry, constraint และ assembly semantics ได้พอสำหรับใช้งานวิศวกรรมต่อหรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **งานทบทวน/สังเคราะห์, ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ ไม่พบ heading ที่เชื่อถือได้ และคำเทคนิคที่พบบ่อย ได้แก่ models, learning, b-rep, sketch, data, dataset, graph, design วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **survey การเรียนรู้บนข้อมูล CAD (B-rep ลำดับ การประกอบ) เป็นแผนที่วิธีและชุดข้อมูลที่มีอยู่**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** survey การเรียนรู้บนข้อมูล CAD (B-rep ลำดับ การประกอบ) เป็นแผนที่วิธีและชุดข้อมูลที่มีอยู่
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'survey การเรียนรู้บนข้อมูล CAD (B-rep ลำดับ การประกอบ) เป็นแผนที่วิธีและชุดข้อมูลที่มีอยู่' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'survey การเรียนรู้บนข้อมูล CAD (B-rep ลำดับ การประกอบ) เป็นแผนที่วิธีและชุดข้อมูลที่มีอยู่' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

metric CAD reconstruction/generation อาจให้รางวัลความคล้ายทางภาพหรือ geometry แต่พลาด topology invalid, design intent ที่หาย, mate ที่เป็นไปไม่ได้ และรายละเอียดผลิตไม่ได้ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **survey การเรียนรู้บนข้อมูล CAD (B-rep ลำดับ การประกอบ) เป็นแผนที่วิธีและชุดข้อมูลที่มีอยู่** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'survey การเรียนรู้บนข้อมูล CAD (B-rep ลำดับ การประกอบ) เป็นแผนที่วิธีและชุดข้อมูลที่มีอยู่' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ประเมิน representation จาก paper บน solid/assembly ที่ซ่อนด้วยการตรวจ topology, watertightness, constraint/editability, mass property, mate, interference, meshing และ load path |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่มอัตรา artifact ผ่านเชิงหน้าที่ที่งบสร้างเท่ากัน โดยไม่เพิ่ม topology corruption, mate invalid หรือ geometry-to-mesh discrepancy |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 28 หน้า, 171,254 ตัวอักษร, 26,272 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 28/28
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 3, 5, 6, 7, 9, 10, 11, 12 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
