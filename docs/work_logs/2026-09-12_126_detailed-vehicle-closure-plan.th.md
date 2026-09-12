# แผน Work 126: การปิดรายละเอียดยานพาหนะ

แหล่งภาษาอังกฤษ: `2026-09-12_126_detailed-vehicle-closure-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

สร้าง G3 geometry registry เชิงกำหนดที่ตรวจสอบได้หนึ่งชุดสำหรับ detailed candidate เชิงสำรวจ และไล่ทุก external function ที่ลงทะเบียนผ่าน material region, hardware ที่ติดตั้ง และ interface ตรึง Work 118–125 ปิด ledger ของ mass/center/inertia/occupied-volume, energy, signal, heat และ load path พร้อม audit assembly และ swept motion แบบสุ่มตัวอย่าง

G3 ในที่นี้หมายถึง solid bounds, placement, ownership และ interface record ราย component ที่ชัดเจนใน registry แบบจำกัดนี้ ไม่ใช่ native CAD, manufacturing release หรือ physical validation ช่องว่างฟิสิกส์ที่จำเป็นต้องแสดงชัดและต้องคงสถานะ candidate เป็น `detailed_exploratory` ไม่ให้ promotion-ready

## ตัวแปร controls และไฟล์

- IV: ตำแหน่ง component, การมี hardware role, connection path, tolerance state และ motion sample
- DV: ความครอบคลุม function/hardware, region ownership ที่ไม่ซ้ำ, residual ของ mass/center/inertia/volume, ความต่อเนื่อง energy/signal/heat/load, overlap/clearance และความสดของ envelope
- Controls: เอา fastener/support/seal/signal path ที่จำเป็นออก; ใส่ hidden void, mass ownership ซ้ำ, interference และ subsystem envelope เก่า
- สำเร็จเมื่อ: deterministic replay, geometry/hardware path ที่ลงทะเบียนปิดครบ, declared ledger residual เป็นศูนย์ภายใน tolerance, assembly/motion ไม่มี collision และมี unresolved-evidence list ที่ปิดกั้น promotion อย่างชัดเจน

ไฟล์ที่วางแผน: `src/formula_ultimate/assembly/detailed_vehicle_closure.py`, `config/development/detailed_vehicle_closure_v1.json`, `scripts/development/run_detailed_vehicle_closure.py`, `tests/test_detailed_vehicle_closure.py`, สัญญาสองภาษา `docs/contracts/DETAILED_VEHICLE_CLOSURE_V1*`, plan/result สองภาษานี้ และ `artifacts/work126/run_a|run_b` ที่ ignore

## การตรวจสอบ

```powershell
python -m unittest tests.test_detailed_vehicle_closure tests.test_repository_contract -v
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_a
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_b --replay-reference artifacts/work126/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 118–125 และตรวจ staged/cached diff โดยตรง; commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

solid แบบ axis-aligned ที่ลงทะเบียนพิสูจน์ได้เฉพาะ bookkeeping และ non-overlap แบบจำกัด ไม่พิสูจน์ detailed surface manufacturability หรือ collision จริง hardware ที่ซื้อถูกระบุที่มา ไม่อ้างเป็น generated discovery สิ่งที่ไม่ทำ: ใช้ blocked geometry จาก Work 088 ซ้ำ, รับรอง native CAD, material/process qualification, physical survival, promotion, push หรือ rewrite history
