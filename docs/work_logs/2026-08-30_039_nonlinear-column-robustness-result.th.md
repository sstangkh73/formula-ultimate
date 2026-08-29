# ผลงาน 039: ความทนทานของผลเสาเชิงไม่เชิงเส้น

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_039_nonlinear-column-robustness-result.md`

สถานะ: เสร็จสมบูรณ์; execution ผ่านและ preferred hypothesis ทั้งสองข้อถูก reject

## ไฟล์ที่เปลี่ยน

- เพิ่ม Work 039 versioned config, runner, PowerShell launcher, bilingual physics report, plan/result log และ ignored solver artifact
- ขยาย nonlinear-column contract ด้วย declared `smoothstep_cubic` imperfection และ fail-closed shape dispatch
- ขยาย focused unit coverage สำหรับ independent shape และ unknown-shape rejection

## การตัดสินใจและหลักฐาน

แยก execution acceptance ออกจาก hypothesis outcome ทั้ง 18 C3D4 `NLGEOM` case เสร็จพร้อม monotonic response และ maximum reaction error `1.749e-16` ดังนั้น evidence-generating experiment ผ่าน Fixed absolute-load schedule แสดง medium-to-fine eigenmode change `1.548%`, `3.639%` และ `8.653%`; ค่าสุดท้ายเกิน declared convergence limit `5%` Fine-mesh shape difference เท่ากับ `7.523%`, `10.980%` และ `13.697%` ซึ่งเกิน robustness limit `10%` ที่สอง load สุดท้าย Preferred hypothesis ทั้งสองข้อถูก reject และไม่มีการเปลี่ยน tolerance หลังเห็นผล

## Validation

Launcher attempt แรกจบด้วย exit `1` ก่อน solver ทำงาน เพราะ runner import path ไม่มี repository root แก้ path แล้ว replay focused test และไม่รับ physical result ใดจาก attempt นั้น Final command ต่อไปนี้จบด้วย exit `0`:

```powershell
py -3.14 -m unittest tests.test_nonlinear_imperfect_column -v
& .\scripts\run_work039.ps1
& .\scripts\run_work038.ps1
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts
```

Focused test ผ่าน `5/5` Work 039 ได้ complete case `18/18` Work 038 regression คืน `status=passed` Full suite ผ่าน `291/291` ใน `23.895 s`; compileall exit `0`

## ข้อจำกัดและงานถัดไป

C3D4 series สาม mesh ปัจจุบันยังไม่พอที่ load สูงสุด และ tip amplitude เท่ากันไม่ได้ทำให้ imperfection shape ต่างกันสมมูลกัน ห้ามเลื่อนไป post-buckling งานถัดไปควรเพิ่ม refinement ต่ำกว่า `1.0 mm` และ higher-order element comparison ที่ fixed absolute load Commit identity จะรายงานใน final handoff หลัง explicit staged-scope validation และ commit
