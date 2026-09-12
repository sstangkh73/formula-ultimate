# ผล Work 113: Contact ของจุดเชื่อมแบบละเอียด

ต้นฉบับภาษาอังกฤษ: `2026-09-12_113_detailed-connection-contact-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐานเชิงตัวเลข

Work 113 สร้าง mating STEP solids แบบ deterministic และ discrete contact fields สามระดับสำหรับ threaded reference กับ segmented-ramp alternative Solid ทั้งสี่ valid และ male/female overlap แต่ละคู่เท่ากับ `0 m3` Rounded reference helix มี `8` รอบ; ทางเลือกมี engagement ramps `6` จุด

Final result SHA-256 คือ `a0b9fe19fbc9a3105a5bcac65a40d682e41a05d793d8063095e3be00afa58148`; replay ตรงทุกบิต ที่ 48 patches reference มี normal stiffness `4643562042.262461 N/m`, shear displacement `2.691898996122744e-7 m` และ maximum patch pressure `29265773.701437008 Pa` ทางเลือกได้ `923076923.076923 N/m`, `1.3541666666666667e-6 m` และ `145212606.229031 Pa` ทั้งคู่ยัง stick ที่ baseline Last-two pressure changes เท่ากับ `0.012639112850523751` และ `0.000525835058853858`; stiffness/displacement changes เป็นศูนย์ Maximum reduced-model error ใน registered stick samples เป็นศูนย์

Preload/friction ต่ำทำให้ slip ที่ capacity `240 N` Half engagement ลด reference stiffness ครึ่งหนึ่ง; clearance เพิ่ม axial displacement จาก `1.0172281535751857e-5 m` เป็น `5.017228153575186e-5 m`; reverse shear กลับทิศ displacement Joint ที่ถอดและตัดถูกปฏิเสธ

ไฟล์ที่เปลี่ยน: implementation/config/runner/test สี่ไฟล์ตามข้อเสนอ, contract `DETAILED_CONNECTION_CONTACT_V1` สองภาษา และ plan/result นี้สองภาษา หลักฐาน ignored อยู่ที่ `artifacts/work113/run_a|run_b`

## Validation และข้อจำกัด

```powershell
python -m unittest tests.test_detailed_connection_contact -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/structural/detailed_connection_contact.py scripts/development/run_detailed_connection_contact.py
# exit 0
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_detailed_connection_contact.py --config config\development\detailed_connection_contact_v1.json --output-root artifacts\work113\run_a
# exit 0; result SHA-256 ตามข้างต้น
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_detailed_connection_contact.py --config config\development\detailed_connection_contact_v1.json --output-root artifacts\work113\run_b --replay-reference artifacts\work113\run_a\result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_vector_solid_fields tests.test_physical_interface_graph tests.test_detailed_connection_contact tests.test_repository_contract -v
# exit 0; ผ่าน 23 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับไฟล์ Work 113 ที่ประกาศไว้ 10 ไฟล์
git diff --cached --check
# exit 0
```

Patch law, rounded thread และ synthetic properties ไม่ยืนยัน local flank/root stress, nonlinear solver convergence, loosening, fatigue, manufacturing หรือ physical safety รายงาน verified commit hash ใน final handoff
