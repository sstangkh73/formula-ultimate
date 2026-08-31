# แผนงาน 068: Drive-to-Ground Slip Coupling v1

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_068_drive-ground-slip-coupling-v1-plan.md`

## วัตถุประสงค์

Couple transient powertrain output จาก Work 067 เข้ากับ ground-propulsion components สองชิ้นของ Work 066 ผ่าน geometry-derived effective radius/rotational inertia, bounded longitudinal slip law, normal-load/friction limits และ forward vehicle translation Torque ต้องกลายเป็น contact force, vehicle kinetic energy, resistance work หรือ slip heat Terminal drive-path failure ต้อง propagate เป็น subsystem failure และ race outcome `DNF`

นี่คือ causal experiment `stored energy -> shaft torque -> ground force -> vehicle acceleration` รุ่นแรก แต่ยังเป็น straight-line synthetic specimen ไม่ใช่ complete tyre, suspension, differential หรือ race simulation

## คำถามวิจัยและสมมติฐาน

คำถาม: independently validated powertrain สามารถส่ง torque ผ่าน declared ground interfaces โดยไม่เกิน contact capacity หรือสร้างพลังงาน และ broken drive path หยุดการแข่งขันเป็น `DNF` อย่าง deterministic ได้หรือไม่

Preferred hypothesis: reference run ให้ finite positive acceleration, contact forces ทุกค่าอยู่ภายใน Work 066 limits และ slip-law friction bound, powertrain useful-work sink แบ่งเป็น body work กับ non-negative slip heat, global energy residual ต่ำกว่า frozen threshold, exact replay/time-step refinement ผ่าน และ deliberate shaft failure ให้ `DNF` พร้อม subsequent drive torque เป็นศูนย์

Falsification รวม motion เมื่อ energy/throttle เป็นศูนย์, ground force โดยไม่มี torque, force เกิน `mu Fz` หรือ declared port/contact limit, torque-to-force residual, negative slip dissipation ที่ไม่รายงาน, vehicle energy มากกว่า powertrain output, incompatible geometry/inertia identity, failed drive connection ยังส่ง torque, ไม่มี `DNF`, non-finite state, nondeterministic replay หรือ refinement ต่างเกิน declared bound

## Model และสมการ

Declared ground unit แต่ละชิ้นใช้ Work 066 component/contact identity, effective radius `r`, geometry-derived axial inertia, normal load, friction coefficient, slip stiffness และ maximum longitudinal force ผลรวม geometry-derived ground-unit inertia กับ explicitly declared other downstream inertia ต้องเท่ากับ Work 067 output inertia โดยห้าม duplicate inertia เงียบๆ

สำหรับ forward-only v1 boundary:

```text
v_slip = r omega - v_vehicle
kappa = v_slip / max(v_vehicle, v_regularization)
F_capacity = min(mu Fz, F_declared)
F_requested = F_capacity tanh(C_kappa kappa / F_capacity), for kappa > 0
T_load = sum(F_applied r)
m dv/dt = sum(F_applied) - F_drag - F_rolling
```

Negative slip ไม่ imply regeneration ใน v1; มันขอ drive force เป็นศูนย์และยังปรากฏใน telemetry Per-step interface partition คือ

```text
T_load omega = sum(F_applied v_vehicle)
               + sum(F_applied (r omega - v_vehicle)).
```

เทอมที่สองคือ slip heat Global ledger แทน Work 067 useful-work sink ด้วย vehicle kinetic energy, aerodynamic/rolling work และ slip heat Residuals ถูกรายงาน ไม่ถูกแก้

## การออกแบบการทดลอง

- Independent variables: throttle, duration, time step, mass, effective radii, geometry-derived inertia, other reflected inertia, normal loads, friction coefficient, longitudinal slip stiffness, contact limits, drag area, rolling resistance และ drive-failure limit
- Dependent variables: ground-unit slip velocity/ratio, requested/applied force, contact utilization, axle load torque, vehicle acceleration/speed/distance, body work, slip heat, drag/rolling work, global energy residual, subsystem state, `DNF` reason/time และ deterministic hash
- Controls: Work 066 architecture identity/geometry, Work 067 committed configuration, SI units, static normal-load closure, no regeneration, no reverse motion, deterministic fixed steps, canonical JSON และ no hidden repair
- Metrics: maximum force/utilization/slip, torque-to-force/power-partition residuals, final speed/distance, energy residual, exact replay และ coarse/fine terminal differences

Controls จะมี zero throttle, zero stored energy, friction saturation, geometry/inertia mismatch, invalid/non-finite declarations, deliberate shaft overload, exact replay และ half-step refinement Analytical constant-state partition แยกต่างหากจะ verify `T omega = F v + Qdot_slip` โดยไม่พึ่ง integration

## ไฟล์ที่วางแผน

- `src/formula_ultimate/simulation/drive_ground_coupling.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/functional_drive_ground_coupling_v1.json`
- `scripts/experiments/run_drive_ground_coupling.py`
- `tests/test_drive_ground_coupling.py`
- `docs/research/DRIVE_GROUND_SLIP_COUPLING_V1.md`
- `docs/research/DRIVE_GROUND_SLIP_COUPLING_V1.th.md`
- matching bilingual Work 068 plan/result records
- ignored deterministic evidence ใต้ `artifacts/work068/`

## Validation และเกณฑ์สำเร็จ

1. Ground component/contact IDs, radii, mass, contact limits และ axial inertias reconcile กับ Work 066 geometry ภายใน declared tolerance
2. Ground-unit กับ other reflected inertia รวมกันตรงกับ Work 067 output inertia
3. Analytical torque/power partition ปิดถึง floating-point tolerance
4. Zero throttle หรือ zero stored energy ให้ ground force, speed, distance และ useful vehicle workเป็นศูนย์
5. Reference forces ไม่เกิน `min(mu Fz, declared maximum)` และ axle load torque เท่ากับ `sum(F r)`
6. Slip heat finite/non-negative; vehicle kinetic, drag, rolling และ slip terms แทน powertrain useful workโดยไม่มี hidden energy
7. Reference global relative energy residual `<= 1e-3` และ per-step torque/power residual ทุกค่าอยู่ใน relative ceiling เดียวกัน
8. Deliberate drive-path failure ให้ subsystem state `failed`, outcome `DNF`, exact reason/time และ transmitted/output drive torque หลังจากนั้นเป็นศูนย์
9. Canonical replay ต้อง exact; half-step refinement เปลี่ยน selected terminal metrics `<= 2%`
10. Focused/full tests, compilation, bilingual evidence, scoped commit และ post-commit clean-tree replayผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Regularized `tanh` slip law เป็น synthetic และใช้ falsify plumbing/conservation errors เท่านั้น ไม่ใช่ measured tyre curve Static normal loads ไม่มี load transfer Common output speed ไม่มี differential action และ independent left/right wheel-speed states Fixed-step explicit coupling อาจมี phase error ซึ่งจะแสดงผ่าน global residual และ refinement

Work 068 ไม่ implement combined lateral slip, steering, suspension motion, dynamic normal loads, road roughness, tyre temperature/wear, aquaplaning, wheel lift, differential/contact mechanics, regenerative braking, reverse motion, aerodynamic maps, race strategy, detailed shaft stress, measured calibration, physical validation หรือ safety certification Reference topology เป็น falsification fixture ไม่ใช่ required vehicle layout
