# แผน Work 071: การเชื่อมพลวัตระนาบ Differential และ Load Transfer ต่อ Step

สถานะ: เสร็จสมบูรณ์ (Completed)

เอกสารต้นฉบับภาษาอังกฤษ: `2026-08-31_071_coupled-planar-differential-load-transfer-plan.md`

## วัตถุประสงค์และขอบเขต

เชื่อมสถานะล้อขับเคลื่อนอิสระ/differential จาก Work 070 เข้ากับการเลี้ยวระนาบสามจุดสัมผัสและ load-transfer ที่ derive จาก geometry ของ Work 069 ในแต่ละ time step ต้องแก้ contact normal loads, longitudinal wheel slip, lateral slip angle, combined-force capacity, powertrain load, differential modal motion, การเคลื่อนที่รถ และ yaw เป็น transaction fixed-point เดียวแบบ deterministic

งานนี้เป็นการกระจายโหลดกึ่งสถิตตามความเร่งในแต่ละ step ไม่ใช่ suspension transient ที่ resolve แล้ว และเป็น coupled admission gate ระดับ Level 0 บน geometry Work 069 เดิม ต้องคง energy/branch-limit contracts ทั้งหมดจาก Work 070 พร้อมเพิ่ม body lateral/yaw energy และ lateral-slip dissipation

## การเชื่อมฟิสิกส์

ที่แต่ละ contact ซึ่งมีตำแหน่ง body-frame `(x_i, y_i)`, มุมเลี้ยว `delta_i`, body velocities `(u, v)` และ yaw rate `r`:

```text
v_x_body_i = u - r y_i
v_y_body_i = v + r x_i
v_x_local_i = cos(delta_i) v_x_body_i + sin(delta_i) v_y_body_i
v_y_local_i = -sin(delta_i) v_x_body_i + cos(delta_i) v_y_body_i
alpha_i = atan2(v_y_local_i, max(abs(v_x_local_i), v_regularization)).
```

longitudinal request ของจุดขับเคลื่อนมาจากความเร็วล้อ Work 070 แต่ละข้างและ slip capacity ที่ขึ้นกับ normal load ส่วน lateral request คือ `-C_alpha alpha_i` ทั้งสองถูก project พร้อมกันบน friction ellipse ที่ประกาศ และ saturation ยังสังเกตได้

normal loads ต่อ step ต้องเป็นไปตาม:

```text
sum(N_i) = m g
sum(x_i N_i) = -m a_x h
sum(y_i N_i) = -m a_y h.
```

fixed-point loop ต้องรวม aerodynamic drag, rolling resistance, powertrain load availability, combined-force projection และ load transfer แรงปกติติดลบเป็น terminal contact lift และไม่ถูก clip

Differential ยังคงใช้:

```text
omega_L = omega_c - delta_omega
omega_R = omega_c + delta_omega
J_delta d(delta_omega)/dt = q_L - q_R - c_delta delta_omega.
```

บัญชีพลังงานเพิ่ม planar body kinetic energy `0.5 m(u^2+v^2)`, yaw energy `0.5 I_z r^2`, lateral-slip heat `-F_y v_y dt`, longitudinal slip heat, branch-connection heat, differential heat, aerodynamic work และ rolling work โดย body integration error กับ global conservation residual ยังคงเป็น output ชัดเจน

## การออกแบบการทดลอง

- ตัวแปรอิสระ: เครื่องหมาย/ขนาดมุมเลี้ยว, throttle, ความเร็วเริ่มต้น, step size, friction ซ้าย/ขวา, cornering stiffness, differential damping, จุดศูนย์กลางมวล/inertia/contact locations จาก geometry และ force limits
- ตัวแปรตาม: trajectory, heading, body velocities, yaw rate, carrier/branch speeds, differential modal energy, normal load/slip/forces/utilization ต่อ contact, saturation, body work, heat ทุกส่วน, equilibrium/interface/body/global residuals, contact lift, subsystem state และ replay hash
- controls: zero steer, steer บวก/ลบขนาดเท่ากัน, split grip กับ mirrored split grip, excessive steer/contact-lift attempt, exact replay และ half-step refinement
- สมมติฐานที่ต้องการ: zero steer คงความสมมาตรโดย yaw/modal motion เป็นศูนย์; steer ตรงข้ามให้ trajectory/yaw เป็น mirror; steering ที่อนุมัติคง contact ทั้งหมดและผ่าน energy/balance gates; branch speeds อิสระยังผูกกับ carrier average; demand สูงเกินถูกปฏิเสธเป็น contact lift หรือขีดจำกัดฟิสิกส์อื่นที่ชัดเจน
- การหักล้าง: มีแรงขับจาก rear support ที่ไม่ถูกขับ, clip normal load เงียบ ๆ, เครื่องหมาย steer/yaw ผิด, mirror ไม่ตรง, differential average ผิด, lateral heat หาย, ละเมิด contact/port limit, fixed point ไม่ converge แต่ถูกแสดงเป็น valid หรือ energy/refinement/replay ไม่ผ่าน

## ไฟล์ที่วางแผน

- `config/vehicle/coupled_planar_differential_v1.json`
- `src/formula_ultimate/simulation/coupled_planar_differential.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_coupled_planar_differential.py`
- `tests/test_coupled_planar_differential.py`
- `docs/research/COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.md`
- `docs/research/COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.th.md`
- บันทึกผล Work 071 สองภาษาที่ตรงกัน
- หลักฐาน deterministic ที่ git ignore ใต้ `artifacts/work071/`

## Validation และเกณฑ์สำเร็จ

1. loader reconcile สถาปัตยกรรม v3 ของ Work 069, differential declaration Work 070, powertrain Work 067, contact identities, mass/COM/yaw inertia จาก geometry, branch radius/inertia, steer limit ของ actuator และขีดจำกัด force/speed/torque
2. ความเร็ว wheel/carrier/converter เริ่มต้น match กับความเร็วรถที่ประกาศทาง kinematics โดยไม่มี hidden initial energy; total initial energy รวม rotating/body kinetic ทุกส่วน
3. coupled fixed-point loop ต้อง converge หรือคืน invalid/DNF ชัดเจน และไม่เผยแพร่ state ที่ไม่ converge
4. ทุก step ที่อนุมัติผ่าน vertical/pitch/roll, longitudinal/lateral/yaw, carrier-average, modal, torque, differential-interface, body-work และ global energy residual gates
5. zero steer คง lateral position, heading, lateral velocity, yaw rate และ differential-mode speed เป็นศูนย์ภายใต้ symmetric gripภายใน tolerance ที่ตรึง
6. steer บวก/ลบที่อนุมัติให้เครื่องหมาย yaw/trajectory ตรงข้ามกันและ selected states เป็น mirror ภายใน tolerance
7. normal loads เปลี่ยนทุก step ตามความเร่ง เป็นบวกในกรณีที่อนุมัติ และไม่เกินขีดจำกัดสถาปัตยกรรม; passive rear contact ไม่ส่ง propulsion torque
8. combined contact utilization คง `<= 1` ภายใน numerical tolerance พร้อมแสดง saturation/unserved force
9. excessive steer หรือ acceleration control ที่ตั้งใจทำให้เกิด contact-lift/limit `DNF` ชัดเจนโดยไม่ clip
10. exact replay, half-step refinement `<= 2%`, focused/full tests, compilation, หลักฐานสองภาษา, scoped commit และ post-commit clean-tree replay ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

fixed-point coupling อาจ stiff ใกล้ saturation หรือ contact lift แบบจำลองใช้ rigid quasi-static normal-load redistribution และ explicit body integration จึงยังไม่มี spring/damper travel, roll centres, unsprung mass, wheel hop, tyre relaxation, camber, aligning moment, aero maps, road roughness และ coefficient จากการวัด Numerical residual เป็นหลักฐาน ไม่ใช่ physical loss

Work 071 ไม่เพิ่ม internal gear geometry, suspension solids, driver/path controller, track boundaries, lap timing, tyre temperature/wear, real-circuit admission หรือ physical validation และยังไม่พิสูจน์ความพร้อมแข่งขัน
