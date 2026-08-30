# แผนงาน 052: Independent Whole-Vehicle Refined Stress/Deformation Evaluator

สถานะ: หยุดดำเนินการ (Stopped)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_052_independent-whole-vehicle-refined-evaluator-plan.md`

## วัตถุประสงค์

Implement และ falsify independent CalculiX beam-network finite-element evaluator ที่ derive stiffness, displacement, stress และ reaction จาก geometry ของ selected Work 050 candidate กับ frozen Work 048 wrench ปิด blocker `independent_refined_evaluation` เฉพาะเมื่อ analytical benchmark, equilibrium, refinement, identity และ negative-control gate ผ่าน

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม versioned structural protocol ใต้ `config/structural/` พร้อม material evidence class, B31 formulation, refinement level, analytical benchmark, stress/deflection limit และ exact upstream identity
- เพิ่ม project-owned beam-network deck builder และ strict CalculiX parser ใต้ `src/formula_ultimate/structural/`
- เพิ่ม acceptance runner และ `scripts/run_work052.ps1` ซึ่ง consume preserved Work 050 ledger, solve promoted candidate ทุกตัวบน frozen holdout และเขียน ignored evidence ใต้ `artifacts/work052/`
- เพิ่ม focused test, physics report สองภาษา และ result record สองภาษาที่ตรงกัน

## นิยามการทดลอง

- ตัวแปรอิสระ: promoted candidate geometry, frozen holdout load case, B31 subdivisions ต่อ branch และ analytical benchmark load
- ตัวแปรตาม: nodal displacement field, element stress field, support reaction, maximum displacement, maximum equivalent stress, utilization/yield margin, force/moment residual, refinement change, solver status และ hash
- ตัวควบคุม: exact candidate variable/ancestry จาก immutable Work 050 ledger; fixed Work 048 wrench; หน่วย SI; CalculiX 2.22; synthetic isotropic `E`, `nu`, yield stress; fixed support; element orientation และไม่มี capacity-factor input จาก Work 050
- Falsification control: analytical cantilever, reversed-load sign, zero stiffness, missing restraint, altered candidate identity, incomplete solver output และ deliberately undersized section

## การตรวจสอบ

1. ตรวจ B31 deck/parser กับ cantilever reaction, tip deflection `F L^3/(3 E I)` และ bending stress `6 F L/b^3` ภายใน tolerance ที่ประกาศ
2. Solve promoted candidate เก้าตัวสำหรับ frozen holdout สองกรณี ที่ `1/2/4` elements ต่อ branch
3. กำหนด fresh `.inp/.dat/.frd` evidence และ exact solver/tool/config/candidate hash
4. กำหนด force/moment reaction residual `<=1e-5` relative และ last-two displacement/stress change `<=5%`
5. กำหนด finite stress/deformation, positive stiffness และ declared yield margin `>=1.1` สำหรับ promotion
6. รัน repository-contract, focused/full unit, compile, staged-diff และ clean-tree replay gate

## เกณฑ์สำเร็จ

- Analytical benchmark ผ่านโดยไม่เปลี่ยน threshold หลังเห็น solver result
- Promoted candidate/holdout ทุกคู่ให้ complete converged stress/deformation evidence หรือ explicit failure
- Same-input run รักษา result identity; malformed/singular model fail closed
- Evaluator ไม่อ่าน Work 050 capacity factor จึงเป็น structural evidence path อิสระ

## ความเสี่ยง

B31 เป็น one-dimensional beam idealization ของ primitive assembly การเลือก section, rigid joint, fixed ground support, linear elasticity และ scaled quasi-static wrench ละเลย solid stress concentration, contact, preload, local plate behavior, nonlinear material response, buckling และ transient dynamics การผ่าน Work 052 รองรับได้เฉพาะ bounded grammar/load/material/beam domain

## สิ่งที่ไม่ทำโดยชัดแจ้ง

ไม่รวม solid whole-vehicle C3D10 model, nonlinear contact, fracture propagation, crash, vibration, CFD, real material certification, physical test, arbitrary topology, main campaign, push หรือ publication
