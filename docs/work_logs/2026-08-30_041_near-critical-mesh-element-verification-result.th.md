# ผลงาน 041: การตรวจ Near-Critical Mesh และ Element

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_041_near-critical-mesh-element-verification-result.md`

สถานะ: เสร็จสมบูรณ์

## ผลลัพธ์

การทดลองที่ประกาศรันสำเร็จ แต่สมมติฐาน convergence โดยรวมที่ต้องการพิสูจน์ถูกปฏิเสธ C3D4 last-two-mesh change คือ `0.702%`, `1.694%` และ `4.323%` ซึ่งอยู่ภายใน `5%` ทั้งหมด ความต่าง refined C3D4/C3D10 คือ `1.455%`, `3.512%` และ `9.213%`; ผลโหลดสูงสุดเกิน `5%` ดังนั้น Gate A ยังเปิดและ post-buckling promotion ยังถูก block

## ไฟล์ที่เปลี่ยน

- `config/structural/near_critical_element_verification_v1.json`
- `src/formula_ultimate/structural/element_verification.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_near_critical_element_verification.py`
- `scripts/run_work041.ps1`
- `tests/test_element_verification.py`
- `docs/physics/NEAR_CRITICAL_ELEMENT_VERIFICATION.md`
- `docs/physics/NEAR_CRITICAL_ELEMENT_VERIFICATION.th.md`
- bilingual plan/result record ของ Work 041

Ignored evidence ถูกสร้างใต้ `artifacts/work041/` และ mesh-only pilot อยู่ใต้ `artifacts/work041_pilot/`

## การตัดสินใจและหลักฐาน

- Freeze C3D10 `1.4 mm` ก่อนเห็น C3D10 solver result โดย pilot node count คือ `65,835` สำหรับ C3D4 `0.65 mm` และ `57,426` สำหรับ C3D10 `1.4 mm`
- เพิ่ม MSH2 support สำหรับ Gmsh linear/quadratic tetrahedra และ triangles, verified Gmsh-to-CalculiX C3D10 final edge-node conversion และ exact consistent TRI6 face loading
- เก็บ stress record จากหลาย integration points โดยไม่แทนค่าเงียบ ๆ
- Solver attempt แรกไม่ถูก admit เพราะการ filter buckling deck ลบ `*NODE FILE` โดยไม่ตั้งใจ จึงไม่มี FRD mode vector หลังแก้ transformation ได้รัน focused test ใหม่ และ admit เฉพาะ run ถัดมาที่หลักฐานครบ
- Execution gate, reaction closure, mode identity, compute comparability, secant check และ C3D4 refinement ผ่าน ส่วน cross-family high-load convergence gate fail ตามกติกาที่ประกาศ

## การตรวจสอบ

```powershell
py -3.14 -m unittest tests.test_element_verification tests.test_eigenvalue_buckling_acceptance tests.test_nonlinear_imperfect_column -v
# exit 0; Ran 11 tests; OK

.\scripts\run_work041.ps1
# exit 0; status=passed; convergence_hypothesis.status=rejected

.\scripts\run_work039.ps1
# exit 0; status=passed; hypothesis ที่ถูก reject ก่อนหน้ายังคง observable

py -3.14 -m unittest discover -s tests -v
# exit 0; Ran 295 tests in 19.614s; OK

py -3.14 -m compileall -q src scripts
# exit 0
```

Repository-contract check, `git diff --cached --check`, explicit commit และ clean-tree Work 041 replay จะบันทึกใน final handoff หลัง commit มีอยู่จริง

## ข้อจำกัดและงานต่อ

Strain energy ถูกระบุ `not_requested` อย่างชัดเจน เพราะ Work 041 ยังไม่มี energy parser ที่ตรวจอิสระแล้ว Memory evidence เป็น deterministic node-count proxy ไม่ใช่ process peak RSS ที่วัดจริง Comparable node count ไม่ได้พิสูจน์ discretization error เท่ากัน งานนี้ไม่มี material nonlinearity, fracture, fatigue, post-critical continuation, physical coupon หรือ whole-vehicle evidence

Roadmap เดิน Work 042 plasticity ต่อเป็น independent stream ได้ แต่ Gate A จะปิดไม่ได้จนกว่าจะมี remedial element/asymptotic refinement study แยกต่างหากเพื่อแก้หรือกำหนดขอบเขต disagreement `9.213%`
