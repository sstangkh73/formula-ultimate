# แผน Work 144: ความสามารถสร้างซ้ำของตัวสร้าง declaration การสำรวจ

แหล่งภาษาอังกฤษ: `2026-09-21_144_survey-generator-reproducibility-plan.md`

วันที่: 2026-09-21 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์

ทำให้ `scripts/development/build_vehicle_part_resolution_config.py` สร้าง declaration ของการสำรวจทั้งสองไฟล์ที่ commit ไว้ได้ตรงทุกไบต์ เพื่อให้ผล admitted ของ Work 141 และ Work 142 ยังสืบย้อนกลับมาจาก repository ได้

## หลักฐานตั้งต้น

Work 142 เพิ่มโหมด `--upgrade` ให้ตัวสร้าง และพร้อมกันนั้นได้เพิ่มคีย์ `upgraded_definitions` ที่ตัวสร้างเขียนลงในทุก declaration รวมถึงการรันแบบธรรมดา การสร้าง declaration ของ Work 141 ใหม่จึงได้ไฟล์ที่มีคีย์เกินมาหนึ่งรายการจาก `config/development/vehicle_part_resolution_v1.json` ที่ commit ไว้

เรื่องนี้สำคัญเพราะผลของ Work 141 บันทึก `config_sha256` และ `protocol_sha256` ของไฟล์นั้นพอดี declaration ที่สร้างซ้ำไม่ได้ก็คือ declaration ที่ผล admitted ของมันสืบย้อนไม่ได้ ซึ่งเป็นคุณสมบัติที่วินัยเรื่อง replay มีไว้ปกป้อง working tree แสดงการเคลื่อนนี้เป็นไฟล์ `vehicle_part_resolution_v1.json` ที่ถูกแก้หลัง commit ของ Work 142

## ขอบเขต

- `scripts/development/build_vehicle_part_resolution_config.py`: เขียน `upgraded_definitions` เฉพาะการรันแบบ upgrade
- คืนไฟล์ `config/development/vehicle_part_resolution_v1.json` จาก repository และยืนยันว่า declaration ทั้งสองสร้างซ้ำได้โดยไม่มี diff
- แผนสองภาษานี้และผลลัพธ์สองภาษาที่ตรงกัน

## การตรวจสอบ

1. `git checkout -- config/development/vehicle_part_resolution_v1.json` แล้วสร้าง declaration ทั้งสองใหม่ และยืนยันว่า `git status` ไม่รายงานการเปลี่ยนแปลงของทั้งสองไฟล์
2. `python -m unittest tests.test_part_resolution tests.test_repository_contract`: exit 0
3. `python -m compileall -q scripts src tests`, `git diff --check`, `git diff --cached --check`: exit 0

## เกณฑ์สำเร็จและล้มเหลว

สำเร็จ: declaration ทั้งสองสร้างซ้ำได้โดยไม่มี diff และการทดสอบผ่าน

ล้มเหลว: มีการเขียนทับ declaration ที่ commit ไว้เพื่อให้ตรงกับตัวสร้าง ซึ่งจะทำให้ hash ของผลที่บันทึกไว้ใช้ไม่ได้อย่างเงียบ ๆ

## ความเสี่ยงและสิ่งที่ไม่ทำ

- ความเสี่ยง: การเคลื่อนแบบเดียวกันจะกลับมาอีกเมื่อตัวสร้างเพิ่มฟิลด์ใหม่ ผลลัพธ์จึงบันทึกกฎไว้ว่าการแก้ตัวสร้างต้องคง declaration เดิมให้สร้างซ้ำได้
- สิ่งที่ไม่ทำ: ไม่แก้เนื้อหาของ declaration ใด ไม่รัน Work 141 หรือ 142 ใหม่ และไม่แก้ gate
