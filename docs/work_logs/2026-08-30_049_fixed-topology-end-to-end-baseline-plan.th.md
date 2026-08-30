# แผนงาน 049: Fixed-Topology End-to-End Whole-Vehicle Baseline

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_049_fixed-topology-end-to-end-baseline-plan.md`

## วัตถุประสงค์

รัน immutable reviewed Work 047 vehicle หนึ่งคันผ่าน complete evidence chain ที่ยอมรับอยู่ก่อนเริ่ม search: deterministic CAD, STEP, independent FreeCAD property, frozen Work 048 training/holdout load, bounded structural/failure outcome และ coupled Level 0 race decision พร้อม falsify chain ด้วย weak, disconnected, heavy-feasible, timestep และ structural-resolution control

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม fixed-baseline manifest ใต้ `config/vehicle/` ที่ pin upstream identity, Level 0 energy/time input, structural capacity scale, timestep level และ refinement level ทั้งหมด
- เพิ่ม end-to-end baseline evaluator ใต้ `src/formula_ultimate/experiments/` และ runner ใต้ `scripts/experiments/`
- เพิ่ม `scripts/run_work049.ps1`, focused test, baseline report สองภาษา และ result record สองภาษาที่ตรงกัน
- เขียน ignored evidence ใต้ `artifacts/work049/`

## นิยามการทดลอง

- ตัวแปรอิสระ: immutable baseline variant, training/holdout partition, capacity scale, declared mass scale, structural resolution label, Level 0 timestep และ frozen energy/race input
- ตัวแปรตาม: CAD/STEP/FreeCAD identity, load-case result hash, maximum structural utilization, failure event/outcome, Level 0 energy/time state, finish หรือ `DNF`, convergence metric และ compute/process evidence
- ตัวควบคุม: ไม่มี geometry mutation สำหรับ reference baseline, fixed adapter/settings/seed/component library, exact Work 048 partition hash, evaluator API เดียว, หน่วย SI และ explicit unsupported-evidence state
- Falsification control: deliberately weak capacity, disconnected load path, heavy but feasible mass, missing evidence, repeated same-input run และ paired timestep/structural-resolution level

## การตรวจสอบ

1. Unit test identity pinning, reference finish, weak/disconnected `DNF`, heavy-feasible finish และ exact replay
2. เรียก Work 048 เป็น upstream CAD/FreeCAD/load/failure stage และกำหนดให้ clean result identity ผ่าน
3. ต้องมี complete result สำหรับ frozen training/holdout ทุกกรณี
4. Timestep และ bounded structural-resolution change ต้องผ่าน preregistered relative gate
5. นับ deliberate failure เป็นผลลัพธ์ ห้าม repair หรือทิ้ง
6. รัน repository-contract, full unit, compile, staged-diff และ clean-tree replay gate

## เกณฑ์สำเร็จ

- Reference fixed topology finish bounded Level 0 fixture ที่ประกาศและ structurally feasible สำหรับ training case ทั้งหมด
- Weak/disconnected control ให้ explicit `DNF`; heavy control ยัง feasible แต่ช้ากว่าและใช้พลังงานมากกว่า
- การ evaluate ซ้ำรักษา exact hash และทุก output ระบุ upstream commit/config/STEP/partition evidence
- Unsupported evidence คืน invalid result โดยไม่มี candidate fitness

## ความเสี่ยง

Race state เป็น bounded deterministic Level 0 fixture ไม่ใช่สนามจริง Structural resolution เป็น analytical capacity perturbation audit ไม่ใช่ mesh-converged whole-vehicle FEA Baseline ที่สำเร็จอาจ validate orchestration แต่ scientific apparatus ยังอาจไม่พร้อมสำหรับ main campaign

## สิ่งที่ไม่ทำโดยชัดแจ้ง

ไม่รวม autonomous mutation, optimization, novelty claim, physical vehicle validation, real-circuit admission, safety certification, CFD, whole-vehicle stress FEA, manufacturing proof, push หรือ publication
