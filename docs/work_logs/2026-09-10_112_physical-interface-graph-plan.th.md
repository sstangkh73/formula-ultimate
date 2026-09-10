# แผน Work 112: กราฟ Physical Interface

ต้นฉบับภาษาอังกฤษ: `2026-09-10_112_physical-interface-graph-plan.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

พัฒนา typed physical-interface multigraph แบบมีขอบเขตที่ผูกกับ material/void regions จริงของ Work 108 รักษา terminal frames, physical domains, variables, units, direction, terminal roles, owner grouping, parallel interactions, allowed motion และ constitutive-law references เมื่อเปลี่ยนเฉพาะ identifiers

Corpus ที่ admitted ครอบคลุม mechanical force, motion และ thermal exchange โดยไม่กำหนดบทบาทชิ้นส่วนรถแบบเดิม ตรวจ compatibility และ conservation fixtures, ถ่าย binding ที่ไม่กำกวมผ่าน split/merge maps ที่ประกาศ และส่ง evidence-invalidation events สำหรับ binding ที่เปลี่ยน กำกวม หรือหาย

## ตัวแปร controls และไฟล์

- IV: terminal roles/orientations, edge direction และ multiplicity, owner grouping, identifier names, split/merge mappings
- DV: canonical identity, connected components, compatibility, exchange residual และ invalidation events
- Controls: identifier-only rename ต้องเท่ากัน; source/sink swap, การลบ parallel edge, owner regrouping และ disconnected paths ต้องแยกออก; incompatible units, missing surfaces และ rigid/moving conflicts ต้องล้มเหลวแบบปิด
- Success: equivalence/distinction fixtures ผ่านทั้งหมด, multiedges คงอยู่, conservation residuals ผ่าน tolerance ที่ตรึง, replay ตรงทุกบิต และ identity ที่เกินขอบเขตรายงาน unresolved แทน fallback จากชื่อ

ไฟล์ที่วางแผน: `src/formula_ultimate/assembly/physical_interface_graph.py`, `config/development/physical_interface_graph_v1.json`, `scripts/development/run_physical_interface_graph.py`, `tests/test_physical_interface_graph.py`, `docs/contracts/PHYSICAL_INTERFACE_GRAPH_V1*` สองภาษา, plan/result นี้สองภาษา และ `artifacts/work112/run_a|run_b` แบบ ignored

## Validation

```powershell
python -m unittest tests.test_physical_interface_graph tests.test_repository_contract -v
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_a
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_b --replay-reference artifacts/work112/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน affected regressions, `git diff --check`, stage เฉพาะไฟล์ที่ประกาศ, ตรวจ cached scope และ `git diff --cached --check`; commit ทันทีเมื่อ gates ผ่านทั้งหมด

## ความเสี่ยงและสิ่งที่ไม่ทำ

Exact canonicalization โตแบบ factorial จึงตรึง terminal bound และให้กราฟเกินขอบเขตรายงาน unresolved อย่างชัดเจน Frame fixtures เป็น semantic evidence ที่ประกาศ ไม่ใช่หลักฐาน geometric contact สิ่งที่ไม่ทำ: general mechanism discovery, contact mechanics, solver-field prediction, physical validation, ติดตั้ง dependency, push หรือ rewrite history
