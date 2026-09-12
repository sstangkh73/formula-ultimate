# แผน Work 123: ระบบรัน Candidate ทั้งคันแบบ Coupled Transient

แหล่งภาษาอังกฤษ: `2026-09-12_123_coupled-vehicle-transient-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

รวมอัตลักษณ์ Work 117–122 ที่ระบุแน่นอนเข้ากับ exploratory candidate transient แบบมีขอบเขตหนึ่งตัว พร้อมเจ้าของ state และเครื่องหมาย exchange ชัดเจน เชื่อม controller demand, ground-force capacity, actuation power/loss, stored energy, drag/cooling และ thermal state ผ่าน time base ร่วม โดยคงข้อจำกัด structural/material/interaction

ใช้บัญชี work ต่อ step ที่อนุรักษ์ event timing, fixed-point power coupling และ time step สามระดับ บันทึก history, interface ledger, validity excursion และ stop/failure state; เทียบ decoupled control เพื่อระบุต้นเหตุ coupling Integration ที่รันสำเร็จต้องไม่ promote candidate ที่ยังไม่ครบ

## ตัวแปร control และไฟล์

- IV: coupling enabled/decoupled, time step, controller demand, event timing, initial energy, frame/sign schema และ model validity
- DV: trajectory, final speed/position/energy/temperature, interface work/heat residual, coupling iteration, event และ promotion blocker
- Controls: external task/initial state เดียวกัน; sign/frame ผิด, power นับซ้ำ, command event หน่วง, พลังงานหมด, flow model นอกช่วง และ decoupled run
- Success: อัตลักษณ์ upstream ตรง, ledger อนุรักษ์, refinement สามระดับเสถียร, control เป็นเชิงเหตุ, blocker unresolved ชัด และ exact replay

ไฟล์ที่วางแผน: `src/formula_ultimate/simulation/coupled_vehicle_transient.py`, `config/development/coupled_vehicle_transient_v1.json`, `scripts/development/run_coupled_vehicle_transient.py`, `tests/test_coupled_vehicle_transient.py`, contract `docs/contracts/COUPLED_VEHICLE_TRANSIENT_V1*` สองภาษา, plan/result สองภาษาชุดนี้ และ `artifacts/work123/run_a|run_b` ที่ไม่ติดตามใน Git

## การตรวจสอบ

```powershell
python -m unittest tests.test_coupled_vehicle_transient tests.test_repository_contract -v
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_a
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_b --replay-reference artifacts/work123/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 117–122 และตรวจ staged/cached diff แบบระบุไฟล์ จะ commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Harness แบบลดรูปนี้ไม่ใช่รถรายละเอียดครบ สิ่งที่ไม่ทำ: เติม coefficient เอื้อให้โดเมน unresolved, อ้าง failure margin ที่ตรวจแล้ว, full controller/ground/aero dynamics, race completion, vehicle readiness, physical validation, push หรือแก้ประวัติ
