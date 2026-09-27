# CAD-019: TG-Diff: Coupling Discrete Topology Diffusion and Topology-conditioned Geometry Diffusions for B-Rep Generation

English source: `CAD-019_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Ming-Ze Sun, Haiyong Jiang, Bingchen Yang, Haoxuan Song, Yidi Li, Jun Xiao, Peter Wonka |
| ปี | 2026 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2607.21928 |
| ระเบียน canonical | [https://arxiv.org/abs/2607.21928](https://arxiv.org/abs/2607.21928) |
| หัวข้อในคลัง | CAD, B-rep, assembly และการสร้างเรขาคณิต |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/04_cad_brep_assembly/CAD-019_Sun2026_tg-diff-coupling-discrete-topology-diffusion-and-t.pdf) |
| SHA-256 ของต้นฉบับ | `65e4810017865136db25147cc1d13babaaa9bc816eeba5b3d99b2467e1f51651` |
| coverage ของ full text | 15/15 หน้า (100.00%); สกัดได้ 11,523 คำ |

## คำถามวิจัย

งาน TG-Diff: Coupling Discrete Topology Diffusion and Topology-conditioned Geometry Diffusions for B-Rep Generation แทนหรือสร้าง CAD topology, geometry, constraint และ assembly semantics ได้พอสำหรับใช้งานวิศวกรรมต่อหรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ conclusion, introduction, limitations, methods, results และคำเทคนิคที่พบบ่อย ได้แก่ generation, surface, topology, b-rep, diffusion, surfaces, geometry, generated วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **สร้าง topology ของ B-rep ก่อนแล้วจึงเรขาคณิต สะท้อนการแบ่ง topology แล้วจึงมิติใน genome ของเรา**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** สร้าง topology ของ B-rep ก่อนแล้วจึงเรขาคณิต สะท้อนการแบ่ง topology แล้วจึงมิติใน genome ของเรา
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'สร้าง topology ของ B-rep ก่อนแล้วจึงเรขาคณิต สะท้อนการแบ่ง topology แล้วจึงมิติใน genome ของเรา' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'สร้าง topology ของ B-rep ก่อนแล้วจึงเรขาคณิต สะท้อนการแบ่ง topology แล้วจึงมิติใน genome ของเรา' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

metric CAD reconstruction/generation อาจให้รางวัลความคล้ายทางภาพหรือ geometry แต่พลาด topology invalid, design intent ที่หาย, mate ที่เป็นไปไม่ได้ และรายละเอียดผลิตไม่ได้ การตรวจ heading แบบอัตโนมัติ **พบ** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **สร้าง topology ของ B-rep ก่อนแล้วจึงเรขาคณิต สะท้อนการแบ่ง topology แล้วจึงมิติใน genome ของเรา** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก 'สร้าง topology ของ B-rep ก่อนแล้วจึงเรขาคณิต สะท้อนการแบ่ง topology แล้วจึงมิติใน genome ของเรา' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test |
| experiment และ control | ประเมิน representation จาก paper บน solid/assembly ที่ซ่อนด้วยการตรวจ topology, watertightness, constraint/editability, mass property, mate, interference, meshing และ load path |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่มอัตรา artifact ผ่านเชิงหน้าที่ที่งบสร้างเท่ากัน โดยไม่เพิ่ม topology corruption, mate invalid หรือ geometry-to-mesh discrepancy |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 15 หน้า, 73,918 ตัวอักษร, 11,523 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 15/15
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 5, 7, 8, 10, 11, 13 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: conclusion, introduction, limitations, methods, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
