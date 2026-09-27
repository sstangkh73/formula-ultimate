# CAD-033: KDH-CAD: Knowledge-data hybrid CAD learning under data scarcity

English source: `CAD-033_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Zi-Qi Gao, Zhijie Yang, Qiang Zou |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2606.01702 |
| ระเบียน canonical | [https://arxiv.org/abs/2606.01702](https://arxiv.org/abs/2606.01702) |
| หัวข้อในคลัง | CAD, B-rep, assembly และการสร้างเรขาคณิต |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/04_cad_brep_assembly/CAD-033_Gao2026_kdh-cad-knowledge-data-hybrid-cad-learning-under-d.pdf) |
| SHA-256 ของต้นฉบับ | `341e6905aeb9509b6f27e8bc7df22361a14a2f25e5e7f2f54dc331699310c6c8` |
| coverage ของ full text | 18/18 หน้า (100.00%); สกัดได้ 12,585 คำ |

## คำถามวิจัย

งาน KDH-CAD: Knowledge-data hybrid CAD learning under data scarcity แทนหรือสร้าง CAD topology, geometry, constraint และ assembly semantics ได้พอสำหรับใช้งานวิศวกรรมต่อหรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract และคำเทคนิคที่พบบ่อย ได้แก่ knowledge, data, models, kdh-cad, part, learning, model, category วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **รวมความรู้ทางวิศวกรรมกับข้อมูล CAD ที่มีน้อย เกี่ยวข้องเพราะข้อมูลชิ้นส่วนรถมีน้อยและเป็นกรรมสิทธิ์**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** รวมความรู้ทางวิศวกรรมกับข้อมูล CAD ที่มีน้อย เกี่ยวข้องเพราะข้อมูลชิ้นส่วนรถมีน้อยและเป็นกรรมสิทธิ์
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'รวมความรู้ทางวิศวกรรมกับข้อมูล CAD ที่มีน้อย เกี่ยวข้องเพราะข้อมูลชิ้นส่วนรถมีน้อยและเป็นกรรมสิทธิ์' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'รวมความรู้ทางวิศวกรรมกับข้อมูล CAD ที่มีน้อย เกี่ยวข้องเพราะข้อมูลชิ้นส่วนรถมีน้อยและเป็นกรรมสิทธิ์' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

metric CAD reconstruction/generation อาจให้รางวัลความคล้ายทางภาพหรือ geometry แต่พลาด topology invalid, design intent ที่หาย, mate ที่เป็นไปไม่ได้ และรายละเอียดผลิตไม่ได้ การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **รวมความรู้ทางวิศวกรรมกับข้อมูล CAD ที่มีน้อย เกี่ยวข้องเพราะข้อมูลชิ้นส่วนรถมีน้อยและเป็นกรรมสิทธิ์** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'รวมความรู้ทางวิศวกรรมกับข้อมูล CAD ที่มีน้อย เกี่ยวข้องเพราะข้อมูลชิ้นส่วนรถมีน้อยและเป็นกรรมสิทธิ์' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ประเมิน representation จาก paper บน solid/assembly ที่ซ่อนด้วยการตรวจ topology, watertightness, constraint/editability, mass property, mate, interference, meshing และ load path |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่มอัตรา artifact ผ่านเชิงหน้าที่ที่งบสร้างเท่ากัน โดยไม่เพิ่ม topology corruption, mate invalid หรือ geometry-to-mesh discrepancy |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 18 หน้า, 79,774 ตัวอักษร, 12,585 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 18/18
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 5, 7, 8, 10, 11, 12, 14 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
