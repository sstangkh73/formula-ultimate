# แผนงาน 028: whole-race coupled orchestrator

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_028_whole-race-coupled-orchestrator-plan.md`

## วัตถุประสงค์

รัน fixed-topology reference vehicle หนึ่งคันผ่าน coupled stage ทุกส่วนด้วย transaction แบบ deterministic จน finish, depletion, physical failure, timeout หรือ invalidity พร้อม same-seed replay แบบ exact และ provenance telemetry ครบทุก step

## ขอบเขต

- สร้าง adapter `race_progress_solver` ที่ merge motion, energy และ health candidate เป็น `state.next` หนึ่งชุด exact
- version architecture สำหรับ race-progress adapter ของ Work 028 หากจำเป็น
- สร้าง fixed-topology reference fixture จาก adapter Work 023-027
- รัน atomic `execute_coupled_step` transaction ซ้ำ
- สร้าง adapter ที่ขึ้นกับ duration ใหม่จาก committed state ทุก step
- หยุดเมื่อ finish, depletion, thermal/degradation/damage/reliability/contact failure, timeout หรือ transaction invalid
- บันทึก architecture, model version, seed, scenario/input fingerprint, start/end state, signal, residual, event, trace และ terminal reason
- พิสูจน์ registration-order invariance และ same-seed replay exact
- เพิ่ม failure fixture สำหรับ depletion, failure, timeout, invalid input และ provenance ไม่ครบ
- บันทึกและแก้ทุก defect ที่พบในรายงานปัญหาสองภาษาแยก

## ไฟล์ที่วางแผน

- `src/formula_ultimate/simulation/whole_race.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_whole_race.py`
- `scripts/validate_whole_race.py`
- `config/simulation/coupled_level0_architecture_v4.json` หากจำเป็น
- `docs/simulation/WHOLE_RACE_COUPLED_ORCHESTRATOR.md`
- `docs/simulation/WHOLE_RACE_COUPLED_ORCHESTRATOR.th.md`
- problem report ของ Work 028 หากจำเป็น
- implementation queue, แผนนี้ และบันทึกผลสองภาษาที่เข้าคู่

## นิยามการทดลอง

- ตัวแปรอิสระ: fixed vehicle/scenario configuration, strategy command, timestep, energy เริ่มต้น, thermal/reliability parameter, timeout, seed และลำดับ adapter registration
- ตัวแปรตาม: outcome, final state/time/distance/energy/health, step count, event winner, telemetry fingerprint, residual ledger และ replay metadata
- ตัวควบคุม: architecture fingerprint, model version, component/contact topology, spatial/weather evidence, evaluation budget และ initial state แบบ exact
- เมตริก: finish-distance residual, energy residual, จำนวน residual ที่ fail, rollback correctness, replay equality, provenance completeness และ terminal localization
- เกณฑ์สำเร็จ: reference ถึง terminal outcome ที่ตั้งใจ; input/seed เดิม replay exact; กลับลำดับ registration แล้วผลตรง; terminal failure ที่ประกาศทุกชนิดสังเกตได้; invalidity ไม่ publish state; telemetry มี provenance ครบทุก committed step
- เกณฑ์ล้มเหลว: terminal state ยังเดินต่อ; transaction fail แต่ commit บางส่วน; telemetry ขาด model/input/seed/state identity; same-seed ต่างกัน; หรือ priority finish/depletion/failure/timeout ไม่สอดคล้อง
- การพยายามหักล้าง: energy ต่ำ, heat/hazard สูง, progress ศูนย์, corridor invalid, evaluation budget หมด, exact finish tie และ adapter-order permutation

## การตรวจสอบ

1. test เฉพาะ Work 028
2. test suite ทั้ง repository
3. validator แยกของ Work 028
4. compile Python bytecode
5. `git diff --check` และ `git diff --cached --check`
6. ตรวจ staged scope แบบระบุไฟล์ก่อน commit

## เกณฑ์สำเร็จ

- architecture ทั้งแปด stage execute ผ่าน atomic transaction boundary
- fixed-topology reference หนึ่งคันจบ analytical race fixture แบบ deterministic
- มี test สำหรับ finish, depletion, failure, timeout และ invalid
- same-seed และ registration-order replay ตรง exact
- เก็บ provenance และ residual/event evidence ครบต่อ step
- เอกสารอังกฤษและไทยตรงกัน
- commit Work 028 เป็น validated commit หนึ่งรายการ

## ความเสี่ยง

- race-progress stage ปัจจุบันอาจยังไม่มี adapter/version contract ของ Work 028
- ไม่มี spatial/weather evidence ครบสำหรับสนามจริง จึงต้องรักษา reference เป็น analytical fixture
- ขอบเขต aerodynamic map และ corridor width อาจหยุด long run ก่อน gate ที่ตั้งใจ
- terminal event ภายใน prospective step ต้อง merge state และ finish priority ให้สอดคล้อง
- telemetry อาจใหญ่ จึงต้องจำกัด validation fixture

## สิ่งที่ไม่ทำโดยชัดแจ้ง

- ไม่ทำ ten-circuit baseline campaign หรือผล compute fairness ของ Work 029
- ไม่ทำ integration-falsification release gate ของ Work 030
- ไม่อ้างว่า analytical fixture ทำนายการแข่งขัน Formula 1 จริง
- ไม่ทำ CAD optimization, topology search, CFD หรือ physical validation
