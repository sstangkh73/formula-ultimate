# แผนงาน 067: Functional Powertrain Dynamics v1

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_067_functional-powertrain-dynamics-v1-plan.md`

## วัตถุประสงค์

สร้าง transient physical model รุ่นแรกสำหรับเส้นทาง Work 066 `energy_storage -> energy_converter -> power_transmission -> ground_propulsion` Torque ที่ร้องขอต้องถูกจำกัดด้วย stored energy, declared power, torque-speed envelope, efficiencies, shaft dynamics, transmission ratio, thermal state และ failure limits ทุก joule ที่ออกจาก storage ต้องกลายเป็น mechanical energy, useful external work, stored heat, rejected heat หรือ observable numerical conservation residual

งานนี้เปลี่ยน reference architecture จาก connected static contract เป็น falsifiable component-dynamics specimen แต่ยังไม่อ้างว่าเป็น complete engine, gearbox, tyre หรือ whole-car simulation

## คำถามวิจัยและสมมติฐาน

คำถาม: functional architecture สามารถส่ง bounded torque ผ่าน transient compliant drivetrain โดย conserve energy และ fail closed เมื่อเกิน energy, torque, speed หรือ temperature limits ได้หรือไม่

Preferred hypothesis: reference path เร่ง declared load, ทำตาม torque-speed/efficiency maps, เปลี่ยน modeled losses ทั้งหมดเป็น heat, conserve energy ภายใน frozen numerical tolerance และให้ downstream drive เป็นศูนย์หลัง terminal connection failure

Falsification รวม acceleration เมื่อ stored energy เป็นศูนย์, output torque เกิน local path limit, output powerมากกว่า conserved input, loss heat หายไป, non-finite state, energy residual ไม่ถูกรายงาน, stored energy เพิ่มโดยไม่มี declared recovery path, shaft ที่ failed แล้วยังส่ง torque, deterministic replay ให้ผลต่าง หรือ time-step refinement ต่างเกิน declared bound

## ขอบเขตและ state model

Technology-neutral reference model จะมี:

1. finite onboard energy state หน่วย joules และ maximum source power
2. interpolated converter torque-speed envelope และ load-dependent efficiency map
3. converter rotational inertia และ viscous loss
4. torsionally compliant connection พร้อม stiffness, damping, torque limit, twist limit และ irreversible failure state
5. transmission ratio, mechanical efficiency, reflected downstream inertia และ output torque/speed limits
6. external output-load torque และ useful-work accumulator
7. converter/transmission lumped thermal states, heat capacities, ambient rejection coefficients และ maximum temperatures
8. explicit energy storage, kinetic, elastic, thermal, useful-work, rejected-heat และ residual terms
9. deterministic terminal state และ event/failure codes

Ratio convention คือ `ratio = omega_input / omega_output`; ideal output torque เท่ากับ input torqueคูณ `ratio` แล้วลดด้วย transmission efficiency ยังคงบังคับ SI units และ right-handed frame

## การออกแบบการทดลอง

- Independent variables: throttle schedule, output load torque, initial stored energy, converter speed, shaft stiffness/damping/limits, inertia, ratio, torque-speed curve, efficiency curve, cooling coefficients, failure thresholds, duration และ time step
- Dependent variables: storage energy, shaft speeds/twist, transmitted/output torque, useful work, component temperatures, generated/rejected heat, limit flags, failure code/time, energy residual และ replay hash
- Controls: frozen Work 066 component limits, piecewise-linear maps, deterministic fixed-step integration, no regeneration, no silent clipping invalid state, explicit SI units และ canonical JSON identity
- Metrics: relative energy-conservation residual, maximum local-limit utilization, terminal speed/energy/temperature, useful-work fraction, failure response, exact replay และ coarse-versus-refined time-step difference

Positive reference case จะใช้ bounded throttle/load schedule Negative controls จะมี zero stored energy, deliberate shaft overload, deliberate thermal limit violation, invalid configuration และ tampered/non-finite inputs Analytical locked-speed conversion case จะ verify power/heat partition แยกจาก transient integrator

## ไฟล์ที่วางแผน

- `src/formula_ultimate/simulation/powertrain_dynamics.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/functional_powertrain_dynamics_v1.json`
- `scripts/experiments/run_functional_powertrain_dynamics.py`
- `tests/test_functional_powertrain_dynamics.py`
- `docs/research/FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.md`
- `docs/research/FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.th.md`
- matching bilingual Work 067 plan/result records
- ignored deterministic evidence ใต้ `artifacts/work067/`

## Validation และเกณฑ์สำเร็จ

1. Configuration values และ maps ต้อง finite, ordered, dimensionally explicit และ fail closed เมื่อ invalid
2. Zero energy ให้ converter torque, output work เป็นศูนย์และไม่มี force-from-nowhere
3. Analytical conversion check ปิด storage, connection, converter และ transmission power/loss termsถึง floating-point tolerance
4. Transient reference runเคารพ declared energy, torque, speed, twist และ temperature limits ทุกค่า หรือรายงาน exact terminal failure
5. Converter, cable, shaft damping, transmission และ viscous lossesปรากฏเป็น heat; ambient coolingปรากฏเป็น rejected heat
6. Total energy accounting รวม storage, mechanical, elastic, thermal, useful work, rejected heat และ signed observable residual ที่มี relative magnitude `<= 1e-3` สำหรับ reference run
7. Deliberate shaft overload ทำให้ connection ขาดถาวรและ transmitted/output drive torque หลังจากนั้นเป็นศูนย์ทั้งหมด
8. Deliberate overtemperature จบด้วย correct component failure code
9. รันซ้ำต้อง byte-identical หลัง canonical serialization; half-step refinement เปลี่ยน selected terminal metrics `<= 2%`
10. Focused/full tests, compilation, bilingual evidence, scoped commit และ post-commit clean-tree replayผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Fixed-step lumped dynamics อาจซ่อน stiff-shaft integration error ดังนั้น conservation residual และ step refinement เป็น admission evidence ไม่ใช่ silent corrections Synthetic torque-speed, efficiency, thermal, stiffness และ failure data เป็น test fixtures ไม่ใช่ measured component maps หรือ certified limits Reference drivetrain อาจ bias future discovery และห้ามกลายเป็น mandatory topology

Work 067 ไม่ model electrochemistry, combustion, electromagnetic fields, gear teeth, bearings, backlash/contact, lubrication, detailed shaft stress, fatigue/fracture growth, differential action, regenerative braking, tyre slip, suspension, vehicle translation, steering, aerodynamics, race strategy, manufacturing, physical validation หรือ safety certification งานเหล่านี้ต้องมี work item และ higher-fidelity evidence ภายหลัง
