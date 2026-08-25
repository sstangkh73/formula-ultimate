# แผน Work 011: Saturation ของแรงรวม Tyre-Road

ต้นฉบับภาษาอังกฤษ: `2026-08-26_011_tyre-road-saturation-plan.md`

สถานะ: Completed

## วัตถุประสงค์

Implement กฎ contact tyre-road ระดับ Level-0 ที่ทำซ้ำได้ รับแรง longitudinal
และ lateral ที่ร้องขอ ใช้ friction circle หรือ ellipse ที่ตรวจสอบได้ และแสดง
ทั้งแรงที่ร้องขอ แรงที่ใช้จริง utilization, saturation scale, residual,
normal load และเหตุผลที่จำกัด

## ขอบเขต

- กำหนด contract SI แบบเข้มงวดสำหรับพารามิเตอร์ contact, force request และ
  force result
- รองรับ friction circle แบบ isotropic และ friction ellipse แบบ anisotropic
  ผ่านสัมประสิทธิ์แรงเสียดทาน longitudinal/lateral ที่แยกกัน
- ฉาย request ที่เกินขอบเขตแบบ radial ลงบน ellipse ที่ normalize แล้ว โดยไม่
  เขียนทับแรงที่ร้องขอแบบเงียบ
- ถือว่า normal load ศูนย์เป็นสถานะ no-contact ที่สังเกตได้แยกต่างหาก
- รักษา symmetry ที่ทำซ้ำได้ในทุก quadrant ของแรง
- เพิ่ม test สำหรับ analytical boundary, saturated, unsaturated, zero-load,
  invalid-input, monotonicity และ replay
- เพิ่ม validator และเอกสาร model/result สองภาษา
- Validate และ commit Work 011 แยกก่อนเริ่ม Work 012

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/tyre.py`
- `src/formula_ultimate/physics/__init__.py`
- `scripts/validate_tyre.py`
- `tests/test_tyre.py`
- `docs/physics/TYRE_ROAD_MODEL.md`
- `docs/physics/TYRE_ROAD_MODEL.th.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.th.md`
- คู่ plan/result Work 011 ภาษาอังกฤษและไทยนี้
- รายงานปัญหาแยกสองภาษาเฉพาะเมื่อพบปัญหาที่มีสาระ

## ขอบเขตโมเดลและสมการ

สำหรับ normal load `Fz >= 0`, สัมประสิทธิ์ longitudinal `mu_x > 0`,
สัมประสิทธิ์ lateral `mu_y > 0` และ request `(Fx_req, Fy_req)` กำหนดแกน:

```text
Fx_limit = mu_x Fz
Fy_limit = mu_y Fz
q = (Fx_req / Fx_limit)^2 + (Fy_req / Fy_limit)^2
```

เมื่อ `Fz > 0` request ที่ `q <= 1` ผ่านโดยไม่เปลี่ยน ส่วน request ที่ `q > 1`
ได้รับ scale `1 / sqrt(q)` บนทั้งสอง component requested utilization คือ
`sqrt(q)` และ applied utilization ต้องไม่เกินหนึ่ง ยกเว้น tolerance floating
point ที่ประกาศ เมื่อ `Fz = 0` zero request ให้ `no_contact_zero_request` ส่วน
request ไม่เป็นศูนย์ให้ applied force ศูนย์พร้อมเหตุผล `no_normal_load` และไม่มี
utilization เชิงตัวเลขที่ไม่ถูกนิยาม

นี่คือขอบเขตความสามารถของแรง ไม่ใช่กราฟ tyre เทียบ slip ratio/angle จึงไม่
สามารถทำนาย relaxation, transient, ความร้อน, การสึก, ความต่างผิวทาง,
aquaplaning, camber, aligning torque หรือ optimum slip

## นิยามการทดลอง

### สมมติฐานที่ต้องการทดสอบ

ขอบเขตแรงรวมป้องกันไม่ให้ agent ใช้ grip longitudinal และ lateral เต็มพร้อมกัน
ที่ contact patch เดียว โดยยังเก็บหลักฐานตรงกับแรงที่ design ร้องขอ

### Independent variables

- แรง longitudinal และ lateral ที่ร้องขอ
- normal load
- สัมประสิทธิ์แรงเสียดทาน longitudinal และ lateral

### Dependent variables

- requested/applied utilization
- saturation scale และ boolean
- applied force และ force residual
- contact status/reason

### Controls

- หน่วย SI และ sign convention คงที่
- radial projection ใน normalized force space
- ไม่มีความสุ่มเชิงตัวเลข
- ใช้ coefficient และ normal load เดียวกันสำหรับ request ที่เปรียบเทียบ

### เกณฑ์หักล้างและความล้มเหลว

- request ที่อยู่บน ellipse พอดีต้องไม่เปลี่ยนและไม่ saturated
- diagonal request นอก friction circle ต้องถูก scale ไปยังขอบ analytical ไม่ใช่
  clip แต่ละแกนแยกกัน
- เมื่อ request/coefficient คงที่ การเพิ่ม normal load เพียงอย่างเดียวต้องไม่ทำให้
  requested utilization เพิ่ม
- load, coefficient หรือ request ที่ติดลบ/non-finite ถูกปฏิเสธในกรณีที่ invalid;
  signed force request ที่ finite ยังใช้ได้
- normal load ศูนย์ส่งแรงไม่เป็นศูนย์ไม่ได้และต้องไม่สร้าง NaN
- input เหมือนกันต้อง replay ได้ผลเหมือนกัน

## Validation

```powershell
python -m unittest tests.test_tyre -v
python -m unittest discover -s tests -v
python scripts/validate_tyre.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

คำสั่งจะใช้ fail-fast exit handling

## เกณฑ์สำเร็จ

- analytical reference ของ circle และ ellipse ผ่าน
- applied utilization อยู่ภายในขอบเขตที่ประกาศ
- เห็น requested force, applied force, residual, saturation และ no-contact state
- tests ทั้งหมด, validator, compilation, contract Markdown สองภาษา,
  whitespace, staged scope แบบระบุ, commit และ post-commit verification ผ่าน

## ความเสี่ยง

- friction ellipse เรียบง่ายกว่า physical tyre curve โดยตั้งใจ และอาจทำให้
  มั่นใจผิดหากไม่แสดงขอบเขตโมเดล
- ความเท่ากันแบบ floating-point ที่ boundary ต้องมี tolerance เชิงตัวเลขที่
  บันทึกไว้ พร้อมเก็บ utilization ดิบ
- contact patch เดียวไม่สามารถกำหนด axle load transfer หรือ vehicle yaw

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มีการ calibrate Pacejka/Fiala หรืออ้างอิงเชิง empirical เกี่ยวกับ tyre
- ไม่มี slip ratio, slip angle, aligning torque, load transfer, thermal, wear,
  wet-surface หรือ aquaplaning physics
- ยังไม่ integrate โดยตรงกับ lap-time/race loop ใน work item นี้
- ไม่เริ่ม Work 012 energy graph ก่อน commit Work 011
- ไม่ push remote
