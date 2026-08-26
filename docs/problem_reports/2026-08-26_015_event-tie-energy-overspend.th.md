# รายงานปัญหา Work 015: Event Tie Exact กลายเป็น Numerical Energy Overspend

ต้นฉบับภาษาอังกฤษ: `2026-08-26_015_event-tie-energy-overspend.md`

สถานะ: Resolved

## ปัญหา

Test หักล้างสร้าง race ที่ finish, primary-energy depletion และ timeout เกิดที่
เวลา analytical เดียวกัน (`10 s`) Tie priority ที่ประกาศต้องให้ `finished`
แต่ implementation แรกให้ `invalid`:

```text
runtime numerical failure: event ordering overspent onboard energy by
0.000244140625 J
```

Energy scale คือ `1354976035920.0 J` ดังนั้น overspend เป็น floating-point
residual สัมพัทธ์ประมาณ `1.8e-16` ไม่ใช่แหล่งพลังงานที่ไม่ประกาศอย่างมีสาระ

## Root cause และผลกระทบ

Finish localization ใช้ first-true bisection bound ส่วน depletion ใช้ last
non-overspending bound เมื่อเป็น physical tie exact ขอบ floating-point ที่ติดกัน
อาจคร่อม event ทางคณิตศาสตร์ การเลือก finish แล้วประเมิน source energy บนขอบบน
ทำให้ remaining energy ติดลบเล็กมาก Guard ที่ห้ามค่าติดลบแบบไม่มี tolerance จึง
เปลี่ยน tie ที่ประกาศเป็น `invalid` และขัด deterministic event semantics

หากไม่แก้ candidate ที่ขอบ finish/energy อาจได้ผลตาม representational rounding
แทนกฎ race ที่ประกาศ

## วิธีแก้ที่วางแผน

1. เพิ่ม absolute/relative energy-event tolerance ชัดเจนใน race control และ
   replay metadata
2. เก็บ raw signed boundary residual ใน step และ terminal telemetry
3. เมื่อ event priority สูงกว่าเป็น `finished` หรือ `failed` ใช้ energy เกิน
   เฉพาะภายใน scaled tolerance ให้ usable remaining energy เป็นศูนย์ แต่เก็บ raw
   residual ติดลบเป็นหลักฐาน
4. Overspend เกิน tolerance ยังคง `invalid`
5. กำหนด exact triple-tie test ให้คืน `finished`, remaining energy ไม่ติดลบ และ
   boundary residual `-0.000244140625 J` ที่สังเกตได้
6. รัน validation Work 015 และ repository ทั้งหมดก่อน mark report resolved

Tolerance นี้แก้เฉพาะ numerical event coincidence ไม่อนุญาต energy replenishment
หรือซ่อน deficit ที่มีนัยทางฟิสิกส์

## หลักฐานการแก้ไข

Control, replay metadata, step telemetry และ terminal result แสดง energy-event
tolerance และ signed boundary residual แล้ว Exact triple tie คืน `finished`,
usable remaining energy `0.0 J` และ residual `-0.000244140625 J` เมื่อรันซ้ำโดย
ตั้ง tolerance ทั้งคู่เป็นศูนย์จะคืน `invalid` พร้อมเหตุผล overspend Tests เฉพาะ
งาน (`10`) และ repository ทั้งหมด (`110`) ผ่าน Validator reproduce tie ที่แก้แล้ว
และรายงาน replenishment event ศูนย์
