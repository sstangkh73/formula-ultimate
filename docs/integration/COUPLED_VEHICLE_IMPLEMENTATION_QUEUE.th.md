# คิว Implementation รถแบบ Coupled — Work 021–030

ต้นฉบับภาษาอังกฤษ: `COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md`

สถานะ: Completed — คิว implementation แบบ coupled Level 0

## กฎการทำงาน

ทำ Work ตามเลขอย่างเคร่งครัดและมี `In progress` ได้ทีละหนึ่งรายการ ทุกงานต้องมี
plan สองภาษาก่อนเปลี่ยนไฟล์, implementation/falsification evidence, result สอง
ภาษาหลัง validation, staged scope ชัดเจน, `git diff --cached --check` และ commit
ที่ยืนยันแล้วหนึ่งชุด ปัญหาสำคัญต้องมีรายงานสองภาษาแยกและแก้หรือกำหนดขอบเขตก่อน
complete

| Work | สถานะ | สิ่งส่งมอบ | Completion gate |
|---:|---|---|---|
| 021 | Completed | Unified experiment manifest, shared state แบบ topology-neutral, deterministic coupling architecture compiler, residual ledger และ event arbitration | Reference architecture compile/fingerprint ตรงกันเมื่อ permute; invalid dependency/state/residual/tie แสดงชัดเจน |
| 022 | Completed | Atomic coupled-step transaction และ adapter execution protocol | Adapter อ่าน immutable start state เดียว เขียนเฉพาะ output ที่ประกาศ และ commit next state ครบหนึ่งชุดหรือคืน invalidity โดยไม่มี partial mutation |
| 023 | Completed | Circuit, environment, weather, traffic และ strategy input adapter | Profile สิบสนามสร้าง typed step input deterministic; spatial/weather evidence ที่หายแสดงชัดและห้ามกลายเป็น neutral เงียบ |
| 024 | Completed | Coupling aerodynamic force/cooling เข้ากับ chassis force-moment และ normal load | Aero force/moment เปลี่ยน shared chassis/contact load พร้อม force/moment residual ปิด และ map query ที่ไม่รองรับทำให้ step invalid |
| 025 | Completed | Coupling tyre, suspension, mechanical braking และ regeneration ราย contact | Contact set จำนวนใดก็ได้แชร์ normal load, combined tyre capacity, travel, brake torque/heat และ central recovery request โดยไม่ redistribute เงียบ |
| 026 | Completed | Coupled longitudinal, lateral, yaw และ race-distance state integration | Motion state เดียว advance จากผลรวม contact/aero force/moment; analytical reference, timestep refinement และ corridor failure สังเกตได้ |
| 027 | Completed | Coupling central energy, thermal, cooling, degradation, damage และ reliability state | Typed transfer ปิดผ่าน independent audit; recovery, heat, derating, damage, seeded failure และ earliest event ตัด step เดียวกัน |
| 028 | Completed | Deterministic whole-race coupled orchestrator และ replay telemetry | Fixed-topology reference หนึ่งคัน execute coupled stage ทั้งหมดจน finish/depletion/failure/timeout/invalid พร้อม same-seed replay exact และ provenance ครบ |
| 029 | Completed | Ten-circuit fixed-topology baseline campaign และ fair compute control | Reference family ที่ป้องกันได้อย่างน้อยหนึ่งแบบจบสิบสนามภายใต้ pinned energy, component opportunity, evaluation budget, seed และ holdout policy |
| 030 | Completed | Integration falsification, numerical refinement, cross-model promotion gate และ release review | Coupling defect ที่จงใจใส่ต้อง fail; บันทึก convergence/uncertainty evidence; candidate ที่หลักฐานไม่พอ promote หรือเรียก discovered ไม่ได้ |

## เส้นทาง Dependency

```text
021 contracts and architecture
  -> 022 atomic adapter transactions
  -> 023 circuit/environment inputs
  -> 024 aero/chassis/load coupling
  -> 025 contact/suspension/brake coupling
  -> 026 shared vehicle motion
  -> 027 energy/thermal/health coupling
  -> 028 coupled whole-race orchestration
  -> 029 fair fixed-topology baselines
  -> 030 falsification and promotion gate
```

## นิยามเสร็จร่วมกัน

1. Signal/state field ทุกตัวมี identity, unit/meaning, producer, consumer, timing
   semantics และ invalid-state behavior ที่ประกาศ
2. Physics module แลก state ผ่าน versioned coupling contract เท่านั้น
3. Force, moment, energy, distance, thermal และ event residual ต้องสังเกตได้และไม่
   แก้เงียบ
4. Contact/component topology valid จำนวนใดก็ได้ยังเป็นไปได้; fixed topology
   อ้างอิงเป็น controlled integration treatment ไม่ใช่ design mandate
5. Input, version, architecture, artifact และ seed เดิม replay exact
6. Full repository test, work validator, compilation, whitespace, staged-scope
   และ commit check ผ่าน
7. Level-0 success เพียงอย่างเดียวไม่เป็น physical validation, safety,
   manufacturability, discovery หรือ real-race superiority

คิวนี้สร้าง central simulator ที่หายไปแบบ falsifiable ทีละขั้น ไม่อนุญาต autonomous
whole-vehicle evolution ก่อน Work 030 ปิด integrated reference และ promotion gate
