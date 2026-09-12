# ผล Work 124: การค้นพบหลายสเกลและบัญชีต้นทุนเป็นธรรม

แหล่งภาษาอังกฤษ: `2026-09-12_124_multiscale-discovery-search-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 124 สร้างบัญชี reserve-before-execute สำหรับ policy score-first และ representation-balanced ที่ได้รับ library แปด candidate, paired seed, hardware opportunity และ partition budget เท่ากัน ทั้งสอง policy คง unknown count `3`; candidate `c7` ถูกระบุ `not_evaluated_budget_exhausted` ชัดเจน Failed solver attempt และ retry ของ `c4` ถูกคิดต้นทุน และ score-independent audit ครอบคลุม representation field กับ B-rep

Admission SHA-256, cache invalidation ที่รวม dependency, tamper rejection, effect ศูนย์ของ inactive appendage และ continuous shape topology เดิมที่มีประโยชน์ผ่านทั้งหมด Work 123 ยังคงบล็อก vehicle promotion Result SHA-256 คือ `8b2cc7908fc4e33a7ab128d3e0e10bcabc3159304ab09ee8b81f6bda9888a887`; exact decision replay ผ่าน ไม่พบบัคในการนำไปใช้

ไฟล์ที่เปลี่ยน: implementation/config/runner/test, contract `MULTISCALE_DISCOVERY_SEARCH_V1` สองภาษา และ plan/result สองภาษาชุดนี้ หลักฐานที่ไม่ติดตามใน Git อยู่ใต้ `artifacts/work124/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_multiscale_discovery_search -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/search/multiscale_discovery_search.py scripts/development/run_multiscale_discovery_search.py
# exit 0
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_a
# exit 0; ได้ result SHA-256 ข้างต้น
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_b --replay-reference artifacts/work124/run_a/result.json
# exit 0; exact decision replay ผ่าน
python -m unittest tests.test_freeform_material_generator tests.test_architecture_part_feedback tests.test_coupled_vehicle_transient tests.test_multiscale_discovery_search tests.test_repository_contract -v
# exit 0; ผ่าน 30 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับ 10 ไฟล์ที่ประกาศสำหรับ Work 124
git diff --cached --check
# exit 0
```

ผล candidate เป็น fixture synthetic แบบมีขอบเขต Accounting/diversity ไม่ยืนยัน novelty, discovery, vehicle benefit หรือ physical validation จะรายงาน commit hash ที่ตรวจแล้วในสรุปสุดท้าย
