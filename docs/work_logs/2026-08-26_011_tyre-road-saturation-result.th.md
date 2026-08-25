# ผลลัพธ์ Work 011: Saturation ของแรงรวม Tyre-Road

ต้นฉบับภาษาอังกฤษ: `2026-08-26_011_tyre-road-saturation-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 011 เสร็จสมบูรณ์ friction circle/ellipse สำหรับ contact patch เดียวที่
ทำซ้ำได้เก็บแรง longitudinal/lateral ที่ร้องขอแยกจากแรงที่ใช้จริง residual,
utilization, saturation scale และสถานะ

หลักฐานสนับสนุนสมมติฐาน: request `(3000, 4000) N` เทียบกับ capacity isotropic
`4000 N` มี utilization `1.25` และถูก scale แบบ radial ด้วย `0.8` เป็น
`(2400, 3200) N` วิธีนี้ป้องกันการใช้ grip เต็มแยกแกนพร้อมกันโดยไม่ซ่อน request
ที่เป็นไปไม่ได้ของ agent

นี่คือกฎ capacity ระดับ Level-0 ไม่ใช่โมเดล tyre ที่ calibrate ตาม slip หรือ
ข้ออ้างว่าได้รับการยืนยันทางฟิสิกส์

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/tyre.py`: input contract, result telemetry,
  friction ellipse, สถานะ zero-load และ numerical failure ที่สังเกตได้
- `src/formula_ultimate/physics/__init__.py`: export API tyre สาธารณะ
- `tests/test_tyre.py`: test 11 รายการสำหรับ analytical, symmetry,
  monotonicity, tolerance, zero-load, invalid-input, numerical-failure และ replay
- `scripts/validate_tyre.py`: reference circle, ellipse และ zero-load ที่ทำซ้ำได้
- `docs/physics/TYRE_ROAD_MODEL.md` และ `.th.md`: สมการ ความหมายสถานะ
  numerical behavior, ข้อจำกัด และงานต่อเนื่อง
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` และ `.th.md`: สถานะ Work 011
- คู่ plan/result Work 011 ภาษาอังกฤษและไทยนี้

## การตัดสินใจและพฤติกรรมที่สังเกตได้

1. แกน capacity longitudinal/lateral คือ `mu_x Fz` และ `mu_y Fz`
2. Utilization คือรัศมี Euclidean ใน normalized force space Request ที่เกินขอบ
   ได้ scale ร่วมหนึ่งค่า `1 / utilization` จึงรักษาทิศทาง
3. Request ภายใน `1 + boundary_tolerance` ผ่านโดยไม่เปลี่ยน ค่าเริ่มต้น
   tolerance คือ `1e-12` และต้องไม่เกิน `1e-6`
4. Component ของ requested, applied และ residual force แสดงแยกกัน
5. Load ศูนย์กับ request ศูนย์เป็น `no_contact_zero_request` Load ศูนย์กับ
   request ไม่เป็นศูนย์เป็น `no_normal_load` ใช้แรงจริงศูนย์ เก็บ request ทั้งหมด
   เป็น residual และใช้ `None` สำหรับ requested utilization ที่ไม่ถูกนิยาม
6. Input invalid ให้ `TyreInputError` ส่วน underflow/overflow ของ capacity axis
   แบบ floating-point ให้ `TyreNumericalError` โดยไม่สร้างผลแรงแบบเงียบ

## การทบทวนการทดลอง

- Independent variables: แรงที่ร้องขอ normal load และสัมประสิทธิ์แรงเสียดทาน
  longitudinal/lateral
- Dependent variables: utilization, scale, แรงใช้จริง, residual, saturation
  และสถานะ
- Controls: convention SI/sign, normalized radial projection, ไม่มีความสุ่ม
  และพารามิเตอร์เดียวกันสำหรับกรณีที่เปรียบเทียบ
- หลักฐานสนับสนุน: reference circle exact ให้ scale `0.8` และ applied
  utilization `1.0`; ขอบ ellipse anisotropic ไม่เปลี่ยน; force quadrant ทั้งหมด
  รักษาเครื่องหมาย/ทิศทาง
- หลักฐานหักล้างที่ทดลอง: ความเป็นไปได้แยกแกนไม่สามารถอนุญาต combined force
  diagonal; load ศูนย์ส่งแรงไม่ได้; capacity underflow เป็น numerical error ชัดเจน
- คำอธิบายทางเลือกที่ตัดออก: output ไม่ใช่การ clip แยกแกน เพราะ component ทั้ง
  สองได้รับ analytical scale เดียวกัน
- หลักฐานที่ยังขาด: coefficient/curve tyre จากการวัด, slip behavior, load
  sensitivity, temperature, wear, wet track และ transient response
- ความมั่นใจ: สูงสำหรับสมการ ellipse และพฤติกรรมซอฟต์แวร์ที่ประกาศ; ไม่มี
  ความมั่นใจต่อสมรรถนะ tyre จริงจนกว่าจะมีหลักฐาน calibration

## ปัญหาที่พบ

ไม่พบปัญหาที่มีสาระซึ่งต้องสร้าง problem report แยก singularity เมื่อ zero-load
และ underflow ของ capacity แบบ floating-point ถูกคาดไว้ใน plan/model boundary
และ implement เป็นสถานะ/error ชัดเจนพร้อม test

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` พร้อม fail-fast exit handling

### Tests เฉพาะงาน

```powershell
python -m unittest tests.test_tyre -v
```

Exit status: `0` ผลสำคัญ: `Ran 11 tests`; `OK`

### Tests ทั้ง repository

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0` ผลสำคัญ: `Ran 68 tests`; `OK`

### Validator

```powershell
python scripts/validate_tyre.py
```

Exit status: `0` ผลสำคัญ:

```text
outside circle: status=saturated, utilization=1.25, scale=0.8
outside circle applied force: [2400.0, 3200.0] N
inside ellipse: status=within_limit, utilization=0.7071067811865476
zero normal load: status=no_normal_load, scale=0.0
```

### Compilation และ whitespace

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` ทุกคำสั่ง โดยรัน staged check หลัง stage แบบระบุขอบเขตและก่อน
commit อีกครั้ง

## ข้อจำกัดและงานต่อเนื่อง

- กฎนี้ไม่มี slip curve, relaxation, torque, thermal, wear, surface หรือ
  wet-weather physics
- coefficient เป็น input ไม่ใช่ข้ออ้างจากการวัด
- Normal-load transfer และ yaw อยู่นอก work item นี้
- Work 012 เชื่อม applied longitudinal force กับ typed energy graph ได้เฉพาะ
  ผ่าน contract power, velocity, direction และ efficiency ที่ชัดเจน
