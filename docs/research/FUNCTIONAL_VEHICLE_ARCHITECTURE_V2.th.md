# Functional Vehicle Architecture v2

ไฟล์ต้นฉบับภาษาอังกฤษ: `FUNCTIONAL_VEHICLE_ARCHITECTURE_V2.md`

## ผลลัพธ์และขอบเขต

Work 066 แทน four-solid visual fixture ในฐานะ research input รุ่นถัดไปด้วย technology-neutral typed functional architecture Candidate อ้างอิงแบบคงที่ประกอบด้วย solid ที่ derive ได้อย่างอิสระ 10 ชิ้น, ports 48 จุด, connections 23 เส้น และ bounded ground contacts สองจุด จึงใช้ถามได้ว่า candidate ส่ง energy, torque, heat, commands และ structural load ได้หรือไม่ โดยไม่ยอมรับเพียงป้าย propulsion เป็นหลักฐานว่ามีแรง

ผลนี้เป็น architecture และ CAD evidence ไม่ใช่ complete vehicle simulation Reference ยังใช้ primitive boxes/cylinders และยังไม่มี detailed gears, shafts, bearings, windings, cells, fasteners, suspension links, tyre model, fluid passages, driver volume, crash structure หรือ manufacturing tolerances

## Technology-neutral contract

Candidate ที่ admit ต้องมี capabilities เทียบเท่า energy storage, energy conversion, power transmission, ground propulsion, direction control, braking, load structure, heat rejection และ control Grammar รู้จัก capability จาก function tags และ compatible connected ports ไม่ใช่จากชื่อหรือการบังคับ engine, motor, gearbox, wheel count, body shape หรือ layout แบบใดแบบหนึ่ง

Evidence graph ของ reference คือ:

```text
energy_store --electrical--> energy_converter --mechanical_rotary-->
torque_transmission --mechanical_rotary--> left_ground_unit/right_ground_unit

vehicle_controller --control--> converter/direction_actuator/brake_actuator
heat sources --thermal--> heat_rejector
all components --structural--> load_spine --> both ground units --> ground
```

Physical domains ได้แก่ `structural`, `electrical`, `mechanical_rotary`, `thermal`, `control` และ `ground` แต่ละ port มี domain, direction, local 3D position และ finite limits ในหน่วย SI Connections ต้องใช้ ports ที่มีอยู่และ compatible และยาวไม่เกินค่าที่ประกาศ Electrical/mechanical efficiency ต้องอยู่ใน `(0, 1]`; conversion และ transmission ห้ามสร้าง power หรือ torque ที่ไม่ได้ประกาศ ส่วน control connectivity ห้ามใช้แทน energy path

## Reference candidate

Candidate `fu-functional-reference-0001` ประกอบด้วย:

| Component | บทบาทที่ต้องมี | Geometry evidence |
| --- | --- | --- |
| `load_spine` | โครงสร้างรับแรง | box solid แยกชิ้น |
| `energy_store` | พลังงานสะสม | box solid แยกชิ้น |
| `energy_converter` | แปลงพลังงานเป็นการหมุนและเป็น heat source | box solid แยกชิ้น |
| `torque_transmission` | ส่ง torque แบบมีขอบเขตและเป็น heat source | box solid แยกชิ้น |
| `left_ground_unit` | ขับ/สัมผัสพื้นด้านซ้าย | transverse cylinder แยกชิ้น |
| `right_ground_unit` | ขับ/สัมผัสพื้นด้านขวา | transverse cylinder แยกชิ้น |
| `direction_actuator` | ควบคุมทิศทาง | box solid แยกชิ้น |
| `brake_actuator` | เบรกและเป็น heat source | box solid แยกชิ้น |
| `heat_rejector` | ระบายความร้อน | box solid แยกชิ้น |
| `vehicle_controller` | แหล่งคำสั่ง | box solid แยกชิ้น |

Declared architecture ผ่านด้วยมวล `272.55249331647553 kg`, centre of mass `(-0.024952088769517506, 0.0, 0.2793091493604943) m`, maximum connection length `0.842140130857092 m`, declaration SHA-256 `aab2aa83b794cbee8f1cdfa897c875bcf440394672e0013805d31f4bd20d9990` และ validation SHA-256 `d29f5d51a9b23db2dce9c33f93539cb71afaa020709fc5bcb69b2b6ebaa27677`

## CAD และการตรวจอย่างอิสระ

CadQuery 2.8.0 สร้าง STEP ต่อ component และ assembly สิบ solid โดยไม่มี geometry repair Assembly มี SHA-256 `983902b813ab6ee3fd69c703521ee32206e224b98013f430d1aeee7249ac75da` FreeCAD 1.1.3 เปิดทุก component และ assembly ใหม่อย่างอิสระ ยืนยัน valid solids 10 ชิ้น และคำนวณ mass properties ซ้ำ

การเปรียบเทียบจาก FreeCAD ให้ relative residuals:

- mass: `2.0855952616365914e-16`
- centre: `1.2421529906547113e-17`
- inertia: `7.979411838121619e-18`

ทุกค่าต่ำกว่า frozen limit `1e-6` การ generate รอบสองใน directory แยกให้ assembly hash และ component hashes ทั้ง 10 รายการตรงกันทั้งหมด

## Falsification evidence

Focused tests 7 รายการมี deliberate controls สำหรับ storage-to-converter path ที่หายไป, incompatible domain, invalid direction, unknown port, disconnected structure, heat path ที่หายไป, uncontrolled brake, efficiency มากกว่าหนึ่ง, การสร้าง power, การสร้าง torque, nonpositive limits, solids overlap, port อยู่นอก solid, ground contact ไม่อยู่ที่ `z = 0`, connection ยาวเกิน limit และ transverse-cylinder inertia ผิด ทุก invalid case fail closed โดยไม่มี silent repair

Repository regression ทั้งหมดผ่าน `388` tests หลักฐานนี้รองรับ deterministic schema, graph, primitive geometry และ STEP/FreeCAD evidence plumbing แต่ยังไม่ validate ว่าขนาดหรือ limits ของ components ที่เลือกเพียงพอทางกายภาพ

## งานถัดไปที่ต้องทำ

Research layer ถัดไปควรเพิ่ม transient component laws ก่อน optimize รถละเอียด: storage state และ power limits; converter torque-speed-efficiency และ heat loss; transmission ratio, inertia, compliance และ failure; ground-force/slip และ braking limits; steering kinematics; thermal capacity และ temperature state; และ bidirectional coupling กับ structural/failure system เมื่อกฎเหล่านี้ผ่าน analytical และ negative controls แล้วจึงนำ architecture เข้าสู่ whole-vehicle dynamics, higher-fidelity structural analysis หรือ race optimization
