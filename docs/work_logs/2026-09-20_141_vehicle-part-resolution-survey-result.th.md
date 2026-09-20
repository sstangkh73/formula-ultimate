# ผลลัพธ์ Work 141: การสำรวจความละเอียดของชิ้นส่วนทั้งคัน

แหล่งภาษาอังกฤษ: `2026-09-20_141_vehicle-part-resolution-survey-result.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

วัด definition ที่เป็นเนื้อวัสดุทั้ง 44 รายการของรถ Work 135 เทียบมาตรฐานของ Work 140 control ทั้งแปดข้อถูกปฏิเสธ และการ replay บน tree ที่สะอาดให้ result SHA-256 ตรงกันทุกประการ ขนาดของช่องว่างด้านความละเอียดจึงเป็นตัวเลขแล้ว

**ผ่านมาตรฐาน 16 จาก 44 รายการ ต่ำกว่ามาตรฐาน 19 รายการ และอีก 9 รายการตัดสินไม่ได้เพราะ mesh ที่ลงทะเบียนแบ่งผ่านไม่ได้** ทุกตัวยึดและทุกชิ้นส่วนหมุนหรือแบริ่งอยู่ต่ำกว่ามาตรฐานทั้งหมด

## การกระจายของผลที่วัดได้

Result SHA-256 `ba0616d501b75966db183b6b643fa651ada1617025f6045cf7d42e6a2c9c40b6` และ `run_b` ตรงกันทุกประการ ช่องว่างที่ประกาศไว้สี่รายการถูกตัดออกและแสดงรายชื่อไว้ใน declaration

| ชั้นของชิ้นส่วน | จำนวน | `passed_resolution` | `insufficient_resolution` | `unresolved_measurement` |
| --- | ---: | ---: | ---: | ---: |
| `structure_or_housing` | 19 | 13 | 2 | 4 |
| `rotating_or_bearing` | 11 | **0** | 10 | 1 |
| `fluid_or_conductor_route` | 6 | 1 | 1 | 4 |
| `fastener_or_seal` | 4 | **0** | 4 | 0 |
| `electronics_module` | 4 | 2 | 2 | 0 |
| **รวม** | **44** | **16** | **19** | **9** |

ไม่มีชิ้นใดเป็น `unmanufacturable_feature` แปลว่าในรถไม่มีเศษบางเฉียบเลย ปัญหาอยู่ตรงข้าม คือชิ้นส่วนเรียบง่ายเกินไป

ชิ้นที่ผ่านมาตรฐานคือ `active_stack`, `busbar`, `carrier_plate`, `cold_plate`, `connector`, `contactor`, `energy_lid`, `front_crosshead`, `front_fork_rail`, `front_hub`, `nose_intake_frame`, `radiator`, `rear_beam`, `rear_hub`, `retention_bar` และ `support_bracket` ซึ่งเกือบทั้งหมดเป็นกล่องหรือแผ่นที่มีรูเจาะ ตรงกับรูปทรงที่ค่าต่ำสุดของชั้นโครงสร้างตั้งใจให้ผ่าน

ข้อที่ตกมากที่สุดคือหน้าโค้ง ขาดไป 11 ชิ้น ตามด้วยจำนวนขอบ 7 ชิ้น และจำนวนสเกลของ feature 5 ชิ้น มีห้าชิ้นที่มีเพียง 4 หน้า และสามชิ้นที่มี 5 หน้า

ชิ้นส่วนหมุนและแบริ่งตกทั้งหมด เพลาเป็นทรงกระบอกเรียบ บูชเป็นวงแหวนเรียบ โรเตอร์ไม่มีร่อง ไม่มีลิ่ม ไม่มีขั้นบ่า ไม่มีรัศมีโคน คือไม่มี geometry ที่ทำให้ชิ้นส่วนหมุนเป็นชิ้นส่วนหมุนเลย

`work135_pack_threaded` ยังเป็น `unsupported_joint_evidence` เหมือนเดิมจาก Work 140 คือเทคโนโลยีข้อต่อเพียงอย่างเดียวที่รถประกาศไว้ ไม่มี geometry ของเกลียวรองรับ

## ข้อค้นพบเรื่อง mesh

สามชิ้นทำ mesh ไม่สำเร็จที่ factor `0.15` ที่ลงทะเบียนไว้ ได้แก่ `spine_frame`, `coolant_supply_tube` และ `power_harness` โดย `spine_frame` ทำ mesh ได้ที่ `0.5` และ `1.0` จึงเป็นพฤติกรรมของตัว mesh ที่ขนาดละเอียดกับ geometry นั้น ไม่ใช่คุณสมบัติของชิ้นส่วน อีกหกชิ้น mesh สำเร็จแต่วาง element ได้ไม่ถึงหนึ่งตัวพาดสเกล feature ทั้งเก้าชิ้นจึงเป็น `unresolved_measurement` คือไม่มีคำตัดสินเรื่องความละเอียด และห้ามใช้อ้างความแข็งแรงใด

เนื่องจาก gate เชิง geometry ถูกตัดสินก่อน gate เรื่อง mesh คำตัดสิน `insufficient_resolution` ทั้ง 19 รายการจึงไม่ได้รับผลกระทบจากพฤติกรรมของ mesh

## ส่วนที่ต่างจากแผน

สคริปต์สร้าง declaration, ไฟล์ declaration ที่สร้างขึ้น และการสำรวจแบบ pilot เกิดขึ้นก่อนที่บันทึกแผนของงานนี้จะมีอยู่ ซึ่งผิดลำดับตามโปรโตคอลการทำงาน แผนถูกเขียนก่อนการรัน admitted `run_a` และไม่ได้อ้างตัวเลขของ pilot เป็นหลักฐาน จึงบันทึกความคลาดเคลื่อนนี้ไว้แทนการย้อนวันที่ของแผน

## ไฟล์ที่เปลี่ยน

- `scripts/development/build_vehicle_part_resolution_config.py`
- `config/development/vehicle_part_resolution_v1.json`
- `scripts/development/run_part_resolution_gate.py` — control เรื่อง mesh จะยกค่าการวัดให้สูงกว่าข้อกำหนดเมื่อไม่มีหัวข้อใดผ่าน gate เชิง geometry เพื่อให้ control ยังทดสอบได้บนรถที่ชิ้นส่วนส่วนใหญ่ไม่ผ่าน
- แผนและผลลัพธ์สองภาษานี้

หลักฐานที่สร้างขึ้นยังถูก ignore ไว้ใต้ `artifacts/work141/{pilot,run_a,run_b}`

## รายงานบั๊ก

1. **control ทดสอบไม่ได้เมื่อประชากรส่วนใหญ่ไม่ผ่าน** อาการ: ในการสำรวจทั้งคัน control `mesh_too_coarse_for_feature` จะไม่มีหัวข้อที่ผ่าน gate เชิง geometry เลย และการรันจะล้มเหลวเพราะข้อบกพร่องของ control แทนที่จะเป็นเพราะข้อค้นพบ การแก้: เมื่อไม่มีหัวข้อใดผ่าน control จะยกค่าที่วัดได้ขึ้นถึงข้อกำหนดของชั้นก่อนทดสอบกฎเรื่อง mesh การทดสอบกำกับ: `tests.test_part_resolution` ผ่าน และการรันสำรวจปฏิเสธ control ครบ 8/8

## การตรวจสอบ

สภาพแวดล้อม: Windows 11, Python 3.14.3, CadQuery 2.8.0 ใน `.tools/cadquery-mcp`, Gmsh 4.15.0 จาก `C:/Program Files/FreeCAD 1.1/bin`

```text
Command: python scripts/development/build_vehicle_part_resolution_config.py
Exit code: 0
Result: 44 ชิ้น; ตัด definition ที่เป็นช่องว่างออก 4 รายการ; ชั้น structure 19, rotating 11, route 6, fastener 4, electronics 4

Command: python scripts/development/run_part_resolution_gate.py --config config/development/vehicle_part_resolution_v1.json --output-root artifacts/work141/run_a
Exit code: 0
Result: passed_part_resolution_gate; ผ่าน 16 / ไม่ผ่าน 19 / ตัดสินไม่ได้ 9; control 8/8 ถูกปฏิเสธ;
        result SHA-256 ba0616d501b75966db183b6b643fa651ada1617025f6045cf7d42e6a2c9c40b6

Command: python scripts/development/run_part_resolution_gate.py --config ... --output-root artifacts/work141/run_b --replay-reference artifacts/work141/run_a/result.json
Exit code: 0
Result: replay exact: true

Command: python -m unittest tests.test_part_resolution
Exit code: 0
Result: Ran 21 tests — OK

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1022 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests
Exit code: 0

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

## ข้ออ้าง

- รองรับ: การกระจายของผลข้างต้น วัดจากชิ้นส่วน STEP ของ Work 135 โดยตรง ด้วยการจัดชั้นที่กำหนดไว้ก่อนรัน, ไม่มีตัวยึด ซีล หรือชิ้นส่วนหมุนใดในรถที่ถึงมาตรฐาน และในรถไม่มีเศษบางเฉียบเลย
- ไม่รองรับ: ชิ้นที่ผ่าน 16 รายการเป็นการออกแบบที่ดี เพราะการผ่านหมายถึงเพียงว่ามี geometry มากกว่า primitive ธรรมดา, ชิ้นใดแข็งแรง ผลิตได้ หรือ promote ได้ และชิ้นที่ตัดสินไม่ได้ทั้งเก้ารายการเพียงพอหรือไม่เพียงพอ

## ข้อจำกัดและงานถัดไป

- ข้อกำหนดยังเป็นกฎเชิงนับ ชิ้นส่วนยังเพิ่ม geometry ที่ไม่มีหน้าที่เพื่อให้ผ่านได้ การตรวจเชิงหน้าที่ควรอยู่ที่ evaluator
- การจัดชั้นใช้ occurrence class ที่ตัวรถประกาศเอง ถ้าป้ายผิดชิ้นส่วนจะไปอยู่ผิดชั้น และการจัดชั้นก็รับข้อผิดพลาดนั้นมาด้วย
- เก้าชิ้นยังไม่มีคำตัดสินจนกว่าจะแก้เส้นทาง mesh ของมันได้
- ถัดไป: ยกระดับตระกูลตัวยึดและชิ้นส่วนหมุนให้ถึงมาตรฐาน โดยเริ่มจากตัวยึดอ้างอิงของ Work 140 แล้วรันสำรวจนี้ซ้ำเพื่อวัดการขยับ จากนั้นคืองานเรื่องผิวต่อ คือการทำให้แรงเดินข้ามข้อต่อได้
