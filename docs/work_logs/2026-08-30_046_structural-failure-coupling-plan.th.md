# แผนงาน 046: Structural Failure Coupling และ DNF

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_046_structural-failure-coupling-plan.md`

## วัตถุประสงค์

Couple หลักฐาน yield, fracture-initiation, fatigue และ exact-interface ที่ admit แล้วเข้าสู่ typed connection state แบบ deterministic เพื่อให้ localized failure ตัด wrench path, redistribute ผ่าน redundancy ที่ประกาศเมื่อทำได้ หรือปล่อย structural `DNF` เมื่อไม่เหลือ required path

## ขอบเขตและขอบเขตการอ้างผล

นี่คือ bounded coupling-policy experiment ภายใต้ narrow Gate A contract ของ Work 051 งานนี้ validate state transition, event localization, wrench closure, failure-energy accounting, topology logic, race-event typing, replay และ fail-closed behavior ไม่ได้ simulate crack propagation, contact separation dynamics, impact, crash absorption, occupant safety หรือ joint strength จริง

## การออกแบบการทดลอง

- ตัวแปรอิสระ: failure mechanism (`yield`, `fracture`, `fatigue`), absolute crossing time, critical/redundant connection topology, timestep, energy partition และ arbitration tie
- ตัวแปรตาม: state `intact -> degraded -> failed`, connection wrench, redistribution, force/moment residual, stored/released/dissipated energy, event time, subsystem outcome, race event และ replay fingerprint
- ตัวแปรควบคุม: pre-failure state เดียวกัน, exact Work 051 element/boundary identity, connection definition, applied wrench, candidate evidence hash, event priority และ energy policy
- สมมติฐานที่ต้องการ: failed connection ส่ง six-component wrench เป็นศูนย์หลัง localized event; redundant survivor ปิด force/moment residual ภายใน `1e-5`; released + dissipated energy ปิดภายใน `1e-4`; localized event time เปลี่ยนไม่เกิน relative `1e-6` ข้าม frozen timestep refinement; required path ที่ไม่มี survivor ให้ deterministic `DNF`; input เดิม replay ตรงกัน
- การหักล้าง: เก็บ tie และ residual, reject unknown/duplicate connection, reject Gate A evidence นอก domain, reject event time นอก step, reject energy partition ไม่ถูกต้อง และคืน no candidate state เมื่อ evidence invalid

## ไฟล์ที่วางแผน

- `config/simulation/structural_failure_coupling_v1.json`
- `src/formula_ultimate/simulation/structural_failure_coupling.py`
- coupling/race integration exports และ event typing
- `scripts/simulation/run_structural_failure_coupling.py`
- `scripts/run_work046.ps1`
- `tests/test_structural_failure_coupling.py`
- `docs/physics/STRUCTURAL_FAILURE_COUPLING_DNF.md` และ `.th.md`
- result record สองภาษาของ Work 046
- ignored evidence ใต้ `artifacts/work046/`

## การตรวจสอบ

รัน focused tests, deterministic Work 046 experiment, coupling/whole-race regression, full repository tests, Python compilation, repository-contract checks, staged-diff checks, explicit scoped commit และ clean-tree replay

## เกณฑ์ความสำเร็จ

- Failed connection มี six-component post-event wrench เป็น bitwise zero
- Redundant redistribution ผ่าน force/moment residual limit `1e-5` หรือ fail อย่างสังเกตได้
- Failure energy ผ่าน residual limit `1e-4` โดยไม่มีการลบหรือแก้เงียบ
- Event-time refinement ผ่าน relative `1e-6`
- Critical topology ให้ deterministic structural `DNF`; redundant topology คง running เฉพาะเมื่อ re-equilibrate ได้
- Invalid evidence ไม่สร้าง committed connection state และ input เดิม replay ตรงกัน

## ความเสี่ยง

Policy ใช้ typed upstream crossing event ไม่ใช่ transient fracture solver Instantaneous redistribution ไม่รวม stress wave และอาจสร้าง load นอก upstream evidence domain Exact Work 051 identity restriction ตั้งใจให้แคบ

## สิ่งที่ไม่ทำอย่างชัดเจน

ไม่รวม whole-vehicle geometry, arbitrary joint transfer, post-critical structural response, fracture propagation, fatigue crack growth, crashworthiness, design search, push หรือ publication
