# ผลงาน 030: Integration Falsification และ Promotion Gate

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_030_integration-falsification-promotion-gate-result.md`

## ผลลัพธ์

ปิดคิว implementation แบบ coupled Level 0 ด้วย release gate ที่มี fingerprint, deliberate transaction fault หกแบบ, หลักฐาน timestep refinement ที่มีขอบเขต, typed cross-model requirement และ promotion review แบบ fail-closed สถานะ repository ปัจจุบันคือ `level0_experimentation_ready_promotion_blocked`: เริ่มทดลอง candidate ที่ Level 0 ภายใต้ gate ได้ แต่ยังเรียก candidate ว่า discovery, real-circuit performer, physically validated design, safe design หรือ manufacturable design จากหลักฐานนี้ไม่ได้

campaign Work 029 ยังคงครบ `30/30` run บนสิบ profile และสาม seed โดย evidence identity ถูกยกระดับเป็น `work029-baseline-campaign-v2` และ promotion gate จะคำนวณ identity กับ aggregate invariant ใหม่ก่อนเชื่อหลักฐาน

## ไฟล์ที่เปลี่ยน

- เพิ่ม `config/simulation/integration_promotion_gate_v1.json`
- เพิ่ม `src/formula_ultimate/simulation/integration_release.py` และ public export
- ทำ `src/formula_ultimate/simulation/baseline_campaign.py` ให้เข้มขึ้นด้วย fingerprint ครบทุก field และ result verification อิสระ
- เพิ่ม focused test สิบรายการใน `tests/test_integration_release.py`
- เพิ่ม `scripts/validate_integration_release.py`
- เพิ่ม model record เรื่อง integration falsification/promotion สองภาษา
- เพิ่ม problem report ที่แก้แล้วหนึ่งเรื่องสองภาษา, plan/result คู่นี้ และปิด implementation queue สองภาษา
- อัปเดต Work 029 campaign record สองภาษาเพื่อแยก historical v1 fingerprint จาก verified v2 evidence ปัจจุบัน

## ปัญหาที่แก้

run fingerprint ของ Work 029 ไม่ครอบคลุม visible field ที่มีผลต่อ promotion เช่น real-circuit admission และ static-width status ขณะที่ campaign fingerprint ไม่ได้พิสูจน์ aggregate consistency แบบอิสระ จึงอาจแก้ in-memory record แล้วคง stale identity ไว้ได้ Work 030 จึง hash ทุก evidence field ยกเว้น fingerprint field เอง และตรวจ run identity, campaign identity, count, family/seed matrix, partition, budget, residual flag และ real-circuit aggregation ใหม่ก่อน promotion review

## การตัดสินใจ

- บังคับให้ control transaction commit และ injected fault ทุกแบบต้องให้ observable code ตรงที่คาดโดยไม่มี committed state
- ตรึง refinement ที่ timestep `(2000, 1000, 500) s`, seed `17`, calibration profile หนึ่งชุด, holdout profile หนึ่งชุด และ common budget `128` step
- ไม่ estimate convergence order จาก steady analytical reference ที่ invariant แบบ exact
- ต้องมี independent passing evidence ระดับ `level1` หรือสูงกว่าสำหรับ geometry/mass/inertia, surveyed circuit corridor, aerodynamics, structural safety, thermal reliability และ quantified uncertainty
- ต้องมี real-circuit admission แยกจาก cross-model evidence
- เมื่อ test evidence ครบ อนุญาตได้เพียง `eligible_for_independent_review`; automatic discovery ยังถูกห้าม
- อนุญาตเฉพาะ gated Level-0 experimentation ขณะที่ promotion ถูกบล็อก

## ผลการทดลองและการพยายามหักล้าง

- ตัวแปรอิสระ: injected fault หกประเภทและ timestep สามค่า
- หลักฐานตัวแปรตาม: failure code, rollback state, detection coverage, finish time, primary energy, finish residual, sensitivity, missing evidence, promotion status และ release status
- ตัวควบคุม: architecture v4, transaction start state/signal, adapter version/output, reference family/opportunity Work 029, calibration/holdout profile, seed `17`, environment/energy control, timeout และ common run budget
- ผล control: `committed`
- ผล fault: ตรวจพบและ rollback `6/6`—adapter หาย, version mismatch, residual identity ซ้ำ, residual fail, output นอกประกาศ และ time regression
- ผล refinement: sample หกชุด finish; maximum relative time variation `0.0`; maximum relative primary-energy variation `1.5466148595436325e-14`; maximum absolute finish residual `0.0 m`; ไม่กล่าวอ้าง convergence order
- ผล promotion: `blocked` จาก independent evidence หกประเภทที่หาย/ไม่ valid และ real-circuit admission ที่หาย
- ผล relaxed test fixture: complete independent evidence ไปได้เพียง `eligible_for_independent_review` ไม่ใช่ discovery
- หลักฐานสนับสนุน: transaction enforcement, deterministic replay, identity verification, budget closure และ explicit claim denial ผ่านทั้งหมด
- หลักฐานขัดแย้ง: ไม่พบต่อ software gate ที่ประกาศ แต่การไม่มี physical evidence ขัดกับคำกล่าวอ้าง performance/validation ที่กว้างกว่าและถูกเก็บเป็น promotion blocker
- คำอธิบายทางเลือก: timestep invariance มาจาก steady drag-balanced analytical control ไม่ได้แสดง nonlinear หรือ higher-fidelity agreement
- หลักฐานที่ขาด: surveyed circuit corridor/condition, geometry-derived mass/inertia, independent aero, structural/safety, thermal/reliability, quantified uncertainty และ physical test
- ความมั่นใจ: สูงต่อ deterministic software/falsification gate; ต่ำต่อ physical หรือ real-circuit performance ซึ่งยังระบุชัดว่าไม่ผ่าน admission

## คำสั่งและหลักฐาน validation

คำสั่งทั้งหมดคืน exit status `0`:

```powershell
python -m unittest tests.test_baseline_campaign tests.test_integration_release -v
python -m unittest tests.test_coupling_contracts tests.test_coupled_transaction tests.test_whole_race tests.test_baseline_campaign tests.test_integration_release -v
python scripts/validate_coupling_contracts.py
python scripts/validate_coupled_transaction.py
python scripts/validate_whole_race.py
python scripts/validate_baseline_campaign.py
python scripts/validate_integration_release.py
python -m compileall -q src scripts tests
python -m unittest discover -s tests -v
git diff --check
git diff --cached --check
```

- final targeted baseline/release regression: ผ่าน 20 รายการใน `21.195 s`
- focused regression Work 021/022/028/029/030: ผ่าน 50 รายการใน `21.479 s`
- repository documentation contract: ผ่าน 6 รายการใน `0.192 s`
- test suite ทั้ง repository: ผ่าน 262 รายการใน `21.997 s`
- campaign result fingerprint v2: `79a03587e6bbeb17101c89a59c7fe61053571f493a29fbe356322418726d2a9b`
- gate fingerprint: `ad629075e69001b17eaf8b8e9371ecb72fc52a4e07a762c4546096daf9d23814`
- falsification fingerprint: `a6c0b5a1a30abda519ed230114ca5c49b5754bb2bd763e505ae0f2f77ec15f4b`
- refinement fingerprint: `fdb02195f1a77709b9f43f5d1b1d86736f73e0862dbb9d605f56017a28462af2`
- blocked promotion fingerprint: `bf78fcb402c43e633399342d3e93a3473d3f2c4defa2e1447163bc34d059400f`
- release-review fingerprint: `783e156bb2a8d8dcad356033b6767fb2b2cbef9b9f0f3d1f94df13a83ab94f29`

## ข้อจำกัด

injected adapter แยกทดสอบ transaction enforcement และไม่ได้ exercise domain defect ที่เป็นไปได้ทุกแบบ Refinement matrix ครอบคลุม steady Level-0 analytical reference ไม่ใช่ nonlinear track dynamics การปิด implementation queue คือ software readiness สำหรับ gated research ไม่ใช่การจบโครงการวิจัย Formula Ultimate หรือหลักฐานว่ารถสำเร็จแล้ว

## งานต่อเนื่อง

research phase ถัดไปควรหา/derive independent evidence หกประเภทและข้อมูล real-circuit admission แล้วส่ง candidate เข้า higher-fidelity falsification และ physical review โดย topology ของ candidate ยังคงเปิดกว้าง; evidence requirement จำกัดคำกล่าวอ้าง ไม่ได้บังคับให้ใช้ layout รถแบบดั้งเดิม
