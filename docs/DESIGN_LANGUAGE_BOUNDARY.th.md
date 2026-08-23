# ขอบเขตของ Design Language

> ฉบับภาษาไทยของ `DESIGN_LANGUAGE_BOUNDARY.md`

## เหตุผลที่ต้องมีเอกสารนี้

คำว่า “ไม่กำหนดสถาปัตยกรรมล่วงหน้า” ไม่สามารถแปลว่า “ไม่มีสมมติฐาน” ได้
ระบบค้นหาค้นพบได้เฉพาะ design ที่ representation และ component library ของมัน
สามารถแสดงออก เอกสารนี้ทำให้ inductive bias ดังกล่าวมองเห็นและมี version

## ขอบเขตการทดลองที่คงที่ในระยะที่ 1

เพื่อแยก powertrain topology ให้เป็น independent variable ระยะที่ 1 กำหนด
สิ่งต่อไปนี้คงที่:

- ตัวถังรถหนึ่งแบบ แทนด้วย mass และ longitudinal coefficient
- จุดสัมผัสยางเชิงนามธรรมสี่จุดในตำแหน่งคงที่
- พิกัด track หนึ่งมิติและ track profile ที่กำหนดไว้
- สภาพแวดล้อมต่อหนึ่ง experiment
- version ของ component catalog
- budget, พลังงานเริ่มต้น และกฎการวิ่งจบการแข่งขัน
- search/evaluation budget และชุด random seed

ข้อจำกัดเหล่านี้ไม่ได้กำหนดรถ Formula Ultimate ฉบับสุดท้าย แต่เป็น control
ของ causal experiment แรก

## อิสระของ Topology ในระยะที่ 1

Candidate สามารถเปลี่ยนสิ่งต่อไปนี้:

- จำนวนและชนิดของ energy source
- จำนวน ชนิด และการเชื่อมต่อ converter
- การมีหรือไม่มี gearing และ mechanical differential
- จำนวน actuator และการผูกกับ tyre endpoint ที่อนุญาต
- เส้นทางพลังงานแบบ series, parallel และผสม
- component parameter ภายใน envelope ที่ประกาศ
- regenerative path เมื่อ component ที่เลือกสนับสนุน

ไม่มี component ใดเป็นสิ่งบังคับ นอกจากสิ่งที่จำเป็นตามตรรกะเพื่อให้รถเคลื่อนที่
อยู่ภายในข้อจำกัด และวิ่งจบการแข่งขัน

## Physical Domain ที่มี Type

ทุก connection ใช้ domain ที่ชัดเจนพร้อม conjugate effort/flow variable:

| Domain | Effort | Flow | ข้อตกลงกำลัง |
|---|---|---|---|
| Electrical DC | voltage (V) | current (A) | `V * A` |
| Mechanical rotational | torque (N m) | angular speed (rad/s) | `tau * omega` |
| Mechanical translational | force (N) | velocity (m/s) | `F * v` |
| Chemical fuel | specific energy (J/kg) | mass flow (kg/s) | model-defined |
| Thermal | temperature (K) | heat flow (W) | signed heat transfer |
| Control | command/state | signal rate | ไม่มี physical power |

Control edge สร้างพลังงานไม่ได้ Component ต้องเปิดเผย loss และ rejected heat
แทนการซ่อนประสิทธิภาพที่สูญเสียไป

## Gate ตรวจความถูกต้องของ Graph

Candidate graph จะถูก reject ก่อน race simulation หากมี:

- port domain หรือ direction ที่ไม่เข้ากัน
- required port ที่ไม่ได้เชื่อมต่อ
- energy-consuming path ที่ไม่มี source ซึ่งเดินทางถึงได้
- source, sink หรือ state value ที่ไม่มีขอบเขต
- connection ซ้ำใน port ที่ exclusive
- algebraic loop ที่ห้ามใช้และไม่มี solver strategy ประกาศไว้
- parameter นอก component envelope
- static mass, cost หรือ volume เกิน experimental budget
- ไม่มี path ที่สามารถส่ง longitudinal force ไปยัง tyre endpoint

การผ่าน graph validation หมายถึงถูกต้องในระดับ representation ไม่ได้หมายความว่า
มี performance เสถียร ปลอดภัย หรือผ่านการรับรองทางฟิสิกส์

## ข้อกำหนดด้าน Version

ทุก experiment record ต้องมี:

- design-language version
- component-catalog version และ hash
- simulator version และ Git commit
- configuration hash
- random seed
- search algorithm และ evaluation budget

การเปรียบเทียบข้าม design-language version ถือเป็นคนละ experiment เว้นแต่มี
compatibility analysis ที่จัดทำเป็นเอกสารและแสดงว่าเทียบกันได้
