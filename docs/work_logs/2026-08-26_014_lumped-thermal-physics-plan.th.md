# แผน Work 014: Lumped Thermal, Cooling, Derating และ Failure Physics

ต้นฉบับภาษาอังกฤษ: `2026-08-26_014_lumped-thermal-physics-plan.md`

สถานะ: Completed

## วัตถุประสงค์

Implement โมเดล lumped-capacitance thermal ที่ทำซ้ำได้ แปลง heat generation,
การแลกเปลี่ยนกับ ambient และ active conductance ที่สั่ง เป็น temperature,
derating, energy accounting และเหตุการณ์ over-temperature failure แบบถาวร
โดยไม่ clip temperature แบบเงียบ

## ขอบเขต

- กำหนด contract SI เข้มงวดสำหรับ thermal parameter, state, step input,
  derating, failure state และ telemetry
- Integrate heat generation คงที่กับ Newton cooling แบบ exact ในแต่ละ step
- แยก passive/active heat exchange energy และแสดงค่าที่มีเครื่องหมาย
- ใช้ derating factor เชิงเส้นจากอุณหภูมิเริ่ม derate ถึงศูนย์ที่ failure
- หา over-temperature crossing แรกแบบ analytical, ลด executed interval ถึง
  event นั้น, latch failure และแสดง requested time ที่ไม่ได้ execute
- เก็บ energy residual ต่อ step ห้ามแก้ invalid/non-finite state แบบเงียบ
- เพิ่ม test heating, cooldown, equilibrium, derating, failure crossing,
  already-failed, invalid-input, conservation และ deterministic replay
- เพิ่ม validator, เอกสาร model/result สองภาษา, อัปเดต queue, validate และ
  commit แยกก่อน Work 015

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/thermal.py`
- `src/formula_ultimate/physics/__init__.py`
- `tests/test_thermal.py`
- `scripts/validate_thermal.py`
- `docs/physics/THERMAL_MODEL.md` และ `THERMAL_MODEL.th.md`
- สถานะ queue และคู่ plan/result สองภาษานี้
- problem report แยกสองภาษาเฉพาะเมื่อพบปัญหาที่มีสาระ

## สมมติฐานและสมการ

Component เป็น thermal mass สม่ำเสมอเชิงพื้นที่หนึ่งก้อน มี heat capacity `C`
(`J/K`) Ambient temperature และ heat generation คงที่ใน step Passive cooling
และ active cooling ที่สั่งเป็น conductance:

```text
G = G_passive + command * G_active
C dT/dt = P_heat - G (T - T_ambient)
```

เมื่อ `G > 0`:

```text
T_eq = T_ambient + P_heat / G
T(t) = T_eq + (T0 - T_eq) exp(-G t / C)
```

เมื่อ `G = 0`, `T(t) = T0 + P_heat t / C` Total exchange energy derive จาก
`P_heat*t - C*(T1-T0)` และแบ่งตาม passive/active conductance ค่า exchange ติดลบ
หมายถึง ambient ให้ความร้อนแก่ component ที่เย็นกว่า

Derating เท่ากับหนึ่งที่หรือต่ำกว่า `T_derate`, ลดเชิงเส้น และเป็นศูนย์ที่
`T_fail` Failure ถูก latch และ step หลังจากนั้นไม่ resume อัตโนมัติ

## นิยามการทดลอง

- สมมติฐาน: cooling และ failure-event physics ที่ชัดเจนป้องกัน agent ใช้ power
  สร้างความร้อนไม่จำกัด โดยยังเห็นผล energy/derating
- Independent variables: heat capacity, passive/active conductance, command,
  heat generation, ambient/initial temperature, threshold และ duration
- Dependent variables: end temperature, exchange energy, storage change,
  residual, derating factor, executed time, status และ failure time
- Controls: หน่วย SI, input คงที่ต่อ step, exact closed-form integration,
  event rule เดียว และไม่มีความสุ่ม
- Metrics: analytical temperature error, energy residual, failure-time error
  และ deterministic equality
- Success: analytical reference ตรงภายใน floating-point tolerance, residual
  เล็กตาม scale และ event/status ถูกต้อง
- Failure/falsification: adiabatic heating/Newton cooldown ต้องตรง closed form;
  equilibrium คงที่; cooling ไม่พอต้องข้าม/latch failure; failed state ห้าม
  recover แบบเงียบ; ค่า invalid ต้องล้มเหลว

## ความเสี่ยง

- โมเดลหนึ่ง node ไม่เห็น internal gradient/hotspot
- Conductance เป็น input ที่ประกาศ ไม่ใช่หลักฐาน CFD/test
- Exact integration exact เฉพาะ input คงที่ภายใน step
- Event termination เหลือ requested time ที่ไม่ได้ execute; loop ขั้นถัดไปต้อง
  ถือเป็น failure ไม่ใช่จบสำเร็จ

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี spatial mesh, coolant inventory, phase change, radiation, fan/pump
  energy, material aging, fire, thermal contact network หรือ calibration
- ไม่อ้าง physical validation จาก Level 0
- ไม่ทำ Work 015 และไม่ push remote

## Validation

```powershell
python -m unittest tests.test_thermal -v
python -m unittest discover -s tests -v
python scripts/validate_thermal.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

ทุก gate รันแบบ fail-fast การเสร็จงานต้องมี result pair, staged scope ที่ระบุ,
commit สำเร็จ และตรวจ clean state/hash หลัง commit
