# EN-012: Battery model impact on time-optimal co-design for electric racing cars: review and application

English source: `EN-012_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | G. Riva, Stefano Radrizzani, Giulio Panzani |
| ปี | 2023 |
| แหล่งตีพิมพ์ | IEEE Transactions on Transportation Electrification |
| DOI | Not recorded |
| arXiv | 2312.17003 |
| ระเบียน canonical | [https://arxiv.org/abs/2312.17003](https://arxiv.org/abs/2312.17003) |
| หัวข้อในคลัง | แหล่งเก็บพลังงาน powertrain และการจัดการพลังงานในการแข่ง |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/08_energy_powertrain/EN-012_Riva2023_battery-model-impact-on-time-optimal-co-design-for.pdf) |
| SHA-256 ของต้นฉบับ | `cf3c7217b631b41703a5a946fa9487ccf0f88b8334c2cd438803a0544fa9d4a6` |
| coverage ของ full text | 12/12 หน้า (100.00%); สกัดได้ 10,936 คำ |

## คำถามวิจัย

รายละเอียด battery model ใดจำเป็นต่อ sizing รถแข่ง และรายละเอียดใดจำเป็นต่อ optimal control ที่ให้ตัวแปรเชิงกายภาพน่าเชื่อถือ?

## วิธีและหลักฐาน

paper ใส่ battery model หลายระดับรายละเอียดใน time-optimal co-design ของรถแข่งไฟฟ้า เทียบ model ง่ายจาก datasheet กับ model ที่รวม open-circuit voltage ตาม state of charge และพฤติกรรมไฟฟ้าที่สมจริงกว่า โดย formulation แบบ convex/nonlinear ใช้ spatial step 15 m (หน้า 5-9)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** model ง่ายให้ผล battery sizing สอดคล้องกัน ส่วน model ละเอียดจำเป็นเมื่อต้องการศึกษาวิวัฒนาการตัวแปร control ที่น่าเชื่อถือ ใน model ละเอียด ความต่างเวลาแข่งระหว่าง 24 กับ 25 cell ขนานแทบไม่มี และ convex relaxation อาจให้ profile ตัวแปรพลังงานที่ไม่เป็นกายภาพ (หน้า 1-2, 9, 11)
- **การตีความของผู้ทบทวน:** paper ไม่ได้แสดงการกลับอันดับ architecture แบบทั่วไป แต่แสดงเส้นแบ่ง fidelity ที่แคบกว่า: model ง่ายอาจพอสำหรับ sizing แต่ไม่พอสำหรับตีความ trajectory การควบคุมพลังงานที่ optimize
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** paper ไม่ได้แสดงการกลับอันดับ architecture แบบทั่วไป แต่แสดงเส้นแบ่ง fidelity ที่แคบกว่า: model ง่ายอาจพอสำหรับ sizing แต่ไม่พอสำหรับตีความ trajectory การควบคุมพลังงานที่ optimize โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผลเฉพาะโจทย์รถแข่งไฟฟ้า parameter battery, discretization 15 m และ formulation convex/non-convex ที่ศึกษา ยังไม่รวมทุก chemistry, degradation pathway, containment หรือ thermal architecture เต็ม การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **paper ไม่ได้แสดงการกลับอันดับ architecture แบบทั่วไป แต่แสดงเส้นแบ่ง fidelity ที่แคบกว่า: model ง่ายอาจพอสำหรับ sizing แต่ไม่พอสำหรับตีความ trajectory การควบคุมพลังงานที่ optimize** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **onboard-energy realization ของ Work 120, power/thermal state model และ race-energy ledger** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | onboard-energy realization ของ Work 120, power/thermal state model และ race-energy ledger |
| การเปลี่ยนแปลงที่เสนอ | ใช้ model ง่ายเฉพาะ sizing pre-screen และบังคับ model ที่ขึ้นกับ state สำหรับตีความ control เทียบทั้งสองด้วย forward replay, energy/heat closure และ ranking stability ก่อนเลื่อน Work 120 |
| experiment และ control | เทียบ model/strategy จาก paper กับ lumped model ปัจจุบันบน lap/stint เดียวกัน โดยรวมมวล carrier/containment, efficiency map, auxiliary, cooling, recovery และ degradation |
| หลักฐานผ่านและล้มเหลว | ต้องปิดสมดุล energy/heat อย่างอิสระ, แข่งจบ, state/temperature error มีขอบเขต และอันดับคงตัวภายใต้ model refinement ที่ admit |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 12 หน้า, 64,333 ตัวอักษร, 10,936 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 12/12
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 3, 4, 5, 6, 8, 9 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
