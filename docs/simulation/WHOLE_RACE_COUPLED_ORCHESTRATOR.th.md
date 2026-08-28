# Whole-Race Coupled Orchestrator

สถานะ: reference implementation ของ Work 028

ไฟล์ต้นฉบับภาษาอังกฤษ: `WHOLE_RACE_COUPLED_ORCHESTRATOR.md`

## จุดประสงค์

Work 028 สร้าง loop ที่ยังขาดรอบ atomic coupled-step transaction โดย execute configuration รถ Level 0 ที่ประกาศไว้จนถึง terminal race outcome และเก็บ identity กับ numerical evidence เพียงพอสำหรับ replay หรือปฏิเสธ run

ระบบนี้เป็น integration และ selection gate ไม่ใช่ real-circuit simulator ที่ calibrate แล้วหรือ physical validation

## Architecture v4

`config/simulation/coupled_level0_architecture_v4.json` ประกาศ stage ตามลำดับแปดส่วน:

1. `input_bridge`
2. `aerodynamic_map`
3. `normal_load_solver`
4. `contact_limit_solver`
5. `vehicle_motion_solver`
6. `energy_graph_audit`
7. `health_event_solver`
8. `race_progress_solver`

การเปลี่ยน v4 route `state.current` เข้า race-progress stage และ version stage นี้เป็น `work028-race-progress-v1` ส่วน architecture รุ่นก่อนยังไม่เปลี่ยนเพื่อรักษา replay compatibility

ลำดับ registration ของ adapter ไม่ได้กำหนดลำดับ execute แต่ compiled architecture เป็นผู้กำหนด

## Race Loop

ใน attempted step แต่ละครั้ง `run_whole_race` จะ:

1. ปฏิเสธ initial state ที่ terminal อยู่แล้ว
2. จำกัด requested duration ด้วย race timeout ที่เหลือ
3. resolve circuit, spatial, weather, traffic, state และ strategy input แบบ typed
4. สร้าง adapter ที่ขึ้นกับ duration จาก committed state
5. execute atomic transaction หนึ่งครั้ง
6. บันทึก trace, residual, event, published signal, fingerprint และ identity ของ start/end state
7. advance เฉพาะเมื่อ transaction commit
8. หยุดเมื่อ finish, depletion, physical failure, timeout, invalidity หรือ evaluation budget หมด

transaction ที่ invalid ยังเก็บ attempted telemetry แต่ไม่มี end-state fingerprint และไม่สามารถ advance committed race state บางส่วนได้

## Race-Progress Merge

race-progress adapter อ่าน current, motion, energy และ health candidate พร้อม upstream residual evidence จากนั้นเพิ่ม candidate สำหรับ finish, timeout และ step-complete แล้วใช้ deterministic event arbitrator ร่วม

candidate ที่ commit ถูก localize ตามเวลา event ที่ชนะ ระยะ finish ถูกตั้งให้ตรง target ที่ประกาศแบบ exact สถานะ terminal เป็นหนึ่งใน:

- `finished`
- `depleted`
- `failed`
- `timeout`
- `invalid`

event ที่เวลาเสมอกัน exact ยังคงมองเห็นใน event ledger โดย common event priority ตัดสินสถานะที่ commit ดังนั้น finish/depletion tie จะเก็บทั้งสอง event พร้อม commit winner ที่ประกาศอย่างสอดคล้อง

## หลักฐานที่สังเกตได้

record `CoupledRaceStepTelemetry` แต่ละรายการมี:

- step index และ requested duration
- transaction status และรายละเอียด failure
- scenario/input fingerprint
- identity SHA-256 ของ start state และ end state หากมี
- ขอบเขต time, distance และ primary energy
- published signal ID
- adapter trace ทั้งหมด
- residual entry ที่แต่ละ adapter เป็นเจ้าของ
- terminal/event candidate ที่ transaction publish

`CoupledRaceReplayMetadata` ตรึง architecture fingerprint, ordered model version, seed, evaluation budget, timestep, initial/final state, scenario fingerprint และจำนวน attempted/committed step ส่วน `WholeRaceResult` มี fingerprint ครอบ outcome, final state, telemetry และ replay metadata อีกชั้น

residual identity มีเจ้าของแต่เพียงผู้เดียว energy adapter publish `energy.*`; health adapter อาจเก็บ truncated energy evidence ภายในแต่ publish เฉพาะ `health.*`; race progress publish `race.*`

## Analytical Reference และการพยายามหักล้าง

controlled reference ใช้รถ fixed four-contact, aerodynamic coefficient ศูนย์, straight analytical corridor, การเคลื่อนที่เริ่มต้นคงที่ `10 m/s`, ไม่มี drive/brake request และ target `30 m` โดย finish ใน committed step หนึ่งวินาทีสามครั้งพร้อม finish-distance residual ศูนย์

falsification matrix มี:

- primary energy ต่ำร่วมกับ auxiliary draw ซึ่ง localize depletion ที่ `0.5 s`
- central heat สูงเกิน ซึ่ง localize failure ที่ `0.2 s`
- timeout ภายใน step ที่ `1.5 s`
- corridor invalidity โดยไม่มี committed next state
- adapter coverage ไม่ครบและ transaction rollback
- evaluation budget หมด
- exact finish/depletion tie
- registration ของ adapter แบบกลับลำดับและ same-seed replay

## Invariant

- มีเพียง `state.next` จาก transaction ครบถ้วนที่สำเร็จเท่านั้นที่ advance race
- terminal state ไม่ถูก step ต่อ
- scenario race distance ต้องตรงกับ race distance ของ shared start state ภายใน `1e-9 m`
- energy depletion ที่ปลาย requested step แบบ exact ยังคงเป็น event ที่สังเกตได้
- residual ID ไม่ซ้ำภายใน transaction เดียว
- input, version, seed และ architecture เดิม replay exact
- การ permute registration เปลี่ยนผล compiled execution ไม่ได้

## ข้อจำกัดและขอบเขตคำกล่าวอ้าง

reference นี้เป็น analytical โดยตั้งใจ ยังไม่ execute spatial/weather evidence ที่วัดจริงครบสิบ real circuit profile, optimize strategy, calibrate tyre/aero/thermal/reliability model, model full 3D contact, พิสูจน์ numerical convergence หรือเปรียบเทียบ topology-search candidate อย่างเป็นธรรม ช่องว่างเหล่านี้ทำให้ยังอ้าง real-race pace, safety, manufacturability, discovered technology หรือ physical validity ไม่ได้

Work 029 ต้องสร้าง controlled ten-circuit baseline campaign ส่วน Work 030 ต้องทำ integrated falsification, refinement, uncertainty review และ cross-model promotion ก่อน autonomous candidate จะผ่านพ้น Level-0 gate นี้ได้
