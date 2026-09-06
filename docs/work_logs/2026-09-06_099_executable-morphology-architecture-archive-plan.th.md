# แผน Work 099: การค้นหา Morphology, Architecture และ Archive ที่ Execute ได้

ต้นฉบับภาษาอังกฤษ: `2026-09-06_099_executable-morphology-architecture-archive-plan.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และหลักฐานเริ่มต้น

Implement deliverable Work 099 แบบจำกัดตาม `WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md` หลังตรวจ Work 098 commit `ec0004b` ที่เสร็จแล้ว Work 098 สร้าง candidate/evidence identity, immutable event history, cost settlement และ decision replay แต่จงใจยังไม่ execute morphology หรือ implement quality-diversity archive Work 099 จะเพิ่ม representation แบบ numerical solid-network ที่ execute ได้ operators ซึ่งเปลี่ยน architecture และ archives แบบมีขอบเขต โดยคง contract นั้นไว้

งานนี้ยังเป็น software และ CAD execution เท่านั้น Geometry measurements ยืนยันว่า computational objects ที่เสนอมีอยู่และต่างกัน แต่ไม่ยืนยัน useful physics, manufacturing feasibility, race performance, technology novelty หรือ physical validation

## ขอบเขตและไฟล์ที่วางแผน

- `src/formula_ultimate/search/executable_morphology.py`: ตรวจ variable-length numerical geometry, material-region/part, interface, terminal ancestry และ optional controller genes แบบเข้มงวด สร้าง deterministic mutation traces; operators perturb/grow/split/merge/rewire/radius/controller และ functional signatures ที่ไม่ขึ้นกับ ID
- `src/formula_ultimate/search/morphology_archive.py`: deterministic bounded niches ที่แยก feasible, failed และ unresolved slots พร้อม evidence scope, tie-breaking, lineage/novelty retention, capacity และ reproduction/escalation accounting ชัดเจน
- `config/experiments/executable_morphology_qd_v1.json`: seeds, representation bounds, operator schedule, CAD measurement fields, archive descriptors/capacities และ software-fixture claim boundary
- `scripts/experiments/run_executable_morphology_qd.py`: deterministic proposals, CadQuery execution/STEP export, geometry/terminal measurement, Work 098 ledger events, archive updates, failure retention, replay หลังเปิดใหม่ และ comparison ข้าม run ตาม tolerance
- `tests/test_executable_morphology_qd.py`: adversarial schema/operator/archive/identity tests และ optional real-CAD integration ภายใต้ local CadQuery environment ที่ตรึงไว้
- `docs/contracts/EXECUTABLE_MORPHOLOGY_ARCHIVE_V1.md` และ `.th.md`: interface ที่ execute ได้, state/archive semantics, คำสั่ง, หลักฐาน และข้อจำกัด
- แผนสองภาษานี้และผลสองภาษาที่ตรงกัน Generated evidence เก็บใต้ ignored `artifacts/work099/`

## ตัวแปรการทดลองและ controls

- Independent variables: mutation operator และ registered seed; ทดสอบ archive disposition ด้วย descriptor/capacity rules เดียวกัน
- Dependent evidence: genotype identity, canonical functional-graph signature, CAD STEP digest, measured volume/surface/bounds/centre/topology counts, terminal positions/ancestry, niche coverage, archive replacement/retention และ exact ledger decision replay
- Controls: root representation, numerical bounds, material hypothesis, external terminal roles/domains, CAD implementation, operator schedule, proposal count ต่อ seed, archive capacities และ Work 098 software-fixture registration เหมือนกัน
- Success: หลาย seeds execute geometry identities ที่ไม่เคยประกาศมาก่อน; morphology mutation อย่างน้อยหนึ่งรายการเปลี่ยนทั้ง geometry digest และ measured geometric field; split/merge เปลี่ยน decomposition; เกิด canonical functional signatures หลายแบบ; ตัวอย่าง failed/unresolved ยังถูกเก็บแยกอย่างมีขอบเขต; เปิด ledger ใหม่แล้วสร้าง decision state ซ้ำได้ตรงกัน
- Failure: diversity ที่เปลี่ยนเฉพาะ identity หรือ rigid transform, hidden geometry repair, archive โตไม่จำกัด, เขียนทับ failures, ใช้ stale evidence, proposal lineage ไม่ deterministic หรืออ้าง physical/manufacturing/discovery จากหลักฐาน CAD เท่านั้น

## Validation และเกณฑ์สำเร็จ

1. รัน `python -m unittest tests.test_executable_morphology_qd -v` รวม negative finite/bounds/ancestry/identity cases, operators ที่ลงทะเบียนทั้งหมด, deterministic replay, split/merge behavior, archive capacity/tie rules และ claim-boundary checks
2. รัน real CAD fixture สองครั้งด้วย `.tools/cadquery-mcp/Scripts/python.exe` แยก `artifacts/work099/run_a` และ `run_b`; เปรียบเทียบ deterministic genotype, functional, geometry และ measured-field evidence ภายใน numerical tolerances ที่ประกาศ พร้อมรายงาน timing ที่เปลี่ยนได้แยกต่างหาก
3. เปิด Work 098 ledger แต่ละไฟล์ใหม่ด้วย trusted head และยืนยัน exact decision/state replay ตรวจว่า representation-invalid และ boundary-unresolved attempts ยังคงคิดต้นทุนและแยกจาก geometry สำเร็จ
4. รัน targeted regressions `python -m unittest tests.test_discovery_contract tests.test_topology_genome tests.test_topology_mutation tests.test_freeform_solid_grammar tests.test_repository_contract -q` จากนั้น `python -m compileall -q src scripts tests` และ `python -m unittest discover -s tests -q` เป็น final gates
5. ตรวจคู่เอกสารอังกฤษ/ไทย local links และ claim wording; รัน `git diff --check`; stage เฉพาะไฟล์ที่ประกาศ; ตรวจ `git diff --cached --name-only`; รัน `git diff --cached --check`; commit งานนี้และตรวจ commit ใหม่

Validation ทุก gate เป็น fail-fast Blocker ทำให้แผนนี้คง `In progress` หรือเปลี่ยนเป็น `Stopped` พร้อมเหตุผลตรงจริง การเสร็จต้องมี scoped commit ที่สำเร็จ

## ความเสี่ยง การควบคุม และสิ่งที่ไม่ทำอย่างชัดเจน

ความเสี่ยงรวม CAD-kernel nondeterminism, topology change ที่ไม่เปลี่ยน executable shape, terminal ancestry stale หลัง split/merge, archive novelty กลบ failure และ software-fixture labels ถูกเข้าใจผิดว่า physical outcomes ควบคุมด้วย canonical genotype/signature hashing, measured geometry identities, ancestry validation หลังทุก mutation, deterministic tie-breaking, evidence scopes แยกกัน และการเก็บต้นทุน/ประวัติด้วย ledger เวลา CAD มองเห็นได้แต่ไม่รวมใน exact numerical identity comparison

ไม่ทำ Work 100 physics/coupled trials, Work 101 vehicle promotion, field solvers, physical feasibility, manufacturability, race-time optimization, statistical superiority, unrestricted representations, distributed/asynchronous scheduling, external publication, push หรือเปลี่ยนหลักฐาน Work 098 ที่เสร็จแล้ว V1 รองรับ swept-solid network และ registered operators แบบจำกัด ไม่อ้าง arbitrary CAD หรือ universal component discovery
