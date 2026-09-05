# แผน Work 097: Generalized Meshing, Contact, and Failure Evaluation

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-05_097_generalized-meshing-contact-failure-evaluation-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

สร้าง bounded geometry-witness-driven benchmark evaluator เพื่อไม่ให้กรณี curved, tapered, hollow, branching, ribbed, bearing-seat และ contact-pair ถูกปฏิเสธเพียงเพราะไม่ใช่ primitive แต่ละกรณีต้องแสดง model selection, discretization refinement, independent reference comparison, equilibrium/energy residual, typed contact law, failure check, solver-invalid state และการ propagate ไปยัง typed connection edge

## ขอบเขตและไฟล์ที่วางแผนเปลี่ยน

- `config/structural/generalized_geometry_benchmarks_v1.json`
- `src/formula_ultimate/structural/generalized_geometry_benchmarks.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_generalized_geometry_benchmarks.py`
- `tests/test_generalized_geometry_benchmarks.py`
- `docs/contracts/GENERALIZED_GEOMETRY_BENCHMARKS_V1.md` และไฟล์ภาษาไทย
- plan/result ชุดนี้และไฟล์ภาษาไทย
- หลักฐาน pilot/replay/control แบบ deterministic ที่ ignore ใต้ `artifacts/work097/`

## ตัวแปรและ controls

- ตัวแปรอิสระ: exact Work 096 report/comparison identity; benchmark family และ source candidate; support/load/contact region ID; load, torque, pressure, temperature change, material และ failure domain ที่ประกาศ; model-selection rule; contact law; discrete level และ residual/convergence threshold
- ตัวแปรตาม: beam/shell/solid/contact model ที่เลือกพร้อมเหตุผล; geometry input จาก Work 096; reference/discrete response; effective element/sample count; last-two change และ observed order; force/moment/energy residual; bending/torsion/buckling/yield/plasticity/fracture/fatigue/thermal indicator; contact state; solver-valid/invalid state และ typed connection-edge transition/affected functional path
- controls: source/report hash ถูกแก้, เปลี่ยนเป็น primitive-only case, semantic region หาย, model-selection mismatch, level ไม่ refine, response non-finite, equilibrium/energy residual เกิน, non-convergence, contact-law mutation, severed edge ยังส่งแรง, hidden geometry repair, failure evidence หลังเห็นผล และ exact replay mutation

## benchmark adapter 7 แบบ

1. `curved_cantilever`: curved branch จาก Work 092, beam bending reference และ midpoint strain-energy integration
2. `tapered_beam`: tapered open shell geometry ภายใต้ beam idealization ที่ประกาศ, piecewise section reference และ discrete integration
3. `hollow_shell`: tapered hollow duct, membrane reference และ polygonized circumference refinement
4. `branched_joint`: organic/branching geometry, parallel branch bending reference และ discrete integration
5. `lattice_rib_junction`: ribbed gusset geometry, axial rib-network reference และ discrete spring assembly
6. `bearing_seat`: bored hub geometry, annular radial-compliance reference และ radial ring integration
7. `contact_pair`: identity ของ revolved member 4 solids, Hertz normal-contact reference และ bounded Newton refinement พร้อม friction/preload state ที่ประกาศ

analytical/reduced reference และ independent discrete implementation เป็นคนละ code path ทั้งหมดเป็น benchmark adapter ที่ขับด้วย measured geometry summary ไม่ใช่ general-purpose FEA

## กฎ model, mesh, contact และ failure

- model selection ใช้มิติของ benchmark load ร่วมกับ solid count, path/section evidence, thickness ratio และ contact-pair declarationจาก Work 096 หาก expected/selected model ไม่ตรงต้อง reject
- discrete level ต้อง refine อย่างเข้มและรายงาน effective element/sample/iteration Curvature, thickness, section gradient, interface-region count และ stress-gradient classมีส่วนใน refinement justification ที่ประกาศ
- contact law ที่ V1 รับคือ `bonded`, `sliding_friction`, `bearing_preload` และ `hertz_frictional`; ทุก case ต้องประกาศหนึ่งแบบ แต่ยังไม่ใช่ arbitrary 3D nonlinear contact solve
- fine result ทุกตัวตรวจ bending, torsion, Euler buckling, yield/plasticity, fracture-domain, synthetic fatigue damage, thermal stress และ contact validity โดยระบุ mechanism ที่ not applicable ชัดเจน
- failure status update typed connection edge ที่ประกาศ Edge ที่ severed ต้องส่ง force/moment เป็นศูนย์และระบุ affected path ส่วน divergence และ invalid stateต้องคงเป็น result โดยไม่เติม fallback

## เกณฑ์สำเร็จ

- benchmark family บังคับทั้ง 7 ผูกกับ exact non-primitive Work 096 candidate และ mandatory semantic region
- baseline ที่รับทุกตัวผ่าน response-reference, last-two refinement, observed-order/exact-match, equilibrium, moment, energy, contact และ failure-domain gate ที่ประกาศ
- ต้องมีการเลือก beam, shell, solid และ contact พร้อม machine-readable justification และมี contact-law family ครบทั้ง 4 แบบใน suite
- control ที่ฉีด divergence, residual, missing-region, model mismatch, hidden repair, invalid contact law และ noncausal severed-edge ต้อง fail แบบมองเห็นได้
- clean run เดิมต้องสร้าง ordered evidence ทั้งชุดและ result SHA-256 เดิม
- focused tests, compilation, repository contracts, pilot/replay และ full regression ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

reduced benchmark adapter เหล่านี้ไม่ resolve arbitrary 3D stress concentration, local shell mode, plastic redistribution, crack growth, fretting, S-N data จริง, nonlinear material/contact history หรือ mesh geometry จาก STEP การ sampling scalar/section ของ Work 096 อาจพลาด local extrema การผ่านพิสูจน์ frozen benchmark path 7 แบบและ failure bookkeeping ไม่ใช่ arbitrary topology, real-material capacity, design admission, manufacturability, safety หรือ physical validation การ promote เกิน benchmark level ยังต้องใช้ Gmsh/CalculiX อย่างอิสระ
