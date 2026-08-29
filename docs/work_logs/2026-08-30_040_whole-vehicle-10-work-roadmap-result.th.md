# ผลงาน 040: Roadmap สิบงานสู่การวิจัยรถทั้งคัน

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_040_whole-vehicle-10-work-roadmap-result.md`

สถานะ: ผ่านและพร้อมสำหรับ required validated commit

## ไฟล์ที่เปลี่ยน

- เพิ่ม roadmap ภาษาอังกฤษแบบละเอียด `docs/reports/WHOLE_VEHICLE_RESEARCH_10_WORK_ROADMAP.md`
- เพิ่มไฟล์คู่ภาษาไทยแยก โดยคง identifier, equation, SI unit, numeric gate, dependency และ claim boundary
- เพิ่ม matching bilingual Work 040 plan/result record

## การตัดสินใจ

Work 040 เป็น evidence item สำหรับการเขียน roadmap ส่วน execution item สิบงานใช้หมายเลข Work 041-050 เพื่อไม่ให้การสร้าง roadmap ปะปนกับ physics implementation Work 041 ต้องแก้ near-critical convergence rejection จาก Work 039 ก่อน Work 042-046 ปิด material/interface/failure evidence; Work 047-049 สร้างและ falsify fixed whole-vehicle evaluator; Work 050 รันเฉพาะ bounded equal-budget search pilot และ readiness review

Roadmap คง topology-neutral และไม่บังคับ conventional vehicle layout ทุก execution item กำหนด independent/dependent variable, control, falsification, implementation output, numeric completion gate และ non-claim หาก gate ไม่ผ่านต้องสร้าง remedial work item ใหม่ ห้ามผ่อน tolerance เงียบ ๆ

## Validation

Final validation command จบด้วย exit `0`:

```powershell
$en=(rg -n '^## Work 0(4[1-9]|50) ' docs/reports/WHOLE_VEHICLE_RESEARCH_10_WORK_ROADMAP.md | Measure-Object).Count
$th=(rg -n '^## Work 0(4[1-9]|50) ' docs/reports/WHOLE_VEHICLE_RESEARCH_10_WORK_ROADMAP.th.md | Measure-Object).Count
if ($en -ne 10 -or $th -ne 10) { throw "Expected 10 work headings per language; en=$en th=$th" }
py -3.14 -m unittest tests.test_repository_contract -v
git diff --check
```

ไฟล์ทั้งสองภาษามี execution heading exactly `10` รายการ หมายเลข 041-050 Repository contract test ผ่าน `6/6` ใน `0.215 s`; `git diff --check` ผ่าน

ก่อนหน้านี้ display-only `rg` command ใช้ wildcard path ที่ใช้ไม่ได้บน Windows และ emit I/O error ขณะที่ command หลังจากนั้นยังรัน ผลนั้นไม่ถูกใช้เป็น final validation และถูกแทนด้วย explicit two-file fail-fast command ด้านบนซึ่งผ่าน

## ข้อจำกัดและงานถัดไป

งานนี้สร้างเอกสารเท่านั้น ไม่ได้รัน structural/material/vehicle experiment, ไม่สร้าง CAD และไม่ authorize whole-vehicle search Execution item ถัดไปคือ Work 041 Commit identity จะรายงานใน final handoff หลัง explicit staged-scope check และ commit สำเร็จ
