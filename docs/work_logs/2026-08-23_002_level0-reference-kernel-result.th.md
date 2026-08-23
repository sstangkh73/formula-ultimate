# ผลงาน 002: Level-0 Longitudinal Reference Kernel

วันที่: 2026-08-23
สถานะ: เสร็จสมบูรณ์

> ฉบับภาษาไทยของ `2026-08-23_002_level0-reference-kernel-result.md`

## สรุป

Implement physics reference kernel หนึ่งมิติแบบ deterministic ตัวแรกของ
Formula Ultimate ระบบจำลอง forward point-mass motion ภายใต้ constant tractive
force, aerodynamic drag, rolling resistance และ constant road grade
Implementation เปิดเผย immutable state, per-step force telemetry, explicit
input failure, partial final timestep และ impulse ที่เกิดจาก forward-only
zero-speed constraint

Physics plan ให้สิทธิ์ agent ในอนาคต generate geometry ของ component 3D จริง
โดยต้องผ่าน trusted geometry/property/solver gate ก่อน component จะมีผลต่อ 1D
หรือ race fitness

## การเปลี่ยนแปลง

### Physics implementation

- เพิ่ม `src/formula_ultimate/physics/longitudinal.py`
- เพิ่ม validated SI-unit parameter record สำหรับ vehicle, environment และ
  integration configuration
- เพิ่ม immutable state, result และ per-step telemetry record
- เพิ่ม analytical drag, grade และ rolling-resistance force function
- เพิ่ม fixed-step/partial-step longitudinal integration
- เพิ่มการคำนวณจุดหยุดภายใน step และ zero-speed constraint impulse อย่างชัดเจน
  แทนการปล่อยให้ถอยหรือซ่อน boundary
- เพิ่ม input error และ numerical error แยกชนิด

### Validation

- เพิ่ม `tests/test_longitudinal.py` พร้อม physics test แปดข้อ
- ขยาย repository contract ให้ plan ที่มีสถานะ `Completed` ทุกไฟล์ต้องมี result
  record คู่กัน ส่วน plan ที่กำลังทำยัง valid
- แก้ GitHub Actions ให้ install package ก่อนรัน test suite

### เอกสารวิจัย

- แก้ `docs/PHYSICS_SYSTEM_PLAN.md` เพิ่ม pipeline geometry ของ component ที่
  agent ออกแบบและ 3D promotion gate
- แก้ `README.md` ให้แยก analytical reference kernel ออกจาก race-car simulator
  ที่ผ่าน validation

## การตัดสินใจด้าน Model

1. Kernel อนุญาตเฉพาะการเคลื่อนที่หนึ่งมิติไปข้างหน้า
2. Tractive force ถูก command จากภายนอก ไม่ได้สื่อพฤติกรรม drivetrain
3. ประเมิน force ที่ต้น timestep แต่ละช่วง
4. Velocity ใช้ constant-acceleration integration ภายใน step และ position ใช้
   average velocity
5. ย่อ final timestep เพื่อจบตรง duration ที่ขอ
6. Step ที่กำลังข้ามไปสู่ reverse จะ integrate ถึง stopping time และบันทึก
   unilateral-constraint impulse ในเวลาที่เหลือ
7. Agent-generated 3D component self-report mass, strength, cooling หรือ
   efficiency ไม่ได้ Trusted extraction และ multi-fidelity solver ต้องสร้าง
   property เหล่านั้นจาก immutable geometry/material artifact

## หลักฐาน Validation

### การติดตั้ง Environment

คำสั่ง:

```powershell
python -m pip install -e .
```

Environment: Windows, Python 3.14.3

Exit code: `0`

ผล: build และ install editable package `formula-ultimate-0.0.1` สำเร็จ

### Test suite ทั้งหมด

คำสั่ง:

```powershell
python -m unittest discover -s tests -v
```

Environment: Windows, Python 3.14.3

Exit code: `0`

ผล:

```text
8 longitudinal physics tests ... ok
5 repository contract tests ... ok

Ran 13 tests
OK
```

Physics case ครอบคลุม:

- zero-input rest
- constant-force analytical acceleration
- drag-only coast-down convergence
- grade equilibrium
- rolling-resistance analytical deceleration
- stop-without-reverse และ constraint impulse
- deterministic replay
- invalid/non-finite input rejection

### ค่า Analytical Reference

คำสั่ง: เรียก committed public API สำหรับกรณี lossless constant-force 1,000 kg
และ drag-only coast-down

Exit code: `0`

ผล:

```text
constant_force: t=5.000000000000 s
                x=25.000000000000 m
                v=10.000000000000 m/s

drag_exact:     26.155187445510 m/s
dt=0.50 result: 26.131992459120 m/s  error=0.023194986390 m/s
dt=0.05 result: 26.152886710667 m/s  error=0.002300734843 m/s
fine/coarse error ratio: 0.099191
```

การลด timestep 10 เท่าลด drag-reference speed error ที่วัดได้เหลือประมาณ
9.92% ของ coarse error ในกรณีนี้

### Compilation และ Pre-commit Gate

คำสั่ง:

```powershell
python -m compileall -q src tests
git diff --cached --check
```

Final exit code ที่คาดของแต่ละคำสั่ง: `0`

รันคำสั่งซ้ำหลัง stage result record นี้ จากนั้น GitHub Actions รัน test suite
ทั้งหมดอย่างอิสระบน Python 3.11 หลัง push

## หลักฐานที่สนับสนุนข้ออ้างเป้าหมาย

- Constant-force motion ตรงกับ closed-form solution ภายใน floating-point
  tolerance ที่ assert
- Grade equilibrium และ constant rolling deceleration ตรง analytical reference
- Drag-only error ลดลงอย่างชัดเจนเมื่อปรับ timestep ละเอียดขึ้น
- Input เดียวกันให้ immutable result record ที่เท่ากันทุกค่า
- Invalid parameter fail ก่อนเข้า simulation

## หลักฐานที่ขัดแย้งหรือยังขาด

- ยังไม่มี energy-conservation audit
- Drag integration ยังเป็น explicit และ first-order สำหรับ force ที่เปลี่ยน
- Rolling resistance เป็น declared envelope ไม่ใช่ detailed tyre model
- ยังไม่มี component, powertrain, thermal, topology, lap หรือ race model
- ยังไม่มี Level-1 หรือ empirical cross-validation
- ยังไม่ได้ generate หรือ evaluate 3D geometry

## คำอธิบายทางเลือก

- การผ่าน analytical case แสดงความถูกต้องเฉพาะภายในสมการที่ทดสอบ ไม่ได้แสดง
  race prediction accuracy
- Deterministic replay อาจเกิดร่วมกับ model ที่ bias คงที่ได้
- Timestep convergence ไปหา drag case เดียวไม่ได้พิสูจน์ว่า force/controller
  combination ในอนาคตทุกแบบ converge เพียงพอ

## ระดับความมั่นใจ

- มั่นใจสูงใน constant-force, grade และ rolling analytical reference behavior
  ที่ทดสอบ
- มั่นใจปานกลางใน bounded drag-only integration behavior จนกว่าจะมี convergence
  matrix ที่กว้างขึ้น
- มั่นใจต่ำมากสำหรับการทำนายรถจริง เพราะยังไม่มี component, tyre, thermal และ
  validation layer ที่จำเป็น

## สิ่งที่เบี่ยงเบนจากแผน

- แก้ GitHub Actions และ repository-contract test เพราะ source package ใหม่
  ต้อง install และ completed plan ต้องบังคับ result record แบบสมมาตร
- เพิ่ม zero-speed constraint impulse telemetry ระหว่าง review เพื่อไม่ซ่อน
  ผลของ forward-only boundary ต่อ force/velocity

## งานถัดไปที่แนะนำ

Work Plan 003 ควรเพิ่ม energy/work audit รอบ reference kernel ก่อน implement
motor หรือ battery Audit ควรเปรียบเทียบ tractive work, kinetic-energy change,
road-load work, grade potential-energy change และ zero-speed constraint
contribution ภายใต้ timestep refinement
