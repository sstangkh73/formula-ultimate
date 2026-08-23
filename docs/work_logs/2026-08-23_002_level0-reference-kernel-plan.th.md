# แผนงาน 002: Level-0 Longitudinal Reference Kernel

วันที่: 2026-08-23
สถานะ: เสร็จสมบูรณ์

> ฉบับภาษาไทยของ `2026-08-23_002_level0-reference-kernel-plan.md`

## วัตถุประสงค์

Implement และทดสอบ physics kernel หนึ่งมิติแบบ deterministic ตัวแรกของ
Formula Ultimate พร้อมรักษาเส้นทางในอนาคตให้ agent ออกแบบ geometry ของ
physical component ใน 3D ได้อย่างชัดเจน

## ขอบเขต

- Implement bounded forward-motion longitudinal point-mass model
- Model constant commanded traction, aerodynamic drag, rolling resistance และ
  road grade ด้วยหน่วย SI
- สร้าง immutable state และ per-step telemetry ที่เหมาะกับ replay
- Reject physics input ที่ invalid หรือ non-finite อย่างชัดเจน
- Validate kernel เทียบ analytical reference case และ deterministic replay
- จัดทำเอกสารว่าส่วนประกอบ 3D ที่ agent generate ในอนาคตจะ promote เข้าระบบ
  1D ผ่าน physical property ที่วัดโดยอิสระอย่างไร

## สิ่งที่ไม่ทำ

- Powertrain component graph หรือ topology evolution
- Implementation gearbox, motor, battery, ICE หรือ thermal component
- Tyre slip curve หรือ lateral vehicle dynamics
- Implementation 3D geometry generation, meshing, CFD หรือ FEA
- อ้างว่า Level-0 kernel ทำนายรถแข่งจริง

## สิ่งส่งมอบที่วางแผนไว้

- `src/formula_ultimate/physics/longitudinal.py`
- `tests/test_longitudinal.py`
- แก้ `docs/PHYSICS_SYSTEM_PLAN.md` เพื่ออธิบาย 1D-to-3D contract
- แก้ `README.md` ให้ตรงกับ reference kernel ที่ implement
- `docs/work_logs/2026-08-23_002_level0-reference-kernel-result.md`

## ขอบเขต Model

- การเคลื่อนที่ของรถไม่ติดลบและเป็นหนึ่งมิติ
- Vehicle mass และ road-load parameter คงที่ระหว่าง run
- Tractive force เป็น external command ส่วน drivetrain physics เลื่อนไปภายหลัง
- ประเมิน force ที่ต้น fixed/partial timestep แต่ละช่วง
- Integrate velocity จาก acceleration ส่วน position ใช้ average velocity ใน
  step พร้อมคำนวณจุดหยุดภายใน step อย่างชัดเจนเมื่อจำเป็น
- Grade คงที่ภายใน reference scenario

## แผน Validation

1. รถที่อยู่นิ่งและไม่มี input ต้องอยู่นิ่ง
2. Constant-force acceleration ที่ไม่มี loss ตรงกับ analytical solution
3. Drag-only coast-down เข้าใกล้ analytical solution เมื่อ timestep เล็กลง
4. Grade-equilibrium traction รักษาความเร็วคงที่เมื่อไม่มี loss อื่น
5. รถกำลังไม่พอไม่ถูก integrate ให้มี speed หรือ distance ติดลบ
6. Mass, timestep, duration, coefficient และ non-finite input ที่ invalid fail
7. Input เดียวกันให้ลำดับ state และ telemetry เดียวกัน
8. รัน repository test suite ทั้งหมด, Python compilation และ Git diff
   whitespace gate

## เกณฑ์สำเร็จ

- Analytical/invariant test ที่วางแผนไว้ผ่านบน Windows และ GitHub Actions
- Implementation ใช้ชื่อหน่วย SI ชัดเจนและไม่มี hidden global state
- Final time exact แม้ duration หารด้วย base timestep ไม่ลงตัว
- Result record เก็บคำสั่ง exact และ output แบบย่อ
- เอกสารแยก agent-designed 3D geometry ออกจาก catalog-only parameter selection
  และกำหนด promotion evidence

## เกณฑ์ล้มเหลว

- Kernel reproduce constant-force analytical motion ไม่ได้ภายใน floating-point
  tolerance
- Timestep เล็กลงไม่ลด error ใน drag-only reference case ที่เลือก
- Invalid state ถูก clip เงียบ ๆ นอกเหนือจาก zero-speed boundary ที่ประกาศไว้
- 3D component สามารถ self-report mass/performance ที่ไม่ผ่าน verification เข้า
  1D model

## ความเสี่ยงและการควบคุม

- ผลเชิงตัวเลขอาจดูสมจริงแต่ผิด: ใช้ closed-form analytical reference และ
  convergence test
- Static friction อยู่นอก model แรก: ประกาศ rolling-resistance activation
  ชัดเจนและไม่อ้าง tyre fidelity
- Fixed Level-0 component catalog อาจกดการประดิษฐ์ในอนาคต: กำหนด promotion
  interface สำหรับ generated geometry และ property ที่ solver คำนวณ
- 3D agent อาจ exploit mesh/solver defect: บังคับ geometry validity,
  independent property extraction, multi-fidelity analysis และ replayable
  artifact ก่อน generated component ส่งผลต่อ research fitness
