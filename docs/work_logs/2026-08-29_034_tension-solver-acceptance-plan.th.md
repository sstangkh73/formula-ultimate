# แผนงาน 034: Tension Solver Acceptance Harness

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_034_tension-solver-acceptance-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

Implement และรัน structural solve ที่รับเป็นหลักฐานครั้งแรกของ Formula
Ultimate: axial-tension specimen แบบ fail-closed/replayable ที่พิสูจน์เส้นทาง
local `3D geometry -> Gmsh mesh -> CalculiX solve -> parsed evidence ->
analytical and mesh-convergence gates`

## ขอบเขต

- กำหนด tension experiment หน่วย SI แบบมีเวอร์ชัน ใช้ rectangular prismatic
  solid, isotropic linear-elastic material, distributed end traction และ fixed
  support face
- สร้าง Gmsh geometry และ first-order tetrahedral mesh ที่ characteristic size
  สามระดับซึ่งประกาศล่วงหน้า
- แปลง exact Gmsh mesh เป็น CalculiX input deck พร้อม surface-area-weighted
  nodal load บน finite loaded face
- รัน CalculiX ใน artifact directory แยก และบังคับ fresh expected output กับ
  parsed completion evidence
- Parse displacement, reaction, non-singular axial stress evidence และ
  external-work/strain-energy consistency เมื่อ output ที่รับของ solver รองรับ
- เทียบ `sigma = F/A`, `epsilon = sigma/E`, `delta = FL/(AE)` และ
  `U = F*delta/2`
- Gate force closure, analytical agreement, finiteness, topology/mesh identity
  และ last-two-mesh convergence โดยไม่บังคับ physical minimum thickness
- เก็บ source/config/tool/input/output hash, command, exit behavior, wall time,
  mesh count/quality evidence, repository identity, failure และ structured
  falsification review ใต้ `artifacts/work034/` ที่ ignore
- เพิ่ม unit/integration test ที่ไม่ต้องรัน external solver และ live acceptance
  launcher หนึ่งชุดสำหรับ toolchain ที่ติดตั้งนี้
- ดูแล Markdown อังกฤษ/ไทยเป็นคู่

## ไฟล์ที่วางแผน

- `config/structural/tension_solver_acceptance_v1.json`
- `src/formula_ultimate/structural/__init__.py`
- `src/formula_ultimate/structural/acceptance.py`
- `scripts/structural/run_tension_acceptance.py`
- `scripts/run_work034.ps1`
- `tests/test_structural_acceptance.py`
- `docs/physics/TENSION_SOLVER_ACCEPTANCE.md`
- `docs/physics/TENSION_SOLVER_ACCEPTANCE.th.md`
- แผน/ผล Work 034 ภาษาอังกฤษและไทยที่ตรงกัน

การแบ่ง adapter/parser อาจเปลี่ยนหลังเห็น artifact จริงจาก Gmsh/CalculiX และจะ
บันทึก deviation

## นิยามการทดลอง

### Preferred hypothesis

ภายใน small-strain linear-elastic range ที่ประกาศ solver mesh ทั้งสามสร้าง
valid connected solid, ปิด applied axial force ผ่าน support reaction, ทำ
analytical end displacement/axial stress ภายใน tolerance และให้ global response
converge ระหว่าง mesh สองระดับละเอียดสุด

นี่คือ solver-route verification ไม่ใช่ general structural/physical validation

### ตัวแปรอิสระ

- Gmsh characteristic mesh size ที่ประกาศสามระดับ

### ตัวแปรตาม

- จำนวน node/tetrahedron/boundary face และ mesh identity
- loaded-end axial displacement
- support reaction และ force residual
- named non-singular axial stress evidence
- external work และ admitted internal-energy evidence
- analytical residual, mesh-to-mesh change, solver status, exit behavior,
  artifact, hash และ wall time

### ตัวแปรควบคุม

- ความยาว/หน้าตัด bar และ coordinate frame
- สมมติฐาน material `E`, `nu`, density
- applied resultant force และ surface-load distribution algorithm
- Gmsh/CalculiX executable, element family/order, solver step, parsing rule,
  tolerance, resource policy และ repository/source/config identity

### Falsification และ failure case

- Unit test ปฏิเสธ malformed/non-finite config, geometry ศูนย์/ติดลบ,
  incomplete/disconnected mesh evidence, boundary identity ผิด, stale/missing
  solver output, nodal load ไม่ปิด, malformed/non-finite result และ analytical/
  convergence residual เกินเกณฑ์
- Live route fail หาก Gmsh/CalculiX ให้ process/artifact evidence ที่รับไม่ได้
  ไม่ว่าไฟล์หลังจากนั้นจะมีหรือไม่
- ห้าม retry failed mesh/solve แบบเงียบหรือแทนด้วย analytical value
- ไม่ใช้ singular peak stress เป็น stress metric

## การตรวจสอบ

คำสั่ง fail-fast ที่วางแผน:

```powershell
py -3.14 -m unittest tests.test_structural_acceptance -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

จะบันทึก exact command, exit code, output สำคัญ, solver/parser behavior,
artifact, hash, limitation และ final commit ใน result

## เกณฑ์สำเร็จ

- สร้างและ solve mesh สามระดับผ่าน installed Gmsh/CalculiX จริง
- ทุก mesh มี admitted 3D load path หนึ่งเส้นและ finite support/load face
- Distributed nodal load รวมเป็น exact declared resultant ภายใน tolerance
- Fresh solver evidence พิสูจน์ completion; stale/missing output fail-closed
- Force equilibrium ปิดและ analytical displacement/stress/energy evidence ผ่าน
  tolerance
- Mesh สองระดับละเอียดสุดผ่าน global-response convergence gate
- Replay metadata/source/artifact hash เพียงพอทำ semantic run ซ้ำ
- focused/full/static/repository/staged check ผ่านและ commit สำเร็จ

## ความเสี่ยง

- Exit behavior ของ CalculiX/Gmsh CLI บน bundled Windows installation อาจต่าง
  ระหว่าง version probe กับ actual run
- Gmsh physical-surface export/tetrahedral face identity อาจต้องมี project-owned
  mesh conversion step ชัดเจน
- Equal nodal load ไม่ใช่ uniform traction; adapter ต้อง weight node บน end face
  ด้วย surface-triangle tributary area
- Fixed end nodes ทั้งหมดสร้าง local Poisson/end effect; displacement/stress
  gauge ต้องห่าง boundary
- Linear tetrahedra อาจ stiff หรือ converge ช้า; หากไม่ผ่าน tolerance ต้องเก็บ
  เป็น evidence และอาจวางแผน element-order change แยก
- Solver output format อาจขึ้นกับ version; parser test ต้องใช้ minimal committed
  fixture หรือ generated string และ fail เมื่อ structure ไม่รู้จัก
- Linear elasticity พิสูจน์ yield redistribution, fracture, fatigue, buckling
  หรือ arbitrary candidate safety ไม่ได้

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี bending, torsion, buckling, loaded-interface, plasticity, fracture,
  fatigue, post-failure หรือ vehicle `DNF` implementation ใน work item นี้
- ไม่มี arbitrary minimum thickness, manufacturability constraint, component
  optimization, design-agent search หรือ whole-vehicle geometry
- ไม่อ้าง physical validation, independent solver agreement, safety,
  certification หรือ real-world material accuracy
- ไม่รัน cloud, upload ภายนอก, push, publish หรือ rewrite history
