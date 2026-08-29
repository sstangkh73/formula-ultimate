# ผลงาน 034: Tension Solver Acceptance Harness

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_034_tension-solver-acceptance-result.md`

สถานะ: เสร็จสมบูรณ์

## ผลลัพธ์

Implement และรันผ่าน local structural solver route แรกแล้ว Gmsh tetrahedral
mesh ที่ประกาศล่วงหน้าสามระดับถูก solve ด้วย installed CalculiX 2.22 โดย fresh
parsed displacement, reaction, stress และ external-work evidence ผ่าน
analytical, equilibrium และ last-two-mesh convergence gate

นี่คือ linear-tension solver-route verification เท่านั้น ไม่ใช่ physical
material validation หรือหลักฐาน vehicle safety/failure behavior

## ไฟล์ที่เปลี่ยน

- `config/structural/tension_solver_acceptance_v1.json`
- `src/formula_ultimate/structural/__init__.py`
- `src/formula_ultimate/structural/acceptance.py`
- `scripts/structural/run_tension_acceptance.py`
- `scripts/run_work034.ps1`
- `tests/test_structural_acceptance.py`
- `docs/physics/TENSION_SOLVER_ACCEPTANCE.md`
- `docs/physics/TENSION_SOLVER_ACCEPTANCE.th.md`
- แผน/ผล Work 034 ภาษาอังกฤษและไทย

สร้าง ignored replay evidence ใต้ `artifacts/work034/` และไม่ได้เพิ่มเข้า Git

## การตัดสินใจและ deviation

- แปลง exact ASCII MSH 2.2 mesh ของ Gmsh เป็น project-owned CalculiX C3D4
  deck โดย solver adapter ไม่สร้าง mesh ใหม่
- Loaded-face nodal force ใช้ surface-triangle tributary area และรวมปิดกับ
  resultant `1000 N` ที่ประกาศ
- Mean `Sxx` ถูก weight ด้วย tetrahedron volume โดย stress output ต้องครอบคลุม
  exact tetrahedral element set และ total mesh volume ต้องปิดกับ declared volume
- Parser จำกัด table ด้วย named header และปฏิเสธ missing, non-finite หรือ
  duplicate evidence identity ส่วนนี้เพิ่มหลัง failed run แรกแสดงว่า unbounded
  stress block รับ strain row เข้ามาด้วยและให้ค่า mean เท็จประมาณ `5 MPa`
- ยังไม่ได้ parse solver-reported internal strain energy โดย energy gate ใช้
  load-weighted external work `0.5*sum(F_i*u_i)` เทียบ `F*delta/2` และระบุเป็น
  ข้อจำกัดอย่างชัดเจน ไม่ใช่ independent energy agreement
- Artifact summary เก็บ process stdout รวม Gmsh mesh-quality diagnostic แทนการ
  แปลงข้อความเป็น scalar ที่ไม่มีนิยาม

## หลักฐานจากการรันจริง

Analytical reference คือ `delta = 1.4285714285714287e-5 m`,
`sigma = 1.0e7 Pa` และ `U = 7.1428571428571435e-3 J`

| Mesh | Nodes | C3D4 | Displacement (m) | Error | Volume-weighted Sxx (Pa) | Force closure relative |
|---|---:|---:|---:|---:|---:|---:|
| coarse_10mm | 86 | 198 | 1.4162150e-5 | 0.86495% | 9,999,999.72 | 2.0e-7 |
| medium_7p5mm | 140 | 313 | 1.4182479165e-5 | 0.72265% | 9,999,999.89 | 0 |
| fine_5mm | 190 | 434 | 1.4198094754e-5 | 0.61334% | 9,999,999.88 | 3.0e-8 |

Last-two-mesh relative change เท่ากับ `0.0011010479343227404` สำหรับ
displacement, `0.0011010479343228495` สำหรับ external work และ
`1.69621242167361e-9` สำหรับ mean axial stress ทุกค่าต่ำกว่า limit ที่ประกาศ

Live summary คือ `artifacts/work034/experiment_summary.json` ซึ่งเก็บ
config/source/tool/per-artifact SHA-256 hash, exact command, exit code, wall
time, repository identity, parsed metric และ falsification review

## การตรวจสอบ

ทุกคำสั่งต่อไปนี้คืน exit status `0` ตาม fail-fast order เมื่อ 2026-08-29:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
py -3.14 -m unittest tests.test_structural_acceptance -v
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Output สำคัญ:

```text
live: status=passed, mesh_count=3, finest_nodes=190,
      finest_tetrahedra=434, finest_displacement_m=1.4198094754435222e-05,
      finest_stress_pa=9999999.875755485,
      force_closure_relative=3.000000003794412e-08
focused: Ran 7 tests ... OK
full: Ran 275 tests in 24.960s ... OK
compileall: no output
git diff --check: no output
git diff --cached --check: no output
```

Staged scope มีเฉพาะ 12 ไฟล์ที่ระบุของ Work 034 และจะรายงาน commit hash ใน
final handoff หลัง required commit สำเร็จ

## Falsification review

Supporting evidence คือ fresh connected mesh สามระดับ, exact finite-volume/load
coverage, reaction ที่ปิด, analytical agreement และ convergence ไม่มี accepted
run ใดขัด preferred local linear-tension hypothesis หลังแก้ parser defect และ
เพิ่ม test ล็อก table boundary

Alternative explanation ยังคงอยู่: uniform prismatic specimen ง่ายผิดปกติ และ
analytical agreement ไม่ generalize ไป arbitrary geometry/nonlinear failure
Confidence สูงเฉพาะ local installed solver route นี้

## ข้อจำกัดและงานถัดไป

ยังไม่มี independent-solver agreement และ physical coupon data รวมทั้งยังไม่
implement bending, torsion, buckling, loaded interface, yield/plasticity,
fracture, fatigue, connection removal, subsystem failure และ vehicle `DNF`
milestone แยกถัดไปควรเพิ่ม beam-bending specimen พร้อม independently derived
deflection/stress gate ก่อนเริ่ม whole-vehicle work
