# แผน Work 095: Constructive Validity and Manufacturing Gate

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_095_constructive-validity-manufacturing-gate-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

สร้าง gate แบบ deterministic และ fail-closed เพื่อไม่ให้ geometry ที่ซับซ้อนขึ้นใช้ invalid B-rep declaration หรือข้าม process limit ที่ประกาศ Gate ต้องแยก constructive validity ออกจาก coarse process-envelope check, บันทึกสาเหตุ rejection ทุกข้อ และทำให้ pre-evaluation repair ที่อนุญาตทุกครั้งเป็นส่วนหนึ่งของ genotype/provenance identity

## ขอบเขตและไฟล์ที่วางแผนเปลี่ยน

- `config/manufacturing/constructive_validity_gate_v1.json`
- `src/formula_ultimate/components/constructive_validity.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/experiments/run_constructive_validity_pilot.py`
- `tests/test_constructive_validity.py`
- `docs/contracts/CONSTRUCTIVE_VALIDITY_MANUFACTURING_GATE_V1.md` และไฟล์ภาษาไทย
- plan/result ชุดนี้และไฟล์ภาษาไทย
- หลักฐาน pilot/replay แบบ deterministic ที่ ignore ใต้ `artifacts/work095/`

## ตัวแปรและ controls

- ตัวแปรอิสระ: representation family, exact source geometry identity, material/process ที่ประกาศ, process-specific limit, synthetic measured witness value, repair declaration, repair budget และ evaluation-observed state
- ตัวแปรตาม: `accepted`, `repaired` หรือ `rejected`; violation code ครบตามลำดับ; constructive/process margin; repair trace; original/repaired genotype identity; validity yield และจำนวน rejection cause แยกตาม representation family
- matched controls: primitive control หนึ่งแบบและ curved/free-form identity จาก Work 092 ห้าแบบได้รับ 8 frozen scenarios และ compute opportunity เหมือนกัน หลักฐานของ scenario ระบุชัดว่าเป็น synthetic contract-verification data ไม่ใช่คำอ้างว่าได้วัดมิติเหล่านี้จาก source STEP
- negative controls: self-intersection, sliver/minimum feature, zero thickness, inaccessible feature/tool path, unsupported overhang/wall, hidden repair, enclosed void, tolerance, joining access, material/process ไม่เข้ากัน, เกิน repair budget, repair หลัง observation, unknown field, non-finite value และ replay mutation

## ลำดับ gate และกฎ repair

1. ตรวจ exact schema, source identity, ค่า SI ต้อง finite, process profile, compatibility และโอกาส scenario ที่เท่ากัน
2. ทำเฉพาะ deterministic repair ที่ preregistered ก่อนมี evaluation observation V1 ยอมรับ `add_support`, `increase_escape_hole` และ `increase_joining_access` ภายใต้จำนวน operation สูงสุดที่ตรึงไว้
3. hash original candidate, ordered repair trace และ repaired candidate Repair ที่ประกาศหรือตรวจพบแต่หายจาก trace คือ `hidden_repair` และต้อง reject
4. ตรวจ constructive B-rep flag ก่อน แล้วจึงตรวจ wall, ligament, radius, minimum feature, tool access, overhang/support, enclosed void/escape, tolerance, joining access และ material/process compatibility ตาม process
5. คืน violation ทุกข้อที่เกี่ยวข้อง โดยไม่แก้เงียบและไม่หยุดหลัง failure แรก

## เกณฑ์สำเร็จ

- representation family ทั้ง 6 ได้รับ matched scenario อย่างละ 8; opportunity ที่ไม่ใช้หรือถูกปฏิเสธยังถูกนับ
- baseline ผ่าน, preregistered support repair คืน `repaired` และ control ที่ฉีด self-intersection, sliver, zero thickness, inaccessible feature, unsupported wall/overhang และ hidden repair ถูกปฏิเสธแบบมองเห็นได้ในทุก family
- control เพิ่มเติมปฏิเสธ enclosed void, tolerance/joining access ที่เป็นไปไม่ได้, material/process ไม่เข้ากัน, repair หลัง observation และ repair-budget violation
- original กับ repaired genotype/provenance hash ต่างกันเมื่อมี repair; clean run ที่เหมือนกันสร้าง ledger ทั้งชุดและ result SHA-256 เหมือนเดิม
- focused tests, compilation, repository contracts, pilot/replay และ full regression ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

coarse witness scalar อาจพลาด local geometry, orientation, collision, topology และ production limit เฉพาะ supplier Matched control แบบ synthetic พิสูจน์พฤติกรรม gate ไม่ได้พิสูจน์ manufacturability ที่วัดจริงของ STEP ใน Work 092 V1 ไม่ infer thickness จาก CAD, ไม่ repair arbitrary B-rep, ไม่วาง tooling plan, ไม่ certify process/material, ไม่ model cost, ไม่รัน FEA/CFD, ไม่ validate strength และไม่อนุญาต result-conditioned change ส่วน Work 096 รับผิดชอบ independent semantic geometry measurement
