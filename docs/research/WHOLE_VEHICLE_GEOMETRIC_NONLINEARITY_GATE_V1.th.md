# Whole-Vehicle Geometric-Nonlinearity Gate v1

ไฟล์ต้นฉบับภาษาอังกฤษ: `WHOLE_VEHICLE_GEOMETRIC_NONLINEARITY_GATE_V1.md`

## วัตถุประสงค์และขอบเขต

`whole_vehicle_geometric_nonlinearity_gate_v1` คือ fail-closed post-refinement sensitivity gate สำหรับ bounded Work 062 vehicle-frame grammar โดยจะรัน frozen finalist geometry แต่ละตัวและ Work 048 holdout loads ทั้งสองกรณีซ้ำด้วย CalculiX B31 beams ที่ใช้ `*STEP,NLGEOM` แล้วเปรียบเทียบกับ exact Work 062 fine-mesh linear reference

Gate นี้ทดสอบว่า geometric nonlinearity ขยาย response ของ candidate อย่างมีนัยสำคัญภายใน beam idealization เดิมหรือไม่ แต่ไม่ใช่ buckling certificate เพราะ v1 ยังไม่มี initial imperfection, eigenvalue extraction, branch-following, contact, solid mesh หรือ material plasticity วัสดุยังเป็น synthetic และ linear elastic

## Frozen inputs

- Inclusion rule: all and only Work 062 candidates 51 ตัวที่ผ่าน holdout, Work 053 refinement และ STEP/FreeCAD witness
- Load cases: `aero_extreme` และ `holdout_combined` จาก frozen Work 048 holdout partition
- Geometry: exact candidate variables/declaration จาก immutable Work 062 evidence; ไม่ repair หรือ optimize
- Mesh: B31 subdivisions ต่อ branch เท่ากับ 16 ตรงกับ Work 062 fine reference
- Material: `synthetic_linear_elastic_aluminium_like_v1`, `E = 70 GPa`, Poisson ratio `0.3`, nominal yield stress `250 MPa`; ไม่ใช่ certified allowable
- Solver evidence: exit code เป็นศูนย์และ stdout มี `nonlinear geometric`; หากไม่มีให้ fail closed

## Outputs และ falsification

สำหรับ candidate/load-case แต่ละคู่ Gate บันทึก nonlinear displacement, surface von Mises stress, อัตราส่วนเทียบ linear reference, nonlinear yield margin, process status, confirmation status, failure codes และ canonical SHA-256 result identity

Case ผ่านเมื่อทุกเงื่อนไขเป็นจริงเท่านั้น:

- nonlinear displacement amplification `<= 1.10`
- nonlinear stress amplification `<= 1.15`
- nonlinear yield margin `>= 1.10`
- numeric evidence ทุกค่า finite และ positive
- process และ solver-confirmation checks ผ่าน

Candidate ผ่านเมื่อมี hash-valid terminal result ที่ตรงหนึ่งรายการต่อ required holdout case และทั้งสอง cases ผ่าน Duplicate, missing, extra, tampered, nonterminal, non-finite หรือ identity-mismatched evidence จะถูก reject โดยไม่ repair

## Implementation validation

Linear B31 deck เดิมยังคง step header แบบเดิมเพราะ geometric nonlinearity เป็น opt-in Live CalculiX 2.22 smoke run ยอมรับ nonlinear deck, รายงาน geometric-nonlinearity activation, exit เป็นศูนย์ และสร้าง displacement, stress และ section-force evidence ที่ parser อ่านได้ Unit tests ครอบคลุม threshold boundaries, invalid configuration, missing confirmation, process failure, non-finite values, exact case sets, duplicate cases, tamper detection และ deterministic replay

Work 063 freeze และ commit เฉพาะ adapter การนำไปใช้กับ Work 062 finalists ต้องเป็น clean-tree execution record แยก เพื่อไม่ให้ candidate outcomes มีอิทธิพลต่อ implementation หรือ thresholds
