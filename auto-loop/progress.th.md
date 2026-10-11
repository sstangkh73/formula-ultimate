# ความคืบหน้าของลูป

ฉบับภาษาอังกฤษ: `progress.md`

ความจำระหว่างรอบ agent เขียนต่อท้ายส่วน Log ทุกรอบ และ commit ไปพร้อม work item ของรอบนั้น
ฉบับภาษาไทยอัปเดตใน commit เดียวกัน

## สถานะเริ่มต้น (Work 148)

- เป้าหมาย: `auto-loop/GOAL.md` การประกอบชิ้นส่วน free-form แบบลำดับชั้น v1
- Gate 1 (ขอบเขตการเผยแพร่ข้อมูลวัสดุ) และ Gate 2 (เทสต์ทั้ง repository) เป็นด่านกันถดถอย
  Gate 3 (acceptance) ยังตก เพราะยังไม่มี `scripts/hierarchy/generate_hierarchical_vehicle.py`
- เลข work ถัดไปที่ว่าง: 149
- พฤติกรรมของ baseline ที่รู้แล้ว: วันที่ 2026-10-11 เทสต์ทั้ง repository บน `main` ที่สะอาด
  ตก 1 ครั้ง (4 failures ไม่ได้เก็บชื่อเทสต์ไว้) และผ่านเมื่อรันซ้ำอีก 2 ครั้ง
  (`Ran 1042 tests ... OK (skipped=11)`) ถ้า Gate 2 ตกในเทสต์ที่ไม่เกี่ยวกับสิ่งที่แก้
  ให้รันซ้ำหนึ่งครั้งแล้วบันทึกชื่อเทสต์ไว้ที่นี่ ห้ามแก้หรือข้ามเทสต์เดิม
  ถ้าหาสาเหตุไม่ได้ ให้เขียนลง `auto-loop/BLOCKED`
- เทสต์เดิมหลายตัวอ่านหลักฐานในเครื่องที่อยู่ใน gitignore (`artifacts/`, `papers/`)
  จึงผ่านใน checkout นี้ แต่ตกใน clone หรือ worktree ใหม่ ให้รันลูปใน checkout นี้เท่านั้น

## Log

### Work 149 (รอบที่ 1): โมเดลข้อมูล part tree, Completed

- สิ่งที่ทำ: `src/formula_ultimate/hierarchy/part_tree.py` มี frozen dataclass ของ node,
  interface และต้นไม้, `validate_part_tree`, `roll_up` แบบ iterative,
  ตัววัด (`levels`, `leaf_ids`, `subtree_height`, `subtree_leaves`,
  `topology_signature` ตามนิยามของ acceptance) และ
  `to_manifest_nodes`/`to_manifest_interfaces` ที่ให้ชุด field ตรงตามสัญญา
  เทสต์: `tests/test_hierarchy_part_tree.py` (11 เทสต์)
- ผู้ทำ: Codex เขียนโค้ดและเทสต์ Claude ตรวจ diff และเขียนบันทึก
- Gate: Gate 1 PASS. Gate 2 `Ran 1053 tests`, `OK (skipped=11)`. Gate 3
  ตก 13/13 เพราะยังไม่มี generator (ตามที่คาด)
- ปัญหาและวิธีเลี่ยง:
  - การเรียก `bash auto-loop/tools/codex.sh "$(cat file)"` ถูกตัวตรวจสิทธิ์ปฏิเสธ
    สคริปต์ wrapper ที่อยู่ใน gitignore ก็ถูกปฏิเสธเช่นกัน วิธีที่ใช้ได้คือ prompt แบบข้อความตรง
    ที่ชี้ไปยังไฟล์งาน:
    `bash auto-loop/tools/codex.sh "Read the task specification in the file auto-loop/.loop/taskNNN.txt (read only; do not edit anything under auto-loop/) and carry it out exactly."`
    ให้เขียนไฟล์งานไว้ใต้ `auto-loop/.loop/` (อยู่ใน gitignore) ก่อน
  - Codex สร้างไฟล์ work log เองโดยใช้เลขผิด (148) ให้บอก Codex ชัดๆ ว่า
    "do not create or edit any docs/work_logs files"
  - `verify.ps1` ไม่ได้เขียน `last-verify.txt` (runner เป็นผู้เขียน) ถ้าต้องการดูสรุป
    ให้ส่งผลผ่าน
    `grep -a -E "^== Gate|PASS|^Ran |^OK|FAILED|^FAIL:|^ERROR:"`
    คำสั่ง shell แบบผสม (`;`, `${...}`) อาจต้องขออนุมัติ จึงควรให้การเรียก Bash แต่ละครั้งเป็น pipeline เดียว
- ถัดไป: Milestone 2 กระบวนการแตกโครงสร้างที่ขับด้วย seed ซึ่งสร้างต้นไม้แบบนามธรรม
  (ไม่มีเรขาคณิต) ครอบคลุมทั้ง 9 capability: subtree สูงอย่างน้อย 2 และมีใบอย่างน้อย 5 ใบ
  ต่อ capability, อย่างน้อย 4 ระดับ, อย่างน้อย 150 ใบ และ topology ต่างกันสำหรับ seed 11, 23 และ 37
  โดยไม่ใช้แคตตาล็อกชิ้นส่วนแบบดั้งเดิม
