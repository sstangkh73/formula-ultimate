# กรอบการวิจัย

> ฉบับภาษาไทยของ `RESEARCH_CHARTER.md`

## วิทยานิพนธ์ตั้งต้น

Formula Ultimate ศึกษาว่าสถาปัตยกรรมทางวิศวกรรมสามารถถูกค้นพบได้หรือไม่
โดยไม่กำหนด layout รถแบบดั้งเดิมล่วงหน้า แต่ยังคงข้อจำกัดด้านฟิสิกส์
ความปลอดภัย ทรัพยากร และภารกิจที่ประกาศไว้อย่างชัดเจน

## คำถามวิจัยหลัก

เมื่อไม่ได้กำหนดสถาปัตยกรรมรถล่วงหน้า การค้นหา design แบบ topology-evolving
จะค้นพบสถาปัตยกรรมรถแข่งแบบดั้งเดิมซ้ำ หรือสร้าง solution ที่แตกต่างและปรับตัว
ตามสภาพแวดล้อมการแข่งขันแต่ละแบบ

## คำถามระยะที่ 1

ภายใต้ resource budget และ search budget ที่เท่ากัน typed-graph topology
search สามารถค้นพบ powertrain architecture หนึ่งมิติที่ valid และมีผลเทียบเท่า
หรือดีกว่า fixed EV, ICE และ hybrid baseline ที่ optimize แล้วหรือไม่

## สมมติฐานที่หักล้างได้

### H1: การค้นพบ topology ที่ feasible

Free-topology search สร้าง candidate ที่ valid ทางฟิสิกส์และวิ่งจบการแข่งขัน
ด้วยอัตราที่สูงกว่า unguided random graph generation อย่างมีนัยสำคัญ

### H2: ประสิทธิภาพที่แข่งขันได้

เมื่อ evaluation budget เท่ากัน จะมี topology ที่ค้นพบอย่างน้อยหนึ่งตัวซึ่ง
ไม่ถูกครอบงำโดย fixed-topology baseline ที่ tune แล้ว ในมิติ race time,
energy, cost, mass และ reliability

### H3: ความเชี่ยวชาญตามสภาพแวดล้อม

เงื่อนไข track/energy ที่ต่างกันทำให้เกิดตระกูล architecture ที่มีการกระจาย
topology ต่างกันข้าม repeated seed และมีการ transfer ระหว่างเงื่อนไขแบบไม่สมมาตร

### H4: การอยู่รอดข้าม fidelity

ลำดับของ candidate ที่ promote แล้วยังคงเสถียรเพียงพอเมื่อประเมินใน fidelity
ระดับถัดไป มิฉะนั้น Level 0 จะไม่ใช่ search gate ที่เชื่อถือได้

## คำอธิบายทางเลือกที่ต้องทดสอบ

- สิ่งที่ดูเหมือนนวัตกรรมเป็น numerical exploit หรือ objective-function exploit
- ความต่างของ topology เกิดจาก compute budget ที่ไม่เท่ากัน
- การ convergence เกิดจากอคติของ component library มากกว่าฟิสิกส์
- ความไม่แน่นอนของ surrogate ซ่อน performance ที่แย่ใน high fidelity
- topology ดูเหมือน specialized เพราะ parameter ต่างกัน ไม่ใช่ connection

## ระยะปัจจุบัน

กำลังสร้างฐาน repository และออกแบบระบบฟิสิกส์ Level-0 ยังไม่มีการทดสอบ
สมมติฐานด้าน discovery หรือ performance

## สิ่งที่ไม่ใช่เป้าหมายของ Simulator ระยะแรก

- การสร้าง 3D geometry เต็มรูปแบบ
- CFD หรือ external aerodynamics แบบละเอียด
- FEA หรือการรับรอง crash
- tyre transient และ contact-patch mechanics แบบละเอียด
- wheel count หรือ wheel placement แบบอิสระ
- active suspension
- การเรียนรู้ driver/control policy
- ข้ออ้างด้าน manufacturability หรือความปลอดภัยในโลกจริง

หัวข้อเหล่านี้เป็นการเพิ่ม fidelity หรือขอบเขตในอนาคต ไม่ใช่ feature ที่
Level 0 แอบประมาณค่าไว้
