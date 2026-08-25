# โมเดล Corridor ของสนามและ Swept Envelope

สถานะ: ดำเนินการแล้วสำหรับ Work 010

ต้นฉบับภาษาอังกฤษ: `CIRCUIT_CORRIDOR_MODEL.md`

## จุดประสงค์และขอบเขตของข้ออ้าง

โมเดลนี้เป็นด่านคัดกรองความเป็นไปได้ระยะแรกที่ตรวจสอบย้อนหลังได้ ระหว่าง
catalogue สนามจริงกับพลวัตยานยนต์ในขั้นถัดไป โมเดลสามารถปฏิเสธรถวัตถุแข็งที่
ความกว้าง มุมเลี้ยวสูงสุด wheelbase หรือ overhang ไม่สามารถอยู่ใน corridor
เชิงวิเคราะห์ได้ แต่ไม่ได้ยืนยันความถูกต้องทางฟิสิกส์ ความปลอดภัยการชน
เวลาแข่งขันต่อรอบ หรือการจบการแข่งขัน

repository นี้มี fixture เชิงวิเคราะห์ ไม่ใช่ข้อมูลสำรวจของสนามจริงทั้งสิบแห่ง
ดังนั้น profile ทั้งสิบยังคงเป็น `indeterminate` ที่ด่านนี้ ข้อจำกัดด้านหลักฐาน
และการแก้ปัญหาถูกบันทึกใน
`docs/problem_reports/2026-08-25_010_survey-geometry-evidence-gap.th.md`

## สัญญาพิกัด หน่วย และเครื่องหมาย

- ระยะทั้งหมดใช้เมตร curvature ใช้ `1/m` และมุมใช้เรเดียน
- จุดอ้างอิงคือกึ่งกลางเพลาหลังของรถ
- `x-y` ท้องถิ่นเป็นระนาบคาร์ทีเซียนแนวนอนแบบมือขวา และ `z` ชี้ขึ้น
- heading ศูนย์ชี้ไปทาง `x` บวก และ curvature บวกหมายถึงเลี้ยวซ้าย
- grade บวกทำให้ `z` เพิ่ม ส่วน bank บวกถูกเก็บเป็นคุณสมบัติของ corridor
- `width_left_m` และ `width_right_m` คือระยะตั้งฉากแนวนอนจาก centerline
  ค่า uncertainty แนวนอนของหลักฐานถูกหักจากทั้งสองด้านแบบอนุรักษนิยม
- `length_m` ของ segment คือระยะในแปลนแนวนอน โดย curvature, grade, bank
  และความกว้างคงที่เป็นช่วงภายในหนึ่ง segment

## การอินทิเกรตเส้นอ้างอิง

สำหรับ pose เริ่ม `(x0, y0, z0, psi0)`, curvature แนวนอนที่มีเครื่องหมาย `k`,
ระยะในแปลน `s` และ grade `g`:

```text
psi1 = psi0 + k s

if k = 0:
    x1 = x0 + s cos(psi0)
    y1 = y0 + s sin(psi0)
else:
    x1 = x0 + [sin(psi1) - sin(psi0)] / k
    y1 = y0 + [-cos(psi1) + cos(psi0)] / k

z1 = z0 + s tan(g)
```

การอัปเดต constant-curvature แบบ exact ถูกใช้ที่ระยะ station ซึ่งกำหนดได้ซ้ำ
ค่า closure residual รายงานความคลาดตำแหน่งแนวนอน ตำแหน่งแนวตั้ง และ heading
ที่ wrap แล้ว โดยไม่มีการแก้ค่าแบบเงียบ

## การคัดกรอง steering และ swept envelope

มุมเลี้ยวจำเป็นตาม bicycle model สำหรับ wheelbase `L` คือ:

```text
delta_required = atan(L |k|)
```

สำหรับ segment โค้ง รัศมี centerline คือ `R = 1 / |k|`, ครึ่งความกว้างรถคือ
`w/2` และระยะตามยาวจากเพลาหลังคือ:

```text
a = max(wheelbase + front_overhang, rear_overhang)
```

ขอบเขตรัศมีของวัตถุแข็งคือ:

```text
r_inside_vehicle  = max(0, R - w/2)
r_outside_vehicle = sqrt(a^2 + (R + w/2)^2)
```

รัศมี corridor ด้านใน/ด้านนอกหลังหัก uncertainty ขึ้นกับทิศทางเลี้ยว margin
เชิงรัศมีทั้งสองต้องไม่ติดลบ และมุมเลี้ยวจำเป็นต้องไม่เกินขีดจำกัดที่ประกาศ
ส่วนทางตรงใช้ margin คงที่ด้านซ้าย/ขวา

โครงสร้างนี้ตั้งใจทดสอบกรณีหักล้างสมมติฐาน: รถสามารถผ่านการตรวจความกว้าง
คงที่ แต่ไม่ผ่านเพราะมุมหน้าด้านนอกกวาดข้ามขอบเขตของโค้งแคบ

## หลักฐานและสถานะผลลัพธ์

| ผลหลักฐานหรือ geometry | สถานะ | ความหมาย |
|---|---|---|
| steering หรือขอบเขตไม่ผ่าน | `rejected` | เงื่อนไขจำเป็นด้าน geometry ไม่ผ่าน |
| ผ่านด้วยหลักฐาน `surveyed` หรือ `operator_engineering` | `admitted` | ผ่านไปยังด่านถัดไปได้เท่านั้น |
| fixture `synthetic_validation` ผ่าน | `verification_passed` | สมการ fixture ผ่าน แต่ไม่มีสิทธิ์อนุญาตสนามจริง |
| geometry โดยประมาณ/digitized ผ่าน | `indeterminate` | หลักฐานไม่เพียงพอสำหรับ admission |
| ไม่มี corridor ของสนามจริง | `indeterminate` | ขาด geometry ที่จำเป็น |

`admitted` หมายถึงผ่านเฉพาะด่าน geometry แบบลดรูปนี้ ไม่ใช่ข้ออ้างว่าได้รับ
การยืนยันทางฟิสิกส์แล้ว

## Fixture ที่ทำซ้ำได้และ validator

`config/circuits/corridor_schema_v1.json` มี fixture เชิงวิเคราะห์โปร่งใสสามชุด:
วงกลมเต็มรัศมี 20 m, โค้งแคบที่ผ่านความกว้างคงที่แต่ overhang ไม่ผ่าน และ
กรณีขีดจำกัดมุมเลี้ยวไม่ผ่าน ใช้คำสั่ง:

```powershell
python scripts/validate_corridor.py
python -m unittest tests.test_corridor -v
```

validator โหลด profile Work 008 ทั้งสิบด้วย และกำหนดให้ทุกแห่งคงสถานะ
`indeterminate` เพราะยังไม่มี corridor ที่มีหลักฐานเพียงพอสำหรับ admission

## ข้อจำกัดและหลักฐานขั้นถัดไป

- การกวาดวัตถุแข็งในระนาบไม่รวม tyre slip, compliance, yaw transient, roll,
  pitch, การเคลื่อนที่ของ suspension, การเสียรูปจาก aero, kerb, กำแพง และ
  พลวัตการชน
- grade และ bank ถูกอินทิเกรต/เก็บไว้ แต่ยังไม่เปลี่ยน swept envelope ในระนาบ
  หรือขีดความสามารถของแรง
- อินพุต piecewise-constant จะประมาณเส้นทางสำรวจได้ก็ต่อเมื่อผ่านการตรวจสอบ
  import และ discretization แยกต่างหาก
- layout จริงต้องมีข้อมูลสำรวจที่มีสิทธิ์ใช้งานหรือ engineering export จาก
  ผู้ดูแลสนาม พร้อมระบบพิกัด ขอบเขต timestamp, uncertainty และ closure audit
  ก่อนจึงจะให้ผล `admitted` ได้
- Work 011 จะเพิ่มการอิ่มตัวของแรง tyre-road และต้องไม่ตีความ Work 010 ใหม่ว่า
  เป็นหลักฐานเชิงพลวัต
