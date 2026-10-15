# CAD-018: Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations

English source: `CAD-018_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Heinrich Jiang, Hager Yasser Mohamed, Alexander Hitt, V. Lomakina, He-Nan Jiang, J. Jang |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv |
| DOI | Not recorded |
| arXiv | 2609.11573 |
| ระเบียน canonical | [https://arxiv.org/abs/2609.11573](https://arxiv.org/abs/2609.11573) |
| หัวข้อในคลัง | CAD, B-rep, assembly และการสร้างเรขาคณิต |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/04_cad_brep_assembly/CAD-018_Jiang2026_learn-the-solid-not-the-file-canonical-inputs-for.pdf) |
| SHA-256 ของต้นฉบับ | `933d6b844ee8fa5fef9cf36c697b9042f92c4be752a2905cf67b0f10980f2fff` |
| coverage ของ full text | 18/18 หน้า (100.00%); สกัดได้ 11,062 คำ |

## คำถามวิจัย

งาน Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations แทนหรือสร้าง CAD topology, geometry, constraint และ assembly semantics ได้พอสำหรับใช้งานวิศวกรรมต่อหรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานคณิตศาสตร์/เชิงรูปนัย** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, introduction, results และคำเทคนิคที่พบบ่อย ได้แก่ b-rep, solid, same, surface, face, features, frame, faces วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

metric CAD reconstruction/generation อาจให้รางวัลความคล้ายทางภาพหรือ geometry แต่พลาด topology invalid, design intent ที่หาย, mate ที่เป็นไปไม่ได้ และรายละเอียดผลิตไม่ได้ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'เสนอว่าแบบจำลองที่เรียนรู้ต้องเห็น solid ในรูปมาตรฐาน ไม่ใช่สิ่งแปลกปลอมจากลำดับในไฟล์ เป็นประเด็นเดียวกับ identity ของเรขาคณิตแบบกำหนดได้และการ hash ของเรา' ใน target ที่ระบุด้านล่าง |
| experiment และ control | ประเมิน representation จาก paper บน solid/assembly ที่ซ่อนด้วยการตรวจ topology, watertightness, constraint/editability, mass property, mate, interference, meshing และ load path |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่มอัตรา artifact ผ่านเชิงหน้าที่ที่งบสร้างเท่ากัน โดยไม่เพิ่ม topology corruption, mate invalid หรือ geometry-to-mesh discrepancy |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 18 หน้า, 67,095 ตัวอักษร, 11,062 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 18/18
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 6, 7, 9 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
