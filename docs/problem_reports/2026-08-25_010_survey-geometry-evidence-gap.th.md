# รายงานปัญหา Work 010: ช่องว่าง Geometry สนามระดับ Survey

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_010_survey-geometry-evidence-gap.md`

สถานะ: แก้ที่ขอบเขตโมเดลและหลักฐานแล้ว

## ปัญหา

ชุดแหล่งข้อมูลสนาม 10 สนามจาก Work 008 มีข้อเท็จจริงขนาดเรซทางการ คำอธิบาย
สนามเชิงคุณภาพ และค่าความกว้างที่เผยแพร่เพียงบางส่วน แต่ไม่มี centerline 3D
ระดับ survey พร้อมขอบซ้าย/ขวา geometry ของ wall/kerb, coordinate reference
system, timestamp และ uncertainty เชิงตัวเลขครบทุก layout

หากไม่มี field เหล่านี้ จะปกป้องผล admission จาก whole-vehicle swept volume บน
สนามจริงไม่ได้ การตีความ map image เป็น dimensional survey หรือกรอก curvature,
grade, banking และ width ที่ขาดด้วยค่าที่ดูสมเหตุผลจะสร้างหลักฐานฟิสิกส์ปลอม

## ผลกระทบ

- ยัง hard-screen ความยาวรถ wheelbase, steering lock และ overhang บนสนามจริง
  ทั้ง 10 layout ไม่ได้
- การผ่าน static minimum width ไม่พิสูจน์ว่ารถเลี้ยว hairpin ผ่าน
- Corridor solver อาจดูเหมือนเสร็จแต่อนุมัติดีไซน์จาก geometry ที่สร้างขึ้นเอง

## หลักฐานที่ตรวจ

- `config/circuits/real_circuits_v1.json` ไม่มีพิกัด station หรือ boundary จาก
  การสำรวจ
- Work 008 มี width evidence ที่ใช้ได้เพียง 4 profile และระบุอีก 6 profile เป็น
  indeterminate อย่างชัดเจน
- หน้าสรุปสนามและ event map ทางการที่ Work 008 อ้างอิงให้ข้อเท็จจริงระดับรอบหรือ
  diagram แต่ไม่ให้ survey และ uncertainty แบบ machine-readable ครบชุดที่
  โมเดลนี้ต้องใช้

รายงานนี้ไม่ได้อ้างว่าไม่มี private homologation หรือ engineering survey อยู่
แต่บันทึกว่าไม่มี survey dataset ที่อนุญาต admission อยู่ในหลักฐาน public/
repository ที่ตรวจ

## สาเหตุราก

ข้อมูล homologation, construction และ survey ของสนามเป็น operational asset
เฉพาะทาง ข้อมูลเรซสาธารณะถูกสร้างเพื่อการกีฬา/งานอีเวนต์และมักไม่เปิดหลักฐาน
boundary ระดับพิกัดที่ต้องใช้ตรวจ vehicle collision clearance อย่างอิสระ

## ทางลัดที่ปฏิเสธ

- trace marketing map ที่ไม่มี scale
- สมมติว่าความกว้างที่เผยแพร่ค่าเดียวใช้ได้ทุกตำแหน่ง
- อนุมานรัศมีจากชื่อโค้งหรือรูปร่างที่เห็นในภาพ
- ตั้ง curvature, grade หรือ banking ที่หายเป็นศูนย์
- เรียก geometry ประมาณแบบ OpenStreetMap/GPS ว่า survey-grade โดยไม่มี
  uncertainty audit
- ให้ synthetic verification fixture อนุมัติการแข่งจริง

## วิธีแก้

Work 010 แก้ปัญหาด้านวิศวกรรม/ซอฟต์แวร์ดังนี้:

1. กำหนด corridor import contract แบบมี version พร้อมหน่วย SI, convention ของ
   พิกัด/sign, source identity, evidence class และ uncertainty
2. อนุญาต `admitted` เฉพาะ evidence class ที่มีสิทธิ์ admission Geometry แบบ
   approximate, digitized, synthetic หรือ real geometry ที่ขาดต้องคืน
   `indeterminate` แม้ผ่าน mathematical check
3. ใช้ analytical fixture ทางตรงและรัศมีคงที่ที่โปร่งใสเพื่อตรวจสมการ steering
   และ swept envelope แยกจากคำอ้างสนามจริง
4. แสดง closure error, minimum margin, required steering และ segment แรกที่ fail
5. คง record corridor สนามจริงที่หลักฐานไม่พอเป็น unresolved จนกว่าจะนำเข้า
   licensed survey, engineering export จาก circuit operator หรือแหล่งที่ตรวจ
   ย้อนกลับเทียบเท่าได้

## การตรวจที่ต้องผ่านเพื่อปิด Work 010

- synthetic mathematical pass ต้องไม่ให้ผล `admitted`
- real profile ที่ไม่มีหลักฐานต้องคืน `indeterminate`
- analytical fixture class surveyed สามารถให้ผล `admitted`
- กรณี static-fit/swept-fail และ steering-fail ต้อง reject พร้อมเหตุผล
- evidence class, uncertainty และ geometry ที่ผิดต้อง fail validation

## ข้อจำกัดคงเหลือและงานติดตาม

ช่องว่างหลักฐานถูกกำหนดขอบเขต ไม่ได้ถูกแปลงเป็น geometry จริง การจัดหาและ license
ข้อมูล survey-grade ยังเป็นงานติดตาม เมื่อได้ข้อมูลต้องนำเข้าผ่าน contract ที่
ประกาศ ตรวจ coordinate/frame และ closure อย่างอิสระ และทำ version โดยไม่เปลี่ยน
ความหมายของผลทดลองก่อนหน้า
