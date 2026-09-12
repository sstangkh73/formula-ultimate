# แผน Work 114: ชุดประกอบ Moving Contact

ต้นฉบับภาษาอังกฤษ: `2026-09-12_114_moving-contact-assembly-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

พัฒนา moving/compliant assembly สองพิกัดแบบมีขอบเขตโดยใช้ joint stiffness/contact applicability ที่ตรงกันของ Work 113 ติดตามสมาชิกเคลื่อนที่ที่ยืดหยุ่นตามแกนภายใต้ imposed base reversal พร้อม tangential stick/slip history, unilateral opening/closing, recovered contact reactions, swept clearance และ energy/work ledger

เปรียบเทียบ explicit time steps สามระดับและ reduced in-range response กับ detailed event law เก็บ Work 088 rigid/moving incompatibility เป็น fail-closed regression แทนการบังคับ rigidity อย่างเงียบ

## ตัวแปร controls และไฟล์

- IV: joint strategy, placement clearance, compliance, preload, motion amplitude/history และ time step
- DV: displacement/phase, constraint drift, contact force, opening/closing/slip events, minimum swept clearance, transmitted impulse และ energy residual
- Controls: initial/boundary histories เดียวกัน; free rigid motion, incompatible constraints, severed coupling, reversal/contact impact, collision และ reduced-model range violation
- Success: histories เป็น deterministic, คำนวณ contact events/reactions ไม่กำหนดค่าเอง, time-step quantities ผ่าน last-two gates, energy/constraint/clearance gates ผ่าน, invalid assemblies ถูกบล็อกเฉพาะกรณี และ replay ตรงทุกบิต

ไฟล์ที่วางแผน: `src/formula_ultimate/assembly/moving_contact_assembly.py`, `config/development/moving_contact_assembly_v1.json`, `scripts/development/run_moving_contact_assembly.py`, `tests/test_moving_contact_assembly.py`, `docs/contracts/MOVING_CONTACT_ASSEMBLY_V1*` สองภาษา, plan/result นี้สองภาษา และ `artifacts/work114/run_a|run_b` แบบ ignored

## Validation

```powershell
python -m unittest tests.test_moving_contact_assembly tests.test_repository_contract -v
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_a
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_b --replay-reference artifacts/work114/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน affected regressions, ตรวจ staged scope แบบ explicit และ cached diff checks; commit หลังทุก gate ที่ประกาศผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Penalty-contact stiffness ทำให้ stable time scale สั้น ต้องแสดง time-step dependence Tangential motion เป็น prescribed-history contact probe ที่ลงทะเบียน ไม่ใช่ full planar rigid-body dynamics สิ่งที่ไม่ทำ: complete suspension, crash, vehicle readiness, nonlinear flexible-body FEA, physical validation, push หรือ rewrite history
