# โมเดลแรงรวม Tyre-Road

สถานะ: ดำเนินการแล้วสำหรับ Work 011

ต้นฉบับภาษาอังกฤษ: `TYRE_ROAD_MODEL.md`

## จุดประสงค์และขอบเขตของข้ออ้าง

โมเดล Work 011 เป็นด่านความสามารถของแรงที่ทำซ้ำได้สำหรับ contact patch ของ
tyre หนึ่งจุด โมเดลป้องกันการใช้ grip longitudinal เต็มและ lateral เต็มอย่าง
อิสระพร้อมกัน โดยยังเก็บแรงที่ agent ร้องขอจริงและแรงที่ใช้จริงแยกกัน

นี่คือ friction circle/ellipse เชิงวิเคราะห์ ไม่ใช่โมเดล tyre ที่ calibrate แล้ว
และไม่ได้ยืนยันสมรรถนะ tyre จริง การยืนยันทางฟิสิกส์ ความปลอดภัย หรือความแม่น
ของเวลาแข่งขันต่อรอบ

## Contract ของหน่วยและเครื่องหมาย

- แรงและ normal load ใช้นิวตัน (`N`)
- สัมประสิทธิ์แรงเสียดทานและ utilization ไม่มีหน่วย
- เครื่องหมายบวก/ลบของ request longitudinal/lateral ใช้ได้ทั้งคู่ ขีดความ
  สามารถสมมาตรใน force quadrant ทั้งสี่
- Normal load ต้องไม่ติดลบ และสัมประสิทธิ์แรงเสียดทานต้องเป็นบวก
- แรงที่ร้องขอไม่ถูกเขียนทับ โดยแรงที่ใช้จริงและ residual เป็น output แยก

## Friction ellipse

สำหรับ normal load `Fz > 0`, สัมประสิทธิ์ longitudinal `mu_x`, สัมประสิทธิ์
lateral `mu_y` และแรงที่ร้องขอ `Fx_req`, `Fy_req`:

```text
Fx_limit = mu_x Fz
Fy_limit = mu_y Fz

u_requested = sqrt(
    (Fx_req / Fx_limit)^2 +
    (Fy_req / Fy_limit)^2
)
```

เมื่อ `mu_x = mu_y` ขอบเขตนี้เป็น friction circle หากไม่เท่ากันจะเป็น ellipse

```text
if u_requested <= 1 + boundary_tolerance:
    scale = 1
else:
    scale = 1 / u_requested

Fx_applied = scale Fx_req
Fy_applied = scale Fy_req
residual   = requested - applied
```

การฉายแบบ radial ในพิกัด normalized รักษาทิศทางแรงและวาง request ที่เกินขอบ
ไว้บน combined-force boundary โดยไม่ clip แต่ละแกนอย่างอิสระ

ค่าเริ่มต้น `boundary_tolerance` คือ `1e-12` และต้องไม่เกิน `1e-6` ค่า
requested/applied utilization ดิบยังแสดงอยู่ รวมถึงค่าที่สูงกว่าหนึ่งเล็กน้อย
แต่ยังอยู่ใน tolerance

## สถานะที่สังเกตได้

| สถานะ | ความหมาย |
|---|---|
| `within_limit` | Request ไม่เปลี่ยนภายใน tolerance ที่ประกาศ |
| `saturated` | Request ถูกฉายแบบ radial ลงบน ellipse |
| `no_contact_zero_request` | Load ศูนย์และ request ศูนย์ ไม่มีแรงส่งผ่าน |
| `no_normal_load` | Load ศูนย์แต่ request ไม่เป็นศูนย์ แรงใช้จริงเป็นศูนย์และ request ทั้งหมดยังคงเป็น residual |

เมื่อ request ไม่เป็นศูนย์แต่ normal load ศูนย์ requested utilization ไม่ถูก
นิยามและแทนด้วย `None` ไม่ใช่ infinity หรือ NaN การ underflow/overflow ของแกน
capacity ให้ `TyreNumericalError` ส่วน input ที่ invalid ให้ `TyreInputError`

## Analytical references

เมื่อ `mu_x = mu_y = 1`, `Fz = 4000 N` และ request `(3000, 4000) N`:

```text
u_requested = 1.25
scale = 0.8
applied = (2400, 3200) N
residual = (600, 800) N
u_applied = 1.0
```

test ขอบเขต anisotropic ใช้ `mu_x = 1.5`, `mu_y = 1.0`, `Fz = 4000 N`,
`Fx = 3000 N` และ `Fy = 4000 sqrt(0.75) N`; utilization เท่ากับหนึ่งภายใน
ความละเอียด floating-point และแรงไม่เปลี่ยน

ใช้คำสั่ง:

```powershell
python scripts/validate_tyre.py
python -m unittest tests.test_tyre -v
```

## ข้อจำกัดและงานถัดไป

- ไม่มี slip ratio, slip angle, stiffness, relaxation length, aligning moment,
  camber, pneumatic trail, load sensitivity, temperature, wear, degradation,
  ความหยาบผิว, ความลึกน้ำ หรือ aquaplaning
- coefficient เป็น input ที่ประกาศ ไม่ใช่ข้อมูลวัดใน work item นี้
- contact patch เดียวไม่คำนวณ normal-load transfer, axle balance, yaw หรือ
  พฤติกรรม suspension
- Work 016 อาจใช้กฎ capacity นี้ใน lateral/yaw dynamics แต่ต้องรักษาหลักฐาน
  requested/applied force และ saturation
- Work 012 ถัดไปจะ implement typed energy/powertrain flow และห้ามอนุมานการใช้
  พลังงานจากแรงโดยไม่มี contract ของความเร็วและ loss ที่ชัดเจน
