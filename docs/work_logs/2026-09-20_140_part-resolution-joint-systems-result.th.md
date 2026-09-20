# ผลลัพธ์ Work 140: ความละเอียดของชิ้นส่วนและระบบข้อต่อ

แหล่งภาษาอังกฤษ: `2026-09-20_140_part-resolution-joint-systems-result.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

คำว่า "ละเอียดพอ" และ "ข้อต่อจริง" กลายเป็น gate ที่วัดได้แล้ว ไม่ใช่ความเห็น งานนี้สร้าง วัด ทำ mesh และตัดสินชิ้นส่วนเจ็ดชิ้นกับข้อต่อสามจุด control ทั้งแปดข้อถูกปฏิเสธ และการ replay บน tree ที่สะอาดให้ result SHA-256 ตรงกันทุกประการ

คำตัดสินต่อรถที่มีอยู่คือข้อค้นพบของงานนี้ คือ **ตัวยึดและน็อตของ Work 135 ไม่ผ่านมาตรฐานความละเอียด** และ **ข้อต่อของชุดยึด Work 135 ไม่มีผิวเกลียวที่วัดได้เลย**

## ผลที่วัดได้

Result SHA-256 `b61dbe3c0f63240d174df24cf1e800eb68fc0b92c086e30fea4c93a4ce0883a5` และ `run_b` ตรงกันทุกประการ มาตรฐานที่ลงทะเบียน: พื้นความเป็นไปได้ในการผลิต `5e-05 m`, อย่างน้อยหนึ่ง element พาดสเกล feature ที่โมเดลไว้, mesh size factor `0.15` และสำหรับชั้น `fastener` ต้องมีอย่างน้อย 12 หน้า 4 หน้าโค้ง 20 ขอบ และ 3 สเกลที่ห่างกันระดับสิบเท่า

| ชิ้นส่วน | สถานะ | หน้า | โค้ง | ขอบ | สเกล | ขอบสั้นสุด | สเกล feature | element พาด |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `work135_bolt` | `insufficient_resolution` | 5 | 2 | 6 | 3 | 6.00 mm | 6.00 mm | 1.37 |
| `work135_nut` | `insufficient_resolution` | 9 | 1 | 21 | 2 | 6.00 mm | 6.00 mm | 15.99 |
| `reference_m8_bolt` | `passed_resolution` | 34 | 17 | 85 | 5 | 0.0843 mm | 0.764 mm | 1.14 |
| `bond_plate_lower` / `bond_plate_upper` | `passed_resolution` | 6 | 0 | 12 | 2 | 5.00 mm | 5.00 mm | 4.63 |
| `press_bushing` | `passed_resolution` | 4 | 2 | 6 | 1 | 10.0 mm | 10.0 mm | 20.95 |
| `press_shaft` | `passed_resolution` | 3 | 1 | 3 | 1 | 12.0 mm | 12.0 mm | 33.39 |

| ข้อต่อ | เทคโนโลยี | สถานะ | ระยะสวม | คู่ผิวสัมผัส | ผิวขบ |
| --- | --- | --- | ---: | ---: | ---: |
| `work135_pack_threaded` | `threaded` | `unsupported_joint_evidence` | 0.000 mm | 3 | **0** |
| `reference_bonded_lap` | `bonded` | `passed_joint_evidence` | 0.150 mm | 21 | 0 |
| `reference_interference_fit` | `interference` | `passed_joint_evidence` | −0.0200 mm | 3 | 0 |

- **ตัวยึดของรถคือทรงกระบอกสองชิ้น** ที่วัดได้: 5 หน้า 6 ขอบ และไม่มีผิวที่ไม่ใช่ระนาบหรือทรงกระบอกเลยแม้แต่หน้าเดียว ส่วนตัวยึดอ้างอิงที่งานนี้สร้างขึ้นที่ระดับความละเอียดของชิ้นส่วนจริง มีเกลียว ISO ที่กวาดจริง หัวหกเหลี่ยม เบ้าหกเหลี่ยม และมุมลบที่หัว วัดได้ 34 หน้า 17 หน้าโค้ง 85 ขอบ และห้าสเกลที่ห่างกันระดับสิบเท่า โดยขอบสั้นสุด `0.0843 mm` ซึ่งละเอียดกว่าสิ่งใดในตัวยึดของรถถึง 71 เท่า
- **ข้อต่อของตัวยึดในรถไม่มีเกลียว** gate พบคู่ผิวสัมผัสและระยะสวมเป็นศูนย์ แปลว่าสองชิ้นสัมผัสกันจริง แต่มีผิวขบเป็นศูนย์ คือไม่มี geometry ให้เกลียวรับแรง เทคโนโลยี `threaded` ที่ประกาศไว้จึงไม่มี geometry รองรับ
- **สองเทคโนโลยีผ่านด้วยการวัดล้วน ๆ** ข้อต่อกาวแบบซ้อนทับวัดชั้นกาวได้ `0.150 mm` เทียบช่วงที่ประกาศ `0.100–0.200 mm` พร้อมพื้นที่ซ้อนทับ `5.60e-03 m^2` ส่วนการสวมอัดวัดความลึกการกดทับได้ `−0.0200 mm` เทียบช่วงที่ประกาศ `−0.030 ถึง −0.010 mm` ซึ่งได้จาก solid ที่ตัดกันด้วยสูตร `2V/A` ทั้งสองค่าประกาศไว้ก่อนรันและไม่ได้ปรับภายหลัง
- **มาตรฐานนี้เป็นกลางทางเทคโนโลยี** ไม่มีข้อใดในทะเบียนบังคับให้ใช้ตัวยึด การเชื่อม การใช้กาว การสวมอัด หรือการขึ้นรูปเป็นชิ้นเดียว ต่างผ่าน gate ได้ด้วยหลักฐานที่วัดได้ของตัวเอง

## ส่วนที่ต่างจากแผน

แผนระบุน็อตอ้างอิงที่มีเกลียวใน แต่การสำรวจความสามารถพบว่า boolean คืนรูที่ไม่มีเกลียวอย่างเงียบ ๆ ไปแล้ว เทคโนโลยี threaded ในการรัน admitted จึงใช้ชุดยึดของ Work 135 ซึ่งไม่ผ่าน และเทคโนโลยีที่ผ่านคือ bonded กับ interference ข้อจำกัดของ kernel ถูกบันทึกไว้ด้านล่าง ไม่ใช่กลบด้วยการประกาศว่าน็อตมีเกลียว

การรัน pilot กำหนดค่าที่ลงทะเบียนสองค่าก่อนการรัน admitted คือ mesh size factor เปลี่ยนจาก `1.0` เป็น `0.15` หลัง pilot แสดงค่า `0.24` แล้ว `0.77` element พาดสเกล feature ของตัวยึดอ้างอิง และข้อกำหนดของแต่ละชั้นชิ้นส่วนตั้งจากผลวัดใน pilot ไม่มีการเปลี่ยนค่าใดหลังการรัน admitted

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/assembly/part_resolution.py`
- `scripts/cad/measure_part_resolution.py`
- `scripts/development/run_part_resolution_gate.py`
- `config/development/part_resolution_gate_v1.json`
- `tests/test_part_resolution.py`
- `docs/contracts/PART_RESOLUTION_GATE_V1.md` และคู่ภาษาไทย
- `docs/plans/detailed_part_to_vehicle_v1/work140-part_resolution_joint_systems.md` คู่ภาษาไทย และดัชนีสองภาษา
- แผนและผลลัพธ์สองภาษานี้

หลักฐานที่สร้างขึ้นยังถูก ignore ไว้ใต้ `artifacts/work140/{pilot,run_a,run_b}`

## รายงานบั๊ก

1. **การตัดเกลียวในไม่เอาเนื้อออก** อาการ: การตัด helix ที่กวาดแล้วออกจากน็อตหกเหลี่ยม ทำให้รูยังไม่มีเกลียว คือมี 23 หน้าโดยไม่มีหน้าอิสระเลย และปริมาตรเท่ากับรูเรียบ ขณะที่การกวาดแบบเดียวกันเชื่อมเป็นเกลียวนอกได้ถูกต้อง สาเหตุ: ยังสรุปไม่ได้ ดูเหมือน OCCT คืนรูปทรงเดิมเมื่อ boolean ล้มเหลวกับเครื่องมือที่กวาดแล้วตัดตัวเอง การจัดการ: ไม่ประกาศว่าน็อตใดมีเกลียว บันทึกข้อค้นพบไว้และยกเรื่องเกลียวในให้งานถัดไป
2. **รัศมีโคนใต้หัวถูกปฏิเสธ** อาการ: `StdFail_NotDone` เมื่อใส่ fillet ที่ขอบใต้หัวของตัวยึดอ้างอิง การจัดการ: ตัด fillet ออก และชิ้นส่วนอ้างอิงยังผ่านมาตรฐานได้โดยไม่มีมัน
3. **ตัววัดสมมติว่าผลลัพธ์อยู่ใน checkout** อาการ: `ValueError: ... is not in the subpath of 'C:\Formula Ultimate'` เมื่อการทดสอบเขียนลงไดเรกทอรีชั่วคราว การแก้: `_repository_path` คืน path ที่อ้างอิงรากของ repository เมื่อทำได้ และคืน path แบบเต็มเมื่อทำไม่ได้
4. **การตกเรื่อง geometry บังคำตัดสินเรื่อง mesh** อาการ: control `mesh_too_coarse_for_feature` ไม่ถูกปฏิเสธ เพราะหัวข้อของมันคือชิ้นส่วนที่วัดได้ชิ้นแรก ซึ่งตกเรื่องความละเอียดไปก่อน การแก้: ประเมิน gate เชิง geometry ก่อน gate เรื่อง mesh และให้ control เลือกหัวข้อที่ผ่าน gate เชิง geometry แล้ว ส่วนความล้มเหลวของ mesh ยังถูกบันทึกใน `mesh_failure`

## การตรวจสอบ

สภาพแวดล้อม: Windows 11, Python 3.14.3, CadQuery 2.8.0 ใน `.tools/cadquery-mcp`, Gmsh 4.15.0 จาก `C:/Program Files/FreeCAD 1.1/bin`

```text
Command: python -m unittest tests.test_part_resolution
Exit code: 0
Result: Ran 21 tests — OK (การทดสอบที่วัดด้วย CadQuery รันจริง และจะข้ามเมื่อไม่มี runtime)

Command: python scripts/development/run_part_resolution_gate.py --config config/development/part_resolution_gate_v1.json --output-root artifacts/work140/run_a
Exit code: 0
Result: passed_part_resolution_gate; ชิ้นส่วนผ่าน 5 / ไม่ผ่าน 2; ข้อต่อผ่าน 2 / ไม่มีหลักฐาน 1;
        control 8/8 ถูกปฏิเสธ; result SHA-256 b61dbe3c0f63240d174df24cf1e800eb68fc0b92c086e30fea4c93a4ce0883a5

Command: python scripts/development/run_part_resolution_gate.py --config ... --output-root artifacts/work140/run_b --replay-reference artifacts/work140/run_a/result.json
Exit code: 0
Result: replay exact: true

Command: python -m unittest discover -s tests
Exit code: 0
Result: Ran 1022 tests — OK (skipped=11)

Command: python -m compileall -q src scripts tests
Exit code: 0

Command: python -m unittest tests.test_repository_contract
Exit code: 0
Result: Ran 6 tests — OK

Command: git diff --check ; git diff --cached --check
Exit code: 0
```

## ข้ออ้าง

- รองรับ: โปรเจกต์มีนิยามที่วัดได้ของความละเอียดชิ้นส่วนและนิยามที่เป็นกลางทางเทคโนโลยีของหลักฐานข้อต่อแล้ว, ตัวยึดและน็อตของ Work 135 ต่ำกว่ามาตรฐานนั้น, ข้อต่อของตัวยึดใน Work 135 ไม่มี geometry ของเกลียว และตัวยึดที่ระดับความละเอียดที่ต้องการสร้างและ mesh ได้ใน toolchain นี้
- ไม่รองรับ: ส่วนที่เหลือของรถ Work 135 ผ่านหรือไม่ผ่านมาตรฐาน เพราะวัดเฉพาะตัวยึดกับน็อต, ข้อต่อใดรับโหลดได้ เพราะยังไม่ได้แก้สมการแรงข้ามผิวต่อ และเรื่องความเป็นไปได้ในการผลิต เวลาแข่ง หรือ physical validation

## ข้อจำกัดและงานถัดไป

- วัดไปเจ็ดชิ้นจาก 48 definition การรัน gate กับรถทั้งคันเป็นก้าวถัดไปที่ชัดเจนและถูก เพราะการรัน admitted ใช้เวลาราว 45 วินาที
- ยังไม่มีการแก้สมการแบบ contact หรือ tied surface หลักฐานของผิวต่อเป็นเชิงเรขาคณิตล้วน
- ข้อกำหนดความละเอียดเป็นกฎเชิงนับ ซึ่งกันการโกงแบบหยาบได้ แต่ในหลักการชิ้นส่วนยังเพิ่ม feature ที่ไม่มีหน้าที่ได้ การตรวจเชิงหน้าที่ควรอยู่ที่ evaluator ไม่ใช่ที่นี่
- เกลียวในยังสร้างไม่ได้ใน toolchain นี้ คู่เกลียวที่สมบูรณ์จึงยังผ่านเทคโนโลยี `threaded` ไม่ได้
- ถัดไป: ใช้ gate กับทั้ง 48 definition ของ Work 135 แล้วรายงานการกระจายของผล จากนั้นยกระดับชิ้นที่ไม่ผ่านและวัดใหม่
