# ความทนทานของผลเสาเชิงไม่เชิงเส้นต่อ Mesh และรูปความคด

ไฟล์ต้นฉบับภาษาอังกฤษ: `NONLINEAR_COLUMN_ROBUSTNESS.md`

## คำถามวิจัยและขอบเขตข้ออ้าง

Work 039 ตรวจจุดอ่อนที่เป็นไปได้สองข้อของผล precritical จาก Work 038 คือการขึ้นกับ mesh และการขึ้นกับรูป initial crookedness ที่สมมติไว้ หลักฐานทั้งหมดยังเป็น linear elastic และต่ำกว่า matching Work 037 eigenvalue load จึงใช้สนับสนุน post-buckling, collapse, yield, fracture, fatigue, safety factor หรือ vehicle capacity ไม่ได้

## วิธี

Fixed-free solid column คง `L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `nu=0.3`, C3D4 element และ tip imperfection `e0=0.1 mm` ใช้ Work 037 mesh สามระดับโดยไม่ renormalize applied load:

| Mesh | Size | Nodes | Tetrahedra | Work 037 `Pcr` |
|---|---:|---:|---:|---:|
| coarse | 1.50 mm | 7,052 | 29,098 | 3852.795 N |
| medium | 1.25 mm | 11,702 | 51,221 | 3776.375 N |
| fine | 1.00 mm | 20,514 | 95,711 | 3715.160 N |

Absolute load คือ `0.50`, `0.70` และ `0.85` เท่าของ fine-mesh `Pcr` รูป normalized สองแบบมี root offset, root slope และ tip amplitude เท่ากัน:

```text
cantilever_eigenmode:  phi(x) = 1 - cos(pi x/(2L))
smoothstep_cubic:      phi(x) = 3(x/L)^2 - 2(x/L)^3
```

Execution ผ่านเมื่อ 18 case converge พร้อม complete evidence, reaction closure `<=1e-5` และ response เพิ่มตาม load Numerical-convergence hypothesis กำหนด eigenmode secant error `<=15%` และ medium-to-fine amplification change `<=5%` Shape-robustness hypothesis กำหนด fine-mesh amplification difference `<=10%`

## ผล

ทั้ง 18 case converge, response ทุกชุด monotonic และ maximum reaction error เท่ากับ `1.749e-16` ดังนั้น execution ของการทดลองผ่าน

| Fine-load fraction | Medium-to-fine eigenmode change | Shape difference บน fine mesh |
|---:|---:|---:|
| 0.50 | 1.548% | 7.523% |
| 0.70 | 3.639% | 10.980% |
| 0.85 | 8.653% | 13.697% |

Eigenmode response ยังตรงกับ secant reference ของแต่ละ mesh อย่างใกล้เคียง โดย maximum error ทุก mesh เท่ากับ `0.912%` แต่ absolute-load medium-to-fine change เกิน gate `5%` ที่ `0.85` fine `Pcr` จึง **reject** numerical-convergence hypothesis สำหรับ load range ทั้งชุด

Fine-mesh amplification คือ:

| Fine-load fraction | Eigenmode amplification | Cubic amplification |
|---:|---:|---:|
| 0.50 | 1.9971 | 1.8523 |
| 0.70 | 3.3269 | 2.9806 |
| 0.85 | 6.6413 | 5.7900 |

Shape difference เกิน `10%` ที่ `0.70` และ `0.85` จึง **reject** shape-robustness hypothesis

## การตีความ

หลักฐานสนับสนุน: solver route เสถียร, force closure ดีมาก, monotonicity คงอยู่ และ eigenmode-shaped case เดินตาม matched secant reference หลักฐานแย้ง: response ที่ load สูงยังไม่ converge ระหว่าง mesh ละเอียดสุดสองระดับปัจจุบัน และ imperfection ที่มี tip amplitude เท่ากันไม่ได้สร้าง shape-independent amplification

คำอธิบายทางเลือก ได้แก่ C3D4 bending stiffness, condition sensitivity ที่สูงใกล้ `Pcr`, first-mode projection ที่ต่างกันของ imperfection shape และ mesh-asymmetry seed หลักฐานที่ยังขาด ได้แก่ mesh ละเอียดกว่า `1.0 mm`, quadratic element, measured/manufacturing imperfection distribution และ nonlinear continuation procedure ที่ validate แยก

ความเชื่อมั่นสูงว่า mesh และ imperfection-shape choice มีผลสาระสำคัญต่อ near-critical fixture นี้ ดังนั้น Work 039 block การเลื่อนไปอ้าง post-buckling capacity การทดลองถัดไปควรขยาย eigenmode study ให้ต่ำกว่า `1.0 mm` ที่ absolute load เดิม และเทียบ higher-order element route ก่อนเลือก continuation method
