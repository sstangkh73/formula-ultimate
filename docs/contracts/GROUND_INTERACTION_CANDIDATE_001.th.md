# สัญญา Ground-Interaction Candidate 001

ไฟล์ต้นฉบับภาษาอังกฤษ: `GROUND_INTERACTION_CANDIDATE_001.md`

## ขอบเขตคำอ้าง

สัญญานี้ยอมรับ specimen สำหรับตรวจซอฟต์แวร์/CAD แบบจำกัดหนึ่งชุด ไม่ได้บังคับ topology ทั่วไปของรถ และไม่ได้ validate suspension, wheel, tyre, steering system, brake, bearing, ชิ้นส่วนการผลิต, fatigue life, safety case หรือพฤติกรรมทางกายภาพ

คำตัดสิน candidate ต้องยังเป็น `not_admitted_synthetic_evidence` และ `design_use_allowed=false` ตราบใดที่สายหลักฐานวัสดุ/กระบวนการเป็น `synthetic_verification` ผลซอฟต์แวร์ที่ผ่านไม่สามารถข้าม evidence gate นี้ได้

## Candidate ที่ตรึงไว้

Candidate มี solid แยกห้าชิ้น:

1. `structural_mount`: Work 081 `bracket_001.step` แบบ exact ซึ่งใช้โดย structural witness ของ Work 082 ด้วย
2. `guide_frame`: guide ตายตัวพร้อม pin ที่เข้าสู่ cylindrical interface ของ mount
3. `carrier`: carrier แบบ clevis-like ที่เลื่อนได้
4. `axle`: ชิ้นถ่ายแรง/แรงบิด
5. `contact_roller`: ชิ้นสัมผัสวงแหวนที่หมุนได้

นี่คือ candidate หนึ่งแบบที่เลือกเพื่อให้ตรวจสอบได้ admissible topology ทั่วไปของ evaluator ไม่ได้ถูกจำกัดให้อยู่ในรูปแบบนี้หรือสถาปัตยกรรมรถแบบดั้งเดิม

## สัญญา Kinematics

กรอบ SI ใช้ `+x` ไปข้างหน้า `+y` ไปทางซ้าย และ `+z` ขึ้นบน วัตถุห้าชิ้นมี spatial DOF ที่ยังไม่ถูกจำกัด `30` DOF ข้อต่อ fixed, fixed, prismatic, fixed และ revolute ให้แถวข้อจำกัดอิสระที่ประกาศ `6 + 6 + 5 + 6 + 5 = 28` จึงเหลือ `2 DOF` พอดี:

- การเลื่อนแนวดิ่งของ carrier-group จาก `-0.007 m` ถึง `+0.007 m`
- การหมุน contact roller รอบ `+y`

CAD runner ประเมินปริมาตรตัดกันของ B-rep exact และระยะห่างของ forbidden pair ที่ตำแหน่งต่ำสุด อ้างอิง และสูงสุด ไม่ปิดบังหรือซ่อม intersection ค่า maximum overlap คือ `1e-12 m3` และ minimum forbidden clearance คือ `0.0005 m`

## สัญญาแรง โมเมนต์ แรงบิด และพลังงาน

แรงจากพื้นที่กระทำต่อ candidate ในกรณีอ้างอิงคือ `[320, 180, 1250] N` ที่ `[-0.04, 0, -0.139] m` องค์ประกอบ `+z` ต้องเป็นบวกอย่างเคร่งครัด กราฟแรงจากพื้นต้องมีเส้นทางต่อเนื่องหนึ่งเส้นพอดี:

`contact_roller -> axle -> carrier -> guide_frame -> structural_mount`

กราฟขับ/เบรกต้องมีเส้นทาง `axle -> contact_roller` หนึ่งเส้นพอดี แรงบิดขับอ้างอิงคือ `42 Nm` ที่ `80 rad/s` นาน `0.25 s` ด้วยประสิทธิภาพ `0.92` แรงบิดเบรกอ้างอิงคือ `-30 Nm` ซึ่งต้านการหมุนทิศบวก แรงและโมเมนต์ปฏิกิริยาถูกระบุชัด และงานขับถูกแบ่งเป็นงานที่ส่งออกกับ loss ค่า force และ moment residual แต่ละค่าต้อง `<=1e-5` และ energy residual ต้อง `<=1e-4` ค่าที่ไม่ finite ประสิทธิภาพนอก `[0,1]` หรือแรงตั้งฉากอ้างอิงไม่เป็นบวกจะ fail closed

## หลักฐานรูปทรงและโครงสร้าง

CadQuery `2.8.0` สร้างสี่ชิ้นและนำเข้า mount ที่ตรึงแบบ exact ทุกชิ้นถูกส่งออกเป็น canonical STEP byte stream Subsystem STEP ต้องนำเข้าเป็น valid solid แยกห้าชิ้น FreeCAD นำเข้า STEP ของแต่ละชิ้นแบบ exact และ assembly อย่างอิสระ บันทึก validity/volume/bounds และบันทึกเอกสาร FCStd ที่มี named `Part::Feature` ห้าชิ้น ไม่อนุญาต healing call หรือ hidden geometry repair

Structural witness ผูกแบบ exact-identity กับผล Work 082 `3b5d82a7a60f68a8420f1fe5bea9915e494cc29f98bf568e1862903e929b805a` และ bracket STEP `b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89` หลักฐานนี้ครอบคลุมเพียง bracket และ load family นั้น ตัวตนวัสดุ synthetic ต้องยังเป็น `72a1b5527e4aede10c6de73523c54835f11458f80100c6383d2a304d4d912097` พร้อม `design_use_allowed=false`

## Falsification controls ที่บังคับ

- `mirror`: แรงแนวข้างและมุมทิศแรงเปลี่ยนเครื่องหมาย ส่วนแรงตั้งฉากคงเดิม
- `rigid_no_travel`: การเลื่อนที่ประกาศเป็นศูนย์และ mobility ลดเหลือหนึ่ง
- `disconnected_mount`: จำนวน force path และแรงที่ส่งเป็นศูนย์ สถานะเป็น `dnf`
- `blocked_translation`: ระยะเคลื่อนที่จริงเป็นศูนย์และสถานะ degraded
- `seized_rotation`: ความเร็วเชิงมุมและกำลังกลที่ส่งเป็นศูนย์
- `broken_torque_path`: จำนวน torque path และแรงบิดที่ส่งเป็นศูนย์
- `undersized_capacity`: utilization ต้องมากกว่าหนึ่งและสถานะเป็น `dnf`
- `contact_loss`: แรงสัมผัสตั้งฉาก แนวยาว และแนวข้างเป็นศูนย์ สถานะเป็น `dnf`

Control ทุกตัวต้องยังอยู่ครบและให้ผลที่วัดได้ตาม preregistration การขาดหายหรือไม่มีผลเชิงสาเหตุทำให้ evaluation ไม่ผ่าน

## Replay และความหมายของการล้มเหลว

รันใหม่สองรอบเปรียบเทียบ declaration, STEP ทุกชิ้น, assembly STEP, geometry manifest, canonical FreeCAD report, evaluation, structural evidence และตัวตน result เวลาใน STEP ถูกแทนด้วยค่าคงที่ `1970-01-01T00:00:00`; ไม่ใช้ไบต์ FCStd เป็นหลักฐาน deterministic เพราะ metadata ของ container อาจเปลี่ยนได้ canonical FreeCAD measurement report คือตัวตน replay สำหรับ FCStd witness

Schema extension, ตัวตนเปลี่ยน, solid ขาด, shape invalid, การละเมิด clearance/overlap, reference path ขาด, ledger residual เกิน gate, การ relabel หลักฐาน synthetic, fault control ที่ไม่เกิดผลเชิงสาเหตุ หรือ replay mismatch ใด ๆ จะ fail closed ไม่มีการซ่อมรูปทรงตามผลลัพธ์
