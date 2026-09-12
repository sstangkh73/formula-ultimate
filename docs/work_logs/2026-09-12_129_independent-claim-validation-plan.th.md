# แผน Work 129: การตรวจสอบ Claim แบบอิสระ

แหล่งภาษาอังกฤษ: `2026-09-12_129_independent-claim-validation-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

ท้าทาย claim ที่มีผลสูงสุดจาก Work 125–128 ด้วย formulation การวิเคราะห์ที่ประกาศแยกบน raw candidate telemetry ที่ล็อกไว้ โดยไม่คัดลอก upstream conclusion เข้าการคำนวณ คำนวณ paired time, energy และ margin evidence ใหม่ ใช้ conservative boundary interpretation ที่แรงกว่า ลงทะเบียน shared assumptions และจำแนก discrepancy ก่อนดู upstream decision

การตรวจต้องปฏิเสธ shared-function wrapper ว่าไม่เป็นอิสระ และสาธิตการจับ known omitted-boundary effect claim ที่รอดยังเป็น bounded numerical evidence; unexplained discrepancy หรือ common-mode assumption ที่ยังไม่คลี่คลายต้องปิดกั้น promotion

## ตัวแปร controls และไฟล์

- IV: independent formulation, conservative boundary correction, fidelity และ critical condition
- DV: response disagreement, ranking stability, minimum margins, discrepancy class และ revised evidence scope
- Controls: ปฏิเสธ backend/source module เดียวกัน; ฉีด known modeling omission และต้องตรวจพบ; ปฏิเสธ candidate หรือ telemetry identity ที่เปลี่ยน
- สำเร็จเมื่อ: คำนวณ claims ใหม่อย่างอิสระ, แสดง shared assumptions, จำแนก discrepancy, exact replay และไม่ rewrite upstream outcomes

ไฟล์ที่วางแผน: `src/formula_ultimate/experiments/independent_claim_validation.py`, `config/development/independent_claim_validation_v1.json`, `scripts/development/run_independent_claim_validation.py`, `tests/test_independent_claim_validation.py`, สัญญาสองภาษา `docs/contracts/INDEPENDENT_CLAIM_VALIDATION_V1*`, plan/result สองภาษานี้ และ `artifacts/work129/run_a|run_b` ที่ ignore

## การตรวจสอบ

```powershell
python -m unittest tests.test_independent_claim_validation tests.test_repository_contract -v
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_a
python scripts/development/run_independent_claim_validation.py --config config/development/independent_claim_validation_v1.json --output-root artifacts/work129/run_b --replay-reference artifacts/work129/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 125–128 และตรวจ staged/cached diff โดยตรง; commit ทันทีเมื่อทุก gate ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

โค้ดแยกยังอาจใช้ telemetry และ physical assumptions ร่วมกัน นี่คือ independent numerical interpretation ไม่ใช่ institutional independence หรือ physical measurement สิ่งที่ไม่ทำ: rewrite ผลก่อนหน้า, external novelty, vehicle promotion, physical validation, push หรือ rewrite history
