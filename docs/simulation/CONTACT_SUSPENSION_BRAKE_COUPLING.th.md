# Contact, Suspension, Brake และ Regeneration Coupling

ต้นฉบับภาษาอังกฤษ: `CONTACT_SUSPENSION_BRAKE_COUPLING.md`

## Boundary

Work 025 consume normal load จาก Work 024, typed strategy command และ shared
contact state แล้ว evaluate contact ที่มี unique ID แต่ละจุดผ่าน explicit
drive/brake allocation, Work 018 suspension/brake/regen และ Work 011 combined tyre
ellipse โดยไม่บังคับจำนวนล้อ, axle, symmetry หรือ driven-contact layout

## Explicit Allocation และ No Redistribution

Drive/brake allocation fraction ประกาศต่อ contact และแต่ละชุดต้องรวม `1` ภายใน
`1e-12` Global drive force/brake torque ถูก split ครั้งเดียว หาก contact หนึ่ง
saturate unmet force/torque ยังอยู่ที่จุดนั้น ไม่ใช้ spare capacity จุดอื่นเงียบ

Throttle กับ brake ที่ไม่เป็นศูนย์พร้อมกันถูก reject เพราะยังไม่มี blending policy
Contact ID ใน spec, load, shared state และ subsystem state ต้องตรงพอดี Wheel speed
ลบต้องมี reverse model ในอนาคตและไม่ถูกแปลงด้วย `abs()`

## ลำดับต่อ Contact

1. ใช้ central recovery fraction cap available regen torque
2. Evaluate subsystem torque capacity และ suspension response
3. แปลง longitudinal torque เป็น contact force และรวม lateral request ผ่าน tyre
   ellipse
4. หาก combined saturation ลด brake force ให้ rerun brake/regen/thermal ที่
   projected torque เพื่อให้ energy/temperature ตรง torque ที่ถนนรับ
5. Rotate local force ด้วย steer angle และคำนวณ `Mz = x*Fy - y*Fx`
6. เก็บ applied/unserved force, recovered energy, conversion loss, mechanical
   heat, storage margin, travel/failure state และ raw residual

Physical suspension/thermal failure เป็น health evidence ไม่ใช่ numerical
invalidity ส่วน malformed input หรือ conservation residual fail คืน atomic
invalidity พร้อม write ศูนย์

## Output และ Evidence

Adapter emit ตรง `contact.force_moment`, `contact.energy_transfers` และ
`contact.health_inputs` Residual ครอบคลุม suspension force, brake torque และ brake
energy ทุก contact

Validator ใช้ arbitrary three-contact topology Front contact load ต่ำจึงเหลือ
force unserved โดยไม่ redistribute Combined braking/steering แสดงว่า wheel energy
ต่อ contact ตรง applied longitudinal force คูณ effective radius, angular speed และ
duration พร้อม replay ตรง

## ข้อจำกัด

Tyre เป็น friction ellipse, suspension เป็น lumped, allocation ถูกประกาศไม่ใช่
optimized และ subsystem state ที่ configure ยังไม่ central commit Work 026 ต้อง
integrate summed contact/aero wrench เป็น longitudinal/lateral/yaw/race-distance
state เดียว Level-0 success ไม่ใช่ physical validation หรือ real-race evidence
