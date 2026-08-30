# ความพร้อมสำหรับ bounded whole-vehicle campaign

ไฟล์ต้นฉบับภาษาอังกฤษ: `BOUNDED_WHOLE_VEHICLE_CAMPAIGN_READINESS.md`

## คำตัดสิน

คำตัดสิน Work 054: `ready_for_bounded_whole_vehicle_campaign`

ความหมายคือกระบวนการวิจัยในขอบเขตจำกัดพร้อมขยับจาก pilot ไปสู่ whole-vehicle campaign ที่ preregister โดยใช้ Work 047 grammar, Work 048 load, Work 049 fixed baseline, Work 050 equal-budget search mechanics และ Work 053 refined structural gate ไม่ได้หมายความว่ารถผ่าน physical validation, ปลอดภัย, ผลิตได้, พร้อมแข่ง หรือเหนือกว่ารถจริงแล้ว

## สายหลักฐาน

```text
Work 047 complete derivable assembly grammar
  -> Work 048 force/moment transfer and overload DNF
  -> Work 049 fixed reference/heavy baseline controls
  -> Work 050 equal 96/96/96 GRID/RANDOM/EVOLUTION pilot
  -> Work 053 independent frame + CalculiX section-force gate
  -> Work 054 deterministic readiness adjudication
```

Work 050 readiness checks ผ่านทั้งหมดอยู่แล้ว ยกเว้น `independent_refined_evaluation` Work 053 ทำให้ evaluator นี้พร้อมและประเมิน frozen promotions ทั้ง 9 แบบ Work 054 join records เหล่านั้นโดยไม่เปลี่ยน objective, threshold, candidate identity, treatment budget หรือผล reject

## ชุดที่ผ่าน refined gate

| Treatment | Promotions เดิม | ผ่าน | Treatment winner | Holdout objective (s) |
|---|---:|---:|---|---:|
| GRID | 3 | 2 | `candidate-12b30a0606bccf88` | `34.1204253544251` |
| RANDOM | 3 | 3 | `candidate-58b6c6238b708e6a` | `35.42349737959053` |
| EVOLUTION | 3 | 2 | `candidate-333486cb11b2f603` | `34.16703235066346` |

global pilot winner คือ `candidate-12b30a0606bccf88` และผ่าน refined gate deterministic adjudication SHA-256 คือ `c8a5e89fba6d96be5a5cfa063a51a1d2b0eb597c25f24784dbe85a4c062da953`

candidate สองแบบยังถูก reject และไม่มีสิทธิ์เข้า bounded campaign:

- GRID `candidate-9b03158dc541df18`
- EVOLUTION `candidate-372db49a7cbceba5`

หลักฐาน cross-model stress ที่ขัดแย้งกันยังถูกเก็บไว้ objective หรือ yield margin ไม่สามารถนำมาลบล้างได้

## สิ่งที่อนุญาตแล้ว

- preregister และรัน whole-vehicle campaign ที่ใหญ่ขึ้นด้วย compute เท่ากัน ภายใน grammar/evaluator/load domain เดิมเท่านั้น
- ใช้ Work 053 refined gate กับ promoted candidate ทุกแบบก่อนเปรียบเทียบ treatment outcome
- เปรียบเทียบ fixed-topology กับ free-topology เฉพาะเมื่อ component library, constraint, seed, compute accounting และ evidence gate เท่ากัน
- รายงาน failure, numerical invalidity, conservation residual และ DNF เป็น outcome โดยไม่แก้เงียบ

## สิ่งที่ยังห้าม

- อ้าง physical validation, real-world safety, race superiority หรือ engineering discovery จาก Level 0/beam-network evidence
- รับ candidate ที่ reject สองแบบ หรือใช้ proxy capacity แทน refined evaluation
- ขยายไป arbitrary topology หรือ load/material อื่นโดยไม่มี protocol และ transfer evidence ใหม่
- ถือ synthetic material yield margin เป็น certified allowable

ก่อนกล่าวอ้าง hardware โครงการยังต้องมี higher-fidelity solid/contact/nonlinear analysis, buckling และ fatigue coupling ที่ vehicle interface, physical material record, calibration specimen, manufacturing tolerance และ hardware test
