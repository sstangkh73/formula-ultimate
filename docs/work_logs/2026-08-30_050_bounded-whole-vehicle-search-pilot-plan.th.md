# แผนงาน 050: Bounded Whole-Vehicle Search Pilot และ Readiness Review

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_050_bounded-whole-vehicle-search-pilot-plan.md`

## วัตถุประสงค์

ทดสอบว่า `GRID`, `RANDOM` และ `EVOLUTION` สามารถ propose, evaluate, fail, compare และ replay whole-vehicle candidate อย่างยุติธรรมผ่าน immutable bounded evaluator เดียวกัน รัน preregistered equal attempted-evaluation budget, promote candidate ที่เลือกไป frozen holdout, audit refined-evaluator availability และคืน `ready_for_bounded_main_campaign` หรือ `not_ready` โดยไม่ผ่อน gate

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม frozen pilot manifest ใต้ `config/experiments/` พร้อม candidate bound, seed สามค่า, `32` attempts ต่อ treatment/seed, immutable upstream identity, promotion rule และ readiness blocker
- Implement `DesignSearchAgentV0`, shared evaluator, treatment adapter, ancestry/RNG checkpoint, exact budget accounting, immutable ledger, holdout promotion, exploit control และ readiness decision ใต้ `src/formula_ultimate/experiments/`
- เพิ่ม acceptance runner, `scripts/run_work050.ps1`, focused test, pilot/readiness report สองภาษา และ result record สองภาษาที่ตรงกัน
- เขียน ignored ledger/summary ใต้ `artifacts/work050/`

## นิยามการทดลอง

- Treatment: `GRID`, `RANDOM` และ `EVOLUTION` ผ่าน evaluator API เดียวกัน
- ตัวแปรอิสระ: treatment, preregistered seed และ bounded Work 047 grammar variable สำหรับ core length/width, ground-contact radius, source primitive size และ propulsor primitive size Material density คงที่เพราะยังไม่มี density-strength law ที่ยอมรับ
- ตัวแปรตาม: grammar validity, mass/inertia-derived mass ratio, structural-capacity proxy, training feasibility, failure code, Level 0 time/energy objective, holdout survival, refined-evaluator status, wall time, attempted budget, ancestry และ replay hash
- ตัวควบคุม: `32` attempts ต่อ treatment/seed บน seed `101/202/303`; variable bound, load, evaluator, tolerance, component library, opportunity set และ failure accounting เหมือนกัน
- Falsification control: hidden evaluator/load/tolerance mutation, out-of-range/NaN variable, unknown variable, skipped failed attempt, changed seed และ ledger mutation

## การตรวจสอบ

1. Unit test treatment adapter ทั้งหมด, exact same-seed replay, candidate schema, budget accounting, ancestry และ fail-closed exploit control
2. รัน attempted evaluation exactly `288`; invalid/failed candidate ทุกตัวใช้หนึ่ง attempt
3. กำหนด equal attempted budget และ evaluator/opportunity identity เดียวกันทุก treatment
4. Promote preregistered best training-feasible candidate ไป Work 048 holdout
5. Readiness ต้องมี independent refined structural evaluator; หากไม่มีให้รายงาน promotion เป็น unverified และคืน `not_ready`
6. รัน repository-contract, full unit, compile, staged-diff และ clean-tree replay gate

## เกณฑ์สำเร็จ

- Same-seed rerunสร้าง candidate, failure, ancestry link, objective และ ledger fingerprint ซ้ำตรงกันทุกค่า
- ทุก treatment ใช้ budget เท่ากันรวม failure และแก้ evaluator input นอก candidate variable ไม่ได้
- Holdout result explicit สำหรับ selected candidate ทุกตัว; refined evaluation ที่ไม่มีห้ามสร้าง winner
- Readiness คืน allowed decision หนึ่งค่าพร้อม evidence-backed blocker

## ความเสี่ยง

ความสัมพันธ์ geometry-to-capacity เป็น declared Level 0 proxy ไม่ใช่ stress FEA Treatment อาจดูดีกว่าเพราะ bounded parameterization Material density ถูกห้ามเปลี่ยนโดยตั้งใจ เพราะการเปลี่ยน density โดยไม่มี strength evidence จะสร้าง exploit Equal attempts ไม่พิสูจน์ equal wall-clock opportunity ที่ higher fidelity ผลที่ถูกต้องอาจเป็น `not_ready` แม้ search mechanics ผ่าน

## สิ่งที่ไม่ทำโดยชัดแจ้ง

ไม่รวม main research campaign, superiority/novelty/discovery claim, arbitrary topology, whole-vehicle stress FEA, real-circuit result, physical validation, safety/manufacturing certification, push หรือ publication
