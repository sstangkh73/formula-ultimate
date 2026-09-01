# แผน Work 072: การเชื่อมช่วงล่าง โหลดล้อ และจุดสัมผัสแบบ Transient

สถานะ: เสร็จสมบูรณ์ (Completed)

เอกสารต้นฉบับภาษาอังกฤษ: `2026-09-01_072_transient-suspension-wheel-contact-plan.md`

## วัตถุประสงค์และขอบเขต

ขยาย transaction ระนาบ/ดิฟเฟอเรนเชียล/การถ่ายน้ำหนักจาก Work 071 ที่ commit แล้ว โดยเพิ่มสถานะแนวดิ่งของช่วงล่างหนึ่งชุดต่อจุดสัมผัสที่ได้จาก geometry ผล load transfer แบบ quasi-static จะเป็น target load ส่วน effective unsprung mass, spring stiffness, damping, travel และ velocity จะกำหนดแรงกดปกติที่ยางใช้ได้จริงระหว่าง step

งานนี้เป็น gate เส้นทางโหลดแบบ transient สังเคราะห์ระดับ Level 0 บน geometry v3 จาก Work 069 และพลวัตแนวราบจาก Work 071 ที่ไม่เปลี่ยน ต้องแสดงการตอบสนองของโหลดที่ล่าช้า พลังงานช่วงล่าง การสูญเสียใน damper ระยะยุบสุดทาง การสูญเสีย contact และ numerical error ห้ามนำโหลดที่ถูกตัด จุดสัมผัสที่เสีย หรือ coupled step ที่ไม่ converge มาแสดงเป็นสถานะ valid

## แบบจำลองฟิสิกส์

ที่จุดสัมผัส `i` กำหนด displacement `z_i` จากสมดุล preload สถิต และค่าบวกหมายถึง compression ใช้มวล ground component ที่ได้จาก geometry เป็น effective unsprung mass `m_i` คำตอบ quasi-static จาก Work 071 ให้ target load `N_target,i` และ static preload คือ `N_0,i`:

```text
delta_N_i = N_target,i - N_0,i
m_i z_ddot_i = delta_N_i - k_i z_i - c_i z_dot_i
N_actual,i = N_0,i + k_i z_mid,i + c_i z_dot_mid,i.
```

oscillator เดินหน้าด้วย implicit-midpoint step โดย `N_actual,i` ไม่ใช่ `N_target,i` เป็นตัวกำหนด combined tyre-force ellipse ใน transaction ของ Work 071 callback ถูกประเมินภายใน fixed point ของ acceleration/load-transfer ชุดเดียวกัน ดังนั้น target load การตอบสนองช่วงล่าง แรงยาง ความเร่งตัวรถ ความเร็วล้อ และสถานะดิฟเฟอเรนเชียลต้อง converge ร่วมกัน

บัญชีพลังงานแนวดิ่งต่อจุดสัมผัสคือ:

```text
E_i = 0.5 m_i z_dot_i^2 + 0.5 k_i z_i^2
W_boundary,i = delta_N_i (z_new,i - z_old,i)
Q_damper,i = c_i z_dot_mid,i^2 dt
R_energy,i = delta(E_i) - W_boundary,i + Q_damper,i.
```

boundary work คือพลังงานที่แลกเปลี่ยนกับโหมด heave/pitch/roll ของ sprung body ซึ่งยังไม่ได้จำลอง โดยจะแสดงอย่างชัดเจนและไม่ดึงแบบเงียบจาก drivetrain แนวราบ พลังงาน perturbation ช่วงล่างตอนเริ่มต้องถูกหักจากงบ storage คงที่ `50,000,000 J` เพื่อไม่ให้ตัวควบคุมสร้างพลังงานแฝง

แรงกดจริง `<= 0 N` เป็น `contact_loss` แบบ terminal ส่วน compression หรือ rebound เกิน travel ที่ประกาศเป็น `suspension_travel` แบบ terminal ค่าจะถูกเก็บไว้โดยไม่ clipping V1 ตรวจเหตุการณ์เหล่านี้ที่ขอบ transaction แบบ deterministic การหาเวลาเหตุการณ์ย่อยภายใน step อย่างแม่นยำเป็น non-goal และข้อจำกัด

## การออกแบบการทดลอง

- ตัวแปรอิสระ: เครื่องหมายมุมเลี้ยว time step, effective mass ต่อ contact ที่ได้จาก geometry, spring stiffness, damping ratio, compression/rebound travel และ initial travel/velocity perturbation ที่ควบคุมไว้
- ตัวแปรตาม: target/actual normal load, travel, vertical velocity/acceleration, suspension energy, boundary work, damper heat, residual แรง/พลังงานแบบ dynamic, วิถี/yaw ระนาบ, ความเร็วล้อ/ดิฟเฟอเรนเชียล, tyre utilization, terminal reason/time และ replay hash
- ตัวควบคุม: rigid reference จาก Work 071, transient reference, มุมเลี้ยวศูนย์, opposite-steer mirror, zero damping, การเปลี่ยน stiffness, perturbation ที่ทำให้ contact loss ทันที, perturbation ที่ทำให้ travel หมด, exact replay และ half-step refinement
- สมมติฐานที่ต้องการทดสอบ: transient reference จบโดยโหลดเป็นบวกและ travel อยู่ในขอบเขต actual load ต่างจาก quasi-static target อย่างสังเกตได้ การเลี้ยว mirror สลับสถานะแนวดิ่งซ้าย/ขวา zero damping ให้ damper heat เป็นศูนย์ stiffness ที่อ่อนลงเปลี่ยนการตอบสนอง และ perturbation ที่เป็นไปไม่ได้ล้มเหลวเป็น contact loss หรือ travel exhaustion
- เงื่อนไขหักล้าง: ยางไม่ใช้ actual load, preload/component identity ไม่ตรง, มี hidden clipping, damping สร้างพลังงาน, residual แรง/พลังงานแนวดิ่งเกิน tolerance, เพิ่มพลังงาน perturbation นอกงบเริ่มต้น, mirror/replay/refinement ไม่ผ่าน หรือช่วงล่างเสียแล้วยังส่งแรง valid ต่อ

## ไฟล์ที่วางแผน

- `config/vehicle/transient_suspension_coupling_v1.json`
- extension hook ใน `src/formula_ultimate/simulation/coupled_planar_differential.py`
- `src/formula_ultimate/simulation/transient_suspension_coupling.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_transient_suspension_coupling.py`
- `tests/test_transient_suspension_coupling.py`
- `docs/research/TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.md`
- `docs/research/TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.th.md`
- result records สองภาษาของ Work 072
- หลักฐาน deterministic ที่ ignore ใน `artifacts/work072/`

## การตรวจสอบและเกณฑ์สำเร็จ

1. Loader ต้อง reconcile declaration Work 071 ที่ตรงกันทุกประการ materialized architecture, contact/component identity, static preload, component mass ที่ได้จาก geometry, contact limits และ numerical domain แบบ SI
2. Work 071 ที่ไม่ใช้ transform ต้องคง reference evidence ตรงกันทุกไบต์และผ่าน tests เดิม
3. ทุก transient contact ต้องปิดสมการแรง midpoint และสมการพลังงานแนวดิ่งภายใน tolerance สัมพัทธ์ `1e-9`
4. พลังงานรวมเริ่มต้นต้องเท่ากับ `50,000,000 J` พอดี รวม suspension kinetic/spring energy เริ่มต้นทุกกรณี
5. reference ต้องจบครบ 500 steps โดย actual load ทุกจุดเป็นบวก travel ทุกจุดอยู่ใน envelope และ actual load มีผลต่อ tyre utilization/force
6. มุมเลี้ยวศูนย์ต้องรักษาสมมาตรซ้าย/ขวา opposite steer ต้อง mirror suspension travel, velocity, load และสถานะระนาบ/yaw ที่เลือกภายใน tolerance
7. zero damping ต้องให้ damper heat เป็นศูนย์พอดี และ stiffness control ต้องเปลี่ยน frozen response metric อย่างน้อยหนึ่งค่า
8. contact-loss และ travel-exhaustion controls ต้องจบเป็น `DNF` อย่างชัดเจนโดยไม่ clipping หรือส่งแรงหลัง failure
9. ทั้ง horizontal energy gates จาก Work 071 และ suspension/global-with-boundary energy gates ใหม่ต้องผ่าน
10. exact replay, half-step refinement `<= 2%`, focused/full tests, compilation, bilingual repository contract, scoped commit และ post-commit clean-tree replay ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

oscillator หนึ่ง degree แบบสังเคราะห์นี้ไม่ได้แก้ tyre vertical stiffness, sprung-body heave/pitch/roll inertia, suspension linkage kinematics, motion ratio, roll centre, anti-dive/squat, bump stop, การเสียรูป geometry ล้อ, road displacement, tyre relaxation หรือ damping hysteresis ที่วัดจริง Geometry ให้ component identity และ effective mass แต่ค่า spring/damper เป็น input การทดลองที่ประกาศไว้ ไม่ได้มาจาก CAD หรือการวัด

Work 072 ไม่เพิ่ม brake actuation, การเชื่อม aero map, path control, ขอบสนาม, lap timing, structural FEA ของชิ้นส่วนช่วงล่าง, joints/fasteners แบบละเอียด, CAD solids หรือ physical validation และยังพิสูจน์ความพร้อมแข่งขันไม่ได้
