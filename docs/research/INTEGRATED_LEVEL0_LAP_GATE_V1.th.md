# Gate หนึ่งรอบแบบ Closed Loop ระดับ Level 0 ที่รวมระบบ V1

แปลจากไฟล์ภาษาอังกฤษ: `INTEGRATED_LEVEL0_LAP_GATE_V1.md`

## ขอบเขตข้อกล่าวอ้าง

Work 076 รวม controller Work 074, geometry-derived linkage transform Work 075, vertical road/tyre/body dynamics Work 073 และ drivetrain/planar plant เดิม แสดงหนึ่งรอบแบบ deterministic บนวงกลม analytical รัศมี `50 m` ภายใต้สมมติฐานสังเคราะห์ Level 0 นี่ไม่ใช่รอบสนามจริง, optimized lap time, physical validation, safety evidence หรือหลักฐานว่ารถครบถ้วน

## ตรรกะการรับรอง

ไม่ให้หนึ่งรอบจาก scalar distance อย่างเดียว แต่ละ step ฉายสถานะ physical `(x,y)` ลง corridor ที่ประกาศ แกะ centreline progress ข้าม seam ของ closed loop และตรวจ:

```text
progress_delta <= planar_spatial_distance + 0.02 m
abs(cross_track) <= applicable_half_width - 0.65 m
N_actual,i > 0
suspension travel within transformed linkage limits
combined energy residual <= 0.001.
```

Finish ถูก localize ระหว่าง physical states สองจุดที่คร่อมความยาว corridor หนึ่งรอบพอดี Finish pose ที่ interpolate แล้วต้องกลับมาไม่เกิน `0.15 m` จากตำแหน่งรถเริ่มต้นและไม่เกิน `0.02 rad` จาก orientation เริ่มต้น การเทียบใช้ initial vehicle pose ไม่จำเป็นต้องเป็น centreline tangent เพราะ steady cornering อาจต้องมี body slip/heading offset ที่ไม่เป็นศูนย์

## ผลอ้างอิง

Linkage ratios ที่เลือกคือ `0.8 / 1.0 / 0.8` Controller เริ่มด้วย heading offset `0.06 rad`, ใช้ `K_heading = 0.6`, `K_cross = 0.15 rad/m`, steer สูงสุด `0.03 rad`, throttle `0.3`, `dt = 0.005 s`

- credited progress พอดี `314.1592653589793 m`;
- localized lap time `22.14108931044568 s` หลัง `4429` executed steps;
- finish position residual `0.047685317265362355 m`;
- finish heading residual `3.56130463712072e-05 rad`;
- cross-track error สัมบูรณ์สูงสุด `0.0714069338543296 m`;
- steering saturation `0` ครั้ง;
- actual normal load ต่ำสุด `156.44738786029893 N`;
- suspension travel สูงสุด `0.024331844801589377 m`;
- combined relative energy residual สูงสุด `7.449174538254737e-08`;
- progress-versus-spatial residual สูงสุด `0.0007138905266217827 m`;
- opposite-direction mirror residual `5.230538224765269e-14`;
- ความต่าง half-step ของช่วงสั้น `8.335276595736185e-05`.

Exact replay ผ่าน Work 074 result SHA-256 คงที่ `a400e8a9c1c0768d11647aa6c2fde3855a5d12898b548edef0b2fd6911244374`; Work 075 application SHA-256 คงที่ `51b6255347e4a6a59428ee309f4f78c8e981baa437386bdcf3505df9d8403487`

Open-loop steering ออกจาก corridor หลัง `346` steps Narrow-corridor control ออกหลัง `23` steps Road-drop ทำให้ `contact_loss` หลัง attempted step `5` ก่อนจบรอบ Timeout control หยุดหลัง `20` steps ผลเหล่านี้ถูกเก็บเป็น causal DNF ไม่แปลงเป็น numerical failure หรือ clip ให้จบ

Reference result SHA-256 คือ `719b39293ecb818560acbd88cf1262da8b3407ffb3e5f150a0130860cf9e0dc3`; canonical evidence SHA-256 คือ `bdbdf31f63dc4da79c12e159d05e1a0e3c870a7994c846b53e73aba9ac2a9df2`; primary/replay file SHA-256 ที่เหมือนกันทุกไบต์คือ `F6E8C83A72510837C32B07F925132BAA594C531D1D9B4DBC4C5087C4AD6F80CB`

## การตีความและการหักล้างถัดไป

ผลสนับสนุน causal integration ระดับซอฟต์แวร์: steering เปลี่ยน physical contact force; linkage geometry เปลี่ยน vertical stiffness/travel; actual load จำกัด tyre force; spatial motion กำหนด progress และ failure ที่ประกาศห้าม finish Mirror, replay, failure injection และ refinement controls ลดคำอธิบายทางเลือกด้านเครื่องหมาย/บัญชีสถานะ

ผลไม่ยืนยัน predictive accuracy สนามเป็นวงกลม analytical ถนนสังเคราะห์ จุด geometry ไม่ได้ดึงจาก CAD joint และแบบจำลองไม่รวม speed/brake control, aerodynamics, tyre relaxation/nonlinear contact, thermal validation ระยะการแข่งขัน, chassis flex, structural load/failure coupling, barrier, weather, traffic และพารามิเตอร์จากการวัด Gate fidelity ถัดไปควรใช้ linkage topology จาก CAD และ sourced 3D corridor ก่อนอ้างรอบสนามจริง
