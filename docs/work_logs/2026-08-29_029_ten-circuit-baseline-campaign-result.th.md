# ผลงาน 029: Ten-Circuit Fixed-Topology Baseline Campaign

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_029_ten-circuit-baseline-campaign-result.md`

## ผลลัพธ์

สร้างและ execute fixed-topology Level-0 baseline campaign แบบเข้มงวดบนระยะ circuit profile ที่มี version ครบสิบสนาม Reference family ที่ใช้ energy หนึ่งชุดจบ circuit/seed run `30/30` ภายใต้ architecture, component opportunity, energy profile, timestep, run budget, design-evaluation budget, ชุด seed และ calibration/holdout split เดียวกันแบบ immutable

ทุก result ยังคงเป็น `profile-distance-analytical-proxy` พร้อม `real_circuit_admitted = false` เพราะยังไม่มี measured local corridor และ event-time weather evidence

## ไฟล์ที่เปลี่ยน

- เพิ่ม `config/simulation/fixed_topology_baseline_protocol_v1.json`
- เพิ่ม `src/formula_ultimate/simulation/baseline_campaign.py` และ public export
- เพิ่ม focused campaign test สิบรายการและ `scripts/validate_baseline_campaign.py`
- เพิ่ม weather แบบ typed `synthetic_control` ผ่าน step input/aerodynamic adapter, test, validator และเอกสารสองภาษาที่เกี่ยวข้อง
- เพิ่ม model record baseline campaign สองภาษา, plan/result คู่นี้, problem report สองภาษาสามเรื่อง และอัปเดต implementation queue

## ปัญหาที่แก้

1. Weather evidence แทน synthetic analytical control ไม่ได้โดยไม่ติดป้ายผิดเป็น observed
2. baseline contact state รอบแรกใส่ `300 K` ลง `suspension_travel_m` จาก positional construction ทำให้ทุก run fail-closed
3. aggregate รอบแรกเผยจำนวนคู่ family-profile เป็น profile count ซึ่งจะนับเกินใน campaign หลาย family

## การตัดสินใจ

- ใช้ aerodynamic drag ไม่เป็นศูนย์และ propulsion ที่ balance แทน frictionless zero-energy coast
- ตรึง primary energy `50,000,000 J`, drive efficiency `0.9`, reference area `1.5 m^2`, drag coefficient `0.5` และ maximum drive force `1000 N`
- ตรึง timestep `1000 s`, timeout `40000 s`, สูงสุด `64` step/run, design-evaluation budget `1` และ seed `(17, 29, 43)`
- ตรึง calibration เจ็ด profile และ holdout สาม profile ก่อน execute
- ถือ actual step count เป็น compute ที่ใช้ พร้อมรักษา maximum opportunity เท่ากัน
- เก็บ static width ที่ยังไม่รู้เป็น `indeterminate` และไม่เรียกผ่าน
- ปฏิเสธ hidden protocol field, implicit budget coercion, partition mismatch, evidence-grade escalation และ real-circuit admission

## ผลการทดลองและการพยายามหักล้าง

- ตัวแปรอิสระ: circuit profile สิบชุดและ seed สามชุด
- หลักฐานตัวแปรตาม: outcome, time, distance, primary energy, step, residual, replay identity, width status และ partition
- ตัวควบคุม: architecture v4, four-contact family หนึ่งชุด, component library, steady-drag strategy, energy, synthetic environment, timestep, budget และ holdout assignment
- ผล: run `30/30` finish; profile สิบชุดจบ; residual ผ่านทั้งหมด; ไม่มี run เกิน `31/64` step
- energy ที่ใช้ตั้งแต่ `12.676688 MJ` ที่ Monaco ถึง `15.012090 MJ` ที่ Bahrain
- metric ของ circuit เดียวกันเท่ากันข้าม seed ขณะที่ replay identity ยังแยกตาม seed
- การหักล้างปฏิเสธ partition overlap/ไม่ครบ, hidden field, ค่า float ใน integer budget, evidence escalation และ opportunity ที่ถูกเปลี่ยน Budget หนึ่ง step ให้ timeout ที่สังเกตได้โดยไม่ขยาย และ catalog permutation replay exact
- หลักฐานขัดแย้ง: ไม่พบสำหรับ software/fairness contract ที่ประกาศ
- คำอธิบายทางเลือก: completion มาจาก straight synthetic path และ environment คงที่ ไม่ใช่ physical circuit layout
- หลักฐานที่ขาด: surveyed local geometry, observed event weather, braking/cornering/traffic, calibrated model, uncertainty และ higher fidelity
- ความมั่นใจ: สูงต่อ deterministic campaign control/execution; ต่ำต่อ real-circuit performance ซึ่งถูกระบุว่าไม่ผ่าน admission

## คำสั่งและหลักฐาน validation

คำสั่งทั้งหมดคืน exit status `0`:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_step_inputs tests.test_aero_load_coupling tests.test_whole_race tests.test_baseline_campaign -v
python -m unittest discover -s tests
python scripts/validate_step_inputs.py
python scripts/validate_aero_load_coupling.py
python scripts/validate_whole_race.py
python scripts/validate_baseline_campaign.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

- focused regression Work 023/024/028/029: ผ่าน 39 รายการใน `12.748 s`
- test suite ทั้ง repository: ผ่าน 252 รายการใน `14.879 s`
- completed run/profile: `30/30`, `10/10`
- architecture fingerprint: `abf3148cfba2063f8fdba23951239b2b0a4a899c391503d3e46db69fd203618d`
- protocol fingerprint: `4c1c93a21c8ada5d8859eebbce1adb11f750787b2f522ba671f30be08ea6f2a6`
- controls fingerprint: `9c6a168a90a1e8d7cf33f72f3410e8d193cfd4edffddf7a136c84a1bed0371c9`
- result fingerprint: `44dc7f85fac097b8ecbb38c04ff14a595702e8e4a0b9134ba70403fc451bfa98`
- real-circuit admission: `false` สำหรับ campaign และทุก run

## ข้อจำกัด

campaign เป็น Level-0 profile-distance analytical proxy ไม่ได้วิ่งบน physical circuit geometry, reproduce lap time, optimize reference หรือ validate safety/manufacturability การใช้ dry weather คงที่, straight corridor, steady speed, traffic ศูนย์, ไม่มี rolling resistance และ component/aero assumption ที่ไม่ calibrate จำกัดการตีความ

## งานต่อเนื่อง

Work 030 ต้องปิด deliberate integration-defect falsification, numerical refinement, uncertainty/claim review และ cross-model promotion/release gate โดย candidate ที่หลักฐานไม่พอต้องไม่ถูก promote
