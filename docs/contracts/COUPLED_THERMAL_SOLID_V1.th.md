# Coupled Thermal-Solid V1

ต้นฉบับภาษาอังกฤษ: `COUPLED_THERMAL_SOLID_V1.md`

Status: พัฒนาโดย Work 115 สำหรับหลักฐาน coupling ระดับ Level-0 แบบมีขอบเขต

## ขอบเขตและหลักฐาน geometry

Contract นี้ตรึง commits/contracts ของ Work 111 และ Work 113 รวมถึง Work 113 threaded-reference result และ male/female STEP hashes ที่ตรงกัน Male/female region volumes คือ `9.803770506463375e-7` และ `2.6351823298910333e-6 m3` Contact area `1.2073261309882398e-4 m2` ถูก derive ใหม่จาก geometry helix แปดรอบที่ลงทะเบียน ไม่ใช่ free fit parameter

Lumped thermal regions สองส่วนใช้ synthetic density, heat capacity, expansion และ temperature-dependent modulus records ที่เปิดเผยและ valid เฉพาะ `250-400 K` Source `10 W` ให้ความร้อน male นาน `5 s`; female มี prescribed ambient-boundary conductance `0.5 W/K` Contact conductance เริ่มจากกฎ synthetic ที่ยังไม่วัด `20000 W/m2/K` และเปลี่ยนตาม interface area กับรากที่สองของ preload ratio Boundary นี้ไม่ใช่ validated convection, radiation หรือ fluid cooling

## Bidirectional coupling และ gates

ในแต่ละ explicit step contact heat transfer เปลี่ยนอุณหภูมิทั้งสองฝั่ง Temperature เปลี่ยน free expansion และ Young's modulus; differential expansion เปลี่ยน preload ผ่าน clamp sensitivity ที่ลงทะเบียน; preload ส่ง contact conductance ที่เปลี่ยนกลับไปยัง heat balance ถัดไป Decoupled control ทำให้ conductance ไม่ขึ้นกับ mechanical state ที่ส่งกลับ

Time steps คือ `0.02`, `0.01` และ `0.005 s` Energy residual ต้องไม่เกิน `1e-10`; last-two relative changes ของอุณหภูมิทั้งสอง, preload และ contact conductance ต้องไม่เกิน `0.01` Single-temperature reduced model รับได้เฉพาะเมื่อ temperature-rise error ไม่เกิน `0.2` การออกนอก property range, modulus/preload ไม่เป็นบวก, geometry เก่า หรือ contact area หายล้มเหลวแบบปิด

Insulated energy rise, zero-source equilibrium, free/constrained expansion, removed heat path และ doubled interface area เป็น causal controls บังคับ Exact replay ต้องได้ result SHA-256 เดิม Lumped regions ไม่ resolve spatial gradients หรือ thermal stress fields; contract นี้ไม่ยืนยัน certified properties, validated cooling, fatigue/loosening, vehicle cooling adequacy หรือ physical validation
