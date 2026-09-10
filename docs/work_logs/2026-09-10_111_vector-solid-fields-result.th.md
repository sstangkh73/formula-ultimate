# ผล Work 111: สนามเวกเตอร์ของ Solid จาก Geometry ที่สร้างขึ้น

ต้นฉบับภาษาอังกฤษ: `2026-09-10_111_vector-solid-fields-result.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และไฟล์

Work 111 ประกอบและแก้ระบบ tetrahedral แบบ three-displacement-DOF, small-strain isotropic linear-elastic บน structured reference และสนามจริงของ Work 109 ที่ส่งผ่าน Work 110 เก็บ vector displacement, tensor stress, p90 von Mises stress, recovered reactions, energy, balance residuals, conditioning proxy และ deterministic field identities Material ระบุชัดว่าเป็น synthetic และ claim ยังเป็นหลักฐาน numerical ระดับ Level-0

ไฟล์ที่เปลี่ยน: `src/formula_ultimate/structural/vector_solid_fields.py`, `config/development/vector_solid_fields_v1.json`, `scripts/development/run_vector_solid_fields.py`, `tests/test_vector_solid_fields.py`, `docs/contracts/VECTOR_SOLID_FIELDS_V1*` สองภาษา และ plan/result นี้สองภาษา ส่วน `artifacts/work111/run_a|run_b` เป็นหลักฐาน ignored

## การตัดสินใจและการพยายามหักล้าง

- Constant-strain TET4 ใช้ `Ke = V B^T D B`; triangle traction ถ่วงตามพื้นที่และ body force กระจายอย่างสอดคล้องตาม element volume
- Support nodes ตรึง translation ทั้งสามแกน Reaction มาจาก assembled residual `K u - f`; uniform assigned-reaction control ที่ hash แยกต่างหากไม่ตรงกับ recovered field
- ปริมาณ stress ที่ admitted คือ volume-weighted p90 von Mises ไม่ใช่ sharp-corner maximum
- Controls ผ่าน affine patch, rigid translation/rotation, exact inverse stiffness scaling และ causal geometry/load mutations ส่วน unsupported rigid modes, severed load path และ stiffness ศูนย์ถูกปฏิเสธ
- ปริมาณของ unfamiliar geometry เปลี่ยนตาม resolution การผ่าน last-two gate ที่ลงทะเบียนไม่แสดง asymptotic หรือ physical convergence

## หลักฐานเชิงตัวเลข

Result SHA-256: `8f057c39a1f79fa45113f86fa48d6cb199562c8ba40ad041bccb9e9c6e8a4c85` และ `run_b/replay.json` รายงาน `exact: true`

| Case / resolution (`m`) | Nodes | Tets | ปริมาณหลัก | Force residual | Moment residual |
|---|---:|---:|---:|---:|---:|
| reference / `0.04` | `16` | `18` | analytic displacement error `0.04087756582701689` | `6.284990487158661e-16` | `4.105232943528381e-16` |
| reference / `0.02` | `63` | `144` | analytic displacement error `0.024271592769903552` | `2.3581991752920518e-15` | `4.3732590578852406e-16` |
| reference / `0.01` | `325` | `1152` | analytic displacement error `0.016137273749221095` | `1.006596157171345e-14` | `7.469678635014262e-15` |
| unfamiliar / `0.02` | `289` | `984` | max displacement `2.722901067165298e-8 m`; p90 `12696.135980341078 Pa` | `1.354820533070906e-15` | `3.8996688400222213e-16` |
| unfamiliar / `0.01` | `1865` | `8100` | max displacement `1.4485540999002353e-8 m`; p90 `8219.449957122448 Pa` | `1.0627066868689837e-14` | `1.7278112555075858e-15` |
| unfamiliar / `0.008` | `3220` | `14880` | max displacement `1.5494724816709918e-8 m`; p90 `8631.834378747026 Pa` | `4.4855856174795724e-15` | `1.1572425024098133e-15` |

Last-two relative changes เท่ากับ `0.06513079965248782` สำหรับ maximum displacement, `0.09063743251857388` สำหรับ compliance และ `0.04777483018440845` สำหรับ p90 stress ค่า patch, translation และ rotation errors เท่ากับ `5.1457251545698746e-20`, `1.4210854715202004e-14` และ `6.776263578034403e-20` ตามลำดับ Energy residual สูงสุด `4.319781655832243e-15`; minimum diagonal proxy อย่างน้อย `0.09848484848484801`

## Validation

```powershell
python -m unittest tests.test_vector_solid_fields -v
# exit 0; 5 tests passed
python -m py_compile scripts/development/run_vector_solid_fields.py src/formula_ultimate/structural/vector_solid_fields.py
# exit 0
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_vector_solid_fields.py --config config\development\vector_solid_fields_v1.json --output-root artifacts\work111\run_a
# exit 0; result SHA-256 8f057c39a1f79fa45113f86fa48d6cb199562c8ba40ad041bccb9e9c6e8a4c85
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_vector_solid_fields.py --config config\development\vector_solid_fields_v1.json --output-root artifacts\work111\run_b --replay-reference artifacts\work111\run_a\result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_spatial_material tests.test_freeform_material_generator tests.test_geometry_mesh_bridge tests.test_vector_solid_fields tests.test_repository_contract -v
# exit 0; ผ่าน 28 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับไฟล์ Work 111 ที่ประกาศไว้ 10 ไฟล์
git diff --cached --check
# exit 0
```

การ stage ใน sandbox ครั้งแรกสร้าง `.git/index.lock` ไม่ได้ (`Permission denied`) และ combined shell sequence รายงาน `0` ของคำสั่งถัดมา จึงไม่นับเป็นหลักฐาน จากนั้นรัน `git add` ใหม่ด้วย permission ที่จำเป็น และรัน inspection/check แต่ละคำสั่งแยกกัน โดยได้ exit `0` ทุกคำสั่ง รายงาน verified commit hash ใน final handoff

## ข้อจำกัดและงานถัดไป

Boundary ที่ไม่คุ้นเคยเป็น voxel steps และ six-tetra cells สม่ำเสมอโดยโครงสร้าง Diagonal ratio ไม่ใช่ full condition number, ยังไม่พิสูจน์ stress convergence และยังไม่มี independent production solver หรือ experiment cross-check Nonlinear/contact/plastic/fatigue response, certified material data, real load cases, manufacturing และ physical validation อยู่นอกขอบเขต Work 113 และ Work 115 ใช้ fields ต่อได้เฉพาะภายใต้ contract นี้และ limitations ที่ระบุ
