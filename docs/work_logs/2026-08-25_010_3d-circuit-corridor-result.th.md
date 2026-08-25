# ผลลัพธ์ Work 010: 3D Circuit Corridor และ Swept Envelope แบบมี Version

สถานะ: Completed

เสร็จเมื่อ: 2026-08-26 (Asia/Bangkok)

ต้นฉบับภาษาอังกฤษ: `2026-08-25_010_3d-circuit-corridor-result.md`

## ผลลัพธ์

Work 010 เสร็จสมบูรณ์ repository มีคิวฟิสิกส์ Work 010–019 แบบเรียงลำดับที่
คงทน และด่าน corridor แบบ SI ซึ่งทำซ้ำได้ โดยอินทิเกรต curvature, grade และ
bank แบบ piecewise-constant เป็น station 3D โมเดลคัดกรองรถวัตถุแข็งทั้งคัน
จากความกว้างคงที่ ขีดความสามารถ steering ตาม bicycle model และ swept
clearance ด้านใน/ด้านนอกของโค้งรัศมีคงที่

หลักฐานสนับสนุนสมมติฐานมาจาก fixture ที่พยายามหักล้าง: รถกว้าง 2.0 m อยู่ใน
corridor กว้างรวม 3.0 m ได้เมื่อดูแบบ static แต่ถูกปฏิเสธบนโค้งรัศมี 5.0 m
เพราะมุมหน้าด้านนอกกวาดจนได้ swept margin ติดลบ

ไม่มีการอ้างว่า Level-0 เป็นการยืนยันทางฟิสิกส์ profile สนามจริงทั้งสิบยังเป็น
`indeterminate` เพราะหลักฐานที่ตรวจสอบยังไม่มี 3D corridor แบบสำรวจที่มี
คุณภาพเพียงพอสำหรับ admission

## ไฟล์ที่เปลี่ยน

- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` และ `.th.md`: คิว Work
  010–019, completion gate และนิยามเสร็จร่วมกัน
- `src/formula_ultimate/physics/corridor.py`: contract แบบเข้มงวดสำหรับ
  evidence, segment, corridor, vehicle, station, closure, swept-envelope,
  assessment, parser และ loader
- `src/formula_ultimate/physics/__init__.py`: export API corridor สาธารณะ
- `config/circuits/corridor_schema_v1.json`: fixture เชิงวิเคราะห์สามชุดใต้
  schema `1.0` ซึ่งระบุชัดว่าไม่ใช่ geometry สนามจริง
- `scripts/validate_corridor.py`: validator สำหรับ fixture และ coverage ของ
  สนามจริงสิบแห่งที่ทำซ้ำได้
- `tests/test_corridor.py`: test 15 รายการ ครอบคลุม analytical,
  negative-input, evidence-gate, closure, symmetry และ replay
- `docs/physics/CIRCUIT_CORRIDOR_MODEL.md` และ `.th.md`: สมการ ระบบพิกัด
  สถานะหลักฐาน ขอบเขตโมเดล และข้อจำกัด
- `docs/problem_reports/2026-08-25_010_survey-geometry-evidence-gap.md` และ
  `.th.md`: การตรวจปัญหาแยกต่างหากและวิธีแก้แบบกำหนดขอบเขต
- คู่ plan/result Work 010 ภาษาอังกฤษและไทยนี้

## Contract และการตัดสินใจที่ implement

1. geometry ทั้งหมดใช้เมตร `1/m` และเรเดียน Segment length คือระยะในแปลน
   แนวนอน curvature บวกเลี้ยวซ้าย และ grade บวกทำให้ `z` สูงขึ้น
2. กึ่งกลางเพลาหลังของรถเคลื่อนตาม centerline ของ corridor โดยความกว้าง
   wheelbase, overhang หน้า/หลัง และ steering limit นิยาม rigid envelope
3. การอินทิเกรต constant-curvature ใช้ analytical arc update แบบ exact ส่วน
   ระยะ station มีผลต่อการสุ่มตัวอย่าง output เท่านั้น
4. uncertainty แนวนอนของแหล่งข้อมูลถูกหักจาก corridor ทั้งสองด้านก่อนตรวจ
   clearance ค่า invalid/non-finite ทำให้ล้มเหลวแทนการแก้ค่า
5. geometry หรือ steering ไม่ผ่านให้ `rejected` fixture สังเคราะห์ที่ผ่านให้
   `verification_passed` ข้อมูลโดยประมาณยังเป็น `indeterminate` และเฉพาะ
   หลักฐาน `surveyed` หรือ `operator_engineering` เท่านั้นที่ให้ `admitted`
6. closure residual ด้านตำแหน่ง ความสูง และ heading ที่ wrap แล้วสังเกตได้ และ
   ไม่ถูกบังคับให้ปิดแบบเงียบ

## ปัญหาที่พบและการแก้ไข

catalogue Work 008 ไม่มี centerline แบบสำรวจ, boundary, geometry กำแพง/kerb,
ระบบพิกัด timestamp และ uncertainty เชิงปริมาณครบทั้งสิบ layout ปัญหานี้ถูก
บันทึกเป็นรายงานแยก แทนการซ่อนไว้ในผลลัพธ์นี้

ขอบเขตซอฟต์แวร์/งานวิจัยถูกแก้ด้วย import contract แบบมี version, gate ตาม
evidence class, fixture เชิงวิเคราะห์โปร่งใส, residual ที่แสดงผล และผล
`indeterminate` สำหรับสนามจริงที่หลักฐานไม่พอ วิธีนี้ไม่ได้สร้างข้อมูลที่ขาด
ขึ้นมาเอง ยังต้องมีข้อมูลสำรวจที่มีสิทธิ์ใช้งานหรือ engineering data จากผู้ดูแล
สนามสำหรับ admission สนามจริง

## การทบทวนการทดลอง

- Independent variables: curvature และความกว้าง segment; ความกว้างรถ,
  wheelbase, overhang, steering limit; evidence class และ uncertainty
- Dependent variables: station 3D, steering demand, margin ด้านใน/ด้านนอก,
  จุดล้มเหลวแรก, closure residual และ admission status
- Controls: convention SI/sign, จุดอ้างอิงเพลาหลัง, คุณสมบัติ segment คงที่,
  spacing ทำซ้ำได้ และ evidence gate เดียวกัน
- หลักฐานสนับสนุน: analytical full circle มี closure residual แนวนอน
  `4.898587196589412e-15 m`, แนวตั้ง `0.0 m` และ heading
  `2.4492935982947064e-16 rad`; endpoint quarter-circle ซ้าย/ขวาตรงกับค่าคู่
  สะท้อนทาง analytical
- หลักฐานขัดแย้ง/หักล้าง: fixture static-fit ไม่ผ่าน outside sweep; fixture
  curvature สูงไม่ผ่าน steering; synthetic ที่ผ่านไม่สามารถให้ `admitted`
- คำอธิบายทางเลือกที่ตัดออก: การล้มเหลวไม่ได้อนุมานจากความกว้างรวมเท่านั้น
  แต่แสดง steering และ swept geometry แยกกัน
- หลักฐานที่ยังขาด: corridor สนามจริงระดับ survey และพลวัตยานยนต์ลำดับสูง
- ความมั่นใจ: สูงสำหรับสมการและพฤติกรรมซอฟต์แวร์ภายในขอบเขต analytical ที่
  ประกาศ; ต่ำ/ไม่มีสำหรับ admission สนามจริงจนกว่าจะมี geometry ที่เชื่อถือได้

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` พร้อมการหยุดทันทีเมื่อ exit ไม่เป็นศูนย์

### Unit tests เฉพาะงาน

```powershell
python -m unittest tests.test_corridor -v
```

Exit status: `0` ผลสำคัญ: `Ran 15 tests`; `OK`

### Tests ทั้ง repository

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0` ผลสำคัญ: `Ran 57 tests`; `OK`

### Validator แบบ deterministic

```powershell
python scripts/validate_corridor.py
```

Exit status: `0` ผลสำคัญ:

```text
synthetic_full_circle_pass: verification_passed
synthetic_overhang_reject: rejected
synthetic_steering_reject: rejected
real circuit total: 10
real circuit admitted: 0
real circuit indeterminate: 10
```

### Compilation และ whitespace

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` ทุกคำสั่ง โดยรัน `git diff --cached --check` อีกครั้งหลัง stage
แบบระบุขอบเขตและก่อน commit

## ข้อจำกัด

- planar rigid-body envelope ไม่รวม tyre force, slip, compliance, roll, pitch,
  suspension, กำแพง, kerb, collision และ transient yaw
- grade และ bank ถูกแทนค่าไว้ แต่ยังไม่เปลี่ยน force capacity หรือ swept
  clearance ใน Work 010
- fixture เชิงวิเคราะห์ยืนยันสมการ แต่ไม่ใช่ validation ทางกายภาพหรือสนามจริง
- admission จริงต้องมีการ ingest geometry ที่มีสิทธิ์ใช้งาน/ตรวจสอบแยกต่างหาก

## งานต่อเนื่อง

เริ่ม Work 011 ได้หลังจากตรวจ commit และสถานะหลัง commit ของ Work 010 แล้ว
เท่านั้น Work 011 จะ implement แรง tyre-road longitudinal/lateral และขอบเขต
saturation ที่สังเกตได้ โดยไม่เปลี่ยนความหมายหลักฐานของ Work 010
