# ผล Work 087: Load Structure, Packaging และ Thermal Integration

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_087_load-structure-packaging-thermal-integration-result.md`

## สถานะและผลลัพธ์

สถานะ: Partial

งานนี้สร้างหลักฐาน integration ที่ตรวจดูได้และมีสาเหตุจาก geometry จริง โดยใช้ชิ้นส่วน exact ห้าชิ้นจาก Work 083, exact เจ็ดชิ้นจาก Work 084 และ integration solid ที่สร้างใหม่ห้าชิ้น ชุดหลักฐานมี STEP แยกชิ้นสิบเจ็ดไฟล์, assembly STEP สิบเจ็ด solid และเอกสาร FCStd ที่มี solid object ตั้งชื่อสิบเจ็ดชิ้น ไม่มีการใช้กล่องแทนชิ้นส่วนทำงานและไม่มีการซ่อม collision แบบเงียบ

Candidate ถูกตัดสินเป็น `not_admitted` อย่างถูกต้อง พบ forbidden pair ข้ามระบบที่มี overlap เป็นบวกแปดคู่ อีกหนึ่ง forbidden pair มี clearance เป็นศูนย์ และ overlap สูงสุดคือ `1.677032693654574e-05 m3` ระหว่าง `carrier` กับ `converter_rotor` นอกจากนี้ระยะเคลื่อนที่แนวดิ่งของ Work 083 ทำให้เกิด misalignment สูงสุด `0.007 m` ที่ rigid Work 084 coaxial butt interface เทียบกับ tolerance `1e-6 m` ขณะที่ load frame ใหม่ยังไม่มีหลักฐาน mesh convergence และค่าด้านวัสดุ/กระบวนการทั้งหมดยังเป็น synthetic

บัญชีแรง โมเมนต์ และความร้อนเชิงพีชคณิตปิดครบ และ preregistered control ทุกกรณีให้ผลตามที่กำหนด แต่ผลผ่านเหล่านี้ไม่สามารถลบ blocker ด้าน geometry, kinematic interface, structural evidence หรือ material evidence ได้

## ไฟล์ที่เปลี่ยน

- `config/candidates/load_structure_integration_001.json`
- `src/formula_ultimate/subsystems/load_structure_integration.py`
- `scripts/candidates/build_load_structure_integration_001.py`
- `scripts/candidates/inspect_load_structure_integration_freecad.py`
- `tests/test_load_structure_integration_001.py`
- `docs/contracts/LOAD_STRUCTURE_INTEGRATION_001.md` และไฟล์ภาษาไทยคู่กัน
- ผลงานนี้และไฟล์ภาษาไทยคู่กัน
- แผน Work 087 และไฟล์ภาษาไทยคู่กัน เปลี่ยนสถานะเป็น `Partial`

หลักฐาน CAD และ replay ที่สร้างใต้ `artifacts/work087/` ถูก ignore และไม่ได้ commit

## หลักฐาน exact

- Result identity: `faae1e084549e6ce5bbe23e1a635e7bb5e16aa37f9f2e339f11af9df6e4ba6ae`
- SHA-256 ของ result JSON ที่เหมือนกันทุก byte: `38c8327a4f454dd0eb46fae7daa466638f938e3fa38aeeb8c971a7ab8bfe7cc9`
- Assembly STEP SHA-256: `33c1ade66729602bf9d022c36af017690ce1783364d38fddc71604684e62ee7d`
- Evaluation SHA-256: `9212dbe1b3e5299fbb11c54e6eacb616e68302e586359ee156c5c576a6131a04`
- Exact replay: `run_c` ทำซ้ำ `run_b` ได้เหมือนกันทุก byte
- Geometry: `17` solids; มวลจากความหนาแน่น synthetic `2.7451889573288466 kg`; ground clearance ของ integration part `0.0697 m`; routing clearance `0.002 m`; service clearance `0.012 m`
- Positive forbidden overlap: `8` คู่; ค่าสูงสุด `1.677032693654574e-05 m3`; minimum forbidden clearance `0 m`
- Maximum rigid-interface misalignment: `0.007 m`; tolerance `1e-6 m`
- Load case ที่ประกาศทั้งหกมี force และ moment residual เป็นศูนย์ตาม precision ที่บันทึก และ thermal residual เป็นศูนย์ตาม precision ที่บันทึก

แปดคู่ที่ overlap เป็นบวกคือ `carrier/converter_housing`, `carrier/converter_rotor`, `carrier/input_shaft`, `contact_roller/converter_housing`, `contact_roller/converter_rotor`, `converter_housing/guide_frame`, `converter_rotor/guide_frame` และ `guide_frame/input_shaft` ส่วน `contact_roller/input_shaft` คือ forbidden pair เพิ่มเติมที่ clearance เป็นศูนย์

## คำสั่งตรวจสอบ exact และผล

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\candidates\build_load_structure_integration_001.py `
  --config config\candidates\load_structure_integration_001.json `
  --output-root artifacts\work087\run_b `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"
# exit 0; status=partial; candidate_verdict=not_admitted

& .\.tools\cadquery-mcp\Scripts\python.exe scripts\candidates\build_load_structure_integration_001.py `
  --config config\candidates\load_structure_integration_001.json `
  --output-root artifacts\work087\run_c `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work087\run_b\result.json
# exit 0; exact replay

python -m unittest tests.test_load_structure_integration_001 tests.test_repository_contract -v
# exit 0; Ran 16 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 608 tests in 340.892s; OK (skipped=3)
```

## การทบทวนหลักฐานและข้อจำกัด

หลักฐานสนับสนุนประกอบด้วย upstream identity exact, การตรวจคู่ B-rep จริง, การตรวจ FCStd ที่มี named object, mass properties จาก geometry, บัญชี load/thermal ชัดเจน, causal failure control และ exact replay แต่หลักฐานขัดแย้งมีน้ำหนักชี้ขาด: layout ปัจจุบันชนกันจริงและ rigid motion interface เข้ากันไม่ได้ คำอธิบายทางเลือกว่าเป็น numerical noise ไม่สอดคล้องกับหลักฐาน เพราะ positive overlap สูงกว่า tolerance ที่ตรึงไว้ `1e-12 m3` หลายลำดับขนาดและเกิดกับหลายคู่ชิ้นส่วน หลักฐานที่ยังขาดคือ collision-free repackaging, motion-transfer interface แบบ articulated หรือแบบอื่นที่เข้ากันได้, mesh convergence ของ load frame ใหม่, ข้อมูล material/process ที่ใช้ตัดสิน design ได้, nonlinear contact, durability, crashworthiness และการทดสอบจริง

Work 088 สามารถ audit ความพร้อมทั้ง candidate จากหลักฐาน immutable นี้ได้ แต่ต้อง fail closed เป็น `not_ready` และห้ามจำลองหรืออ้างว่าเป็นรถทั้งคันที่ผ่าน mechanical admissibility จาก geometry ชุดนี้
