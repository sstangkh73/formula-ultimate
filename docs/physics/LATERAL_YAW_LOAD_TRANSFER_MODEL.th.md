# โมเดล Lateral/Yaw และ Load Transfer

ต้นฉบับภาษาอังกฤษ: `LATERAL_YAW_LOAD_TRANSFER_MODEL.md`

## สถานะและขอบเขตคำอ้าง

Work 016 สร้าง `work016-planar-v1` ซึ่งเป็น planar rigid-body selection model
ระดับ Level-0 ที่ deterministic โดย coupling contact kinematics, linear
slip-angle force request, combined tyre-force saturation จาก Work 011,
quasi-static longitudinal/lateral load transfer และ planar state integration
ที่ประกาศชัดเจน

การผ่าน model นี้ไม่ใช่ physical validation, tyre calibration, safety evidence
หรือคำอ้าง lap time จริง

## Contract ด้าน topology

`PlanarVehicle` รับ tuple ที่เรียงลำดับของ `PlanarContact` แต่ละ contact ประกาศ:

- ID ไม่ซ้ำและตำแหน่ง body frame `(x_i, y_i)` ใดก็ได้ หน่วย metre;
- baseline normal load หน่วย newton;
- steer angle หน่วย radian;
- cornering stiffness หน่วย newton per radian;
- longitudinal force ที่ขอ หน่วย newton; และ
- friction coefficient longitudinal/lateral จาก Work 011

Implementation ไม่บังคับสี่ล้อ, คู่ซ้ายขวา หรือสองเพลา Baseline load ต้องรวม
เป็น `m*g` และมี pitch/roll moment ศูนย์ Contact geometry ที่ active ต้องมีข้อมูล
ตำแหน่งอิสระพอแก้ vertical, pitch และ roll equilibrium; layout ที่ rank ไม่พอ
คืน `invalid`

## Contact kinematics และ force ที่ขอ

สำหรับ body velocity `(u, v)`, yaw rate `r`, contact position `(x_i, y_i)` และ
steer angle `delta_i`:

```text
Vx_body_i = u - r*y_i
Vy_body_i = v + r*x_i

Vx_local_i =  cos(delta_i)*Vx_body_i + sin(delta_i)*Vy_body_i
Vy_local_i = -sin(delta_i)*Vx_body_i + cos(delta_i)*Vy_body_i

alpha_i = atan2(Vy_local_i,
                max(abs(Vx_local_i), speed_regularization))
Fy_requested_i = -C_alpha_i * alpha_i
```

`Fx_requested_i` ที่ประกาศและ `Fy_requested_i` ที่คำนวณถูกส่งตรงเข้า
`resolve_tyre_force` Work 011 project คำขอที่เกิน limit แบบ radial ลงบน friction
circle/ellipse ที่ประกาศ `PlanarContactResult` แต่ละตัวเก็บ local velocity, slip
angle, requested/applied force, utilization, saturation, body-frame force และ
yaw moment

Linear slip law เป็นเพียง request model ไม่มี relaxation length, temperature,
camber, pressure, wear หรือ empirical nonlinear force curve

## Quasi-static load transfer

ที่ body-frame inertial acceleration `(a_x, a_y)` normal load ต้องผ่าน:

```text
sum(Fz_i)       = m*g
sum(x_i*Fz_i)   = -m*a_x*h
sum(y_i*Fz_i)   = -m*a_y*h
```

ในทุก solution solver เลือกค่าที่เปลี่ยนจาก baseline-load vector น้อยที่สุดใน
Euclidean norm ถ้า `A` มี constraint สามแถว projection คือ:

```text
Fz = Fz_baseline + A^T * (A*A^T)^-1 * (b - A*Fz_baseline)
```

จึงได้ distribution deterministic สำหรับ contact topology ที่ full rank
Projected normal load ติดลบถูกรายงานเป็น contact lift และคืน `invalid`; ไม่ clip
เป็นศูนย์ Raw projected load และ equilibrium residual ยังคงสังเกตได้

## Coupled solve

Tyre capacity ขึ้นกับ normal load ขณะที่ load transfer ขึ้นกับ force จาก tyre
ดังนั้น `step_planar_dynamics` ทำ fixed-point iteration deterministic:

1. เริ่มจาก acceleration ศูนย์;
2. project normal load ที่ acceleration guess;
3. resolve combined force ของทุก contact;
4. คำนวณ `a_x = sum(Fx)/m` และ `a_y = sum(Fy)/m`;
5. เปรียบเทียบกับ guess แล้ว update ด้วย relaxation factor ที่ประกาศ;
6. หยุดเฉพาะเมื่ออยู่ใน acceleration tolerance แบบ absolute/relative

ค่าเริ่มต้นมี limit 64 iterations และ relaxation factor `0.5` Result รายงาน
iterations และ convergence Rank deficiency, contact lift, arithmetic ไม่ finite,
numerical failure จาก Work 011, iteration budget ไม่พอ หรือ balance เกิน tolerance
ที่ประกาศ คืน `invalid` โดย state ไม่เปลี่ยน

## Planar balance และ integration

Applied local force ถูก rotate เข้า body frame Total force และ moment กำหนด:

```text
m*(du/dt - r*v) = sum(Fx_body_i)
m*(dv/dt + r*u) = sum(Fy_body_i)
I_z*dr/dt       = sum(x_i*Fy_body_i - y_i*Fx_body_i)
```

หนึ่ง step ใช้ explicit Euler derivative ที่ start state:

```text
du/dt = a_x + r*v
dv/dt = a_y - r*u
dx/dt = cos(heading)*u - sin(heading)*v
dy/dt = sin(heading)*u + cos(heading)*v
dheading/dt = r
```

Result แสดง residual ของ vertical force, pitch moment, roll moment,
longitudinal force, lateral force และ yaw moment Residual เหล่านี้พิสูจน์เพียง
internal accounting ไม่ได้พิสูจน์ model fidelity

## หลักฐานอ้างอิง

`scripts/validate_lateral.py` ตรวจ:

- steady straight motion: หนึ่ง iteration และ residual ทั้งหกเป็นศูนย์ exact;
- positive front steering: lateral/yaw acceleration เป็นบวก;
- load-transfer analytical ที่ `a_x=2 m/s^2`, `a_y=3 m/s^2` มีทิศถูกต้องและ
  vertical/pitch/roll residual ศูนย์;
- combined-force saturation โดย applied utilization ไม่เกิน `1`; และ
- replay exact พร้อม iteration budget ที่จงใจให้ไม่พอแล้วคืน `invalid`

Test suite ยังครอบคลุม layout delta สาม contact, geometry rank ไม่พอ, contact
lift โดยไม่ clip, dynamic balance, invalid contract และ deterministic replay

## ข้อจำกัดและขอบเขตงานต่อ

- ไม่มี heave, pitch/roll dynamics, suspension travel, compliance, camber,
  relaxation length, contact-patch transient หรือ road roughness
- ไม่มี aerodynamic force หรือ aerodynamic load transfer; เป็นขอบเขต Work 017
- ไม่มี mechanical/regen braking-system หรือ suspension model; เป็นขอบเขต Work
  018
- ไม่มี calibrated tyre data, racing line จริง, sector geometry coupling หรือ
  physical-validation claim
