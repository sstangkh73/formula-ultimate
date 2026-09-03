# ผล Work 083: Ground-Interaction Candidate 001

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-03_083_ground-interaction-candidate-001-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

การพัฒนา Work 083 แบบจำกัดเสร็จสมบูรณ์ CadQuery `2.8.0` สร้างกลไกสัมผัสพื้นห้าชิ้น canonical STEP แยกชิ้น และ assembly STEP ที่มีห้า solid FreeCAD `1.1.3` / OCCT `7.8.1` นำเข้าไฟล์ exact โดยไม่มี healing call รักษา valid solid แยกห้าชิ้น และบันทึกเอกสาร FCStd ที่ตรวจดูได้พร้อม named object ห้าชิ้น

Assembly mobility ที่คำนวณได้คือ `2 DOF` พอดี: carrier เคลื่อนที่แนวดิ่งรวม `0.014 m` และ contact roller หมุนรอบ `+y` การตรวจ B-rep exact ที่ `-0.007 m`, `0 m` และ `+0.007 m` พบ overlap `0 m3` และ clearance อย่างน้อย `0.008 m` สำหรับ forbidden pair ทุกคู่ กราฟแรงและกราฟแรงบิดที่ตรึงไว้มีเส้นทางต่อเนื่องอย่างละหนึ่งเส้นพอดี ค่า reference force, moment และ drive-energy residual เป็น `0.0` ทั้งหมด ผ่าน gate `1e-5`, `1e-5` และ `1e-4` ตามลำดับ falsification control ทั้งแปดกรณีทำให้เกิดผลที่วัดได้ตาม preregistration

Work item ด้านซอฟต์แวร์เสร็จแล้ว แต่ candidate นี้ตั้งใจให้ **ยังไม่ design-admitted** คำตัดสินคือ `not_admitted_synthetic_evidence` และ `design_use_allowed=false` Structural witness ใช้หลักฐานวัสดุ/กระบวนการ synthetic และครอบคลุมเพียง bracket exact กับ load family แบบแรงสัมผัส `500 N` ของ Work 082 ไม่ได้ validate กรณีแรงพื้น `[320, 180, 1250] N` ของ candidate นี้หรืออีกสี่ชิ้นส่วน

## ไฟล์ที่เปลี่ยน

- `config/candidates/ground_interaction_candidate_001.json`
- `src/formula_ultimate/subsystems/__init__.py`
- `src/formula_ultimate/subsystems/ground_interaction.py`
- `scripts/candidates/build_ground_interaction_candidate_001.py`
- `scripts/candidates/inspect_ground_interaction_freecad.py`
- `tests/test_ground_interaction_candidate_001.py`
- `docs/contracts/GROUND_INTERACTION_CANDIDATE_001.md` และไฟล์คู่ภาษาไทย
- result นี้และไฟล์คู่ภาษาไทย
- แผน Work 083 และไฟล์คู่ภาษาไทย ซึ่งเปลี่ยนสถานะเป็น `Completed`

CAD, FCStd, manifest, evaluation และ replay evidence ที่สร้างภายใต้ `artifacts/work083/` ถูก ignore และไม่ได้ commit

## การตัดสินใจและหลักฐานที่วัดได้

- กลไกนี้เป็น candidate หนึ่งแบบที่ตรวจดูได้ ไม่ใช่ topology ที่ฝังบังคับไว้ใน evaluator ทั่วไป solid แยกห้าชิ้นคือ `structural_mount`, `guide_frame`, `carrier`, `axle` และ `contact_roller`
- Mount ใช้ STEP exact จาก Work 081/082 ที่มี hash `b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89`; ไบต์ต้นทางที่เปลี่ยนจะ fail ก่อนการสร้าง
- Assembly STEP hash คือ `57dc477bbec58da05a0908d1b9b8de04c57a482f710c2362980fed8c51ccb135` ตัวตน canonical geometry manifest คือ `0ea7151e3610aa8652d0fd0352216bf3e667d84e34fc70e1720d00b26d517066`
- มวล synthetic รวมของห้าชิ้นจากรูปทรง exact คือ `0.533616275507311 kg`; ค่านี้คำนวณจากรูปทรงและความหนาแน่น synthetic ที่ประกาศ ไม่ใช่มวลที่วัดจากของจริง
- ขนาดแรงพื้นอ้างอิงคือ `1302.8046668629952 N` แรงตั้งฉากบวกคือ `1250 N` และ reference capacity utilization คือ `0.6514023334314976`
- บัญชีพลังงานขับคือ input `840 J`, ส่งออก `772.8000000000001 J` และ loss `67.19999999999993 J` กรณีเบรกแยกต่างหากต้านการหมุนด้วย `-30 Nm` และส่ง `600 J` ไปยังการคายพลังงาน โดยไม่สร้าง recovery credit ขึ้นมาเอง
- Control แบบ disconnected mount และ contact loss ทำให้ `dnf`; undersized capacity ให้ utilization `2.6056093337259902` และ `dnf` ส่วน blocked translation, seized rotation และ broken torque path ให้ degraded state ที่ระบุชัด พร้อมระยะเคลื่อนที่ กำลัง หรือแรงบิดส่งออกเป็นศูนย์ตามกรณี
- `run_b` และ `run_c` สร้าง result identity `a061d0b2de7b01eb31233cd3ed1ab9945eb5dbc015ca478c26fb9b77fbfaded3` ซ้ำกัน SHA-256 ของไฟล์ result JSON เท่ากันคือ `afc157a46b0837fb1c0d762f5e72225edc26929cfa1c8897bc7f99cabdc9eaa4`; replay identity คือ `acde7d11a1d32df69ace91dc9e6b7add31e46c9d7cfe4e8d4ac4d2dd3e2805b9`
- Canonical FreeCAD report สองรอบเหมือนกันทุกไบต์ โดยมี report identity `de4b4c8f632b102f5dfeb8ba5a899b8a7773c4ccc852af046b49873f32e91afd` แต่ hash ของ FCStd ดิบต่างกัน (`cc8477...` กับ `2f4a0e...`) เพราะ ZIP container ของ FCStd มี metadata ที่เปลี่ยนได้ จึงไม่อ้างว่าไบต์ FCStd ดิบ deterministic หลักฐาน replay คือ source STEP hash exact ร่วมกับ canonical FreeCAD report

## การทบทวนหลักฐาน

หลักฐานสนับสนุน: solid ห้าชิ้นที่ตรวจดูแยกกันได้, STEP identity exact, FCStd ห้าวัตถุ, mobility 2 DOF ที่คำนวณได้, B-rep clearance สามตำแหน่ง, เส้นทางแรง/แรงบิดต่อเนื่อง, บัญชี quasi-static ที่ปิด, causal controls แปดกรณี และ canonical replay แบบ exact

หลักฐานที่ขัดแย้ง: structural case ของ Work 082 เป็นแรงสัมผัสที่รู bracket เพียง `500 N` แนวสัมผัส ขณะที่ candidate นี้ประกาศแรงพื้นสามแกนที่ใหญ่กว่า และไบต์ FCStd ดิบไม่ replay ข้อเท็จจริงเหล่านี้ทำให้ยัง structural/design admission ไม่ได้ และถูกเก็บไว้โดยไม่ปิดบัง

คำอธิบายทางเลือก: ความเป็นไปได้ที่ดูเหมือนผ่านอาจเกิดจาก clearance ที่เผื่อมากและ bookkeeping quasi-static อย่างง่าย CadQuery กับ FreeCAD ใช้เทคโนโลยี OCCT ร่วมกัน และ residual ศูนย์เกิดจาก reaction ที่จับคู่เชิงพีชคณิต ไม่ใช่การวัดทดลอง

หลักฐานที่ยังขาด: บันทึกวัสดุ/กระบวนการที่ใช้ design ได้, structural analysis ของ guide/carrier/axle/roller และเวกเตอร์แรงเต็มของ candidate, nonlinear contact, ข้อมูล bearing/friction, tyre หรือ surface interaction, dynamic response, fatigue/buckling, thermal behavior, tolerance การผลิต, physical tests, safety evidence และ integration กับ Works 084-086

ความเชื่อมั่นสูงสำหรับตัวตนซอฟต์แวร์ exact, CAD solid ที่แยกกัน, mobility arithmetic ที่ประกาศ, static clearance ณ สามตำแหน่งที่ตรึงไว้, bookkeeping และ fault propagation ภายใต้ fixture นี้ ความเชื่อมั่นต่ำสำหรับคำอ้าง capacity, durability, controllability หรือ production ในโลกจริง

## คำสั่งตรวจสอบและผลลัพธ์แบบ exact

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\candidates\build_ground_interaction_candidate_001.py `
  --config config\candidates\ground_interaction_candidate_001.json `
  --output-root artifacts\work083\run_b `
  --structural-result artifacts\work082\run_e\result.json `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"
# exit 0; 5 parts; 5 assembly solids; 2 DOF; minimum clearance 0.008 m;
# maximum overlap 0.0 m3; residual ทุกค่า 0.0;
# verdict=not_admitted_synthetic_evidence

& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\candidates\build_ground_interaction_candidate_001.py `
  --config config\candidates\ground_interaction_candidate_001.json `
  --output-root artifacts\work083\run_c `
  --structural-result artifacts\work082\run_e\result.json `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work083\run_b\result.json
# exit 0; replay_exact=true;
# result_sha256=a061d0b2de7b01eb31233cd3ed1ab9945eb5dbc015ca478c26fb9b77fbfaded3

python -m unittest `
  tests.test_ground_interaction_candidate_001 `
  tests.test_repository_contract -v
# exit 0; Ran 18 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 546 tests in 432.451s; OK (skipped=3)
```

การลองครั้งแรกที่ส่ง inspection script ให้ `FreeCADCmd.exe` โดยตรงคืน exit `0` แต่ไม่ได้รัน script หรือสร้าง output ตอนนี้ runner เรียก `python.exe` ที่มากับ FreeCAD นำเข้า FreeCAD/Part APIs ชุดเดียวกัน และบังคับให้มีทั้ง JSON report กับ FCStd; หาก output หายจะ fail แม้ subprocess exit code เป็นศูนย์

## ข้อจำกัดและงานถัดไป

Work 083 ยังไม่ผ่าน entry gate ด้าน real part หรือ design evidence ตาม roadmap Work item ใหม่ต้องหาหลักฐานวัสดุ/กระบวนการ/การวัดที่ใช้ design ได้ และรัน structural/contact case ที่ตรงกับ candidate และเวกเตอร์แรง exact นี้ ก่อนทบทวน admission ใหม่ Work 084 ใช้ torque/contact interface ที่ประกาศนี้ได้เฉพาะเป็น synthetic integration fixture ไม่ใช่ validated hardware interface
