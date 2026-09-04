# ผล Work 094: การกลายพันธุ์และรวมโทโพโลยีที่ทำซ้ำได้

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_094_reproducible-topology-mutation-recombination-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

Work 094 สร้าง proposal ledger แบบ deterministic, bounded และ pre-evaluation บน typed topology corpus ของ Work 093 initializer ทั้ง 6 strata ได้รับ operator อย่างละ 8 slot เท่ากัน pilot 48 slot ยอมรับ topology-changing family 4 แบบ ได้แก่ `grow_branch`, `split_part`, `add_crosslink` และ `reroute_path` การ exact replay สร้างผลทั้งชุดตามลำดับและ SHA-256 เดิมได้

ผลนี้ยืนยันเพียงกลไก proposal แบบมีชนิดที่ทำซ้ำได้ ไม่ได้ยืนยันว่า CAD สร้างได้ ผ่าน constructive validity ผลิตได้ ถูกต้องทางฟิสิกส์ ปลอดภัย มีสมรรถนะ หรือเป็นการค้นพบ

## ไฟล์ที่เปลี่ยน

- `config/experiments/topology_mutation_v1.json`
- `src/formula_ultimate/search/topology_mutation.py`
- `src/formula_ultimate/search/__init__.py`
- `scripts/experiments/run_topology_mutation_pilot.py`
- `tests/test_topology_mutation.py`
- `docs/contracts/REPRODUCIBLE_TOPOLOGY_MUTATION_V1.md` และไฟล์ภาษาไทย
- plan/result ชุดนี้และไฟล์ภาษาไทย
- หลักฐาน replay ที่ ignore ใต้ `artifacts/work094/`

## การตัดสินใจและหลักฐาน

- โอกาส proposal ถูกตรึงก่อนรันเป็น 6 strata คูณ 8 operator ตามลำดับ การปฏิเสธห้ามโยก slot หรืองบ retry
- entry ที่ยอมรับบันทึก parent genotype/topology identity, seed, slot, operator/probability, bounded retry, RNG checkpoint, trace, child genotype ทั้งชุด, child identity และ lineage SHA-256
- `reroute_path` เก็บเส้นทางเดิมที่ trace ได้ครบและเพิ่ม typed alternate route; แบบที่ลบเส้นทางเดิมระหว่างพัฒนาทำให้ part ตรงกลาง trace ไม่ได้และถูกปฏิเสธ
- protocol policy ถูกทำให้ตรงกับ interface domain/DOF และคู่ material/process ของ Work 093 ที่ตรึงไว้ การขยายที่ไม่รองรับยัง fail closed
- `prune_branch` ไม่ยอมรับ child เพราะไม่มี terminal leaf ที่ตัดได้โดยรักษา trace บังคับทั้งหมด ความล้มเหลว 18 ครั้ง (6 slot คูณ 3 attempt) ยังมองเห็นได้
- non-topology control เป็น `declared_topology_change: false` และ V1 crossover ปิดชัดเจนเพราะยังไม่มี compatible typed cut boundary
- mutation หลัง observation เกิด error ก่อนมี proposal และมี negative control สำหรับ cycle, disconnected route, impossible interface policy, incompatible material/process, exhausted retry, protocol mutation และ replay mutation

## หลักฐาน pilot

- slot รวม: `48`; โอกาสต่อ stratum: `8`
- ยอมรับต่อ stratum: primitive `5`, skeletal/serial `7`, shell `7`, rotary `7`, branching `6`, hybrid `7`
- ยอมรับต่อ operator: `grow_branch=6`, `prune_branch=0`, `split_part=6`, `add_crosslink=5`, `reroute_path=4`; non-topology control แต่ละตัว `=6`
- Protocol SHA-256: `1d475fbca89bf9395fe97d51f68a7c3ca1cb2cd063e9d4101cc4263a84c2cf10`
- Source Work 093 declaration SHA-256: `e1583e9aec9c3a4968ec5e35d1b81478d9023ca2392e08ec78ee0a48e9e5c69d`
- Result SHA-256: `75637c436e38452e588521402cf325e9b494bdcb77333d1fb72109e87e3b006f`
- `mutation_after_observation_allowed: false`; `cad_executed: false`

## คำสั่งตรวจสอบที่ใช้จริง

```powershell
python -m unittest tests.test_topology_mutation -q
# exit 0; ผ่าน 9 tests

python scripts/experiments/run_topology_mutation_pilot.py --genome-config config/genomes/typed_morphology_topology_genome_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --protocol config/experiments/topology_mutation_v1.json --output artifacts/work094/run_a/result.json
# exit 0; 48 slot; ผ่าน topology operator family 4 แบบ

python scripts/experiments/run_topology_mutation_pilot.py --genome-config config/genomes/typed_morphology_topology_genome_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --protocol config/experiments/topology_mutation_v1.json --output artifacts/work094/run_b/result.json --replay-reference artifacts/work094/run_a/result.json
# exit 0; exact replay ของผลทั้งชุด

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; ผ่าน 663 tests ใน 523.121 s; skip ตามสภาพแวดล้อมที่คาดไว้ 7 tests
```

คำสั่งอำนวยความสะดวก `python scripts/check_repository.py` คืน exit 2 เพราะไม่มี script นี้ จึงไม่ได้นับเป็น gate; ได้รัน gate ที่โครงการดูแลจริงคือ `tests.test_repository_contract` ก่อน commit

## ข้อจำกัดและงานถัดไป

โอกาส operator ถูกตรึงและยุติธรรม แต่ acceptance rate ยังไม่เท่ากัน corpus ไม่มี leaf ที่ซ้ำซ้อนอย่างปลอดภัย ดังนั้น `prune_branch` เป็น bounded rejection ที่มองเห็นได้ `reroute_path` เพิ่ม alternate route แทนการสลับเพื่อรักษา trace Work 095 ต้องปฏิเสธความล้มเหลวด้าน constructive validity และการผลิตอย่างอิสระ งานหลังจากนั้นต้องสร้าง CAD assembly และประเมินฟิสิกส์โดยไม่ป้อน observed result กลับเข้า ledger นี้
