# ผล Work 148: Auto-Loop สำหรับการประกอบชิ้นส่วน free-form แบบลำดับชั้น

ฉบับภาษาอังกฤษ: `2026-10-11_148_hierarchical-composition-auto-loop-result.md`

วันที่: 2026-10-11

แผน: `2026-10-11_148_hierarchical-composition-auto-loop-plan.th.md`

Status: Completed

## ผลลัพธ์

ตอนนี้ `auto-loop/` เป็น runner ของ Claude + Codex ที่ทำตามกฎของ repository
และตั้งเป้าหมายเป็นการประกอบชิ้นส่วน free-form แบบลำดับชั้น v1 ยังไม่ได้เขียน generator
และยังไม่ได้รันลูป วัดสถานะเริ่มต้นของลูปแล้ว: Gate 1 และ 2 ผ่าน ส่วน Gate 3 ตก 13 จาก 13 เทสต์
เพราะยังไม่มี `scripts/hierarchy/generate_hierarchical_vehicle.py`

## ไฟล์ที่แก้

- `auto-loop/GOAL.md`, `GOAL.th.md`: เป้าหมาย, สัญญาของ manifest, เกณฑ์การยอมรับ 7 ข้อ,
  ขอบเขต และสิ่งที่การผ่านไม่ได้หมายความ
- `auto-loop/acceptance/test_hierarchical_composition.py`: acceptance test แบบ black box 13 ตัว
  คำนวณใหม่อย่างอิสระจาก mesh ที่ generator สร้าง ทั้ง replay, ลำดับชั้น, ความครอบคลุมของความสามารถ,
  ความปิดของ mesh, ปริมาตรและมวล, จุดศูนย์กลางมวล, สัดส่วนกล่อง, hash ของโปรแกรม,
  การสัมผัสของ interface, การทะลุกัน และความหลากหลายตาม seed
- `auto-loop/verify.ps1`: 3 gate แบบหยุดทันทีเมื่อตก (ขอบเขตข้อมูลวัสดุ, เทสต์ทั้ง repository,
  acceptance) และล้าง `FU_ACCEPTANCE_GENERATOR`
- `auto-loop/run-loop.ps1`: รันที่ root ของ repository และไม่ `git init`
  ต้องให้ tree สะอาด ไม่ยอมรันบน `main` และทำงานบน `loop/hierarchical-composition`
  hash ไฟล์ที่ป้องกัน 133 ไฟล์ (ไฟล์ของลูป, `AGENTS*.md`, `.github/`, เทสต์ทุกไฟล์ที่ track)
  ตรวจว่า branch ไม่เปลี่ยน ประวัติไม่ถูกเขียนใหม่ และ `main` ไม่ขยับ
  ไม่ stage และไม่ commit เอง ห้าม agent stage แบบเหมารวม, amend, reset, rebase, switch,
  push และใช้ web tool มี `-PreflightOnly` และ agent หยุดลูปได้ด้วยการเขียน `auto-loop/BLOCKED`
- `auto-loop/PROMPT.md`, `PROMPT.th.md`: หนึ่ง work item ที่มีเลขกำกับต่อรอบ ภายใต้ `AGENTS.md`
- `auto-loop/README.md`, `README.th.md`, `progress.md`, `progress.th.md`,
  `.gitignore`, `tools/codex.sh`
- ลบไฟล์ตัวอย่างของ template `auto-loop/src/bahttext.py` และ `auto-loop/tests/test_bahttext.py`
  (ไม่เคยถูก track)
- `.gitattributes`: `/auto-loop/tools/*.sh text eol=lf` ไม่ได้อยู่ในแผน
  เพิ่มเพราะ `core.autocrlf=true` จะ checkout `codex.sh` เป็น CRLF ทำให้ bash พัง

## การตัดสินใจ

- เป้าหมายแปลงคำขอของเจ้าของโครงการเป็นเกณฑ์ที่วัดได้ (อย่างน้อย 4 ระดับ, อย่างน้อย 150 leaf,
  ช่วงขนาดอย่างน้อย 100 เท่า, ครบทั้งเก้าความสามารถในเชิงลึก, การสัมผัสที่วัดได้, ความหลากหลายตาม seed)
  โดยไม่กำหนดรายการชิ้นส่วนแบบดั้งเดิมใดๆ
- acceptance test รันด้วย Python ของระบบและตรวจ mesh โดยตรง
  ส่วน generator รันด้วย CadQuery runtime ที่ pin ไว้ในฐานะ subprocess
- ไฟล์ข้อความสุดท้ายของ Codex ใช้นามสกุล `.txt` ไม่ใช่ `.md` เพราะ
  `tests/test_repository_contract.py` บังคับให้ `.md` ทุกไฟล์นอกโฟลเดอร์ที่ยกเว้นต้องมีฉบับภาษาไทย
  และ `auto-loop/.loop/` ไม่ได้ถูกยกเว้น
- agent commit work item ของตัวเองแบบระบุไฟล์ runner ทำหน้าที่เฝ้าและตัดสินเท่านั้น

## Validation

1. ตรวจชุด acceptance เองด้วย fixture generator ใน scratchpad (โซ่ปริซึมสามเหลี่ยมสังเคราะห์
   ฉีดผ่าน `FU_ACCEPTANCE_GENERATOR`) fixture ไม่ได้ commit
   คำสั่งของแต่ละกรณี:
   `FIXTURE_BREAK=<case> python -m unittest discover -s auto-loop/acceptance`

   | กรณี | ผล |
   |---|---|
   | valid | `OK` (13 เทสต์) |
   | open_mesh | FAIL `test_leaf_meshes_closed_and_masses_measured` |
   | wrong_mass | FAIL `test_leaf_meshes_closed_and_masses_measured` |
   | missing_cap | FAIL `test_each_capability_has_a_deep_subtree`, `test_each_capability_varies_across_seeds` |
   | penetrate | FAIL `test_interfaces_touch_and_nothing_interpenetrates` |
   | gap | FAIL `test_interfaces_touch_and_nothing_interpenetrates` |
   | nondeterministic | FAIL `test_same_seed_is_byte_identical` |
   | template | FAIL `test_whole_trees_differ_across_seeds`, `test_each_capability_varies_across_seeds` |
   | boxes | FAIL `test_not_mostly_boxes` |
   | disconnected | FAIL `test_children_of_every_assembly_are_connected` |

2. `pwsh -NoProfile -File auto-loop/verify.ps1` รันโดยตั้ง `FU_ACCEPTANCE_GENERATOR`
   เป็นคำสั่งปลอมเพื่อพิสูจน์ว่าถูกล้าง ได้ exit 3 Gate 1 ผ่าน
   Gate 2: `Ran 1042 tests in 287.832s`, `OK (skipped=11)`
   Gate 3: `Ran 13 tests`, `FAILED (failures=13)` ทุกตัวตกด้วย
   `missing: ...scripts\hierarchy\generate_hierarchical_vehicle.py`
3. PowerShell parser รายงาน 0 error สำหรับ `run-loop.ps1` และ `verify.ps1`
   และ `bash -n auto-loop/tools/codex.sh` ผ่าน
4. ลอง preflight ของ runner ใน worktree ชั่วคราวบน branch `loop/preflight-check-148`
   พร้อม commit ชั่วคราว `2e855fb` (ลบทิ้งภายหลังพร้อม worktree และ branch)
   - tree ไม่สะอาดถูกปฏิเสธ: `working tree is not clean`
   - รอบแรกพบว่าฟังก์ชันช่วยชื่อ `Git` บัง `git` แล้ววนเรียกตัวเอง (`call depth overflow`)
     จึงเปลี่ยนชื่อเป็น `Invoke-Git`
   - `-PreflightOnly -Branch loop/preflight-check-148`:
     `133 protected files hashed` verify รัน และ runner exit 0
   - branch ผิดถูกปฏิเสธ: `on branch 'loop/preflight-check-148'; switch to
     'loop/hierarchical-composition' or main first`
   - ชื่อ branch ผิดรูปแบบถูกปฏิเสธ: `Branch must be named loop/<name>`
5. รันเทสต์ทั้ง repository 3 ครั้งบนโค้ด `main` ที่ไม่ได้แก้ ครั้งที่ 1:
   `Ran 1042 tests in 354.374s`, `FAILED (failures=4, skipped=11)`
   ไม่ได้เก็บชื่อเทสต์เพราะบันทึกไว้แค่ท้าย output ครั้งที่ 2 และ 3 ผ่าน (`OK (skipped=11)`)
   ยังหาสาเหตุไม่พบ บันทึกไว้ใน `auto-loop/progress.md` เป็นพฤติกรรมที่เกิดเป็นครั้งคราวและรู้แล้ว
6. ใน worktree ใหม่ ผลคือ `FAILED (failures=3, errors=6, skipped=41)`
   ตกใน `test_design_diversity`, `test_vehicle_load_cases`, `test_whole_vehicle_baseline`,
   `test_whole_vehicle_search`, `test_paper_reviews` และ `test_part_resolution`
   ซึ่งทั้งหมดอ่าน `artifacts/` หรือ `papers/` ในเครื่องที่อยู่ใน gitignore
   เป็นช่องโหว่ของ clean checkout ที่มีอยู่ก่อนแล้ว ไม่ได้เกิดจากงานนี้
7. gate ก่อน commit: `python -m unittest tests.test_repository_contract`, ตรวจไฟล์ที่ stage
   และ `git diff --cached --check` (hash ของ commit ดูในรายงานส่งมอบสุดท้าย)

## ข้อจำกัด

- ยังไม่ได้รันลูป จึงยังไม่รู้ค่าใช้จ่ายต่อรอบและพฤติกรรมจริงของ agent
- ใช้ `--max-turns` ตาม template เดิม แต่ไม่มีอยู่ใน `claude --help` (version 2.1.293)
  จึงยังไม่ได้ยืนยัน
- การตรวจชิ้นทะลุกันสุ่มดูเฉพาะ vertex และจุดศูนย์กลาง สัดส่วนกล่องและความหลากหลายจากสาม seed เป็นตัวแทน
  การผ่าน Gate 3 คือด่าน representation ไม่ใช่การยืนยันทางฟิสิกส์
- ยังอธิบายไม่ได้ว่าทำไม baseline ตกเป็นครั้งคราว (1 ใน 3 รอบ)

## งานต่อไป

- ตรวจ `auto-loop/GOAL.md` และเกณฑ์ของ acceptance ก่อนรันครั้งแรก
- รัน `pwsh -File auto-loop/run-loop.ps1 -PreflightOnly` แล้วลองรันจริงสั้นๆ
  (เช่น `-MaxIterations 2`) เพื่อวัดค่าใช้จ่าย
- เก็บชื่อเทสต์ทุกครั้งที่ Gate 2 ตกเป็นครั้งคราว และกันเทสต์ที่พึ่ง artifact ไว้สำหรับ clean checkout
- เป้าหมายรอบหลัง: เชื่อมลำดับชั้นเข้ากับ physics Level-0 และ race kernel
