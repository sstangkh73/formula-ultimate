# Motion Ratio ของ Linkage ที่คำนวณจาก Geometry V1

แปลจากไฟล์ภาษาอังกฤษ: `GEOMETRY_LINKAGE_MOTION_RATIO_V1.md`

## ขอบเขตข้อกล่าวอ้างและสมการ

Work 075 แทนการกระจัด spring/wheel แบบหนึ่งต่อหนึ่งโดยปริยายของ Work 073 ด้วย rigid-rocker transform แบบ small-angle ที่คำนวณจากจุดและทิศ 3D ที่ประกาศ เป็นหลักฐาน geometry-causal ระดับ Level 0 แต่จุดยังเป็นค่าประกาศสังเคราะห์ ไม่ใช่การวัด joint จาก STEP/FreeCAD

สำหรับแกนหมุน rocker หน่วย `a`, pickup arm `r` และทิศการกระจัดหน่วย `d`, projected lever คือ:

```text
l = d dot (a cross r)
motion ratio R = l_spring / l_wheel
k_wheel = k_spring R^2
c_wheel = c_spring R^2
travel_wheel = travel_spring / R.
```

เครื่องหมายต้องเป็นบวกเพื่อให้ spring compression ตรงกับ wheel compression แขนฉายเป็นศูนย์ เครื่องหมายตรงข้าม contact ขาด และ geometry non-finite ต้อง fail closed แกนและทิศถูก normalize จึงเปลี่ยน ratio ด้วยการคูณขนาดเวกเตอร์ไม่ได้

## การทดลองและผล

Geometry ที่เลือกของ powered contact ใช้ projected spring arm `0.16 m` และ wheel arm `0.20 m` ได้ `R = 0.7999999999999999` Rear contact ได้ `R = 1.0` ดังนั้น stiffness/damping ที่พิกัดล้อ powered scale `0.64` และ wheel travel scale `1.25`

Work 073 ที่ transform แล้ววิ่งจบด้วย:

- heave สูงสุด `0.0008656698982980348 m`;
- suspension travel สูงสุด `0.019278824606844512 m`;
- actual normal load ต่ำสุด `266.8789268655951 N`;
- combined relative energy residual สูงสุด `5.0778645277023315e-9`.

Geometry unit-ratio รักษา Work 073 result SHA-256 พอดีที่ `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973` การเปลี่ยน spring pickup หนึ่งจุดจาก `0.16 m` เป็น `0.18 m` เปลี่ยนทั้ง application และ coupled-result identity Axis scaling, linkage permutation และ mirrored geometry รักษา ratio ส่วนกรณี degenerate/ทิศตรงข้ามถูกปฏิเสธ

Selected application SHA-256 คือ `51b6255347e4a6a59428ee309f4f78c8e981baa437386bdcf3505df9d8403487`; coupled result SHA-256 คือ `7fd4af71e95dc49be5330762efe284a20a0ac86bc73b19df6a17c41d0e0b552a`; canonical evidence SHA-256 คือ `69d4ad48f82026fdca4134a0c00519f9dc4df837cb43c2ad0608b7eafe16c939`; primary/replay file SHA-256 ที่เหมือนกันทุกไบต์คือ `37864D0AE558AFBEB4E2E90B63DE1A48D84C17D4C6B8EC6EB106414E02A2DE64`

## การตีความและหลักฐานที่ขาด

Unit-ratio preservation และ geometry mutation สนับสนุนว่า virtual-work coupling ถูกต้อง ไม่ใช่ geometry field สำหรับตกแต่ง อย่างไรก็ตาม transform ปัจจุบันเป็น local/linear ไม่รวม finite-angle arc, pushrod articulation, joint/bearing compliance, backlash, friction, collision, anti-dive/squat, structural load และการดึงจาก CAD topology จริง ความเชื่อมั่นสูงต่อ transform small-angle ที่ประกาศ และต่ำว่าจุดสังเคราะห์นี้เป็น suspension ที่สร้างได้
