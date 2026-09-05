# แผน Work 104: Protocol การค้นพบรถทั้งคันและเทคโนโลยี

ต้นฉบับภาษาอังกฤษ: `2026-09-06_104_whole-vehicle-discovery-protocol-plan.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

เขียน execution protocol ทดแทนแบบสองภาษาและลงวันที่ เพื่อเชื่อมสถาปัตยกรรมรถทั้งคันแบบเปิด executable morphology ชิ้นส่วนหลายหน้าที่ การควบคุม การทดลองประกอบร่วม และ evidence promotion สำรอง generation-first roadmap เดิมแบบตรงทุก byte ก่อนเพิ่มประกาศเปลี่ยนเอกสารอ้างอิง Revision เริ่มต้น: `9889daf`; worktree ที่ตรวจสะอาด Work 104 เป็นงานเอกสาร โดยยังเว้น Works 098–101 ไว้สำหรับ implementation

## ไฟล์ที่วางแผน

- `docs/contracts/WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md` และคู่ `.th.md`
- `docs/reports/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` และคู่ `.th.md`: เพิ่มลิงก์ลงวันที่ไป protocol ใหม่ โดยรักษาเนื้อหาประวัติเดิม
- `docs/reports/backups/2026-09-06_104/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` และคู่ `.th.md`: สำเนาก่อนแก้ที่ตรงทุก byte
- แผนสองภาษานี้และผลลัพธ์สองภาษาที่ตรงกัน

## ลำดับงาน

1. สร้างแผนทั้งสองภาษาโดยใช้สถานะ `In progress`
2. คัดลอกและตรวจ hash เอกสารเดิมทั้งคู่ก่อนแก้ต้นฉบับใด ๆ
3. เขียน protocol ใหม่พร้อมคำแปลไทย และเพิ่มลิงก์ประกาศเปลี่ยนเอกสารอ้างอิงในเอกสารเดิม
4. ตรวจ backup identity, local links, companion coverage, contract content และ whitespace/scope ของ staged files
5. เขียนผล เปลี่ยนแผนเป็น `Completed` เมื่อ validation ผ่านแล้วเท่านั้น stage เฉพาะไฟล์ของงาน commit และตรวจ commit

## Validation และเกณฑ์สำเร็จ

- เทียบ byte stream ของ backup ทั้งคู่กับ `git show 9889daf:<original-path>` ด้วย SHA-256 และ byte equality
- ตรวจว่าลบประกาศใหม่แล้วได้เอกสารต้นฉบับแต่ละฉบับกลับมาเหมือนเดิมทุกประการ
- ตรวจวันที่ version การระบุไฟล์อังกฤษ หัวข้อหมายเลขที่ตรงกัน technical identifiers และสมการ/คำสั่ง/ข้อกำหนดเชิงตัวเลขที่เทียบเท่ากันในภาษาไทย
- ตรวจปลายทาง relative Markdown links ทั้งหมดใน protocol ใหม่และประกาศใหม่ ลิงก์ใน backup ที่เก็บตรงทุก byte ยังคงอ้างบริบท directory ของรายงานเดิมและจะไม่ถูกแก้
- รัน `python -m unittest tests.test_repository_contract -q` และ `git diff --check`
- ตรวจขอบเขตไฟล์ staged แบบระบุชัด รัน `git diff --cached --check` สร้าง descriptive commit เดียวและตรวจยืนยัน
- สำเร็จเมื่อได้ protocol สองภาษาที่ review ได้ มีต้นฉบับเดิมครบ ระบุขอบเขต implementation ชัด และไม่อ้างว่าการเขียนเอกสารทำให้มีรถใช้งานได้หรือเทคโนโลยีใหม่แล้ว

## ความเสี่ยงและการควบคุม

- อาจสับสน protocol ทดแทนกับความสามารถที่ implement แล้ว: แยก normative target, software fixtures, exploratory evidence และ admitted physical evidence
- การตรึงขอบเขตชิ้นส่วนเร็วเกินไปอาจปิดกั้นกลไกทำงานร่วม: ให้ขอบเขตภายในวิวัฒนาการและทดลองประกอบได้ แต่ยังเข้มงวดกับ claim gates
- การไม่ตรึงการทดลองอาจทำให้ผลรั่วไหล: กำหนด experiment registration ที่แก้ย้อนหลังไม่ได้ แยก exploratory/admitted และใช้ identity ใหม่เมื่อเปลี่ยนแบบหลังเห็นผล
- คำแปลหรือ archive อาจคลาดเคลื่อน: เทียบเนื้อหาและ hash เก็บ backup ตรงต้นฉบับ และ commit ทั้งสองภาษาพร้อมกัน

## สิ่งที่ไม่ทำ

ไม่ implement simulator กฎฟิสิกส์ CAD operator scheduler หรือ search; ไม่รัน admitted experiment; ไม่อ้าง hardware หรือความใหม่; ไม่อัปเดตกฎการแข่งขันสด; ไม่เขียนทับ work logs เก่า; ไม่ push หรือเผยแพร่
