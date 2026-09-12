# แผน Work 119: ชุดส่งกำลังและ actuation ที่มีฮาร์ดแวร์รองรับ

แหล่งภาษาอังกฤษ: `2026-09-12_119_realized-actuation-chain-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

สร้าง reference route แบบ rotary coaxial ที่เปิดเผยและมีขอบเขตหนึ่งเส้นทาง เพื่อแปลง port torque/speed ขาเข้าเป็น port torque/speed ขาออกผ่าน transfer member, support และ containment ที่มี geometry จริง ตรึงหลักฐาน load/motion จาก Work 114, thermal burden จาก Work 115 และ material applicability จาก Work 116 พร้อมเปิดทาง conversion แบบอื่นผ่าน extension slot ที่ชัดเจน

หา mass, torsional stiffness/stress, speed/load saturation, efficiency loss, heat และ support reaction จาก geometry และ property synthetic ที่ลงทะเบียน คง claim การรอดของ material เป็น blocked และปฏิเสธ ideal conversion ที่ hardware coverage ไม่ครบ

## ตัวแปร control และไฟล์

- IV: geometry ของ transfer member, reduction ratio, input torque/speed, temperature, ทิศทาง, output lock และการเชื่อมต่อ path/support
- DV: output torque/speed/work, loss/heat, stiffness/twist, stress, capacity, mass ของ hardware ครบชุด และ support reaction
- Controls: port/material/โอกาสพลังงานเดียวกัน; path ถูกตัด output ถูกล็อก การทำงานย้อนทิศ torque อิ่มตัว และเอา support ออก
- Success: geometry รองรับ action ที่รับเข้าทุกรายการ; input power เท่ากับ output บวก modeled loss; envelope/temperature fail closed; control เป็นเชิงเหตุ; exact replay ผ่าน

ไฟล์ที่วางแผน: `src/formula_ultimate/subsystems/realized_actuation_chain.py`, `config/development/realized_actuation_chain_v1.json`, `scripts/development/run_realized_actuation_chain.py`, `tests/test_realized_actuation_chain.py`, contract `docs/contracts/REALIZED_ACTUATION_CHAIN_V1*` สองภาษา, plan/result สองภาษาชุดนี้ และ `artifacts/work119/run_a|run_b` ที่ไม่ติดตามใน Git

## การตรวจสอบ

```powershell
python -m unittest tests.test_realized_actuation_chain tests.test_repository_contract -v
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_a
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_b --replay-reference artifacts/work119/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 114/115/116 และตรวจ staged/cached diff แบบระบุไฟล์ จะ commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Route ที่เลือกเป็น synthetic Level-0 reference ไม่ใช่ technology whitelist ถาวรหรือใบอนุญาตให้สร้าง สิ่งที่ไม่ทำ: บังคับ gear/shaft/motor สำหรับทุกข้อเสนอ, อ้าง efficiency/material strength ที่ validate แล้ว, fatigue/wear, รายละเอียด bearing/fastener, controller hardware, physical validation, push หรือแก้ประวัติ
