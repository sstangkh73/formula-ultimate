# ผล Work 146: อ่าน paper เต็มฉบับและสังเคราะห์เพื่อโครงการ

แหล่งภาษาอังกฤษ: `2026-09-28_146_full-paper-reading-and-synthesis-result.md`

วันที่: 2026-09-28 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

ทำบัญชีและสกัดเนื้อหาทีละหน้าของคลัง PDF ในเครื่องครบ 261 ฉบับ พร้อมจัดทำรายงานภาษาอังกฤษ/ภาษาไทย 261 คู่ รายงานสังเคราะห์สองภาษาครอบคลุมผลที่พบ ประเด็นน่าสนใจ ความเชื่อมโยงกับ Formula Ultimate ช่องว่างหลักฐาน และการปรับปรุงตามลำดับความสำคัญครบทั้ง 15 หัวข้อของคลัง

corpus มี 6,280 หน้าและข้อความที่สกัดได้ 3,503,351 คำ paper ที่สำคัญต่อการตัดสินใจ 15 ฉบับได้รับ deep review ด้านวิธี ผล ข้อจำกัด และอ้างหน้าที่เจาะจง ส่วนรายงานอีก 246 ฉบับระบุชัดว่าเป็น full-text transfer record ไม่ใช่การทำซ้ำผลหรือ critical review เชิงลึกที่เทียบเท่ากัน

## ไฟล์ที่เปลี่ยน

- `docs/research/paper_reviews/FULL_LIBRARY_SYNTHESIS_2026-09-28.md`
- `docs/research/paper_reviews/FULL_LIBRARY_SYNTHESIS_2026-09-28.th.md`
- `docs/research/paper_reviews/by_paper/`: รายงานอังกฤษ 261 ไฟล์และคู่ภาษาไทย 261 ไฟล์
- `docs/research/paper_reviews/reading_manifest.json`: ตัวตนแหล่งข้อมูล hash, coverage, ตัวชี้ตำแหน่งหน้า section/evidence, บรรณานุกรม และ path รายงานของ PDF ครบ 261 ฉบับ
- `scripts/research/extract_paper_corpus.py`: ระบบทำบัญชี สกัด สร้าง metadata และตรวจรายงานแบบ deterministic
- `scripts/research/generate_paper_review_reports.py`: ระบบสร้างรายงานและบทสังเคราะห์สองภาษาที่ทำซ้ำได้
- `tests/test_paper_reviews.py`: test บัญชีไฟล์ coverage, ขอบเขตข้อมูล/ขนาด คู่สองภาษา ลิงก์ ระดับการอ่าน และ schema regression
- แผนและบันทึกผลสองภาษาของงานนี้

ไม่ได้แก้หรือ stage source PDF การเปลี่ยนแปลงเดิมใน `.gitignore`, `LICENSE-DATA.md`, `README.md`, `README.th.md`, `docs/MATERIAL_DATA_POLICY.md` และ `docs/MATERIAL_DATA_POLICY.th.md` ถูกเก็บไว้นอก work item นี้

## การตัดสินใจและการจัดการหลักฐาน

1. แยก paper finding, reviewer interpretation และ project proposal ในรายงานทุกฉบับ
2. เปิดเผยระดับการอ่านสองแบบ: decision-critical deep review 15 ฉบับ และ full-text transfer record 246 ฉบับ โดยไม่เรียกการสกัดครบว่าเป็น independent replication
3. ให้ทุก paper มีข้อเสนอ transfer ที่ไม่ซ้ำกัน พร้อม target artifact/module, proposed change, experiment/control และ acceptance/failure evidence
4. เก็บข้อความที่สกัดแบบคำต่อคำไว้ใน local artifact ที่ ignore และเผยแพร่เฉพาะ provenance กับตัวชี้หน้าขนาดกะทัดรัดใน `reading_manifest.json`
5. ใช้ cue page และ evidence-profile label อัตโนมัติเป็นเพียง navigation aid ไม่ใช่ evidence grade
6. ตรวจภาพของหน้าที่มีข้อความน้อยแบบตัวแทน แหล่งข้อมูลหกฉบับที่มี substantial-text coverage ต่ำกว่า 95% เป็นหน้ารูป CFD/geometry/diagram/dataset หรือหน้าท้ายว่าง ไม่พบ source ที่เป็นภาพสแกนอ่านไม่ได้
7. แก้การตีความ EN-012: paper สนับสนุนความแตกต่างของ fidelity สำหรับ sizing กับ control และไม่ได้พิสูจน์การกลับลำดับ architecture แบบทั่วไป
8. รักษาขอบเขตโครงการว่า วรรณกรรมและ Level-0 simulation สนับสนุนการคัดเลือกและการพยายามหักล้างได้ แต่ไม่สามารถยืนยัน vehicle ทางกายภาพได้ด้วยตัวเอง

## การตรวจแบบ fresh-reader

fresh-reader อิสระรอบแรกพบว่า output ราย paper เริ่มต้นใช้ template มากเกินไป การเปลี่ยนแปลงโครงการยังไม่ได้อนุมานจาก paper อย่างเพียงพอ ข้อกล่าวสำคัญตรวจสอบย้อนกลับได้ไม่พอ ส่วน “น่าสนใจ” ของ synthesis กว้างเกินไป บรรณานุกรมไม่ครบ และประโยคไทยเรื่องอำนาจ agent หนึ่งตำแหน่งกำกวม จึงสร้างรายงานใหม่โดยเพิ่มคำถาม/ข้อเสนอที่แยกกัน บรรณานุกรม บทบาทของข้อกล่าว transfer table จุดอ้างอิงที่ระบุชื่อใน synthesis, deep review 15 ฉบับ และแก้ถ้อยคำภาษาไทย

fresh-reader รอบสองที่ร้องขอไม่สามารถทำเสร็จได้ เพราะ reviewing agent ถึงขีดจำกัดการใช้งานของบริการ จึงทำ automated validation และ manual content audit ขั้นสุดท้ายในงานหลักแทน

## การตรวจสอบ

รันทุกคำสั่งจาก `C:\Formula Ultimate`

### ไวยากรณ์ Python

คำสั่ง:

```powershell
python -m py_compile scripts/research/extract_paper_corpus.py scripts/research/generate_paper_review_reports.py tests/test_paper_reviews.py
```

Exit status: `0` และไม่มี output

### ตรวจ corpus และรายงาน

คำสั่ง:

```powershell
python scripts/research/extract_paper_corpus.py --validate-reports
```

Exit status: `0`

```text
Validated 261 PDFs; pages=6280; words=3503351
```

### Repository tests

คำสั่ง:

```powershell
python -m unittest tests.test_paper_library tests.test_paper_reviews tests.test_repository_contract
```

Exit status: `0`

```text
...................
----------------------------------------------------------------------
Ran 19 tests in 0.892s

OK
```

### Content audit

คำสั่งนับ/ค้นด้วย PowerShell มี exit status: `0`

```text
EN_REPORTS=261
TH_REPORTS=261
DEEP_REVIEWS=15
PROPOSALS=261
UNIQUE_PROPOSALS=261
OVERCLAIM_PHRASE=absent
PAPER_TREE_CHANGES=none
```

การตรวจ staged scope และ `git diff --cached --check` ถูกบันทึกโดย commit workflow ทันทีหลังบันทึกผลนี้

## ข้อจำกัด

- รายงานครอบคลุม PDF ทุกฉบับที่มีในคลังเครื่องปัจจุบัน ไม่ใช่วรรณกรรมทั้งหมดในสาขา
- การสกัด full text ไม่รักษารูปแบบสมการ ตาราง หรือภาพทุกส่วน ก่อน implement ยังต้องตรวจข้อกล่าวที่สำคัญต่อการตัดสินใจกับหน้า source ที่อ้าง
- work item นี้ทำ deep critical review เพียง 15 ฉบับ รายงานอีก 246 ฉบับเป็น transfer record ที่ตรวจสอบย้อนกลับได้เพื่อใช้คัดกรองและวางแผน ไม่ใช่สิ่งทดแทน independent replication
- งานนี้ไม่ได้ implement หรือ physically validate model, controller, geometry, material law หรือ experiment ใด
- ช่องบรรณานุกรมจำกัดตาม identifier ที่กู้ได้จาก source ในเครื่องและ metadata ของคลัง ช่อง DOI หรือ venue ที่หาไม่ได้ระบุไว้ตามจริง

## งานต่อเนื่อง

1. เพิ่ม deep review ราย paper เมื่อ paper นั้นกลายเป็นหลักฐานสำคัญต่อ work item ที่เฉพาะเจาะจง
2. แปลง action ลำดับสูงจาก synthesis เป็น experiment ที่วางแผนแยก พร้อม control, metric, falsification criterion และ deterministic replay metadata ที่ตายตัว
3. เริ่มจากหลักฐาน transient tyre/contact, การตรวจ aerodynamic field, การปิดสมดุล energy/thermal endurance, หลักฐานโครงสร้างอิสระ, tolerance/fatigue และ coupled whole-vehicle replay
4. บันทึกหลักฐาน implementation แยกต่างหาก ห้ามเลื่อนสถานะ design ด้วยการเทียบเคียงวรรณกรรมหรือ Level-0 simulation เพียงอย่างเดียว
