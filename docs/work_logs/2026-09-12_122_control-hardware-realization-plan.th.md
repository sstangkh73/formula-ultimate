# แผน Work 122: Controller, Sensor และฮาร์ดแวร์รองรับ

แหล่งภาษาอังกฤษ: `2026-09-12_122_control-hardware-realization-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

ทำ signal path แบบ sensor-controller-actuator ที่มีขอบเขตหนึ่งเส้นทางให้มี sensor, controller, harness, connector, mount และ actuator-interface hardware ชัดเจน ตรึง actuator authority จาก Work 119 และ supply จาก Work 120; แยก signal synthetic/estimated จากหลักฐาน measured

สร้าง sampled closed-loop reference ที่ทำซ้ำได้พร้อม noise, latency, saturation, dropout, signal disconnection และ supply exhaustion ที่ลงทะเบียน เปรียบเทียบ parameter ของ common-controller และ adapted-controller ด้วย tuning budget สี่ evaluation เท่ากัน และปฏิเสธ parameter mutation ที่ไม่มีผลเชิงเหตุ

## ตัวแปร control และไฟล์

- IV: ตำแหน่ง/คุณสมบัติ hardware, proportional gain, sample delay, deterministic noise, dropout, signal connectivity, supply และ actuator limit
- DV: tracking RMSE/final error, จำนวน saturation/dropout, energy, hardware mass และ tuning cost
- Controls: task/authority/budget เดียวกัน; dropout, signal ขาด, supply หมด, saturation, delay เพิ่ม และ noncausal mutation
- Success: path ทุกเส้นมี hardware ที่นับ, finite limit ทำงาน, tuning ที่ match คิด failures/evaluation, control เป็นเชิงเหตุ และ exact replay ผ่าน

ไฟล์ที่วางแผน: `src/formula_ultimate/subsystems/control_hardware_realization.py`, `config/development/control_hardware_realization_v1.json`, `scripts/development/run_control_hardware_realization.py`, `tests/test_control_hardware_realization.py`, contract `docs/contracts/CONTROL_HARDWARE_REALIZATION_V1*` สองภาษา, plan/result สองภาษาชุดนี้ และ `artifacts/work122/run_a|run_b` ที่ไม่ติดตามใน Git

## การตรวจสอบ

```powershell
python -m unittest tests.test_control_hardware_realization tests.test_repository_contract -v
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_a
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_b --replay-reference artifacts/work122/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 119/120 และตรวจ staged/cached diff แบบระบุไฟล์ จะ commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Reference plant, noise, latency และข้อมูล hardware เป็น synthetic สิ่งที่ไม่ทำ: ideal full-state observation, arbitrary electronics, safety-critical certification, stability ของ controller จริง, physical validation, push หรือแก้ประวัติ
