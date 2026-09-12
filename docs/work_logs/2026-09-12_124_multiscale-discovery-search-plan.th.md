# แผน Work 124: การค้นพบหลายสเกลและบัญชีต้นทุนเป็นธรรม

แหล่งภาษาอังกฤษ: `2026-09-12_124_multiscale-discovery-search-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

สร้าง reference การค้นหา/บัญชีหลายสเกลที่ทำซ้ำได้ โดยตรึง representation แบบ freeform จาก Work 109, task feedback จาก Work 117 และ exploratory vehicle harness จาก Work 123 รักษา archive feasible, near-feasible และ unresolved ตาม scope โดยไม่ถือ diversity เป็น novelty หรือ promote หลักฐานรถที่ยังไม่ครบ

จองทรัพยากร CAD/mesh/solver/tuning/audit ที่แบ่ง partition ก่อน execute; คิดต้นทุน failure, retry และ audit; แสดง proposal not-evaluated หลังงบหมด ตรวจ ancestry/admission hash ครบ ทำ stale cache ใช้ไม่ได้ และแยก exact decision replay จาก upstream numerical replay

## ตัวแปร control และไฟล์

- IV: search/representation policy, fidelity allocation, archive rule, coupling mode, topology/continuous shape และ seed
- DV: scoped utility/diversity, signed effect, uncertainty, archive membership, time-to-evidence, counter unknown/not-evaluated และ resource usage
- Controls: task/library/seed/hardware/budget เท่ากัน; งบหมดก่อน execute, failure ที่ถูกคิดต้นทุน, stale cache, summary ถูกแก้, appendage ไม่ทำงาน และ shape topology เดิมที่มีประโยชน์
- Success: provenance/accounting/replay ผ่าน; unknown counter ไม่เป็นศูนย์; representation audit ไม่ขึ้นกับคะแนน; continuous shape ที่เป็นประโยชน์ยัง eligible

ไฟล์ที่วางแผน: `src/formula_ultimate/search/multiscale_discovery_search.py`, `config/development/multiscale_discovery_search_v1.json`, `scripts/development/run_multiscale_discovery_search.py`, `tests/test_multiscale_discovery_search.py`, contract `docs/contracts/MULTISCALE_DISCOVERY_SEARCH_V1*` สองภาษา, plan/result สองภาษาชุดนี้ และ `artifacts/work124/run_a|run_b` ที่ไม่ติดตามใน Git

## การตรวจสอบ

```powershell
python -m unittest tests.test_multiscale_discovery_search tests.test_repository_contract -v
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_a
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_b --replay-reference artifacts/work124/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 109/117/123 และตรวจ staged/cached diff แบบระบุไฟล์ จะ commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

นี่เป็น reference ด้านบัญชี/การค้นหาที่มีขอบเขต ไม่ใช่ optimizer บังคับหรือหลักฐาน discovery สิ่งที่ไม่ทำ: อ้าง novelty จาก diversity อย่างเดียว, ประเมินทุก proposal, promote รถ, อ้างสมรรถนะที่ validate แล้ว, physical validation, push หรือแก้ประวัติ
