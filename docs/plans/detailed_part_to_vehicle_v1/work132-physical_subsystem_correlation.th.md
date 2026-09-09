# Work 132: เทียบ subsystem จริงและความทนทานเมื่อได้รับอนุญาต

ต้นฉบับภาษาอังกฤษ: `work132-physical_subsystem_correlation.md`

Status: Planned

หมายเลขเดิมใน Work 106: 131

พึ่งพา: Work 131

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ตรวจพฤติกรรม coupled subsystem ที่เลือกและ endurance ที่เกี่ยวข้องใน physical test envelope ที่อนุมัติ

ขอบเขตย่อยที่สอบเทียบจาก Work 131 และ packages subsystem ที่เกี่ยวข้องทั้งหมด; ต้องทบทวน safety/authorization เฉพาะ subsystem ใหม่

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/experiments/physical_subsystem_correlation.py`
- `config/development/physical_subsystem_correlation_v1.json`
- `scripts/development/run_physical_subsystem_correlation.py`
- `tests/test_physical_subsystem_correlation.py`

## 3. ขั้นลงมือทำ

1. เลือก subsystem/คำอ้างและรวม dossier geometry, model, instruments และ safety
2. ล็อกคำทำนาย coupled, test sequence, duration/cycles ที่อนุมัติ และสิ่งสังเกต failure
3. เก็บการวัดที่อนุญาตพร้อมบันทึก boundary/energy และ abort ครบ
4. วิเคราะห์ losses, degradation และ uncertainty; recalibrate เฉพาะข้อมูลที่กำหนดแล้ว validate ใหม่

## 4. การทดลอง

- IV: ประวัติ load/thermal/control ที่อนุมัติและ subsystem configuration ที่ตรวจ
- DV: coupled response, efficiency/loss, degradation, failure onset และ prediction error
- Controls: fixture/environment ที่อนุมัติและ instrumentation ย้อนที่มาได้เหมือนกัน แยก validation runs ที่ยังไม่ใช้

## 5. Tests และการหักล้าง

pipeline offline ตรวจ boundary power หาย เปลี่ยนชิ้นโดยไม่บันทึก calibration leakage, ซ่อน aborts และ sensors ขัดแย้ง

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก loads/cycles ที่อนุมัติ ช่วง material/model, endurance claim, uncertainty และ stop criteria ไม่ extrapolate อายุสากล

การวัดย้อนที่มาได้ผ่าน claim criteria ที่ลงทะเบียนหรือให้ผลลบมีขอบเขต calibration ย่อยอย่างเดียวไม่ยืนยัน subsystem

## 7. สิ่งส่งมอบและงานรับต่อ

raw data subsystem, ประวัติ energy/loss/degradation, discrepancy analysis และ dossier ขอบเขตใช้ที่ปรับ

ส่งหลักฐาน subsystem ที่ผ่านขอบเขตและความเสี่ยง unresolved ให้รถทั้งคัน Work 133

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

การทดสอบ subsystem เดียวไม่รับรองสถาปัตยกรรมอื่นหรืออายุใช้งานครบ การเปลี่ยนสภาพทำงานอันตรายต้องอนุญาตแยก วิเคราะห์ offline เท่านั้น

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_physical_subsystem_correlation tests.test_repository_contract -v
python scripts/development/run_physical_subsystem_correlation.py --config config/development/physical_subsystem_correlation_v1.json --output-root artifacts/work132/run_a
python scripts/development/run_physical_subsystem_correlation.py --config config/development/physical_subsystem_correlation_v1.json --output-root artifacts/work132/run_b --replay-reference artifacts/work132/run_a/result.json
```
