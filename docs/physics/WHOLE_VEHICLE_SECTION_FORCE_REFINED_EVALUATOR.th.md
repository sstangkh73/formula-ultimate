# ตัวประเมินทั้งคันแบบละเอียดด้วย section force

ไฟล์ต้นฉบับภาษาอังกฤษ: `WHOLE_VEHICLE_SECTION_FORCE_REFINED_EVALUATOR.md`

## ขอบเขตคำกล่าวอ้าง

Work 053 ทำให้ `project_frame6dof_plus_calculix_b31_section_force_v2` เป็น independent refined evaluator สำหรับ beam-network grammar ของ Work 047, frozen Work 048 holdout wrench และวัสดุ linear-elastic สังเคราะห์ที่ประกาศไว้ ตัวประเมินคำนวณ stiffness, deformation, reaction, section resultant, surface equivalent stress และ yield margin จาก candidate geometry และไม่ใช้ structural capacity factor ของ Work 050

นี่คือหลักฐานเชิงตัวเลขของ beam network ไม่ใช่ physical validation ของรถทั้งคัน และยังไม่พิสูจน์ local solid stress, พฤติกรรม joint จริง, nonlinear yield, fracture, fatigue life, buckling, crash response หรือ hardware safety

## เหตุผลที่ Work 052 หยุด

CalculiX B31 ขยายคานเพื่อรายงาน material stress ค่า stress จาก `*EL PRINT` ถูก sample ที่ integration point ของ expanded element ขณะที่สมการ cantilever `6 F L/b^3` เป็น extreme-fiber stress ที่โคนคาน การเทียบโดยตรงจึงเป็นการเทียบคนละตำแหน่ง เอกสาร [CalculiX beam](https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node60.html) แยก integration-point output ออกจาก section-force output และ [ตัวอย่าง cantilever](https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node20.html) อธิบาย integration-point, extrapolated-node และ section-force representation

Work 053 จึงร้องขอ `*EL FILE,SECTION FORCES` โดย resultants หกองค์ประกอบเป็นไปตาม [นิยาม component ของ CalculiX](https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node265.html): แรงเฉือนสองแกน, แรงปกติ, torque และ bending moment สองแกน สำหรับหน้าตัดสี่เหลี่ยม evaluator คำนวณ

```text
sigma_surface = |N|/A + |M1| c1/I1 + |M2| c2/I2
tau_surface   = 1.5 sqrt(V1^2 + V2^2)/A + |T| cmax/J
sigma_vm      = sqrt(sigma_surface^2 + 3 tau_surface^2)
```

หน้าตัดต่างชนิดแต่ละชุดถูกร้องขอด้วย full coupled CalculiX run แยกกัน เพื่อไม่ให้ shared-node averaging ผสมสมบัติหน้าตัด และ section-output run ทุกชุดต้อง replay displacement ตรงกัน

## ผลการทดลอง

refinement series ที่ตรึงไว้คือ B31 `4/8/16` elements ต่อ branch ที่ 16 subdivisions error สูงสุดของ analytical benchmark เมื่อรวมสอง solver และ displacement/stress เท่ากับ `3.4276%` project-frame equilibrium residual ไม่เกิน `2.2293e-11` relative ใน candidate states 54 ชุด candidate 7 จาก 9 แบบที่ promote ใน Work 050 ผ่าน holdout ทั้งสองกรณี สำหรับ 7 แบบนี้ last-two change สูงสุด `2.0489%`, fine cross-model difference สูงสุด `5.0207%`, yield margin ต่ำสุด `379.45` และ displacement สูงสุด `6.1326e-6 m`

candidate สองแบบไม่ผ่านเฉพาะ fine stress-difference gate `8%` ที่ preregister:

- `candidate-9b03158dc541df18`: stress ต่าง `16.69%` และ `17.66%`
- `candidate-372db49a7cbceba5`: stress ต่าง `32.24%` และ `33.51%`

yield margin ที่สูงไม่สามารถลบความขัดแย้งนี้ ทั้งสองแบบยังถูก reject เพราะ formulation sensitivity คือหลักฐานที่ขัดแย้งเช่นกัน

## คำตัดสินและหลักฐานที่ยังขาด

คำตัดสิน: `independent_refined_evaluator_available`; candidate set: `partially_supported` (`7/9`) ผลนี้ปิด blocker ด้านการมี evaluator แต่ไม่ได้ทำให้สอง candidate ที่ถูก reject กลับมาผ่านย้อนหลัง

สิ่งที่ยังขาดคือ solid/contact stress concentration, nonlinear material response, local buckling, fatigue calibration, vibration, crash, physical material record, manufacturing variation และ hardware test whole-vehicle pilot ถัดไปต้องรับเฉพาะ candidate ที่ผ่าน refined gate นี้และคงขอบเขตหลักฐานเดิม
