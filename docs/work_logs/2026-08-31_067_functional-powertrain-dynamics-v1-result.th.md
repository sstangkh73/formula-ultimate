# ผลงาน 067: Functional Powertrain Dynamics v1

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_067_functional-powertrain-dynamics-v1-result.md`

สถานะ: เสร็จสมบูรณ์ (Completed)

## ผลลัพธ์

สร้างและทดลอง deterministic transient model สำหรับเส้นทาง Work 066 energy-storage, converter, compliant connection, transmission และ output-load แล้ว Positive reference conserve energy ภายใน frozen threshold, declared local limits ทุกค่าถูกเคารพ, modeled losses ทุกชนิดปรากฏใน heat ledger และ refined integration ตรงกับ reference step ส่วน zero-energy, shaft-overload, thermal-failure, invalid-input และ replay controls ผ่าน

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/simulation/powertrain_dynamics.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/functional_powertrain_dynamics_v1.json`
- `scripts/experiments/run_functional_powertrain_dynamics.py`
- `tests/test_functional_powertrain_dynamics.py`
- `docs/research/FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.md`
- `docs/research/FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.th.md`
- bilingual Work 067 plan/result ชุดนี้

Ignored experiment evidence คือ `artifacts/work067/powertrain_dynamics_evidence.json`

## การตัดสินใจ

- Converter ยังคง technology-neutral และนิยามด้วย energy interface, torque-speed map, efficiency map, inertia, thermal state และ limits
- Two-inertia compliant shaft เปิดเผย twist, torque, damping heat และ irreversible failure แทนการถือ drivetrain เป็นป้ายสร้างแรง
- Transmission ratio คือ `omega_input / omega_output`; torque multiplication รวม declared shaft/transmission efficiencies
- Forward-only output load inject reverse energy ไม่ได้ Reverse operation และ regeneration ยังคงเป็น explicit non-goals
- Numerical energy residuals ถูกบันทึกและ gate แต่ไม่ถูกใช้ repair state

## คำสั่ง validation และ outputs ที่แน่นอน

```powershell
py -3.14 -m unittest tests.test_functional_powertrain_dynamics -v
```

Exit status `0`; `Ran 8 tests ... OK`

```powershell
py -3.14 scripts/experiments/run_functional_powertrain_dynamics.py --config config/vehicle/functional_powertrain_dynamics_v1.json --output artifacts/work067/powertrain_dynamics_evidence.json
```

Exit status `0`; status `passed`; evidence SHA-256 `9b99b5afb6a0368b450d54d6bab983c4e0444be188baf783ed1f54c0e3a8713c`; reference result SHA-256 `3248fe721f8fdc39aca182cb81ced64ee7163fdabfa6874778636bd3df2b3543`; maximum relative energy residual `1.0006847977638245e-08`; maximum refinement difference `1.79900311164274e-05`; overload terminal `shaft_connection_failure`; thermal terminal `converter_overtemperature`

Reference evidence: `4,000` steps; final converter/output speeds `322.205241054604/107.403266469072 rad/s`; source energy used `65,729.4197853313 J`; useful work `30,286.8669266214 J`; maximum connection demand `182.066064231239 N m`; maximum twist `0.0812613938084503 rad`; maximum output drive torque `513.699400228442 N m`; final temperatures `300.317298442075/300.2848072388 K`

```powershell
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Exit statuses `0`; full regression output `Ran 396 tests ... OK`; compilation และ diff checks ไม่มี error

## Falsification และข้อจำกัด

Zero-energy control ให้ source use และ useful work เป็นศูนย์พอดี Overload control เกิน deliberate shaft limit `50 N m` ด้วย demand `56.331665505 N m`, fail ที่ `0.002 s` และหลังจากนั้นส่ง torque เป็นศูนย์ Thermal control จบเป็น `converter_overtemperature` ที่ `0.016 s` Invalid maps, efficiencies, conservation declarations, temperatures, tolerances, time grids และ non-finite states ถูก reject

ไม่พบข้อขัดแย้งภายใน declared model แต่ผลนี้ไม่ได้ validate physical engine, motor, battery, gearbox, shaft หรือ complete vehicle Reference maps และ thermal/failure values ทั้งหมดเป็น synthetic Fixed-step two-inertia model ยังไม่มี detailed fields, contact, geometry-derived stress/fatigue, tyre slip, translation, regeneration และ measured calibration ห้ามใช้ผลนี้อ้าง race performance หรือ safety

## งานถัดไป

Work 068 ควร couple powertrain outputs สองฝั่งเข้ากับ wheel inertia และ bounded ground-force/slip law, verify torque-to-force กับ wheel/vehicle energy transfer ด้วย analytical check และ propagate failed drive connection ไปเป็น subsystem failure และ `DNF` Work item ภายหลังควรแทน synthetic shaft limit ด้วย geometry/material evidence จาก torsion, yield, fracture และ fatigue chain
