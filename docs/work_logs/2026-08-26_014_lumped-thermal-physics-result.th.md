# ผลลัพธ์ Work 014: Lumped Thermal, Cooling, Derating และ Failure Physics

ต้นฉบับภาษาอังกฤษ: `2026-08-26_014_lumped-thermal-physics-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 014 เสร็จสมบูรณ์ repository มี lumped thermal step แบบ exact สำหรับ input
คงที่ พร้อม passive/active Newton cooling, temperature derating เชิงเส้น,
analytical first-failure event localization, failure latch และ energy residual
ที่สังเกตได้ โดยไม่ clip temperature แบบเงียบ

สมมติฐานได้รับการสนับสนุนภายในขอบเขต Level-0: cooling ไม่พอทำให้เกิด failure
ในเวลาจำกัด และป้องกัน caller ใช้เวลาที่ไม่ได้ execute ที่เหลือเสมือนว่าสำเร็จ

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/thermal.py`: contract SI input/state, exact
  temperature integration, derating, event localization, failure latch,
  passive/active exchange ที่มีเครื่องหมาย และ energy residual
- `src/formula_ultimate/physics/__init__.py`: public thermal API export
- `tests/test_thermal.py`: test 11 รายการสำหรับ analytical, failure, energy,
  invalid-input, numerical-failure และ replay
- `scripts/validate_thermal.py`: reference heating, cooldown และ failure
- `docs/physics/THERMAL_MODEL.md` และ `.th.md`: สมการ ความหมายสถานะ หลักฐาน
  boundary และข้อจำกัด
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` และ `.th.md`: สถานะ Work 014
- คู่ plan/result Work 014 ภาษาอังกฤษและไทยนี้

ไม่ต้องสร้าง problem report แยก Numerical overflow, state ที่เริ่มเหนือ threshold
และ state ที่ failed แล้วถูกประกาศใน plan และจัดการเป็น error/status ที่ชัดเจน
พร้อม test

## การตัดสินใจและหลักฐานฟิสิกส์

1. Component เป็น thermal mass สม่ำเสมอหนึ่งก้อน มี `C` หน่วย `J/K`
2. Passive/active cooling ที่สั่งเป็น conductance `W/K`; active command จำกัด
   `[0,1]`
3. Heat/conductance คงที่ถูก integrate ด้วย exact exponential solution หรือ
   exact linear adiabatic solution เมื่อ conductance ศูนย์
4. Heat rejected มีเครื่องหมายและแบ่งตามสัดส่วน conductance Storage change และ
   energy residual แสดงชัดเจน
5. Derating เชิงเส้นจาก `T_derate` ถึงศูนย์ที่ `T_fail`
6. Threshold crossing หยุดที่ analytical event การกำหนด event temperature คือ
   event localization ไม่ใช่ post-step clipping และแยก requested/executed time
7. Failure ย้อนกลับไม่ได้ในโมเดลนี้; step หลังให้ `already_failed`

## การทบทวนการทดลอง

- Independent variables: `C`, passive/active conductance, cooling command,
  heat generation, ambient/initial temperature, threshold และ duration
- Dependent variables: temperature, rejected/storage energy, residual,
  derating, executed/unexecuted time, status และ failure time
- Controls: หน่วย SI, input คงที่, exact closed form, event rule เดียว และไม่มี
  ความสุ่ม
- Metrics: temperature/failure-time error และ energy residual
- หลักฐานสนับสนุน: adiabatic `300 -> 301 K`; Newton cooldown เท่ากับ
  `333.1091497054298 K`; equilibrium คงที่; active conductance เย็นกว่าและแยก
  energy ได้
- หลักฐานหักล้าง: `C=1000 J/K`, `P=1000 W`, `350 K`, ไม่มี cooling เกิด
  failure ตรง `50 s / 400 K`; เหลือ `50 s` จาก request `100 s` ที่ไม่ execute
  และ follow-up recover ไม่ได้
- ไม่พบหลักฐานขัดแย้งใน analytical reference set
- คำอธิบายทางเลือก: cooldown เทียบกับ exponential reference ที่เขียนอิสระ
  ไม่ใช่เรียก implementation ซ้ำ
- หลักฐานที่ขาด: gradient จาก geometry, parameter calibrated, coolant,
  radiation, auxiliary energy, material aging และ hardware test
- ความมั่นใจสูงต่อสมการ/ซอฟต์แวร์ในขอบเขต constant-input หนึ่ง node; ไม่มีต่อ
  hardware performance หรือ safety จริง

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` พร้อม fail-fast exit handling

```powershell
python -m unittest tests.test_thermal -v
```

Exit status: `0`; `Ran 11 tests`; `OK`

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`; `Ran 100 tests`; `OK`

```powershell
python scripts/validate_thermal.py
```

Exit status: `0`; ผลสำคัญ:

```text
adiabatic end_temperature_k: 301.0
Newton analytical/end_temperature_k: 333.1091497054298
failure status: failed
failure_time_s/executed_duration_s: 50.0
unexecuted_duration_s: 50.0
latched: true
temperature_silently_clipped: false
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status `0` ทุกคำสั่ง รัน full fail-fast validation ซ้ำหลังเพิ่ม result นี้
และรัน `git diff --cached --check` หลัง stage แบบระบุขอบเขตก่อน commit

## ข้อจำกัดและงานต่อเนื่อง

- หนึ่ง node แก้ internal hotspot หรือ thermal contact geometry ไม่ได้
- Input คงที่ใน step และไม่ใช่หลักฐาน calibrated
- Work 014 ยังไม่คิด cooling auxiliary energy
- ไม่มี radiation, coolant mass/flow, boiling, aging หรือ fire
- Work 015 ต้องส่ง derating, latched failure และ unexecuted time ไปเป็น race
  outcome ที่ล้มเหลว โดย Work 015 ยังไม่เริ่มใน work item นี้
- รายงาน verified commit hash ใน final handoff และไม่ push remote
