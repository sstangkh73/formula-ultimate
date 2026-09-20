# แผน Work 141: การสำรวจความละเอียดของชิ้นส่วนทั้งคัน

แหล่งภาษาอังกฤษ: `2026-09-20_141_vehicle-part-resolution-survey-plan.md`

วันที่: 2026-09-20 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์

นำ gate ของ Work 140 ไปใช้กับทุก definition ที่เป็นเนื้อวัสดุของรถ Work 135 และรายงานการกระจายของผลตัดสิน เพื่อให้ขนาดของช่องว่างด้านความละเอียดเป็นตัวเลข ไม่ใช่ความรู้สึก

## หลักฐานตั้งต้น

- Work 140 สร้าง gate และวัดหัวข้อไปเจ็ดรายการ ผล admitted คือ `b61dbe3c0f63240d174df24cf1e800eb68fc0b92c086e30fea4c93a4ce0883a5`
- รถ Work 135 ประกาศ 48 definition โดยสี่รายการเป็นช่องว่างที่ประกาศไว้และมีความหนาแน่นเชิงโครงสร้างเป็นศูนย์
- การสำรวจต้นทุน mesh ที่ factor `0.15` ที่ลงทะเบียนไว้: ชิ้นใหญ่สุดเจ็ดชิ้นใช้เวลารวม `7.7 วินาที` การสำรวจทั้งคันจึงถูกมาก ส่วน `spine_frame` ทำ mesh ที่ `0.15` ไม่สำเร็จ ทั้งที่สำเร็จที่ `0.5` และ `1.0` คาดว่าจะปรากฏเป็น `unresolved_measurement` และคำตัดสินเชิง geometry ถูกตัดสินก่อนคำตัดสินเรื่อง mesh อยู่แล้ว
- การสำรวจแบบ pilot กับทั้ง 44 definition ที่เป็นเนื้อวัสดุ รันไปก่อนที่จะเขียนบันทึกนี้ เพื่อประเมินขนาดงานและยืนยันว่าการจัดชั้นให้กลุ่มที่สมเหตุสมผล ตัวเลขของ pilot ไม่ใช่หลักฐาน admitted หลักฐานคือ `run_a` ด้านล่าง

## ขอบเขต

- `scripts/development/build_vehicle_part_resolution_config.py`: สร้าง declaration ของการสำรวจจากรถ Work 135 โดยกำหนดชั้นของแต่ละ definition ด้วยกฎที่อ่านจาก occurrence class ที่ตัวรถประกาศเอง definition ที่เป็นช่องว่างถูกตัดออกและแสดงรายชื่อไว้
- `config/development/vehicle_part_resolution_v1.json`: declaration ที่สร้างขึ้นและ commit ไว้เพื่อให้รันซ้ำได้
- runner ของ Work 140 ไม่เปลี่ยน ยกเว้นการซ่อมหนึ่งจุด คือเมื่อไม่มีหัวข้อใดผ่าน gate เชิง geometry เลย control เรื่อง mesh จะยกค่าการวัดให้สูงกว่าข้อกำหนด เพื่อให้ control ยังทดสอบได้
- แผนสองภาษานี้และผลลัพธ์สองภาษาที่ตรงกัน

## มาตรฐานที่ลงทะเบียน

เหมือน Work 140 ทุกประการ: พื้นความเป็นไปได้ในการผลิต `5e-05 m`, อย่างน้อยหนึ่ง element พาดสเกล feature ที่โมเดลไว้, mesh size factor `0.15` ส่วนข้อกำหนดของแต่ละชั้นเป็นค่าต่ำสุดเชิงวิศวกรรมที่ตั้งไว้เหนือ primitive ธรรมดา เพราะกล่องมี 6 หน้า 12 ขอบ ส่วนค่าต่ำสุดของชั้นโครงสร้างคือ 8 หน้า 14 ขอบ

## การตรวจสอบ

1. `python scripts/development/build_vehicle_part_resolution_config.py`: exit 0, 44 ชิ้น, ตัดช่องว่างออก 4 รายการ
2. `python scripts/development/run_part_resolution_gate.py --config config/development/vehicle_part_resolution_v1.json --output-root artifacts/work141/run_a`: exit 0, control แปดข้อถูกปฏิเสธ, ทุก definition มีสถานะที่ลงทะเบียนหนึ่งค่า
3. runner ตัวเดิมไปที่ `run_b` พร้อม `--replay-reference`: exit 0 และ result SHA-256 ตรงกัน
4. `python -m unittest tests.test_part_resolution -v`, `python -m unittest discover -s tests`, `python -m unittest tests.test_repository_contract -v`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0

## เกณฑ์สำเร็จและล้มเหลว

สำเร็จ: ทุก definition ที่เป็นเนื้อวัสดุมีสถานะที่ลงทะเบียนหนึ่งค่าพอดี การจัดชั้นเป็นกฎที่ตรวจสอบได้ control ทั้งหมดถูกปฏิเสธ และ replay ตรงทุกประการ

ล้มเหลว: มี definition หลุดจากการสำรวจ, มีการผ่อนข้อกำหนดหลังเห็นการกระจายของผล หรือมีการนำเสนอผลว่าเป็นคำตัดสินเรื่องสมรรถนะของรถแทนที่จะเป็นเรื่อง geometry

## ความเสี่ยงและสิ่งที่ไม่ทำ

- ความเสี่ยง: ชิ้นส่วนสัดส่วนมากของรถจะไม่ผ่าน นั่นคือผลการวัด และจะรายงานตามที่พบ
- ความเสี่ยง: การจัดชั้นอาจเข้าข้างรถ วิธีรับมือ: กฎถูกกำหนดก่อนรัน อ่านจาก occurrence class เท่านั้น และพิมพ์ออกมาพร้อม declaration ที่สร้าง
- สิ่งที่ไม่ทำ: ไม่ออกแบบชิ้นส่วนใดใหม่, ไม่แก้สมการ contact, ไม่เชื่อมกับเวลาแข่ง, ไม่ push และไม่เขียนประวัติใหม่
