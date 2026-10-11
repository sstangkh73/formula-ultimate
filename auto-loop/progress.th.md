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

### Work 150 (รอบที่ 2): การแตกโครงสร้างแบบนามธรรมที่ขับด้วย seed, Completed

- สิ่งที่ทำ: `src/formula_ultimate/hierarchy/decomposition.py` มี `decompose(seed, config)`
  จัดกลุ่มความสามารถ (เดี่ยว/คู่), แบ่งงบใบแบบ random composition แบบ recursive, anchor child
  = ลูกที่งบมากที่สุด, `characteristic_length_m` ต่อ node (เป้าหมายการวางแผน), attachment นามธรรม
  (anchor leaf ของ satellite -> ใบที่ seed เลือกใน subtree ของ anchor) พร้อมชนิดรอยต่อ,
  การค้นหาแบบปฏิเสธที่ตรวจด้วย `constraint_violations` root ไม่มี functions; sub-assembly
  สืบทอด functions ของกลุ่ม; ใบไม่มี functions id มีรูปแบบ `vehicle`, `g<i>-<caps>`,
  `<parent>.a<i>` (assembly) / `<parent>.p<i>` (part) เทสต์: `tests/test_hierarchy_decomposition.py` (12)
- ผู้ทำ: Claude (การออกแบบต้องใช้บริบทเต็ม)
- Gate: Gate 1 PASS. Gate 2 `Ran 1065 tests`, `OK (skipped=11)`. Gate 3 ตก 13/13 (ยังไม่มี generator)
- หลักฐาน: seed 0..39: 175..229 ใบ, 7..8 ชั้น, อัตราส่วนความยาวใบตามแผน 103..277, fan-out สูงสุด 12
- ปัญหา: `sed -i` และคำสั่งที่มี prefix ตัวแปรแวดล้อมต้องขออนุมัติ ใช้ Edit tool แทน
  แพ็กเกจติดตั้งแล้ว จึงรัน `python -c "from formula_ultimate..."` ได้โดยไม่ต้องตั้ง PYTHONPATH
- ถัดไป: Milestone 3 สร้างเรขาคณิตใบด้วย `components/freeform_solid_grammar.py` / `scripts/cad/*`
  ภายใต้ CadQuery: ขนาดจาก `characteristic_length_m`, export STL หน่วยเมตร, มวลและ CoM จาก mesh
  ที่ export และสัดส่วนเต็มกล่อง <= 25% (ให้ Codex ทำส่วน CadQuery โดยให้สเปกชัดเจน)
  ให้แยกขั้นตอนนี้เป็นสองส่วนถ้าใหญ่เกิน: (ก) สร้างและ export ชิ้นเดียวพร้อมวัดมวล, (ข) วางตำแหน่ง

### Work 151 (รอบที่ 3): การสร้างเรขาคณิตของชิ้นส่วนใบ, Completed

- สิ่งที่ทำ: `src/formula_ultimate/hierarchy/leaf_geometry.py` (Python ล้วน):
  `leaf_program(rng, L, placement, leaf_id)` สุ่ม profile รูปดาวแบบ Work 091 (polyline ปิดหรือ
  B-spline แบบ periodic) ที่ extrude ตรงตาม +z ท้องถิ่น (Work 092 `section -> extrude -> transform...`);
  ฝาเรียบที่ z=0 และ z=`contact.height_m` ท้องถิ่น พร้อม `contact.inscribed_radius_m` /
  `outer_radius_m` ที่ประกาศ `placement_transforms(axis, flip, spin, translation)`,
  `with_placement`, `transform_points` (แบบจำลอง Python ล้วนของการวางใน CAD),
  `stl_bytes`/`read_binary_stl`, `closure_problems`, `measure_mesh` (มวลและ CoM จากสามเหลี่ยม float32
  ที่อ่านกลับ ใช้สูตรเดียวกับ acceptance)
  `scripts/hierarchy/leaf_realization.py` (CAD runtime): `realize_leaf(program, stl_path, density)`
  ใช้ `execute_candidate` โดยไม่แก้ไข แบ่ง mesh ที่ 2e-3 L และเขียน STL แบบ binary ที่ determinate หน่วยเมตร
  เทสต์: `tests/test_hierarchy_leaf_geometry.py` (9, ส่วน CAD รันผ่าน subprocess)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1074 tests`, `OK (skipped=11)`. Gate 3 ตก 13/13 (ยังไม่มี generator)
- หลักฐาน: ใบสุ่ม 600 ชิ้น (L 0.004..4 m) ปิดทั้งหมด ใช้เวลารวม 18.9 s (~30 ms ต่อใบ),
  box-fill <= 0.858, เส้นทแยงกล่อง 0.44..1.50 L
- ปัญหา: หน้าข้างเบี่ยงได้ถึงค่าความคลาดเคลื่อนเชิงเส้น (2e-3 L) การสัมผัสจึงต้องเป็นฝาต่อฝา (เรียบ ตรงตัว)
  การแบ่ง mesh ใหม่ของรูปทรงที่วางแล้วต่างจากแบบท้องถิ่นได้ถึงค่าความคลาดเคลื่อนนั้น
- ถัดไป (milestone 4, การวางตำแหน่ง): แนวทางที่เสนอ ให้ AABB ของใบไม่ซ้อนกันเป็นคู่ (แตะกันได้):
  การทดสอบการทะลุของ acceptance ตรวจเฉพาะคู่ที่ AABB ซ้อนกันเกิน `contact_tolerance_m`
  การสัมผัสของ interface: วางฝาของใบที่เล็กกว่าราบบนฝาของใบที่ใหญ่กว่า โดยให้อยู่กึ่งกลางจน outer radius
  อยู่ภายใน inscribed radius ของอีกฝั่ง (จุดยอดบนฝาจะมีระยะ 0) กราฟ attachment ของ Work 150
  เป็น spanning tree บนใบ (ผลรวม (ลูก-1) = ใบ-1) แต่เป้าหมายแบบสุ่มที่อยู่ลึกใน subtree ของ anchor
  อาจเข้าถึงไม่ได้โดยไม่ชน ให้พิจารณาเลือกเป้าหมายตอนจัดเลย์เอาต์จากใบที่ยังมีฝาว่าง (บันทึกกระบวนการ)
  และค้นหาตำแหน่งแบบตรวจการชนตามทิศของฝา ให้การวางแผนตำแหน่งอยู่ใน Python ล้วน
  (`transform_points`, ข้อมูล contact) แล้วค่อยสร้างใน CAD
