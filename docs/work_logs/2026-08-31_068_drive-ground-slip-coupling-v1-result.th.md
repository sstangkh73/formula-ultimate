# ผลงาน 068: Drive-to-Ground Slip Coupling v1

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_068_drive-ground-slip-coupling-v1-result.md`

สถานะ: เสร็จสมบูรณ์ (Completed)

## ผลลัพธ์

สร้าง deterministic coupling จาก Work 067 powertrain output ผ่าน geometry-bound ground units ของ Work 066 ไปยัง slip-limited longitudinal force และ vehicle translation Reference เร่งความเร็วได้พร้อมผ่าน geometry, inertia, contact, torque, interface-power และ global-energy gates Zero-input controls ไม่เกิด motion และ drive-path failure propagate เป็น subsystem failure กับ `DNF` โดย output drive torque เป็นศูนย์

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/simulation/drive_ground_coupling.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/functional_drive_ground_coupling_v1.json`
- `scripts/experiments/run_drive_ground_coupling.py`
- `tests/test_drive_ground_coupling.py`
- `docs/research/DRIVE_GROUND_SLIP_COUPLING_V1.md`
- `docs/research/DRIVE_GROUND_SLIP_COUPLING_V1.th.md`
- bilingual Work 068 plan/result ชุดนี้

Ignored evidence คือ `artifacts/work068/drive_ground_evidence.json`

## การตัดสินใจ

- Ground radius, axial inertia, mass และ contact limits ถูกตรวจเทียบ Work 066 แทนการกรอกใหม่โดยไม่มี provenance
- Geometry-derived ground inertia บวก explicit other reflected inertia ปิด Work 067 output inertia จึงไม่ double count
- Positive slip ใช้ bounded synthetic `tanh` law; nonpositive slip ขอ drive force เป็นศูนย์เพราะ regeneration อยู่นอก v1
- Work 067 useful work ถูกแทนใน global ledger ด้วย vehicle kinetic energy, aerodynamic/rolling work และ slip heat
- Powertrain terminal failure กลายเป็น drive subsystem `failed` และ race outcome `DNF` ทันที

## คำสั่ง validation และ evidence ที่แน่นอน

```powershell
py -3.14 -m unittest tests.test_drive_ground_coupling -v
```

Exit status `0`; `Ran 8 tests ... OK`

```powershell
py -3.14 scripts/experiments/run_drive_ground_coupling.py --config config/vehicle/functional_drive_ground_coupling_v1.json --vehicle-root config/vehicle --output artifacts/work068/drive_ground_evidence.json
```

Exit status `0`; status `passed`; evidence SHA-256 `747d7ab1fbc7b73093151cf685e444160aa55fade6c385e1a5fb5c1f8c4d1b0f`; reference SHA-256 `b7311a924e74bc412c611f261e11928745dec381f093c13085814b05624a3070`; final speed/distance `14.399690385591617 m/s` และ `16.45505131092282 m`; maximum contact utilization `0.8831466159464643`; maximum global relative energy residual `1.0215881764888763e-08`; maximum refinement difference `4.969084181339372e-05`; deliberate failure outcome `DNF`, reason `shaft_connection_failure`

Reference energy evidence: source used `65239.388932965 J`; vehicle kinetic `28257.0273591386 J`; slip heat `1791.64460139612 J`; aerodynamic work `984.746997658385 J`; rolling work `659.722558888986 J`; maximum ground force `2832.59764718983 N`; maximum torque residual `0 N m`; maximum interface residual `1.81721304670646e-12 J`; maximum global residual `0.510794088244438 J`

```powershell
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Exit statuses `0`; full regression `Ran 404 tests ... OK`; compilation และ diff checks ไม่มี error

## Falsification, ข้อจำกัด และงานถัดไป

Zero throttle และ zero energy ไม่เกิด motion High positive slip ไม่เกิน contact capacity Negative slip ไม่สร้าง undeclared regeneration การลด shaft limit ทำให้ `DNF` ที่ `0.002 s`; terminal output drive torque คือ `0 N m` Invalid radius, axial inertia, force/normal-load limits, inertia closure, tolerance และ non-finite friction fail closed

ไม่พบข้อขัดแย้งภายใน declared model แต่ slip curve, friction, normal loads, drag และ rolling values ยังเป็น synthetic Common wheel speed, static loads, straight-line translation และ explicit fixed steps ใช้ validate differential, suspension, steering, real tyre, lap time หรือ safety ไม่ได้

Work 069 ควรสร้าง dynamic normal-load transfer และ independent left/right wheel states แล้ว couple steering กับ combined slip สำหรับ planar motion โดยรักษา exact energy/failure evidence
