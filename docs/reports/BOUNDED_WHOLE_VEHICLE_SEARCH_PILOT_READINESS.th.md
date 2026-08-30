# Bounded Whole-Vehicle Search Pilot และ Readiness Review

ไฟล์ต้นฉบับภาษาอังกฤษ: `BOUNDED_WHOLE_VEHICLE_SEARCH_PILOT_READINESS.md`

## คำตัดสิน

```text
not_ready
blocker: independent_refined_evaluation
```

Search apparatus ผ่าน equal-budget, replay, provenance, candidate-schema, exploit และ frozen-holdout mechanics แต่ยังไม่พร้อมสำหรับ bounded main campaign เพราะไม่มี independent whole-vehicle stress/deformation evaluator จึงไม่มี candidate ใดถูกประกาศเป็นผู้ชนะ

## Pilot ที่ preregister

- treatment: `GRID`, `RANDOM`, `EVOLUTION`
- seed: `101`, `202`, `303`
- attempted evaluation ต่อ treatment/seed: `32`
- attempts ต่อ treatment: `96`
- attempted evaluation รวม: `288`
- grammar, structural, energy หรือ numerical failure ทุกกรณีใช้หนึ่ง attempt

ทุก treatment ใช้ evaluator, Work 048 training/holdout case, bound, component library และ tolerance เดียวกัน Candidate code เปลี่ยนได้เฉพาะ Work 047 grammar variable ห้าค่า: core length, core width, ground-contact radius, source primitive size และ propulsor primitive size Material density คงที่เพราะยังไม่มี density-strength relation ที่ยอมรับ

Candidate geometry ถูก rebuild และ grammar-validate ทุก attempt Analytical mass มาจาก primitive volume และ fixed material density Bounded structural-capacity proxy ขึ้นกับ cross-section/radius/primitive scale ที่เกี่ยวข้อง จึงมี causal geometry path ที่ Level 0 แต่ไม่ใช่ stress solver

## ผลตาม treatment

| Treatment | Attempts | Feasible | Feasible rate | Structural failures | Best training time |
|---|---:|---:|---:|---:|---:|
| `GRID` | 96 | 50 | `0.5208333333333334` | 46 | `34.1204253544251 s` |
| `RANDOM` | 96 | 71 | `0.7395833333333334` | 25 | `35.42349737959053 s` |
| `EVOLUTION` | 96 | 86 | `0.8958333333333334` | 10 | `34.16703235066346 s` |

ผลเหล่านี้เป็น descriptive pilot ไม่ใช่หลักฐานว่า treatment/candidate หนึ่งเหนือกว่า ความต่างอาจอธิบายด้วย five-variable bound และ analytical proxy `GRID` มี provisional training objective ต่ำสุด แต่ไม่ใช่ผู้ชนะเพราะ refinement ไม่มี

## Promotion และ readiness

Promote best training-feasible candidate หนึ่งตัวต่อ treatment/seed รวมเก้าตัว ทั้งเก้าตัวยัง feasible บน frozen Work 048 holdout case และทั้งเก้าตัวได้ `refined_status=unavailable`; ไม่มีตัวใดถูกใส่ค่าผ่านอย่างเงียบ ๆ ดังนั้น promotion chain ไม่เลือกผู้ชนะ

Readiness check:

| Check | ผล |
|---|---:|
| exact replay | ผ่าน |
| equal budget | ผ่าน |
| same evaluator | ผ่าน |
| frozen holdout pass | ผ่าน |
| no exploit | ผ่าน |
| complete provenance | ผ่าน |
| independent refined evaluation | **ไม่ผ่าน** |

## Replay และ ledger evidence

- record-set SHA-256: `b35beb7d8b08040c56ab26ec0633f4eb48d9f18ef3219b592cf5c2ffa62ed3bc`
- result/replay JSONL SHA-256: `15d20e607ddc0e60d6f70e5dc027be680f392a1c55c1a744edf0f1fdd0cbb7bb`
- budget-ledger SHA-256: `1c27bbe2a5917dd1334a140be3e1550d6028b3391af438bbdd6aa87bceb79224`
- ledger content equality: exact
- exploit control ที่ reject: `5`

แต่ละ record มี treatment, seed, attempt index, geometry variable, parent identity, RNG checkpoint, status/failure code, evaluator identity และ result hash Evolution attempt หลัง initial random phase เก็บ parent ancestry Result/budget ledger ถูกเขียนตามลำดับ; failed candidate ยังมองเห็นและถูกนับ

## Falsification และข้อจำกัด

ก่อน admitted run ได้ตัด mutable material-density variable ออก เพราะ density ต่ำลงโดยไม่มี strength evidence จะสร้าง unphysical optimization exploit แล้วแทนด้วย source/propulsor geometry scale โดย material property คงเดิม

Pilot ไม่สามารถ establish engineering merit หลักฐานที่ขาดมี independent whole-vehicle stress/deformation solver, mesh/refinement convergence, arbitrary topology, calibrated material strength, contact/preload/friction, transient load, aerodynamics ที่สูงกว่า frozen proxy, thermal reliability, real-circuit admission, manufacturing และ physical test

งานถัดไปต้อง implement และ validate independent refined evaluator จริง ห้ามเพียงเปลี่ยนชื่อ capacity-factor proxy เดิม เมื่อมี evidence แล้วควรรัน Work 050 ซ้ำเป็น remedial work item ใหม่โดยเก็บ ledger เดิมไว้

## การทำซ้ำ

```powershell
.\scripts\run_work050.ps1
py -3.14 -m unittest tests.test_whole_vehicle_search -v
```
