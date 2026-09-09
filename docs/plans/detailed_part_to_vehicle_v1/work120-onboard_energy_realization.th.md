# Work 120: การทำระบบพลังงานบนรถให้เกิดจริงอย่างละเอียด

ต้นฉบับภาษาอังกฤษ: `work120-onboard_energy_realization.md`

Status: Planned

หมายเลขเดิมใน Work 106: 119

พึ่งพา: Work 115, Work 116, Work 119

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ทำเส้นทาง storage/conversion บนรถที่ระบุขอบเขตหนึ่งเส้นทางให้ครบ รวม geometry ภายใน containment, loss และขีดจำกัดพลังงานใช้ได้

ports Work 119 และกติกา primary-energy ภายนอกเดิม; หลักฐาน material/thermal จาก Works 115/116

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/subsystems/onboard_energy_realization.py`
- `config/development/onboard_energy_realization_v1.json`
- `scripts/development/run_onboard_energy_realization.py`
- `tests/test_onboard_energy_realization.py`

## 3. ขั้นลงมือทำ

1. ล็อก energy boundary, stored state เริ่มต้น, capacity/rate และ reference technology ที่รองรับ
2. แทนภายใน storage/conversion, enclosure, insulation, connectors และ mounting
3. ติดตาม input, output, stored energy ที่เปลี่ยน และ losses ที่จำลองทั้งหมด โดยไม่มีการเติมพลังงานภายนอก
4. ส่งขีดจำกัด temperature/rate และโหลด containment ไปสู่ geometry/assembly models

## 4. การทดลอง

- IV: geometry ภายใน การจัด storage, rate demand และ thermal environment
- DV: primary energy ใช้ได้ กำลังส่ง ความร้อน มวลครบ และสถานะขีดจำกัด
- Controls: โอกาสพลังงานภายนอก task และการนับ initial state เหมือนกันข้ามเส้นทาง

## 5. Tests และการหักล้าง

storage หมด สั่งเกินขีด converter ขาด มวล containment ถูกละ และเติมพลังงานลับ ปฏิเสธหน่วย/energy boundary ขัดกัน

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก constitutive/data validity, energy budget, capacity/rate/temperature limits และ residual tolerances

บัญชี energy และ hardware ครบสำหรับเส้นทางที่เลือก ฟิสิกส์ chemistry/field/conversion ที่ขาดบล็อกคำอ้างสูงขึ้น ไม่ห้ามข้อเสนอเทคโนโลยีอื่น

## 7. สิ่งส่งมอบและงานรับต่อ

ชุดพลังงานละเอียด state/loss ledger, มวลจาก geometry และขอบเขตใช้ที่รองรับ

ส่งให้ hardware supply Work 122 และ coupled energy integration Work 123

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

อันตราย containment/chemistry ต้องหลักฐานเฉพาะ นี่เป็นแผน simulation ไม่ใช่อนุญาตให้สร้างหรือจ่ายพลังงานฮาร์ดแวร์ ไม่อ้าง technology-neutrality เกินโอกาสที่ตรวจ

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_onboard_energy_realization tests.test_repository_contract -v
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_a
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_b --replay-reference artifacts/work120/run_a/result.json
```
