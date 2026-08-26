# ผล Work 016: Lateral/Yaw Dynamics และ Load Transfer

ต้นฉบับภาษาอังกฤษ: `2026-08-26_016_lateral-yaw-load-transfer-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 016 เสร็จสมบูรณ์ `work016-planar-v1` ให้ planar rigid-body step ระดับ
Level-0 ที่ deterministic รองรับ ground-contact layout แบบ full-rank ใดก็ได้,
project quasi-static normal load, resolve ทุก contact ผ่าน combined tyre-force
boundary จาก Work 011, advance lateral/yaw state และเก็บ force/moment residual
กับ invalid condition ที่ประกาศทั้งหมด

สมมติฐานหลักได้รับการสนับสนุนภายในขอบเขต model นี้: steering, combined-force
saturation และ load transfer ที่ขึ้นกับ acceleration สร้าง force/yaw result ที่
coupled แต่ deterministic Geometry singular, contact lift และ solver iteration
ไม่พอที่จงใจสร้างถูก reject แทนการซ่อมเงียบ

นี่เป็น internal analytical evidence ระดับ Level-0 ไม่ใช่ physical validation
หรือคำทำนาย vehicle dynamics จริง

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/lateral.py`: contact contract แบบ
  topology-neutral, normal-load projection, slip kinematics, combined-force
  coupling, fixed-point solve, planar integration, residual และ invalidity
- `src/formula_ultimate/physics/__init__.py`: export API Work 016
- `tests/test_lateral.py`: 11 tests สำหรับ steady/transient, load transfer,
  saturation, topology, replay, balance, lift, singularity, convergence และ input
- `scripts/validate_lateral.py`: validator ของ reference/falsification
- `docs/physics/LATERAL_YAW_LOAD_TRANSFER_MODEL.md` และ `.th.md`: สมการ,
  contract, evidence และ limitation ของ model
- `docs/problem_reports/2026-08-26_016_slotted-dataclass-serialization.md` และ
  `.th.md`: ปัญหา serialization ใน test/validator ที่แก้แล้ว
- queue และคู่ plan/result Work 016 สองภาษานี้

## การตัดสินใจและหลักฐาน

1. Contact topology เป็นชุดเรียงลำดับใดก็ได้ ไม่ hard-code สี่ล้อหรือสองเพลา
   Fixture แบบ delta สาม contact ผ่าน
2. Baseline load ต้องเท่ากับน้ำหนักรถและมี pitch/roll moment ศูนย์
3. Dynamic normal load ใช้ minimum-change projection deterministic
   `Fz = Fz0 + A^T(AA^T)^-1(b-AFz0)`
4. Projected load ติดลบเป็น contact lift ที่สังเกตได้และทำให้ solve invalid;
   ไม่มีการ clip normal load
5. Local contact kinematics สร้าง lateral request แบบ linear
   `-C_alpha*alpha` แล้วส่ง force ที่ขอทั้งคู่ผ่าน ellipse Work 011
6. Load transfer และ tyre capacity ปิดด้วย fixed-point iteration ที่ประกาศ
   limit, relaxation, absolute/relative tolerance และ iteration count
7. State integration เป็น explicit Euler จาก derivative ที่ start state พร้อม
   เก็บ force, yaw moment, load, convergence, saturation และ replay evidence

## ปัญหาที่พบและแก้แล้ว

การรัน Work 016 ครั้งแรกผ่าน 10 tests แต่ steady-state evidence test error เพราะ
พยายาม serialize `slots=True` dataclass ผ่าน `__dict__` Validator มีสมมติฐาน
เดียวกัน Test เปลี่ยนเป็น `dataclasses.astuple`; validator ใช้
`dataclasses.asdict` ไม่มีค่า physics หรือ solver behavior เปลี่ยน Problem report
แยกบันทึก failure, root cause, fix และการรันที่ผ่านแล้ว

## ทบทวนการทดลอง

- Independent variables: contact topology/position/load, steering, cornering
  stiffness, friction limit, longitudinal request, mass, yaw inertia, CG height,
  state, step, relaxation, iteration limit และ tolerance
- Dependent variables: projected load, slip angle, requested/applied force,
  utilization, saturation, total force/moment, acceleration, end state,
  iteration, status และ residual
- Controls: SI/sign convention, กฎ Work 011, contact order deterministic,
  control คงที่, initial state เดียว และ random draw ศูนย์
- Metrics: balance residual หกตัว, convergence iteration, ทิศ load, saturation
  count/utilization, เครื่องหมาย response และ replay equality exact
- Supporting evidence: straight equilibrium ปิดในหนึ่ง iteration โดย residual
  หกตัวศูนย์; steering บวกให้ lateral/yaw response บวก; analytical load transfer
  longitudinal/lateral มี load residual ศูนย์ exact; transient replay เท่ากัน exact
- Falsifying evidence: combined request เกิน limit saturate; case CG สูงและ
  acceleration สูงให้ raw load ติดลบและ invalid contact lift; geometry collinear
  rank ไม่พอ; iteration เดียวคืน non-convergence
- Contradicting evidence: test harness รอบแรก error แต่ไม่ได้ขัดแย้ง physical
  balance และถูกเก็บใน problem report
- Alternative explanations: test เฉพาะเครื่องหมาย response อาจผ่านแม้ magnitude
  ผิด จึงต้องมี analytical equilibrium, force/moment residual, tyre utilization
  และ replay check แยก
- Missing evidence: nonlinear tyre calibrated, roll/pitch/heave dynamics,
  suspension, aero, road geometry coupling, relaxation, temperature, wear และ
  independent/higher-fidelity validation
- Confidence: สูงสำหรับ deterministic software contract และ balance accounting
  ที่ประกาศ; ต่ำ/ไม่มีสำหรับ response รถจริงหรือ race performance

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` แบบ fail-fast

```powershell
python -m unittest tests.test_lateral -v
```

Exit status: `0`; `Ran 11 tests`; `OK`

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 121 tests`; `OK`

```powershell
python scripts/validate_lateral.py
```

Exit status: `0` ผลสำคัญ:

```text
steady: status ok, iterations 1, all six residuals 0
transient a_y: 0.6665333377777185 m/s^2
transient yaw acceleration: 0.6665333377777185 rad/s^2
transient iterations: 33; replay_equal: true
transient pitch residual: -1.8613102170661477e-09 N*m
transient roll residual: 9.311389703725581e-08 N*m
load transfer front/rear: 5486.0 / 6286.0 N
load transfer left/right: 4761.0 / 7011.0 N
load residuals: 0
combined-force saturated contacts: 3
maximum applied utilization: 1.0
one-iteration falsification: invalid, did not converge
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` ทุกคำสั่ง Full validation รันซ้ำหลัง result นี้ และตรวจ staged
scope/check ก่อน commit

## ข้อจำกัดและงานต่อ

- Load transfer เป็น quasi-static และไม่มี suspension หรือ body roll/pitch state
- Linear slip request ไม่ใช่ tyre model calibrated
- Explicit Euler response ขึ้นกับ time step
- Work 016 ไม่มี aero, braking/regen, degradation, circuit-line coupling หรือ
  race-loop integration
- Work 017 จะรับผิดชอบ aerodynamic force, balance และ cooling flow โดยยังไม่ได้
  เริ่มในงานนี้
- รายงาน commit hash ใน final handoff และไม่ push remote
