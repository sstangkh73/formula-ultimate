# ผล Work 121: การไหลและแลกเปลี่ยนความร้อนจาก Geometry

แหล่งภาษาอังกฤษ: `2026-09-12_121_geometry-flow-heat-exchange-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 121 สร้าง reference internal laminar-passage และ external quadratic-drag ที่มี gate แยกกัน ตรวจ SHA-256 ของ mesh Work 110 ที่ระบุแน่นอนแล้ว; node `503` จุดให้ extents `[0.08, 0.048, 0.104] m` และ projected YZ area `0.004992 m2` Heat source จาก Work 115 ยังคง `10 W` และ material eligibility จาก Work 116 ยังคง blocked

กรณี internal ละเอียดสุด 40 segment มี Reynolds `891.4465070933691`, pressure drop `3.5411974837946705 Pa`, pumping power `1.7705987418973355e-5 W`, heat-capacity error `0.0003268634672523165`, rejected heat `10 W` และ residual `-3.4283687000424834e-13 W` กรณี far-field `2 m` ได้ drag `3.027798918144 N`, domain error `0.000256` และ force residual ศูนย์ Geometry/control mutation และ refinement สามระดับผ่านแยกกัน

Result SHA-256 คือ `6fbd7cd8562a7ec65d201dacaf05140194f144968c68cf9cebb6a5ad47398681`; replay ตรงกันทุกบิต ไม่พบบัคในการนำไปใช้ ไฟล์ที่เปลี่ยน: implementation/config/runner/test, contract `GEOMETRY_FLOW_HEAT_EXCHANGE_V1` สองภาษา และ plan/result สองภาษาชุดนี้ หลักฐานที่ไม่ติดตามใน Git อยู่ใต้ `artifacts/work121/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_geometry_flow_heat_exchange -v
# exit 0; ผ่าน 7 tests
python -m py_compile src/formula_ultimate/physics/geometry_flow_heat_exchange.py scripts/development/run_geometry_flow_heat_exchange.py
# exit 0
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_a
# exit 0; ได้ result SHA-256 ข้างต้น
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_b --replay-reference artifacts/work121/run_a/result.json
# exit 0; replay ตรงกันทุกบิต
python -m unittest tests.test_geometry_mesh_bridge tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_geometry_flow_heat_exchange tests.test_repository_contract -v
# exit 0; ผ่าน 28 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับ 10 ไฟล์ที่ประกาศสำหรับ Work 121
git diff --cached --check
# exit 0
```

ทั้งสอง scope ใช้ reduced analytic law และ property/closure แบบ synthetic ความสำเร็จ internal ไม่ยืนยัน external flow หรือ whole-car aerodynamics ส่วน turbulence, cavitation, compressibility, conjugate CFD, validated cooling และ physical validation ยัง unresolved จะรายงาน commit hash ที่ตรวจแล้วในสรุปสุดท้าย
