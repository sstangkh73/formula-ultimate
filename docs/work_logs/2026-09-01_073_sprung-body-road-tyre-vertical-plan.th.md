# แผน Work 073: การเชื่อม Sprung-Body Heave/Pitch/Roll ถนน และความยืดหยุ่นแนวดิ่งของยาง

สถานะ: เสร็จสมบูรณ์ (Completed)

เอกสารต้นฉบับภาษาอังกฤษ: `2026-09-01_073_sprung-body-road-tyre-vertical-plan.md`

## วัตถุประสงค์และขอบเขต

แทนที่ vertical boundary ที่ยังไม่ได้แก้ใน Work 072 ด้วยระบบแนวดิ่งเชิงเส้นที่เชื่อม sprung-body heave, pitch, roll; unsprung displacement หนึ่งค่าต่อ contact ที่ได้จาก geometry; spring/damper ช่วงล่าง; spring/damper แนวดิ่งของยาง และ road displacement แบบ deterministic โดย actual tyre normal load ต้องย้อนเข้า combined-force ellipse ของ Work 071 ภายใน fixed point acceleration/load ชุดเดียวกัน

งานนี้เป็น whole-vehicle vertical-dynamics gate สังเคราะห์ระดับ Level 0 บน geometry v3 จาก Work 069 และ drivetrain/planar dynamics แนวราบจาก Work 071 ที่ไม่เปลี่ยน ต้องรักษาผล Work 072 เมื่อไม่ได้เลือก Work 073 แสดงเส้นทางพลังงานแนวดิ่งทุกทาง และล้มเหลวโดยไม่ clipping เมื่อ contact loss หรือ suspension travel หมด

## คุณสมบัติจาก Geometry และพิกัด

มวล ground-contact component ยังคงเป็น effective unsprung mass จาก Work 072 Sprung mass คือผลรวมมวล architecture component ทุกชิ้นที่ไม่ได้ถูกกำหนดเป็น ground contact ส่วน roll/pitch inertia ของ sprung body ประกอบจาก primitive centroidal inertia และ parallel-axis term ของ component เหล่านั้นรอบจุดศูนย์กลางมวลรถที่ประกาศ Loader ต้อง reconcile identity เหล่านี้กับ materialized architecture

displacement แนวดิ่งทั้งหมดวัดจากสมดุลสถิตและค่าบวกชี้ขึ้น Generalized coordinates คือ:

```text
q = [z_s, theta, phi, z_u1, z_u2, z_u3]
```

โดย `z_s` คือ sprung heave, `theta` คือ pitch รอบแกน `y` ของตัวรถ, `phi` คือ roll รอบแกน `x` และ `z_ui` คือตำแหน่ง unsprung แต่ละจุด ที่ contact `(x_i, y_i)` เทียบกับจุดศูนย์กลางมวลรถ:

```text
z_body_i = z_s - x_i theta + y_i phi
s_i = z_ui - z_body_i
t_i = z_road_i - z_ui.
```

`s_i` คือ suspension compression และ `t_i` คือ tyre compression

## สมการและการเชื่อม

แรงส่วนเพิ่มของช่วงล่างและยางคือ:

```text
F_s,i = k_s,i s_i + c_s,i s_dot_i
F_t,i = k_t,i t_i + c_t,i t_dot_i
N_actual,i = N_0,i + F_t,i.
```

ระบบเชิงเส้นที่ประกอบแล้วคือ:

```text
M q_ddot + C q_dot + K q = f_inertial(a_x, a_y) + f_road(z_road, z_dot_road).
```

ความเร่งแนวราบสร้าง generalized force pitch/roll ที่แสดงชัดเจนรอบความสูงจุดศูนย์กลางมวล `h`:

```text
Q_theta = -m a_x h
Q_phi   =  m a_y h.
```

ระบบเดินหน้าด้วย implicit midpoint ในทุก fixed-point iteration ของ Work 071 โหลดเป้าหมาย quasi-static ใช้เพียงสร้าง inertial forcing `a_x/a_y` ปัจจุบัน จากนั้น Work 073 แก้ vertical state และคืน `N_actual` ให้ tyre model เมทริกซ์ singular, state ไม่ finite หรือ residual เกินกำหนดเป็น invalid และ commit ไม่ได้

## บัญชีพลังงาน

พลังงานสะสมแนวดิ่งประกอบด้วย kinetic energy ของ sprung/unsprung, suspension spring energy และ tyre spring energyเทียบกับตำแหน่งถนนปัจจุบัน การสูญเสียประกอบด้วย suspension-damper และ tyre-damper heat งานภายนอกคือ:

```text
W_inertial = Q_inertial dot (q_body,new - q_body,old)
W_road = sum(F_t,i z_dot_road,i dt)
R_vertical = delta(E_vertical) + Q_suspension_damper + Q_tyre_damper
             - W_inertial - W_road.
```

พลังงานแนวดิ่งเริ่มต้นทั้งหมดต้องถูกหักจากงบ storage คงที่ `50,000,000 J` Road work ยังคงเป็น external input ที่แสดงชัดเจน บัญชีแนวราบและแนวดิ่งแยกกันและรวมเฉพาะผ่าน conservation residual ที่ประกาศ

## การออกแบบการทดลอง

- ตัวแปรอิสระ: เครื่องหมายมุมเลี้ยว time step, mass/inertia จาก geometry, stiffness/damping ช่วงล่าง, tyre vertical stiffness/damping และ amplitude/start/duration ของ road profile ต่อ contact
- ตัวแปรตาม: heave/pitch/roll และ rate, unsprung state, suspension/tyre deflection, actual load, แรงแนวดิ่งทั้งหมด, stored energy, damper heat, inertial/road work, force/energy residual, วิถี/yaw แนวราบ, terminal state และ replay identity
- ตัวควบคุม: การรักษา Work 072, flat-road reference, เลี้ยวศูนย์, opposite-steer mirror, raised-cosine bump จุดเดียวและ spatial mirror, zero tyre damping, soft-tyre scale, road-drop contact loss, large-bump travel failure, exact replay และ half-step refinement
- สมมติฐานที่ต้องการทดสอบ: ความเร่งแนวราบบน flat road กระตุ้น heave/pitch/roll ที่ finite ขณะที่ contact ทุกจุด valid; mirror control สลับสถานะซ้าย/ขวา; bump สร้าง road work ไม่เป็นศูนย์และ local load response; zero tyre damping ให้ tyre heat เป็นศูนย์; ยางอ่อนเปลี่ยนผลตอบสนอง และ road control รุนแรงล้มเหลวอย่างชัดเจน
- เงื่อนไขหักล้าง: นับ mass/inertia ซ้ำ, เครื่องหมาย pitch/roll ผิด, tyre target load ข้าม vertical dynamics, ถนนเคลื่อนโดยไม่มีงาน, damping สร้างพลังงาน, hidden clipping, contact identity ขาด, นำ singular solve มาเป็น valid, hash Work 072 เปลี่ยน หรือ mirror/replay/refinement ไม่ผ่าน

## ไฟล์ที่วางแผน

- `config/vehicle/sprung_body_road_tyre_vertical_v1.json`
- `src/formula_ultimate/simulation/sprung_body_vertical_coupling.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_sprung_body_vertical_coupling.py`
- `tests/test_sprung_body_vertical_coupling.py`
- `docs/research/SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.md`
- `docs/research/SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.th.md`
- result records สองภาษาของ Work 073
- หลักฐาน deterministic ที่ ignore ใน `artifacts/work073/`

## การตรวจสอบและเกณฑ์สำเร็จ

1. Loader derive sprung mass และ roll/pitch inertia จาก architecture component ที่ไม่ใช่ ground และ reject identity/mass closure mismatch
2. ตัวควบคุม Work 072 ที่ไม่เลือก Work 073 ต้องรักษา committed result SHA-256
3. implicit-midpoint matrix solve ต้องปิด generalized equations ทั้งหกและสมการพลังงานแนวดิ่งภายใน tolerance สัมพัทธ์ `1e-9`
4. พลังงานรวมเริ่มต้นต้องเท่ากับ `50,000,000 J` พอดี
5. flat-road reference ต้องจบ 500 steps ด้วย actual load เป็นบวก travel อยู่ใน `0.05 m` และมี body-mode response finite ที่ไม่เป็นศูนย์
6. actual tyre load ต้องเป็นโหลดเดียวกับที่ Work 071 ใช้คำนวณ contact force capacity
7. มุมเลี้ยวศูนย์ต้องสมมาตรซ้าย/ขวา opposite steer ต้อง mirror roll, unsprung state ซ้าย/ขวา, load และสถานะระนาบ/yaw ที่เลือก
8. raised-cosine bump ต้องสร้าง signed road work ไม่เป็นศูนย์และ local load response ที่สังเกตได้ ส่วน spatial mirror ต้องสลับหลักฐานซ้าย/ขวา
9. zero tyre damping ต้องให้ tyre-damper heat เป็นศูนย์พอดี และ soft-tyre response ต้องต่างจาก reference
10. road-drop และ large-bump controls ต้องจบเป็น `contact_loss` หรือ `suspension_travel` โดยไม่ clipping
11. exact replay, half-step refinement `<= 2%`, focused/full tests, compilation, bilingual repository contract, scoped commit และ post-commit clean-tree replay ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

แบบจำลอง linear small-angle นี้ยังไม่มี nonlinear linkage kinematics, motion ratio จาก CAD joint, bump stop, tyre enveloping/contact-patch pressure, chassis flex, anti-dive/squat geometry, damper hysteresis, gyroscopic coupling ของล้อ, aero downforce, measured road spectra และ sub-step failure localization Horizontal inertial forcing ใช้มวลรถทั้งหมดและความสูงจุดศูนย์กลางมวลที่ประกาศ ขณะที่ sprung properties ตัด ground component ออก ข้อตกลงนี้แสดงชัดเจนแต่ยังไม่ได้ calibrate ด้วยการทดลอง

Work 073 ไม่เพิ่ม path control, ขอบสนาม, lap timing, suspension CAD ละเอียด, structural FEA, measured parameter identification หรือ physical validation และยังพิสูจน์ความพร้อมแข่งขันไม่ได้
