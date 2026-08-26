# โมเดล Lumped Thermal, Cooling, Derating และ Failure

สถานะ: ดำเนินการแล้วสำหรับ Work 014

ต้นฉบับภาษาอังกฤษ: `THERMAL_MODEL.md`

## จุดประสงค์และขอบเขตของข้ออ้าง

Work 014 เพิ่ม thermal node ที่ทำซ้ำได้หนึ่ง node ต่อ component ที่ model โดย
แปลง heat และ ambient conductance ที่ประกาศเป็น temperature, power-availability
factor และ over-temperature event ที่ latch นี่คือโมเดล analytical ระดับ
Level-0 ไม่ใช่หลักฐานอุณหภูมิ hardware จริง ความปลอดภัย สมรรถนะ cooling หรือ
physical validation

## Contract SI และ exact step

Temperature ใช้ kelvin (`K`), heat capacity `J/K`, conductance `W/K`, power
`W`, time `s` และ energy `J` สำหรับ input คงที่ในหนึ่ง step:

```text
G = G_passive + cooling_command * G_active
C dT/dt = P_heat - G (T - T_ambient)
```

เมื่อ `G > 0`:

```text
T_eq = T_ambient + P_heat / G
T(t) = T_eq + (T0 - T_eq) exp(-G t / C)
```

เมื่อ `G = 0`, `T(t) = T0 + P_heat*t/C` Total heat rejected ที่ integrate
derive แยกจาก storage:

```text
E_rejected = P_heat*t - C*(T1 - T0)
residual = E_generated - E_passive - E_active - delta_E_stored
```

Passive/active rejected energy แบ่งตามสัดส่วน conductance และมีเครื่องหมาย:
ค่าติดลบหมายถึง ambient ที่อุ่นกว่าให้ความร้อนแก่ component ที่เย็นกว่า Residual
ยังเป็น output และไม่ถูกแก้ทิ้ง

## Derating และ failure

```text
factor = 1                                      if T <= T_derate
factor = (T_fail - T) / (T_fail - T_derate)    if T_derate < T < T_fail
factor = 0                                      if T >= T_fail
```

ถ้า requested step ข้าม `T_fail` ระบบแก้หา crossing time แรกจาก analytical
trajectory เดียวกัน Execute เฉพาะเวลาถึง event, end temperature คืออุณหภูมิ
event, รายงาน requested duration ที่เหลือเป็น unexecuted และ latch failure
step หลังจากนั้นให้ `already_failed` โดยไม่เดินเวลา State ที่เริ่มเหนือ threshold
เก็บอุณหภูมิจริงและให้ `failed_at_start` ไม่ clip กลับลงมา

## สถานะที่สังเกตได้

| สถานะ | ความหมาย |
|---|---|
| `normal` | Step จบโดยไม่เข้า derating |
| `derated` | จุดเริ่มหรือจบของ step ที่ complete อยู่ในช่วง derating |
| `failed` | Localize threshold crossing แรกภายใน requested step |
| `failed_at_start` | Input state ที่ยังไม่ latch อยู่ที่/เหนือ threshold แล้ว |
| `already_failed` | State ที่ latch ปฏิเสธการ execute ต่อ |

## หลักฐาน Analytical

- `C=1000 J/K`, `100 W`, `10 s`, ไม่มี cooling: `300 -> 301 K`
- `C=1000 J/K`, `G=100 W/K`, `390 K`, ambient `300 K`, `10 s`:
  `333.1091497054298 K` ตรง exponential closed form
- `C=1000 J/K`, `1000 W`, `350 K`, ไม่มี cooling, `T_fail=400 K`: failure
  ที่ `50 s`; requested step `100 s` เหลือ `50 s` ไม่ได้ execute

ใช้คำสั่ง:

```powershell
python scripts/validate_thermal.py
python -m unittest tests.test_thermal -v
```

## ข้อจำกัดและงานต่อเนื่อง

- Node สม่ำเสมอหนึ่ง node ไม่เห็น gradient/hotspot จาก geometry
- Conductance, heat capacity และ threshold เป็น input ที่ประกาศโดยไม่มี CFD,
  material หรือ test calibration ใน Work 014
- Input คงที่ใน step; controller ต้องเลือกระยะ step เอง
- Convection เป็นเชิงเส้น; ไม่มี radiation, coolant flow/inventory, phase change,
  contact resistance, fan/pump energy, aging และ fire
- Work 015 ต้องถือ `unexecuted_duration_s` และ latched failure เป็นผล race ล้มเหลว
  ห้ามถือเป็น step สั้นที่สำเร็จ
