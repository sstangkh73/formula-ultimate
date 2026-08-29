# Integration Falsification และ Promotion Gate

สถานะ: Level-0 release review ของ Work 030

ไฟล์ต้นฉบับภาษาอังกฤษ: `INTEGRATION_FALSIFICATION_PROMOTION_GATE.md`

## จุดประสงค์

Work 030 ปิด coupled implementation queue โดยแยกสามคำถาม:

1. transaction ปฏิเสธ deliberate integration defect ได้หรือไม่
2. analytical reference คงที่ภายใต้ timestep refinement ที่ประกาศหรือไม่
3. มี independent evidence พอ promote candidate ให้พ้น Level 0 หรือไม่

คำตอบของ repository ปัจจุบันคือ **ได้**, **ได้ภายใน steady analytical control ที่แคบ** และ **ยังไม่ได้** ดังนั้น release status เป็น `level0_experimentation_ready_promotion_blocked`

## Gate Protocol

`config/simulation/integration_promotion_gate_v1.json` fingerprint:

- fault case ที่บังคับหกชุดและ expected failure code
- refinement timestep `(2000, 1000, 500) s`, seed `17`, common budget `128` step และ tolerance
- completion ขั้นต่ำสิบ profile
- real-circuit admission ที่บังคับ
- independent evidence ระดับ `level1` หรือสูงกว่า
- cross-model evidence type ที่บังคับหกชนิด
- `automatic_discovery_claim = false`

unknown field, implicit budget type, requirement ซ้ำ, fidelity level ที่ไม่รองรับ และ automatic discovery ถูกปฏิเสธ

## Deliberate Fault Matrix

control transaction commit ส่วน injected defect ทุกตัวคืน invalid transaction และไม่มี committed state:

| Fault | Expected/observed code | Rollback |
|---|---|---|
| ตัด adapter | `adapter_coverage` | yes |
| ทำ model version เสีย | `adapter_version_mismatch` | yes |
| ทำ residual identity ซ้ำ | `evidence_identity_duplicate` | yes |
| บังคับ numerical residual ให้ fail | `residual_failure` | yes |
| emit output นอกประกาศ | `adapter_exception` | yes |
| ทำ next-state time ถอยหลัง | `time_regression` | yes |

synthetic adapter เหล่านี้แยกทดสอบ atomic transaction enforcement ส่วน domain fixture Work 023-029 ก่อนหน้า exercise physical adapter, invalid corridor, energy depletion, thermal failure, missing evidence และ budget exhaustion แยกแล้ว

## Baseline Evidence Identity v2

promotion gate เชื่อ visible field กับ stale hash ที่ไม่เกี่ยวกันไม่ได้ Work 030 จึง upgrade campaign evidence model เป็น `work029-baseline-campaign-v2`:

- hash run field ทุกตัวนอกจากช่อง fingerprint ของตัวเอง
- hash campaign result field ทุกตัวนอกจากช่อง fingerprint ของตัวเอง
- คำนวณ run/aggregate count และ flag ซ้ำ
- identity protocol/control/architecture ของ run ต้องตรงกับ campaign
- top-level real-circuit admission ต้องตรงกับทุก run

validated campaign result fingerprint v2 คือ `79a03587e6bbeb17101c89a59c7fe61053571f493a29fbe356322418726d2a9b`

## Timestep Refinement

calibration profile หนึ่งชุดและ holdout profile หนึ่งชุดรันที่ timestep ทั้งสามด้วย seed `17` และ maximum ร่วม `128` step Sample หกชุด finish พร้อม residual ผ่านทั้งหมด

- maximum relative finish-time variation: `0.0`
- maximum relative primary-energy variation: `1.5466148595436325e-14`
- maximum absolute finish-distance residual: `0.0 m`
- attempted step ต่อ profile: `16`, `31` และ `62`

energy variation อยู่ระดับ floating point อย่างไรก็ตาม `convergence_order_estimated = false`: steady drag-balanced analytical solution ใช้สร้าง convergence order, nonlinear circuit behavior, quantified model uncertainty หรือ higher-fidelity agreement ไม่ได้

## Cross-Model Promotion Requirement

promotion ต้องมี independent passing evidence ระดับ `level1` หรือสูงกว่าสำหรับ:

1. `geometry-mass-inertia`
2. `surveyed-circuit-corridor`
3. `cross-model-aerodynamics`
4. `structural-safety`
5. `thermal-reliability`
6. `quantified-uncertainty`

candidate ปัจจุบันไม่มีหลักฐานเหล่านี้และไม่มี real-circuit admission สถานะ promotion จึงเป็น `blocked` พร้อมเก็บเหตุผลเจ็ดข้อครบ Test-only complete evidence fixture ภายใต้ real-admission requirement ที่ผ่อนเฉพาะ test ไปได้เพียง `eligible_for_independent_review`; discovery และ automatic promotion ยังเป็น false

## Release Decision

repository พร้อมสำหรับ **gated Level-0 experimentation** เพราะ:

- baseline 30 run/สิบ profile finish ภายใน control
- campaign identity และ aggregate verify
- transaction fault หกชุด fail-closed ทั้งหมด
- bounded timestep sensitivity gate ผ่าน

คำกล่าวอ้างต่อไปนี้ยังถูกห้าม:

- real-circuit performance หรือ lap time
- discovery หรือ technological superiority
- physical validation
- safety
- manufacturability

Level-0 autonomous candidate generation สามารถใช้ contract เหล่านี้เป็น early selection environment ได้ แต่ candidate ทุกตัวต้องอยู่หลัง fair-compute, evidence-identity, falsification, refinement และ cross-model gate เดียวกัน

## Evidence Fingerprint

- gate: `ad629075e69001b17eaf8b8e9371ecb72fc52a4e07a762c4546096daf9d23814`
- falsification suite: `a6c0b5a1a30abda519ed230114ca5c49b5754bb2bd763e505ae0f2f77ec15f4b`
- refinement: `fdb02195f1a77709b9f43f5d1b1d86736f73e0862dbb9d605f56017a28462af2`
- blocked promotion decision: `bf78fcb402c43e633399342d3e93a3473d3f2c4defa2e1447163bc34d059400f`
- release review: `783e156bb2a8d8dcad356033b6767fb2b2cbef9b9f0f3d1f94df13a83ab94f29`

## งานวิจัยที่เหลือ

การจบ Work 030 ปิด software implementation queue ไม่ใช่ปิดโปรแกรมวิจัย ระยะวิจัยถัดไปต้องหา/สร้าง geometry-linked physical evidence, measured circuit corridor/condition, calibrated หรือ independent model, uncertainty bound และ physical testing สิ่งเหล่านี้เป็น evidence prerequisite ไม่ใช่ conventional design prescription ดังนั้น vehicle architecture search ยังเปิดกว้าง
