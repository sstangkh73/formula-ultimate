# แผนงาน 048: Whole-Vehicle Load Cases และ Structural Coupling

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_048_whole-vehicle-load-cases-plan.md`

## วัตถุประสงค์

แปลง frozen Level 0 vehicle snapshot เป็น quasi-static structural load case ที่ trace และสมดุลได้สำหรับ assembly ที่ Work 047 ยอมรับ แล้วเชื่อม bounded interface demand เข้ากับ structural-failure contract ของ Work 046 โดยไม่สร้างค่ากลางแทน evidence ที่ไม่รองรับอย่างเงียบ ๆ

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม versioned load-case manifest ใต้ `config/vehicle/` ซึ่งมี training/holdout snapshot, frame definition, immutable evidence identity และ structural limit
- เพิ่ม load-case module ใต้ `src/formula_ultimate/simulation/` สำหรับ validate snapshot, rigid-body wrench balance, component/interface load transfer, bounded analytical structural response, failure-coupling input และ deterministic identity
- เพิ่ม acceptance runner และ `scripts/run_work048.ps1` ซึ่งเขียน ignored evidence ใต้ `artifacts/work048/`
- เพิ่ม focused test, physics report สองภาษา และ result record สองภาษาที่ตรงกัน

## นิยามการทดลอง

- ตัวแปรอิสระ: frozen case identifier และ partition, translational acceleration, gravity, aerodynamic wrench, external contact wrench, component mass state และ declared interface capacity
- ตัวแปรตาม: component/interface six-axis wrench, global/local force/moment residual, demand/capacity ratio, structural state/event และ manifest/replay hash
- ตัวควบคุม: exact Work 047 declaration/STEP identity, หนึ่ง immutable snapshot ต่อ case, หน่วย SI, assembly frame เดียว, fixed load-path graph, fixed Work 046 failure-policy identity, frozen training/holdout membership และ threshold ที่ไม่เปลี่ยน
- Falsification control: unbalanced external wrench, missing evidence, geometry identity ที่ถูกเปลี่ยน, unsupported dynamic/contact evidence, partition membership ซ้ำ และ deliberately overloaded interface

## การตรวจสอบ

1. Unit test สำหรับ frame/wrench algebra, residual, partition, identity rejection, overload coupling และ exact replay
2. Acceptance run ครอบคลุม straight acceleration, braking, cornering, combined manoeuvre, bump, aero extreme และ holdout mass-state extreme
3. กำหนด global และทุก interface force/moment residual `<= 1e-5` ในหน่วย SI
4. กำหนด mapped mass/inertia ตรงกับ Work 047 FreeCAD evidence ภายใน relative `1e-6`
5. Unsupported/incomplete evidence ต้อง reject promotion โดยไม่มี neutral numeric substitution
6. รัน full repository test suite, compile check, repository-contract check และ Git whitespace check

## เกณฑ์สำเร็จ

- ทุก applied wrench trace กลับไปยัง frozen snapshot และ exact geometry/material/failure-policy identity ได้
- Training/holdout partition immutable, ไม่ทับกัน และถูก hash ก่อน Work 050
- Nominal case ที่ admit ทุกกรณีสมดุลและให้ deterministic structural result; deliberate overload ต้องให้ degraded/failed state หรือ `DNF` ตาม bounded coupling contract
- การรันซ้ำรักษา exact result hash และ provenance

## ความเสี่ยง

Work 047 grammar มี translation-only primitive และ idealized interface Quasi-static equivalent load อาจสมดุลทางพีชคณิตแต่ละเลย transient, contact, vibration หรือ local stress Analytical interface demand เป็น bounded adapter ไม่ใช่ arbitrary whole-vehicle FEA หรือ physical validation

## สิ่งที่ไม่ทำโดยชัดแจ้ง

ไม่รวม transient crash, vibration, random road, CFD, tyre-test calibration, contact/preload/friction, arbitrary free-form FEA, physical-track validation, design search, push หรือ publication
