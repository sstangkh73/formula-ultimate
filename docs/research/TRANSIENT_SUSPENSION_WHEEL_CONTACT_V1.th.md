# การเชื่อมช่วงล่างและจุดสัมผัสล้อแบบ Transient V1

ต้นฉบับภาษาอังกฤษ: `TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.md`

## ขอบเขตคำกล่าวอ้าง

Work 072 เพิ่มสถานะแนวดิ่งแบบ transient ที่ deterministic ให้ทุกจุดสัมผัสของ Work 071 และส่งแรงกดปกติจริงกลับเข้าไปในการคำนวณแรงยาง งานนี้ทดสอบคำกล่าวอ้างระดับ software ที่แคบว่า มวลล้อ/ตัวรองรับที่ระบุจาก geometry, spring และ damper ที่ประกาศ, ขีดแรงยาง, การเคลื่อนที่ระนาบ, yaw, ดิฟเฟอเรนเชียล และบัญชีพลังงานสามารถทำงานใน transaction ระดับ Level 0 ที่ converge ร่วมกันได้

ผลนี้ไม่ใช่ physical validation ไม่ใช่ช่วงล่างสมบูรณ์ และไม่ใช่หลักฐานความพร้อมแข่งขัน ค่า spring/damper เป็น input การทดลองสังเคราะห์ architecture ที่ materialize ยังคงเดิมโดยมี SHA-256 `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`

## แบบจำลอง

แต่ละจุดสัมผัสใช้มวล component ที่ได้จาก geometry เป็น effective unsprung mass: `13.30024665823775 kg` ต่อ ground unit หน้าที่ขับเคลื่อน และ `4.342937684322531 kg` สำหรับตัวรองรับหลังแบบ passive จุดสัมผัสที่ขับเคลื่อนใช้ `k = 35,000 N/m` และ damping ratio `0.35`; จุด passive ใช้ `k = 50,000 N/m` และ damping ratio `0.4` ทุกจุดประกาศ compression/rebound travel `0.05 m`

วัด displacement `z` จากสมดุล static preload โดยค่าบวกหมายถึง compression โหลด quasi-static จาก Work 071 กลายเป็น `N_target` ส่วน spring-damper oscillator กำหนดโหลดที่ยางใช้:

```text
delta_N = N_target - N_0
m z_ddot = delta_N - k z - c z_dot
N_actual = N_0 + k z_mid + c z_dot_mid.
```

ใช้ implicit-midpoint integration โดยส่ง `N_actual` ไม่ใช่ `N_target` เข้า combined tyre-force ellipse ของ Work 071 ภายใน fixed point acceleration/load ชุดเดียวกัน โหลดจริง `<= 0 N` ให้ `contact_loss` และ travel นอก envelope ให้ `suspension_travel` โดยไม่มีการ clipping

พลังงานแนวดิ่งถูก audit แยก:

```text
E = 0.5 m z_dot^2 + 0.5 k z^2
W_boundary = delta_N (z_new - z_old)
Q_damper = c z_dot_mid^2 dt
R = delta(E) - W_boundary + Q_damper.
```

`W_boundary` แทนการแลกเปลี่ยนพลังงานกับโหมดแนวดิ่งของ sprung body ที่ยังไม่ได้จำลองอย่างชัดเจน พลังงาน perturbation เริ่มต้นถูกหักจากงบ storage ร่วม `50,000,000 J`

## การออกแบบการทดลอง

- ตัวแปรอิสระ: เครื่องหมายมุมเลี้ยว time step, stiffness, damping และ initial travel/velocity ที่ควบคุมไว้
- ตัวแปรตาม: target/actual normal load, travel, velocity, acceleration, แรง spring/damper, energy/work/heat, แรง/การใช้ขีดจำกัดยาง, วิถี, yaw, สถานะดิฟเฟอเรนเชียล, terminal state และ identity hash
- ตัวควบคุม: rigid Work 071, เลี้ยวศูนย์, เลี้ยวตรงข้าม, zero damping, stiffness ครึ่งหนึ่ง, contact-loss perturbation, travel-exhaustion perturbation, exact replay และ half-step refinement
- สมมติฐานที่ต้องการทดสอบ: actual load ต่างจาก target และเปลี่ยนการตอบสนองแนวราบ invariant สมมาตร/mirror ต้องคงอยู่ damping ต้องสลายพลังงานเท่านั้น และสถานะที่เป็นไปไม่ได้ต้องล้มเหลวอย่างมองเห็นได้
- เงื่อนไขหักล้าง: ยางใช้ target แทน actual load, ซ่อน load/travel clipping, geometry identity ผิด, undamped heat ไม่เป็นศูนย์, มีพลังงานอธิบายไม่ได้, mirror/replay/refinement ไม่ผ่าน หรือยังส่งแรงหลัง failure

## ผลการทดลอง

reference จบครบ 500 steps ด้วยมุมเลี้ยว `+0.01 rad`, throttle `0.3`, ระยะเวลา `0.5 s` และ `dt = 0.001 s` ตำแหน่งระนาบสุดท้ายคือ `(5.369677667803904, 0.13391224133502547) m` และ yaw rate สุดท้าย `0.3637589747733689 rad/s`

ช่วง actual normal load ของ reference คือ `282.92044294869817` ถึง `1597.6137536723597 N` ความต่าง target-to-actual สูงสุด `96.89914047704144 N` แสดงการตอบสนอง transient ที่ไม่ rigid travel สูงสุด `0.011753827694854656 m` และความเร็วแนวดิ่งสูงสุด `0.19365997408307992 m/s` สถานะสุดท้ายคือ:

- ซ้าย: `z = -0.011753827694854656 m`, `z_dot = -0.016030373931809734 m/s`
- หลัง: `z = 0.0026632563500025683 m`, `z_dot = -0.010840790285720183 m/s`
- ขวา: `z = 0.007851425941973965 m`, `z_dot = 0.031545417354367576 m/s`

vertical boundary work สะสมที่แสดงชัดเจนคือ `4.606168739325264 J` และ damper heat คือ `0.9238099457339569 J` force residual สูงสุด `3.979039320256561e-13 N`, suspension-energy residual สูงสุด `8.296586074402201e-16 J` และ total global relative residual สูงสุด `5.010984838008881e-9`

มุมเลี้ยวศูนย์รักษาสมมาตรช่วงล่างซ้าย/ขวาและสถานะ lateral/yaw เป็นศูนย์พอดี การเลี้ยวตรงข้ามสลับ travel/velocity ซ้ายขวาและ mirror สถานะระนาบ/yaw โดย mismatch ที่บันทึกเป็นศูนย์ ตัวควบคุมไม่มี damping ให้ damper heat `0 J` พอดี การลด stiffness ครึ่งหนึ่งเพิ่ม travel สูงสุดจาก `0.011753827694854656 m` เป็น `0.02332339540361481 m` จึงขัดกับคำอธิบายที่ว่าสถานะแนวดิ่งเป็นเพียง telemetry ที่ไม่ได้เชื่อมแรง

ตัวควบคุม contact loss เริ่มจุดซ้ายที่ `-0.03 m` transaction แรกเก็บ actual load `-329.1330469175954 N` ไว้ ไม่ commit step ที่ล้มเหลว และคืน `DNF: contact_loss` ตัวควบคุม travel เริ่มจุดขวาที่ `0.049 m` และ `1.0 m/s`; ระบบ commit สอง deterministic steps เก็บค่าเกิน travel `0.05068991458357319 m` และคืน `DNF: suspension_travel` พลังงานช่วงล่างเริ่มต้น `15.75 J` และ `48.66762332911888 J` ถูกหักจาก storage ทำให้พลังงานรวมเริ่มต้นยังเท่ากับ `50,000,000 J` พอดี

ความต่าง half-step แบบสัมพัทธ์สูงสุดคือ `0.008650825751444935` ที่ damper heat สะสม ต่ำกว่า gate `0.02` ไฟล์ evidence primary/replay ตรงกันทุกไบต์ด้วย file SHA-256 `E48CA5034D8361C5E45AAF2D88BA5FC1349015AAD4144345CB5CBFD2AE66B719` ส่วน canonical evidence payload ระบุตัวเองเป็น `25b269082eb921efc54c334c6dc3d9623bcb7d6fa91beb9d2ea9b4083270b97b`

ตัวควบคุม Work 071 ที่ไม่ใช้ transform ยังคง result SHA-256 `f8f3d888b23a9e21b7bb9ad8b7153ecd5bd4752c7937ebf8cc42a952b64c9cdd` แสดงว่า extension hook ไม่เปลี่ยนแบบจำลองเดิม

## การตีความ หลักฐานที่ขัดแย้ง และข้อจำกัด

หลักฐานสนับสนุนคำกล่าวอ้างระดับ software ว่าสถานะช่วงล่างแบบ transient เปลี่ยนแรงกดปกติของยางอย่างเป็นเหตุเป็นผล และจึงเปลี่ยนแรง/การเคลื่อนที่แนวราบ อีกทั้งสนับสนุนสมการแรง/พลังงานของ oscillator ที่ประกาศ และหักล้างแนวคิดว่าระบบซ่อม contact/travel failure แบบเงียบ

ผลนี้ไม่ได้แสดงว่าค่าสัมประสิทธิ์หรือการเคลื่อนที่ทำนายรถจริง residual ที่ดีอาจแสดงเพียงความสอดคล้องของสมการภายใน effective mass คือมวล ground component ทั้งชิ้นจาก geometry ไม่ใช่ unsprung modal mass ที่วัดจริง boundary work มาจากโหมด heave/pitch/roll ที่ยังไม่ได้แก้ ไม่ได้มี tyre vertical stiffness, road displacement, linkage motion ratio, roll centre, anti-dive/squat, bump stop, hysteresis, aero load, ข้อมูลวัด หรือ sub-step event localization ความเชื่อมั่นสูงต่อ deterministic coupling และต่ำต่อความแม่นยำในโลกจริง

ก่อนกล่าวอ้าง whole-vehicle dynamics ที่เข้มแข็ง fidelity ขั้นถัดไปควรปิด sprung-body heave/pitch/roll และ road/tyre vertical compliance แล้วจึงเชื่อมรถเข้ากับ closed-loop path และ circuit gate
