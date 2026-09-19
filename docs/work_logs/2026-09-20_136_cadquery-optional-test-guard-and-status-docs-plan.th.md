# แผน Work 136: Test Guard สำหรับ CadQuery ที่เป็น Optional และการอัปเดตเอกสารสถานะ

แหล่งภาษาอังกฤษ: `2026-09-20_136_cadquery-optional-test-guard-and-status-docs-plan.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## หมายเหตุเรื่องเลขงาน

เอกสารของ Work 135 เรียกงานที่จะรันฟิสิกส์ต่อบน native solids ของ Work 135 ว่า "Work 136" แต่ดัชนีแผนละเอียดกำหนดไว้ว่าเลขงานในอนาคตไม่ใช่การจองล่วงหน้า และงานที่แทรกเข้ามาให้ใช้เลขถัดไปที่ยังว่าง งานซ่อมนี้จึงใช้เลข 136 และงานรันฟิสิกส์บน native solids จะใช้เลขถัดไปที่ยังว่างแทน (ตอนนี้คือ 137) โดยไม่เขียนบันทึกของ Work 135 ใหม่

## วัตถุประสงค์

1. ทำให้ชุดทดสอบ default ผ่านอีกครั้งในสภาพแวดล้อมที่ไม่มี CadQuery ที่ commit `ed5dae3` เมื่อรัน `python -m unittest discover -s tests` บน Python 3.14.3 ที่ไม่มี CadQuery ได้ผล `Ran 956 tests ... FAILED (errors=1, skipped=8)` สาเหตุคือ `tests/test_native_detailed_vehicle.py` มี `from scripts.cad.build_native_detailed_vehicle import ...` ที่ระดับโมดูล และสคริปต์นั้นเรียก `import cadquery as cq` ทันทีที่ถูก import ขณะที่ `pyproject.toml` ประกาศว่า CadQuery เป็น optional extra ("CadQuery-backed CAD kernel tests skip themselves when it is absent") และ CI ติดตั้งแค่ `pip install -e .` ดังนั้นถ้า push commit ในเครื่องที่ยังไม่ได้ push อีก 29 ตัว การรัน CI บน Ubuntu จะพัง
2. แก้ข้อความสถานะที่ล้าสมัยใน `EVIDENCE.md`, `README.md` และไฟล์คู่ภาษาไทย

## ขอบเขต

- `tests/test_native_detailed_vehicle.py`: การทดสอบ declaration/admission 6 ตัวยังรันเสมอ ย้ายการทดสอบ 3 ตัวที่ต้องใช้ kernel (closed-flag regression, fan fusion regression และ signed-zero signature) ไปไว้ใน class ที่มี `unittest.skipUnless(HAS_CADQUERY, ...)` และ import สคริปต์ build แบบ lazy ใน `setUpClass` ตาม pattern เดิมใน `tests/test_brep_grammar.py`
- `EVIDENCE.md` / `EVIDENCE.th.md`: แทนจำนวนการทดสอบของวันที่ 7 กันยายนด้วยจำนวนปัจจุบันที่วัดจริง ระบุว่า commit ในเครื่อง 29 ตัวหลัง `2c2bf36` ยังไม่เคยผ่าน CI และเปิดเผยว่าผลการเปรียบเทียบของ Work 125, 127, 128 และ 129 เป็น synthetic fixture ที่ประกาศไว้ใน config ไม่ใช่ผลจาก simulator
- `README.md` / `README.th.md`: อัปเดตหัวข้อ "Current Implementation Status" ให้ตรงกับ Level-0 kernel, bounded campaign v3, ชุดงาน Works 108–135 และ native geometry ของ Work 135 และลบข้อความเก่าที่บอกว่ามีปัญหาเปิดสองข้อทำให้ Ubuntu CI แดง
- แผนสองภาษานี้และผลลัพธ์สองภาษาที่ตรงกัน

## สิ่งที่ไม่ทำ

ไม่แก้ `scripts/cad/build_native_detailed_vehicle.py`, source modules, configurations, artifacts หรือบันทึกของ Work 125–135 ไม่ทำให้ assertion ใดอ่อนลง การทดสอบ kernel ต้องยังรันและผ่านเมื่อมี CadQuery ไม่ push ไม่ trigger CI และไม่เขียนประวัติใหม่

## การตรวจสอบ

1. `python -m unittest tests.test_native_detailed_vehicle -v` บน system Python ที่ไม่มี CadQuery: exit 0, ผ่าน 6, ข้าม 3
2. `.tools/cadquery-mcp/Scripts/python.exe -m unittest tests.test_native_detailed_vehicle -v`: exit 0, ผ่าน 9, ข้าม 0
3. `python -m unittest discover -s tests`: exit 0 และไม่มี error
4. `python -m unittest tests.test_repository_contract -v`: exit 0
5. `git diff --check` และ `git diff --cached --check`: exit 0

## เกณฑ์สำเร็จและล้มเหลว

สำเร็จ: ผ่านทุกด่านตรวจสอบ และเอกสารระบุเฉพาะจำนวนที่วัดได้จริง ล้มเหลว: การทดสอบ kernel หายไปแทนที่จะถูกข้าม, assertion ใดอ่อนลง หรือชุดทดสอบยังมี error

## ความเสี่ยง

- จำนวนที่อ้างในเอกสารจะล้าสมัยได้ วิธีรับมือ: ระบุวันที่ และให้คำสั่งที่ใช้ทำซ้ำเป็นตัวตัดสิน
- การเปิดเผยว่าผลลัพธ์ประกาศไว้ใน config อาจถูกอ่านว่าเป็นการถอน Works 125–129 ทั้งหมด จึงจำกัดขอบเขตให้ชัด: งานเหล่านั้นตรวจสอบ logic ของ gate, control และ replay ได้จริง ส่วนตัวเลขผลลัพธ์เป็น synthetic fixture
