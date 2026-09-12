# แผน Work 128: ความทนทานในการแข่งแบบ Held-Out

แหล่งภาษาอังกฤษ: `2026-09-12_128_heldout-race-robustness-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

ประเมิน finalist และ controller ที่ตรึงจาก Work 127 บนชุด synthetic race conditions ที่ไม่เคยเห็นและถูก seal โดยไม่มี tuning, repair หรือเปลี่ยน threshold หลังเปิดเผย ตรึง hash ของ finalist, evaluator, rules และ holdout; รัน paired trajectory ที่ลงทะเบียนทั้งหมด; เก็บ failure และส่งต่อ environment/numerical uncertainty เข้าการเปรียบเทียบที่ลงทะเบียน

การทดลองทำสำเร็จได้แม้เป็น negative result robust superiority ต้องผ่าน paired time effect, complete-race rate, energy, thermal และ structural gates ที่ลงทะเบียนเพิ่มเติม Numerical completion ไม่ใช่ physical validation

## ตัวแปร controls และไฟล์

- IV: finalist ที่ตรึงและกรณี held-out environment/load/initial-condition ที่ seal
- DV: completion, race time หน่วย `s`, primary energy หน่วย `J`, thermal/structural margin, paired interval และ failure distribution
- Controls: ปฏิเสธ training condition ที่นำกลับมาใช้, source hash ที่เปลี่ยน, incomplete race ที่ซ่อน, tuning หลัง exposure และ threshold ที่แก้ทีหลัง
- สำเร็จเมื่อ: identities เปลี่ยนไม่ได้, telemetry ครบทุกคู่ที่ลงทะเบียน, uncertainty analysis, exact replay และ decision ที่จำกัดขอบเขต

ไฟล์ที่วางแผน: `src/formula_ultimate/experiments/heldout_race_robustness.py`, `config/development/heldout_race_robustness_v1.json`, `scripts/development/run_heldout_race_robustness.py`, `tests/test_heldout_race_robustness.py`, สัญญาสองภาษา `docs/contracts/HELDOUT_RACE_ROBUSTNESS_V1*`, plan/result สองภาษานี้ และ `artifacts/work128/run_a|run_b` ที่ ignore

## การตรวจสอบ

```powershell
python -m unittest tests.test_heldout_race_robustness tests.test_repository_contract -v
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_a
python scripts/development/run_heldout_race_robustness.py --config config/development/heldout_race_robustness_v1.json --output-root artifacts/work128/run_b --replay-reference artifacts/work128/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ของ Work 127 ที่ได้รับผลและตรวจ staged/cached diff โดยตรง; commit ทันทีเมื่อทุก gate ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

synthetic race telemetry อาจสะท้อนสมมติฐานของแบบจำลองมากกว่าพฤติกรรมเมื่อผลิตจริง finalist ที่เปลี่ยนทำให้ admission เป็น invalid และต้องใช้ holdout ใหม่ สิ่งที่ไม่ทำ: repair หลังเห็นผล, external novelty, physical validation, promotion จาก Level 0, push หรือ rewrite history
