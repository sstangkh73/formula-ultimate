# แผน Work 016: Lateral/Yaw Dynamics และ Load Transfer

ต้นฉบับภาษาอังกฤษ: `2026-08-26_016_lateral-yaw-load-transfer-plan.md`

สถานะ: Completed

## วัตถุประสงค์

สร้าง planar rigid-body model ระดับ Level-0 ที่ deterministic โดย coupling
lateral/yaw dynamics, quasi-static longitudinal/lateral load transfer และ
combined tyre-force saturation จาก Work 011 พร้อมทำให้หลักฐาน force, moment,
load, convergence และ invalid state สังเกตได้

## ขอบเขต

- กำหนด contract SI เข้มงวดสำหรับ ground contact patch จำนวนใดก็ได้ โดยไม่
  บังคับ topology แบบรถสี่ล้อหรือสองเพลา
- แทน contact แต่ละจุดด้วยตำแหน่ง body frame, steer angle, cornering stiffness,
  friction parameter, longitudinal force ที่ขอ และ baseline normal load
- คำนวณ contact slip kinematics จาก body longitudinal/lateral velocity และ yaw
  rate แล้วขอ lateral force ด้วย linear slip-angle law ที่ประกาศ
- ส่งคู่ longitudinal/lateral force ที่ขอทุกคู่ผ่าน combined-force saturation
  ของ Work 011 และแสดง requested, applied, utilization และ saturation state
- แก้ normal load แบบ quasi-static จาก vertical, pitch และ roll equilibrium
  ด้วย minimum-change projection จาก baseline load แบบ deterministic แสดง
  residual และ reject contact lift แทนการ clip
- Iterate load transfer ที่ขึ้นกับ force ด้วย limit คงที่ deterministic และ
  แสดงผล convergence ชัดเจน
- Advance planar body velocity, yaw rate, heading และ position ด้วย integration
  semantics ที่ประกาศ พร้อมแสดง force/moment balance residual
- Test layout contact ที่ไม่ conventional, steady straight equilibrium,
  steering transient, saturation, longitudinal/lateral load transfer, replay
  exact, non-convergence, singular layout, contact lift และ numerical input
  invalid
- เพิ่ม validator, เอกสาร model/result สองภาษา, validation evidence และ commit
  แยก โดยไม่เริ่ม Work 017

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/lateral.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_lateral.py`
- `scripts/validate_lateral.py`
- `docs/physics/LATERAL_YAW_LOAD_TRANSFER_MODEL.md` และ `.th.md`
- สถานะ queue และคู่ plan/result สองภาษานี้
- problem report แยกสองภาษาเฉพาะเมื่อพบปัญหาที่มีสาระ

## ขอบเขตฟิสิกส์

รถเป็น planar rigid body หนึ่งก้อน มี body-frame velocity `(u, v)`, yaw rate
`r`, mass `m`, yaw inertia `I_z` และความสูง centre of mass `h` สำหรับ contact
ตำแหน่ง `(x_i, y_i)` และ steer angle `delta_i` ความเร็ว contact จะถูก rotate
เข้า local tyre frame Lateral force ที่ขอคือ:

```text
alpha_i = atan2(v_local_y, max(abs(v_local_x), v_regularization))
Fy_requested_i = -C_alpha_i * alpha_i
```

จากนั้นคู่ `(Fx_requested_i, Fy_requested_i)` ถูก resolve ด้วย friction
circle/ellipse ของ Work 011 ที่ normal load ปัจจุบัน

Normal load ต้องผ่าน quasi-static constraint ที่ประกาศ:

```text
sum(Fz_i)       = m * g
sum(x_i Fz_i)   = -m * a_x * h
sum(y_i Fz_i)   = -m * a_y * h
```

Solver เลือกผลเฉพาะที่เปลี่ยนจาก baseline load น้อยที่สุดใน Euclidean norm
ภายใต้ constraint เหล่านี้ Layout ที่ rank ไม่พอ, normal load ติดลบ, state
ไม่ finite หรือ fixed-point ไม่ converge ต้องเป็น invalid ที่สังเกตได้ ห้าม
clip หรือซ่อมอย่างเงียบ ๆ

สมดุล planar force และ yaw moment คือ:

```text
m * (du/dt - r*v) = sum(Fx_body_i)
m * (dv/dt + r*u) = sum(Fy_body_i)
I_z * dr/dt       = sum(x_i*Fy_body_i - y_i*Fx_body_i)
```

## นิยามการทดลอง

- สมมติฐานหลัก: load transfer และ yaw dynamics ที่ชัดเจนเปลี่ยน combined tyre
  force ที่ใช้ได้แบบ deterministic และปิด balance ได้ คำขอ force ที่ละเลย
  coupling ต้องถูกหักล้างได้ด้วย saturation, lift, convergence หรือ residual
- Independent variables: contact topology/position, baseline load, steering,
  cornering stiffness, friction limit, longitudinal request, mass, yaw inertia,
  centre-of-mass height, state, time step และ solver tolerance
- Dependent variables: normal load, slip angle, requested/applied contact force,
  utilization, body force/moment, acceleration, state, convergence, iteration,
  residual และ validity
- Controls: SI/sign convention, Work 011 saturation law, contact order
  deterministic, solver limit/tolerance คงที่, initial state เดียว และไม่มี
  random draw
- Metrics: vertical/pitch/roll residual, longitudinal/lateral/yaw balance
  residual, solver iteration, replay equality, saturation count และ state
  response
- Success: steady zero-slip converge; steering transient ให้เครื่องหมาย lateral
  และ yaw ตามคาด; ทิศ load transfer และ balance ที่ประกาศผ่าน analytical check;
  replay exact และ repository gate ผ่าน
- Failure criteria: contact geometry singular, contact lift, non-convergence,
  arithmetic ไม่ finite หรือ residual เกิน tolerance ต้อง invalid
- Falsification: บังคับ combined request เกิน limit, case CG สูงจน contact lift,
  layout rank ไม่พอ และ iteration budget ไม่พอ โดยห้าม accept อย่างเงียบ ๆ

## ความเสี่ยง

- Planar rigid body ไม่มี heave, pitch/roll rate, suspension travel, compliance,
  camber, relaxation length, tyre temperature และ aero load
- Linear cornering stiffness เป็น request law ระดับ Level-0 ไม่ใช่ calibrated
  tyre model; Work 011 เพียงจำกัด force ที่ได้
- Quasi-static load transfer สมมติ vertical equilibrium ทันทีและอาจให้ response
  สูงเกินจริงใน transient เร็ว
- Explicit integration deterministic แต่ขึ้นกับ step size; residual พิสูจน์
  internal accounting ไม่ใช่ความแม่นยำโลกจริง

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่บังคับ wheel count/layout แบบดั้งเดิม และไม่อ้างว่า model นี้ครอบคลุม
  locomotion architecture แบบเปิดทั้งหมด
- ไม่มี aerodynamic, suspension, braking-system, regenerative, degradation,
  traffic, weather, strategy, lap-time, safety หรือ physical-validation claim
- ไม่ทำ Work 017 และไม่ push remote

## Validation

```powershell
python -m unittest tests.test_lateral -v
python -m unittest discover -s tests -v
python scripts/validate_lateral.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

ทุก gate รัน fail-fast การเสร็จต้องมี result สองภาษา, staged scope ที่ระบุ,
commit สำเร็จ และหลักฐาน clean-state/hash หลัง commit
