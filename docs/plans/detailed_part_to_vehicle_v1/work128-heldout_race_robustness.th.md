# Work 128: การแข่ง held-out และความทนทาน

ต้นฉบับภาษาอังกฤษ: `work128-heldout_race_robustness.md`

Status: Planned

หมายเลขเดิมใน Work 106: 127

พึ่งพา: Work 127

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ประเมิน finalists ที่ล็อกในเงื่อนไขโจทย์ใหม่ที่ประกาศ โดยไม่ซ่อมหลังผลหรือรั่วจาก training

finalists Work 127, ที่มา holdout ที่ยังไม่ถูกใช้ และโจทย์ race/energy กำกับ

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/experiments/heldout_race_robustness.py`
- `config/development/heldout_race_robustness_v1.json`
- `scripts/development/run_heldout_race_robustness.py`
- `tests/test_heldout_race_robustness.py`

## 3. ขั้นลงมือทำ

1. ล็อก identities ของ candidate/controller/evaluator และ manifests เงื่อนไข held-out ก่อนเปิดเห็น
2. รัน trajectories ที่ลงทะเบียนครบ บันทึกทุก failure, stop และ attempt ที่ติดงบ
3. ส่งผ่าน numerical/material/environment uncertainty และประเมิน robustness metrics
4. เทียบผล finalists แบบจับคู่ เก็บหลักฐานลบและขอบเขตใช้ครบ

## 4. การทดลอง

- IV: candidate ที่ล็อกและความแปรผัน environment/load/initial-condition แบบ held-out
- DV: race completion/time, primary energy, thermal/structural margins และ uncertainty intervals
- Controls: เงื่อนไขใหม่และกฎเดียวกันทุก arm ไม่ tuning เพิ่มหลังเปิดเห็น

## 5. Tests และการหักล้าง

ต้องปฏิเสธการใช้ holdout ซ้ำ source hashes เปลี่ยน ซ่อนการแข่งไม่จบจาก summary และแก้ thresholds ภายหลัง

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก sample/condition design, statistical estimand, การจัด multiplicity เมื่อจำเป็น กฎ completion และ acceptance thresholds

comparison admitted ต้องมี freeze/leakage และ execution evidence ครบ คำอ้างเหนือกว่าอย่างทนทานต้องผ่าน effect/constraint gates ที่ลงทะเบียนเพิ่ม

## 7. สิ่งส่งมอบและงานรับต่อ

holdout manifests เปลี่ยนไม่ได้ telemetry รายรัน การกระจาย failures, uncertainty analysis และ comparative result

ส่งผลชี้ขาดและเงื่อนไขสำคัญให้ independent analysis Work 129

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

ถ้าเปลี่ยน finalists ชุดที่เห็นแล้วเป็น exploratory ต้องมี holdout ใหม่ การแข่งจำลองจบไม่ใช่ physical validation

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_heldout_race_robustness tests.test_repository_contract -v
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_a
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_b --replay-reference artifacts/work128/run_a/result.json
```
