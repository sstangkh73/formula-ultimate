# Work 129: ตรวจคำกล่าวอ้างอิสระด้วย fidelity สูงขึ้น

ต้นฉบับภาษาอังกฤษ: `work129-independent_claim_validation.md`

Status: Planned

หมายเลขเดิมใน Work 106: 128

พึ่งพา: Work 125, Work 126, Work 127, Work 128

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ท้าทายกลไกและ margins ที่ชี้ขาดผลด้วย analysis ที่สร้างอิสระและเข้มขึ้น

geometry สุดท้าย source materials และ boundary histories จาก Works 125–128; ไม่คัดข้อสรุป solver เดิมมาเป็น inputs

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/experiments/independent_claim_validation.py`
- `config/development/independent_claim_validation_v1.json`
- `scripts/development/run_independent_claim_validation.py`
- `tests/test_independent_claim_validation.py`

## 3. ขั้นลงมือทำ

1. เลือกคำอ้างสำคัญตามผลกระทบและ uncertainty รวมกรณีลบ/ใกล้ขีดจำกัด
2. สร้าง mesh/model/การตีความขอบเขตอิสระ และบันทึกสมมติฐานร่วมอย่างชัดเจน
3. ใช้ฟิสิกส์ที่เข้มขึ้นและใช้ได้พร้อม refinement เทียบ fields เฉพาะที่และ response สำคัญต่อระบบ
4. จำแนก discrepancies เป็นตัวเลข แบบจำลอง หรือข้อมูล ปรับขอบเขตคำอ้างโดยไม่เขียนผลเดิมใหม่

## 4. การทดลอง

- IV: formulation/backend อิสระ fidelity และเงื่อนไขสำคัญ
- DV: field/response disagreement, ranking stability, margin ที่เปลี่ยน และ uncertainty
- Controls: candidate จริงและเงื่อนไขทางกายภาพเทียบเท่า ไม่จำเป็น mesh เดียวกัน

## 5. Tests และการหักล้าง

wrapper ที่ใช้ function เดียวกันไม่ผ่านความอิสระ ใส่การละแบบจำลองที่ทราบแล้วตรวจว่าการเทียบพบหรือไม่

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกการเลือกคำอ้าง declaration ความอิสระ ขอบเขต stronger model และเกณฑ์ตัดสิน discrepancy

คำอ้างที่เลือกต้องรอดการตรวจอิสระตามขอบเขตหรือถูกลดระดับพร้อมเหตุผล discrepancy ของ ranking/margin ที่อธิบายไม่ได้บล็อก promotion

## 7. สิ่งส่งมอบและงานรับต่อ

independent model package, comparison fields, discrepancy register และขอบเขตหลักฐานปรับใหม่

ส่งหลักฐานเฉพาะ candidate ให้ manufacturing Work 130 และแผนทดสอบของจริง

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

ซอฟต์แวร์อิสระอาจใช้สมมติฐานผิดร่วมกัน ต้องบันทึก common-mode uncertainty งานนี้ยังแทนการวัดจริงไม่ได้

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_independent_claim_validation tests.test_repository_contract -v
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_a
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_b --replay-reference artifacts/work129/run_a/result.json
```
