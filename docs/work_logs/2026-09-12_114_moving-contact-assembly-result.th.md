# ผล Work 114: ชุดประกอบ Moving Contact

ต้นฉบับภาษาอังกฤษ: `2026-09-12_114_moving-contact-assembly-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 114 พัฒนา deterministic axial moving-member/contact simulation และ prescribed tangential stick/slip probe โดยใช้ reduced properties ของ Work 113 threaded reference ที่ตรงกัน Time steps ทั้งสามสร้าง opening/closing/slip events `38` รายการและ swept clearance เป็นบวก Reactions กับ impulse มาจาก penetration histories ไม่ได้กำหนดจาก input

Result SHA-256 คือ `5926e067cbe4b07d0bf90364275649f72a7ad4b4566ff204901172fdd9f1ce5f`; replay ตรงทุกบิต สำหรับ coarse/medium/fine steps maximum displacement คือ `7.087472714465673e-6`, `7.0943046957599814e-6`, `7.099179394127206e-6 m`; maximum force คือ `19216.63250943933`, `19203.781781291575`, `19196.837823792008 N`; minimum clearance คือ `4.291252728553433e-5`, `4.290569530424002e-5`, `4.2900820605872797e-5 m`; energy residual คือ `0.05055660301082888`, `0.02599497047954028`, `0.013144323898850088`

Last-two changes คือ displacement `0.000686656597417022`, force `0.0003615932308880738` และ impulse `0.00017990058869692504` Free motion ตรง analytic; rigid/moving conflict และ severed coupling ถูกปฏิเสธ; mutation ที่ลด clearance ถูกบล็อกเฉพาะกรณีเป็น collision; opening/slip ทำเครื่องหมาย reduced stick model ว่าอยู่นอกช่วง

ไฟล์ที่เปลี่ยน: implementation/config/runner/test ตามข้อเสนอ, contract `MOVING_CONTACT_ASSEMBLY_V1` สองภาษา และ plan/result นี้สองภาษา Histories แบบ ignored อยู่ที่ `artifacts/work114/run_a|run_b`

## Validation และข้อจำกัด

```powershell
python -m unittest tests.test_moving_contact_assembly -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/assembly/moving_contact_assembly.py scripts/development/run_moving_contact_assembly.py
# exit 0
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_a
# exit 0; result SHA-256 ตามข้างต้น
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_b --replay-reference artifacts/work114/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_detailed_connection_contact tests.test_moving_contact_assembly tests.test_repository_contract -v
# exit 0; ผ่าน 18 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับไฟล์ Work 114 ที่ประกาศไว้ 10 ไฟล์
git diff --cached --check
# exit 0
```

Tangential history เป็น prescribed, damping เป็น synthetic และไม่อ้าง flexible modes, full 3D collision, crash, vehicle readiness หรือ physical validation รายงาน verified commit hash ใน final handoff
