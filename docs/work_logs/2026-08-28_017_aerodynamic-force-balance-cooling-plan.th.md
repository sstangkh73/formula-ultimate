# แผน Work 017: Aerodynamic Force, Balance และ Cooling Flow

ต้นฉบับภาษาอังกฤษ: `2026-08-28_017_aerodynamic-force-balance-cooling-plan.md`

สถานะ: Completed

## วัตถุประสงค์

สร้าง aerodynamic coefficient-map evaluator ระดับ Level-0 ที่ deterministic
เพื่อ interpolate drag, side force, downforce, pitch/yaw moment และ ram-air
cooling flow ข้าม envelope ของ speed, ride height, yaw และ discrete active state
ที่ประกาศ พร้อมเก็บ provenance, interpolation evidence, residual และสถานะ
invalid/out-of-envelope

## ขอบเขต

- กำหนด SI contract สำหรับ aerodynamic reference แบบ topology-neutral, map
  provenance, grid axis, active-state grid, coefficient sample, operating point,
  interpolation evidence, force/moment/cooling output และ residual
- ไม่กำหนดว่าต้องมีปีก, body shape, wheel count, aero device แบบเดิม หรือ layout
  Formula One ปัจจุบัน
- บังคับ coefficient grid ที่ครบและ deterministic พร้อม reject active state ซ้ำ,
  axis ไม่เรียง, sample ขาด และ evidence contract ที่ไม่รองรับ
- ใช้ tensor-product linear interpolation ตาม airspeed, ride height และ yaw;
  active state เป็น discrete และไม่ interpolate
- Reject จุดนอก envelope ที่ประกาศแทนการ clamp หรือ extrapolate
- แปลง coefficient เป็น drag, side force, downforce, pitch moment และ yaw moment
  ด้วย dynamic pressure กับ reference dimension ที่ประกาศ
- หา longitudinal centre of pressure แบบ signed เฉพาะเมื่อ downforce ไม่เป็นศูนย์
  โดยยังแสดง pitch-moment evidence แยก
- แปลง cooling-flow coefficient เป็น air mass flow, heat-capacity rate,
  effective conductance และ signed heat rejection/absorption ที่อุณหภูมิ air และ
  component ที่ประกาศ
- Test exact node, interpolation, symmetry reference, speed-squared force
  scaling, ผล ride-height/yaw, active-state trade-off, zero speed, provenance,
  replay exact, malformed grid และ out-of-envelope rejection
- เพิ่ม validator, เอกสาร model/result สองภาษา, validation evidence และ commit
  แยก โดยไม่เริ่ม Work 018

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/aerodynamics.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_aerodynamics.py`
- `scripts/validate_aerodynamics.py`
- `docs/physics/AERODYNAMIC_FORCE_BALANCE_COOLING_MODEL.md` และ `.th.md`
- สถานะ queue และคู่ plan/result สองภาษานี้
- problem report สองภาษาแยกสำหรับทุกปัญหาที่พบและแก้

## ขอบเขตฟิสิกส์

ที่ airspeed `V`, density `rho`, reference area `A` และ reference length `L`:

```text
q       = 0.5 * rho * V^2
drag    = q * A * C_D                 (ขนาดบวกต้าน flow)
side    = q * A * C_Y                 (signed body +y)
down    = q * A * C_L_down            (signed บวก body -z)
pitch   = q * A * L * C_m             (signed body +y moment)
yaw     = q * A * L * C_n             (signed body +z moment)
x_cp    = pitch / down                 (เฉพาะเมื่อ down != 0)
```

Cooling เป็น reduced-order ram-air path:

```text
m_dot_air = rho * V * A_inlet * C_flow
C_dot_air = m_dot_air * cp_air
G_cooling = effectiveness * C_dot_air
Q_reject  = G_cooling * (T_component - T_air)
```

`Q_reject` บวกหมายถึงความร้อนออกจาก component ที่ร้อนกว่า; ค่าลบหมายถึง air
ทำให้ component ที่เย็นกว่าร้อนขึ้น พลังงาน actuation และงาน fan/pump ไม่รวมและ
ต้องคิดแยกใน energy model

## ความหมายของ Map และ Evidence

แต่ละ map มี axis เพิ่มขึ้นอย่างเคร่งครัดและ ordered sample tuple ครบหนึ่งชุดต่อ
active state ลำดับ sample คือ speed-major แล้ว ride-height แล้ว yaw Evidence
basis ที่อนุญาตคือ `synthetic_reference`, `geometry_derived`, `cfd` และ
`measured` Geometry-derived evidence ต้องมี SHA-256 geometry digest; synthetic
map ห้ามถูกนำเสนอเป็น geometry evidence

Interpolation คืน bracket index สองด้านและ fraction ของทุก continuous axis
Exact node ยังคง exact จุดนอก axis ใด ๆ หรือ active state ที่ไม่รู้จักคืน
`invalid` ที่สังเกตได้โดยไม่ clamp boundary

## นิยามการทดลอง

- สมมติฐานหลัก: aerodynamic map ที่ประกาศสามารถแสดง force, balance และ cooling
  trade-off ข้าม control envelope ทั้งหมดแบบ deterministic โดยจุดที่ไม่รองรับ
  และ provenance อ่อนยังแยกจาก geometry-derived evidence ที่ validated ได้
- Independent variables: coefficient grid, evidence basis, active state,
  airspeed, density, ride height, yaw, reference area/length, cooling inlet,
  air heat capacity, effectiveness และอุณหภูมิ
- Dependent variables: coefficient ที่ interpolate, bracket/weight, dynamic
  pressure, force, moment, centre of pressure, air mass flow, cooling conductance,
  heat flow, residual, status และ reason
- Controls: SI/sign convention, grid ordering เดียว, ไม่ extrapolate,
  tensor-linear interpolation, discrete active state และ random draw ศูนย์
- Metrics: exact-node error, interpolation error, force/moment/cooling residual,
  force ratio ตามกำลังสองของ speed, mass-flow speed ratio, symmetry sign,
  drag/cooling delta จาก active state, replay equality และ invalid-case coverage
- Success: node/interior/envelope reference ทุกกรณีตรง analytical value;
  active-state trade-off สังเกตได้; malformed/outside case fail; repository gate
  ทั้งหมดผ่าน
- Failure criteria: extrapolation/clamping เงียบ, grid ไม่ครบ, ค่าไม่ finite,
  drag/cooling-flow coefficient ติดลบ, provenance invalid หรือ algebraic residual
  ที่ประกาศเกิน tolerance
- Falsification: query ต่ำ/สูงกว่า continuous envelope ทุกแกน, ขอ active state ที่
  ไม่รู้จัก, ให้ grid ไม่ครบ และให้ geometry-derived evidence ไม่มี digest โดย
  ห้าม accept ทุกกรณี

## ความเสี่ยง

- Linear interpolation ไม่สามารถแทน nonlinear separated-flow transition ระหว่าง
  node ที่ห่างได้
- ความน่าเชื่อถือ coefficient map จำกัดด้วย provenance geometry/CFD/test;
  synthetic map เป็น software evidence เท่านั้น
- Cooling model ไม่มี pressure-drop curve, duct loss, heat-exchanger UA, fan work,
  recirculation และ compressibility
- Quasi-steady coefficient ไม่มี gust, wake history, transient active-device
  motion และ fluid-structure interaction

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี CFD solver, wind-tunnel calibration, geometry meshing, automatic
  coefficient extraction หรือคำอ้าง aerodynamic performance จริง
- ไม่กำหนด vehicle shape หรือ conventional aerodynamic component library
- ไม่ทำ suspension/braking/regen, Work 018 หรือ remote push

## Validation

```powershell
python -m unittest tests.test_aerodynamics -v
python -m unittest discover -s tests -v
python scripts/validate_aerodynamics.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

ทุก gate รัน fail-fast การเสร็จต้องมี result สองภาษา, problem report แยกสำหรับ
ปัญหาที่พบ, staged scope ที่ระบุ, commit สำเร็จ และหลักฐาน clean-state/hash หลัง
commit
