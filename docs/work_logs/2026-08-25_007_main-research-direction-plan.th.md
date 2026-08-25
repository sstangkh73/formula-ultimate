# แผน Work 007: ทิศทางวิจัยหลักใน README

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_007_main-research-direction-plan.md`

## วัตถุประสงค์

ทำให้ทิศทาง Formula Ultimate ที่ตกลงกันเด่นชัดใน README ภาษาอังกฤษและไทย
พร้อมเก็บเป็นแนวทางข้าม session ของโปรเจกต์: เอเจนต์อัตโนมัติออกแบบรถทั้งคัน
และชิ้นส่วน 3D ได้โดยไม่ถูกกำหนดให้ใช้สถาปัตยกรรมดั้งเดิม แต่ candidate ทุกตัว
ยังต้องอยู่ใต้ฟิสิกส์ race/energy contract ที่อ้างอิง Formula One และมี version,
หลักฐานที่คำนวณจาก geometry อย่างอิสระ และ multi-fidelity validation

## ขอบเขต

- เขียนบทนำ README ใหม่โดยให้ภารกิจวิจัยหลักเด่นกว่าระยะ implementation แคบ
  ในปัจจุบัน
- ระบุคำถามวิจัยหลักด้วยภาษาที่หักล้างได้
- แยกข้อจำกัดสถาปัตยกรรมเก่าที่นำออกจากข้อจำกัด explicit ที่ยังคงไว้
- บันทึกกฎพลังงานการแข่งขัน: ต้องบรรทุก primary propulsion energy ก่อนแข่ง
  และห้ามเติมระหว่างแข่ง ส่วน internal recovery ต้องตรวจย้อนกลับผ่าน energy
  conservation ได้
- อธิบายว่าการเปรียบเทียบสถาปัตยกรรมที่อยู่นอก layout ICE/ERS ของ FIA
  ปัจจุบันต้องใช้ technology-neutral energy-equivalent profile
- กำหนดให้การออกแบบ 3D ทั้งคันเป็น causal input ของ simulation: geometry
  ต้องกำหนด packaging, mass, centre of mass, inertia และหลักฐาน structural,
  thermal และ aerodynamic ใน fidelity ถัดไป
- รักษาระยะ implementation Phase 1 ที่ยังแคบและขอบเขตข้ออ้างของมัน
- อัปเดต README อังกฤษและไทยพร้อมกัน โดยรักษา identifier, equation, unit,
  status, source และ limitation ให้เทียบเท่ากัน
- เพิ่ม ad-hoc memory update note ขนาดเล็ก เพราะผู้ใช้สั่งโดยตรงให้ทิศทางนี้
  เป็นแนวทางหลักของงานต่อไป

## ไฟล์ที่วางแผน

- `README.md`
- `README.th.md`
- plan/result record Work 007 ที่ตรงกัน แยกภาษาอังกฤษและไทย
- note ใหม่หนึ่งไฟล์ใต้
  `C:\Users\sstan\.codex\memories\extensions\ad_hoc\notes\`

## การตรวจสอบ

```powershell
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Final review จะตรวจด้วยว่า:

- README แต่ละภาษาลิงก์ไปยังไฟล์คู่ภาษา;
- README ภาษาไทยระบุ `README.md` เป็น English source;
- README ไม่สื่อว่า Level 0 หรือ Work 006 validate รถทางฟิสิกส์แล้ว;
- ข้ออ้าง FIA ลิงก์ regulations ทางการปี 2026 ที่ตรวจในงานนี้;
- open-ended invention กับ hard physics/energy/3D evidence constraint
  ถูกระบุพร้อมกันโดยไม่ขัดแย้ง

## เกณฑ์สำเร็จ

- ผู้อ่านใหม่หา ultimate mission, objective function, retained constraint,
  ข้อกำหนดหลักฐาน 3D, มาตรฐาน discovery, current phase และ non-claim
  ได้โดยตรงจาก README
- กฎห้ามเติมพลังงานระหว่างแข่งมี attribution และ version ที่ถูกต้อง
- Energy carrier ทางเลือกไม่ได้เปรียบจากพลังงานที่ไม่ประกาศ
- Generated geometry รายงานมวลหรือ performance เองไม่ได้ และยังระบุ
  independent evaluation ชัดเจน
- เอกสารอังกฤษและไทยมีโครงสร้างเทียบเท่ากัน และ repository test ทั้งหมดผ่าน
- Memory update note เก็บทิศทางเดียวกันโดยไม่แก้ managed memory registry โดยตรง

## ความเสี่ยง

- การคัดลอกข้อจำกัด power-unit เฉพาะสถาปัตยกรรมของ FIA ทั้งหมดจะลดความเปิด
  ของ design search README ต้องแยก inherited race protocol ออกจากกฎ
  technology-neutral equivalence
- การเขียนว่า “ไม่มีข้อจำกัด” จะเปิดช่องให้ infinite energy, magic material
  หรือ solver exploit README ต้องใช้ “ไม่มีสถาปัตยกรรมดั้งเดิมที่กำหนดล่วงหน้า
  นอกเหนือจากข้อจำกัดที่ประกาศ”
- ภารกิจระยะยาวที่กว้างอาจถูกเข้าใจผิดว่าเป็น capability ปัจจุบัน ต้องรักษา
  current status และ fidelity limit ให้เด่น
- FIA regulations เปลี่ยนได้ จึงต้องบันทึก issue และลิงก์ปี 2026 ที่แน่นอน
  แทนการเรียกว่าเป็นกฎถาวร

## สิ่งที่ไม่ทำโดยชัดเจน

- ไม่แก้ simulator, CAD, physics, optimization หรือ configuration
- ไม่อ้างว่าเอเจนต์ค้นพบเทคโนโลยีรถใหม่แล้ว
- ไม่อ้างว่า Work 006 มี FEA, CFD, manufacturability, safety หรือ full-vehicle
  validation
- ไม่รับข้อจำกัด geometry, power-unit architecture หรือ component ของ FIA
  ปัจจุบันทั้งหมด
- ไม่เขียน research charter หรือ design-language boundary ใหม่ใน work item นี้;
  อาจทำ consistency work item แยกภายหลังหากผู้ใช้ขอ
