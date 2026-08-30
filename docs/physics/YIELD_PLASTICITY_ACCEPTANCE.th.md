# การยอมรับ Yield และ Plasticity Solver

ไฟล์ต้นฉบับภาษาอังกฤษ: `YIELD_PLASTICITY_ACCEPTANCE.md`

## ผลลัพธ์และขอบเขตข้ออ้าง

Work 042 ผ่าน declared synthetic uniaxial bilinear material-law acceptance CalculiX ให้ plastic strain เป็นศูนย์ใต้ yield, แสดง elastic-to-plastic tangent change, มี equivalent plastic strain ที่ `270 MPa`, มี residual strain หลัง unload, reverse response เป็น elastic, reaction ปิด และ internal-energy ledger สอดคล้องกับ external work

งานนี้ validate เฉพาะ numerical route ที่ประกาศ ไม่ใช่ real-alloy allowable, physical coupon validation, cyclic plasticity, fracture, fatigue, component strength หรือ vehicle safety evidence

## Law และ Fixture ที่ประกาศ

Prismatic coupon มี `L=0.1 m` และพื้นที่ `1e-4 m^2` Synthetic material ใช้ `E=70 GPa`, `nu=0.3`, `sigma_y=250 MPa` และ total post-yield tangent `Et=1 GPa` CalculiX `*PLASTIC` ต้องรับ stress เทียบ equivalent plastic strain ดังนั้น tabular hardening slope คือ

```text
H = E Et / (E - Et) = 1.0144927536 GPa
epsilon = sigma/E                         for sigma <= sigma_y
epsilon = sigma_y/E + (sigma-sigma_y)/Et for sigma > sigma_y
epsilon_p = epsilon - sigma/E
```

Absolute stress history คือ `200, 250, 270, 0, -200, 0 MPa` ครอบคลุม below-yield control, bilinear corner, post-yield loading, unload, reverse-elastic loading และ final zero load Deterministic C3D8 mesh สองระดับมี `8` และ `16` elements ความหมาย output `PEEQ` และ `ELSE` อิง CalculiX user manual

## ผลการทดลอง

| Metric ของ fine mesh | ผล | Gate |
|---|---:|---:|
| yield-onset error | `1.0145e-9` relative | `<=0.02` |
| post-yield tangent error | `5.0000e-8` relative | `<=0.05` |
| peak `PEEQ` error | `2.1739e-7` relative | `<=0.05` |
| residual-strain error | `2.1739e-7` relative | `<=0.05` |
| below-yield `PEEQ` | `0` | `<=1e-10` |
| maximum reaction residual | `1.0840e-16` relative | `<=1e-5` |
| maximum energy-ledger residual | `2.7508e-7` relative | `<=1e-4` |
| maximum last-two-mesh response change | `0` | `<=0.05` |

Analytical peak total strain คือ `0.0235714286`; residual plastic strain คือ `0.0197142857` Fine solver residual คือ `0.0197142900` การ reverse ถึง `-200 MPa` ยังเป็น elastic ภายใต้ enlarged isotropic yield surface นี่เป็น control ไม่ใช่ cyclic-plasticity validation

## Falsification review

หลักฐานสนับสนุนประกอบด้วย solver-emitted multi-step displacement, reaction, stress, strain, `PEEQ`, `ELSE`; below-yield behavior ที่ตรง, residual deformation, work-energy closure และ homogeneous response ที่ไม่ขึ้นกับ mesh Exploratory run แรกไม่ถูก admit เพราะ default print frequency ส่งทุก increment และเผย parser heading ที่ไม่ตรง จากนั้นจึง freeze output frequency และ exact heading ที่สังเกตพร้อมเพิ่ม test

ไม่มี admitted result ที่ขัดสมมติฐาน คำอธิบายทางเลือกคือ homogeneous coupon ลด stress concentration และ synthetic bilinear curve ง่ายกว่า processed real material มาก หลักฐานที่ขาดคือ sourced material allowable, physical coupon, temperature/rate effect, cyclic hardening/ratcheting, multiaxiality, fracture และ fatigue มีความมั่นใจสูงเฉพาะ local synthetic uniaxial solver-law route นี้

## การรันซ้ำ

```powershell
.\scripts\run_work042.ps1
py -3.14 -m unittest tests.test_plasticity_acceptance -v
```

Machine-readable evidence อยู่ที่ ignored `artifacts/work042/experiment_summary.json`; accepted clean replay ต้องระบุ committed implementation และ clean worktree
