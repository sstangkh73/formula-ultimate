# แผน Work 080: Mechanical Assembly and Joint Kernel

สถานะ: In progress

ต้นฉบับภาษาอังกฤษ: `2026-09-02_080_mechanical-assembly-joint-kernel-plan.md`

## วัตถุประสงค์และขอบเขต

เริ่ม batch สาม Work ถัดไปด้วยการ preregister โปรแกรมดำเนินงาน Work 080-086 แบบละเอียด แล้วจึง implement mechanical assembly kernel ที่ geometry เป็นสาเหตุตัวแรก Work 080 ต้องประกอบ declaration ของ physical part จาก Work 077/078 ผ่าน constraint แบบ datum, axis และ surface; คำนวณ DOF ที่เกิดจริง; บังคับ joint limit/clearance; ตรวจ alignment, interference, looseness และ overconstraint; และรักษา deterministic replay identity

Plan นี้ยังไม่ถือว่า Work 080 implement เสร็จ การเปลี่ยนเอกสารทันทีคือสร้าง `docs/plans/WORKS_080_086_DETAILED_EXECUTION_PLAN.md` และคู่ภาษาไทย Work 080 จะคง `In progress` จนกว่า code, experiment, negative control, full validation, bilingual result และ implementation commit แยกจะสำเร็จทั้งหมด

## แบบการทดลอง

- ตัวแปรอิสระ: part topology, datum/interface transform, mate type, joint axis/limit ที่ประกาศ, bearing spacing/alignment, clearance/tolerance, preload declaration, connection compliance และ motion sample
- ตัวแปรตาม: constraint rank, translational/rotational DOF ที่เกิดจริง, mate residual, alignment error, axial/radial clearance, interference depth, minimum gap, collision ตลอด motion envelope และ deterministic assembly identity
- ตัวแปรควบคุม: reference mechanism ที่ผ่าน, mirrored/permuted declaration replay, shaft misalignment, redundant two-bearing lock, clearance มากเกิน, interference แน่นเกิน, collision ตลอด joint travel, intended DOF ผิด, interface ซ้ำ/หาย และ transform non-finite
- สมมติฐานที่ต้องการ: reference assembly ที่รับได้เกิด motion ตรง declaration exact และ control ที่ malformed, overconstrained, underconstrained, misaligned, colliding หรือ identity drift ทุกตัว fail closed ก่อน downstream physics
- การหักล้าง: ทิ้ง constraint แบบเงียบ, auto-align geometry, clip joint motion, รับ penetration residual, รายงาน DOF ที่ประกาศแทนค่าคำนวณ หรือ assembly result เปลี่ยนเมื่อสลับเพียง mapping-key order

## ไฟล์ที่วางแผน

- `docs/plans/WORKS_080_086_DETAILED_EXECUTION_PLAN.md` และคู่ภาษาไทย
- schema/config ของ Work 080 ใต้ `config/assembly/`
- assembly/joint implementation ใต้ `src/formula_ultimate/assembly/` หรือ package boundary ที่ review แล้ว
- deterministic runner ใต้ `scripts/assembly/`
- focused unit/acceptance/negative-control tests
- contract/research record สองภาษาและ result record คู่ของ Work 080
- solver/geometry evidence ที่ ignore ใต้ `artifacts/work080/`

ชื่อ implementation file แบบ exact ยังเป็นข้อเสนอจนกว่าจะ review repository boundary ตอนเริ่ม code; program plan จะระบุ intended artifact/interface ของ Work ที่เหลือทั้งเจ็ด

## การตรวจและเกณฑ์สำเร็จ

Program plan EN/TH แบบละเอียดต้องครอบคลุม Work 080-086, dependency, independent/dependent variables, controls, metrics, artifacts, proposed commands, success/failure gate, claim boundary และ stop/go rule สำหรับการจบ Work 080 ในอนาคต focused tests, deterministic replay, full regression, compilation, bilingual contract, staged scope แบบ explicit, `git diff --cached --check`, implementation commit หนึ่งรายการ และ post-commit replay ต้องผ่าน ต้อง freeze geometry/config ก่อน admitted run แรกของ Work 080

## ความเสี่ยงและสิ่งที่ไม่ทำโดยชัดแจ้ง

Constraint-rank calculation อาจไวต่อ numerical singularity การไม่ชนใน sampled motion ไม่พิสูจน์ continuous clearance หาก continuous/swept-volume check ที่ประกาศยังไม่ผ่าน Work 080 ไม่ validate bearing life, contact friction, fastener/weld strength, wear, full multibody dynamics หรือ physical safety และ plan ของ Work หลังจากนี้ไม่อนุญาตให้เริ่ม implementation ก่อน dependency ผ่าน
