# แผน Work 115: การตอบสนอง Coupled Thermal-Solid

ต้นฉบับภาษาอังกฤษ: `2026-09-12_115_coupled-thermal-solid-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

พัฒนา transient thermal network สอง regions แบบมีขอบเขตจาก mating geometry และ contact patches ของ Work 113 threaded reference แล้วเชื่อม temperatures เข้ากับ thermal expansion, temperature-dependent elastic stiffness, joint preload และ preload-dependent contact conductance ตรึง contracts ที่ตรงกันของ Work 111 และ Work 113

ใช้ synthetic thermal properties และ prescribed boundary conductance ที่ประกาศชัด งานนี้ไม่ใช่ validated convection, radiation หรือ fluid cooling เปรียบเทียบ fully coupled, explicitly decoupled และ reduced single-temperature models ผ่าน time steps สามระดับ และ invalidate properties/reductions เมื่ออยู่นอก temperature/load ranges ที่ตรึง

## ตัวแปร controls และไฟล์

- IV: heat input, prescribed boundary conductance, contact state/area, thermal properties และ coupling time step
- DV: regional temperature, interface heat transfer, energy residual, free/constrained expansion, modulus, preload shift, contact conductance และ reduced-model error
- Controls: insulated analytic energy rise, zero-source equilibrium, free เทียบ constrained expansion, heat path ถูกถอด, interface-area mutation และ one-way decoupled response
- Success: contact area จริงได้จาก geometry parameters ของ Work 113, energy/refinement gates ผ่าน, temperature เปลี่ยน mechanics และ mechanics ส่ง conductance ที่เปลี่ยนกลับ, controls เป็นเหตุเป็นผล, invalid ranges ล้มเหลวแบบปิด และ replay ตรงทุกบิต

ไฟล์ที่วางแผน: `src/formula_ultimate/physics/coupled_thermal_solid.py`, `config/development/coupled_thermal_solid_v1.json`, `scripts/development/run_coupled_thermal_solid.py`, `tests/test_coupled_thermal_solid.py`, `docs/contracts/COUPLED_THERMAL_SOLID_V1*` สองภาษา, plan/result นี้สองภาษา และ `artifacts/work115/run_a|run_b` แบบ ignored

## Validation

```powershell
python -m unittest tests.test_coupled_thermal_solid tests.test_repository_contract -v
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_a
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_b --replay-reference artifacts/work115/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน affected regressions และ explicit staged/cached diff checks; commit ทันทีหลังทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Lumped regions ไม่แทน spatial gradients และ contact conductance เป็น uncertainty ที่ยังไม่วัด สิ่งที่ไม่ทำ: validated convection/radiation/fluid flow, thermal-stress FEA, certified properties, fatigue/loosening, vehicle cooling adequacy, physical validation, push หรือ rewrite history
