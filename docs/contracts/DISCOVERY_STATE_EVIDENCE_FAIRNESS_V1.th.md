# Contract V1 สถานะ หลักฐาน และความเป็นธรรมของการค้นหา

ต้นฉบับภาษาอังกฤษ: `DISCOVERY_STATE_EVIDENCE_FAIRNESS_V1.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Implementation: Work 098; schema `discovery_contract_v1`

แบบกำกับ: [Protocol V1 การค้นพบรถทั้งคันและเทคโนโลยี](WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.th.md) Implementation นี้สร้าง software admission/accounting contract สำหรับการค้นหา geometry, controller และรถในขั้นถัดไป ไม่ได้ยืนยันกฎฟิสิกส์ การ execute CAD, field solution หรือรถที่ค้นพบ

## 1. Modules และ entry point ที่ implement

| ไฟล์ | หน้าที่ |
| --- | --- |
| `src/formula_ultimate/experiments/discovery_registration.py` | Registration envelope แบบเข้มงวด coverage/gate declarations ตรวจ budget/partition และ immutable digest |
| `src/formula_ultimate/experiments/discovery_evidence.py` | Causal identity, orthogonal outcomes, scoped artifact admission, exploratory permission, promotion และ legacy annotations ที่ไม่อ้างเกินจริง |
| `src/formula_ultimate/experiments/discovery_ledger.py` | Single-writer durable JSONL events, semantic replay, costs, recovery, selection และ current scientific eligibility |
| `src/formula_ultimate/experiments/discovery_audit.py` | Score-independent stratified sampling, descriptive error accounting และ numerical replay comparison |
| `scripts/experiments/run_discovery_contract.py` | Execute mixed ledger ที่ประกาศชัดว่า synthetic และเทียบ report แบบ deterministic |
| `config/experiments/discovery_contract_fixture_v1.json` | Software fixture registration ที่ครบ ตัวเลขทั้งหมดเป็นค่าทดสอบ |

รันจาก repository root โดยติดตั้ง package `formula_ultimate` หรือใช้ source import configuration เดิม:

```powershell
python scripts/experiments/run_discovery_contract.py --output-dir artifacts/work098/run_a
python scripts/experiments/run_discovery_contract.py --output-dir artifacts/work098/run_b --replay-reference artifacts/work098/run_a/result.json
python -m unittest tests.test_discovery_contract -v
```

Output directory ของแต่ละ run ต้องใหม่หรือว่าง จะไม่ลบหรือเขียนทับหลักฐานเดิมเพื่อให้ replay ผ่าน Outputs คือ `ledger.jsonl` และ `result.json`; report มี registration, event-head, state และ implementation hashes ทั้งหมดเป็น software fixtures รวมถึง events ที่ใช้ชื่อ `candidate_survivor` หรือ `promotion_ready`

## 2. Frozen registration และ trusted provenance

`freeze(body)` คืน `{body, registration_sha256}` ส่วน `validate_registration(envelope, expected_sha256=...)` ตรวจ fields แบบตรงชุด finite values, identity และ policy constraints ทุก ledger row ตรึง registration hash การเปลี่ยน threshold แล้วคำนวณ registration hash ใหม่คือ registration ใหม่ ledger เดิมจะปฏิเสธ

Declarations บังคับครอบคลุม hypotheses/alternatives, independent variables/controls, task/energy/material/representation/operator/environment identities, matched treatments/seeds, calibration/training/holdout datasets ที่ไม่ทับกัน evaluator coverage, physical/process/holdout/replay/safety/independent gates, intended promotion use, statistical plan, budget partitions, audit design และ execution policy Sample size ของ paired seeds ต้องตรง seed list ห้ามขาด study effect sizes, error limits, test names, interval plans และ stopping criteria V1 ตรวจ statistical declarations แต่ไม่ทำ power analysis หรือ execute scientific hypothesis test

แต่ละ gate ตรึง domain, fidelity และ `fidelity_rank`, evaluator, metric, หน่วย SI หรือ dimensionless `1`, comparator, threshold, minimum refinement count, numerical error limit และ evidence type Field gates ต้องมี refinement เพิ่มขึ้นอย่างน้อยสามระดับ ส่วน independent promotion evaluator ต้องมี implementation identity ต่าง มี source evaluator ที่ลงทะเบียน และประกาศ fidelity rank สูงกว่าหลักฐาน survivor ของ source นั้น Rank ordering เป็นสมมติฐานที่ลงทะเบียน การเป็น physical fidelity ที่เข้มกว่ายังต้อง validate นอก software contract นี้

Registrations และ evaluator coverage records เป็น study inputs ที่เชื่อถือ Hashes ตรวจการสับเปลี่ยนเทียบ inputs เหล่านั้น แต่ไม่ authenticate แหล่งข้อมูลที่โกหกหรือพิสูจน์ว่า solver รันแล้ว Config ปัจจุบันลงทะเบียนเฉพาะ evaluators แบบ `software_fixture` โดยชัดเจน Admitted producer ต้องยืนยัน registry, validation-artifact provenance, geometry applicability และ field evidence อย่างอิสระก่อนใช้ class `admitted_simulation` Work 098 ไม่ได้ติดตั้ง producer ดังกล่าว Known synthetic flags, class mismatch และหลักฐานที่ระบุว่าขาด field execution ห้ามเปลี่ยนป้ายเป็น admitted science

## 3. Candidate และ evidence identity

Candidate declarations มี executable-genotype declaration พร้อม hash, parents, mutation trace, representation, treatment, seed, partition และ dataset Contract นี้ตรวจ declaration/provenance ส่วนการ execute genotype เป็น Work 099 โดย V1 จำกัด declaration ไว้ที่ `1048576` serialized UTF-8 bytes

Causal context ประกอบด้วย:

```text
candidate_id
genotype_sha256
geometry_sha256
material_sha256
boundary_sha256
controller_sha256
environment_sha256
task_sha256
registration_sha256
```

Geometry และ boundary hashes อาจยังไม่ทราบตอนแรก Measured-geometry/boundary event แรกจะ seal identity แต่ละตัวครั้งเดียว Context fields อื่นต้องตรงทั้งหมด การเปลี่ยนแบบภายหลังต้องเป็น descendant ใหม่ V1 จงใจให้ evidence transfer ใช้ได้เฉพาะ exact contexts ยังไม่ implement numerical applicability envelopes หรือ cross-candidate transfer

Scoped evaluation artifact มี body พร้อม hash ซึ่งประกอบด้วย producer/validation/class identities, context hash, gate, dataset, metric/unit/value, convergence, error, refinement levels, evidence type และ diagnostic details ตรวจ outcome labels เทียบ threshold ที่ลงทะเบียน ไม่เชื่อเพียงเพราะ producer เขียน `physically_feasible` หาก artifact hash, class, context, unit, producer, coverage หรือ convergence ผิด จะปฏิเสธ admission

## 4. Outcomes และสิทธิ์ integration

แยก fields เก็บ representation, boundary, physics ตาม gate/domain/fidelity, manufacturing ตาม process gate และ promotion ตาม use ที่ลงทะเบียน Promotion เริ่มต้นระบุ `not_ready` ชัด การผ่านฟิสิกส์ที่ fidelity หนึ่งอาจอยู่ร่วมกับ higher fidelity ที่ unresolved และ manufacturing process ที่ไม่ผ่าน Observations ประวัติยังอยู่ใน event ledger และ outcome history ของ candidate แม้ attempts ภายหลังเปลี่ยน current view

`physically_failed` ต้องมีผล converged ในขอบเขตที่ข้าม threshold ส่วน timeout, divergence, mesh failure, unsupported physics และ lost output เป็น unresolved outcomes พร้อมเหตุผลแยก หากงบหมดก่อน invocation ให้บันทึกด้วย `defer` เป็น `not_evaluated` พร้อม execution disposition `budget_exhausted` Metadata submission ที่ถูกปฏิเสธโยน `DiscoveryViolation`; caller สามารถเก็บ source digest และเหตุผลใน `quarantine` event ที่มี disposition `protocol_invalid` ส่วนรายละเอียด physics payload ที่ไม่ผ่านเก็บใน settlement diagnostics ได้โดยไม่ admit เป็น physical result

`exploration_permission` ต้องมี measured geometry, resolved typed boundary identity, scope ที่ตั้งชื่อ declared missing domains และ explicit approximations ให้สิทธิ์ลอง bounded coupled evaluation เท่านั้น ไม่ใช่ physical pass ไม่ได้รัน assembly solver หรือแต่ง coefficients ที่ขาด

`promotion_decision` ต้องผ่าน survivor gates ที่ลงทะเบียนครบสำหรับ `candidate_survivor` และเพิ่ม safety/independent gates สำหรับ `promotion_ready` Gate results ต้องใช้ current context และ registered use ผล class exploratory promote ไม่ได้ ส่วน fixture promotion มี `scientific_survivor: false` และ `physical_validation: false` Outcome ใหม่จะ reset current promotion view เป็น `not_ready` โดยยังเก็บ decisions ประวัติใน ledger

ใช้ `scientific_summary(state)` สำหรับจำนวนของ campaign ปัจจุบัน Pending work, recovered actual costs ที่ไม่ทราบ หรือ campaign ที่หยุด ปิดกั้น current scientific counts รวมถึง decisions ที่เคยบันทึกแล้ว การอ่าน promotion event เก่าตัวเดียวไม่ใช่ final campaign-admission decision

## 5. Events บัญชีทรัพยากร และ recovery

| Event | ผล |
| --- | --- |
| `candidate` | ลงทะเบียน immutable lineage และคิดหนึ่ง proposal ใน exploration pool ของ treatment/seed |
| `reserve` | ตรวจและจอง resource vector เต็มของหนึ่ง operation ตรึง scope/context พร้อม retry/cache/selection source เมื่อใช้ |
| `start` | บันทึกอย่าง durable ว่ากำลังจะเริ่ม execution ต้องมีก่อน settle result |
| `settle` | ตรวจ result เก็บ observed costs และลงบัญชี registered charge ครั้งเดียว |
| `recover` | ปิด pending operation ตาม lost-output policy ที่ลงทะเบียน ไม่แต่งผลที่หาย |
| `defer` | พิสูจน์ว่าทรัพยากรที่ขอเกิน pool ที่เหลือ บันทึก evaluation ที่ยังไม่เรียกชัดเจน |
| `select` | Replay deterministic audit, quality หรือ bounded failed/unresolved selection จาก training evidence ปัจจุบัน |
| `explore` / `promote` | บันทึก exploratory eligibility และ evidence-based promotion แยกกัน |
| `quarantine` | เก็บ digest/เหตุผลของ input เสียโดยไม่แต่ง physical outcome |

Resources คือ `proposals`, `attempts`, `geometry_executions`, `cad_calls`, `mesh_attempts`, `elements`, `dof`, `solver_iterations`, `cpu_s`, `gpu_s`, `wall_s`, `peak_memory_bytes` และ `cache_hits` ระบุทุก counter ชัด เวลาเป็น seconds และ memory เป็น bytes โดย peak memory ใช้ maximum ไม่ใช่ sum ส่วน `observed_cost` เป็นค่าที่ producer วัด และ `charged` เป็นยอดหักเพื่อเปรียบเทียบตามกติกาที่ลงทะเบียน Library นี้ไม่ได้วัด external process เอง

แต่ละ treatment/seed มี pools แยกเป็น `exploration`, `audit`, `quality`, `stepping_stone` และ `finalist` โดยได้รับ resource opportunity ตาม config เดียวกัน ไม่อนุญาตย้ายงบอัตโนมัติ Primary resource เป็น `cpu_s` หรือ `wall_s` และบังคับ vector limits อื่นทั้งหมดด้วย Audit pools ต้องมีโอกาสมากกว่าศูนย์ มี operation pending ได้เพียงหนึ่งทั่วระบบ เป็น serial scheduler ไม่ใช่ distributed executor

Retries ต้องมี attempt identity ยอดคิดต้นทุน และลิงก์ไป unresolved attempt ล่าสุดใน context/scope เดียวกัน ห้ามหลบ retry cap ด้วยการอ้าง parent เก่ากว่า แบบที่เปลี่ยนคือ descendant ไม่ใช่ retry สำเร็จของ parent ที่พังทางฟิสิกส์ การประเมินผลเดิมซ้ำต้องใช้ explicit cache path ใน V1 ที่จำกัดนี้ ส่วน refinement ใหม่ใช้ gate/fidelity ที่ลงทะเบียนแยก ยังไม่ implement general stochastic replication

V1 มี cache policy เดียวคือ `same_context_full_charge` Cache hit ต้องใช้ source result เดิมตรงทั้งหมดและ reserve อย่างน้อยเท่า registered charge ของ source ยอดหักใช้ elementwise maximum ของ source charge กับ observed costs ปัจจุบัน โดยนับหนึ่ง cache hit และยังรายงาน lookup time จริงที่ถูกกว่าแยกกัน Implementation นี้ไม่ admit cross-candidate, cross-treatment หรือ externally precomputed shared caches

ถ้าต้นทุนจริงเกิน reservation หรือ pool ต้องบันทึกค่าเต็มและหยุด campaign operations ต่อไป ไม่ clamp ซ่อนส่วนเกิน ไม่มี external process watchdog: producer ต้องจำกัด/หยุด solver และส่ง measurements มา Reservation ไม่ใช่หลักฐานว่า execution จริงอยู่ใต้ขีดจำกัด

Recovery ก่อน `start` คิดหนึ่ง attempt และคง physics ว่ายังไม่เรียก Recovery หลัง `start` หักยอด reservation ระบุ actual cost ว่าไม่ทราบ บันทึก `lost_output` และปิดกั้น scientific accounting completeness อาจรองรับการวินิจฉัยที่ระบุว่า non-admitted ต่อได้ ยอด reservation ที่ลงบัญชีไม่ได้ถูกอ้างว่าเป็น upper bound ของต้นทุนงานที่หายจริง Recovery จะไม่ rerun หรือทำ physical operation ซ้ำโดยเงียบ

## 6. Replay, archives และ holdouts

`DiscoveryLedger(path, registration, expected_head=...)` replay ทั้ง JSONL hash chain และทุก semantic event rule Appends ตรวจข้อมูลก่อนเขียน flush และเรียก `fsync` ใช้ exclusive lock file ป้องกัน writers พร้อมกัน และไม่ลบ stale lock ที่มีอยู่โดยอัตโนมัติ ต้องตรวจ writer/process และรักษาหลักฐานก่อน explicit recovery Rows ที่ truncated, malformed, duplicate-key หรือ hash ไม่ตรงต้อง fail closed

Hash chains อย่างเดียวตรวจผู้โจมตีที่เขียน hashes ใหม่ทั้งหมดหรือลบ tail rows ทั้งแถวไม่ได้ ต้องมี `expected_head` ที่เชื่อถือจากอีกแหล่งเพื่อตรวจ rollback/substitution ตอน reopen หากไม่มี checkpoint จะยืนยันได้เพียง internal chain และ semantic consistency ไม่ซ่อม partial tail เงียบ ๆ Hashes ไม่ได้ให้ signature หรือ authenticity claim

Exact decision replay สร้าง state, cost, selection และ promotion จาก events เดิม ส่วน `compare_execution` ตรวจ registration/evaluator/context/tolerance identities ที่ตรึงและ per-field absolute/relative tolerances แยกกัน รายงาน timings ทั้งคู่และไม่อ้าง bitwise equality Comparison helper นี้ไม่ launch solvers

Quality selection ใช้ proxy direction ที่ประกาศและตัดสิน ties ด้วย candidate ID แบบ deterministic แยกแต่ละ treatment/seed ส่วน stepping-stone selection ให้โอกาสแบบจำกัดแก่ failed/unresolved candidates รวม unresolved ที่ไม่มีคะแนน ทั้งสองยังไม่ implement QD archive ของ Work 099 เมื่อ candidate มี holdout-gate result แล้ว จะนำไปสร้าง training descendant ใหม่หรือ selection ถัดไปไม่ได้ Disjoint dataset registration ป้องกัน partition overlap โดยตรง ส่วน provenance ของ external learning ยังเป็นหน้าที่ producer

## 7. ความหมายของ proxy audit

Audit sampling แบ่งกลุ่มตาม treatment, seed และ representation จัดอันดับ candidate IDs ด้วย seeded hash โดยไม่ใช้ proxy score ในการจัดอันดับ ทุก selected record เก็บ stratum population/sample sizes และ inclusion probability ลำดับ input และ proxy scores ที่เปลี่ยนต้องไม่เปลี่ยน selected identities สำหรับ population/seed เดิม

Ledger audit reports ต้องใช้ physical gate ที่ rank สูงกว่าและเทียบกันได้ใน domain, metric และ unit เดียวกัน Unknown reference outcomes ยังคง unknown รายงาน reference-positive/reference-negative denominators, false-negative/false-positive counts และ rates ของ known references **แยกในแต่ละ stratum** พร้อม sample identification bounds สำหรับ reference labels ที่ขาด ไม่มี pooled rate ที่มีอคติ และไม่อ้างว่า bounds นี้เป็น population confidence intervals ถ้าไม่มี reference evidence ทั้งหมด สถานะเป็น `not_estimable`; proxy label ที่ไม่ทราบก็ปิดกั้นการแต่ง rate เช่นกัน

Population inference, power และ registered confidence procedures ต้อง implement สำหรับ admitted experiment ขั้นถัดไป Audit ปัจจุบันยืนยันได้เฉพาะ deterministic sampling และ descriptive accounting ที่ถูกต้อง

## 8. Acceptance mapping และ baselines ที่เก็บไว้

| Acceptance case จาก governing protocol | การตรวจที่ implement ใน `tests/test_discovery_contract.py` |
| --- | --- |
| 1 — Orthogonal states | Physics/process/fidelity outcomes ที่อยู่ร่วมกัน sealed identities, `not_ready` ชัดเจน และ mixed runner promotion events |
| 2 — Distinct failures | Budget deferral, unstarted/started recovery, timeout/unsupported reasons, threshold-label rejection และ quarantine |
| 3 — Exploratory versus promotion | Incomplete exploratory permission; ขาด survivor gate แต่ละตัว; ไม่รับ unbound assembly หรือ unsupported use |
| 4 — Evidence identity | ตรวจทุก causal field, unit, producer, class, refinement, field/scalar และ artifact mismatch |
| 5 — Learning without rewriting | Immutable parents, mutation trace ใหม่ ปฏิเสธ holdout/cross-treatment ancestry และห้าม retry เพื่อซ่อม physical failure |
| 6 — Resource integrity | Serial reservation, once-only settlement, retries, full-charge cache, peak memory, overshoot, per-pool opportunity และ lost costs ชัด |
| 7 — Two replay meanings | Runner outputs ตรงกัน reopened ledger, trusted checkpoints, truncated/tampered inputs และ numerical tolerances |
| 8 — Audit integrity | Score/order invariance, inclusion probabilities, denominators ถูกต้อง unknown bounds และ reference fidelity ที่เข้มกว่า |
| 9 — Registration and claim classes | Registration ครบและ immutable แยก fixture class, statistical/budget inputs และการบล็อก scientific counts ปัจจุบัน |
| 10 — Legacy behavior | `legacy_annotation` ของ Work 095/097 ที่ไม่อ้างเกินจริง พร้อม benchmark regression suites เดิมที่ไม่เปลี่ยน |

Labels `accepted`/`repaired`/`rejected` ของ Work 095 ยังคงเป็น synthetic pre-performance annotations ไม่ใช่ measured manufacturing หรือ physical admission ส่วน `passed` ของ Work 097 ยังคงเป็น scoped scalar benchmark evidence และ `invalid` ที่ระบุ solver divergence จะแปลงเป็น numerical uncertainty ไม่มี legacy output ใด promote อัตโนมัติ และไม่ได้แก้ legacy implementation ทั้งสอง

## 9. ข้อจำกัดและงานถัดไป

Implementation นี้เป็น contract และ executable software fixture ที่ใช้ trusted producer inputs, exact-context applicability, serial scheduling และ cache/recovery policies แบบระมัดระวัง ไม่ validate arbitrary geometry ไม่ประเมิน manufacturability จริง ไม่ execute CAD/field solvers ไม่ค้นพบเทคโนโลยี ไม่พิสูจน์ fairness ของ search distribution จริง และไม่ authenticate scientific artifacts ที่แหล่งข้อมูลโกหก

Work 099 ต้องสร้าง executable numerical morphology, component/interfaces ที่เปลี่ยนได้ และ bounded QD archives ส่วน Work 100 ต้องมี local/coupled evaluators ที่ validate อย่างอิสระและ preregistered contrasts จริง และ Work 101 ต้องสาธิต full-vehicle evidence กับ promotion ที่เข้มกว่า ทุกงานต้องมี work logs, tests และ commits ของตัวเอง ดู [ผล Work 098](../work_logs/2026-09-06_098_discovery-state-evidence-fairness-result.th.md) สำหรับ validation evidence ตรงจริงและข้อจำกัดที่เหลือ
