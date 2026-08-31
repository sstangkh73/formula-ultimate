# ผล Bounded Main Campaign v3

ไฟล์ต้นฉบับภาษาอังกฤษ: `BOUNDED_MAIN_CAMPAIGN_V3_RESULT.md`

## คำตัดสิน

Protocol `bounded_whole_vehicle_main_campaign_v3`, campaign `FU-BMC-003` จบด้วยสถานะ `completed_with_supported_finishers` Attempted evaluations ครบ `2,880` รายการและเป็น terminal results ทั้งหมดด้วยงบเท่ากัน: treatment/seed ทั้ง 36 streams มี 80 attempts, treatment ละ 960 attempts, ไม่มี pending reservation และ GRID proposals ไม่ซ้ำ 960 รายการ Exact clean-tree replay ผ่าน

นี่เป็น comparative evidence เฉพาะภายใน frozen five-variable geometry grammar, synthetic-material assumptions, load partitions, Level-0 evaluator, linear-beam refinement และ STEP/FreeCAD witness route เท่านั้น ไม่ใช่ physical validation, safety certification, manufacturability evidence, arbitrary-topology validation หรือหลักฐานว่า algorithm เหนือกว่า

## แบบการทดลอง

- Independent variable: proposal treatment `GRID`, `RANDOM` หรือ `EVOLUTION`
- Paired experimental units: seeds `55001` ถึง `55012`; individual attempts ไม่ใช่ independent replicates
- Controls: งบ 80 attempts เท่ากัน, candidate bounds, training evaluator, frozen training/holdout partitions, promotion count, Work 053 refinement gates และข้อกำหนด `3D -> STEP -> FreeCAD` witness เหมือนกัน
- Dependent variables: supported-finisher presence ต่อ treatment/seed, seed-level best frozen-holdout time, failure distribution, refinement survival และ CAD-witness completion
- Primary falsification rule: EVOLUTION-minus-RANDOM supported-finisher-rate difference ที่ไม่เป็นบวกจะขัดแย้งกับทิศทางที่ตั้งสมมติฐานไว้ การอ้าง algorithm superiority ยังต้องมี independent replication ภายใต้ protocol ใหม่

## หลักฐานการรัน

Training ให้ผล feasible `2,107` และ structural failure `773` ทั้ง 36 streams เลือก candidate ได้ stream ละสองตัว จึงมี 72 candidates เข้าสู่ frozen holdout โดย promotion shortfall เป็นศูนย์ ทุก promoted candidate feasible บน holdout Work 053 refinement ผ่าน 51 และปฏิเสธ 21 ด้วย `refined_disagreement`; กรณีหลังถูกบันทึกและ CAD stage เป็น `not_run` Refinement survivors ทั้ง 51 ตัวสร้าง four-solid STEP assemblies ที่ valid และผ่าน FreeCAD 1.1.3 inspection โดยไม่มี hidden geometry repair

Stage ledger มี refinement benchmark หนึ่งรายการ, promotion records 36, holdout records 72, refinement records 72 และ CAD-witness records 72 หลักฐานบันทึก CalculiX processes 1,299, CadQuery generation processes 51 และ FreeCAD inspection processes 51 Admitted invocation ใช้เวลา `10,327.025 s`; ผลรวม external-process wall time ที่บันทึกใน stage evidence คือ `239.847 s`

## ผลลัพธ์ที่ preregistered

| Treatment | Supported seeds | Rate |
| --- | ---: | ---: |
| GRID | 10/12 | 0.8333 |
| RANDOM | 9/12 | 0.7500 |
| EVOLUTION | 11/12 | 0.9167 |

สำหรับ primary EVOLUTION-minus-RANDOM comparison, paired rate difference เท่ากับ `+0.1667`, มี EVOLUTION-only pairs สองคู่, RANDOM-only pairs ศูนย์คู่, exact two-sided McNemar `p = 0.5` และ paired-bootstrap 95% interval `[0.0000, 0.4167]` ทิศทางที่สังเกตสนับสนุน preferred hypothesis ในเชิงพรรณนา แต่ exact test ยังไม่สร้างความแตกต่างที่มีนัยสำคัญทางสถิติ

ในเก้า seeds ที่ทั้งสอง treatments มี supported finishers, EVOLUTION-minus-RANDOM paired median best-time difference เท่ากับ `-2.232959 s`; exact two-sided sign-flip `p = 0.0625` และ paired-bootstrap 95% interval `[-2.564327, -1.546702] s` ผลนี้เข้าข้าง EVOLUTION ใน bounded run นี้ แต่ยังไม่ผ่าน conventional `0.05` significance threshold การเปรียบเทียบ GRID ยังคงเป็น descriptive ตาม preregistration

## Replay identities

- Protocol fingerprint: `9ef748f2719923632a05ef5fcbba95b8f2fa1b4156d2dbbf6cb9b4fbd02d4c36`
- Training fingerprint: `503917192f3029c66e27cec2a2ef1f7521ebfba9c2872e3541945bf35a281176`
- Stage fingerprint: `9e2554f865788b98c21cff736063d46857eff888e022299256222fad186e1182`
- Analysis fingerprint: `f6a86288b3653b75d1d5c56f62b948344884911d946b91ef8ddbfc6e46dbef19`
- Execution source commit: `bfa33a29bc92890628df0429351cef3e6eed017e`
- Worktree dirty during run: `false`

## Scientific review

หลักฐานสนับสนุนคือ equal opportunity allocation, immutable consumed failures, frozen holdout separation, exact chained-ledger replay, terminal downstream evidence ของทุก promotion และ derivable STEP/FreeCAD survivors 51 ตัว หลักฐานที่ขัดแย้งคือ primary exact test ไม่มีนัยสำคัญและ 21/72 เกิด refined disagreement แม้ Level-0 holdout feasible คำอธิบายที่ดูดีอาจขึ้นกับ frozen five-variable grammar แทนที่จะเป็น general search quality

Confidence สูงว่า bounded campaign รันและ replay ตาม preregistration, ปานกลางว่า EVOLUTION เร็วกว่าใน common-success seeds ของ campaign นี้ และต่ำสำหรับการ transfer นอก evaluator domain หลักฐานที่ยังขาดคือ independent replication, solid/contact/nonlinear whole-vehicle analysis, calibrated physical material properties, manufacturing tolerances, fatigue spectra, crash/failure propagation และ hardware tests
