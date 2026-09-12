# ชุด Actuation ที่มีฮาร์ดแวร์รองรับ V1

แหล่งภาษาอังกฤษ: `REALIZED_ACTUATION_CHAIN_V1.md`

Status: Work 119 นำไปใช้เป็นหลักฐาน reference แบบมีขอบเขตที่ Level-0

## Route ที่ทำจริงและขอบเขตหลักฐาน

Contract นี้ตรึงอัตลักษณ์ motion/load จาก Work 114, thermal จาก Work 115 และ material scope จาก Work 116 Route ลดรอบแบบ rotary coaxial synthetic ที่เปิดเผยหนึ่งเส้นทางเชื่อม port torque/speed ขาเข้าและขาออก ผ่าน transfer member ทรงกระบอกสองชิ้น support สี่จุด containment shell และ coupler โดย geometry ที่ลงทะเบียนกำหนด mass, torsional stiffness/stress และ reaction load Route นี้เป็น reference ที่รับเข้า ไม่ใช่ข้อบังคับถาวรว่าข้อเสนออื่นต้องใช้ gear, shaft, motor หรือเทคโนโลยีใด

Ratio คือ `3.5`; ขีดจำกัด input คือ `80 N*m`, `300 rad/s` และ `280-360 K` กฎ loss แบบ synthetic ที่เปิดเผยกำหนด fractional, fixed, speed, torque และ temperature loss ทุก operating point ที่รับเข้าต้องมี accepted input power เท่ากับ output power บวก heat/loss ภายใน `1e-10 W` Output work และ loss energy ใช้ช่วงที่ลงทะเบียน `5 s`

## Control และข้อจำกัด

Response map มีสาม speed, สาม torque และสอง temperature บังคับ control disconnected, locked-output, reverse, saturated-demand, removed-support และไม่มี transfer member Route ที่ตัดไม่รับ input/output energy; output ที่ล็อกส่ง admitted power ไป modeled heat; การย้อนทิศคงขนาด power/loss; support หรือ hardware ที่ขาด fail closed

Conversion route อื่นต้องมีกฎและ hardware coverage ที่ตรวจเอง Material eligibility จาก Work 116 ยังคง blocked Contract นี้ไม่ยืนยัน measured efficiency, material survival, fatigue/wear, รายละเอียด bearing/fastener, controller hardware, เทคโนโลยีที่เหนือกว่า หรือ physical validation
