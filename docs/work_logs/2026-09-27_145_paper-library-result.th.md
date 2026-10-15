# ผลลัพธ์ Work 145: คลัง paper ในเครื่อง

แหล่งภาษาอังกฤษ: `2026-09-27_145_paper-library-result.md`

วันที่: 2026-09-27 ถึง 2026-09-28 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

คลังนี้บันทึก **411 paper** ใน 15 หมวด แบ่งเป็นตรง 143 อ้อม 234 และข้อมูล/ผลที่ใช้ได้ 34 **มี PDF เก็บในเครื่อง 261 ไฟล์** ที่ `papers/<category>/` (2.0 GB, git-ignore) ทุกไฟล์ผ่านการตรวจตัวตนและตรงกับ SHA-256 ที่บันทึกไว้ อีก 150 ชิ้นมีสถานะระบุชัดเจน:

| สถานะ | จำนวน | ความหมาย |
| --- | ---: | --- |
| `downloaded` | 261 | มี PDF ในเครื่อง ยืนยันตัวตนกับ resolver แล้ว และพบคำในชื่อเรื่องบนหน้าแรก |
| `download_failed` | 60 | มีแหล่งระบุว่ามีสำเนาฟรี แต่เซิร์ฟเวอร์ปฏิเสธการดาวน์โหลดด้วยสคริปต์ จึงแสดงไว้ให้ดาวน์โหลดผ่านเบราว์เซอร์ |
| `no_open_access_copy` | 90 | ไม่มีแหล่งใดระบุว่ามีสำเนาฟรี ต้องขอผ่านห้องสมุด |
| `identity_unconfirmed` | 0 | — |

paper ทั้ง 62 ชิ้นของ Work 102 (P01–P62) อยู่ในคลังพร้อมหมายเลข P เดิม และ 44 ชิ้นมีสำเนาในเครื่องแล้ว แค็ตตาล็อกอยู่ที่ [`PAPER_LIBRARY_2026-09-27.th.md`](../research/paper_library/PAPER_LIBRARY_2026-09-27.th.md)

| หมวด | จำนวน | มี PDF |
| --- | ---: | ---: |
| OE การค้นพบแบบ open-ended เชิงวิวัฒนาการ และการออกแบบร่วม | 43 | 33 |
| AG LLM/AI agent สำหรับวิศวกรรม โค้ด CAD และการจำลอง | 43 | 43 |
| QD Quality diversity การค้นหา surrogate และ multifidelity | 36 | 31 |
| CAD CAD, B-rep และการประกอบ | 34 | 30 |
| ST Topology optimization, meshing, FE, contact และการพัง | 24 | 9 |
| SI โครงสร้างพื้นฐานการจำลอง optimal control และ MDO | 21 | 12 |
| LT การควบคุมเวลาต่อรอบต่ำสุด พลวัตรถ และ co-design | 32 | 11 |
| EN พลังงานการแข่ง powertrain และแหล่งเก็บพลังงาน | 31 | 15 |
| TY ยางและแรงเสียดทาน | 17 | 5 |
| AE อากาศพลศาสตร์ CFD ชุดข้อมูล และ surrogate | 33 | 22 |
| TH ความร้อนและการระบายความร้อน | 6 | 2 |
| MA วัสดุ ข้อต่อ การชน การผลิต และพิกัดความเผื่อ | 15 | 2 |
| VV Verification, validation สถิติ และวินัยการอ้างผล | 32 | 20 |
| AR การแข่งอัตโนมัติ telemetry และกลยุทธ์ | 27 | 23 |
| DS การสังเคราะห์การออกแบบ การแทนค่าเชิงหน้าที่ และความใหม่ | 17 | 3 |

จาก 261 ไฟล์ที่ดาวน์โหลด 213 ไฟล์มาจาก arXiv ที่เหลือมาจากหน้า open access ของสำนักพิมพ์ (Nature, Springer, IOP, PLOS, Frontiers) คลังของมหาวิทยาลัย (Southampton, KU Leuven, Oxford ORA, HAL, Lund, Zenodo) หน้าของผู้แต่ง และ NASA NTRS

## ไฟล์ที่เปลี่ยน

- `scripts/research/build_paper_library.py`: resolver, downloader, ตัวสร้างแค็ตตาล็อก, `--verify` และ `--ingest`
- `docs/research/paper_library/sources/01…15_*.json`: รายการคัดสรรพร้อมหมายเหตุความเกี่ยวข้องสองภาษา
- `docs/research/paper_library/intro.json`: บทนำแค็ตตาล็อกสองภาษา ไฟล์นี้ไม่ได้ระบุไว้ในแผน
- `docs/research/paper_library/manifest_v1.json`: ตัวตน URL SHA-256 ขนาด และประวัติการพยายามดาวน์โหลดที่สร้างอัตโนมัติ
- `docs/research/paper_library/PAPER_LIBRARY_2026-09-27.md` และ `.th.md`: แค็ตตาล็อกที่สร้างอัตโนมัติ
- `tests/test_paper_library.py`: ความถูกต้องของแค็ตตาล็อก
- `papers/.gitignore`: กันไม่ให้ PDF ใดเข้า version control
- แผนและผลลัพธ์สองภาษานี้

ไม่ได้แก้โค้ดฟิสิกส์ configuration gate หรือ claim ใด การแก้ที่ยังไม่ commit ของผู้ใช้ (`.gitignore`, `LICENSE-DATA.md`, `README*.md`, `docs/MATERIAL_DATA_POLICY*.md`) ไม่ถูกแตะและไม่ถูก stage

## การตัดสินใจ

- **PDF อยู่ในเครื่องเท่านั้น** repository นี้เป็นสาธารณะภายใต้ CC BY 4.0 และ paper ส่วนใหญ่ แม้เป็น open access ก็เผยแพร่ซ้ำภายใต้สัญญาอนุญาตนั้นไม่ได้ จึง commit เฉพาะ metadata โฟลเดอร์ `papers/` ignore ตัวเองด้วย `.gitignore` ของตัวเอง จึงไม่ต้องแตะ `.gitignore` ที่ root ซึ่งมีการแก้ของผู้ใช้ค้างอยู่
- **ยืนยันตัวตนก่อนเก็บ** arXiv ID และ DOI ที่จำมาถือเป็นคำใบ้ ไฟล์จะถูกบันทึกเฉพาะเมื่อ:
  1. metadata ของ arXiv, Crossref หรือ Semantic Scholar ตรงกับชื่อเรื่องที่คัดสรร ด้วยความคล้ายอย่างน้อย 0.86 (ระเบียนจาก DOI ตรงได้เมื่อชื่อเรื่องเป็นส่วนย่อยของชื่อที่คัดสรร)
  2. พบคำสำคัญในชื่อเรื่องอย่างน้อย 60% บนสองหน้าแรกของ PDF

  ในการรันสุดท้ายไม่มีคำใบ้ DOI หรือ arXiv ใดถูกปฏิเสธ ชื่อเรื่องที่จำผิดได้รับการแก้ตามแหล่งจริงแทน: AG-022, AG-042, SI-021, EN-018, LT-010 และ LT-032 ซึ่งชื่อปัจจุบันต่างจากที่บันทึกไว้ครั้งแรก
- **เปลี่ยนลำดับ resolver ระหว่างทำงาน** แผนเดิมใช้ OpenAlex แต่งบรายวันแบบไม่ระบุตัวตนหมดหลังค้นประมาณ 100 ครั้ง (HTTP 429 "Insufficient budget" ปัจจุบันต้องใช้ key) ลำดับจึงเปลี่ยนเป็น arXiv แล้ว Crossref (รวม subtitle) แล้ว Semantic Scholar แบบ batch ครั้งเดียวซึ่งให้ตำแหน่ง PDF แบบ open access ส่วน OpenAlex ยังใช้ได้ผ่าน `--openalex`
- **ไม่ได้ข้ามการตรวจ bot ใด ๆ** โฮสต์ open access หลายแห่งตอบสคริปต์ด้วย 403 แบบ Cloudflare: MDPI, ACM (คลังเป็น open access), PNAS, Royal Society, IEEE, T&F, Europe PMC, Cranfield, UniTN, Padova และ TU/e ส่วน PMC และบางคลัง (DTU, mediaTUM) ส่งหน้าคั่นหรือหน้าเว็บแทน PDF ทั้งหมดถูกบันทึกไว้ ไม่ได้หลบเลี่ยง ตัว client ระบุตัวเองตามจริงว่าเป็นเครื่องมือที่ไม่ใช่เบราว์เซอร์ และนั่นคือเหตุผลที่ HAL ซึ่ง challenge client ที่ทำตัวเหมือนเบราว์เซอร์ส่ง PDF ให้โดยตรง
- **ไม่ใช้ mirror ที่ไม่น่าเชื่อถือ** สำเนาของ MA-006 และ MA-008 มีเฉพาะบนเว็บไซต์แฟนคลับที่ไม่ทราบที่มา จึงไม่ดาวน์โหลด และไม่ได้ใช้ Scribd, ResearchGate หรือโฮสต์ลักษณะเดียวกัน
- **เส้นทางเติมให้ครบด้วยมือ** paper `download_failed` 60 ชิ้นแสดงเป็นตารางพร้อมลิงก์ท้ายแค็ตตาล็อก คำสั่ง `--ingest <folder>` นำ PDF ที่ดาวน์โหลดด้วยมือเข้าคลังภายใต้กฎตัวตนเดียวกัน

## การตรวจสอบ

```text
Command: python scripts/research/build_paper_library.py --download
Exit code: 0
Result: {"papers": 411, "downloaded": 242, "no_open_access_copy": 102, "identity_unconfirmed": 0, "download_failed": 67}

Command: python scripts/research/build_paper_library.py --download --only <169 ids ที่ยังไม่ได้ดาวน์โหลดหรือถูกแก้>
Exit code: 1 (crash ที่รายการ 153/169)
Result: OSError: [Errno 22] Invalid argument ขณะเขียน manifest_v1.json (Windows ล็อกไฟล์ชั่วคราวขณะอีก process อ่าน)
Fix: เขียน manifest ลงไฟล์ชั่วคราวแล้วแทนที่แบบ atomic พร้อม retry (write_manifest)

Command: python scripts/research/build_paper_library.py --download --only AR-016,AR-024,DS-001,…,DS-016   (16 รายการที่ยังไม่ถึง)
Exit code: 0
Result: {"papers": 411, "downloaded": 258, "no_open_access_copy": 94, "identity_unconfirmed": 0, "download_failed": 59}

Command: python scripts/research/build_paper_library.py --download --only SI-007,LT-010,TY-010,DS-008,LT-018,AE-032
Exit code: 0
Result: {"papers": 411, "downloaded": 261, "no_open_access_copy": 90, "identity_unconfirmed": 0, "download_failed": 60}

Command: การทดสอบเชิงลบของ --ingest (คัดลอก PDF ของ OE-001 เข้าไปเป็น "OE-003.pdf" และ "unnamed.pdf")
ผลครั้งแรก: "OE-003.pdf" ถูกปฏิเสธ แต่ "unnamed.pdf" ถูกบันทึกผิดเป็น DS-007 ("Development of a Functional Basis for Design")
            เพราะคำทั้งหมดในชื่อเรื่องสั้นและทั่วไปนั้นปรากฏอยู่ใน paper ของ Sims
Fix: ไฟล์ที่ไม่มีชื่อ ID ต้องมีชื่อเรื่องที่ค้างอยู่ในแค็ตตาล็อกเป็นวลีต่อเนื่องบนหน้าแรกเพียงหนึ่งเรื่อง
     ไฟล์ที่ตั้งชื่อตาม ID ต้องมีวลีนั้น หรือ word coverage >= 0.8 ไฟล์ที่ผิดถูกลบ และ DS-007 ถูกคืนสถานะ
     (--download --only DS-007: no_open_access_copy)
ทดสอบซ้ำ: ไฟล์เชิงลบทั้งสองถูกปฏิเสธ และ PDF ที่ถูกต้องแต่ไม่มีชื่อ ID (ST-003) ถูกบันทึก ทำในสำเนาที่ scratch ไม่ใช่ manifest จริง

Command: python scripts/research/build_paper_library.py --verify
Exit code: 0
Result: {"downloaded_checked": 261, "problems": 0}   (ไฟล์มีอยู่ ขึ้นต้นด้วย %PDF และ SHA-256 กับขนาดตรงกัน)

Command: ตรวจวลีชื่อเรื่องใน PDF ทั้ง 261 ไฟล์ (สองหน้าแรก)
Result: 254 ไฟล์มีชื่อเรื่องที่คัดสรรเป็นวลี อีก 7 ไฟล์ตรวจด้วยตาแล้วว่าเป็น paper ที่ถูกต้อง:
  OE-040 (ชื่อเรื่องเป็นภาพสแกนของ NASA), ST-011 ("3-D" กับ "three-dimensional"), LT-005 ("Optimising"),
  VV-024 ("ML-based"), AR-005 (หัวกระดาษแม่แบบ preprint), AR-023 (ชื่อ preprint "physics-constrained"),
  DS-012 (ฉบับ working paper ที่ KU Leuven ของผู้แต่งชุดเดียวกัน ชื่อ "Identifying ex ante characteristics of radical
  inventions through patent-based indicators" ของบทความใน Research Policy)

Command: python -m unittest tests.test_paper_library tests.test_repository_contract
Exit code: 0
Result: Ran 12 tests — OK

Command: python -m compileall -q scripts src tests ; git diff --cached --check
Exit code: 0

Command: git status --short --ignored papers
Result: มีเพียง papers/.gitignore ที่เป็น untracked ทุกโฟลเดอร์หมวดถูก ignore (!!) ไม่มี PDF ถูก stage
```

## Claim

- สนับสนุน: paper ที่เกี่ยวข้อง 411 ชิ้นถูกบันทึกพร้อมหมายเหตุสองภาษา มี PDF ที่ตรวจตัวตนแล้ว 261 ไฟล์ในเครื่อง แต่ละไฟล์ตรงกับ hash ที่บันทึก และทุก paper มีสถานะการได้มาที่ระบุชัดเจน
- ไม่สนับสนุน:
  - ว่าการค้นครบถ้วน
  - ว่าหมายเหตุความเกี่ยวข้องมาจากการอ่านทุก paper เต็มฉบับ (ส่วนใหญ่มาจากบทคัดย่อและเนื้อหาที่ทราบ)
  - ว่าวิธีใดในรายการใช้ได้กับโครงการนี้
  - ว่าการไม่พบคู่แข่งโดยตรงแสดงความใหม่

## ข้อจำกัดและงานต่อ

- paper open access 60 ชิ้นยังต้องดาวน์โหลดผ่านเบราว์เซอร์ ตารางท้ายแค็ตตาล็อกแสดงรายการไว้ ให้บันทึกไว้ในโฟลเดอร์เดียวแล้วรัน `python scripts/research/build_paper_library.py --ingest <folder>` การตั้งชื่อไฟล์เป็น `<ID>.pdf` ทำให้จับคู่ชัดเจน
- 90 paper ไม่มีสำเนาฟรี รวมถึงงานคลาสสิกที่ปิด (เช่น Bendsøe & Kikuchi 1988, NSGA-II, Katz 2006, paper ของ Pacejka, Junker 1969) และ paper VSD หลายชิ้นของ Taylor & Francis ต้องใช้สิทธิ์เข้าถึงของสถาบัน
- osti.gov เข้าไม่ได้จากเครือข่ายนี้ (เชื่อมต่อ TCP ไม่สำเร็จ) VV-001 และ VV-004 มีสำเนาที่ OSTI ซึ่งอาจดาวน์โหลดได้จากเครือข่ายอื่น
- OpenAlex ต้องใช้ API key สำหรับการใช้งานระดับนี้ การรันใหม่ด้วย `--openalex` พร้อม key อาจพบสำเนาในคลังเพิ่ม
- คลังมีขนาดใหญ่ (2.0 GB) ไฟล์ที่ใหญ่ที่สุดเป็น paper ด้านกราฟิก สูงสุดไฟล์ละ 75 MB
- งานต่อที่แนะนำ: จัดอันดับการทบทวนช่องว่างของ Work 102 ใหม่ตามหมวดใหม่ โดยเฉพาะ CAD-013 ถึง CAD-016, DS-013 ถึง DS-015 (การสังเคราะห์การประกอบและข้อต่อสำหรับ part resolution), LT-011, LT-012 และ LT-022 ถึง LT-025 (lap solver สำหรับ co-design) และ AE-022 ถึง AE-024 (surrogate นอกการกระจายข้อมูลฝึก)
