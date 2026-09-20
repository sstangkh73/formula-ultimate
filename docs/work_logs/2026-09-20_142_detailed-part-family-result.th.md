# ผลลัพธ์ Work 142: ตระกูลชิ้นส่วนละเอียดและผลต่างของการสำรวจ

แหล่งภาษาอังกฤษ: `2026-09-20_142_detailed-part-family-result.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

สร้างและตรวจชิ้นส่วนเจ็ดชิ้นที่ระดับความละเอียดของชิ้นส่วนจริง แล้วรันการสำรวจรถซ้ำโดยแทน definition เก้ารายการด้วยชิ้นส่วนเหล่านั้น การรันทั้งสองคู่ปฏิเสธ control ครบแปดข้อและ replay ได้ตรงทุกประการ

geometry ขยับไปไกลมาก แต่คำตัดสินขยับน้อยกว่า เพราะการเพิ่มความละเอียดของชิ้นส่วนทำให้ mesh ต้องละเอียดตามไปด้วย และ mesh ที่ลงทะเบียนกลายเป็นข้อจำกัดที่ผูกมัดแทน

## การรันตระกูลชิ้นส่วน

`artifacts/work142/family_a` result SHA-256 `744463abe5e1daa2d6cc1920d245284d678e8672a6b9b2f2c2c9a8edf46a07eb` และ `family_b` replay ตรงทุกประการ ใช้ mesh size factor `0.08` ที่เลือกจาก pilot ก่อนการรัน admitted ส่วนค่าอื่นของมาตรฐานไม่เปลี่ยนจาก Work 140

| ชิ้นส่วน | สถานะ | หน้า | โค้ง | ขอบ | element พาด |
| --- | --- | ---: | ---: | ---: | ---: |
| `reference_m8_bolt` | `passed_resolution` | 28 | 17 | 73 | 2.13 |
| `detailed_nyloc_nut` | `passed_resolution` | 13 | 4 | 28 | 8.07 |
| `detailed_serrated_washer` | `passed_resolution` | 52 | 50 | 125 | 1.88 |
| `detailed_stepped_axle` | `passed_resolution` | 17 | 7 | 42 | 1.03 |
| `detailed_flanged_bushing` | `passed_resolution` | 14 | 9 | 23 | 1.84 |
| `detailed_slotted_rotor` | `passed_resolution` | 53 | 27 | 151 | 1.18 |
| `detailed_beaded_gasket` | `unresolved_measurement` | — | — | — | — |

ปะเก็นไม่มีค่าที่วัดได้เลย เพราะการสร้างของมันเองไม่ reproducible ระดับไบต์ ดูรายงานบั๊ก

**ข้อต่อแบบเกลียวยังไม่ผ่านตามที่คาดไว้** `reference_threaded_pair` เป็น `unsupported_joint_evidence` โดยมีผิวขบ `[2, 0]` คือสลักมีสันเกลียวส่วนน็อตไม่มี เพราะเกลียวในยังสร้างไม่ได้ที่นี่ กฎที่รัดกุมขึ้นในงานนี้คือสิ่งที่ทำให้เห็นเรื่องนี้ เพราะ Work 140 นับผิวขบรวมทั้งคู่ ข้อต่อนี้จึงจะผ่านได้ด้วยเกลียวของสลักเพียงฝ่ายเดียว

## ผลต่างของการสำรวจ

`artifacts/work142/survey_a` result SHA-256 `8d4e4e5e926c2af5af4b3bfdc9e33c7da57d14af930c768329c81af54c08acdf` และ `survey_b` replay ตรงทุกประการ มาตรฐานเหมือน Work 141 ทุกประการรวมถึง mesh size factor `0.15` การรันทั้งสองจึงเทียบกันได้

| สถานะ | Work 141 (`ba0616d5`) | Work 142 (`8d4e4e5e`) | เปลี่ยนแปลง |
| --- | ---: | ---: | ---: |
| `passed_resolution` | 16 | 18 | **+2** |
| `insufficient_resolution` | 19 | 11 | **−8** |
| `unresolved_measurement` | 9 | 15 | **+6** |
| `unmanufacturable_feature` | 0 | 0 | 0 |

แยกตาม definition ที่ถูกแทน

| Definition | Work 141 | Work 142 | หน้า |
| --- | --- | --- | --- |
| `washer` | `insufficient_resolution` | `passed_resolution` | 4 → 52 |
| `nut` | `insufficient_resolution` | `passed_resolution` | 9 → 13 |
| `bolt` | `insufficient_resolution` | `unresolved_measurement` | 5 → 33 |
| `motor_rotor` | `insufficient_resolution` | `unresolved_measurement` | 6 → 53 |
| `front_bushing` / `rear_bushing` | `insufficient_resolution` | `unresolved_measurement` | 4 → 14 |
| `rear_axle` | `insufficient_resolution` | `unresolved_measurement` | 8 → 17 |
| `front_axle` | `unresolved_measurement` | `unresolved_measurement` | 12 → 17 |
| `pack_gasket` | `insufficient_resolution` | `unresolved_measurement` | 10 → สร้างซ้ำไม่ตรง |

ไม่มี definition ที่ไม่ถูกแทนเปลี่ยนสถานะเลย ซึ่งเป็นพฤติกรรมที่ควรเป็นของการแทนที่แบบมีการควบคุม

**วิธีอ่านผลนี้** ชิ้นส่วนที่ถูกแทนทุกชิ้นมี geometry ตามที่ชั้นของมันต้องการแล้ว นั่นคือผลเชิงเรขาคณิตและชัดเจนไม่กำกวม แต่เจ็ดในเก้าชิ้นยังไม่มีคำตัดสิน เพราะที่ mesh factor `0.15` ตัวแก้สมการแบ่งผ่าน feature ใหม่ของมันไม่ได้ สลักได้ `0.20` element พาดสเกล feature บูชได้ `0.99` เพลาได้ `0.56` และโรเตอร์ได้ `0.64` ขณะที่การรันตระกูลชิ้นส่วนแสดงว่าชิ้นเดียวกันแบ่งผ่านได้ที่ factor `0.08` ความละเอียดจึงไม่ฟรี มันย้ายงานจากผู้สร้างแบบไปที่ตัวทำ mesh

## ส่วนที่ต่างจากแผน

แผนคาดว่าชิ้นส่วนที่ยกระดับจะได้ `passed_resolution` ในการสำรวจ แต่เจ็ดชิ้นได้ `unresolved_measurement` แทนด้วยเหตุผลเรื่อง mesh ข้างต้น มาตรฐานของการสำรวจถูกคงไว้ที่ค่าของ Work 141 โดยตั้งใจ ไม่ผ่อนและไม่ทำให้ละเอียดขึ้น เพื่อให้การสำรวจทั้งสองยังเทียบกันได้ การปรับหลังเห็นผลจะเป็นการซ่อมหลังสังเกต

## ไฟล์ที่เปลี่ยน

- `scripts/cad/detailed_part_builders.py`: builder เจ็ดแบบ พร้อมรูปทรงอ้างอิงอย่างง่ายสามแบบที่ย้ายออกมาจากตัววัด
- `scripts/cad/measure_part_resolution.py`: import builder จากไลบรารี, ผิวขบรายชิ้น, การ canonicalise ตัวนับของ STEP และการสร้างซ้ำครั้งที่สองเพื่อจับการสร้างที่ไม่ reproducible
- `scripts/structural/mesh_step_solid.py`: pin Gmsh ให้ใช้เธรดเดียว
- `src/formula_ultimate/assembly/part_resolution.py`: `threaded` ต้องมี geometry ขบทั้งสองชิ้น
- `scripts/development/build_vehicle_part_resolution_config.py`: ชุดแทนที่ผ่าน `--upgrade`
- `config/development/detailed_part_family_v1.json`, `config/development/vehicle_part_resolution_v2.json`
- `tests/test_part_resolution.py` ครอบคลุมเส้นทางที่งานนี้แตะอยู่แล้วและผ่านโดยไม่ต้องแก้
- แผนและผลลัพธ์สองภาษานี้

หลักฐานที่สร้างขึ้นยังถูก ignore ไว้ใต้ `artifacts/work142/`

## รายงานบั๊ก

1. **Gmsh คืน mesh ต่างกันสำหรับอินพุตเดียวกันระหว่างการรัน** อาการ: `family_b` ต่างจาก `family_a` ที่จำนวน node และความยาวลักษณะเฉพาะของปะเก็น ทำให้ replay ไม่ตรง สาเหตุ: Gmsh ใช้หลายเธรดโดยปริยายและชุด node ที่ได้ไม่ reproducible การแก้: pin `General.NumThreads` และ `Mesh.MaxNumThreads1D/2D/3D` เป็น 1 ในตัวเขียน geo ทั้งสอง ผลที่ต้องระบุตรง ๆ: การรันที่บันทึกไว้ก่อนการเปลี่ยนนี้ คือ Works 138, 139, 140 และ 141 จะให้ hash ต่างออกไปถ้ารันใหม่ตอนนี้ หลักฐานที่บันทึกไว้ยังคงเป็นสิ่งที่การรันเหล่านั้นให้จริง แต่ไม่สามารถสร้างซ้ำได้ภายใต้ mesher ที่ pin แล้ว
2. **boolean แบบขนานของ OCCT ทำให้ปริมาตรต่างกันหนึ่งหน่วยสุดท้าย** อาการ: ปริมาตรที่วัดของปะเก็นต่างกันที่หลักที่สิบเจ็ดระหว่างการรัน การแก้: `BOPAlgo_Options.SetParallelMode_s(False)` ในไลบรารี builder
3. **ไฟล์ STEP มีตัวนับการส่งออกต่อ process** อาการ: ส่งออก solid เดียวกันสองครั้งใน process เดียวได้ SHA-256 ต่างกัน โดยต่างกันแค่ `Open CASCADE STEP translator 7.9 1` กับ `... 2` ในชื่อ product การแก้: canonicalise ตัวนับนั้นพร้อมกับ timestamp
4. **การสร้างที่ไม่ reproducible ไม่มีสถานะรองรับ** อาการ: หลังแก้ข้อ 1 ถึง 3 แล้ว ปะเก็นยังให้ไบต์ต่างกันระหว่างการสร้างสองครั้งในการรันเดียว การแก้: ตัววัดสร้างทุกชิ้นสองครั้ง และเมื่อสองครั้งต่างกันจะบันทึก `unresolved_measurement` พร้อมสาเหตุและไม่มีตัวเลขใด เพื่อให้การรันยัง replay ได้และปัญหาปรากฏแทนที่จะแปรปรวนเงียบ ๆ ปะเก็นเป็นชิ้นเดียวในตระกูลนี้ที่เจอ โดยการสร้างของมันใช้ fillet บนชุดขอบที่เลือกหลัง boolean ซึ่งน่าจะเป็นต้นเหตุ
5. **ข้อต่อแบบเกลียวผ่านได้ด้วยเกลียวฝ่ายเดียว** อาการ: ผิวขบถูกนับรวมทั้งคู่ การแก้: นับรายชิ้น และ `threaded` ต้องมีอย่างน้อยหนึ่งผิวในแต่ละชิ้น คู่อ้างอิงจึงไม่ผ่านอย่างตรงไปตรงมา

## การตรวจสอบ

สภาพแวดล้อม: Windows 11, Python 3.14.3, CadQuery 2.8.0 ใน `.tools/cadquery-mcp`, Gmsh 4.15.0 ที่ pin เป็นเธรดเดียว

```text
Command: python -m unittest tests.test_part_resolution
Exit code: 0
Result: Ran 21 tests — OK

Command: run_part_resolution_gate.py --config config/development/detailed_part_family_v1.json --output-root artifacts/work142/family_a
Exit code: 0
Result: passed_part_resolution_gate; ผ่าน 6 / ตัดสินไม่ได้ 1; control 8/8; SHA-256 744463abe5e1daa2...

Command: คำสั่งเดิมไปที่ family_b พร้อม --replay-reference
Exit code: 0
Result: replay exact: true

Command: run_part_resolution_gate.py --config config/development/vehicle_part_resolution_v2.json --output-root artifacts/work142/survey_a
Exit code: 0
Result: passed_part_resolution_gate; ผ่าน 18 / ไม่ผ่าน 11 / ตัดสินไม่ได้ 15; control 8/8; SHA-256 8d4e4e5e926c2af5...

Command: คำสั่งเดิมไปที่ survey_b พร้อม --replay-reference
Exit code: 0
Result: replay exact: true

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1022 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests ; git diff --check ; git diff --cached --check
Exit code: 0
```

## ข้ออ้าง

- รองรับ: สร้างชิ้นส่วนเจ็ดชิ้นที่ความละเอียดที่ประกาศไว้ และหกชิ้นผ่านมาตรฐานภายใต้ mesh ที่ละเอียดพอจะแบ่งผ่านมันได้, การแทนเก้าชิ้นในการสำรวจลบคำตัดสิน `insufficient_resolution` ไปแปดรายการ และการรันทั้งสองคู่ replay ได้ตรงภายใต้ toolchain ที่ pin แล้ว
- ไม่รองรับ: ชิ้นส่วนที่ยกระดับใดถูกต้องสำหรับรถ เพราะยังไม่ได้จับคู่ขนาดกับชิ้นข้างเคียง ยังไม่ได้ติดตั้ง และยังไม่ได้ผ่าน gate การจัดวาง, ข้อต่อแบบเกลียวใดในโปรเจกต์นี้มีหลักฐานเกลียวครบทั้งสองฝั่ง และการมีหน้ามากขึ้นแปลว่าวิศวกรรมดีขึ้น

## ข้อจำกัดและงานถัดไป

- เจ็ดในเก้าชิ้นที่แทนยังไม่มีคำตัดสินในการสำรวจ จนกว่าจะทำให้ mesh ที่ลงทะเบียนละเอียดขึ้นทั้งการสำรวจ ซึ่งจะเทียบกับ Work 141 ไม่ได้เว้นแต่รัน Work 141 ใหม่ด้วย หรือจนกว่าจะมีการลงทะเบียน mesh แยกตามชั้นของชิ้นส่วน
- ต้องทำให้การสร้างปะเก็น reproducible ก่อน จึงจะมีค่าวัดใด ๆ ได้
- เกลียวในยังสร้างไม่ได้ `threaded` จึงยังผ่านไม่ได้ที่ใดเลย
- hash ที่บันทึกไว้ก่อนหน้านี้สร้างซ้ำไม่ได้ภายใต้ mesher ที่ pin แล้ว งานถัดไปควรรัน Works 138 ถึง 141 ใหม่และบันทึกตัวตนใหม่หากต้องการให้ replay ได้
