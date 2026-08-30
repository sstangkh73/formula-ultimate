# แผนงาน 042: การยอมรับ Yield และ Plasticity Solver

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_042_yield-plasticity-solver-acceptance-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

ตรวจว่า CalculiX route ที่ติดตั้งเปลี่ยนจาก elastic ไปเป็น declared bilinear elastic-plastic response เมื่อถึง yield, สะสม plastic strain และคง residual deformation หลัง unload แทนการมี linear-elastic strength แบบไม่จำกัด

## ขอบเขตและข้ออ้าง

- ใช้ synthetic rate-independent isotropic bilinear material ที่ `E=70 GPa`, `nu=0.3`, `sigma_y=250 MPa` และ declared total post-yield tangent `Et=1 GPa`
- ใช้ uniform prismatic tension coupon และ homogeneous end loading ในหน่วย SI
- เทียบ solver onset, post-yield tangent, plastic strain, residual strain, reaction, work partition และ mesh สองระดับกับ independently implemented closed-form uniaxial reference
- มี below-yield negative control, unload-to-zero sequence, reversed loading ภายในข้อจำกัด isotropic hardening ที่ประกาศ และ exact rejection สำหรับ material provenance/law ที่ขาดหรือ malformed

งานนี้ตรวจ numerical material-law route เท่านั้น Synthetic material ไม่ใช่ real-alloy allowable และไม่พิสูจน์ temperature/rate effect, cyclic plasticity, fracture, fatigue, component strength หรือ vehicle safety

## การออกแบบการทดลอง

- ตัวแปรอิสระ: load amplitude, loading direction/history, hardening declaration และ structured mesh density
- ตัวแปรตาม: axial stress/strain, yield-onset load, tangent stiffness, equivalent plastic strain, residual displacement/strain, reaction closure, elastic energy, plastic work, external work, convergence, hash และ replay identity
- ตัวแปรควบคุม: coupon geometry, material identity, temperature/rate declaration, boundary surface, integration rule, solver executable, parser และ absolute load schedule
- สมมติฐานที่ต้องการพิสูจน์: onset/tangent/residual/energy/equilibrium และ mesh gate ทุกตัวผ่านสำหรับ synthetic law
- การพยายามหักล้าง: เก็บ below-yield และ post-yield case, reject non-finite/missing step evidence และห้ามใช้ analytical value แทน solver output ที่ไม่มี

## Implementation และไฟล์ที่วางแผน

- versioned `config/structural/yield_plasticity_acceptance_v1.json`
- elastic-plastic record, analytical reference, structured mesh/deck generator และ multi-step parser ใต้ `src/formula_ultimate/structural/`
- Work 042 runner/launcher และ ignored evidence ใต้ `artifacts/work042/`
- focused negative/analytical tests
- bilingual physics report และ matching result records

Admitted solver deck จะใช้ CalculiX `*PLASTIC` convention คือ yield stress เทียบ equivalent plastic strain Configured total tangent `Et` จะถูกแปลงเป็น plastic hardening modulus `H=E Et/(E-Et)` เพื่อให้ uniaxial total stress-strain tangent คงเป็น `Et`

## Validation และเกณฑ์สำเร็จ

- yield-onset error `<=2%`, post-yield tangent error `<=5%`, residual-strain error `<=5%`
- reaction residual `<=1e-5`, energy-ledger residual `<=1e-4` และ below-yield plastic strain เล็กจนละเลยได้
- last-two-mesh nominal-response change `<=5%`
- deterministic event/step identity และ invalid material/provenance control ต้อง fail closed
- focused test, live installed-solver run, full test, compile check, staged-diff check, explicit commit และ clean-tree replay ผ่านทั้งหมด

## ความเสี่ยงและสิ่งที่ไม่ทำ

ต้องสังเกต CalculiX output name/multi-step table structure แล้ว freeze ใน parser test Load-controlled unloading อาจต้องมี load step เพียงพอเพื่อ integrate work โดยไม่ซ่อน bilinear corner ไม่มี element deletion, fracture, fatigue, kinematic hardening, ratcheting, arbitrary CAD component, whole vehicle, push หรือ publication
