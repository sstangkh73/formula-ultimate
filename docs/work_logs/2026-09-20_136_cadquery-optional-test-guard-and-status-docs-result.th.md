# ผลลัพธ์ Work 136: Test Guard สำหรับ CadQuery ที่เป็น Optional และการอัปเดตเอกสารสถานะ

แหล่งภาษาอังกฤษ: `2026-09-20_136_cadquery-optional-test-guard-and-status-docs-result.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## สรุป

ชุดทดสอบ default กลับมาผ่านได้โดยไม่ต้องมี CadQuery การทดสอบ 3 ตัวของ Work 135 ที่ต้องใช้ kernel จะข้ามเมื่อไม่มี CadQuery และยังรันผ่านใน environment CadQuery ที่ pin ไว้ ส่วน `EVIDENCE.md`, `README.md` และไฟล์คู่ภาษาไทยตอนนี้ระบุสถานะการทดสอบที่วัดได้จริง ระบุว่า commit ที่ยังไม่ได้ push ไม่มีผล CI และระบุว่าผลลัพธ์ใดของ Works 125–129 เป็น synthetic fixture ที่ประกาศไว้ใน config

## รายงานบั๊ก

- อาการ: ที่ `ed5dae3` คำสั่ง `python -m unittest discover -s tests` บน Python 3.14.3 ที่ไม่มี CadQuery ให้ผล `Ran 956 tests ... FAILED (errors=1, skipped=8)` พร้อม `ModuleNotFoundError: No module named 'cadquery'`
- สาเหตุ: `tests/test_native_detailed_vehicle.py` import `scripts.cad.build_native_detailed_vehicle` ที่ระดับโมดูล และสคริปต์นั้นเรียก `import cadquery as cq` ทันทีที่ถูก import แต่ CadQuery เป็น optional extra (`pyproject.toml`) และ CI ติดตั้งแค่ `pip install -e .` ส่วนที่ Work 135 แก้ bootstrap ไว้เป็นปัญหาในทิศตรงข้าม (environment CadQuery ที่ไม่มี local package)
- การแก้: เพิ่ม `HAS_CADQUERY = importlib.util.find_spec("cadquery") is not None` แล้วย้ายการทดสอบ closed-flag, fan-fusion และ signed-zero ไปไว้ใน `NativeDetailedVehicleKernelTests` โดยไม่แก้เนื้อหา class นี้มี `unittest.skipUnless(HAS_CADQUERY, ...)` และ import สคริปต์ build ใน `setUpClass` ตาม pattern ของ `tests/test_brep_grammar.py` ไม่มี assertion ใดถูกแก้
- ทดสอบซ้ำ: ดูหัวข้อการตรวจสอบ

## ไฟล์ที่เปลี่ยน

- การทดสอบ: `tests/test_native_detailed_vehicle.py`
- เอกสาร: `EVIDENCE.md`, `EVIDENCE.th.md`, `README.md`, `README.th.md`
- บันทึก: แผนและผลลัพธ์ Work 136 สองภาษานี้

## การตัดสินใจ

- **เลขงาน:** งานซ่อมนี้ใช้เลข 136 ส่วนงานรันฟิสิกส์บน native solid ที่บันทึกของ Work 135 เรียกว่า "Work 136" จะใช้เลขถัดไปที่ยังว่าง (ตอนนี้คือ 137) ตามกฎในดัชนีแผนละเอียดที่ว่าเลขในอนาคตไม่ใช่การจอง และไม่ได้แก้บันทึกของ Work 135
- **สถานะใน README:** แทนย่อหน้าเก่าที่บอกว่า "Phase 1 เป็นแค่ powertrain หนึ่งมิติ" ด้วยรายการที่ระบุวันที่ ได้แก่ Level-0 kernel, campaign v3 (`p = 0.5`), ชุดงาน Works 108–133 และ native geometry ของ Work 135
- **ข้อความ CI ที่ล้าสมัย:** ข้อความใน README ที่ว่า "มีปัญหาเปิดสองข้อทำให้ Ubuntu CI แดง" ล้าสมัยแล้ว เพราะ `EVIDENCE.md` บันทึกการแก้ไว้แล้ว จึงเปลี่ยนเป็นสภาพจริงปัจจุบัน คือ commit ล่าสุดที่ push แล้ว `2c2bf36` ผ่าน CI ส่วน commit ในเครื่องหลังจากนั้นยังไม่มีผล CI
- **การเปิดเผย synthetic fixture:** `EVIDENCE.md` ระบุแล้วว่า Works 125, 127, 128 และ 129 คำนวณตัวเลขผลลัพธ์จากค่าที่ประกาศไว้ใน configuration ตัวอย่างเช่น ผลที่ Work 128 เร็วขึ้น `0.5 s` คือ `base_time_s: 100.0` ลบ `99.5` ใน `config/development/heldout_race_robustness_v1.json` และระบุด้วยว่า Works 126–130 ใช้ registry แบบกล่องมวล `60.0 kg` ขณะที่ native geometry ของ Work 135 หนัก `1023.65 kg` ข้อความเหล่านี้มาจากการตรวจ configuration และโมดูลในเซสชันนี้ และไม่ได้ถอน logic ของ gate, control และ replay ที่งานเหล่านั้นทดสอบไว้

## การตรวจสอบ

สภาพแวดล้อม: Windows 11, system Python 3.14.3 (ไม่มี CadQuery) และ Python 3.12.14 ของ `.tools/cadquery-mcp` ที่ pin ไว้และมี CadQuery

```text
Command: python -m unittest tests.test_native_detailed_vehicle -v
Exit code: 0
Result: Ran 9 tests — OK (skipped=3); ทั้ง 3 ตัวที่ข้ามระบุ CadQuery kernel environment

Command: .tools/cadquery-mcp/Scripts/python.exe -m unittest tests.test_native_detailed_vehicle -v
Exit code: 0
Result: Ran 9 tests — OK (ไม่มีการข้าม)

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 964 tests in 380.405s — OK (skipped=11)
ก่อนแก้ (ed5dae3): Ran 956 tests — FAILED (errors=1, skipped=8)

Command: python -m unittest tests.test_repository_contract -v
Exit code: 0
Result: Ran 6 tests — OK

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

จำนวนการทดสอบเพิ่มจาก 956 เป็น 964 เพราะเดิมโมดูลที่ import ไม่ได้ถูกนับเป็น error test หนึ่งตัว ตอนนี้โมดูลนั้นให้การทดสอบ 9 ตัวและข้าม 3 ตัว: 956 − 1 + 9 = 964 และข้าม 8 + 3 = 11

## ข้ออ้าง

- รองรับ: ชุดทดสอบผ่านบนเครื่องด้วยชุด dependency เดียวกับ CI และ regression ของ kernel ใน Work 135 ยังผ่านเมื่อมี CadQuery
- ไม่รองรับ: CI บน Ubuntu เขียวสำหรับ commit ที่ยังไม่ได้ push เพราะไม่มีการ push และไม่มีผล CI ส่วนความต่างข้ามแพลตฟอร์มอื่นหรือความต่างของ elementary function ใน Works 108–135 ยังไม่เคยทดสอบบน Linux

## ข้อจำกัดและงานถัดไป

- push เพื่อให้ได้ผล CI บน Ubuntu ครั้งแรกของ Works 108–136 ผู้ใช้ต้องสั่งแยกต่างหาก
- งานวิจัยถัดไป (เลข 137 หรือเลขถัดไปที่ยังว่าง): รันการประเมิน structural, thermal, flow, ground, actuation, energy และ controller ใหม่บน solid ของ Work 135 โดยตรง
- เปลี่ยนผลลัพธ์ที่ประกาศไว้ใน config ของ comparison gate ใน Work 125/127/128/129 ให้มาจาก simulator ก่อนจะอ้างผลเชิงเปรียบเทียบใด
