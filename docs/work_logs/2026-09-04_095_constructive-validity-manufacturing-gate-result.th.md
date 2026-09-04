# ผล Work 095: Constructive Validity and Manufacturing Gate

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_095_constructive-validity-manufacturing-gate-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

Work 095 สร้าง constructive-validity และ coarse manufacturing gate แบบ deterministic และ fail-closed pilot 48 opportunities แบบ matched ให้ primitive control หนึ่งตัวและ curved/free-form identity จาก Work 092 อีก 5 ตัวได้รับ scenario 8 แบบเดียวกัน ทุก family ได้ baseline accepted 1, preregistered repaired 1 และ rejected control ที่มองเห็นได้ 6 จึงมี synthetic-fixture yield เท่ากันที่ `0.25`

นี่คือหลักฐานพฤติกรรม gate บน synthetic matched measurements ไม่ใช่หลักฐาน manufacturability ที่วัดอย่างอิสระจาก STEP geometry ที่อ้างอิง

## ไฟล์ที่เปลี่ยน

- `config/manufacturing/constructive_validity_gate_v1.json`
- `src/formula_ultimate/components/constructive_validity.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/experiments/run_constructive_validity_pilot.py`
- `tests/test_constructive_validity.py`
- `docs/contracts/CONSTRUCTIVE_VALIDITY_MANUFACTURING_GATE_V1.md` และไฟล์ภาษาไทย
- plan/result ชุดนี้และไฟล์ภาษาไทย
- หลักฐาน replay ที่ ignore ใต้ `artifacts/work095/`

## การตัดสินใจและหลักฐาน

- ตรวจ source candidate ID และ STEP hash เทียบกับ Work 092 manifest และ primitive witness config ส่วน dimensional/process evidence ติดป้ายแยกเป็น `synthetic_contract_fixture`
- exact schema ปฏิเสธ unknown field, non-finite value และ numeric alias ของ Boolean flag Negative test พบพฤติกรรม `1 == True` ของ Python และปิดด้วย exact type check
- constructive violation ครอบคลุม invalid B-rep, solid count ผิด, self-intersection, zero thickness และ sliver feature size ส่วน process violation ครอบคลุม minimum wall/ligament/radius, tool access, overhang/support, enclosed void/escape, tolerance, joining access และ material/process compatibility
- คืน violation ทุกข้อที่เกี่ยวข้องตามลำดับคงที่ matched scenario `unsupported_wall` บันทึกทั้ง `wall_below_minimum` และ `unsupported_overhang`
- preregister เฉพาะ `add_support`, `increase_escape_hole` และ `increase_joining_access` pilot ใช้ `add_support` และบันทึก evidence hash ก่อน/หลัง, operation, original genotype, evaluated genotype และ provenance identity
- hidden, unregistered, over-budget และ post-observation repair ต้อง reject และ gate ไม่ใช้ performance evidence

## หลักฐาน pilot

- opportunities รวม: `48`; opportunity ต่อ family: `8`
- family: `primitive_control`, `curved_branch`, `tapered_hollow_duct`, `lofted_rotary_member`, `organic_load_bridge`, `variable_section_shell`
- สถานะต่อ family: `accepted=1`, `repaired=1`, `rejected=6`
- validity yield ต่อ family: `0.25` เท่ากันทั้ง 6 family
- จำนวน cause บังคับต่อ family: `self_intersection=1`, `sliver_feature=1`, `zero_thickness=1`, `tool_access_blocked=1`, `wall_below_minimum=1`, `unsupported_overhang=1`, `hidden_repair=1`
- Gate SHA-256: `4e9f8b3d739ccbcdb88c395954e4fcf6ad295ea6ca6c7b82cb53fb94b4531e8f`
- Result SHA-256: `59f7df5aa86c0c858eb336867a7c10a4b934db66629f44b0e5f4493619830e14`
- `post_observation_repair_allowed: false`; `cad_measurement_executed: false`

## คำสั่งตรวจสอบที่ใช้จริง

```powershell
python -m unittest tests.test_constructive_validity -q
# exit 0; ผ่าน 9 tests

python scripts/experiments/run_constructive_validity_pilot.py --config config/manufacturing/constructive_validity_gate_v1.json --mutation-protocol config/experiments/topology_mutation_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --work092-manifest artifacts/work092/run_g/manifest.json --primitive-witness config/cad/step_freecad_geometry_witness_v2.json --output artifacts/work095/run_a/result.json
# exit 0; 48 opportunities; yield_per_family=[0.25]

python scripts/experiments/run_constructive_validity_pilot.py --config config/manufacturing/constructive_validity_gate_v1.json --mutation-protocol config/experiments/topology_mutation_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --work092-manifest artifacts/work092/run_g/manifest.json --primitive-witness config/cad/step_freecad_geometry_witness_v2.json --output artifacts/work095/run_b/result.json --replay-reference artifacts/work095/run_a/result.json
# exit 0; exact replay ของผลทั้งชุด

python -m compileall -q src scripts tests
# exit 0

python -m unittest tests.test_constructive_validity tests.test_repository_contract -q
# exit 0; ผ่าน 15 tests

python -m unittest discover -s tests -q
# exit 0; ผ่าน 672 tests ใน 283.044 s; skip ตามสภาพแวดล้อมที่คาดไว้ 7 tests
```

## ข้อจำกัดและงานถัดไป

matched synthetic scalar evidence พิสูจน์การปฏิบัติของ gate ที่เท่ากัน ไม่ได้พิสูจน์ความน่าจะเป็นของ failure จริงที่เท่ากัน Gate ยังไม่ derive thickness field, curvature, access path, void หรือ joining region จาก CAD และไม่พิสูจน์ supplier capability, structural capacity, production quality, cost, safety หรือ physical validity Work 096 ต้อง recover independent semantic geometry witness แล้วจึงใช้ค่าที่วัดนั้นแทน synthetic fixture โดยไม่เปลี่ยน fail-closed rules
