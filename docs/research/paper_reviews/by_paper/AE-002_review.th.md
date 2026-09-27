# AE-002: Spectral/hp element simulation of flow past a Formula One front wing: validation against experiments

English source: `AE-002_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | F. Buscariolo, Julien Hoessler, D. Moxey, Ayad Jassim, Kevin Gouder, J. Basley, Yushi Murai, G. Assi, S. Sherwin |
| ปี | 2019 |
| แหล่งตีพิมพ์ | Journal of Wind Engineering and Industrial Aerodynamics |
| DOI | Not recorded |
| arXiv | 1909.06701 |
| ระเบียน canonical | [https://arxiv.org/abs/1909.06701](https://arxiv.org/abs/1909.06701) |
| หัวข้อในคลัง | อากาศพลศาสตร์และข้อมูล aerodynamic |
| ความสัมพันธ์กับโครงการ | `data` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/10_aerodynamics/AE-002_Buscariolo2019_spectral-hp-element-simulation-of-flow-past-a-form.pdf) |
| SHA-256 ของต้นฉบับ | `8d241b76654c21b2d35d3b5a37fb92e92b71a9c254e30a76d8401d68370ef078` |
| coverage ของ full text | 18/18 หน้า (100.00%); สกัดได้ 5,545 คำ |

## คำถามวิจัย

high-fidelity CFD ต้องใช้ spatial/temporal resolution เท่าใดจึงสร้างโครงสร้างการไหลที่วัดได้ของปีกหน้าใน ground effect?

## วิธีและหลักฐาน

Imperial Front Wing มี CAD และข้อมูลทดลอง oil-flow/PIV แล้วเทียบ under-resolved DNS/implicit LES ด้วย spectral/hp order 3, 4 และ 5 กับตำแหน่ง/ความเข้ม vortex, wall feature, lift และ drag ที่วัด (หน้า 1, 7-16)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** กรณี order 3 มี resolution ไม่พอ กรณี order 5 ตรงการทดลองด้าน reattachment/flow feature ดีที่สุด ให้ downforce สูงกว่า order 4 อยู่ 4.5% และ lift เสถียรเฉพาะช่วงท้ายของ averaging window (หน้า 8, 16)
- **การตีความของผู้ทบทวน:** field resolution ต่ำที่ดูสมจริงอาจให้แนวโน้ม load ผิด จึงต้องตรวจ resolution และ averaging-time sensitivity ไม่ใช่ coefficient ภาพเดียว
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** field resolution ต่ำที่ดูสมจริงอาจให้แนวโน้ม load ผิด จึงต้องตรวจ resolution และ averaging-time sensitivity ไม่ใช่ coefficient ภาพเดียว โดยเป็นความเชื่อมโยงชนิด `data` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

เป็น geometry ปีกหน้าหนึ่งแบบและ high-fidelity setup หนึ่งชุด ไม่ใช่รถเต็มคันหรือ validation turbulence model ทั่วไป lift ของ order สูงสุดยังเปลี่ยนในช่วงรันมาก จึงต้องระวัง averaging convergence การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **field resolution ต่ำที่ดูสมจริงอาจให้แนวโน้ม load ผิด จึงต้องตรวจ resolution และ averaging-time sensitivity ไม่ใช่ coefficient ภาพเดียว** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **geometry-flow-heat path ของ Work 121, aero-field evaluator และ surrogate promotion audit** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | geometry-flow-heat path ของ Work 121, aero-field evaluator และ surrogate promotion audit |
| การเปลี่ยนแปลงที่เสนอ | ใช้ IFW CAD/PIV เป็น independent aero gate แรก โดยทำซ้ำตำแหน่ง vortex, reattachment, lift/drag ที่ resolution อย่างน้อยสามระดับและกฎ averaging convergence ที่ลงทะเบียนล่วงหน้า |
| experiment และ control | ประเมิน geometry เดียวกันข้าม ride height, yaw, wheel/ground treatment, Reynolds number และ cooling flow แล้วเทียบ surrogate/CFD กับ independent CFD และการทดลองที่มี |
| หลักฐานผ่านและล้มเหลว | ต้องมี error ของ force, moment, balance, surface field และ uncertainty มีขอบเขตบน geometry held-out และไม่คัดทิ้งรูปทรงไม่คุ้นอย่างเป็นระบบ |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 18 หน้า, 40,766 ตัวอักษร, 5,545 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 18/18
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 5, 6, 8, 10 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, introduction, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
