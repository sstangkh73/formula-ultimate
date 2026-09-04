# ผล Work 090: Search-Space Bias and Diversity Contract

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_090_search-space-bias-diversity-contract-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

Contract วัด diversity แบบ deterministic และ census ของ search ปัจจุบันเสร็จแล้ว Opportunity ledger exact ของ Work 050 สร้าง proposal ที่ descriptor valid `288` ตัว แต่มี topology signature เพียง `1` แบบและ functional-path signature เพียง `1` แบบ แม้มี normalized geometry signature `264` แบบจากการเปลี่ยน scale parameter แต่ candidate ทุกตัวยังเป็น primitive เท่านั้น ผลนี้วัดความต่างระหว่าง parametric variation กับ topology diversity โดยตรง

Mean primitive fraction คือ `1.0`; mean curved-surface-area fraction `0.0598413769094221`; primitive-type entropy `0.8112781244591328 bits`; และ normalized phenotype duplication `8.333333333333337%` Bounded Work 050 evaluator บันทึก non-failure `207` กับ structural failure `81` แต่ category เหล่านี้ไม่ใช่ general physical failure-mode coverage

## ไฟล์ที่เปลี่ยน

- `config/experiments/design_diversity_v1.json`
- `src/formula_ultimate/experiments/design_diversity.py`
- `scripts/experiments/run_design_diversity_baseline.py`
- `tests/test_design_diversity.py`
- `docs/contracts/DESIGN_DIVERSITY_V1.md` และไฟล์ภาษาไทยคู่กัน
- ผลงานนี้และไฟล์ภาษาไทยคู่กัน
- แผน Work 090 และไฟล์ภาษาไทยคู่กัน เปลี่ยนสถานะเป็น `Completed`

หลักฐาน census/replay ที่สร้างใต้ `artifacts/work090/` ถูก ignore และไม่ได้ commit

## หลักฐาน exact

- Config identity: `fef23e7250a1a451f775f96bd799872b4967ba2f448f484438bb89d11d6cc2ff`
- Census identity: `8b2f1e52fdc72c6743aea5cf472eb6c29ddde01220a97f9d352b9fb6941bc69c`
- Result identity: `5729ed2b3282e3634e601ac91a983f58f2c3dcbc205fa8203379a3f3dad170e9`
- SHA-256 ของ result file ที่เหมือนกันทุก byte: `5f38578d9d4b8cbbcc90ac02ce4f40f37e8f4e1fa0ef2e25f1621135465b2604`
- SHA-256 ของ census file ที่เหมือนกันทุก byte: `57138cbae2df84f6fa007818fb8ecd9bf44f8ccc330794352bfcca69d99b24da`
- อธิบาย candidate ได้ `288/288`; normalized geometry signature ต่างกัน `264`; topology signature ต่างกัน `1`; functional-path signatureต่างกัน `1`
- Invariance/change-detection control ผ่านทั้งหมด

## คำสั่งตรวจสอบ exact และผล

```powershell
python -m unittest tests.test_design_diversity tests.test_repository_contract -v
# exit 0; Ran 16 tests; OK

python -m compileall -q src scripts tests
# exit 0

python scripts/experiments/run_design_diversity_baseline.py `
  --config config/experiments/design_diversity_v1.json `
  --output-root artifacts/work090/run_a
# exit 0; attempted_candidates=288; unique_topology_signatures=1

python scripts/experiments/run_design_diversity_baseline.py `
  --config config/experiments/design_diversity_v1.json `
  --output-root artifacts/work090/run_b `
  --replay-reference artifacts/work090/run_a/result.json
# exit 0; result และ census เหมือน run_a ทุก byte

python -m unittest discover -s tests -q
# exit 0; Ran 630 tests in 418.326s; OK (skipped=3)

git diff --check
# exit 0
```

## การทบทวนหลักฐานและข้อจำกัด

หลักฐานสนับสนุนประกอบด้วยการล็อก source exact, proposal ledger ที่ equal-budget ครบ, invariant control, topology-change control และ exact replay หลักฐานขัดแย้งกับอิสระในการออกแบบปัจจุบันมีน้ำหนักชี้ขาด: dimension ของ geometry เปลี่ยน แต่ topology และ functional path ไม่เปลี่ยน ดังนั้น unique-geometry ratio ที่สูงห้ามตีความเป็น architectural diversity Signature V1 แบบ Weisfeiler-Lehman ที่มีขอบเขตอาจ collision ระหว่าง graph non-isomorphic ได้ยาก และ radial geometry descriptor ตั้งใจไม่เก็บ chirality Work 091 และงานภายหลังต้องขยาย descriptor เมื่อ representation ใหม่ execute ได้

ผลนี้สร้าง measurement baseline เท่านั้น ไม่ได้สร้าง profile, topology, physical evaluator หรือ discovery ใหม่
