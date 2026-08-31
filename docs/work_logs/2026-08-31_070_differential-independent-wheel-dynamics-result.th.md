# ผล Work 070: Differential และพลวัตล้อขับเคลื่อนอิสระ

เอกสารผลภาษาไทยของแผนต้นฉบับ `2026-08-31_070_differential-independent-wheel-dynamics-plan.md`

สถานะ: เสร็จสมบูรณ์ (Completed)

เอกสารต้นฉบับภาษาอังกฤษ: `2026-08-31_070_differential-independent-wheel-dynamics-result.md`

## ผลลัพธ์

สร้าง ideal open-differential carrier และสถานะล้อขับเคลื่อนซ้าย/ขวาอิสระบน geometry v3 เดิมจาก Work 069 แบบจำลองปิด common/modal inertia โดยไม่นับซ้ำ ใช้ branch connection efficiency `0.98` ที่ประกาศ แสดง connection/slip/differential heat รักษา carrier-average constraint และส่งต่อ branch overspeed เป็น `DNF`

grip สมมาตรคง branch speed เท่ากันและ modal energy เป็นศูนย์ split grip ที่อนุมัติวิ่งจบด้วย branch speed `141.05601957062677` และ `74.25341080361065 rad/s`; mirrored control สลับทั้งสองค่าตรง ๆ พลังงานศูนย์ไม่สร้างการเคลื่อนที่ และ operational limit `25 rad/s` ทำให้เกิด terminal event `differential_branch_overspeed` ตามคาด

## ไฟล์ที่เปลี่ยน

- `config/vehicle/functional_differential_drive_v1.json`
- `src/formula_ultimate/simulation/differential_drive_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_differential_drive.py`
- `tests/test_differential_drive_coupling.py`
- `docs/research/DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.md`
- `docs/research/DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.th.md`
- บันทึกแผน/ผล Work 070 สองภาษาที่ตรงกัน

หลักฐานที่ git ignore อยู่ใต้ `artifacts/work070/` รวม materialized architecture, canonical experiment JSON และ exact replay copies

## หลักฐาน

- Common inertia closure: `2.2393151654985397 + 2(0.13034241725073026) = 2.5 kg m^2`
- แรงสถิตที่ driven contact: `701.6810927158073 N` ต่อ branch จากสมดุล Work 069
- ความเร็วรถสุดท้ายแบบสมมาตร: `11.68448249437216 m/s`; branch speed เท่ากัน `103.15502526901471 rad/s`; modal energy `0 J`
- ความเร็วรถสุดท้ายแบบ split: `9.96057727044386 m/s`; ซ้าย/ขวา `141.05601957062677/74.25341080361065 rad/s`; modal speed `-33.401304383508055 rad/s`
- split modal energy สูงสุด `324.1158550756573 J`; connection heat `599.8816054535888 J`; differential heat `60.115830964968396 J`
- split interface residual สูงสุด `1.9071116214020023e-12 J`; global relative residual `1.0060348957777023e-8`
- mirror aggregate และ exchanged-branch residual: `0` ตรง ๆ สำหรับค่าที่เลือก
- half-step difference สูงสุด `0.00023334677638767642` ต่ำกว่า `0.02`
- Reference result SHA-256: `c23eea2641b6863da2d63eb8a2ca3b7ae5ad94a53822c70bffd8fa1bffb1b92a`
- Split result SHA-256: `eee844e411d194c5d2205e5467ce42d3877867b013863fd4cd0772bda2be4879`
- Evidence SHA-256: `bc23719a3fbd0d343898488f263bf805d8aae8152acc6de4ef23ff2d410cd79a`
- architecture bytes ตรงกับ Work 069; ไม่มีการกล่าวอ้าง CAD solid ใหม่

## คำสั่ง validation ที่ใช้จริงและสถานะ

```powershell
python -m unittest tests.test_differential_drive_coupling -v
# exit 0; Ran 9 tests; OK

python scripts/experiments/run_differential_drive.py --config config/vehicle/functional_differential_drive_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work070/materialized_architecture_v3.json --output artifacts/work070/experiment_evidence.json
# exit 0; status passed

# ทำซ้ำโดยเขียน output ใต้ artifacts/work070/replay
# evidence_exact=true, architecture_bytes_exact=true,
# reference_exact=true, split_exact=true

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests
# exit 0; Ran 421 tests in 39.066s; OK
```

## การตัดสินใจ ข้อจำกัด และงานถัดไป

split-grip control ที่อนุมัติถูกตรึงที่ `mu=(1.0,1.2)` การสำรวจ `mu=(0.35,1.2)` ถึง architecture branch overspeed ก่อน `2 s` จึงไม่ถูกระบุผิดว่าเป็นการรันที่ผ่าน Overspeed ยังคงเป็น failure evidence ที่ชัดเจน

งานนี้เป็น open differential แบบ lumped สังเคราะห์ ไม่ใช่ internal geometry ที่ resolve หรือ hardware validation ยังคงใช้แรงสถิตคงที่ และไม่มี shaft elasticity ต่อ branch, backlash, bearings, lubrication, limited-slip behavior, reverse rotation, tyre thermal/wear state และ suspension transients

งานถัดไปควรรวม independent branch states กับ planar steering/yaw และ transient normal-load transfer แล้วจึงเพิ่ม internal transmission geometry พร้อม structural/thermal evidence
