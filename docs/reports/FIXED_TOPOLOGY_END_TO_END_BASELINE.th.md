# Fixed-Topology End-to-End Whole-Vehicle Baseline

ไฟล์ต้นฉบับภาษาอังกฤษ: `FIXED_TOPOLOGY_END_TO_END_BASELINE.md`

## ขอบเขตผลลัพธ์

Work 049 พิสูจน์ deterministic orchestration สำหรับ fixed Work 047 candidate หนึ่งคันผ่าน evidence class ที่ implement อยู่ในปัจจุบัน:

```text
3D declaration -> STEP -> FreeCAD mass properties
-> frozen Work 048 load cases -> bounded failure coupling
-> deterministic Level 0 distance/time/energy fixture
```

งานนี้ไม่พิสูจน์ว่า candidate แข็งแรงจริง, aerodynamically valid, ปลอดภัย, ผลิตได้, optimized หรือแข่งขันได้ Structural stage ยังเป็น rigid-component cut-load algebra พร้อม declared synthetic capacity

## การทดลองที่ freeze

Reference candidate และ Work 048 training/holdout identity เป็น immutable Level 0 fixture ใช้ `1000 m`, reference speed `25 m/s`, initial energy `150000 J`, propulsion demand `100 J/m` และ auxiliary power `200 W` นี่คือ synthetic orchestration fixture ไม่ใช่ circuit/lap-time model

Reference ถูก evaluate ที่ timestep `1.0/0.5/0.25 s` และ bounded capacity factor `0.995/1.000/1.002` Exact finish-event localization ทำให้ timestep comparison deterministic Capacity factor ใช้ audit sensitivity เท่านั้น ไม่ใช่ finite-element mesh

## Reference และ falsification control

| Variant | Outcome | เวลา | พลังงานที่ใช้ | Maximum utilization | ความหมาย |
|---|---:|---:|---:|---:|---|
| reference | `finished` | `40.0 s` | `108000 J` | `0.715678478993928` | fixed reviewed baseline |
| weak control | `DNF` | n/a | n/a | มากกว่า `1` | ลด structural capacity ครึ่งหนึ่งโดยตั้งใจ |
| disconnected control | `DNF` | n/a | n/a | demand ไม่เปลี่ยน | ตัด load path แบบ explicit |
| heavy feasible control | `finished` | `43.81780460041329 s` | `128763.56092008266 J` | `0.8588141747927136` | mass scale `1.2`, topology ไม่เปลี่ยน |

Heavy control แสดงว่า evaluator นี้ไม่ได้บังคับว่ามวลต่ำสุดเท่านั้นจึง feasible: มัน finish แต่จ่าย penalty ด้านเวลา พลังงาน และ structural demand อย่าง explicit

## Refinement และ replay

- finish-time maximum relative change: `0`
- bounded structural-utilization maximum relative change: `0.007035175879396918`
- structural change ที่ยอมรับ: `0.01`
- reference result SHA-256: `12774be503f21212cd35cc10b48f1eb60ab5740005ab264dfa17b35f87eb1097`
- nine-cell reference matrix SHA-256: `237b2454eb0d4d83c750177ce96964d3fdadbcf52e456687f47e2c43f28fb71c`
- negative control ที่ reject: `4`

Frozen training/holdout load case ทั้งเจ็ดกรณีอยู่ในทุก reference record Same-input evaluation exact Missing evidence, STEP identity ที่เปลี่ยน, nominal case set ไม่ครบ และ unregistered timestep fail closed

## บันทึก falsification

Acceptance runner รอบแรกพยายามสร้าง incomplete-case control โดยลบ Work 048 record ตัวสุดท้าย Record นั้นเป็น overload control แยกต่างหาก ทำให้ nominal set ยังครบและ negative control ถูก admit อย่างถูกต้อง Fixture ถูกแก้ให้ลบ training case ที่ระบุชื่อ; ไม่มี evaluator, threshold หรือ result formula เปลี่ยน

Supporting evidence แข็งแรงสำหรับ orchestration/bookkeeping แต่ contradicting evidence ชี้ readiness blocker ชัดเจน: structural-resolution matrix ที่เรียกอยู่เปลี่ยน declared capacity factor และไม่มี independent stress field, deformation field, mesh convergence หรือ alternate solver Work 050 รัน bounded pilot เพื่อทดสอบ fairness mechanics ได้ แต่ readiness review ต้องรักษา unresolved blocker นี้

## การทำซ้ำ

```powershell
.\scripts\run_work049.ps1
py -3.14 -m unittest tests.test_whole_vehicle_baseline -v
```
