# การไหลและแลกเปลี่ยนความร้อนจาก Geometry V1

แหล่งภาษาอังกฤษ: `GEOMETRY_FLOW_HEAT_EXCHANGE_V1.md`

Status: Work 121 นำไปใช้เป็น reference สอง scope แบบมีขอบเขตที่ Level-0

## Geometry และ scope ที่แยกกัน

Contract นี้ตรึง Gmsh artifact ของ hollow B-rep ระดับละเอียดสุดจาก Work 110, heat source `10 W` จาก Work 115 และข้อจำกัด material จาก Work 116 Node bounds ของ Gmsh กำหนด projected YZ area ภายนอก ส่วน circular adapter แบบมีขอบเขตที่ลงทะเบียนชัดกำหนดความยาว/เส้นผ่านศูนย์กลาง passage ภายใน Boundary inlet, outlet และ wall แยกจาก body-wall, far-field และ symmetry

Internal flow จำกัดที่ทางไหลวงกลม laminar แบบ synthetic และ property คงที่ ต่ำกว่า Reynolds `2300` ใช้ Hagen-Poiseuille pressure drop และ fully developed constant-wall-temperature Nusselt `3.66` เป็น analytic reference Segment `10`, `20`, `40` ต้องลู่เข้าหา analytic heat-transfer capacity แบบ monotonic; source heat, outlet enthalpy และ wall heat ต้องปิดภายใน `1e-10 W`

External flow เป็น adapter quadratic drag แบบ incompressible subsonic synthetic ที่แยกต่างหาก ส่วน pressure และ shear ต้องรวมเป็น drag ภายใน `1e-12 N` Far-field width `0.5`, `1.0`, `2.0 m` ใช้ blockage correction ที่เปิดเผย และ error ของ domain ละเอียดสุดต้องไม่เกิน `0.001`

## Control และขอบเขต claim

บังคับ control passage ถูกอุด, flow/source/speed ศูนย์, mutation ของ passage diameter/projected area และ domain sensitivity การเปลี่ยน geometry ต้องเปลี่ยน pressure หรือ drag เชิงเหตุ ส่ง load และ heat กลับ assembly แต่ความสำเร็จภายในใช้ยืนยัน external หรือ whole-car aerodynamics ไม่ได้

Fluid property, closure และ drag coefficient เป็น synthetic ส่วน turbulence, cavitation, compressibility, arbitrary passage, conforming fluid mesh, conjugate 3D CFD, validated cooling, whole-car aerodynamics และ physical validation ยัง unresolved
