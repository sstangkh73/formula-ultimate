# แผน Work 130: Manufacturing Tolerance Handoff

แหล่งภาษาอังกฤษ: `2026-09-12_130_manufacturing-tolerance-handoff-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

จับคู่ทุก component region จาก Work 126 กับ candidate process route, stock/source assumption, assembly step และ inspection access ที่ชัดเจน; ส่งต่อ tolerance ที่ลงทะเบียนเข้า clearance และ preload; และนำ downgraded evidence envelope จาก Work 129 เข้า manufacturing handoff decision

อนุญาต readiness เฉพาะ route ที่มี process-capability evidence ใช้ได้, assembly/inspection เข้าถึงได้, ลำดับทำได้ และ worst-case tolerance margin ผ่าน Unsupported route ยังคง `unknown` ไม่ใช่ impossible ไม่อนุญาต purchasing, fabrication หรือ safety certification

## ตัวแปร controls และไฟล์

- IV: process route, evidence class, tolerance allocation, assembly order และ access state
- DV: route status, access, worst-case clearance/preload, assembly feasibility และ unresolved blockers
- Controls: inaccessible fastener, trapped core, cyclic/impossible assembly, nominal-only clearance และ insufficient preload ต้อง fail closed
- สำเร็จเมื่อ: ทุก region มี mapping, source identity ตรง, ส่งต่อ worst-case tolerance, มี inspection/assembly dossier, redesign list ชัด และ exact replay

ไฟล์ที่วางแผน: `src/formula_ultimate/assembly/manufacturing_tolerance_handoff.py`, `config/development/manufacturing_tolerance_handoff_v1.json`, `scripts/development/run_manufacturing_tolerance_handoff.py`, `tests/test_manufacturing_tolerance_handoff.py`, สัญญาสองภาษา `docs/contracts/MANUFACTURING_TOLERANCE_HANDOFF_V1*`, plan/result สองภาษานี้ และ `artifacts/work130/run_a|run_b` ที่ ignore

## การตรวจสอบ

```powershell
python -m unittest tests.test_manufacturing_tolerance_handoff tests.test_repository_contract -v
python scripts/development/run_manufacturing_tolerance_handoff.py --config config/development/manufacturing_tolerance_handoff_v1.json --output-root artifacts/work130/run_a
python scripts/development/run_manufacturing_tolerance_handoff.py --config config/development/manufacturing_tolerance_handoff_v1.json --output-root artifacts/work130/run_b --replay-reference artifacts/work130/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 126/129 และตรวจ staged/cached diff โดยตรง; commit ทันทีเมื่อทุก gate ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

input เป็น G3 box registry ไม่ใช่ native manufacturing CAD minimum-feature heuristic ไม่ยืนยัน process capability สิ่งที่ไม่ทำ: purchasing, fabrication, supplier qualification, safety certification, global impossibility claims, push หรือ rewrite history
