# Drive-to-Ground Slip Coupling v1

ไฟล์ต้นฉบับภาษาอังกฤษ: `DRIVE_GROUND_SLIP_COUPLING_V1.md`

## ผลลัพธ์และขอบเขต

Work 068 ปิด causal chain แบบ deterministic รุ่นแรกจาก stored energy/shaft torque ของ Work 067 ไปยัง ground contact ของ Work 066, longitudinal force และ vehicle acceleration Ground unit ที่ admit ทุกชิ้นถูก reconcile กับ architecture component, contact, radius, geometry-derived axial inertia, port limits และ static normal load Broken drive connection propagate เป็น drive-subsystem state `failed` และ race outcome `DNF`

ผลนี้เป็น straight-line synthetic slip experiment ซึ่ง validate coupling identities, limits, energy partition, failure propagation, deterministic replay และ numerical refinement แต่ไม่ใช่ measured tyre model หรือ whole-vehicle physical validation

## Geometry และ inertia closure

Reference ใช้มวลรถ `272.55249331647553 kg` จาก Work 066 geometry Ground units ทั้งสองใช้รัศมี `0.14 m` และ geometry-derived axial inertia `0.13034241725073026 kg m^2` รวม inertia `0.2606848345014605 kg m^2`; remaining downstream inertia ที่ประกาศชัดคือ `2.2393151654985397 kg m^2` ผลรวมตรงกับ Work 067 output inertia `2.5 kg m^2` พอดี จึงไม่ count wheel inertia ซ้ำ

Static normal load แต่ละจุดคือ `1336.4134542910074 N` และทั้งคู่ปิด `m g = 2672.8269085820148 N` แต่ละ reference contact ประกาศ maximum longitudinal force `4000 N` ส่วน synthetic friction capacity ต่ำกว่า คือ `mu Fz = 1.2 * 1336.4134542910074 = 1603.6961451492088 N`

## Slip และ force law

สำหรับ common output speed `omega`, vehicle speed `v`, effective radius `r`, regularization speed `v0`, stiffness `C` และ forward drive slip:

```text
v_slip = r omega - v
kappa = v_slip / max(v, v0)
F_capacity = min(mu Fz, F_declared)
F = F_capacity tanh(C kappa / F_capacity), when kappa > 0
F = 0, when kappa <= 0
T_load = sum(F r).
```

Zero-force negative-slip branch ป้องกัน undeclared regenerative energy ใน v1 ส่วน request, capacity, applied force, utilization และ unserved torque ยังคง explicit

ที่ analytical constant state `omega = 100 rad/s`, `v = 12 m/s`, forces สองแรงเท่ากับ `1000 N` และรัศมีทั้งคู่ `0.14 m`:

```text
T_load = 280 N m
T_load omega = 28,000 W
sum(F v) = 24,000 W
slip heat = 4,000.0000000000036 W
power residual = -3.637978807091713e-12 W.
```

ดังนั้นผลต่างระหว่าง axle power กับ body power เป็น observable slip dissipation ไม่ใช่พลังงานหาย

## Transient reference result

Reference ใช้ throttle `0.5`, duration `2 s`, step `0.0005 s` และ `4000` steps

| Metric | Result | Gate |
| --- | ---: | --- |
| final vehicle speed | `14.3996903855916 m/s` | positive/finite |
| final distance | `16.4550513109228 m` | positive/finite |
| source energy used | `65239.388932965 J` | decreasing onboard store |
| vehicle kinetic energy | `28257.0273591386 J` | derived from mass/speed |
| slip heat | `1791.64460139612 J` | non-negative |
| aerodynamic work | `984.746997658385 J` | non-negative |
| rolling work | `659.722558888986 J` | non-negative |
| maximum total ground force | `2832.59764718983 N` | below combined capacity |
| maximum contact utilization | `0.883146615946464` | `<= 1` |
| maximum slip ratio | `0.111448036394737` | observable |
| maximum torque residual | `0 N m` | passed |
| maximum interface residual | `1.81721304670646e-12 J` | passed |
| maximum global residual | `0.510794088244438 J` | observable |
| maximum global relative residual | `1.02158817648888e-8` | `< 1e-3` |

Result SHA-256 คือ `b7311a924e74bc412c611f261e11928745dec381f093c13085814b05624a3070` Exact replay ให้ค่าเดิม การลด time step ครึ่งหนึ่งเปลี่ยน selected terminal values สูงสุด `4.969084181339372e-5` ต่ำกว่า frozen ceiling `0.02`

## Falsification controls

- Zero throttle: force, speed, distance และ contact body work คงเป็นศูนย์
- Zero stored energy พร้อม full throttle: ค่าชุดเดียวกันคงเป็นศูนย์ ไม่มี force from nowhere
- Friction saturation: positive slip ที่สูงมากเข้าใกล้แต่ไม่เกิน `min(mu Fz, F_declared)`
- Negative slip: requested drive force เป็นศูนย์; ไม่ infer undeclared regeneration
- Drive failure: ลด shaft limit โดยเจตนาทำให้เกิด `shaft_connection_failure` ที่ `0.002 s`, drive subsystem `failed`, outcome `DNF` และ final transmitted output drive torque `0 N m`
- Invalid controls: เปลี่ยน radius, axial inertia, contact force/normal-load limit, inertia closure, numerical tolerance และ non-finite friction แล้วถูก reject

Frozen experiment checks ทั้ง 10, focused tests 8 และ full repository regression 404 tests ผ่าน

## หลักฐานที่ยังขาดและงานถัดไป

v1 coupling ใช้ static normal loads, common output speed, forward-only regularized `tanh` force curve และ fixed-step explicit coupling ยังไม่มี differential action, independent wheel speeds, load transfer, suspension motion, lateral slip, steering, tyre thermal/wear state, road surface variation, regeneration หรือ reverse motion Force curve กับ friction coefficient เป็น synthetic ไม่ใช่ค่าที่ fit จากการวัด

งานถัดไปควรเพิ่ม dynamic normal-load transfer และ independent left/right wheel states แล้วรวม longitudinal/lateral slip กับ steering เพื่อเปลี่ยน straight-line powertrain specimen เป็น planar vehicle-dynamics experiment โดยไม่ลดความเข้มของ energy และ DNF contracts
