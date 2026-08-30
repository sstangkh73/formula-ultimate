# ผลงาน 059: Protocol v2 Serialization Remediation และ Fresh Burn-In

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_059_v2-serialization-remediation-burn-in-result.md`

## ผลลัพธ์

สร้าง protocol `bounded_whole_vehicle_main_campaign_v2` / campaign `FU-BMC-002` เชื่อมไป immutable stopped v1 evidence และตรวจว่า scientific rules ทุกตัวเท่ากับ v1 แก้เฉพาะ tuple/list serialization representation boundary พร้อมเพิ่ม append/reload regression coverage Fresh process recovery และ fresh excluded-seed burn-in ผ่าน Decision: `burn_in_accepted_for_admitted_main_campaign`

## ไฟล์ที่เปลี่ยน

- v2 protocol config ใหม่และ exact successor validation
- JSON-compatible promotion canonicalization ใน generic campaign command
- Process probe ที่เลือก protocol ได้และ Work 059/060 wrappers
- Regression และ scientific-equivalence tests
- แผนสองภาษา Work 059/060, v2 admission research record และผล Work 059

## คำสั่งและผล exact

1. Focused tests:

   ```powershell
   py -3.14 -m unittest tests.test_main_campaign_protocol tests.test_campaign_physics tests.test_campaign_runner -q
   ```

   Exit status: `0`; `Ran 26 tests in 0.415s`; `OK`

2. Fresh process probe และ burn-in:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work059.ps1
   ```

   Exit status: `0` Process probe `1/1/0` Burn-in: attempts `240`, promotions `6`, refinement passed `6`, witness passed `6`, supported streams `3`, replay exact และ decision accepted

3. Verify-only replay:

   ```powershell
   py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind burn-in --protocol config/experiments/bounded_whole_vehicle_main_campaign_v2.json --artifact-root artifacts/work059 --verify-only
   ```

   Exit status: `0`; counts/fingerprints ตรงและไม่เรียก evaluator หรือ solver process

4. Full suite:

   ```powershell
   py -3.14 -m unittest discover -s tests -q
   ```

   Exit status: `0`; `Ran 369 tests in 26.151s`; `OK`

5. Compilation:

   ```powershell
   py -3.14 -m compileall -q src scripts tests
   ```

   Exit status: `0`

## หลักฐาน

- Protocol fingerprint: `d09e33dd0ff0438f379ccadfac5b8bcde3e611f2bf71bde3c74ced2697d58123`
- Training reservations/results/pending: `240/240/0`; counts `80/80/80`; GRID unique `80`
- Training feasible/structural failure: `189/51`
- Promotions/shortfall: `6/0`; holdout/refinement/CAD terminal: `6/6/6`; passed refinement/CAD: `6/6`
- Training combined fingerprint: `52de5c3a44423b126e6e05b50c594a0a70c4956d084bc4bc2a02b3c4fa9b3054`
- Stage fingerprint: `cd019afbe7b85b10e6fc5bc744314b16b281e4dd1701b0eab0c94681f7978e97`
- Refinement benchmark result: `185b3749575325ff7c6be9aee2553abf37ac44320b222a330b802b90da21a038`
- External process evidence: 123 processes, cumulative recorded wall time `37.7205395991914 s`

## Review และข้อจำกัด

หลักฐานสนับสนุน: scientific equivalence test, new identity/provenance checks, exact process recovery, equal opportunity accounting, benchmark, downstream terminal recordsครบ และ exact verify-only replay

หลักฐานที่ขัดแย้ง: v1 เปิดเผยว่าไม่มี serialization-boundary test และ v2 ไม่ได้ลบ failure นั้น Physical evaluator ยัง bounded และ linear-elastic

คำอธิบายทางเลือก: successful burn-in อาจมาจาก primitive geometry ที่เรียบง่ายและไม่ได้หมายถึง arbitrary-vehicle robustness

หลักฐานที่ยังขาด: v2 main campaign, independent replication, solid/contact/nonlinear analysis, physical material calibration, manufacturing tolerance และ hardware tests

ความเชื่อมั่น: สูงสำหรับ v2 admission ภายใต้ exact committed software/tool environment แต่ต่ำเมื่อออกนอก frozen domain

Staged-scope checks, commit hash และ post-commit clean-tree replay จะรายงานใน final Work 059 handoff เพราะ commit ยังไม่เกิดตอนเขียน record นี้
