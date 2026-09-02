# ผล Work 080: Mechanical Assembly and Joint Kernel

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-02_080_mechanical-assembly-joint-kernel-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

ชุดประกอบอ้างอิงผ่านระบบ rigid-body constraint ที่คำนวณจริง 19 แถว, rank 19, ไม่มีแถวซ้ำ และมี DOF จริง 5 ค่า ชิ้นส่วนสี่ชิ้นต่อกับ ground ครอบคลุม fixed, revolute, prismatic และ spherical โดย SHA-256 ของ STEP ที่แน่นอนจาก Work 078 เป็นส่วนหนึ่งของ canonical assembly declaration ตลอด motion ของ proxy ที่ประกาศไม่มีการชน และมี minimum conservative envelope gap `0.13999999999999999 m`

ผลนี้สนับสนุนเฉพาะ deterministic declaration validation, DOF ที่คำนวณ, การตรวจ mate residual และ clearance ของ proxy envelope ต่อเนื่องเชิงอนุรักษนิยม ไม่ได้ยืนยัน physical validation, exact B-rep collision clearance, ความถูกต้องของ envelope ใน multibody ที่ parent เคลื่อนที่, อายุ bearing, ความแข็งแรงข้อต่อ, การสึกหรอ, friction, fatigue หรือความปลอดภัย

## ไฟล์ที่เปลี่ยน

- `config/assembly/mechanical_assembly_joint_kernel_v1.json`
- `src/formula_ultimate/assembly/__init__.py`
- `src/formula_ultimate/assembly/joint_kernel.py`
- `scripts/assembly/run_joint_kernel_acceptance.py`
- `tests/test_joint_kernel.py`
- `docs/contracts/MECHANICAL_ASSEMBLY_JOINT_KERNEL_V1.md` และไฟล์ภาษาไทย
- ผลฉบับนี้และไฟล์ภาษาไทย
- แผน Work 080 และไฟล์ภาษาไทย ซึ่งเปลี่ยนสถานะเป็น `Completed`

หลักฐาน runtime ที่ ignore ถูกเขียนไว้ใต้ `artifacts/work080/` และไม่รวมใน commit

## การตัดสินใจและหลักฐาน

- คำนวณ constraint rank ด้วย Gaussian elimination แบบ deterministic ที่ tolerance แบบ absolute ซึ่งประกาศไว้ ส่วน rank/DOF ที่คาดหมายเป็น assertion หลังคำนวณ
- frame ต้อง finite, มือขวา, orthonormal และจัดแนวมาแล้ว ไม่มีการ snap, heal, clip หรือซ่อมแบบซ่อน
- ตรวจชนิด interface กับชุด compatibility ของ joint ที่มีขอบเขต
- proxy ของ prismatic ใช้ continuous segment sweep ส่วน revolute/spherical ใช้ conservative swept sphere รอบศูนย์กลางข้อต่อ
- การสลับลำดับ mapping key ไม่เปลี่ยน declaration/result identity แต่การเปลี่ยน exact component geometry hash เปลี่ยนทั้งคู่
- negative controls ปฏิเสธแกน/จุดกำเนิดเหลื่อม, constraint ซ้ำ, DOF ที่ประกาศ/คาดผิด, expected DOF ที่ไม่ใช่จำนวนเต็ม, clearance เกิน, limit ผิด, การชนตลอด motion, interface หาย/ซ้ำ/ไม่เข้ากัน, ค่า non-finite และ frame มือซ้าย

หลักฐานสนับสนุน: ชุดอ้างอิงคำนวณได้ `constraint_rank=19`, `realized_dof_count=5`, `constraint_redundancy_count=0`, `collision_count=0` และ `minimum_motion_envelope_gap_m=0.13999999999999999` ไม่พบหลักฐานขัดแย้งในตัวควบคุมที่ยอมรับ คำอธิบายทางเลือกที่ตรวจแล้ว: ผลผ่านไม่ได้เกิดจากการคัดลอก DOF ที่ประกาศ เพราะค่าประกาศและค่าคาดหมายที่ผิดถูกปฏิเสธแยกกัน หลักฐานที่ยังขาด: การวัด B-rep อิสระและ collision ของ geometry แบบ exact เป็นขอบเขต Work 081

## คำสั่งตรวจสอบจริงและผล

```powershell
python -m unittest tests.test_joint_kernel -v
# exit 0; Ran 10 tests; OK

python scripts/assembly/run_joint_kernel_acceptance.py `
  --output artifacts/work080/acceptance.json
# exit 0; declaration_sha256=81100a8a98b47b404ff925015886e81e1ab3229b264144fa814b4f611509c778
# result_sha256=2db26f683c4cf552c120a6e7878a69be61e2a07ccab8506fde882fec483ff9a1

python -m unittest tests.test_repository_contract -v
# exit 0; Ran 6 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -v
# exit 0; Ran 514 tests in 300.407s; OK (skipped=3 tests ของ pinned CadQuery environment)

python scripts/assembly/run_joint_kernel_acceptance.py `
  --output artifacts/work080/replay_a.json > $null
python scripts/assembly/run_joint_kernel_acceptance.py `
  --output artifacts/work080/replay_b.json > $null
Get-FileHash artifacts/work080/replay_a.json -Algorithm SHA256
Get-FileHash artifacts/work080/replay_b.json -Algorithm SHA256
# exit 0; ไฟล์ผลทั้งคู่ตรงกันแบบ exact:
# ae5abe0025210071c91923446f2feb8635f5885ee292c52ecb135c4c9ffd7c6b
```

## ข้อจำกัดและงานถัดไป

collision bound ของ V1 ใช้ทรงกลมเฉพาะชิ้นส่วนที่ประกาศ ชุดอ้างอิงมี ground joint หนึ่งจุดต่อหนึ่งชิ้นส่วน; implementation นี้ยังไม่ validate โซ่ kinematic ที่ parent เคลื่อนที่ Work 081 ต้อง import ไบต์ STEP ชุดเดียวกันอย่างอิสระด้วย FreeCAD ตรวจ topology และ hash วัด geometry/mass properties หน่วย SI โดยไม่ heal และค้น interface witness จาก geometry signature แทน face index
