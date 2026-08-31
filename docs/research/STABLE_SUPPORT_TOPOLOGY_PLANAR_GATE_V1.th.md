# โทโพโลยีฐานรองรับที่เสถียรและด่านพลวัตระนาบ v1

เอกสารต้นฉบับภาษาอังกฤษ: `STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.md`

## ผลลัพธ์และขอบเขตคำกล่าวอ้าง

Work 069 หักล้าง fixture สองจุดสัมผัสที่ตรึงจาก Work 066/068 ก่อนขยายพลวัต จุดสัมผัส v2 ทั้งสองอยู่บนเส้น `x = 0.45 m` แต่ภาพฉายจุดศูนย์กลางมวลจาก geometry อยู่ที่ `x = -0.0249520887695175 m` ขอบเขตฐานรองรับจึงเสื่อมมิติ มีพื้นที่ `0 m^2` และ signed margin `-0.4749520887695175 m` ทำให้ปิดสมดุลโมเมนต์ pitch สถิตไม่ได้

แบบอ้างอิง v3 แยกต่างหากเพิ่มฐานรองรับหลังแบบ passive ที่มีขีดจำกัด ณ `(-0.55, 0, 0) m` โดยคงจุดขับเคลื่อนสองจุดและเส้นทางพลังงาน การควบคุม ความร้อน เบรก และโครงสร้างทั้งหมดไว้ พร้อมสร้างรูปหลายเหลี่ยมสามจุดสัมผัสที่ไม่บังคับเทคโนโลยี แบบนี้ไม่ได้บังคับว่าต้องเป็นรถสี่ล้อและไม่ใช่รถที่ optimize แล้ว

ผลลัพธ์นี้อนุมัติเฉพาะฐานรองรับสถิต/กึ่งสถิตที่ derive จาก geometry และการเลี้ยวระนาบ Level 0 ไม่ใช่การยืนยันทางกายภาพ แบบจำลองช่วงล่าง แบบจำลองยางจากการวัด หรือหลักฐานว่ารถทั้งคันจบการแข่งขันได้

## ฐานรองรับที่ derive จาก geometry

สถาปัตยกรรม v3 ที่ materialize แล้วมี `11` components, `24` connections และ `3` ground contacts โดยมีสมบัติรวม:

```text
mass = 276.89543100079806 kg
centre of mass = (-0.0331871483063111, 9.21878252910516e-19, 0.276183105667901) m
support polygon area = 0.32000000000000006 m^2
signed centre-of-mass margin = 0.15751201265152398 m
```

แรงปกติสามค่าถูกแก้โดยตรงจากตำแหน่งโลกของ component และ port:

```text
sum(N_i) = m g
sum((x_i - x_COM) N_i) = -m a_x h
sum((y_i - y_COM) N_i) = -m a_y h.
```

ระบบไม่ clip แรงติดลบ ดังนั้นคำตอบติดลบจะคงเป็นหลักฐาน contact lift ที่สังเกตได้

## กรณีโหลดกึ่งสถิตที่ตรึงไว้

| กรณี | ความเร่ง `(a_x, a_y)` | แรง `(left, right, rear)` N | ค่าต่ำสุด N | ผล |
| --- | ---: | ---: | ---: | --- |
| static | `(0, 0) m/s^2` | `(701.681093, 701.681093, 1312.054393)` | `701.681093` | passed |
| acceleration | `(6, 0) m/s^2` | `(472.259572, 472.259572, 1770.897433)` | `472.259572` | passed |
| braking | `(-6, 0) m/s^2` | `(931.102613, 931.102613, 853.211353)` | `853.211353` | passed |
| lateral left | `(0, 3) m/s^2` | `(343.209967, 1060.152218, 1312.054393)` | `343.209967` | passed |
| lateral right | `(0, -3) m/s^2` | `(1060.152218, 343.209967, 1312.054393)` | `343.209967` | passed |
| contact-lift control | `(0, 8) m/s^2` | `(-254.241908, 1657.604094, 1312.054393)` | `-254.241908` | contact_lift |

residual สมดุลกึ่งสถิตสัมบูรณ์สูงสุดคือ `2.2737367544323206e-13 N m` ต่ำกว่า tolerance สัมพัทธ์ `1e-9` ทุกกรณีที่อนุมัติมีแรงเป็นบวกและไม่เกินขีดจำกัดแรงปกติ ส่วนกรณีหักล้าง `8 m/s^2` สูญเสียจุดสัมผัสตามที่กำหนด

## การตอบสนองการเลี้ยวระนาบ

specimen ระนาบเริ่มที่ `10 m/s` ขอแรงตามยาว `300 N` ที่จุดขับเคลื่อนแต่ละจุด ใช้มุมเลี้ยวขนาด `0.02 rad` ทำงาน `0.5 s` และ step `0.002 s` ขีดจำกัดการเลี้ยวของ protocol ถูกตรวจให้สอดคล้องกับขีดจำกัด direction actuator `0.6 rad`

| control | `y` สุดท้าย m | heading rad | yaw rate rad/s | ผล |
| --- | ---: | ---: | ---: | --- |
| zero steer | `0` | `0` | `0` | passed |
| `+0.02 rad` | `0.239430705274132` | `0.173102791267070` | `0.573668613831193` | passed |
| `-0.02 rad` | `-0.239430705274132` | `-0.173102791267070` | `-0.573668613831193` | passed |

ผลบวกและลบ anti-symmetric ตรงกันพอดีสำหรับสถานะแนวข้างที่เลือก การรันด้านบวกครบ `250` steps มีแรงปกติ dynamic ต่ำสุด `116.77062376095432 N` และ combined tyre utilization สูงสุด `1.0000000000000002` ส่วนที่เกินหนึ่งเป็น floating-point roundoff ภายใน `1e-12` ไม่ใช่แรงที่ทะลุขอบเขต residual สมดุลแรง/โมเมนต์สูงสุดที่ solver รายงานคือ `2.277775479342381e-8`

เมื่อลด step ครึ่งหนึ่งเป็น `0.001 s` metric ปลายทางที่เลือกเปลี่ยนสูงสุด `0.001216322032258299` ต่ำกว่าเพดานสัมพัทธ์ `0.02` การ replay แบบ exact ให้ result hash เดิม `8bfd4a8ea64cac71821930ea7e4769eeb0c7094639d16fc6edde4de6e5974936`

## หลักฐาน STEP และ FreeCAD อิสระ

hash ของสถาปัตยกรรมที่ materialize แล้วคือ `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418` CadQuery สร้าง STEP solid ที่ valid หนึ่งชิ้นต่อ component รวม `11` ชิ้น และ assembly `11` solids ที่มี SHA-256 `a260b74185fbd473ef33fb0e71387121af25c045609a4007347e3256b3affaf4`

FreeCAD `1.1.0` import ทุก component และ assembly แยกอิสระ residual สัมพัทธ์สูงสุดของ mass/centre/inertia คือ `5.000115436834047e-16` ต่ำกว่าเกณฑ์ `1e-6` และไม่มี hidden geometry repair การ replay แบบ clean ให้ materialized JSON bytes, experiment evidence hash, assembly hash, STEP hash ของทุก component และมวลจาก FreeCAD ตรงกันทั้งหมด

SHA-256 ของหลักฐานการทดลอง canonical คือ `d3a480c4637f5955668259d7e3b52b8bc474ce084a32359964558d4c624a81b5`

## การหักล้าง หลักฐานที่ขัดแย้ง และความมั่นใจ

- สมมติฐานที่ต้องการถูกหักล้างสำหรับ v2: แบบนี้ไม่ผ่านสถิต แม้ solid และ functional connection แต่ละส่วนจะ valid
- กรณี lateral สูงเกินพิสูจน์ว่า fixture v3 ไม่สามารถคงฐานรองรับภายใต้ความเร่งทุกขนาด
- การสำรวจเดิมที่มุม `0.04 rad` ทำให้ contact lift ที่ `0.368 s`; specimen ที่อนุมัติและตรึงไว้ใช้ `0.02 rad` นี่คือขอบเขตทางกายภาพ/ตัวเลข ไม่ใช่ output ที่ถูกซ่อมเงียบ ๆ
- base identity ที่แก้ไข, numerical tolerance ที่มากเกิน และขีดจำกัดการเลี้ยวที่ไม่ตรงกับ direction actuator ถูกปฏิเสธแบบ fail closed
- focused tests `8` รายการและ repository tests ทั้งหมด `412` รายการผ่าน

ความมั่นใจสูงสำหรับการบังคับ contract แบบ deterministic, geometry identity, สมดุลสถิต, กรณีโหลดที่ประกาศ, เครื่องหมายการเลี้ยว Level 0, STEP import และ replay แต่ความมั่นใจต่อ handling transient จริงยังต่ำ เพราะยังไม่มี compliance, damping, การวัดยาง, road input, aerodynamic transient load และการทดสอบจริง

## หลักฐานที่ยังขาดและงานถัดไป

แบบอ้างอิงสามจุดสัมผัสใช้คำตอบ rigid quasi-static จึงยังไม่มี suspension travel, pitch/roll/heave inertia, wheel-hop, road roughness, tyre relaxation length, camber, thermal/wear evolution, contact patch pressure, actuator dynamics และ coefficient ที่ validate แล้ว จุดสัมผัสหน้าทั้งสองยังใช้ความเร็วเพลา output ร่วมกันจาก Work 067

Work 070 ควรเพิ่ม differential/carrier energy contract อย่างชัดเจนก่อนเพิ่มความเร็วเชิงมุมอิสระของจุดขับเคลื่อน แต่ละ branch ต้องมี inertia, torque, speed, slip power, heat, limits และ failure state ที่ประกาศ เพื่อให้การแยกเพลาไม่ทำให้ inertia ซ้ำหรือสร้างพลังงาน จากนั้นจึงค่อยเชื่อมแบบอ้างอิงกับ circuit trajectory และ whole-race gate
