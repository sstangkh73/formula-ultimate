# แผน Work 024: Aerodynamic Chassis และ Normal-Load Coupling

ต้นฉบับภาษาอังกฤษ: `2026-08-28_024_aero-chassis-load-coupling-plan.md`

สถานะ: Completed

## วัตถุประสงค์

Couple ผล aerodynamic map เดิมเป็น chassis force/moment wrench ชัดเจนและ
normal-load equilibrium สำหรับ contact topology ใดก็ได้ พร้อมเก็บ cooling
evidence และ force/moment residual โดย map query ที่ไม่รองรับหรือ contact load ที่
เป็นไปไม่ได้ต้องทำให้ adapter step invalid

## ขอบเขต

- กำหนด body-axis force/moment และ aerodynamic reference-origin contract
- Translate map force/moment มาที่ centre of mass ด้วย `r x F`
- Generalize minimum-change normal-load projection ให้รวม aerodynamic vertical
  force, pitch moment และ roll moment สำหรับ arbitrary contact topology
- เก็บ vertical/pitch/roll equilibrium residual โดยไม่แก้ค่า
- สร้าง `aerodynamic_map` และ `normal_load_solver` adapter ด้วย signal set จาก
  Work 021 และ fail-closed behavior จาก Work 022
- พิสูจน์ sign ของ drag/downforce/cooling, centre-of-pressure load shift,
  three-contact support, replay, map-envelope rejection, contact lift และ rank
  deficiency
- เพิ่ม validator, เอกสาร model/result สองภาษา, queue update, bug report หากพบ,
  validation และ commit หนึ่งชุด

## ไฟล์ที่วางแผน

- `src/formula_ultimate/simulation/aero_load_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_aero_load_coupling.py`
- `scripts/validate_aero_load_coupling.py`
- `docs/simulation/AERO_CHASSIS_LOAD_COUPLING.md` และ `.th.md`
- queue และ Work 024 plan/result สองภาษา; problem report หากจำเป็น

## นิยามการทดลอง

- สมมติฐาน: aerodynamic wrench ที่ translate รอบ centre of mass เปลี่ยน total/
  per-contact normal load พร้อม force/moment balance ปิด โดยไม่ขึ้นกับรถสี่ล้อ
- Independent variables: map operating point, reference-origin offset, contact
  coordinate, acceleration estimate และ map validity
- Dependent variables: body wrench, cooling evidence, per-contact load,
  equilibrium residual, adapter status และ candidate write
- Controls: Work 017 map evaluator เดิม, SI body axes (`x` หน้า, `y` ซ้าย,
  `z` ขึ้น), immutable Work 016 contact geometry และ exact signal contract
- Success: analytical symmetric/offset case ปิดใน tolerance; three-contact ผ่าน;
  invalid map/lift/rank ไม่ emit successful coupling output; repository ผ่าน
- Failure: sign กลับ, moment translation หาย, clipping เงียบ, residual ถูกแก้,
  บังคับ topology, รับ unsupported query หรือ commit fail

## ความเสี่ยงและสิ่งที่ไม่ทำ

ต้องประกาศ coefficient sign convention และ reference origin ชัด Level-0 map เป็น
synthetic จนกว่าจะมี evidence สูงกว่า งานนี้ไม่ resolve tyre, suspension, braking,
motion, whole race, CFD/FEA หรือ physical validation; ไม่แก้ README และไม่ push
remote history

## Validation

```powershell
python -m unittest tests.test_aero_load_coupling -v
python -m unittest discover -s tests -v
python scripts/validate_aero_load_coupling.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```
