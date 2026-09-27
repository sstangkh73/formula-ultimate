# AE-007: CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics

English source: `AE-007_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | M. Elrefaie, Du-Le Shu, Matt Klenk, Faez Ahmed |
| ปี | 2025 |
| แหล่งตีพิมพ์ | arXiv.org |
| DOI | Not recorded |
| arXiv | 2512.07847 |
| ระเบียน canonical | [https://arxiv.org/abs/2512.07847](https://arxiv.org/abs/2512.07847) |
| หัวข้อในคลัง | อากาศพลศาสตร์และข้อมูล aerodynamic |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | full-text transfer record |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/10_aerodynamics/AE-007_Elrefaie2025_carbench-a-comprehensive-benchmark-for-neural-surr.pdf) |
| SHA-256 ของต้นฉบับ | `653bf51e34585036ffee19733c52ec4b5f5e356af5f0698ed1fef2fb46b1cad5` |
| coverage ของ full text | 39/39 หน้า (100.00%); สกัดได้ 24,347 คำ |

## คำถามวิจัย

งาน CarBench: A Comprehensive Benchmark for Neural Surrogates on High-Fidelity 3D Car Aerodynamics ยืนยันกลไก aerodynamic, dataset, solver หรือ surrogate ใด และในโดเมน geometry/flow ใด?

## วิธีและหลักฐาน

ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **ชุดข้อมูล/benchmark, หลักฐานการทดสอบกายภาพ, หลักฐานเชิงประจักษ์/การทดลอง, หลักฐาน simulation/เชิงตัวเลข** ป้ายนี้ใช้ช่วยนำทาง ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ abstract, conclusion, discussion, introduction, methods, results และคำเทคนิคที่พบบ่อย ได้แก่ models, training, model, error, pressure, surface, learning, test วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้**

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้
- **การตีความของผู้ทบทวน:** ทำให้ข้อค้นพบ 'benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้ออากาศพลศาสตร์และข้อมูล aerodynamic
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** ทำให้ข้อค้นพบ 'benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้ออากาศพลศาสตร์และข้อมูล aerodynamic โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ข้อสรุป aero ผูกกับตระกูล geometry, Reynolds number, turbulence/ground/wheel treatment, mesh และข้อมูล validation การถ่ายโอนจากรถถนนหรือทรงมาตรฐานมีขอบเขต การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-flow-heat path ของ Work 121, aero-field evaluator และ surrogate promotion audit** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-flow-heat path ของ Work 121, aero-field evaluator และ surrogate promotion audit |
| การเปลี่ยนแปลงที่เสนอ | สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ 'benchmark ความแม่นยำ ความสอดคล้องทางฟิสิกส์ ต้นทุน และความไม่แน่นอนของ surrogate รวมถึงหมวดที่ไม่เคยเห็น เป็นระเบียบการประเมินของ surrogate aero ที่เราจะใช้' ใน target ที่ระบุด้านล่าง |
| experiment และ control | ประเมิน geometry เดียวกันข้าม ride height, yaw, wheel/ground treatment, Reynolds number และ cooling flow แล้วเทียบ surrogate/CFD กับ independent CFD และการทดลองที่มี |
| หลักฐานผ่านและล้มเหลว | ต้องมี error ของ force, moment, balance, surface field และ uncertainty มีขอบเขตบน geometry held-out และไม่คัดทิ้งรูปทรงไม่คุ้นอย่างเป็นระบบ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 39 หน้า, 160,322 ตัวอักษร, 24,347 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 39/39
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 4, 9, 10, 12, 13, 16 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, discussion, introduction, methods, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
