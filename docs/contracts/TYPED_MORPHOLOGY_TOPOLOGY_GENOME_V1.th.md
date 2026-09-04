# Typed Morphology and Topology Genome V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `TYPED_MORPHOLOGY_TOPOLOGY_GENOME_V1.md`

## จุดประสงค์และขอบเขตคำอ้าง

`typed_morphology_topology_genome_v1` แทน candidate เป็น bounded typed graphs แทน fixed list ห้า part ที่ควบคุมด้วย scalar dimension ห้าค่า Validator และ topology signature ที่ไม่ขึ้นกับ identifier อยู่ใน `src/formula_ultimate/search/topology_genome.py`; corpus ที่รับคือ `config/genomes/typed_morphology_topology_genome_v1.json`; และ deterministic report สร้างด้วย `scripts/experiments/inspect_topology_genome_corpus.py`

การผ่านพิสูจน์เฉพาะ representation และ functional traceability ก่อน CAD V1 ไม่ mutate genome, สร้าง full assembly, พิสูจน์ interface geometry, รัน physics หรือยืนยันว่า topology ที่แทนไว้มีประโยชน์

## Root และ source identity

Root ประกาศ exact genome version, SHA-256 ของ Work 092 solid grammar, required domain ทั้งหก, bounded counts และ genomes ขอบเขตรับไม่เกิน 8 parts, 24 interfaces, 32 features ต่อ part และ 24 paths Unknown field/identity ต้อง fail closed Legacy scalar parameter ไม่มี field ที่รับและไม่สามารถกระทบ topology signature

แต่ละ part ประกาศ parent containment, exact Work 092 source candidate/family, material/process identity, ordered feature DAG ที่ใช้ Work 092 operator identity และ final feature Material/process ID เป็นเพียง declaration ไม่ใช่หลักฐานว่ามีอยู่หรือผลิตได้

## Interface, terminal และ path

Interface เชื่อม known part สองตัวที่ต่างกันและประกาศ interface type, functional domain ที่รองรับ และ allowed DOF Duplicate typed edge, self-interface, domain/DOF ไม่รองรับ และจำนวนเกินขอบเขตต้อง fail Parent containment ต้อง acyclic

Terminal ทุกตัวเป็น mandatory และ typed เป็น source, sink หรือ bidirectional ในหนึ่งหรือหลาย domain จาก `load`, `energy`, `motion`, `fluid`, `thermal` และ `control` Required domain ทุกตัวต้องมี source-to-sink path Path ประกาศ ordered parts และ exact interface identities; ทุก adjacent step ต้องตรงกับ endpoint ของ interface และ interface ต้องรองรับทุก domain ที่ path นั้นขนส่ง Terminal และ part ทุกตัวต้องอยู่ใน valid route อย่างน้อยหนึ่งเส้น รายการที่ disconnected ไม่สามารถอ้าง functional closure

Symmetry เป็น optional gene ชัดเจน: `none`, `mirror` หรือ `rotational` ค่า `none` ห้ามซ่อน axis/order จึงไม่ทำให้ symmetry เป็น mandatory prior

## Canonical topology identity

ภายใต้ maximum 8 parts แบบ bounded V1 enumerate permutation ของ part แล้วเลือก complete typed representation ที่เล็กสุดตาม lexicographic ภายในมี part family/source/material/process, feature ancestry ที่ไม่ขึ้นกับ identifier, directed containment, typed interface/DOF, terminal role/domain, functional route และ symmetry จากนั้นใช้ SHA-256 เป็น topology signature

ดังนั้นการ rename part, feature, interface, terminal และ path ID อย่างสอดคล้องจะคง signature ส่วนการเปลี่ยน part/branch, containment, interface, route, feature dependency, material/process declaration หรือ symmetry จะเปลี่ยน signature นี่เป็น exact ภายใน V1 schema/bound ไม่ใช่คำอ้างเรื่อง unbounded graph canonicalization

## Corpus และ replay

ตัวอย่างที่รับหกแบบคือ monolithic, serial-three, branching-four, cyclic-four, nested/cross-linked-five และ asymmetric-hybrid-six Part count คือ `[1, 3, 4, 5, 6]`; topology signature ทั้งหกต่างกัน Corpus มี branching vertex และ interface cycle และไม่สามารถเข้าถึงได้ด้วยการเปลี่ยน scalar value ห้าค่าเดิมเพียงอย่างเดียว

```powershell
python scripts/experiments/inspect_topology_genome_corpus.py `
  --config config/genomes/typed_morphology_topology_genome_v1.json `
  --solid-config config/cad/freeform_brep_solid_grammar_v2.json `
  --output artifacts/work093/run_a/result.json

python scripts/experiments/inspect_topology_genome_corpus.py `
  --config config/genomes/typed_morphology_topology_genome_v1.json `
  --solid-config config/cad/freeform_brep_solid_grammar_v2.json `
  --output artifacts/work093/run_c/result.json `
  --replay-reference artifacts/work093/run_a/result.json
```

## ข้อจำกัดและงานต่อ

V1 ยังไม่กำหนด proposal probability, mutation eligibility, retry budget, crossover, repair, lineage checkpoint หรือ archive selection และไม่รับประกันว่า valid graph ทุกตัวประกอบเชิง geometry หรือ evaluate เชิง physics ได้ Work 094 ต้อง implement reproducible topology mutation และ reject invalid proposal; Work 095–097 จึงค่อยสร้าง construction, semantics, meshing และ physics ก่อนกราฟเหล่านี้สนับสนุน discovery trial ได้
