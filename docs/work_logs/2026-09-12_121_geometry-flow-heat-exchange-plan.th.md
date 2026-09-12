# แผน Work 121: การไหลและแลกเปลี่ยนความร้อนจาก Geometry

แหล่งภาษาอังกฤษ: `2026-09-12_121_geometry-flow-heat-exchange-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

สร้าง reference internal-flow/heat และ external-flow load ที่มี gate แยกกัน โดยตรึงกับ hollow B-rep mesh จาก Work 110, heat source จาก Work 115 และ applicability boundary จาก Work 116 ทำให้ passage diameter/length ที่ลงทะเบียนและ projected bounds ภายนอกจาก mesh เปลี่ยน pressure, heat-transfer capacity, pumping power และ aerodynamic load เชิงเหตุ

ตรวจ reference ของทางไหลวงกลม laminar ด้วย Hagen-Poiseuille pressure drop และ fully developed constant-wall-temperature heat transfer ตรวจ adapter quadratic drag แบบ incompressible subsonic แยกต่างหากด้วย coefficient synthetic ที่ประกาศและ far-field domain sensitivity ส่ง pressure/heat/drag load กลับโดยไม่เลื่อน scope ใดเป็น whole-car aerodynamics

## ตัวแปร control และไฟล์

- IV: passage diameter/length, segment refinement, flow/source, projected geometry จาก mesh, external speed, surface/cavity mutation และ far-field size
- DV: pressure drop, outlet temperature, heat rejected/capacity, pumping power, drag/pressure/shear load, moment และ reference error
- Controls: source/ambient/task เดียวกัน; passage ถูกอุด, flow/source ศูนย์, mutation diameter/projected area, far-field sensitivity และ conservation
- Success: internal/external scope ผ่าน analytic/refinement/conservation gate ของตนเอง; geometry mutation เป็นเชิงเหตุ; exact replay ผ่าน

ไฟล์ที่วางแผน: `src/formula_ultimate/physics/geometry_flow_heat_exchange.py`, `config/development/geometry_flow_heat_exchange_v1.json`, `scripts/development/run_geometry_flow_heat_exchange.py`, `tests/test_geometry_flow_heat_exchange.py`, contract `docs/contracts/GEOMETRY_FLOW_HEAT_EXCHANGE_V1*` สองภาษา, plan/result สองภาษาชุดนี้ และ `artifacts/work121/run_a|run_b` ที่ไม่ติดตามใน Git

## การตรวจสอบ

```powershell
python -m unittest tests.test_geometry_flow_heat_exchange tests.test_repository_contract -v
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_a
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_b --replay-reference artifacts/work121/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 110/115/116 และตรวจ staged/cached diff แบบระบุไฟล์ จะ commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Adapter ทั้งสองเป็น analytic/reduced reference ที่มีขอบเขตและใช้ property synthetic สิ่งที่ไม่ทำ: arbitrary cooling geometry, turbulence, cavitation, compressibility, conjugate 3D CFD, whole-car aerodynamics, validated cooling, physical validation, push หรือแก้ประวัติ
