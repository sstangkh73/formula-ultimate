# Constrained Component Grammar รุ่น 1

ไฟล์ต้นฉบับภาษาอังกฤษ: `CONSTRAINED_COMPONENT_GRAMMAR.md`

## ขอบเขตข้ออ้าง

`mounting_plate_v1` คือภาษา geometry และ interface แบบแคบรุ่นแรกที่ใช้ทดลอง
เส้นทางหลักฐาน CAD ของโปรเจกต์ การผ่าน grammar หมายถึงเพียง candidate
เขียนแทนได้ภายในข้อจำกัด dimension และ topology ที่ประกาศไว้ ไม่ได้พิสูจน์
strength, stiffness, fatigue life, manufacturability, safety, usefulness หรือ
optimality

## Production

```text
mounting_plate_v1
  := rounded_prismatic_plate
   + symmetric_four_hole_mounting_interface
   + optional_central_circular_lightening_cut
   + constant_density_material_assumption
```

Production ตั้งใจให้ได้ prismatic solid หนึ่งชิ้นเสมอ รูยึดสี่รูเป็น interface
port ไม่ใช่ free topology รุ่น 1 ไม่มี stochastic production แต่ทุกการทดลองยัง
บันทึก seed เพื่อไม่ให้ replay metadata ต้องเปลี่ยน schema ภายหลัง

## หน่วยและระบบพิกัด

ค่า grammar ทั้งหมดใช้ SI:

- length, width, thickness, radius, spacing, bound และ centre of mass: metre;
- volume: cubic metre;
- density: kilogram per cubic metre;
- mass: kilogram

แผ่นมีศูนย์กลางที่ `X=0, Y=0` เริ่มที่ `Z=0` และยื่นไปทาง `Z` บวก CadQuery รับ
millimetre ดังนั้น generator คูณ metre ด้วย `1000` เฉพาะภายใน CAD adapter
ส่วน measurement จาก CadQuery และ FreeCAD ถูกหารด้วย conversion metric ที่ตรงกัน
ก่อนเข้าสัญญาหลักฐาน

## Parameter และข้อจำกัดที่ประกาศ

| Parameter | ช่วงรุ่น 1 | กฎเพิ่มเติม |
|---|---:|---|
| `length_m` | `[0.12, 0.30]` | finite |
| `width_m` | `[0.08, 0.20]` | finite |
| `thickness_m` | `[0.004, 0.015]` | finite |
| `corner_radius_m` | `[0.002, 0.030]` | ไม่เกินหนึ่งในสี่ของมิติภายนอกด้านที่เล็กกว่า |
| `mounting_hole_diameter_m` | `[0.005, 0.012]` | รูเท่ากันสี่รู |
| `mounting_spacing_x_m` | `[0.012, 0.260]` | สมมาตรรอบจุดกำเนิด |
| `mounting_spacing_y_m` | `[0.012, 0.160]` | สมมาตรรอบจุดกำเนิด |
| `lightening_radius_m` | `[0.0, 0.080]` | `0` หมายถึงไม่มี central cut |
| `density_kg_per_m3` | มากกว่า `0` | finite และสมมติเป็น constant density |

ตรวจ interface และ web constraint ก่อน CadQuery execute:

- edge ligament ของ mounting hole อย่างน้อย `0.006 m` ในทั้งสองแกน;
- mounting hole ต้องรักษา ligament ดังกล่าวถึงส่วนโค้งมุมด้วย ไม่ใช่เพียงถึง
  axis-aligned outer bound;
- pitch ระหว่างศูนย์ mounting hole ต้องเหลือเนื้อระหว่างขอบรูอย่างน้อย `0.006 m`;
- central cut ต้องห่างขอบนอกที่ใกล้ที่สุดอย่างน้อย `0.006 m`;
- central cut ต้องห่างขอบ mounting hole ทุกจุดอย่างน้อย `0.006 m`;
- unknown schema key, missing key, grammar version ผิด และค่าที่ไม่ finite
  ถูกปฏิเสธแทนการ clip

สำหรับ family แบบ prismatic นี้ สูตร volume อ้างอิงคือ:

```text
A_outer = length*width - (4 - pi)*corner_radius^2
A_cut = 4*pi*(mounting_hole_diameter/2)^2 + pi*lightening_radius^2
volume = (A_outer - A_cut)*thickness
mass = FreeCAD_STEP_volume*density
```

บันทึก analytical mass เพื่อเปรียบเทียบ แต่ input ระดับ Level 0 ใช้ volume จาก
การ import STEP ด้วย FreeCAD ไม่ใช่ค่าที่ generator รายงานเอง

## วงจรหลักฐาน

```text
versioned JSON candidate
  -> pure-Python grammar validation
  -> CadQuery B-rep generation และ single-solid gate
  -> ไฟล์ STEP พร้อม manifest SHA-256
  -> FreeCAD headless import hash เดียวกัน
  -> วัด validity, solid count, volume, bound และ centre อย่างอิสระ
  -> analytical/CadQuery/FreeCAD residual gate
  -> FreeCAD volume * density ที่ประกาศ
  -> point mass รวมระดับ Level 0
  -> final speed และ distance จากแรงขับคงที่
```

ไม่มีการแทนค่า CAD ที่ล้มเหลวด้วยค่า analytical tolerance ของ volume ปัจจุบันคือ
absolute `1e-10 m^3` และ relative `1e-6` ส่วน bounding-box tolerance คือ
`1e-7 m` configuration ของการทดลองอยู่ที่
`config/work006_mounting_plate.json`

## การทดลองควบคุม Work 006

ตัวแปรอิสระที่ประกาศล่วงหน้าคือรัศมี central cut: `0`, `0.025` และ `0.040 m`
ส่วน outer dimension, mounting interface, density, seed, base vehicle mass,
force, duration, timestep และเส้นทาง software ถูกควบคุมให้คงที่ สมมติฐานที่
ต้องการทดสอบคือ volume/mass ลดลง และ final speed/distance ระดับ Level 0 เพิ่มขึ้น
เมื่อรัศมี cut เพิ่มขึ้น

รัศมี invalid `0.055 m` ที่ใส่โดยเจตนาต้องไม่ผ่านกฎ outer ligament ก่อนรัน
CadQuery negative case นี้เป็นส่วนหนึ่งของการทดลอง ไม่ใช่ generation failure
ที่ถูกทิ้ง

รันวงจร local ทั้งหมดด้วย:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work006.ps1
```

STEP, manifest, measurement อิสระ และ summary รวมที่สร้างขึ้นจะเก็บใต้ directory
`artifacts/work006/` ซึ่ง Git ignore

## ข้อจำกัดการตีความ

CadQuery และ FreeCAD เป็นคนละ application ในวงจรนี้ แต่ทั้งคู่พึ่งพา solid
geometry ตระกูล OCCT ดังนั้นการตรงกันไม่ใช่ทฤษฎี geometry ที่อิสระเต็มที่ จากนั้น
Level 0 ถือ imported volume เป็นเพียง point mass ที่มี constant density Work 006
ไม่มี load, boundary condition, material allowable, mesh, FEA, fatigue, joint,
tolerance, manufacturing process, collision model หรือ empirical calibration
สิ่งที่ขาดเหล่านี้ห้ามอ้าง physical validation
