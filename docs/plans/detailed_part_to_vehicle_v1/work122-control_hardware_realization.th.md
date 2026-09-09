# Work 122: controller, sensor และฮาร์ดแวร์รองรับ

ต้นฉบับภาษาอังกฤษ: `work122-control_hardware_realization.md`

Status: Planned

หมายเลขเดิมใน Work 106: 121

พึ่งพา: Work 119, Work 120

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ทำให้การรับรู้และ actuation มี hardware, mounting, signal paths, authority จำกัด และพลังงานรองรับจริง

actuator envelope Work 119, supply Work 120 และ interfaces Work 112; ระบุอะไร measured/estimated

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/subsystems/control_hardware_realization.py`
- `config/development/control_hardware_realization_v1.json`
- `scripts/development/run_control_hardware_realization.py`
- `tests/test_control_hardware_realization.py`

## 3. ขั้นลงมือทำ

1. นิยามสถานะที่ต้องสังเกตและ sensor/signal pathways ที่ทำได้จริง
2. แทน geometry ของ sensor/controller/ส่วนรองรับ actuator, connectors, mounting และ supply loads
3. พัฒนา latency, noise, saturation และ fault behavior ตามสมมติฐานที่ลงทะเบียน
4. ประเมิน controller ร่วมและโหมดปรับด้วยงบเท่ากัน คิดต้นทุน tuning

## 4. การทดลอง

- IV: ตำแหน่ง/คุณสมบัติ hardware, controller parameters, noise, delay และ failure states
- DV: tracking/stability metrics, sensing error, energy, mass และต้นทุน adaptation
- Controls: task, actuator limits และโอกาส tuning รวมเดียวกัน

## 5. Tests และการหักล้าง

sensor dropout, signal ขาด, supply หมด, actuator saturation และ delay เพิ่ม; parameter controller ที่ไม่มีผลจริงไม่นับเป็น mutation มีประโยชน์

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกขอบเขต sensor/actuator, sample interval, noise/delay models, tuning budget และ error criteria

ทุกเส้นทาง sensing/actuation ที่อ้างมี hardware/accounting รองรับ comparisons รวมขีดจำกัดจริงและต้นทุน adaptation เท่ากัน

## 7. สิ่งส่งมอบและงานรับต่อ

hardware CAD/manifest, signal graph, closed-loop traces, fault report และ tuning ledger

ส่งให้ closed-loop simulation Work 123 และ fair controller comparisons Work 127

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

การเห็น state ครบอุดมคติอาจซ่อน hardware ที่ต้องใช้ ต้องติดป้าย idealization สำรวจ ไม่อ้าง electronics ขั้นสูงทุกชนิดหรือรับรอง controller ความปลอดภัย

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_control_hardware_realization tests.test_repository_contract -v
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_a
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_b --replay-reference artifacts/work122/run_a/result.json
```
