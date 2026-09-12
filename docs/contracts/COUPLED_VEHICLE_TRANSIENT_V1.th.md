# Coupled Vehicle Transient V1

แหล่งภาษาอังกฤษ: `COUPLED_VEHICLE_TRANSIENT_V1.md`

Status: Work 123 นำไปใช้สำหรับ integration แบบ exploratory ที่มีขอบเขตใน Level-0

## Identity, state และ exchange boundary

Contract นี้ตรึง contract/result ของ Work 117–122 ที่ระบุแน่นอน State position/velocity, stored energy, temperature และ controller delay มีเจ้าของที่ประกาศเพียงรายเดียว Frame route-X และเครื่องหมายของ traction work, drag work, storage draw, generated heat และ removed cooling แก้ไม่ได้; ถ้าไม่ตรงให้ fail closed

Trial แบบลดรูปเชื่อม controller force demand, ground capacity จาก Work 118, output-power ceiling จาก Work 119, initial energy จาก Work 120, drag/cooling จาก Work 121 และ controller load จาก Work 122 ภายในแต่ละ step ใช้ fixed-point iteration แก้ speed-dependent power cap Traction work แบ่งเป็น kinetic-energy change กับ drag work; storage decrease แบ่งเป็น traction work, actuation loss และ controller energy Residual ยังคงสังเกตได้

Time step คือ `0.02`, `0.01` และ `0.005 s` Maximum step residual `1e-8 J`, global residual `1e-7 J` และการเปลี่ยน state สองระดับสุดท้าย `0.005` แบบสัมพัทธ์ Target event เกิดที่ `2 s`; history เก็บหลักฐาน event และ coupling iteration

## Control และขอบเขต promotion

บังคับ control signs ไม่ตรง, power นับซ้ำ, event หน่วง, พลังงานหมด, reduced flow state นอกช่วง และ decoupled run Integration ที่สำเร็จยังเป็น `passed_exploratory_only` พร้อม `promotion_allowed: false`

Complete candidate geometry, measured material, validated ground device, full aerodynamics, structural failure และ physical validation ยัง unresolved Harness นี้ไม่ยืนยันรถที่สมบูรณ์ race completion, readiness หรือสมรรถนะจริง
