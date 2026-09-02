# ตัวควบคุม Corridor แบบ Closed Loop V1

แปลจากไฟล์ภาษาอังกฤษ: `CLOSED_LOOP_CORRIDOR_CONTROLLER_V1.md`

## ขอบเขตข้อกล่าวอ้าง

Work 074 ปิด steering feedback รอบ plant ของ Work 073 ซึ่งรวม drivetrain, planar, sprung-body, suspension, tyre และ road นี่เป็นการทดลอง tracking สังเคราะห์ระดับ Level 0 ระยะ `0.5 s` แบบ deterministic ไม่ใช่ autonomous racing, optimal racing line หรือการตรวจสอบสนามจริง

## วิธีการ

`CircuitCorridor` ที่ประกาศถูก sample ด้วยระยะไม่เกิน `0.1 m` ตำแหน่งรถถูกฉายตั้งฉากลงแต่ละช่วง polyline พร้อมเก็บ signed cross-track error `e_y`, desired heading, curvature, ความกว้าง และ centreline progress สำหรับ wheelbase `L` ที่ได้จาก geometry ของ contact:

```text
delta_ff = atan(L kappa)
delta_raw = delta_ff - K_heading e_heading - K_cross e_y
delta = clamp(delta_raw, -0.03 rad, +0.03 rad).
```

การ clamp ไม่ถูกซ่อน ทุก saturated command ถูกนับและเก็บค่าก่อน clip คำสั่งที่ใช้ถูกส่งเข้า Work 073 ก่อน physical step แต่ละขั้น Corridor departure เกิดเมื่อ signed centreline error เกินความกว้างด้านนั้นหลังหัก half-envelope `0.65 m`

## การทดลองและผล

กรณีอ้างอิงใช้วงกลมซ้ายสังเคราะห์รัศมี `50 m`, lateral disturbance เริ่มต้น `0.25 m`, heading disturbance `0.03 rad`, `K_heading = 0.8`, `K_cross = 0.2 rad/m`

- cross-track error เริ่มต้น/สุดท้าย `0.24999987503241972 m` / `0.02307508195600006 m`;
- zero-feedback final error `0.3772375000371769 m`;
- wrong-sign final error `0.46591408662822736 m`;
- tracking error สัมบูรณ์สูงสุด `0.2620130810314983 m`;
- progress ใน `0.5 s` คือ `5.39206238640666 m`;
- actual normal load ต่ำสุด `290.149480377666 N`;
- suspension travel สูงสุด `0.011457919570257338 m`;
- combined relative energy residual สูงสุด `4.73869100213051e-9`;
- mirror residual `1.1102230246251565e-16`;
- ความต่าง half-step `0.0003151468688774861`.

กรณีอ้างอิง saturation `348/500` steps นี่คือข้อจำกัด control authority ที่มองเห็นได้ ไม่ใช่ความสำเร็จที่ซ่อนการ clip: feedback ยังลด final error ประมาณ `94%` เทียบ zero feedback ในช่วงสั้น แต่จำนวน saturation สูงแสดงว่ายังไม่ควรเรียกว่า tune พร้อมหนึ่งรอบ Saturation control แยกต่างหาก saturation ครบ `500` steps Initial-departure control ให้ `DNF: corridor_departure` ก่อนรัน plant step ส่วน straight และ right-circle mirror ผ่าน

Fixed-steer Work 073 ที่ไม่เปลี่ยนยังมี SHA-256 `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973` Work 074 result SHA-256 คือ `a400e8a9c1c0768d11647aa6c2fde3855a5d12898b548edef0b2fd6911244374`; canonical evidence SHA-256 คือ `9572a793e45713ee9768d3bca7ead9460ce3d1fe1824d6cee273b89e7737efea`; primary/replay file SHA-256 ที่เหมือนกันทุกไบต์คือ `B21A66201270C99CB0177CA6A4BF82755DDF734C6F1EACFF46ACB7A78C84FE5B`

## การตีความและข้อจำกัด

Feedback เครื่องหมายถูกต้องทำได้ดีกว่าทั้ง zero feedback และ wrong-sign feedback จึงสนับสนุนสมมติฐานเชิงเหตุ Mirror, straight, replay และ half-step controls ลดคำอธิบายทางเลือกด้านเครื่องหมายและตัวเลข จำนวน saturation สูงเป็นหลักฐานขัดแย้งว่า authority/tuning ยังไม่พอสำหรับการแข่งต่อเนื่อง

การฉายลง sampled polyline เป็นค่าประมาณและอาจเลือก station กำกวมตรง seam ของ closed loop ไม่มี speed controller, braking, actuator model, latency, noise, estimator, look-ahead optimization, obstacle/traffic response, real corridor survey หรือ learning Work 076 ต้องไม่ให้หนึ่งรอบจาก scalar distance อย่างเดียว แต่ต้องตรวจ spatial containment และ seam ชัดเจน
