# ผล Work 093: Typed Morphology and Topology Genome V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_093_typed-morphology-topology-genome-v1-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

Work 093 แทนขอบเขต representation แบบ fixed list ด้วย bounded typed topology genome Genome ที่รับหกแบบครอบคลุม part count ต่างกันห้าค่าและ topology signature ที่ไม่ขึ้นกับ ID ซึ่งต่างกันเป็นคู่ครบหกค่า Terminal ด้าน load, energy, motion, fluid, thermal และ control ทุกตัว trace ผ่าน exact compatible interface ก่อน CAD

งานนี้พิสูจน์เฉพาะ topology representation และ traceability ไม่ได้รัน genome mutation, CAD assembly, physics หรือ discovery

## ไฟล์ที่เปลี่ยน

- `config/genomes/typed_morphology_topology_genome_v1.json`
- `src/formula_ultimate/search/topology_genome.py`
- `src/formula_ultimate/search/__init__.py`
- `scripts/experiments/inspect_topology_genome_corpus.py`
- `tests/test_topology_genome.py`
- `docs/contracts/TYPED_MORPHOLOGY_TOPOLOGY_GENOME_V1.md` และไฟล์ภาษาไทยคู่กัน
- แผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- หลักฐาน replay ที่ ignore ใต้ `artifacts/work093/`

## การตัดสินใจและหลักฐาน

- Genome มี part containment, Work 092 source solid family, feature DAG ต่อ part, material/process identity, typed interface/DOF, terminals, ordered functional paths และ optional symmetry
- Adjacent path step ทุกตัวต้องอ้าง interface ที่เชื่อม exact parts และรองรับทุก domain ที่ขนส่ง
- Terminal/part ทุกตัวต้องอยู่ใน valid path และ parent containment ต้อง acyclic
- Topology signature enumerate permutation ทั้งหมดภายในขอบเขตแปด part แล้ว hash complete typed representation ที่เล็กสุดตาม lexicographic การ rename identifier อย่างสอดคล้องจึงคง signature
- Field แบบ legacy five-scalar อยู่นอก schema และ fail closed
- Initial corpus validation เปิดเผย cross-link ที่ domain ไม่เข้ากันในตัวอย่าง nested/asymmetric จึงประกาศ electrical กับ fluid/thermal interface แยกกัน โดยไม่แอบเพิ่ม domain ให้ interface คนละชนิด

## หลักฐาน corpus ที่สำเร็จ

| Genome | Parts | Interfaces | Paths | Branch parts | Cycle rank |
|---|---:|---:|---:|---:|---:|
| `monolithic_crossdomain_001` | 1 | 0 | 1 | 0 | 0 |
| `serial_three_001` | 3 | 2 | 1 | 0 | 0 |
| `branch_four_001` | 4 | 3 | 3 | 1 | 0 |
| `cyclic_four_001` | 4 | 4 | 2 | 0 | 1 |
| `nested_crosslink_five_001` | 5 | 7 | 3 | 3 | 3 |
| `asymmetric_hybrid_six_001` | 6 | 7 | 3 | 2 | 2 |

- Distinct part counts: `[1, 3, 4, 5, 6]`
- Unique topology signatures: `6 / 6`
- Source Work 092 declaration: `a0e1c47ee15dbebac9dce2183a502c26199197b751fe427c74c2824dd1b4ad8a`
- Genome declaration SHA-256: `e1583e9aec9c3a4968ec5e35d1b81478d9023ca2392e08ec78ee0a48e9e5c69d`
- Result SHA-256: `65599c0b3153609c2b532d10b95051c339d1766ffbd345dfefded711e6bfab0e`
- `legacy_five_scalar_dependency: false`
- `cad_executed: false`

## คำสั่ง validation แบบ exact

```powershell
python -m unittest tests.test_topology_genome -v
# exit 0; ผ่าน 7 tests

python scripts/experiments/inspect_topology_genome_corpus.py --config config/genomes/typed_morphology_topology_genome_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --output artifacts/work093/run_a/result.json
# exit 0

python scripts/experiments/inspect_topology_genome_corpus.py --config config/genomes/typed_morphology_topology_genome_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --output artifacts/work093/run_c/result.json --replay-reference artifacts/work093/run_a/result.json
# exit 0; complete result equality

python -m compileall -q src scripts tests
python -m unittest tests.test_topology_genome tests.test_repository_contract -v
# exit 0; ผ่าน 13 tests

python -m unittest discover -s tests -q
# exit 0; ผ่าน 654 tests ใน 475.837 s; skip 7 รายการที่ขึ้นกับ environment ตามคาด
```

Full-regression process ก่อนหน้าจบอยู่นอก execution session ที่เก็บไว้ จึงไม่นับเป็นหลักฐาน ระบบรัน full suite ด้านบนใหม่และสังเกต exit status โดยตรง

## ข้อจำกัดและงานต่อ

Material/process ID เป็น declaration ไม่ใช่ evidence Interface domain แสดง routing compatibility แต่ยังไม่พิสูจน์ geometry ที่เข้ากันหรือ conservation Bounded permutation canonicalizer exact ภายในแปด part แต่ตั้งใจไม่ใช้กับ unbounded graph Work 094 ต้องเพิ่ม proposal แบบ reproducible สำหรับ add/remove/split/merge/branch/reroute พร้อม lineage และ bounded retries; Work 095 ต้องปฏิเสธ construction/manufacturing failure ให้มองเห็น
