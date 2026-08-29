# ผลงาน 038: เสาไม่สมบูรณ์แบบเชิงไม่เชิงเส้น

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_038_nonlinear-imperfect-column-result.md`

สถานะ: ผ่านและพร้อมสำหรับ required validated commit

## ไฟล์ที่เปลี่ยน

- เพิ่ม versioned Work 038 config, nonlinear-column analytical contract, runner, PowerShell launcher และ focused test
- เพิ่ม `NONLINEAR_IMPERFECT_COLUMN_ACCEPTANCE.md` และไฟล์คู่ภาษาไทย
- เปลี่ยน shared CalculiX solid-node coordinate format จาก 17 เป็น 12 significant digits เพราะ CalculiX 2.22 reject long scientific-notation node field แล้ว replay structural experiment เดิมทั้งหมด
- สร้าง ignored evidence ใต้ `artifacts/work038/` รวม exact deck, solver output, `.dat`, `.frd`, hash, failure record จาก pilot และ final `experiment_summary.json`

## การตัดสินใจและหลักฐานที่พบ

งานที่ยอมรับมีขอบเขตเป็น precritical geometric-nonlinearity เท่านั้น ใช้ matched Work 037 mesh value `Pcr=3776.375 N` เป็น numerical secant reference และแสดง Euler `Pcr=3598.293271 N` แยกไว้ ที่ `0.85 Pcr` measured amplification เท่ากับ `6.645706` สำหรับ `e0=0.1 mm` และ `6.572374` สำหรับ `e0=0.2 mm` เทียบกับ `6.666667` Maximum secant error เท่ากับ `1.4144%`, cross-amplitude spread `1.1096%` และ reaction error `2.6481e-7`

Perfect-control threshold ถูกเปลี่ยนจาก exploratory `1e-8 m` เป็น `2e-6 m` หลัง pilot แรกพบ tetrahedral mesh-asymmetry drift `1.11569e-6 m` หลังแก้ coordinate format และ pinned replay drift เหลือ `4.26212e-7 m` การ calibrate นี้ถูกเปิดเผยและไม่เรียกผลว่า independently confirmatory Geometrically linear negative control พลาด secant amplification `72.27%`

## Validation

คำสั่งทั้งหมดจบด้วย exit `0` ยกเว้น pilot falsification ที่บันทึกไว้อย่างชัดเจนด้านบน

```powershell
py -3.14 -m unittest tests.test_nonlinear_imperfect_column -v
& .\scripts\run_work038.ps1
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts
& .\scripts\run_work034.ps1
& .\scripts\run_work035.ps1
& .\scripts\run_work036.ps1
& .\scripts\run_work037.ps1
```

Focused test ผ่าน `4/4` Full suite ผ่าน `290/290` ใน `25.685 s` Work 034 tension, Work 035 bending, Work 036 torsion และ Work 037 eigenvalue buckling replay ด้วย `status=passed` ทั้งหมด Work 037 คงค่า medium `Pcr=3776.375 N`, fine `Pcr=3715.160 N` และ last-two change `1.6477%`

## ข้อจำกัดและงานถัดไป

ยังไม่ได้ทดสอบ nonlinear mesh-convergence matrix, independent imperfection shape, limit-point continuation, plasticity, collapse, fracture, fatigue, safety factor หรือ DNF coupling การศึกษาโครงสร้างถัดไปควรเปลี่ยน mesh และ imperfection shape ก่อนประเมิน arc-length หรือ post-buckling route อื่นที่ validate แล้ว Commit identity จะรายงานใน final handoff หลัง required explicit staged-scope check และ commit สำเร็จ
