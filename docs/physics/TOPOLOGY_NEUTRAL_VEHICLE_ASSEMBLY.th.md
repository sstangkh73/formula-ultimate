# Topology-Neutral Whole-Vehicle Assembly Grammar

ไฟล์ต้นฉบับภาษาอังกฤษ: `TOPOLOGY_NEUTRAL_VEHICLE_ASSEMBLY.md`

## ขอบเขตการอ้างและผลลัพธ์

Work 047 validate complete multi-solid vehicle declaration หนึ่งตัวผ่าน topology-neutral assembly contract Contract ไม่กำหนด conventional body, จำนวนล้อ/contact, powertrain layout หรือ component count แต่บังคับ explicit geometry, material density, interface, connection, ground contact, energy path, external-load path, envelope, keep-out และ Work 046 failure-contract identity

Admitted fixture มีสี่ solid และหนึ่ง ground contact รูปแบบที่ไม่เหมือนรถทั่วไปนี้แสดงว่า schema ไม่บังคับรถสี่ล้อ นี่คือ geometric admission เท่านั้น ไม่ใช่หลักฐาน structural feasibility, aerodynamics, cooling, manufacturing, safety, race completion, novelty หรือ superiority

## Grammar v1

Initial library มี solid `box` และ `cylinder_z` ใน SI units พร้อม translation-only placement หน้าที่ component เป็น tag ไม่ได้ผูกกับชื่อรูปทรง Fixture ประกาศ:

- `source`: `energy_source`
- `core`: `external_load_receiver`
- `propulsor`: `propulsion`
- `contact_alpha`: explicit `ground_contact` หนึ่งจุด

Energy graph คือ `source -> core -> propulsor` External-load graph คือ `core -> contact_alpha` Coincident point interface เชื่อม solid ห้าม positive-volume overlap แต่อนุญาต face/point contact ทุก component ต้องอยู่ใน envelope และนอก protected keep-out

## หลักฐาน CAD แบบ deterministic

CadQuery `2.8.0` สร้าง STEP แยกแต่ละ component และ compound STEP ที่มีสี่ solid Canonicalize OCCT wall-clock field โดยไม่เปลี่ยน geometry การ export อิสระสองครั้งให้ component/assembly hash ตรงกัน

Canonical assembly STEP SHA-256 คือ:

```text
f60bb686dfaca51c06bed8b1b086418c5f9ce2208d861b5b2ff18d8f845f18b9
```

Canonical declaration SHA-256 คือ:

```text
041057afd245bd4a10482837672d474b0e310ebbfc38fdca4c40408f1f441170
```

ไม่ถือ STEP application label เป็น persistent identity Identity มาจาก immutable declaration, per-component file/hash, material ID และ measured geometric signature

## FreeCAD cross-check

FreeCAD `1.1.3` import component STEP ทุกไฟล์และ assembly STEP อย่างอิสระ พบ valid solid สี่ชิ้น Analytical component summation และ FreeCAD ให้:

```text
mass = 30.657168026350796 kg
centre of mass = (-0.01875580939197546,
                   0.002656151458968935,
                   0.14557308090171845) m
```

Analytical assembly inertia tensor components `(Ixx,Iyy,Izz,Ixy,Ixz,Iyz)` คือ:

```text
(0.12214756112199837,
 0.8039434564567454,
 0.8490539916188957,
-0.0015272870889071375,
 0.002545478481511896,
 0.00778252377477898) kg*m^2
```

Maximum relative difference ของ mass, centre และ inertia เท่ากับ `1.7042240975184457e-15` ต่ำกว่า preregistered limit `1e-6` Maximum connection-interface position residual เท่ากับ `1.3877787807814457e-17 m`

## Falsification และหลักฐาน defect

Control แปดกรณี reject floating component, protected-volume overlap, unmatched interface, disconnected energy path, zero-size solid, massless energy source, envelope violation และ undeclared ground position

Exploratory cylinder export ครั้งแรกใช้ CadQuery `both=True` ทำให้ความสูงเป็นสองเท่าของ declaration FreeCAD วัด mass `32.01433605270158 kg` แทน analytical `30.657168026350796 kg` ต่าง `4.43%` รอบนั้นไม่ถูก admit Generator ถูกแก้ให้สร้างความสูง `h` จาก `-h/2` ถึง `+h/2` แล้ว rerun frozen declaration เหตุการณ์นี้แสดงว่า independent mass evidence จับ CAD-generator defect ที่ดูสมเหตุสมผลได้

หลักฐานสนับสนุนคือ exact replay, valid-solid inspection, explicit graph reachability, mass-property agreement ที่เข้ม และ fail-closed control คำอธิบายทางเลือกคือ primitive มี analytical form ที่ง่าย หลักฐานที่ยังขาดคือ arbitrary rotation, free-form geometry, joint/contact physics, FEA load case, aerodynamics, thermal path, manufacturing และ physical measurement

ความมั่นใจสูงสำหรับ v1 primitive fixture นี้และต่ำเมื่ออยู่นอก declared grammar

## การทำซ้ำ

```powershell
.\scripts\run_work047.ps1
py -3.14 -m unittest tests.test_vehicle_assembly tests.test_repository_contract -q
py -3.14 -m unittest discover -s tests -q
```

Machine-readable evidence และ STEP อยู่ใต้ `artifacts/work047/` และ Git จงใจ ignore ต้องทำ clean-tree replay หลัง commit
