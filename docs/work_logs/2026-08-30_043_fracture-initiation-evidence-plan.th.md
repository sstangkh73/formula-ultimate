# แผนงาน 043: หลักฐาน Fracture Initiation

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_043_fracture-initiation-evidence-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

Implement และ validate deterministic fracture-initiation evaluator ที่แปลง explicit crack, nominal load, material toughness, thickness regime และ material state เป็น observable initiation event โดยไม่ถือ singular finite-element peak stress หรือ arbitrary element deletion เป็น physical proof

## ขอบเขตและข้ออ้าง

- ใช้ ideal infinite-plate center-crack LEFM fixture `K_I=sigma*sqrt(pi*a)` พร้อม declared half-crack length `a`, gross nominal stress และ `Y=1`
- บังคับ finite-width approximation-domain declaration, plane-strain thickness check `B>=2.5(K_IC/sigma_y)^2` และ small-scale-yielding check ก่อน admit ผล
- ใช้ synthetic toughness/material record พร้อมข้อห้ามใช้ใน design fitness; Work 042 ให้เพียง yield-state contract ไม่ใช่ toughness
- ประเมิน crack-length case, load level ที่คร่อม initiation, deterministic event localization, exact reaction/work ledger control และ representation-refinement invariance

งานนี้ validate เฉพาะ analytical LEFM initiation arithmetic และ evidence contract ไม่ validate crack-tip FEA, stable/unstable propagation, crack path, fracture-energy dissipation, real material toughness, crashworthiness หรือ element deletion

## การออกแบบการทดลอง

- ตัวแปรอิสระ: crack half-length, nominal tensile load, representation resolution, toughness, thickness regime และ declared geometry-factor domain
- ตัวแปรตาม: `K_I`, utilization, initiation load, event identity/load fraction, reaction residual, work residual, domain margin และ replay hash
- ตัวแปรควบคุม: geometry convention, gross stress area, `Y=1`, material state, load sequence, SI unit และไม่มี crack healing
- สมมติฐานที่ต้องการพิสูจน์: evaluator ให้ closed-form initiation load ภายใน `5%`, representation last-two change `<=5%`, ledger ปิด และ invalid-domain fixture ทุกตัว fail closed
- การพยายามหักล้าง: มี below/at/above initiation load, too-thin, excessive finite-width ratio, missing provenance, missing flaw และ yielding-before-fracture controls

## Implementation และไฟล์ที่วางแผน

- `config/structural/fracture_initiation_acceptance_v1.json`
- immutable fracture record, cracked-coupon grammar, domain validator, evaluator และ event contract
- Work 043 deterministic runner/launcher และ ignored evidence ใต้ `artifacts/work043/`
- focused analytical, identity, replay และ invalid-domain test
- bilingual report และ matching result records

## Validation และเกณฑ์สำเร็จ

- initiation-load error `<=5%` ใน admitted LEFM domain
- last-two representation change `<=5%` สำหรับ `K_I` ไม่ใช่ raw peak stress
- reaction residual `<=1e-5`, work-ledger residual `<=1e-4` และ deterministic first-crossing identity
- exact rejection สำหรับ missing crack/toughness/provenance/thickness regime และ material yield ที่เกิดก่อน claimed LEFM initiation
- focused/full test, compile/static check, staged-diff check, explicit commit และ clean-tree replay ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Infinite-plate fixture แคบโดยตั้งใจและจะ reject finite-width/nonlinear material state นอก preregistered domain CalculiX evidence ปัจจุบันยังไม่มี independently validated fracture contour-integral route จึงไม่อ้าง solver crack-tip field ไม่มี propagation, cohesive zone, XFEM, fatigue crack growth, physical coupon, vehicle component, push หรือ publication
