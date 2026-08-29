# แผนงาน 035: การยอมรับ Beam Bending

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_035_beam-bending-acceptance-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

Implement และรัน canonical structural specimen ถัดไป: cantilever-beam solve
แบบ replayable ที่ตรวจว่า finite transverse end load ทำให้เกิด shear transfer,
bending moment, displacement, axial bending stress, reaction force/moment และ
external work ผ่าน 3D solid ตามที่คาด

## ขอบเขต

- เพิ่ม rectangular cantilever configuration หน่วย SI แบบมีเวอร์ชัน โดยใช้
  synthetic linear-elastic material และ claim boundary เดียวกับ Work 034
- สร้าง Gmsh C3D4 mesh สามระดับที่ประกาศล่วงหน้า และกระจาย transverse end load
  ตาม boundary-triangle tributary area
- ขยาย strict CalculiX parser ให้เก็บ complete element stress tensor โดยยัง
  compatible กับ Work 034
- ประเมิน load-weighted tip displacement, support force/moment closure,
  external work และ interior element-centroid `Sxx` bending-stress field
- เทียบ Euler-Bernoulli reference เฉพาะใน slender, small-deflection และ
  Saint-Venant interior gauge domain ที่ประกาศ
- Gate analytical agreement, force/moment equilibrium, exact volume/element
  coverage, mesh convergence, output freshness, hash และ failure evidence
- เพิ่ม focused test และเอกสาร physics/result ภาษาอังกฤษ/ไทย

## ไฟล์ที่วางแผน

- `config/structural/beam_bending_acceptance_v1.json`
- `src/formula_ultimate/structural/acceptance.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_beam_bending_acceptance.py`
- `scripts/run_work035.ps1`
- `tests/test_beam_bending_acceptance.py`
- `tests/test_structural_acceptance.py`
- `docs/physics/BEAM_BENDING_ACCEPTANCE.md`
- `docs/physics/BEAM_BENDING_ACCEPTANCE.th.md`
- แผน/ผล Work 035 ภาษาอังกฤษและไทยที่ตรงกัน

## นิยามการทดลอง

### Preferred hypothesis

ภายใน Euler-Bernoulli domain ที่ประกาศ C3D4 cantilever solve จาก mesh สามระดับ
ปิด transverse force/root moment, ทำ tip deflection/external work ภายใน
tolerance, ทำ signed interior axial bending-stress field ภายใน tolerance แยก
และ converge ระหว่าง mesh สองระดับละเอียดสุด

### ตัวแปรอิสระ

- Gmsh characteristic mesh size สามระดับที่ประกาศล่วงหน้า

### ตัวแปรตาม

- mesh identity/count/volume และ loaded/fixed surface identity
- load-weighted transverse tip displacement และ external work
- support force และ support moment รอบ declared origin
- signed element-centroid `Sxx` เทียบ Euler-Bernoulli stress ใน declared
  interior gauge domain
- analytical residual, last-two-mesh change, solver status, wall time,
  artifact/source/config/tool hash และ typed failure evidence

### ตัวแปรควบคุม

- geometry, coordinate frame, material law/provenance, resultant force,
  tributary-area load distribution, clamp representation, element family/order,
  gauge exclusion, solver/mesher executable, tolerance และ compute policy

### Falsification case

- ปฏิเสธ malformed/non-finite material, geometry, load, mesh, stress หรือ
  boundary identity
- loaded-face area ผิดหรือ nodal resultant ไม่ปิดต้อง fail
- stress component/element ขาดหรือ evidence identity ซ้ำต้อง fail
- force/moment closure, analytical response และ convergence มี gate แยก
- clamp/load-introduction region ถูก exclude ด้วย geometry ที่ประกาศ ไม่เลือก
  ภายหลังจากเห็นผล
- ห้ามแทน failed solve ด้วย analytical value

## Analytical reference

เมื่อ beam length `L`, section width `b`, bending depth `h`, end force magnitude
`P`, `I = b*h^3/12`, centroid coordinate `z_c = h/2` และ interior element
centroid `(x, z)`:

```text
tip deflection magnitude = P*L^3/(3*E*I)
root moment magnitude    = P*L
Sxx(x,z)                 = P*(L-x)*(z-z_c)/I
external work            = P*tip_deflection/2
```

จะตรวจ stress sign ตาม declared negative-`z` load/coordinate convention การกลับ
sign ถือว่า fail ไม่ใช่ผ่านด้วย absolute value

## การตรวจสอบ

คำสั่ง fail-fast ที่วางแผน:

```powershell
py -3.14 -m unittest tests.test_beam_bending_acceptance tests.test_structural_acceptance -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work035.ps1
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

## เกณฑ์สำเร็จ

- Real Gmsh/CalculiX run ทั้งสามสร้าง fresh admitted evidence
- Applied nodal force ปิดกับ declared resultant
- Support force/root moment ปิดภายใน tolerance ที่ประกาศ
- Tip displacement, external work และ signed interior `Sxx` field ผ่าน
  analytical tolerance ที่ประกาศ
- Mesh สองระดับละเอียดสุดผ่าน displacement/work/stress convergence
- Focused/full/static/staged check ผ่านและ explicit commit สำเร็จ

## ความเสี่ยง

- First-order tetrahedron อาจ stiff เกินจริงใน bending และอาจต้องใช้ mesh ละเอียด
  กว่า tension
- Fully fixed face สร้าง local end stress effect จึงต้องประกาศ stress gauge ให้
  ห่าง clamp/load-introduction region ล่วงหน้า
- Euler-Bernoulli theory ไม่รวม shear deformation/local 3D effect จึงต้องให้
  beam slender และระบุ comparison domain
- Element-centroid stress ของ C3D4 เป็น piecewise constant และอาจ converge ช้า
  กว่า global displacement
- การผ่าน specimen นี้ไม่ validate yield, plastic collapse, buckling, fracture,
  fatigue, joint, contact หรือรถทั้งคัน

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี nonlinear material law, yield credit, fracture, fatigue, buckling,
  loaded-interface failure, connection removal หรือ `DNF` coupling
- ไม่มี arbitrary minimum thickness, design optimization, whole-car geometry,
  independent-solver agreement, physical coupon claim, push หรือ publication
