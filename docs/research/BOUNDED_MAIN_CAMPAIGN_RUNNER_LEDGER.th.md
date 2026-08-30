# สัญญา Bounded Main Campaign Runner และ Ledger

ไฟล์ต้นฉบับภาษาอังกฤษ: `BOUNDED_MAIN_CAMPAIGN_RUNNER_LEDGER.md`

สถานะ: implement และตรวจแบบ preparation แล้ว แต่ campaign execution ยังถูกล็อก

## วัตถุประสงค์และขอบเขตหลักฐาน

ส่วนนี้ทำให้งบ opportunity ที่ freeze ไว้ของ `FU-BMC-001` เป็น deterministic, append-only และ recover ได้ แต่ไม่ได้ทำให้ผล Level-0 valid ทางฟิสิกส์ และไม่ได้อนุญาตให้รัน burn-in หรือ admitted main seed Synthetic evaluations ใน unit tests เป็นเพียง software fixtures และใช้เป็น campaign observations ไม่ได้

## ลำดับ transaction

ในแต่ละ treatment/seed stream runner ทำ logical transaction ที่ย้อนการใช้งบไม่ได้ดังนี้:

1. reconstruct search agent จาก reservations และ terminal training results ก่อนหน้าทั้งหมด
2. propose candidate ถัดไปและ RNG checkpoint ที่ exact
3. append และ `fsync` `attempt_reserved` หนึ่ง row เพื่อ consume หนึ่ง opportunity
4. เรียก evaluator
5. append และ `fsync` `training_result` หนึ่ง rowเท่านั้น
6. ส่ง terminal result นั้นกลับเข้า reconstructed agent

ถ้า process สะดุดระหว่างขั้น 3 ถึง 5 จะเหลือ pending reservation ที่มองเห็นได้หนึ่งรายการ เมื่อ resume ต้องสร้าง candidate, ancestry และ RNG checkpoint เดิมให้ตรงกัน ประเมิน reservation นั้นเพียงครั้งเดียว และห้าม reserve opportunity ใหม่ก่อน Reserved attempt ถือว่าใช้ไปแล้วแม้ evaluator จะคืน failure state ภายหลัง

## ความสมบูรณ์ของ ledger

Budget และ result ledgers ใช้ canonical JSONL schema `chained_campaign_jsonl_v1` แต่ละ row มี protocol ID, campaign ID, evidence class, ledger kind, zero-based sequence, SHA-256 ของ row ก่อนหน้า, payload และ SHA-256 ของตัวเอง previous hash ของ row แรกคือเลขศูนย์ 64 ตัว

Record hash คือ:

```text
record_sha256 = SHA256(canonical_json(row_without_record_sha256))
```

Replay ต้อง fail closed เมื่อพบ malformed/blank row, sequence gap, previous-hash mismatch, record mutation, cross-ledger identity mismatch, reservation/result ซ้ำ, result ที่ไม่ reserve, attempt สลับลำดับ, pending มากกว่าหนึ่งรายการใน stream, candidate identity mismatch, evaluation identity mismatch หรือ numeric evidence ที่ไม่ finite Hash chain นี้ตรวจ accidental/local content alteration ได้ แต่ไม่ใช่ external signature และพิสูจน์ไม่ได้ว่าใครสร้างข้อมูล

## Deterministic recovery

`reconstruct_training_agent` สร้าง proposal ทุกตัวใหม่จาก frozen protocol, treatment และ paired seed แล้วตรวจ candidate ทั้งก้อน รวม variable ordering/values, parent candidate ID และ RNG checkpoint ก่อน proposal จากนั้น observe completed results ตาม attempt order หากไม่ตรงกันต้องหยุด execution แทนการแก้ state แบบเงียบ ๆ

Execution target ต้องเพิ่มทางเดียว ห้ามเกิน frozen budget ต่อ treatment/seed และห้ามลดต่ำกว่า opportunities ที่ consume ไปแล้ว Main-campaign evidence ต้องมี authorization ID ที่ไม่ว่างและตรงกับ campaign ID, evidence class และ seed สำหรับ admitted campaign ต้องมี explicit main-execution flag เพิ่มด้วย

## กติกา promotion

Promotion selection อ่านเฉพาะ terminal records ที่ partition เป็น `training` ในแต่ละ treatment/seed จะเรียง feasible candidates ตาม training objective จากน้อยไปมาก แล้วตาม candidate ID เลือกไม่เกิน frozen cap สองตัว และบันทึก shortfall ห้ามยืม shortfall จาก treatment หรือ seed อื่น และ reject holdout/refined evidence หากถูกส่งเข้าขั้น selection นี้

## การตรวจ Work 056 และข้อจำกัด

คำสั่ง Work 056 initialize ledgers แยกชื่อ `PREP-FU-BMC-001` ด้วย evidence class `preparation_only`, replay empty fingerprint ให้ exact และพิสูจน์ว่า unauthorized execution ถูก reject ก่อนเรียก evaluator ผลที่บังคับคือ `runner_prepared_campaign_locked` พร้อม `candidate_evaluations=0`, `burn_in_evaluations=0` และ `main_seed_evaluations=0`

หลักฐานที่ยังต้องทำใน work item ถัดไป ได้แก่ CalculiX evaluation adapter, STEP/FreeCAD finalist adapter, การทดลอง process interruption จริง, burn-in acceptance และ admitted campaign execution ไม่มีผลใดใน Work 056 ที่รองรับคำกล่าวอ้างเรื่อง race performance, material strength, fatigue, fracture หรือ whole-vehicle physical validation
