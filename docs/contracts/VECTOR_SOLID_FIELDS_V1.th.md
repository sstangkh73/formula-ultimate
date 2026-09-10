# สนามเวกเตอร์ของ Solid V1

ต้นฉบับภาษาอังกฤษ: `VECTOR_SOLID_FIELDS_V1.md`

Status: พัฒนาโดย Work 111 สำหรับหลักฐาน Level-0 แบบมีขอบเขต

## ขอบเขต หน่วย และ dependency

Contract นี้แก้สมการ small-strain, isotropic, linear elasticity บน mesh tetrahedral สี่ node ของ Work 110 พิกัดและ displacement ใช้ `m`, force ใช้ `N`, stress และ Young's modulus ใช้ `Pa`, density ใช้ `kg/m3`, acceleration ใช้ `m/s2` และ strain energy ใช้ `J` ตรึง Work 110 commit และ SHA-256 ของ `GEOMETRY_MESH_BRIDGE_V1.md` ที่ตรงกันก่อนเริ่ม run

ข้อมูล material เป็น synthetic fixture ไม่ใช่ข้อมูล production ที่ได้รับการรับรอง Output เป็นหลักฐาน numerical field ระดับ Level-0 เท่านั้น ไม่ยืนยัน nonlinear response, contact, plasticity, fatigue, strength, vehicle feasibility, manufacturing feasibility หรือ physical validation

## Formulation และข้อตกลง boundary

แต่ละ mesh node มี translational displacement DOFs สามแกน Constant-strain tetrahedron ใช้ symmetric engineering-strain vector `[exx, eyy, ezz, gxy, gyz, gxz]` และ three-dimensional isotropic elasticity matrix Element stiffness คือ `Ke = V B^T D B` Consistent body force คือ `density * V * acceleration / 4` ต่อ node

กระจาย resultant ที่ประกาศอย่างสม่ำเสมอตามพื้นที่สามเหลี่ยมบน `load_surface` ตรึง translation ทั้งสามแกนของทุก node บน `contact_surface` Reaction กู้คืนจาก `K u - f` ที่ constrained DOFs; ไม่ได้กำหนดค่าจาก input resultant ต้องมี graph path เชื่อม loaded node อย่างน้อยหนึ่ง node กับ supported node อย่างน้อยหนึ่ง node กรณี support หาย, solve singular/non-finite, path ขาด, Young's modulus ไม่เป็นบวก และ tetrahedron ไม่ถูกต้องล้มเหลวแบบปิด

## ปริมาณที่ลงทะเบียนและ gates

Output มี displacement vector field เต็ม, element stress field หกองค์ประกอบ, von Mises stress, loaded-face mean displacement, maximum displacement, compliance, strain energy, recovered resultant reaction และ deterministic SHA-256 identities ไม่ใช้ sharp-corner maxima ใน acceptance; ปริมาณ stress ที่ลงทะเบียนคือ element-volume-weighted p90 von Mises stress

ทุก admitted solve ต้องมี relative force และ moment residual ไม่เกิน `1e-8`, strain-energy/work residual ไม่เกิน `1e-10` และ stiffness diagonal proxy แบบค่าต่ำสุดต่อค่าสูงสุดของ free DOFs อย่างน้อย `1e-6` Proxy นี้เป็นหลักฐาน screening ที่สังเกตได้ ไม่ใช่ spectral condition number

Structured cuboid reference ใช้ `0.04`, `0.02` และ `0.01 m`; loaded-face axial displacement ของระดับละเอียดสุดต้องตรงกับ `F L / (E A)` ภายใน `8%` Affine patch, rigid translation และ rigid rotation strain errors ต้องไม่เกิน `1e-12` สนาม Work 109 ที่ไม่คุ้นเคยถูกส่งผ่าน Work 110 ที่ `0.02`, `0.01` และ `0.008 m`; last-two relative change ของ maximum displacement, compliance และ p90 von Mises stress ต้องไม่เกิน `0.8` แต่ bound นี้เป็น selection gate ไม่ใช่หลักฐาน asymptotic convergence

## การพยายามหักล้างและการส่งต่อ

Controls ต้องปฏิเสธ unsupported rigid modes, disconnected load path และ corrupt stiffness เมื่อเพิ่ม Young's modulus เป็นสองเท่า compliance ต้องลดครึ่งหนึ่ง ส่วน mutation ของ load direction และ geometry ที่ลงทะเบียนต้องเปลี่ยน displacement-field identity กำหนด hash ของ prohibited uniform reaction assignment แยกต่างหากและต้องไม่ตรงกับ recovered reaction field

Exact replay ต้องได้ result SHA-256 เดิม Work 113 และ Work 115 ใช้ fields เหล่านี้ต่อได้เฉพาะพร้อม metadata ของ mesh, material, load, support, resolution และ limitations ที่ประกาศไว้ การอ้าง higher-fidelity หรือ physical claim ต้องมี independent validation นอก contract นี้
