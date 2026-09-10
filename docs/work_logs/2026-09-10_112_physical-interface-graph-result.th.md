# ผล Work 112: กราฟ Physical Interface

ต้นฉบับภาษาอังกฤษ: `2026-09-10_112_physical-interface-graph-result.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 112 พัฒนา typed multigraph ที่มี 6 terminals และ 4 edges ผูกกับ regions ของ Work 108 รักษา mechanical paths ขนานสองทางและ physical-domain components ที่แยกกันสามส่วน Identifier-only renaming ให้ identity เดิม ส่วน source/sink reversal, การลบ parallel edge หนึ่งเส้น, owner regrouping และ disconnection ยังแยกออก

Result SHA-256 คือ `45e821a075f98258a8fbe5c1a954def9e12b561db1c0e5f1d8f6d21ffe901b37`; `run_b/replay.json` ตรงทุกบิต Maximum exchange residual เท่ากับ `0` Corpus มี `6` terminals, `4` edges, parallel edge เพิ่ม `1` เส้น และ `3` connected components Controls ด้าน unit, surface, rigid/moving และ exchange imbalance ถูกปฏิเสธ Unambiguous split transfer เปลี่ยน region และ invalidate dependent evidence; ambiguous split รักษา binding และส่ง invalidation เมื่อมี 9 terminals identity รายงาน `unresolved` อย่างชัดเจนเหนือขอบเขตแปด

ไฟล์ที่เปลี่ยน: implementation, config, runner และ tests ตาม proposed paths ของ Work 112; contract `PHYSICAL_INTERFACE_GRAPH_V1` สองภาษา; และ plan/result นี้สองภาษา ส่วน `artifacts/work112/run_a|run_b` เป็น ignored

## Validation

```powershell
python -m unittest tests.test_physical_interface_graph -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/assembly/physical_interface_graph.py scripts/development/run_physical_interface_graph.py
# exit 0
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_a
# exit 0; result SHA-256 ตามข้างต้น
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_b --replay-reference artifacts/work112/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_spatial_material tests.test_physical_interface_graph tests.test_repository_contract -v
# exit 0; ผ่าน 19 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับไฟล์ Work 112 ที่ประกาศไว้ 10 ไฟล์
git diff --cached --check
# exit 0
```

Identity bound และ declared surface frames จำกัดการ generalize; ไม่อ้าง contact mechanics, general mechanism discovery หรือ physical validation รายงาน verified commit hash ใน final handoff
