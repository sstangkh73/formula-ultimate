# โมเดล Aerodynamic Force, Balance และ Cooling Flow

ต้นฉบับภาษาอังกฤษ: `AERODYNAMIC_FORCE_BALANCE_COOLING_MODEL.md`

## สถานะและขอบเขตคำอ้าง

Work 017 สร้าง `work017-aerodynamic-map-v1` ซึ่งเป็น coefficient-map evaluator
ระดับ Level-0 ที่ deterministic ใช้หา quasi-steady aerodynamic force, pitch/yaw
moment, longitudinal centre of pressure และ ram-air cooling flow ที่ operating
point หนึ่งภายใน envelope ของ speed, ride height, yaw และ active state ที่ประกาศ

นี่ไม่ใช่ CFD solver, wind-tunnel result, geometry mesher, calibrated vehicle
model, safety case หรือ physical validation Reference map ที่รวมใน repository
ระบุชัดว่าเป็น synthetic

## ขอบเขต Topology และ Geometry

Model ใช้ reference area และ length โดยไม่กำหนด wing, body shape, wheel count
หรือ architecture Formula One แบบเดิม Candidate topology ใดก็ส่ง coefficient map
ได้หากผ่าน evidence contract

`AerodynamicEvidence.basis` ต้องเป็นหนึ่งใน:

- `synthetic_reference`: analytical/software fixture เท่านั้น;
- `geometry_derived`: มาจาก geometry ที่ระบุ จึงต้องมี geometry digest SHA-256
  lowercase 64 ตัวอักษร;
- `cfd`: computational-flow evidence ที่สร้างภายนอก; หรือ
- `measured`: test evidence ที่สร้างภายนอก

Evaluator เก็บ evidence แต่ไม่ตรวจคุณภาพ CFD หรือ measurement อย่างอิสระ Digest
เชื่อม data กับ geometry แต่ไม่พิสูจน์ mesh quality, convergence, uncertainty หรือ
experimental validity

## Map Contract และลำดับ

`AerodynamicCoefficientMap` ประกาศ axis ที่เพิ่มอย่างเคร่งครัด:

```text
airspeeds_m_per_s >= 0
ride_heights_m   >= 0
yaw_angles_rad    finite และ signed
```

Active state ที่ไม่ซ้ำแต่ละตัวมี sample tuple ครบหนึ่งชุด ลำดับ flattened แบบ
deterministic คือ speed-major แล้ว ride height แล้ว yaw:

```text
index = (speed_index * height_count + height_index) * yaw_count + yaw_index
```

แต่ละ sample เก็บ:

- drag coefficient `C_D` ไม่ติดลบ;
- side-force coefficient `C_Y` แบบ signed;
- downforce coefficient `C_L_down` แบบ signed (ค่าบวกหมายถึง force body `-z`);
- pitching-moment coefficient `C_m` แบบ signed รอบ body `+y`;
- yawing-moment coefficient `C_n` แบบ signed รอบ body `+z`; และ
- cooling-flow coefficient `C_flow` ไม่ติดลบ

อนุญาต `C_L_down` ติดลบและหมายถึง lift ตาม sign contract นี้ Active state เป็น
discrete; evaluator ไม่สร้าง fractional state

## Envelope และ Interpolation

Evaluator หา exact node หรือ bracket สองด้านของแต่ละ continuous axis แล้วทำ
tensor-product linear interpolation Result เก็บ lower/upper index, value,
fraction, active-state identity และข้อมูลว่าทั้งสาม axis เป็น exact nodeหรือไม่

จุดต่ำ/สูงกว่า continuous axis ใด ๆ และ active state ที่ไม่รู้จักคืน `invalid`
ไม่มี extrapolation หรือ boundary clamping Decimal bracket fraction เก็บ binary
floating-point representation ปกติ เช่น midpoint ทางคณิตศาสตร์ของ `0.04` กับ
`0.08` ถูกบันทึกเป็น `0.4999999999999999` บน runtime ที่ทดสอบ

## สมการ Force, Moment และ Balance

สำหรับ airspeed `V`, air density `rho`, reference area `A` และ reference length
`L`:

```text
q       = 0.5 * rho * V^2
drag    = q * A * C_D
side    = q * A * C_Y
down    = q * A * C_L_down
pitch   = q * A * L * C_m
yaw     = q * A * L * C_n
x_cp    = pitch / down, เมื่อ down != 0
```

`drag` เป็นขนาดบวกที่ต้าน relative airflow ส่วน `side`, `down`, `pitch` และ
`yaw` เก็บ sign ที่ประกาศ `x_cp` signed เทียบกับ reference origin และละไว้เมื่อ
downforce เป็นศูนย์ Pitch moment ยังคงถูกเก็บเสมอ การละ `x_cp` จึงไม่ซ่อน moment
evidence

Result คำนวณซ้ำและแสดง residual แยกสำหรับสมการ force/moment ทั้งห้า ผลไม่ finite
หรือ residual magnitude เกิน `1e-9` ในหน่วย SI ของมันคืน `invalid`

## สมการ Ram-Air Cooling

สำหรับ cooling inlet area `A_inlet`, air specific heat `cp_air`, effectiveness
`epsilon`, component temperature `T_component` และ air temperature `T_air`:

```text
m_dot_air = rho * V * A_inlet * C_flow
C_dot_air = m_dot_air * cp_air
G_cooling = epsilon * C_dot_air
Q_reject  = G_cooling * (T_component - T_air)
```

`Q_reject > 0` หมายถึงความร้อนออกจาก component ที่ร้อนกว่า `Q_reject < 0`
หมายถึง air เพิ่มความร้อนให้ component ที่เย็นกว่า Airspeed ศูนย์ให้ ram flow,
conductance และ heat transfer ศูนย์ แม้ coefficient ใน map ไม่เป็นศูนย์

Mass-flow, conductance และ heat-flow residual แสดงชัด Model ไม่มี pressure loss,
fan/pump curve, heat-exchanger UA limit, recirculation, compressibility หรือ
active-device energy พลังงาน actuation/fan/pump ต้องประกาศใน accounting ที่เข้า
กับ Work 012/013

## หลักฐานอ้างอิง

`scripts/validate_aerodynamics.py` ประเมิน synthetic map สอง state และตรวจ:

- interior operating point ที่ algebraic residual ทั้งแปดเป็นศูนย์;
- drag ratio `4.0` ระหว่าง `40/20 m/s` จาก scaling `V^2`;
- ram-air mass-flow ratio `2.0` ระหว่าง `40/20 m/s` จาก scaling เชิงเส้น `V`;
- cooling-open state เพิ่มทั้ง drag และ cooling mass flow;
- replay equality exact; และ
- `41 m/s` นอก map `0–40 m/s` คืน `invalid`

Unit suite ยังตรวจ exact node, tensor interpolation, drag/downforce symmetric ตาม
yaw, side force/moment antisymmetric ตาม yaw, signed heat flow, zero speed,
geometry-digest provenance, malformed grid, envelope ทุกมิติ, active state ที่ไม่
รู้จัก และ runtime output ไม่ finite

## ขอบเขต Integration ปัจจุบัน

Work 017 คืน force, moment, centre of pressure และ cooling conductance เป็น typed
evidence แต่ยังไม่ inject ค่าเหล่านี้เข้า race motion Work 015, contact load Work
016 หรือ thermal integration Work 014 Coupling นั้นต้องเป็น experiment ที่วางแผน
แยกพร้อม event ordering และ conservation check

## ข้อจำกัดและงานต่อ

- Tensor-linear interpolation อาจพลาด nonlinear separation, stall, hysteresis,
  ground-effect transition และ wake interaction ระหว่าง node ที่ห่าง
- Coefficient เป็น quasi-steady ไม่มี gust, transient device motion,
  compressibility, fluid-structure interaction และ turbulence uncertainty
- Synthetic test ยืนยันเพียง software semantics การประเมิน candidate จริงต้องมี
  CFD/measurement ที่เชื่อม geometry พร้อม uncertainty และ higher-fidelity check
  อิสระ
- Work 018 รับผิดชอบ suspension, mechanical braking และ regenerative braking
  และยังไม่ถูกทำในงานนี้
