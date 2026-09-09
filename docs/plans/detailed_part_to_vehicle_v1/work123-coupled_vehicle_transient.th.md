# Work 123: ระบบรัน candidate ทั้งคันแบบ coupled transient

ต้นฉบับภาษาอังกฤษ: `work123-coupled_vehicle_transient.md`

Status: Planned

หมายเลขเดิมใน Work 106: 122

พึ่งพา: Work 117, Work 118, Work 119, Work 120, Work 121, Work 122

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

เชื่อม subsystem states และการแลกพลังงานจริงตามเวลาบน candidate revision เดียว รวมแบบสำรวจที่ยังไม่ครบ

ใช้ response models ที่ตรงขอบเขตและ physical interfaces; แสดงโดเมน unresolved ไม่เติม coefficients เอื้อเอง

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/simulation/coupled_vehicle_transient.py`
- `config/development/coupled_vehicle_transient_v1.json`
- `scripts/development/run_coupled_vehicle_transient.py`
- `tests/test_coupled_vehicle_transient.py`

## 3. ขั้นลงมือทำ

1. นิยามเจ้าของ state, time bases, initialization และการแลกตัวแปร interface
2. พัฒนา coupling iterations/events และบัญชี work/heat transfer ที่อนุรักษ์
3. รวม controller, ground, actuation, energy, structure และ cooling พร้อม validity checks
4. รัน trajectories ขอบเขตจำกัด refine time/coupling และ replay input identities ครบ

## 4. การทดลอง

- IV: architecture, subsystem variants, coupling step และโหมดปรับ controller
- DV: trajectory, completion, energy/heat residuals, failure margins และ integration error
- Controls: task/environment ภายนอกเดียวกันและ initial physical state สอดคล้อง

## 5. Tests และการหักล้าง

frames/signs ไม่ตรง power นับซ้ำ events หน่วง พลังงานหมด และแบบลดรูปนอกช่วง รันทดสอบ decoupled ซ้ำเพื่อหาต้นเหตุ

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก exchange schema, time-step ladder, coupling tolerance, stop/failure rules และ trial envelope

ผ่าน coupled reference และ numerical gates; โดเมนจำเป็น unresolved บล็อก promotion แต่ยังอยู่ใน exploratory runs ที่ระบุชนิดชัดได้

## 7. สิ่งส่งมอบและงานรับต่อ

state histories, interface energy ledger, เหตุออกนอก validity, convergence และ exact decision replay

เปิดโหมด vehicle-search Work 124 และ candidate comparisons Works 126–128

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

coupled harness ไม่ใช่รถรายละเอียดครบ อย่าอนุมานความพร้อมจากการรวมรันได้หรือวิ่งเส้นทางสั้น ไม่อ้าง physical validation

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_coupled_vehicle_transient tests.test_repository_contract -v
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_a
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_b --replay-reference artifacts/work123/run_a/result.json
```
