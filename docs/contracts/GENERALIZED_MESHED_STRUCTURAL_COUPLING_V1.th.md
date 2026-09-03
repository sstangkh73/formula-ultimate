# สัญญา Generalized Meshed Structural Coupling V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `GENERALIZED_MESHED_STRUCTURAL_COUPLING_V1.md`

## วัตถุประสงค์และขอบเขต

สัญญานี้ขยายการตรวจ exact geometry ด้วย Gmsh/CalculiX จากรูแกน `z` และ support plane แกน `x` เพียงแบบเดียวของ Work 082 ให้รองรับ end plane ตามแกนหลักใด ๆ, cylindrical surface แกน `y`, โหลดแรง/คู่แรงร่วม และ support plane ตามแกนหลักใด ๆ หลักฐานนี้เป็น synthetic meshed software evidence ไม่ใช่ physical หรือ design validation

## ตัวตนและกรณีที่บังคับ

ทุกรันต้องตรวจตัวตน Work 084 result, geometry manifest, canonical FreeCAD report และ STEP แยกชิ้นที่ตรึงไว้ก่อน mesh กรณีบังคับคือ:

- `output_shaft_combined`: แรง radial `415.3846153846154 N` ร่วมกับแรงบิด `22.8 Nm`
- `support_block_bearing`: โหลดที่รู `384.6153846153847 N`
- `converter_housing_mount`: คู่แรงที่รู `8 Nm`

แต่ละกรณีใช้ characteristic length สามระดับที่ลดลงอย่างเคร่งครัดและประกาศก่อนรัน Node ที่รับโหลดและ support ต้องไม่ว่างและไม่ทับกัน

## กฎโหลดและหลักฐาน

พื้นที่สามเหลี่ยมให้น้ำหนักแรงหนึ่งในสามต่อ vertex แต่ละจุด แรงบิดรอบ `y` ใช้แรงสัมผัสที่ node ถ่วงด้วยพื้นที่ ลบ roundoff ของแรงลัพธ์ และ scale คู่แรงให้เท่ากับแรงบิดที่ประกาศ ค่าต่ำกว่า `1e-12 N` เป็น arithmetic zero แบบ canonical ค่าโหลด CalculiX ใช้ scientific notation ความยาวคงที่เพื่ออยู่ภายในขีดจำกัด token แบบ free-field

Solver รายงานจำนวน loaded/support node, loaded area, displacement, compliance, p90 von Mises stress, force residual, moment residual และ residual ระหว่าง external/internal energy Metadata เวลาใน FRD ถูก canonicalize เฉพาะเพื่อ hash; ไม่มีการแก้ physical output

## Gate และความหมายการล้มเหลว

- force residual `<=1e-5`
- moment residual `<=1e-5`
- energy residual `<=1e-4`
- การเปลี่ยนแปลงสัมพัทธ์ของสอง mesh สุดท้าย `<=12%` แยกอิสระสำหรับ maximum displacement, compliance และ p90 stress

ตัวตน/ผิว/support หาย, solver ล้มเหลว, metric ไม่ finite, residual เกิน หรือ convergence เกินแม้เพียง metric เดียวทำให้รันไม่ผ่าน ห้ามเฉลี่ย gate ข้าม metric หรือกรณี Support ที่ถูกตัดต้องทำให้แรงและแรงบิดส่งผ่านเป็นศูนย์และเกิด `dnf`

Verdict ที่ผ่านได้เพียงค่าเดียวคือ `synthetic_meshed_verification_only` พร้อม `design_use_allowed=false` ไม่มีคำอ้าง fatigue, fracture, contact, fastener, bearing life, manufacturing, safety หรือ physical ตามมา
