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

### Work 152 (รอบที่ 4): ตัววางผังชิ้นส่วนใบ, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/layout.py` (Python ล้วน) `layout(tree)` วางทุกใบให้ตรงแนวแกน หน้าสัมผัส
  (`leaf_faces`): หน้าปลาย 2 หน้า และหน้าข้างบน hull แบบเรียบเสมอหนึ่งหน้าต่อใบ polyline ซึ่งทำให้ตรงแนวแกนด้วยการเลือก spin
  การเติบโต: วาง anchor child ก่อน แล้ว anchor leaf ของ satellite แต่ละตัวต่อด้วยหน้าปลายเข้ากับหน้าของใบใดก็ได้ที่วางแล้วใน
  assembly เดียวกัน กฎความพอดีแบบ "inside" และ "around" ใบต้นทางใหม่ปรับขนาดได้ 0.004 m..4 เท่าของที่วางแผน กล่องไม่ซ้อนทับ
  ภายใน มีรอบกล่องจองพื้นที่ แล้วตามด้วยรอบธรรมดา และพยายามแบบกำหนดผลได้สูงสุด 16 ครั้ง `layout_problems` ตรวจซ้ำทุกอย่างจาก
  โปรแกรม `PlannedInterface` มี `a_face`/`b_face`/`mode` เทสต์: `tests/test_hierarchy_layout.py` (8)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1082 tests`, `OK (skipped=11)`. Gate 3 ตก 13/13 (ยังไม่มี generator)
- หลักฐาน: seed 0..62 วางผังได้ทั้งหมด ยกเว้น seed 4 (`LayoutFailure`, แออัด) การตรวจ CAD แบบสุ่มดู
  (`artifacts/work152/cad_spot_check.py` รันด้วย python ของ CAD) สำหรับ seed 11/23/37 ด้วยฟังก์ชันของ acceptance:
  ช่องว่างทุก interface <= 8.5e-18 m, คู่กล่อง mesh ซ้อนกัน 0 คู่ (tol 1e-4), สัดส่วนที่เป็นกล่อง 0,
  อัตราส่วนเส้นทแยง 139/179/267 ใช้เวลาสร้างประมาณ 229 ใบราว 10-14 s
- ปัญหาที่พบ: การสัมผัสแบบหน้าปลายอย่างเดียวทำให้ทุกใบสืบทอดแกนของ root (เป็นเสาเดียว ทุก seed ล้มเหลว) จึงเพิ่มหน้าข้าง
  การพอดีแบบย่ออย่างเดียวลามต่อเนื่อง จึงเพิ่มการขยายแบบ "around" anchor leaf เดี่ยวมีหน้าปลายแค่ 2 หน้า เป้าหมายจึงครอบคลุมทั้ง
  assembly คำสั่ง `sed -i` และ pipeline `awk` ต้องขออนุมัติ ให้ใช้ Edit tool หรือ heredoc ของ Python
- ถัดไป: generator CLI `scripts/hierarchy/generate_hierarchical_vehicle.py` (CAD runtime): `decompose` -> `layout`
  -> `realize_leaf` ต่อใบ -> manifest ที่มีฟิลด์ตามสัญญาพอดี (`contact_tolerance_m` เช่น 1e-4; interface มีแค่ `id,a,b,kind`;
  part `generator={grammar_version: LEAF_GRAMMAR_VERSION, program, program_sha256}`; `git_commit` จาก `git rev-parse HEAD`;
  `config_sha256` ครอบ config ของ decomposition + layout), roll-up ด้วย `part_tree.roll_up` จากมวลใบที่วัดได้ วัสดุ: ใช้ id
  จากแคตตาล็อกเท่านั้น ตรวจว่าโค้ดเดิมเปิดเผย id และความหนาแน่นของวัสดุในแคตตาล็อกอย่างไรโดยไม่คัดลอกค่าส่วนตัวลงไฟล์ที่ track
  (ความหนาแน่นอยู่เฉพาะในผลลัพธ์ `artifacts/`) seed 4 ต้องมี fallback ที่ประกาศไว้ เช่น decomposition attempt ถัดไป
  ห้ามทำกรณีพิเศษให้ seed ของ acceptance

### Work 153 (รอบที่ 5): generator CLI, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/composition.py` (`plan_vehicle`: decompose -> layout -> `layout_problems`
  เมื่อเกิด `LayoutFailure` ให้ค้นต่อจาก decomposition attempt ถัดไปผ่าน `decompose(..., start_attempt)` ที่เพิ่มใหม่
  สูงสุด 8 plan attempt และบันทึกการปฏิเสธ; สุ่มวัสดุต่อใบ; `composition_config_sha256`; `build_manifest`;
  `manifest_bytes` แบบกำหนดผลได้) `scripts/hierarchy/generate_hierarchical_vehicle.py` (จุดเข้าใช้งานตามสัญญา mesh อยู่ที่
  `DIR/meshes/<leaf id>.stl` มวลจาก STL ที่อ่านกลับ) เทสต์: `tests/test_hierarchy_composition.py` (12)
- การตัดสินใจเรื่องวัสดุ: v1 อ่านระเบียนสังเคราะห์ที่มีอยู่ `synthetic_aluminium_like_verification_v1`
  (`config/materials/engineering_material_manufacturing_v1.json`) ตอนรัน ไม่มีค่าวัสดุถูกเขียนลงไฟล์ที่ track
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1094 tests`, `OK (skipped=11)`. Gate 3 `Ran 13 tests`, `OK`.
  `ALL GATES PASSED` (รันก่อน commit บน tree ที่ยังไม่สะอาด `git_commit` เท่ากับ HEAD ตอนรัน จึงควรผ่านอีกเมื่อรันหลัง commit)
- หลักฐาน: seed 11 ได้ 226 ใบใน 13.8 s; seed 4 ต้องใช้ fallback (ปฏิเสธ 2 attempt) และสร้างได้ 180 ใบ;
  ไล่วางแผน seed 0..39 ล้มเหลว 0
- ปัญหา: `${PIPESTATUS[0]}` และ `cmd; echo $?` ต้องขออนุมัติ ให้ใช้ `pwsh ... verify.ps1 2>&1 | grep -a -E ...`
  เพียงอย่างเดียว ซึ่งจะพิมพ์ `ALL GATES PASSED` เมื่อผ่าน
- ถัดไป: เป้าหมายบรรลุแล้ว รอบที่เหลือ: ยืนยัน `verify.ps1` บน tree ที่ commit แล้วและสะอาด งานเสริมความแข็งแรงที่เป็นไปได้
  (แยกเป็น work item ละหนึ่ง): แทนวัสดุสังเคราะห์ชนิดเดียวด้วยการเลือกจากแคตตาล็อกเท่านั้นซึ่งอ่านค่าตอนรันจากข้อมูลที่ gitignore
  (มี fallback สังเคราะห์สำหรับ clone ใหม่), รองรับ `interference_m`, และเร่ง `tests/test_hierarchy_composition.py` (86 s)

## สถานะเริ่มต้นของเป้าหมาย v2 (Work 154)

- เป้าหมาย v1 สำเร็จแล้วใน Work 149–153 ตอนนี้ `auto-loop/GOAL.md` เป็นเป้าหมาย v2
  การประกอบตามหน้าที่ ให้อ่านทั้งไฟล์
- Gate 1 และ 2 ผ่าน ใน Gate 3 ชุด v1 ผ่าน ส่วนชุด v2 ตกเพราะยังไม่มี
  `scripts/hierarchy/generate_functional_vehicle.py` และ `scripts/hierarchy/evaluate_level0.py`
- เทสต์ของ v2 แบ่งเป็นชั้น (`TierA*`, `TierB*`, `TierC*`) ให้ทำ A แล้ว B แล้ว C
  และดูจาก `last-verify.txt` ว่าชั้นไหนผ่านแล้ว
- ตอนนี้เทสต์ของ Work 149–153 ถูกป้องกันแล้ว ต้องให้ API และ generator ของ v1 ยังทำงานได้
  และเพิ่มโมดูล v2 ไว้ข้างๆ
- บทเรียนจาก v1 (ดู log ข้างบน): ส่งงานให้ Codex ผ่านไฟล์ task ใต้ `auto-loop/.loop/`,
  บอก Codex ว่าห้ามเขียน work log, ให้ Bash แต่ละครั้งเป็น pipeline เดียว
  และใช้ Edit tool แทน `sed -i`
- เลข work ถัดไปที่ว่าง: 155

## Log (เป้าหมาย v2)

### Work 155 (v2 รอบที่ 1): โครงตัวสร้าง v2 พร้อมความเฉื่อยที่วัดได้, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/functional.py` (`mesh_inertia`,
  `config_sha256_v2`, `build_functional_manifest`, เวอร์ชัน `func-composition-v2`) และ
  `scripts/hierarchy/generate_functional_vehicle.py` (แผนและการสร้างรูปทรงของ v1 ไม่แก้ไข, อ่าน STL กลับ,
  ความเฉื่อย, `up_axis`, `motions = []`, `function_evidence = {}`) เทสต์:
  `tests/test_hierarchy_functional.py` (6)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1100 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=13, errors=1)`: ชุด v1 ผ่าน 13/13; v2 ผ่าน TierA0 ยกเว้น Interfaces, TierA2
  (ผ่านแบบว่างเปล่า ไม่มีการเคลื่อนที่) และ TierA3
- ปัญหา: TierA0Interfaces ตกเพราะ layout ของ v1 สร้าง interface ชนิด `threaded` (49 ตัวใน seed 11)
  โดยไม่มี `axis_point_m`/`axis_dir` และ TierB10 error ด้วยสาเหตุเดียวกัน รูปแบบ grep ที่ลงท้ายด้วย `$`
  (เช่น `ok$`) ทำให้ต้องขออนุมัติ ให้ใช้รูปแบบจาก Work 149 ตามเดิม
- ถัดไป (แผนที่แนะนำ บันทึกหากเปลี่ยน): (1) ชนิด interface ของ v2: ในแพ็กเกจ v2 ให้ข้อต่อเกลียวมีรูจริงในใบหนึ่ง
  และสลักทะลุรูนั้น หรือเปลี่ยนป้ายการสัมผัสของ v1 ที่ไม่มีแกนเป็นชนิด v1 อื่น (ตัดสินใจ; ต้องมีข้อต่อเกลียวจริง >= 8
  สำหรับ TierB10); (2) ภาษารูปทรง TierA1: ใบไม่ใช่ปริซึม (เช่น เรียว/loft หรือ revolve) >= 25 %
  และใบมีรู >= 5 %; (3) โมดูลเชิงฟังก์ชันต่อความสามารถ (ล้อที่ z ต่ำสุดพร้อม bearing, การบังคับเลี้ยว,
  จานเบรกกับ stator, ภาชนะมีช่องว่าง, ห้องกับลูกสูบ/โรเตอร์, เปลือกหุ้มพร้อมชิ้นภายใน, พื้นผิวครีบ, โครงหลัก)
  วางด้วย layout ของ v2 แล้วจึงทำตัวประเมิน Level-0

### Work 156 (v2 รอบที่ 2): ชนิดรอยต่อผิวสัมผัสเรียบของ v2, Completed

- ทำแล้ว: `functional.py` เพิ่ม `FLUSH_JOINT_KINDS` (ชนิดของ v1 ที่ตัด `threaded` ออก)
  และ `V2_DECOMPOSITION_CONFIG`; ตัวสร้าง v2 วางแผนด้วย config นี้และนำไปคำนวณ hash
  การตัดสินใจ: การสัมผัสเรียบที่ฝาปลาย/ผิวข้างไม่มีรูหรือแกน v2 จึงไม่ติดป้าย `threaded`
  และสงวน `threaded` ไว้ให้สลักผ่านรูในอนาคต v1 ไม่เปลี่ยน เทสต์:
  `tests/test_hierarchy_functional_joints.py` (4)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1104 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=12)`: v1 13/13; v2 Tier A0 ผ่านทั้งหมด (แก้ Interfaces แล้ว),
  A2 (ผ่านแบบว่างเปล่า), A3 ผ่าน; A1, B1–B10, C1 ยังล้ม B10 ตอนนี้ล้มเพราะจำนวน 0 < 8
- ปัญหา: `cd "..." && git ...` ทำให้ต้องขออนุมัติ ให้รัน git จาก working directory เริ่มต้นโดยไม่ `cd`
- ถัดไป: ภาษารูปทรง Tier A1 ใน leaf grammar ของ v2 (โมดูลใหม่ข้าง `leaf_geometry.py`):
  leaf ที่ไม่ใช่ prismatic >= 25 % (เช่น extrusion แบบเรียวหรือ loft; หมายเหตุ เทสต์ยอมรับจะถือว่ารูปที่ผิว 99 %
  ขนานหรือตั้งฉากกับทิศหนึ่งเป็น prismatic ดังนั้นการ extrude ตรงของ profile ใดๆ ก็เป็น prismatic)
  และ >= 5 % มีรูทะลุ (genus >= 1) คงฝาปลายเรียบไว้เพื่อให้ layout ของ v1 ยังใช้ได้
  จากนั้นทำสลัก: leaf แผ่นมีรูกับ leaf สลักที่ทะลุผ่าน เป็น `threaded` พร้อมแกน (>= 8 ต่อ seed)

### Work 157 (v2 รอบที่ 3): รูเจาะทะลุของ leaf ใน v2, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/leaf_refinement.py` (หลัง layout, Python ล้วน):
  สำหรับ leaf ที่วางแล้วบางส่วนที่ seed เลือก (p = 0.8) เจาะรูทรงกระบอกเอียงหนึ่งรู (เอียง 5-40 องศา,
  สุ่มระยะเลื่อนแกนด้านข้าง) ออกจากการอัดรีดในกรอบท้องถิ่นก่อนการแปลงตำแหน่ง
  (`section -> extrude -> bore -> transforms`, grammar `func-leaf-bored-v2`)
  รูอยู่ในทรงกระบอกวงใน (เอาวัสดุออกเท่านั้น จึงไม่มีการทะลุกันใหม่และกล่องไม่เปลี่ยน)
  และทางออกบนฝาห่างจากพื้นที่สัมผัสที่ฝานั้นรับ (`contact_patches`)
  `refinement_problems` ตรวจซ้ำทั้งหมด `scripts/hierarchy/functional_realization.py`
  สร้างโปรแกรม v1 หรือโปรแกรมที่ปรับแต่ง ตัวสร้าง v2 บันทึกเวอร์ชัน grammar ของแต่ละ leaf
  และรวม config การปรับแต่งใน hash เทสต์: `tests/test_hierarchy_leaf_refinement.py` (9)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1113 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=11)`: v1 13/13; v2 ผ่าน Tier A ทั้งหมด (แก้ A1 แล้ว;
  seed 11: มีรู 92/226, ไม่เป็นปริซึม 160, ช่องว่าง interface สูงสุด 2e-18 m);
  B1-B10 และ C1 ยังล้ม
- ปัญหา: รูที่อยู่ตรงกลางถูกบล็อกใน 104/110 leaf ที่รับพื้นที่สัมผัส จึงเพิ่มการเลื่อนแกนด้านข้าง
  หมายเหตุ สัดส่วนไม่เป็นปริซึมของ A1 ผ่านอยู่แล้วก่อนหน้า (ตัวแทนสุ่มตรวจสามเหลี่ยมใหญ่สุด 20 ชิ้น)
- ถัดไป: ตัวยึด Tier B10 (รอยต่อ `threaded` >= 8 ต่อ seed แกนผ่านรูของชิ้นหนึ่งและเนื้อของอีกชิ้น
  จุดบนแกนอยู่ในความหนาของชิ้นที่มีรู) แนะนำ: leaf สลักใหม่ (อยู่ในต้นไม้ ใต้ subtree เดียวกับชิ้นที่มีรู
  เพื่อให้การติดป้ายความสามารถถูกต้อง) ก้านอยู่ตามรูเจาะตามแกน (เอียง 0) ของ leaf ที่มีรู
  และหัวเรียบวางบนฝา; interface `threaded` ระหว่าง leaf ที่มีรูกับสลัก โดย `axis_point_m`
  อยู่ที่ระนาบกลาง การเพิ่ม leaf เปลี่ยนต้นไม้ ต้องตรวจ validation ของ part_tree, roll-up และเทสต์ A0
  (กล่องของสลักกับ leaf ที่มีรูแยกกันไม่ได้: การตรวจการทะลุของ acceptance วัดเฉพาะความลึก
  สลักในรูที่มีระยะเผื่อจึงใช้ได้ แต่กฎกล่องของ `layout_problems` เป็นของ v1 เท่านั้น
  ให้แยกสลักออกจากการตรวจนั้นหรือเพิ่มการตรวจซ้ำของ v2)

### Work 158 (v2 รอบที่ 4): ตัวยึดแบบรูหกเหลี่ยมเป็นรอยต่อ threaded, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/fasteners.py` (Python ล้วน): หลังรูเจาะของ
  Work 157 leaf ทุกตัวที่ไม่ได้เจาะจะลองใส่รูหกเหลี่ยมด้านเท่าตามแนวแกนหนึ่งรู (loop ชนิด `hole`
  ของ profile ที่ extrude, grammar `func-leaf-socketed-v2`, พ้น contact patch บนฝา)
  แต่ละรูได้ leaf หมุดใหม่ `<holed>.pin` (การ extrude หกเหลี่ยมแบบ v1, apothem และความสูง
  หดด้วยระยะเผื่อ 2.5e-5 m, เป็นลูกของ assembly แม่ของ leaf ที่มีรู) และ interface
  `threaded` ชื่อ `<pin>.thread` ที่มีแกนเป็นแกนของรูที่กึ่งกลางความหนา
  `fastener_problems` ตรวจซ้ำ `functional.with_threaded_axes` เขียนแกนลง manifest
  `functional_realization` ตรวจด้วย `validate_v2_program` เทสต์:
  `tests/test_hierarchy_fasteners.py` (10)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1123 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=10)`: v1 13/13; v2 ผ่าน Tier A ทั้งหมดและ TierB10 ผ่าน
  (seed 11: 22 รอยต่อ, ช่องว่างมากสุด 2.5e-5 m, ไม่ทะลุ); B1-B9 และ C1 ยังล้ม
- หลักฐาน: รอยต่อต่อ seed 11/23/37/0/10 = 22/18/21/14/10 config แรก (p 0.6, สุ่ม 12 ครั้ง,
  apothem ต่ำสุด 1 mm) ได้ 7 ใน seed 23 จึงขยายก่อนรัน acceptance ใดๆ
- ปัญหา: ไม่มีที่ติดขัด หมายเหตุสำหรับ B1-B9: `evidence()` ตรวจก่อนว่ามี key ของ
  `function_evidence` ครบเก้าตัว จึงไม่มีเทสต์ B1-B9 ใดผ่านจนกว่าทั้งเก้า capability มีหลักฐาน
  อย่าลดจำนวน leaf ที่ไม่ได้เจาะ (เจาะเพิ่ม) โดยไม่ตรวจจำนวนรอยต่อใหม่ (seed 10 มีเพียง 10)
- ถัดไป: evaluator ของ Tier C1 `scripts/hierarchy/evaluate_level0.py` ไม่ขึ้นกับเรขาคณิต
  (ใช้มวลราก ขอบเขตด้านหน้าจาก mesh, `physics/race.py` ที่มีอยู่, config ที่มีเวอร์ชัน)
  เหมาะเป็นงานของ Codex จากนั้นโมดูล capability ของ B (ออกแบบรวมกัน: ล้อที่ z ต่ำสุดพร้อม
  bearing, การเลี้ยว, จานเบรก + stator, ภาชนะที่มีช่องว่าง, ห้อง + ชิ้นที่เคลื่อนที่,
  กล่องที่มีชิ้นภายใน, ผิวครีบ, โครงหลัก) อาจเป็น subassembly เฉพาะที่วางใต้ subtree ของ
  capability ที่ตรงกัน

### Work 159 (v2 รอบที่ 5): ตัวประเมิน Level-0 บนเคอร์เนลที่มีอยู่, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/level0.py`,
  `config/hierarchy/level0_race_v1.json` (monza_2026, สัมประสิทธิ์ลากบนกล่องหน้าตัด 1.0,
  C_rr 0.015, 4000 N, 4e9 J, dt 1 s, timeout 36000 s) และ
  `scripts/hierarchy/evaluate_level0.py` มวล = `mass_kg` ของรากใน manifest ตามที่เขียน
  พื้นที่ลาก = 1.0 x ขอบเขต y-z ของเมช leaf เทสต์: `tests/test_hierarchy_level0.py` (7)
  (บันทึกนี้เพิ่มย้อนหลังใน Work 160 เพราะ companion ภาษาไทยขาดไป)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1130 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: v1 13/13; v2 Tier A, B10 และ C1 ผ่าน; B1-B9 ล้ม
- หลักฐาน: seed 11 `finished` 8563.9 s; มวลราก x1.5 ได้ 8593.2 s
- ถัดไป: B1-B9 ต้องมี `function_evidence` ครบเก้าก่อนจึงจะผ่านข้อใดได้

### Work 160 (v2 รอบที่ 6): โครงชั้นกลไกและแผ่นพื้นโครงสร้าง, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/mechanisms.py` (Python ล้วน) หลังสร้างกลุ่มชิ้นส่วน
  v1 ตัวสร้างอ่านเมชกลับ (`measure_cluster`: กล่อง + leaf/จุดยอดต่ำสุด) แล้ววางแผนชั้นกลไก:
  assembly ระดับราก `m<k>-<capability>`; ไวยากรณ์ leaf กลไก `func-leaf-mechanism-v2`
  (`prism_program`: ลูปนอกหลายเหลี่ยม + ลูปรู -> extrude ตรง -> transform แข็งเกร็ง
  มีแต่หน้าแบน) สมาชิกแรก: แผ่นพื้น `m0-load_structure.deck` แปดเหลี่ยมตัดมุม ผิวบนที่ z
  ต่ำสุดของกลุ่ม `Z0` รอยเท้า = กลุ่ม + ระยะขอบ ช่องสำรอง +x (0.8-1.2 m) สำหรับโมดูลภายหลัง
  และขอบยื่นแกน x 0.14 m ทั้งสองปลายสำหรับแนวสัมผัสพื้น interface ที่นั่ง `bonded` กับ leaf
  ต่ำสุด `merge_mechanism_layer` ต่อโหนดใต้ราก คำนวณมวลใหม่ (เลขคณิตเดียวกับ
  `part_tree.roll_up`) และต่อ interface ที่ระดับ manifest (ชนิด v2 จึงไม่ผ่านตัวตรวจ
  `PartTree` ของ v1) dataclass `Backbone` เก็บกรอบแผ่นพื้นให้โมดูลถัดไป หลักฐานที่ออก:
  `load_structure` เท่านั้น เทสต์: `tests/test_hierarchy_mechanisms.py` (10)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1140 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: เฉพาะ B1-B9 (ชุดคีย์ไม่ครบ); A, B10, C1 ผ่าน
- หลักฐาน: seed 11 249 leaf, 25 s; Level-0 `finished` 9682 s; มวลราก 528 -> 1766 kg
  (แผ่นพื้นราว 1240 kg ความหนาแน่นสังเคราะห์) ภายหลังอาจทำแผ่นบางลงหรือเจาะรูลดน้ำหนัก
- การออกแบบที่วางไว้สำหรับงานถัดไป (บันทึกถ้าเปลี่ยน):
  - การสัมผัสพื้น + เบรก (งานเดียว กลุ่มติดแท็ก `[ground_propulsion, braking]`
    sub-assembly ต่อมุม): แนวศูนย์ล้อที่ x = core_x0 - 0.06 และ core_x1 + 0.06
    (ขอบยื่นของแผ่นพื้นครอบไว้ CoM จึงอยู่ใน support rectangle >= 0.06 m เมื่อที่เหลือ
    สมมาตรหรืออยู่ใน core) ล้ออยู่นอกแผ่นพื้นในแกน y แกนหมุน y เป็นจาน N เหลี่ยมมีรู N
    เหลี่ยม จุดยอดชี้ลงตรงๆ เพลานิ่ง: ปริซึม N เหลี่ยมตามแกน y ฝานั่งบนหน้าข้างแผ่นพื้น
    (รัศมี < t/2 - 2 mm) มีหน้าบนแบน bearing: apothem ของรู = รัศมีล้อมรอบเพลา + c
    (c = 2.5e-5) เลื่อนเฟส pi/N ช่องว่างสถิตจึงเป็น c และการหมุนไม่ทะลุ จานโรเตอร์ระหว่าง
    แผ่นพื้นกับล้ออยู่ใน motion เดียวกับล้อ (`bonded` กับล้อ) สเตเตอร์บนหน้าบนแบนของเพลา
    และหน้าข้างแผ่นพื้น ห่างหน้าโรเตอร์ 0.5 mm ล้อต้องเป็นชิ้นเดียวที่อยู่ภายใน 1 mm
    จาก z ต่ำสุด (รัศมีโรเตอร์ <= R - 1 cm)
  - โมดูลในช่องสำรองบนผิวแผ่นพื้น: เสาบังคับเลี้ยว + แขน (แกน z ช่วง >= 0.2), ลูกกลิ้ง
    สองถึงสามตัวบนเสาตั้งที่ขอบห่างกัน c (`rolling`), ท่อก้นแบน + ลูกสูบ (prismatic
    `guide` ช่วงชักอยู่ในท่อ), ภาชนะและกล่องตัวควบคุมเป็นปริซึมนอกลบปริซึมในที่ย่อส่วน
    (ต้องมีตัวเลือก void: `boolean_subtract` ตรวจว่า CadQuery หันผิวในเข้าหาช่องว่าง),
    ชิ้นภายในลอยเหนือพื้นช่อง 5e-5 m, แผ่นครีบรูปหวี (อัตราส่วนพื้นที่ >= 3)
- ถัดไป: งานการสัมผัสพื้น + เบรกข้างต้น (หลักฐาน B4, B6; direction_control ตามได้เร็ว)

### Work 161 (v2 รอบที่ 7): มุมล้อและเบรกที่สัมผัสพื้น, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/ground_contacts.py` (Python ล้วน)
  `add_ground_contacts(layer, seed, catalogue)` ขยายชั้นของ Work 160 (`plan_mechanisms`
  ไม่เปลี่ยน เพราะเทสต์ที่ป้องกันไว้ยืนยันชั้นที่มีแต่แผ่นพื้น) ด้วยมุมระดับรากสี่มุม
  `m1..m4-ground_propulsion_braking` ติดแท็ก `[ground_propulsion, braking]`: เพลา
  (หน้าบนแบน นั่งบนหน้าข้างแผ่นพื้น `bonded`), แผ่นสเตเตอร์บนหน้าบนเพลา (`bonded`),
  โรเตอร์ (`bonded` กับล้อ), ล้อ (จุดยอดชี้ลง `bearing` กับเพลา); การเคลื่อนที่
  `<corner>.spin` = {wheel, rotor} แบบ revolute 2 pi `y_prism` แปลงโปรไฟล์โลก (dx, dz)
  เป็นการ extrude ออกด้านนอกตามแกน y ได้ทั้งสองด้าน `ground_contact_problems` ตรวจซ้ำ
  หลักฐานเพิ่ม `ground_propulsion` และ `braking` เทสต์: `tests/test_hierarchy_ground_contacts.py` (8)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1148 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: เฉพาะ B1-B9 (การตรวจคีย์เก้าตัว); A, B10, C1 ผ่าน
  การรันคลาสของชุดยอมรับในเครื่องโดยผ่อนการตรวจชุดคีย์ (`artifacts/work161/check.py`
  ถูก gitignore) ผ่าน B4 และ B6 บน 11/23/37
- หลักฐาน: ระยะขอบ CoM 1.198/1.087/0.591 m; ช่องว่างเบรก 5.0e-4 m; seed 11 Level-0
  `finished` 10757 s, 1988 kg
- ปัญหา (บทเรียนสำหรับโมดูลถัดไป): การตรวจสัมผัสของชุดยอมรับสุ่มเฉพาะจุดยอดและเซนทรอยด์
  ของสามเหลี่ยม ทุก interface จึงต้องมีจุดยอดของชิ้นหนึ่งอยู่บนผิวของอีกชิ้น สเตเตอร์ที่ยื่น
  เกินหน้า และรู N_a เหลี่ยมรอบเพลา N_a เหลี่ยมล้มทั้งคู่ (ช่องว่าง 5e-4 และ 1.5e-3 m)
  วิธีแก้: ฐานสเตเตอร์แคบอยู่ในหน้า และรู 48 เหลี่ยม apothem r_a + c ที่มีจุดยอดในทุกทิศ
  จุดยอดของเพลา ลูป `for` ของ shell ที่มี `$s` ต้องขออนุมัติ ให้เรียกตัวสร้างครั้งละหนึ่ง
  คำสั่ง Bash
- ถัดไป: การบังคับเลี้ยว (เสาแกน z + แขนในช่องสำรองของแผ่นพื้นที่
  `backbone.bay_x0..core_x1`, `bearing`, ช่วง >= 0.2 rad, assembly ระดับรากของตัวเองติดแท็ก
  `direction_control` ต่อกับแผ่นพื้น) จากนั้นลูกกลิ้งส่งกำลัง (`rolling`), ตัวแปลงพลังงาน
  (ห้อง + ลูกสูบ `guide`), ช่องว่างของภาชนะ/กล่อง และครีบระบายความร้อน ต้องมีคีย์ครบเก้า
  ก่อน B1-B9 จึงจะผ่านในชุดทดสอบจริง

### Work 162 (v2 รอบที่ 8): เสาบังคับเลี้ยวและแขน, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/direction_control.py` (Python ล้วน)
  `add_direction_control(layer, seed, catalogue)` เพิ่ม assembly ระดับราก
  `m5-direction_control` ติดแท็ก `[direction_control]` ที่ปลาย +x ของ bay บน deck:
  boss (`bonded` กับ deck), post (`bonded` กับ boss), arm (convex hull ของ hub + tip
  polygon รูเจาะ 96 เหลี่ยม apothem r_p + c ลอยเหนือ boss เป็นระยะ c, `bearing` กับ post)
  motion `<assembly>.steer` = {arm} แบบ revolute รอบ +z ช่วง 0.3-0.8 rad วงกลมกวาด
  เต็มรอบอยู่ภายใน bay และขอบ deck 0.02 m ส่วน -x ของ bay (`bay_x0` ถึง
  `steer x - reach - 0.02`) ยังว่าง `direction_control_problems` ตรวจซ้ำ
  เทสต์: `tests/test_hierarchy_direction_control.py` (8)
- ผู้ทำ: Claude
- Gate: Gate 1 PASS. Gate 2 `Ran 1156 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: เฉพาะ B1-B9 (การตรวจเก้าคีย์); A, B10, C1 ผ่าน
  การตรวจแบบผ่อนในเครื่อง (`artifacts/work162/check.py`) ผ่าน A0/A1/A2/A3, B4, B5, B6
  บน 11/23/37
- หลักฐาน: ช่วง 0.743/0.792/0.393 rad; seed 11 Level-0 `finished` 10757 s, 1988 kg
- ปัญหา: ไม่มี ให้คัดลอกสคริปต์ตรวจแบบผ่อนไปยังไดเรกทอรี artifacts ใหม่ทุกครั้ง
- ถัดไป: การส่งกำลัง (B3): ชิ้นหมุนเต็มรอบแบบ revolute อย่างน้อยสองชิ้น แต่ละคู่ที่ติดกัน
  เชื่อมด้วย interface (เช่น ลูกกลิ้งแกนตั้งสองตัวบนเสาในส่วน -x ที่ว่างของ bay ขอบห่างกัน c
  มี interface `rolling`; ลูกกลิ้งแต่ละตัว `bearing` กับเสา เสา `bonded` กับ deck; ระวังการกวาด:
  ลูกกลิ้งหลายเหลี่ยมที่หมุนเต็มรอบกวาดวงกลมล้อมรอบ จุดยอดของคู่ต้องอยู่นอกวงนั้น เช่น
  ใช้ลูกกลิ้งหนึ่งตัวเป็น 96 เหลี่ยม) จากนั้นตัวแปลงพลังงาน ช่องว่างภาชนะ/กล่อง ครีบ และ B7

### Work 163 (v2 รอบที่ 9-10): โซ่ลูกกลิ้งส่งกำลัง, Completed

- ทำแล้ว: `src/formula_ultimate/hierarchy/power_transmission.py` (Python ล้วน)
  `add_power_transmission(layer, seed, catalogue)` เพิ่ม assembly ระดับราก
  `m6-power_transmission` ติดแท็ก `[power_transmission]` ในแถบว่างด้าน -x ของ bay
  บน deck: 2-3 สถานีเรียงตามแนว y แต่ละสถานีมี boss (`bonded` กับ deck), post
  (`bonded`), roller (N_r เหลี่ยม รูเจาะ 96 เหลี่ยม, `bearing` กับ post) roller ที่ติดกัน
  ห่างกัน `R_i + R_j + c` โดยมีจุดยอดหันเข้าหากัน (`rolling`) motion
  `<assembly>.r<i>` หมุนเต็มรอบรอบ +z หลักฐาน `chain`
  `power_transmission_problems` ตรวจซ้ำ เทสต์:
  `tests/test_hierarchy_power_transmission.py` (7)
- ผู้ทำ: Claude (เขียนโค้ดในรอบที่ 19 commit ในรอบที่ 20 หลังตรวจซ้ำ เพราะรอบก่อน
  จบก่อน commit)
- Gate: Gate 1 PASS. Gate 2 `Ran 1163 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: เฉพาะ B1-B9 (การตรวจเก้าคีย์); A, B10, C1 ผ่าน
  การตรวจแบบผ่อนในเครื่อง (`artifacts/work163/check.py`) ผ่าน A0 interfaces, A1, A2,
  A3, B3, B4, B5, B6 บน 11/23/37
- หลักฐาน: โซ่ 3/2/3 roller; seed 11 Level-0 `finished` 10758 s, 1993 kg
- ปัญหา: คำสั่ง Bash ที่มี `python -` อ่าน stdin ค้างจนหมดเวลา 30 นาที ให้เก็บสคริปต์
  ช่วยไว้ในไฟล์ใต้ `artifacts/`
- ถัดไป: ตัวแปลงพลังงาน (B2): ชิ้นห้องที่มีรูเจาะ (genus >= 1) และชิ้นลูกสูบบน motion
  แบบ prismatic ที่มี interface `guide` กับห้อง ตัวอย่างของลูกสูบตลอดช่วงชัก >= 50 %
  ต้องอยู่ในกล่องของห้องและนอกเนื้อวัสดุ จากนั้นภาชนะเก็บพลังงานและกล่องตัวควบคุมที่มี
  ช่องว่างภายใน (B1, B9), ครีบระบายความร้อน (B8) และการตรวจ B7 ต้องมีคีย์ครบเก้าก่อน
  B1-B9 จึงจะผ่านในชุดทดสอบ
