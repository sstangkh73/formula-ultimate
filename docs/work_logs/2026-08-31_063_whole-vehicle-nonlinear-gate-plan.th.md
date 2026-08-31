# แผนงาน 063: Whole-Vehicle Geometric-Nonlinearity Gate

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_063_whole-vehicle-nonlinear-gate-plan.md`

## วัตถุประสงค์

สร้างและ validate reusable adapter ที่ใช้เชื่อมหลักฐาน finalist แบบ linear-beam จาก Work 062 ไปยัง candidate-derived geometric-nonlinearity check ที่เข้มขึ้น โดย freeze inputs, outputs, thresholds และ replay contract ก่อนทดสอบ Work 062 finalist ใด ๆ การรัน candidates จะเป็น successor work item แยกต่างหากโดยใช้ adapter ที่ commit แล้ว

## แบบการทดลอง

- Independent variable ในการใช้ภายหลัง: geometry ของ Work 062 finalist; จะไม่แก้หรือ optimize geometry
- Dependent variables: nonlinear solver convergence, maximum displacement และ surface von Mises stress, nonlinear-to-linear displacement/stress amplification และ nonlinear yield margin สำหรับ frozen holdout load cases ทั้งสองกรณี
- Controls: exact Work 062 candidate declaration, Work 048 holdout loads, Work 053 synthetic material, fine mesh subdivision `16`, boundary conditions เดียวกัน, CalculiX executable identity และ frozen threshold configuration หนึ่งชุด
- Falsification: candidate ไม่ผ่านหาก required process ขาด/มี nonzero exit, ไม่มี geometric-nonlinearity confirmation, output invalid, displacement amplification เกิน `1.10`, stress amplificationเกิน `1.15` หรือ nonlinear yield marginต่ำกว่า `1.10`
- Future selection contract: รวม all and only Work 062 CAD-witness-passed candidates; outcome ห้ามเปลี่ยน inclusion set

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม `config/structural/whole_vehicle_nonlinear_gate_v1.json`
- เพิ่ม reusable fail-closed nonlinear gate module ใต้ `src/formula_ultimate/structural/` และ export
- ขยาย B31 deck builder โดยไม่เปลี่ยน default linear output
- เพิ่ม unit/integration tests สำหรับ deck identity, threshold boundaries, missing evidence, non-finite evidence, solver confirmation และ deterministic aggregation
- เพิ่ม bilingual gate-contract และ result documentation

## Validation และเกณฑ์สำเร็จ

ต้องมี frozen versioned configuration, default linear deck output ไม่เปลี่ยน, deterministic fail-closed adjudication/fingerprinting, focused/full tests ผ่าน, compilation ผ่าน, เอกสารสองภาษา และ scoped commit Successor execution work ต้องใช้ committed implementation นี้และตรวจ exact inclusion, terminal records และ replay อย่างอิสระ

## ความเสี่ยงและสิ่งที่ไม่ทำ

ความเสี่ยงคือ CalculiX nonlinear convergence, parser ambiguity ข้าม increments, การพึ่ง beam idealization และ low-load responses อาจเล็กเกินกว่าจะเผย instability งานนี้ยังไม่รัน Work 062 finalists; ต้องทำใน post-commit work item แยก และไม่เพิ่ม initial imperfections, contact, solid elements, material plasticity, fracture, fatigue spectra, crash propagation, calibrated material data, manufacturing tolerances, hardware validation, independent replication หรือ physical-safety claim นี่คือ geometric-nonlinearity sensitivity gate ไม่ใช่ buckling certificate หรือ physical validation
