# Protocol ของ bounded whole-vehicle main campaign v1

ไฟล์ต้นฉบับภาษาอังกฤษ: `BOUNDED_WHOLE_VEHICLE_MAIN_CAMPAIGN_PROTOCOL.md`

Protocol ID: `bounded_whole_vehicle_main_campaign_v1`

Campaign ID: `FU-BMC-001`

สถานะ: `preregistered_not_run`

## จุดประสงค์และขอบเขตข้ออ้าง

protocol นี้ตรึงกติกาของ comparative main campaign แรก หลัง Work 054 ให้สถานะ `ready_for_bounded_whole_vehicle_campaign` คำถามวิจัยคือ proposal treatment ส่งผลต่อความสามารถระดับ seed ในการสร้าง finisher ที่มีหลักฐานรองรับหรือไม่ ภายใต้ attempted-evaluation opportunity เท่ากัน

ข้ออ้างที่รับได้คือหลักฐานเปรียบเทียบภายใน Work 047 assembly grammar, Work 048 load partition, Work 049 baseline, Work 053 linear-elastic beam/refined evaluator, วัสดุสังเคราะห์ และ Level 0 domain ปัจจุบันเท่านั้น ห้ามอ้าง physical validation, safety, manufacturability, real-race superiority, algorithm superiority จาก campaign เดียว, novelty, engineering discovery, arbitrary-topology transfer หรือ certified material allowable

## สมมติฐาน

Primary `H1_EVOLUTION_SUPPORTED_FINISHER_RATE`:

- preferred hypothesis: เมื่อ opportunity เท่ากัน `EVOLUTION` มี paired-seed probability ที่จะสร้าง refined-supported finisher อย่างน้อยหนึ่งแบบสูงกว่า `RANDOM`
- null: paired-seed rate difference `EVOLUTION - RANDOM` เท่ากับศูนย์
- falsification: observed rate difference ที่ไม่เป็นบวกขัดแย้งกับ preferred hypothesis ห้ามใช้ attempt-level feasible rate แทน seed-level endpoint นี้

คำถามรอง:

- บน seed ที่ทั้งสอง treatment สำเร็จ `EVOLUTION` ให้ seed-level best frozen-holdout time ต่ำกว่า `RANDOM` หรือไม่
- fixed discrete `GRID` calibration treatment มีพฤติกรรมเชิงพรรณนาอย่างไร โดยไม่ถือว่า GRID มี proposal distribution แบบเดียวกับ continuous treatments

## Treatment, seed และ opportunity budget

| กติกา | ค่าที่ตรึง |
|---|---:|
| Treatments | `GRID`, `RANDOM`, `EVOLUTION` |
| Paired main seeds | `55001` ถึง `55012` |
| Excluded pilot seeds | `101`, `202`, `303` |
| Excluded burn-in seed | `55999` |
| Attempts ต่อ treatment/seed | `80` |
| Attempts ต่อ treatment | `960` |
| Total attempted evaluations | `2,880` |
| Promotions ต่อ treatment/seed | สูงสุด `2` |
| Total promotion cap | `72` |

invalid declaration, invalid geometry, numerical failure, structural/energy failure, exploit rejection, holdout failure, refined disagreement หรือ DNF ทุกกรณีใช้หนึ่ง opportunity ห้าม retry/replace failed attempt, ใส่ neutral numeric score หรือยืม budget ข้าม seed

candidate bounds ห้าค่ายังคงตรงกับ Work 050 GRID มีสี่ระดับในห้าตัวแปร จึงมี capacity `4^5=1,024` โดย GRID opportunities ที่วางแผน `12 x 80=960` รายการไม่ซ้ำ ห้าม wrap หรือ repeat

`EVOLUTION` ใช้ initial random 20 attempts ต่อ seed, mutation sigma `0.12` ของ declared range และเลือก best training-feasible candidate เป็น parent โดย fallback เป็น best observed record ต้องบันทึก bound clamping ส่วน `RANDOM` sample แต่ละตัวแปรอย่างอิสระและ uniform ภายใน bounds เดียวกัน

## ลำดับการประเมินที่ตรึง

```text
declaration and identity
  -> candidate proposal
  -> grammar/geometry and training Level 0
  -> seed-level training selection
  -> frozen holdout Level 0
  -> Work 053 refined stress/deformation
  -> finalist 3D -> STEP -> FreeCAD witness
  -> eligibility and analysis
```

ข้อมูล holdout ห้ามไปถึง parent selection, training ranking, mutation หรือ retry decision เลือก training-feasible candidates สูงสุดสองแบบต่อ treatment/seed ด้วย minimum training finish time แล้ว tie-break ด้วย candidate ID หากมีเพียงศูนย์หรือหนึ่งแบบต้องบันทึก shortfall โดยไม่ replace หรือยืมข้าม seed

candidate มีสิทธิ์เป็น winner เมื่อผ่าน frozen holdout ทั้งสอง, Work 053 refined evaluator เดิม, provenance/exploit checks และ final STEP/FreeCAD witness โดยไม่มี hidden geometry repair เท่านั้น Refined thresholds เปลี่ยนไม่ได้ระหว่าง campaign

## Outcome และการวิเคราะห์

paired seed คือ inferential unit Attempts 80 ครั้งภายใน seed เป็น dependent search opportunities ไม่ใช่ independent replicates 80 ชุด

Primary outcomes ต่อ treatment/seed:

1. มี refined-supported finisher อย่างน้อยหนึ่งแบบหรือไม่
2. best frozen-holdout time ใน eligible finishers

เมื่อไม่มี supported finisher ให้ presence เป็น `false` และ best time เป็น `null` โดย seed ยังอยู่ใน supported-finisher-rate analysis และการไม่มีเวลาต้องรายงานชัดเจน

primary comparison คือ `EVOLUTION - RANDOM` protocol กำหนด paired rate difference, exact McNemar analysis และ 95% paired-bootstrap interval สำหรับ common-success best time ใช้ paired median difference, exact sign-flip analysis และ 95% paired-bootstrap interval Analysis RNG seed คือ `551337` ต้องรายงาน GRID comparisons และ secondary metric ที่ preregister ทุกตัวโดยไม่เลือกเฉพาะผลที่ชอบ

ลำดับเลือก candidate winner:

1. eligibility gates ทุกตัวผ่าน
2. frozen-holdout time ต่ำสุด
3. tie-break ด้วย candidate ID จากน้อยไปมาก

แม้ primary effect เป็นบวกก็ยังอ้าง algorithm superiority ไม่ได้จนมี independent replication ภายใต้ protocol ใหม่

## Stop/go และ immutability

หยุดก่อน admitted run หาก upstream/protocol identity ต่าง, GRID ซ้ำ, treatment opportunities ไม่เท่ากัน, holdout รั่วสู่ training, Work 053 unavailable หรือ ledger/replay ไม่ exact การเปลี่ยนหลัง burn-in ต้องใช้ protocol ID ใหม่ การเปลี่ยนหลัง admitted start ต้องใช้ campaign ID ใหม่ Result/budget ledger เป็น append-only และต้องเก็บ RNG checkpoint กับ ancestry

final statuses ที่อนุญาต:

- `completed_with_supported_finishers`
- `completed_without_supported_finisher`
- `stopped_protocol_violation`
- `stopped_infrastructure_failure`

การจบโดยไม่มี supported finisher เป็นผลวิจัยที่ถูกต้อง ไม่ใช่สิทธิ์ผ่อน gate

## สถานะ validation ปัจจุบัน

Work 055 validate เฉพาะ declaration และประเมิน candidate `0` ครั้ง Machine-readable source คือ `config/experiments/bounded_whole_vehicle_main_campaign_v1.json`; ignored validation evidence เขียนที่ `artifacts/work055/protocol_validation.json` ส่วน campaign runner และ burn-in เป็น work item ถัดไป
