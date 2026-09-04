# แผน Work 094: Reproducible Topology Mutation and Recombination

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_094_reproducible-topology-mutation-recombination-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

Implement proposal machinery แบบ deterministic และ bounded ที่เปลี่ยน typed topology ของ Work 093 โดยไม่ hand-author child ทุกตัว Proposal ทุกตัวต้องบันทึก exact parent identity, seed/RNG checkpoint, operator/probability ที่เลือก, attempt/retry accounting แบบ bounded, mutation trace, validation outcome และ final genotype/topology identity

## ขอบเขตและไฟล์ที่วางแผน

- `config/experiments/topology_mutation_v1.json`
- `src/formula_ultimate/search/topology_mutation.py`
- `src/formula_ultimate/search/__init__.py`
- `scripts/experiments/run_topology_mutation_pilot.py`
- `tests/test_topology_mutation.py`
- `docs/contracts/REPRODUCIBLE_TOPOLOGY_MUTATION_V1.md` และไฟล์ภาษาไทยคู่กัน
- แผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- หลักฐาน pilot/replay deterministic ที่ ignore ใต้ `artifacts/work094/`

## ตัวแปรต้น/ตามและตัวควบคุม

- Input อิสระ: Work 093 parent corpus/identity ที่ freeze, initializer stratum, RNG seed/checkpoint, operator probability table, attempt/retry budget, typed part/interface/domain pool, material/process compatibility table และ mutation-after-observation policy
- Output ตาม: proposal sequence, selected operator, attempt/retry count, accepted/rejected state, failure code, child genotype/topology identity, topology-change status และ opportunity/yield ต่อ family
- Control: parent/seed/budget เดิมต้อง replay exact; key reorderingต้องคง protocol identity; seed/checkpoint/operator budget ที่เปลี่ยนต้องเปลี่ยน lineage; parent cycle, mandatory terminal disconnected, joint/domain เป็นไปไม่ได้, material/process ไม่เข้ากัน, retry budget หมด และ mutation หลังเห็น result ต้อง fail ให้เห็น

## Bounded proposal family ที่รับ

- `grow_branch`: เพิ่ม typed child part, interface, sink terminal และ domain branch ที่ route แล้ว
- `prune_branch`: ลบ terminal leaf ที่เข้าเงื่อนไขและ reroute/remove declaration ที่ครอบคลุมเฉพาะเมื่อ mandatory domain ทั้งหมดยัง trace ได้
- `split_part`: แทน routed part position หนึ่งตำแหน่งด้วยสอง serial parts และ compatible interface
- `add_crosslink`: เพิ่ม non-duplicate typed interface ระหว่าง existing parts
- `reroute_path`: แทน route ด้วย alternate compatible interface chain
- `replace_solid_family`, `insert_feature` และ `mutate_material_process` เป็น typed non-topology controls

Protocol แทน optional crossover ไว้แต่ปิดใน V1 pilot เว้นแต่ parent สองตัวเปิด typed cut boundary ที่ compatible exact Opportunity ที่ปิดต้องถูกบันทึก ไม่ย้ายแบบเงียบ

## ความเป็นธรรมและเกณฑ์สำเร็จ

- Initializer stratum แบบ primitive, skeletal/serial, shell, rotary, branching และ hybrid ได้ proposal slot เท่ากัน; slot ที่ใช้ไม่ได้/invalid ห้ามโอนไป family อื่น
- Topology-changing operator family อย่างน้อยสี่ชนิดต้องสร้าง Work 093-valid child genome ใน bounded pilot
- Accepted topology proposal ทุกตัวต้องมี topology signature ต่างจาก parent; non-topology control ห้ามถูกเรียกเป็น topology change
- Clean run ที่เหมือนกันต้องสร้าง ordered ledger และ result SHA-256 exact เหมือนกัน
- Negative control ต้องปฏิเสธ cycle, disconnected terminal/domain, interface rule ที่เป็นไปไม่ได้, material/process ไม่เข้ากัน, post-result mutation และ replay mutation
- Focused tests, compilation, repository contracts, pilot/replay และ full regression ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Mutation อาจ bias ไปกราฟเล็กที่ง่าย, retry จนได้ผลที่ชอบ, โอน compute ระหว่าง initializer family โดยไม่ตั้งใจ หรือสร้าง novelty จาก ID อย่างเดียว V1 ใช้ fixed slots, deterministic operator selection, bounded retries และ Work 093 canonical signature งานนี้ไม่ execute CAD/physics, ทำ result-conditioned repair, optimize operator probability, อ้าง quality หรือ implement graph crossover แบบไม่จำกัด
