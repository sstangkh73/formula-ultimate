# Aerodynamic Chassis และ Normal-Load Coupling

ต้นฉบับภาษาอังกฤษ: `AERO_CHASSIS_LOAD_COUPLING.md`

## Boundary

Work 024 เชื่อม declared weather แบบ `local_enu` และ shared motion state เข้ากับ
aerodynamic map จาก Work 017, translate wrench มาที่ centre of mass และ project
normal load บน contact topology ใดก็ได้ที่ไม่ rank-deficient พร้อม emit signal set
ตรงของ `aerodynamic_map` และ `normal_load_solver`

declared weather เป็น `observed` หรือ `synthetic_control` ได้ โดยใช้ numerical
path ร่วมกัน แต่ typed status และ scenario fingerprint รักษา evidence class ไว้
synthetic control ไม่กลายเป็นหลักฐานสนามจริง

ยังเป็น Level 0; synthetic coefficient และ analytical weather ไม่ใช่ CFD,
measurement, calibration, safety หรือ physical validation

## Axis และ Wrench Translation

Body axes คือ `x` หน้า, `y` ซ้าย, `z` ขึ้น Map drag/downforce บวกกลายเป็น body
force `(-drag, side, -downforce)` Intrinsic moment คือ `(0, pitching_moment,
yawing_moment)` และ reference origin `r` จาก centre of mass translate ด้วย:

```text
M_com = M_map + r x F
```

Raw/query airspeed/yaw และ numerical node snap ถูกเก็บใน
`AerodynamicQueryEvidence`

## Atmosphere และ Relative Wind

Observed pressure, temperature, relative humidity สร้าง moist-air density จาก
ideal dry-air/water-vapour mixture กับ Tetens saturation pressure จากนั้นนำ vehicle
velocity ลบ `local_enu` wind และ rotate เข้า body axis ด้วย yaw

Coordinate-transform roundoff snap เข้า declared node ได้เฉพาะใน `1e-12` และมี
หลักฐานบันทึก ค่าออก envelope มากกว่านั้น invalid พร้อม write ศูนย์ ไม่มี physical
clamp

## Normal-Load Equilibrium

Solver เปลี่ยน baseline load น้อยที่สุดใน Euclidean sense โดยปิดสามสมการ เมื่อ
aero force `(Fx,Fy,Fz)`, COM moment `(Mx,My,Mz)`, acceleration `(ax,ay)`, mass
`m`, COM height `h` และ contact coordinate `(xi,yi)`:

```text
sum(Ni)      + Fz - m*g       = 0
sum(xi*Ni)   + m*ax*h - My    = 0
sum(yi*Ni)   + m*ay*h + Mx    = 0
```

Raw vertical/pitch/roll residual emit เป็น SI `ResidualEntry` Rank-deficient
geometry, negative contact load หรือ residual fail ทำให้ adapter invalid; ไม่ clip
หรือ redistribute load เงียบ

## Evidence

Analytical validator ได้ drag `-525.9915 N`, downforce `-1051.9830 N`, cooling
heat rejection `17620.7160 W` และ pitch moment จาก forward origin `1051.9830
N*m` Front load เพิ่มเป็น `2978.4915 N` ต่อจุด ขณะที่ rear `2452.5 N`;
vertical/roll residual เป็นศูนย์และ pitch `-9.09e-13 N*m` Query speed นอก map
invalid และ emit ศูนย์

Test ครอบคลุม humidity density direction, ENU rotation, replay, symmetric
downforce, forward load shift, arbitrary three-contact topology, contact-ID
mismatch, rank deficiency, lift และ invalid declaration

## ข้อจำกัดและงานถัดไป

Acceleration estimate ยังเป็น adapter configuration จน Work 026 ปิด motion
feedback งานนี้ไม่ resolve tyre/suspension/brake Work 025 ต้อง consume contact
load โดยไม่ redistribute เงียบ Level-0 balance ไม่พิสูจน์ real aerodynamics หรือ
structural feasibility
