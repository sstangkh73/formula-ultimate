# การ coupling พลังงานกลางและ health state

ไฟล์ต้นฉบับภาษาอังกฤษ: `CENTRAL_ENERGY_HEALTH_COUPLING.md`

## ขอบเขต

Work 027 เชื่อม wheel work, auxiliary demand, regeneration, brake heat, aerodynamic cooling conductance, lumped thermal state, degradation, damage และ seeded reliability ที่ประกาศ โมเดลยังเป็นระบบ evidence/event localization ระดับ Level 0 ไม่ใช่ calibrated physical validation

## เจ้าของพลังงาน

- applied local contact force บวกสร้าง no-slip `drive_wheel_energy_j = F_x r omega dt`
- drive source demand คือ `drive_wheel_energy_j / drive_efficiency`
- auxiliary demand คือ `auxiliary_power_w * dt`
- recovered storage energy, conversion loss และ mechanical brake heat มาจาก Work 025 และต้องปิดสมดุลกับ wheel energy removed
- ใช้ recovered energy ที่มีอยู่ก่อน primary energy โดย recovery ที่เข้าระหว่าง interval มีส่วนใน average-rate store balance ที่ประกาศ
- recovered capacity overflow เป็น invalid และ solver ไม่ clip

typed energy audit อิสระสามชุดตรวจ propulsion chain, auxiliary chain และ aggregate braking/recovery boundary ส่วน `ResidualEntry` ห้ารายการแสดง central-store, contact-braking และ audit residual

## การหาเวลาเหตุการณ์

Work 025 rerun contact ทุกตัวถึง positive contact failure ที่เร็วสุดก่อน จากนั้น central energy solverหา depletion แบบ analytical จาก net demand rate ส่วน health solver สร้าง candidate สำหรับ energy depletion, contact failure, component thermal failure, degradation/damage limit และ seeded reliability hazard ราย component

`arbitrate_event_candidates` เลือกเวลาที่เร็วสุดและใช้ priority ที่ประกาศเฉพาะ tolerance tie ระบบคำนวณหรือ localize energy, component thermal state, degradation, damage, motion และ final time ถึง duration ที่เลือก

สำหรับ constant acceleration ที่อนุมานจาก candidate ของ Work 026 การ localize motion ใช้สมการ kinematic ที่สอดคล้องกัน ส่วน race-distance progress localize ตามสัดส่วนภายใน prospective step หาก central event เกิดก่อน contact physics ที่ประเมินแล้ว persistent contact state จะคงค่าเริ่มต้นแทนการ interpolate แบบเท็จ เหตุการณ์ terminal สังเกตได้และห้ามเดิน step ต่อ

## สัญญา thermal และ cooling

central component แต่ละตัวประกาศ lumped `ThermalParameters`, base heat generation, สัดส่วน loss/cooling, กฎ degradation/damage, limit และ reliability hazard โดยผลรวม loss fraction และ cooling fraction แต่ละชุดเท่ากับหนึ่ง

Mechanical brake heat เป็นของ contact brake thermal model และไม่ถูกเพิ่มใน central component ค่า aerodynamic `conductance_w_per_k` แทน active component conductanceตามสัดส่วนที่ประกาศ ส่วน `heat_rejection_w` เก็บเป็น reference evidence และไม่ลบซ้ำ Ambient temperature เป็น configuration บังคับ ไม่มี neutral default แบบซ่อน

## สัญญา seed

แต่ละ component ได้ random stream แบบ deterministic ที่สร้างด้วย SHA-256 จาก `(random_seed, step_index, component_id)` ลำดับ registration เปลี่ยน draw ไม่ได้ Same-seed replay ตรง exact ส่วน seed ต่างเปลี่ยน draw evidence แต่ไม่จำเป็นต้องเปลี่ยนเหตุการณ์ที่ชนะหากมี deterministic event ที่เร็วกว่า

## Architecture

`coupled-level0-reference-v3` เก็บ v2 และเพิ่ม `energy.residuals` กับ `state.motion_candidate` เข้า health stage Energy/health adapter version คือ `work027-central-energy-v1` และ `work027-central-health-v1`

## หลักฐานจาก validator

- wheel work `900 J` ที่ efficiency `0.9` ต้องใช้ source energy `1000 J`; auxiliary demand `100 J` ทำให้ primary จาก `2000 J` เหลือ `900 J`
- braking `1000 J` ปิดเป็น recovered `700 J` + conversion loss `100 J` + mechanical heat `200 J`
- store `550 J` ภายใต้ net demand `1100 W` depletion ที่ `0.5 s` โดยพลังงานไม่ติดลบ
- thermal fixture ถึง `302 K` ที่ `0.2 s`; motion localize ที่ `x = 2 m` และ replay ตรง exact

## ข้อจำกัด

Wheel work สมมติ no slip ความร้อนและ degradation ของ component เป็น lumped model Reliability hazard เป็น synthetic และไม่ได้ calibrate Cooling ใช้ conductance ไม่ใช่ CFD เมื่อ central event ตัดก่อนและไม่มี input สำหรับ rerun Work 018 แบบ exact ระบบจะรักษา contact state เริ่มต้น ข้อจำกัดเหล่านี้ห้ามอ้าง physical validation หรือ safety
