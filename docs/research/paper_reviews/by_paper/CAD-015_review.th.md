# CAD-015: Assemble Them All: Physics-Based Planning for Generalizable Assembly by Disassembly

English source: `CAD-015_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Yunsheng Tian, Jie Xu, Yichen Li, Jieliang Luo, Shinjiro Sueda, Hui Li, Karl D. D. Willis, Wojciech Matusik |
| ปี | 2022 |
| แหล่งตีพิมพ์ | ACM Transactions on Graphics |
| DOI | 10.1145/3550454.3555525 |
| arXiv | 2211.03977 |
| ระเบียน canonical | [https://doi.org/10.1145/3550454.3555525](https://doi.org/10.1145/3550454.3555525) |
| หัวข้อในคลัง | CAD, B-rep, assembly และการสร้างเรขาคณิต |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/04_cad_brep_assembly/CAD-015_Tian2022_assemble-them-all-physics-based-planning-for-gener.pdf) |
| SHA-256 ของต้นฉบับ | `c50242c262ee42e158b7e051157e14323b907d27e0c069f4a107d5b305cdb7c6` |
| coverage ของ full text | 15/15 หน้า (100.00%); สกัดได้ 11,928 คำ |

## คำถามวิจัย

งาน Assemble Them All: Physics-Based Planning for Generalizable Assembly by Disassembly แทนหรือสร้าง CAD topology, geometry, constraint และ assembly semantics ได้พอสำหรับใช้งานวิศวกรรมต่อหรือไม่?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ introduction, limitations, results และคำเทคนิคที่พบบ่อย ได้แก่ assembly, planning, disassembly, parts, path, state, assemblies, physics-based วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **การวางแผนถอดประกอบด้วยฟิสิกส์พิสูจน์ว่าประกอบได้จริง เป็น gate ความสามารถในการสร้างสำหรับรถหลายชิ้นส่วนที่สร้างขึ้น**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** การวางแผนถอดประกอบด้วยฟิสิกส์พิสูจน์ว่าประกอบได้จริง เป็น gate ความสามารถในการสร้างสำหรับรถหลายชิ้นส่วนที่สร้างขึ้น
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'การวางแผนถอดประกอบด้วยฟิสิกส์พิสูจน์ว่าประกอบได้จริง เป็น gate ความสามารถในการสร้างสำหรับรถหลายชิ้นส่วนที่สร้างขึ้น' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'การวางแผนถอดประกอบด้วยฟิสิกส์พิสูจน์ว่าประกอบได้จริง เป็น gate ความสามารถในการสร้างสำหรับรถหลายชิ้นส่วนที่สร้างขึ้น' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อCAD, B-rep, assembly และการสร้างเรขาคณิต โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

metric CAD reconstruction/generation อาจให้รางวัลความคล้ายทางภาพหรือ geometry แต่พลาด topology invalid, design intent ที่หาย, mate ที่เป็นไปไม่ได้ และรายละเอียดผลิตไม่ได้ การตรวจ heading แบบอัตโนมัติ **พบ** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **การวางแผนถอดประกอบด้วยฟิสิกส์พิสูจน์ว่าประกอบได้จริง เป็น gate ความสามารถในการสร้างสำหรับรถหลายชิ้นส่วนที่สร้างขึ้น** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140 |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'การวางแผนถอดประกอบด้วยฟิสิกส์พิสูจน์ว่าประกอบได้จริง เป็น gate ความสามารถในการสร้างสำหรับรถหลายชิ้นส่วนที่สร้างขึ้น' ใน target ที่ระบุด้านล่าง |
| experiment และ control | ประเมิน representation จาก paper บน solid/assembly ที่ซ่อนด้วยการตรวจ topology, watertightness, constraint/editability, mass property, mate, interference, meshing และ load path |
| หลักฐานผ่านและล้มเหลว | ต้องเพิ่มอัตรา artifact ผ่านเชิงหน้าที่ที่งบสร้างเท่ากัน โดยไม่เพิ่ม topology corruption, mate invalid หรือ geometry-to-mesh discrepancy |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 15 หน้า, 74,639 ตัวอักษร, 11,928 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 15/15
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 6, 7, 8, 9, 12 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: introduction, limitations, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
