# TY-011: Bayesian Optimization-based Tire Parameter and Uncertainty Estimation for Real-World Data

English source: `TY-011_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Sven Goblirsch, Benedikt Ruhland, Johannes Betz, Markus Lienkamp |
| ปี | 2025 |
| แหล่งตีพิมพ์ | 2025 IEEE Intelligent Vehicles Symposium (IV) |
| DOI | Not recorded |
| arXiv | 2504.20863 |
| ระเบียน canonical | [https://arxiv.org/abs/2504.20863](https://arxiv.org/abs/2504.20863) |
| หัวข้อในคลัง | ยาง แรงเสียดทาน และการสัมผัสถนน |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/09_tyres_friction/TY-011_Goblirsch2025_bayesian-optimization-based-tire-parameter-and-unc.pdf) |
| SHA-256 ของต้นฉบับ | `3fb9b0adadf1d34a0c9ec92e3923ef10cddfeb9d94d4519fd4f4d13e86345d8a` |
| coverage ของ full text | 8/8 หน้า (100.00%); สกัดได้ 5,640 คำ |

## คำถามวิจัย

จะระบุพารามิเตอร์ยางและ uncertainty จากข้อมูลขับจริงได้หรือไม่ และ excitation ของ manoeuvre มีผลต่อ identifiability อย่างไร?

## วิธีและหลักฐาน

งานใช้ stochastic variational inference ใน workflow แบบ Bayesian optimization ประเมินผลของ excitation และเทียบ Nelder-Mead baseline ในกรณี identification เชิงทฤษฎีและข้อมูลจริง (หน้า 2-3)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** วิธีประมาณ distribution ของพารามิเตอร์แทน best fit จุดเดียวและแสดงว่า excitation มีผลต่อความแม่น งานยังพบว่าการ identify เฉพาะพารามิเตอร์ยางอาจแย่กว่าการ identify model เต็ม เตือนว่าห้ามถือพารามิเตอร์รถอื่นว่ารู้แน่ (หน้า 2-3)
- **การตีความของผู้ทบทวน:** การทดลองเชื่อมการออกแบบ manoeuvre กับ uncertainty เพราะการขับทั่วไปที่ทำได้ง่ายอาจไม่กระตุ้นพารามิเตอร์ที่ racing controller ต้องใช้
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** การทดลองเชื่อมการออกแบบ manoeuvre กับ uncertainty เพราะการขับทั่วไปที่ทำได้ง่ายอาจไม่กระตุ้นพารามิเตอร์ที่ racing controller ต้องใช้ โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผลขึ้นกับ tyre/vehicle model, ช่วง excitation, sensor และคุณภาพข้อมูลจริง posterior uncertainty ไม่แก้ model-form error หรือ extrapolation นอกสภาวะที่วัด การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **การทดลองเชื่อมการออกแบบ manoeuvre กับ uncertainty เพราะการขับทั่วไปที่ทำได้ง่ายอาจไม่กระตุ้นพารามิเตอร์ที่ racing controller ต้องใช้** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ground-interaction contract, tyre-state estimator และการส่งต่อ uncertainty ไปยัง lap/safety** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ground-interaction contract, tyre-state estimator และการส่งต่อ uncertainty ไปยัง lap/safety |
| การเปลี่ยนแปลงที่เสนอ | ออกแบบชุด manoeuvre ระบุยางแบบ D-optimal fit uncertainty ร่วม tyre/vehicle และส่ง posterior sample ผ่าน held-out lap replay ก่อนลดขอบเขต ground-contact envelope |
| experiment และ control | fit และ validate กับ manoeuvre แยกข้าม combined slip, load, camber, pressure, temperature, wear, speed และสภาพถนน แล้วเทียบ low-fidelity model ปัจจุบัน |
| หลักฐานผ่านและล้มเหลว | ต้องมี force/moment และ temperature/wear error มีขอบเขตบน manoeuvre held-out และทำ lap replay ดีขึ้นโดยไม่ซ่อน extrapolation นอก tyre envelope |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 8 หน้า, 34,495 ตัวอักษร, 5,640 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 8/8
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 4 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
