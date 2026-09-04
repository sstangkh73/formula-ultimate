# แผน Work 093: Typed Morphology and Topology Genome V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_093_typed-morphology-topology-genome-v1-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

Implement genome แบบ bounded และ canonical ที่แทน candidate ด้วยกราฟ part containment, interface/joint, feature DAG ต่อ part, material/process และ functional path ที่ mutate ได้ แทน fixed component list ร่วมกับ scalar dimension ห้าค่าแบบเดิม ปฏิเสธ genome ที่ terminal บังคับด้าน load, energy, motion, fluid, thermal หรือ control ไม่สามารถ trace เชิงสาเหตุได้ก่อนเข้า CAD

งานนี้กำหนดและตรวจ topology representation ส่วน Work 094 จะเป็นผู้ implement stochastic mutation/recombination ไม่ใช่ Work 093

## ขอบเขตและไฟล์ที่วางแผน

- `config/genomes/typed_morphology_topology_genome_v1.json`
- `src/formula_ultimate/search/topology_genome.py`
- `src/formula_ultimate/search/__init__.py`
- `scripts/experiments/inspect_topology_genome_corpus.py`
- `tests/test_topology_genome.py`
- `docs/contracts/TYPED_MORPHOLOGY_TOPOLOGY_GENOME_V1.md` และไฟล์ภาษาไทยคู่กัน
- แผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- deterministic evidence ที่ ignore ใต้ `artifacts/work093/`

## ชั้นของ genome

1. Functional domain บังคับและ source/sink terminal แบบ typed
2. Part graph พร้อม parent/child containment แบบ bounded และ exact Work 092 solid-family declaration
3. Interface/joint graph พร้อม domain ที่รับและ allowed degrees of freedom
4. Acyclic feature graph ต่อ part พร้อม material/process declaration
5. Ordered path ด้าน load, energy, motion, fluid, thermal และ control
6. Optional symmetry gene (`none`, mirror หรือ rotational) ซึ่งไม่เป็น mandatory vehicle prior

## ตัวแปรต้น/ตามและตัวควบคุม

- Input อิสระ: จำนวน/type/parent ของ part, feature ancestry/operator, interface endpoint/type/domain/DOF, terminal placement/role/domain, ordered path routing, material/process ID และ optional symmetry
- Output ตาม: validity, exact traceability, จำนวน part/interface/path, topology-canonical signature, degree/branch/cycle descriptor, feature-operator coverage และ replay identity
- Negative control: ID ซ้ำ, feature ancestry หาย/อ้างไปข้างหน้า, parent cycle, self-interface, duplicate edge, domain/DOF ไม่รองรับ, source/sink หาย, mandatory terminal orphan, endpoint path ไม่ตรง, domain interface/path ไม่ตรง, route disconnected, symmetry misuse, ค่า non-finite/เกิน bound และ unknown field
- Metamorphic control: ลำดับ key และการ rename identifier แบบสอดคล้องต้องคง topology signature; การเพิ่ม/ลบ branch, part, interface, feature dependency หรือ path ต้องเปลี่ยน

## การตรวจสอบและเกณฑ์สำเร็จ

- Corpus genome valid อย่างน้อยหกตัว มี part count ต่างกันอย่างน้อยสี่ค่า
- Required domain ทุกชนิดมี source-to-sink path; mandatory terminal ทุกตัวอยู่ใน valid path; part step ที่ติดกันทุกคู่ใช้ interface ที่ประกาศและรองรับ domain นั้น
- Canonical typed-graph signature ต่างกันเป็นคู่ไม่น้อยกว่าหกแบบ รวม monolithic, serial, branching, cyclic, nested/cross-linked และ asymmetric hybrid
- Genome valid อย่างน้อยหนึ่งตัวมี part count ต่างจาก assumption ห้า part แบบ fixed ของ Work 050 และ topology signature ต้องไม่พึ่ง scalar dimension ห้าค่าเดิม
- Identifier-renaming/declaration-key-order controls ต้อง replay; branch/reroute/feature-dependency mutation ต้องเปลี่ยน identity
- Focused tests, repository contracts, compilation, deterministic inspector replay และ full regression ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Signature ที่อ่อนอาจสับสนกราฟ isomorphic ที่ rename กับ topology change จริง; path list อาจอ้าง connectivity ที่ interface ไม่รองรับ; optional symmetry อาจกลายเป็น prior โดยไม่ตั้งใจ; และ family label อาจนำ conventional layout กลับมา V1 จึง canonicalize bounded typed graph โดยไม่ขึ้นกับ ID และ validate route edge ทุกตัว งานนี้ไม่ mutate genome, execute ทุก genome ใน CAD, repair invalid topology, evaluate physics/manufacturing, optimize รถ หรืออ้าง discovery
