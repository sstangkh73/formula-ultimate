# ผลลัพธ์ Work 144: ความสามารถสร้างซ้ำของตัวสร้าง declaration การสำรวจ

แหล่งภาษาอังกฤษ: `2026-09-21_144_survey-generator-reproducibility-result.md`

วันที่: 2026-09-21 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

declaration ของการสำรวจทั้งสองไฟล์สร้างซ้ำจาก repository ได้โดยไม่มี diff ผล admitted ของ Work 141 คือ `ba0616d501b75966db183b6b643fa651ada1617025f6045cf7d42e6a2c9c40b6` และผลการสำรวจของ Work 142 คือ `8d4e4e5e926c2af5af4b3bfdc9e33c7da57d14af930c768329c81af54c08acdf` จึงยังสืบย้อนกลับมาจากอินพุตที่ commit ไว้ได้

## รายงานบั๊ก

- **อาการ:** หลัง commit ของ Work 142 `git status` แสดงว่า `config/development/vehicle_part_resolution_v1.json` ถูกแก้ ทั้งที่ไม่มีใครแก้ไฟล์นั้น การเปลี่ยนแปลงคือคีย์ที่เพิ่มมาหนึ่งรายการ `"upgraded_definitions": []`
- **สาเหตุ:** Work 142 เพิ่มโหมด `--upgrade` ให้ตัวสร้าง และเขียนคีย์ใหม่นั้นโดยไม่มีเงื่อนไข การสร้างใหม่แบบธรรมดาจึงไม่ได้ declaration ของ Work 141 อีกต่อไป และเนื่องจากผลของ Work 141 hash ไฟล์นั้นพอดีผ่าน `config_sha256` และ `protocol_sha256` ผลที่บันทึกไว้จึงหยุดสืบย้อนจาก repository ได้อย่างเงียบ ๆ
- **การแก้:** เขียนคีย์นั้นเฉพาะการรันแบบ upgrade และคืนไฟล์ declaration ของ Work 141 จาก repository แทนการเขียนทับให้ตรงกับตัวสร้าง เพราะการเขียนทับจะทำให้ hash ที่บันทึกไว้ใช้ไม่ได้เพียงเพื่อให้เครื่องมือดูถูกต้อง
- **การทดสอบกำกับ:** การสร้าง declaration ทั้งสองใหม่ทำให้ working tree สะอาด คือการ `git add` ทั้งสองไฟล์ไม่มีอะไรถูก stage

**กฎที่เหลือไว้จากเรื่องนี้:** การแก้ตัวสร้างต้องคงให้ declaration ทุกไฟล์ที่มันเคยผลิตสร้างซ้ำได้ การเพิ่มฟิลด์ให้เอาต์พุตใหม่ทำได้ แต่การเพิ่มให้เอาต์พุตเก่าคือการทำลายตัวตนที่บันทึกไว้อย่างเงียบ ๆ

## ไฟล์ที่เปลี่ยน

- `scripts/development/build_vehicle_part_resolution_config.py`
- แผนและผลลัพธ์สองภาษานี้

เนื้อหาของ declaration ไม่เปลี่ยน

## การตรวจสอบ

```text
Command: git checkout -- config/development/vehicle_part_resolution_v1.json
         python scripts/development/build_vehicle_part_resolution_config.py
         python scripts/development/build_vehicle_part_resolution_config.py --upgrade --output config/development/vehicle_part_resolution_v2.json
         git add config/development/vehicle_part_resolution_v1.json config/development/vehicle_part_resolution_v2.json ; git diff --cached --stat
Exit code: 0
Result: ไม่มีการเปลี่ยนแปลงที่ถูก stage — declaration ทั้งสองสร้างซ้ำได้ตรงทุกไบต์

Command: python -m unittest tests.test_part_resolution tests.test_repository_contract
Exit code: 0
Result: Ran 27 tests — OK

Command: python -m compileall -q scripts src tests ; git diff --check ; git diff --cached --check
Exit code: 0
```

## ข้ออ้าง

- รองรับ: declaration ของการสำรวจทั้งสองไฟล์ที่ commit ไว้สร้างซ้ำได้จากตัวสร้าง ณ commit นี้
- ไม่รองรับ: configuration ที่ถูกสร้างขึ้นทุกไฟล์ใน repository สร้างซ้ำได้ ตรวจเพียงสองไฟล์นี้เท่านั้น

## ข้อจำกัดและงานถัดไป

คำถามที่กว้างกว่า คือ configuration ที่ commit ไว้ไฟล์ใดบ้างที่ยังสร้างซ้ำได้จากสคริปต์ที่ผลิตมัน ยังไม่ได้ทดสอบ งานแยกต่างหากอาจเพิ่มการทดสอบ contract ที่สร้าง declaration ทุกไฟล์ใหม่และล้มเหลวเมื่อมี diff
