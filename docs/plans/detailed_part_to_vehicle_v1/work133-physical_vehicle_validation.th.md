# Work 133: โปรแกรมตรวจรถทั้งคันเมื่อได้รับอนุญาต

ต้นฉบับภาษาอังกฤษ: `work133-physical_vehicle_validation.md`

Status: Planned

หมายเลขเดิมใน Work 106: 132

พึ่งพา: Work 128, Work 129, Work 130, Work 131, Work 132

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

สร้างหลักฐานวัดของรถ configuration ที่แน่นอนผ่าน test envelope เป็นขั้นซึ่งผู้มีความสามารถทบทวน

คำอ้างดิจิทัลอิสระ การตรวจผลิต/ประกอบ และหลักฐาน physical subsystem ที่เกี่ยวข้อง; ต้องมีอนุญาตชัดและสถานที่พร้อม

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/experiments/physical_vehicle_validation.py`
- `config/development/physical_vehicle_validation_v1.json`
- `scripts/development/run_physical_vehicle_validation.py`
- `tests/test_physical_vehicle_validation.py`

## 3. ขั้นลงมือทำ

1. ทบทวน hazards ที่ยัง unresolved, instrumentation และการ abort/recovery กับผู้มีความสามารถ
2. ล็อก configuration และคำทำนาย กำหนดเกณฑ์ขยายช่วงทดสอบก่อนเดินเครื่อง
3. ให้ผู้ได้รับอนุญาตทำเฉพาะ stages ที่อนุมัติ บันทึก incidents และ configuration changes ทั้งหมด
4. เทียบพฤติกรรม/ขีดจำกัดทั้งระบบที่วัดกับคำทำนาย ออกข้อสรุปตามขอบเขต

## 4. การทดลอง

- IV: vehicle configuration ที่อนุมัติ และเงื่อนไข environment/operation แต่ละขั้น
- DV: completion/time, energy, thermal/structural response, controllability ที่วัด และ model discrepancy
- Controls: เงื่อนไขย้อนที่มาได้และ measurement uncertainty; รถที่นำมาเทียบต้องมีโอกาสที่อนุมัติเทียบเท่า

## 5. Tests และการหักล้าง

audit offline ตรวจการขยาย stage ไม่อนุมัติ hardware/control เปลี่ยน failures หาย energy records ไม่ครบ และ extrapolation ไม่เหมาะสม

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก safety bounds จาก qualified review, กฎเข้า/ออก stage, measurement plan และขอบเขตคำอ้าง performance/safety ที่แน่นอน

เฉพาะ stages ที่อนุมัติและหลักฐานวัดใช้ได้รองรับข้อสรุป incidents, ข้อมูลขาด หรือ discrepancy unresolved หยุด promotion ได้แม้รถเคลื่อนที่

## 7. สิ่งส่งมอบและงานรับต่อ

configuration/test dossiers, telemetry เปลี่ยนย้อนหลังไม่ได้ incident reports, uncertainty analysis และ validation statement ตามขอบเขตทดสอบ

กำหนดขอบเขตทางกายภาพที่ทำได้และช่องว่างวิจัยใหม่ คำอ้างเพิ่มต้องงานหมายเลขใหม่และอำนาจอนุญาต

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

นี่เป็นโปรแกรมที่ต้องแยกงานทดสอบอนุมัติเล็ก ๆ ไม่ใช่รันไร้คนดูครั้งเดียว ไม่อนุญาตแข่งอัตโนมัติ ใช้ถนน รับรองความปลอดภัย หรือรับประกันเหนือกว่า

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_physical_vehicle_validation tests.test_repository_contract -v
python scripts/development/run_physical_vehicle_validation.py --config config/development/physical_vehicle_validation_v1.json --output-root artifacts/work133/run_a
python scripts/development/run_physical_vehicle_validation.py --config config/development/physical_vehicle_validation_v1.json --output-root artifacts/work133/run_b --replay-reference artifacts/work133/run_a/result.json
```
