# แผนงาน 036: การยอมรับ Solid-Shaft Torsion

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_036_solid-shaft-torsion-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

Implement และรัน solid-circular-shaft specimen แบบ replayable เพื่อตรวจว่า
declared pure torque ไหลผ่าน finite 3D solid แล้วสร้าง reaction torque, twist,
signed shear-stress vector field และ external work ตามที่คาดใน declared
small-strain linear-elastic domain

## ขอบเขตของข้ออ้าง

การผ่าน Work 036 จะ verify เฉพาะ Saint-Venant torsion ของ homogeneous,
isotropic, prismatic solid shaft ผ่าน installed Gmsh/CalculiX route ไม่ validate
yielding, plastic redistribution, fracture, fatigue, spline/gear contact,
bearing, joint, rotating inertia, power transmission หรือ vehicle drivetrain

## Canonical fixture ที่เสนอ

- shaft axis: positive `x`
- length `L = 0.1 m`
- radius `R = 0.01 m`
- synthetic material: `E = 70 GPa`, `nu = 0.3`, density `2700 kg/m^3`
- derived shear modulus: `G = E/[2*(1+nu)] = 26.9230769231 GPa`
- base torque magnitude: `T = 10 N*m` รอบ positive `x`
- fixed face: `x = 0`
- loaded face: `x = L`
- stress gauge: interior interval ที่ประกาศล่วงหน้า เริ่มต้น
  `0.02 m <= x <= 0.08 m`
- Gmsh characteristic size ลดลงสามระดับ โดย pin exact accepted sequence ใน
  configuration ก่อน accepted run

ค่าทั้งหมดเป็น synthetic analytical fixture ไม่ใช่ material certificate หาก
first-order tetrahedral sequence ผ่าน gate ไม่ได้ จะเก็บ failed run และเปลี่ยน
mesh/element strategy อย่างชัดเจน โดยไม่ผ่อน tolerance เพียงเพื่อให้ผลผ่าน

## Analytical reference

เมื่อ polar second moment `J = pi*R^4/2`, radial coordinate เทียบ shaft centre
`(y_c, z_c)` และ `y_r = y-y_c`, `z_r = z-z_c`:

```text
J                   = pi*R^4/2
tau_xy(x,y,z)       = -T*z_r/J
tau_xz(x,y,z)       =  T*y_r/J
tau(r)              = T*r/J
tau_max             = T*R/J
theta               = T*L/(J*G)
U                   = T*theta/2
```

สำหรับ fixture ที่เสนอ reference โดยประมาณคือ:

```text
J       = 1.57079632679e-8 m^4
tau_max = 6.36619772368e6 Pa
theta   = 2.36493114917e-3 rad
U       = 1.18246557458e-2 J
```

ค่าจริงจะ generate จาก committed configuration ไม่ copy จากเอกสารที่ปัดเศษ

## การสร้าง Pure-torque load

Loaded circular face จะรับ distributed tangential traction ไม่ใช่ single point
force สำหรับ linear boundary triangle ที่มี vertices `i,j,k`, area `A` และ
linearly varying tangential traction `t`, consistent nodal force คือ:

```text
f_i = A/12 * (2*t_i + t_j + t_k)
```

Assembled load ต้องเป็นไปตามเงื่อนไขรอบ loaded-face centre:

```text
sum(F_i)             = (0, 0, 0)
sum(r_i cross F_i)   = (T, 0, 0)
```

Normalization หรือ pure-wrench projection ใด ๆ ต้อง deterministic, บันทึก และ
มี test โดยลบได้เฉพาะ numerical integration residual ห้ามซ่อน surface identity
ผิดหรือใช้ arbitrary point-load shortcut

## การวัด

### Loaded-face twist

หา twist ด้วย area-weighted least-squares rigid rotation ของ loaded face รอบ
centre ไม่อ่านจาก node เดียว:

```text
theta_fit = sum(w_i * (y_r*u_z - z_r*u_y)) / sum(w_i * r_i^2)
```

ต้องรายงาน radial expansion, axial translation และ rigid transverse translation
แยกเพื่อไม่ให้ปนใน twist อย่างเงียบ

### Reaction และ equilibrium

- total support force vector
- support moment vector รอบ fixed-face centre
- applied-minus-reaction torque residual
- unintended bending moment รอบ `y`/`z`
- external work `0.5*sum(F_i dot u_i)`

### Shear-stress field

เทียบ complete element stress tensor ที่ tetrahedron centroid ใน declared
interior gauge Primary metric คือ volume-weighted signed normalized RMS error ของ
vector `(Sxy, Sxz)` เทียบ analytical field Signed vector correlation gate ป้องกัน
swapped axis/reversed torque ผ่านการเทียบแค่ magnitude Neutral-axis region ต้อง
ไม่ครอง normalization และ end region ยังคง exclude ตามที่ประกาศ

## Experiment matrix

### Canonical mesh sequence

รัน base `+T` บนสาม mesh และ gate:

- finite connected volume และ circular-boundary identity
- applied zero resultant force และ exact torque
- force/moment closure
- analytical twist/external-work agreement
- signed shear-vector RMS/correlation
- last-two-mesh convergence ของ twist, energy และ shear error
- fresh `.msh`, `.inp`, `.dat`, `.frd` evidence พร้อม hash

### Live metamorphic case

ใช้ declared mesh หนึ่งระดับกับ geometry/material/load adapter เดียวกัน:

1. `-T`: twist และ shear component ทั้งสองกลับ sign; energy ยังเป็นบวกและเท่ากัน
   ภายใน tolerance
2. `2T`: twist/shear เพิ่มสองเท่าใน linear range; external work เพิ่มสี่เท่า
3. `2G` fixture: twist ลดครึ่งหนึ่ง ส่วน torque/shear คงเดิมภายใน comparison
   tolerance ที่ประกาศ
4. Missing rotational restraint: solver/evidence ต้อง fail ไม่ใช่คืน admitted
   torsion result

Radius `R^4` sensitivity จะเริ่มจาก unit/reference test ส่วน second live-radius
solve จะเพิ่มเมื่ออยู่ใน common declared compute budget โดยไม่ลด canonical mesh
sequence

## ตัวแปรและ control

### ตัวแปรอิสระ

- characteristic mesh size ของ canonical sequence
- signed torque และ torque scale ของ metamorphic case
- declared shear modulus ของ stiffness metamorphic case

### ตัวแปรตาม

- twist และ contaminating rigid/radial motion
- support force/moment และ residual ทุก component
- interior signed `(Sxy, Sxz)` field metric
- external work และ analytical residual
- mesh count/quality/volume, solver status/iteration, wall time, hash และ typed
  failure status

### ตัวแปรควบคุม

- geometry/coordinate frame
- material-law ID/provenance และ SI units
- boundary/load-face identity และ pure-wrench construction
- clamp, gauge exclusion, element family/order, mesher/solver/adapter version
- tolerance, resource budget, source/config identity และ repository revision

## Gate ที่เสนอ

จะประกาศ initial gate ใน versioned configuration ก่อน accepted run โดย target
bound คือ:

- load resultant เทียบ `T/R`: `<= 1e-8`
- applied torque construction relative residual: `<= 1e-10`
- support torque closure: `<= 1e-5` relative
- unintended support moment component: `<= 1e-5` relative
- twist analytical error: `<= 5%`
- external-work analytical error: `<= 5%`
- signed shear-vector normalized RMS error: `<= 15%`
- signed shear-vector correlation: `>= 0.98`
- last-two twist/work change: `<= 3%`
- last-two shear-error absolute change: `<= 5` percentage points

นี่คือ solver-acceptance gate ไม่ใช่ safety factor หรือ material allowable

## ไฟล์ที่วางแผน

- `config/structural/shaft_torsion_acceptance_v1.json`
- `src/formula_ultimate/structural/acceptance.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_shaft_torsion_acceptance.py`
- `scripts/run_work036.ps1`
- `tests/test_shaft_torsion_acceptance.py`
- regression update ของ structural test เดิมเมื่อ shared code เปลี่ยน
- `docs/physics/SHAFT_TORSION_ACCEPTANCE.md`
- `docs/physics/SHAFT_TORSION_ACCEPTANCE.th.md`
- matching Work 036 result ภาษาอังกฤษ/ไทย

## การตรวจสอบ

คำสั่ง fail-fast ที่วางแผน:

```powershell
py -3.14 -m unittest tests.test_shaft_torsion_acceptance tests.test_beam_bending_acceptance tests.test_structural_acceptance -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work036.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work035.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

## เกณฑ์สำเร็จ

- Canonical real solver mesh สามระดับและ mandatory metamorphic case ผ่าน
- Applied load พิสูจน์ว่าเป็น pure torque ไม่ใช่ hidden force couple ที่มี
  undeclared resultant
- Twist, torque reaction, shear-vector field, energy และ mesh convergence ผ่าน
  independent declared gate
- Reversed/doubled torque และ doubled shear modulus ให้ signed scaling ที่บังคับ
  ส่วน missing restraint fail-closed
- Work 034/035 regression, focused/full/static/staged check, bilingual record,
  explicit commit และ clean committed-tree replay ผ่านทั้งหมด

## ความเสี่ยง

- Faceted tetrahedral approximation เปลี่ยน circular area, volume และ `J` จึง
  ต้องรายงาน/converge geometry error ไม่ผสมเงียบกับ solver error
- First-order tetrahedron อาจ stiff หรือ noisy ใน shear
- Tangential load integration อาจสร้าง unintended force/bending หาก surface
  coordinate หรือ centre identity ผิด
- Full-face clamp สร้าง end effect จึงต้องตรึง interior gauge
- CalculiX text precision อาจไม่พอสำหรับ residual เล็ก ต้องใช้ explicit total
  row หรือ higher-precision evidence แทนการผ่อน physics gateโดยไม่มีเหตุผล

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี yield/plasticity, fracture, fatigue, buckling, contact,
  spline/gear/bearing model, rotating inertia, drivetrain efficiency, failure
  coupling หรือ `DNF`
- ไม่มี arbitrary minimum radius/thickness, whole-vehicle optimization,
  physical-validation claim, external upload, push, publication หรือ history
  rewrite
