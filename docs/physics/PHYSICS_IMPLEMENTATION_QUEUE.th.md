# คิว Implementation ฟิสิกส์ — Work 010–019

ไฟล์ต้นฉบับภาษาอังกฤษ: `PHYSICS_IMPLEMENTATION_QUEUE.md`

สถานะ: คิวเรียงลำดับเสร็จสมบูรณ์

## กฎการทำงาน

Work item ต้องทำตามหมายเลขอย่างเคร่งครัด และมีได้เพียงหนึ่งงานที่เป็น
`In progress` แต่ละงานต้องมี plan สองภาษา, implementation, validation, result
report เต็มสองภาษา และ commit ที่ตรวจแล้ว หากพบปัญหาที่มีสาระ ต้องสร้างรายงาน
แยกสองภาษาใต้ `docs/problem_reports/` แก้หรือกำหนดขอบเขตปัญหาให้ชัด รัน
validation ใหม่ แล้วจึง complete และ commit งาน ห้ามเริ่มข้อถัดไปก่อนตรวจ commit
ของข้อก่อนหน้า

| Work | สถานะ | สิ่งส่งมอบ | Gate การเสร็จงาน |
|---:|---|---|---|
| 010 | Completed | 3D circuit corridor แบบมี version และ whole-vehicle swept-envelope admission | ปฏิเสธกรณี static-fit/swept-fail และ steering-fail; real geometry ที่หลักฐานไม่พอยังคง indeterminate |
| 011 | Completed | ขอบเขตแรง tyre-road longitudinal/lateral และ saturation | ทดสอบ friction circle/ellipse analytical; เห็นทั้ง requested และ saturated force |
| 012 | Completed | Typed energy และ powertrain component graph | Port ของ source, converter, transmission และ tyre compile deterministic พร้อม contract SI/sign |
| 013 | Completed | Independent energy-conservation audit | Chain lossless/lossy ปิด balance ใน scaled tolerance; hidden หรือ double-counted energy ทำให้ run invalid |
| 014 | Completed | Lumped thermal, cooling, derating และ failure physics | Reference heating/cooldown ผ่าน; ห้าม clip อุณหภูมิเงียบ ๆ |
| 015 | Completed | Deterministic full-race completion loop | ผล finish, depletion, timeout, invalidity และ failure replay เหมือนกันข้าม circuit profile |
| 016 | Completed | Lateral/yaw dynamics, load transfer และ combined tyre force | กรณี steady-state/transient อ้างอิง converge และรักษา balance ที่ประกาศ |
| 017 | Completed | Aerodynamic force, balance และ cooling-flow model | Map drag/downforce/moment validate ข้าม speed, ride height, yaw และ active-state envelope |
| 018 | Completed | Suspension, mechanical braking และ regenerative braking | Wheel load, travel, brake energy, regen limit และ failure event ถูกคิดทางฟิสิกส์ |
| 019 | Completed | Reliability, traffic, weather, degradation และ race strategy | Digital race หลายรอบ/หลาย event จบด้วย strategy control deterministic และ failure พร้อม uncertainty |

## นิยามเสร็จร่วมกัน

ทุกข้อต้องผ่านทั้งหมดต่อไปนี้:

1. ประกาศสมมติฐาน SI, model boundary, independent/dependent variable, control,
   success criteria และ failure criteria ก่อน implementation
2. กฎฟิสิกส์ทุกข้อที่ implement มี test แบบ analytical หรือตรวจอิสระได้
3. Numerical invalidity, conservation residual, saturation, depletion,
   derating และ missing evidence ต้องสังเกตได้
4. พยายามหักล้างสมมติฐานที่ต้องการด้วย reference case อย่างน้อยหนึ่งกรณี
5. Markdown ภาษาอังกฤษและไทยตรงกัน
6. Full repository test, validator เฉพาะงาน, compilation และ whitespace check
   ผ่าน
7. Explicit staged scope และ `git diff --cached --check` ผ่าน
8. มี local commit หนึ่งรายการที่ตรวจแล้วและรายงาน hash ใน final handoff การ
   push remote อยู่นอกคิวนี้หากไม่ได้สั่งแยก

## เส้นทาง Dependency

```text
010 circuit corridor
  -> 011 tyre/contact
  -> 012 energy graph
  -> 013 conservation audit
  -> 014 thermal/cooling
  -> 015 race loop
  -> 016 lateral/yaw/load transfer
  -> 017 aerodynamics
  -> 018 suspension/braking/regen
  -> 019 digital race reliability and strategy
```

คิวนี้เป็นแผนหลักฐานแบบแบ่งขั้น ไม่ใช่คำอ้างว่าฟิสิกส์ที่ Queued มีอยู่แล้ว
ความสำเร็จ Level 0 หรือ reduced-order เพียงอย่างเดียวไม่ยืนยัน physical
validation, safety, manufacturability หรือความเหนือกว่าในโลกจริง
