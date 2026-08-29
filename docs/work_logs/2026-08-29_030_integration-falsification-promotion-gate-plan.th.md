# แผนงาน 030: Integration Falsification และ Promotion Gate

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_030_integration-falsification-promotion-gate-plan.md`

## วัตถุประสงค์

ปิดคิว implementation แบบ coupled Level 0 ด้วย deliberate transaction/integration fault injection, หลักฐาน timestep refinement ที่มีขอบเขต, requirement ด้าน uncertainty/cross-model ที่ชัดเจน และ release/promotion decision ที่เรียก candidate ซึ่งหลักฐานไม่พอว่า discovery หรือ real-circuit performer ไม่ได้

## ขอบเขต

- กำหนด integration release-gate protocol แบบ strict และมี fingerprint
- inject fault adapter หาย, version mismatch, residual ซ้ำ, residual fail, output นอกประกาศ และ state-time regression ใน transaction v4
- บังคับให้ fault ที่ประกาศทุกตัว fail-closed โดยไม่มี committed state
- execute analytical reference จาก Work 029 ที่หลาย timestep ภายใต้ reduced control อื่นที่เหมือนกัน
- บันทึก pairwise time/energy sensitivity, finish residual, budget และ analytical boundary โดยไม่อนุมาน convergence order เมื่อ steady reference invariant แบบ exact
- กำหนด typed independent higher-fidelity evidence requirement สำหรับ geometry/mass/inertia, surveyed circuit corridor, aero, structure/safety, thermal/reliability และ quantified uncertainty
- ประเมิน campaign Work 029 ที่เสร็จแล้วผ่าน falsification, refinement, real-circuit และ cross-model gate
- สร้าง release review ที่อาจอนุญาต gated Level-0 experimentation แต่บล็อกคำกล่าวอ้าง discovery, real race, safety, manufacturability และ physical validation
- บันทึกและแก้ defect ทุกเรื่องที่พบใน problem report สองภาษาแยก

## ไฟล์ที่วางแผน

- `config/simulation/integration_promotion_gate_v1.json`
- `src/formula_ultimate/simulation/integration_release.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_integration_release.py`
- `scripts/validate_integration_release.py`
- `docs/simulation/INTEGRATION_FALSIFICATION_PROMOTION_GATE.md`
- `docs/simulation/INTEGRATION_FALSIFICATION_PROMOTION_GATE.th.md`
- problem report ของ Work 030 หากจำเป็น
- implementation queue, แผนนี้ และ result record สองภาษาที่เข้าคู่

## นิยามการทดลอง

- ตัวแปรอิสระ: injected fault class และ timestep `(2000, 1000, 500) s`
- ตัวแปรตาม: failure code, rollback state, fault-detection completeness, finish time, primary energy, finish residual, refinement sensitivity, promotion status, missing evidence และ release status
- ตัวควบคุม: architecture v4, transaction start state/signal, adapter version/output ที่ประกาศ, family/opportunity Work 029, calibration/holdout profile ที่เลือก, seed `17`, energy/environment, timeout และ common step budget ที่สูงพอ
- เมตริก: detected fault fraction, false-positive control status, การไม่มี committed state เมื่อ fault, maximum relative time/energy variation, residual pass, missing evidence coverage และ discovery-claim denial
- เกณฑ์สำเร็จ: control commit; injected defect ทั้งหมด fail ด้วย code ที่คาดและ rollback; refinement sample finish ใน budgetและผ่าน tolerance; higher-fidelity evidence ที่หายบล็อก promotion; complete independent evidence fixture ไปได้เพียง review eligibility ไม่ใช่ automatic discovery
- เกณฑ์ล้มเหลว: injected defect ใด commit, control fail, timestep sensitivity เกิน toleranceแต่ไม่บล็อก, ยอมรับ missing evidence เงียบ, proxy evidence กลายเป็น real-circuit admission หรือ software ประกาศ discovery อัตโนมัติ
- การพยายามหักล้าง: ตัด adapter, ทำ version เสีย, evidence identity ซ้ำ, ทำ residual fail, emit signal นอกประกาศ, ทำ state time ถอยหลัง, ให้ refinement sample diverge, ตัด required evidence type, ทำ evidence dependent/failed และพยายาม promote proxy

## การตรวจสอบ

1. focused test Work 021/022/028/029/030
2. test suite ทั้ง repository
3. standalone validator Work 030 รวม full campaign Work 029
4. compile Python bytecode
5. `git diff --check` และ `git diff --cached --check`
6. ตรวจ staged scope แบบระบุไฟล์ก่อน commit

## เกณฑ์สำเร็จ

- integration fault ที่ประกาศทุกตัวถูกตรวจพบและ rollback
- refinement matrix deterministic และบันทึกการตีความที่จำกัด
- Level-0 proxy evidence ปัจจุบันถูกบล็อกจาก cross-model promotion ด้วยเหตุผลชัดเจน
- แม้ complete evidence fixture ก็เป็นเพียง `eligible_for_independent_review` ไม่ใช่ discovered อัตโนมัติ
- release review อนุญาตเฉพาะ gated Level-0 experimentation
- work item 021-030 และ queue ถูกทำ Completed หลัง validation เท่านั้น
- เอกสารอังกฤษและไทยตรงกัน
- commit Work 030 เป็น validated commit หนึ่งรายการ

## ความเสี่ยง

- exact steady-state invariance อาจถูกตีความผิดเป็น proof of convergence
- synthetic fault adapter อาจทดสอบ transaction enforcement โดยไม่ exercise domain model ทุกตัว
- release status อาจถูกอ่านเกินเป็น physical readiness
- required evidence type อาจมีแต่ไม่ independent หรือ valid
- การรัน full campaign 30 run ซ้ำทำให้ validation ใช้เวลามากขึ้น

## สิ่งที่ไม่ทำโดยชัดแจ้ง

- ไม่อ้าง physical validation, real lap time, safety, manufacturability หรือ discovered technology
- ไม่สร้าง higher-fidelity หรือ independent evidence ปลอม
- ไม่ทำ autonomous topology search หรือ candidate optimization ในงานนี้
- ไม่ promote จาก Level 0 เป็น discovery claim อัตโนมัติ
- ไม่แทน CFD, FEA, surveyed geometry, track testing หรือ expert review
