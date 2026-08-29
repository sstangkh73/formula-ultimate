# แผนงาน 029: Ten-Circuit Fixed-Topology Baseline Campaign

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_029_ten-circuit-baseline-campaign-plan.md`

## วัตถุประสงค์

รัน fixed-topology Level-0 reference family ที่ประกาศอย่างน้อยหนึ่งชุดบน circuit profile ที่มี version ครบสิบสนาม ภายใต้ energy, component opportunity, seed, evaluation budget, architecture และ holdout control เดียวกัน พร้อมแยก analytical proxy completion ออกจากหลักฐานฟิสิกส์สนามจริงอย่างชัดเจน

## ขอบเขต

- กำหนด baseline campaign protocol ที่เข้มงวดและมี fingerprint
- ตรึง reference vehicle family, component library, strategy, energy profile, timestep, step budget ต่อ run, design-evaluation opportunity, ชุด seed และ calibration/holdout split
- execute Work 028 whole-race orchestrator แปด stage สำหรับทุกคู่ circuit/seed
- ใช้ race distance และ lap length ทางการจาก profile แต่ประกาศ local corridor และ weather input เป็น analytical control ไม่ใช่ observation
- บันทึก outcome, time, distance, energy, residual, replay, evidence grade, width screen, compute use และ partition ต่อ run
- aggregate completion ระดับ circuit/family โดยไม่เลือกจากผล holdout
- พิสูจน์ protocol/catalog permutation invariance และปฏิเสธ control ที่ไม่เป็นธรรม, overlap, ไม่ครบ หรือถูกเปลี่ยน
- บันทึกและแก้ defect ทุกเรื่องที่พบใน problem report สองภาษาแยก

## ไฟล์ที่วางแผน

- `config/simulation/fixed_topology_baseline_protocol_v1.json`
- `src/formula_ultimate/simulation/baseline_campaign.py`
- `src/formula_ultimate/simulation/__init__.py`
- `src/formula_ultimate/simulation/step_inputs.py` หาก analytical-control evidence ต้องแก้ typed contract
- `tests/test_baseline_campaign.py`
- step-input regression test ที่เกี่ยวข้องหากจำเป็น
- `scripts/validate_baseline_campaign.py`
- `docs/simulation/TEN_CIRCUIT_BASELINE_CAMPAIGN.md`
- `docs/simulation/TEN_CIRCUIT_BASELINE_CAMPAIGN.th.md`
- problem report ของ Work 029 หากจำเป็น
- implementation queue, แผนนี้ และ result record สองภาษาที่เข้าคู่

## นิยามการทดลอง

- ตัวแปรอิสระ: circuit profile และ random seed ที่ประกาศ
- ตัวแปรตาม: finish status/time/distance, energy ที่ใช้, จำนวน attempted/committed step, residual pass count, replay fingerprint, width-screen status และ compute use
- ตัวควบคุม: architecture/model version, fixed topology, component library, strategy law, aerodynamic map, initial state/energy, timestep, maximum step, design-evaluation budget, analytical environment policy และ partition assignment
- เมตริก: completion สิบ profile, completion ทุก seed, finish residual, จำนวน residual fail, การอยู่ใน step budget ต่อ run, control identity equality, permutation invariance และ holdout isolation
- เกณฑ์สำเร็จ: run ทุก circuit/seed finish ภายใน common budget เดียว; residual ผ่านทั้งหมด; control ตรงกัน; ทุก profile อยู่ใน calibration/holdout partition exactly once; replay deterministic; proxy evidence ไม่ถูกเรียก real-circuit admission
- เกณฑ์ล้มเหลว: run ใดได้ energy/component/evaluation เพิ่ม, holdout เปลี่ยน protocol, profile ที่หายถูกตัดเงียบ, residual fail ถูกละเลย หรือ analytical control ถูกนำเสนอเป็น measured evidence
- การพยายามหักล้าง: partition ซ้ำ/overlap/ขาด, circuit ไม่รู้จัก, seed ศูนย์/ซ้ำ, component opportunity ถูกเปลี่ยน, step budget ไม่พอ, permute protocol/catalog และ evidence grade ถูกแก้

## การตรวจสอบ

1. focused test Work 023/028/029
2. test suite ทั้ง repository
3. standalone validator ของ Work 029
4. compile Python bytecode
5. `git diff --check` และ `git diff --cached --check`
6. ตรวจ staged scope แบบระบุไฟล์ก่อน commit

## เกณฑ์สำเร็จ

- fixed-topology family อย่างน้อยหนึ่งชุดจบระยะ profile ทั้งสิบสนามสำหรับ seed ที่ตรึงทั้งหมด
- ทุก run ใช้ opportunity และ compute/energy control ที่ประกาศเหมือนกัน
- holdout assignment เปลี่ยนไม่ได้และไม่ถูกใช้ tune reference
- result เก็บ provenance Work 028 ครบและ fingerprint deterministic
- analytical proxy result ไม่มีสิทธิ์ใช้เป็นคำกล่าวอ้างสนามจริงหรือ discovery
- เอกสารอังกฤษและไทยตรงกัน
- commit Work 029 เป็น validated commit หนึ่งรายการ

## ความเสี่ยง

- Work 023 รายงานว่าไม่มี profile ใดมี measured local spatial/weather evidence ครบ
- official race distance ที่ยาวอาจทำให้ campaign แพงหากไม่มี timestep/budget ที่มีเหตุผล
- คำศัพท์สถานะ weather ปัจจุบันอาจบังคับให้ synthetic control ถูกเรียก observation ผิด
- reference ที่ไม่มีแรงต้านหรือไม่ใช้ energy จะเป็น fairness baseline ที่อ่อน
- ผล seed ต่างอาจเหมือนกันได้เมื่อปิด stochastic hazard ทั้งหมด แต่ identity ยังต้องเก็บ seed

## สิ่งที่ไม่ทำโดยชัดแจ้ง

- ไม่อ้างว่า proxy completion ทำนาย lap time หรือ ranking ของรถจริง
- ไม่ทำ topology optimization หรือ autonomous candidate search
- ไม่ใช้ผล holdout เปลี่ยน baseline configuration
- ไม่ทำ higher-fidelity CFD, FEA, surveyed 3D corridor, calibrated reliability, safety หรือ physical validation
- ไม่ promote candidate เพราะ Work 030 เป็นเจ้าของ gate นี้
