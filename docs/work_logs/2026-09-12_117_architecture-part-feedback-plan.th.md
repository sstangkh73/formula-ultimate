# แผน Work 117: Bidirectional Architecture-Part Feedback

ต้นฉบับภาษาอังกฤษ: `2026-09-12_117_architecture-part-feedback-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

พัฒนา feedback/regeneration loop แบบมีขอบเขตที่ตรึง Work 112 terminal semantics, Work 114 motion/load history และ Work 115 thermal coupling รักษา external task ให้ immutable ขณะที่ versioned internal tasks รับ load, heat, motion, envelope และ unknown-model requirements จาก assembly

สร้าง local free-parameter region geometry จากแต่ละ task ประเมิน structural/thermal margins และ mass ส่ง requirements ที่เปลี่ยนกลับ และ invalidate stale evidence หลัง causal task revision ทุกครั้ง เปรียบเทียบ feedback-enabled กับ frozen-task controls โดยใช้ initial candidate, coefficients, seeds และ evaluation cap เดียวกัน

## ตัวแปร controls และไฟล์

- IV: feedback enabled/frozen, task version, geometry parameters, decomposition/merge และ architecture-derived conditions
- DV: task/geometry identities, load/heat margins, mass, missing-model blockers, invalidation events และ evaluations ต่อ iteration
- Controls: external task immutable, compute opportunity เท่ากัน, assembly load เปลี่ยนต้อง reevaluate, multifunctional region merge ไม่ duplicate mass และ missing-coefficient rejection
- Success: feedback/regeneration cycle อย่างน้อยหนึ่งรอบเปลี่ยนทั้ง task และ geometry evidence; ancestry/invalidation ครบ; unresolved models ใช้ยืนยัน feasibility ไม่ได้; replay ตรงทุกบิต Improvement ถูกวัดแต่ไม่บังคับ

ไฟล์ที่วางแผน: `src/formula_ultimate/experiments/architecture_part_feedback.py`, `config/development/architecture_part_feedback_v1.json`, `scripts/development/run_architecture_part_feedback.py`, `tests/test_architecture_part_feedback.py`, `docs/contracts/ARCHITECTURE_PART_FEEDBACK_V1*` สองภาษา, plan/result นี้สองภาษา และ `artifacts/work117/run_a|run_b` แบบ ignored

## Validation

```powershell
python -m unittest tests.test_architecture_part_feedback tests.test_repository_contract -v
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_a
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_b --replay-reference artifacts/work117/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน affected regressions และ explicit staged/cached diff checks; commit ทันทีหลังทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Bounded generator และ reduced evaluators ไม่ใช่ complete optimizer สิ่งที่ไม่ทำ: เปลี่ยน race rules, complete feasibility, isolated-survivor promotion, unrestricted search, vehicle readiness, physical validation, push หรือ rewrite history
