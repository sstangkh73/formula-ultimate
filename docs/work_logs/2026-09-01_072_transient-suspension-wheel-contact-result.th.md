# ผล Work 072: การเชื่อมช่วงล่าง โหลดล้อ และจุดสัมผัสแบบ Transient

สถานะ: เสร็จสมบูรณ์

ต้นฉบับภาษาอังกฤษ: `2026-09-01_072_transient-suspension-wheel-contact-result.md`

## ผลลัพธ์

Work 071 รองรับ deterministic normal-load transform แบบ optional โดยไม่เปลี่ยนผลเดิมเมื่อไม่ใช้ hook แล้ว Work 072 ใช้ hook นี้แก้สถานะ spring/damper/effective-mass ที่ระบุจาก geometry หนึ่งชุดต่อ contact ภายใน fixed point acceleration/load-transfer โหลด transient จริงเป็นตัวกำหนดขีดแรงยาง ส่วน target load, travel, velocity, boundary work, damper heat, residual, contact loss และ travel failure ถูกแสดงไว้อย่างชัดเจน

reference และตัวควบคุมผ่าน Level-0 gates ที่ประกาศไว้ ผลนี้เป็นหลักฐานความเป็นไปได้ของ coupled software ไม่ใช่ physical validation หรือความพร้อมแข่งขัน

## ไฟล์ที่เปลี่ยน

- `config/vehicle/transient_suspension_coupling_v1.json`
- `src/formula_ultimate/simulation/coupled_planar_differential.py`
- `src/formula_ultimate/simulation/transient_suspension_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_transient_suspension_coupling.py`
- `tests/test_transient_suspension_coupling.py`
- `docs/research/TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.md`
- `docs/research/TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.th.md`
- ชุด plan/result สองภาษาของ Work 072

หลักฐาน deterministic ที่ ignore โดย Git ถูกสร้างใหม่ใน `artifacts/work072/`

## การตัดสินใจและหลักฐานการทำงาน

- คง materialized architecture v3 จาก Work 069 ที่ SHA-256 `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`
- derive effective mass ต่อ contact จาก ground component: จุดขับเคลื่อน `13.30024665823775 kg`; ตัวรองรับหลังแบบ passive `4.342937684322531 kg`
- ใช้ implicit-midpoint oscillator และส่ง actual midpoint spring/damper load เข้า Work 071 tyre calculation ภายใน fixed point เดียวกัน
- แสดง boundary work จากโหมดแนวดิ่ง sprung-body ที่ยังไม่ได้จำลอง แทนการโยนพลังงานเข้า drivetrain แบบเงียบ
- หักพลังงาน initial suspension perturbation จาก storage เพื่อคงงบเริ่มต้น `50,000,000 J`
- โหลดจริง `<= 0 N` เป็น `contact_loss` แบบไม่ commit ส่วน over-travel ถูกเก็บเป็น `suspension_travel` ที่ขอบ step ไม่มี load/travel clipping
- รักษา result SHA-256 ของ Work 071 เมื่อไม่ใช้ transform ที่ `f8f3d888b23a9e21b7bb9ad8b7153ecd5bd4752c7937ebf8cc42a952b64c9cdd`

## ผลการทดลอง

คำสั่ง reference: มุมเลี้ยว `+0.01 rad`, throttle `0.3`, ระยะเวลา `0.5 s`, `dt = 0.001 s`

- สถานะ/ผลลัพธ์: `passed/finished`, 500 steps
- ตำแหน่งสุดท้าย: `(5.369677667803904, 0.13391224133502547) m`
- yaw rate สุดท้าย: `0.3637589747733689 rad/s`
- ช่วง actual load: `282.92044294869817` ถึง `1597.6137536723597 N`
- ความต่าง target/actual load สูงสุด: `96.89914047704144 N`
- travel/ความเร็วแนวดิ่งสูงสุด: `0.011753827694854656 m`, `0.19365997408307992 m/s`
- boundary work/damper heat: `4.606168739325264 J`, `0.9238099457339569 J`
- force residual สูงสุด: `3.979039320256561e-13 N`
- suspension-energy residual สูงสุด: `8.296586074402201e-16 J`
- total global relative energy residual สูงสุด: `5.010984838008881e-9`
- ความต่าง half-step แบบสัมพัทธ์สูงสุด: `0.008650825751444935` ต่ำกว่า `0.02`

มุมเลี้ยวศูนย์สมมาตรพอดี การเลี้ยวตรงข้ามสลับสถานะแนวดิ่งซ้าย/ขวาและ mirror สถานะระนาบ/yaw ที่เลือกโดย mismatch เป็นศูนย์ Zero damping ให้ damper heat เป็นศูนย์พอดี stiffness ครึ่งหนึ่งเพิ่ม travel สูงสุดเป็น `0.02332339540361481 m`

ตัวควบคุม contact loss เก็บค่า `-329.1330469175954 N` และคืน `DNF: contact_loss` ที่ attempted step 1 โดยไม่ commit transaction ตัวควบคุม travel เก็บ `0.05068991458357319 m` และคืน `DNF: suspension_travel` หลัง step 2 ทั้งสองกรณีคงพลังงานรวมเริ่มต้น `50,000,000 J` พอดี

ไฟล์ evidence primary/replay ตรงกันทุกไบต์ File SHA-256 คือ `E48CA5034D8361C5E45AAF2D88BA5FC1349015AAD4144345CB5CBFD2AE66B719` และ canonical evidence payload SHA-256 คือ `25b269082eb921efc54c334c6dc3d9623bcb7d6fa91beb9d2ea9b4083270b97b`

## บันทึกการตรวจสอบ

```text
python -m unittest tests.test_transient_suspension_coupling -v
Exit: 0
Ran 11 tests in 19.231s — OK

python scripts/experiments/run_transient_suspension_coupling.py --config config/vehicle/transient_suspension_coupling_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work072/materialized_architecture_v3.json --output artifacts/work072/experiment_evidence.json
Exit: 0
status=passed; evidence_sha256=25b269082eb921efc54c334c6dc3d9623bcb7d6fa91beb9d2ea9b4083270b97b

python scripts/experiments/run_transient_suspension_coupling.py --config config/vehicle/transient_suspension_coupling_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work072/replay/materialized_architecture_v3.json --output artifacts/work072/replay/experiment_evidence.json
Exit: 0
primary SHA-256 = replay SHA-256 = E48CA5034D8361C5E45AAF2D88BA5FC1349015AAD4144345CB5CBFD2AE66B719

python -m unittest discover -s tests -v
Exit: 0
Ran 442 tests in 84.210s — OK

python -m compileall -q src scripts/experiments/run_transient_suspension_coupling.py tests/test_transient_suspension_coupling.py
Exit: 0

python -m unittest tests.test_transient_suspension_coupling tests.test_coupled_planar_differential -q
Exit: 0
Ran 21 tests in 40.284s — OK
```

ผล bilingual repository contract, staged-diff check, commit และ post-commit replay ขั้นสุดท้ายจะรายงานใน final handoff หลังทำคำสั่งเสร็จ

## ข้อจำกัดและงานถัดไป

แบบจำลองนี้ยังไม่มี sprung-body heave/pitch/roll inertia, tyre vertical compliance, road displacement, linkage geometry, motion ratio, roll centre, anti-dive/squat, bump stop, hysteresis, coefficient ที่วัดจริง, aero load และ exact sub-step event localization Geometry ให้ identity และ component mass แต่ยังไม่ได้ให้พฤติกรรม spring/damper การปิดพลังงานภายในไม่ได้แสดงความแม่นยำต่อโลกจริง

งานถัดไปควรแก้โหมดแนวดิ่งของ sprung body และ road/tyre compliance ก่อน หรือใช้เป็น prerequisite ของ closed-loop path และ circuit gate
