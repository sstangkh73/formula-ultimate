# Whole-Vehicle Load Cases และ Structural Coupling

ไฟล์ต้นฉบับภาษาอังกฤษ: `WHOLE_VEHICLE_LOAD_CASES.md`

## ขอบเขตหลักฐาน

Work 048 ยอมรับ deterministic quasi-static rigid-component cut-load adapter สำหรับ exact Work 047 primitive assembly เท่านั้น ไม่ได้ยอมรับ whole-vehicle stress FEA, arbitrary geometry, transient response, contact mechanics หรือ physical strength จุดประสงค์ที่แคบกว่าคือพิสูจน์ว่า frozen Level 0 state สร้าง interface wrench ที่ครบ trace ได้ และสมดุล พร้อม trigger failure-state policy แบบ bounded ของ Work 046 ได้

## Identity ที่ freeze

- assembly protocol: `topology_neutral_vehicle_v1`
- declaration SHA-256: `041057afd245bd4a10482837672d474b0e310ebbfc38fdca4c40408f1f441170`
- assembly STEP SHA-256: `f60bb686dfaca51c06bed8b1b086418c5f9ce2208d861b5b2ff18d8f845f18b9`
- structural failure contract: `structural_failure_coupling_v1`
- frame: right-handed SI, `x` เดินหน้า, `y` ซ้าย, `z` ขึ้น

Acceptance runner สร้าง STEP ใหม่และให้ FreeCAD วัด mass, centre of mass และ inertia หาก hash หรือ mass property ไม่ตรงจะ reject load-case protocol

## แบบจำลองสมดุล

สำหรับ component `i` แรง body ในกรอบรถที่เร่งคือ

```text
F_i = m_i (g - a)
```

และ moment รอบ assembly centre of mass คือ

```text
M_i = (r_i - r_COM) x F_i
```

Frozen aerodynamic/contact wrench ถูกเพิ่มโดยไม่แก้ค่า ผลรวม global ต้องปิดภายใน force/moment tolerance ที่ประกาศ Connection graph ของ assembly เป็น tree ซึ่ง root อยู่ที่ ground-contact component สำหรับทุก non-root subtree `S`, connection wrench ที่กระทำต่อ subtree คือ

```text
W_connection = -sum(W_external,i), i in S
```

ระบบ audit สมดุลซ้ำที่ทุก component วิธีนี้ไม่ประมาณ local stress แต่รักษาการส่ง force/moment ที่ common reference origin

## Case และ partition

Training partition ถูก freeze ก่อน search ด้วยห้ากรณี: straight acceleration, braking, steady cornering, combined manoeuvre และ bump extreme Holdout partition ถูก freeze ด้วย aero extreme และ combined manoeuvre ชุดที่สอง Deliberately overloaded control แยกต่างหากและไม่เป็น training/holdout evidence

- training partition SHA-256: `d19f8e33c1259e64632e6e89f9768fddeb8c6e54f4a204994e200037c6beba38`
- holdout partition SHA-256: `5045fd461c740e4edc461a702dc96bf3e93fba0b4dbb0bbeeca8adcaf4d5cf41`

ทุก snapshot ต้องประกาศ exact dynamics, contact, aerodynamics และ mass-state evidence class หาก evidence หายจะเกิด error; adapter ไม่แทนด้วยศูนย์

## ผลลัพธ์

Training/holdout nominal ทั้งเจ็ดกรณียัง `running` Maximum declared interface utilization อยู่ประมาณ `0.37` ถึง `0.72` Deliberate overload ถึงประมาณ `1.30`, ทำให้ critical `core_contact` path และอีก capacity หนึ่งจาก physical moment arm ล้มเหลว และ Work 046 contract คืน `DNF`

- maximum global residual: `1.5631940186722204e-13`
- maximum component residual: `2.2737367544323206e-13`
- maximum interface action/reaction residual: `0`
- maximum FreeCAD mass-property relative error: `1.7042240975184457e-15`
- exact replay result-set SHA-256: `da4848de71c19f9d76cad00cdf5013791e5b0d6f5b544293dcf9e094d782bb03`
- negative control ที่ reject: `7`

## บันทึก falsification

Implementation รอบแรก serialize typed connection load เร็วเกินไป Focused test ตรวจพบ type ที่หาย จึงแก้ boundary ระหว่าง result กับ JSON รอบถัดมาพบว่า overload ยังเกิน `energy_core` moment capacity ด้วย ผลนี้ถูกเก็บเป็น physical evidence แทนการเปลี่ยน capacity เพื่อซ่อน และแก้ test ให้ตรวจ expectation ที่ preregister จริงว่า `core_contact` ต้อง fail และรถเป็น `DNF`

Contradicting evidence ที่สำคัญที่สุดคือยังไม่มี whole-vehicle stress solver สมดุลทางพีชคณิตไม่สามารถตัด local stress concentration, joint flexibility, contact separation, vibration, buckling หรือ nonlinear material response ออกได้ Work 049 ใช้ adapter นี้เป็น bounded load-path stage ได้ แต่ห้ามเรียกว่า FEA หรือ physical validation

## การทำซ้ำ

```powershell
.\scripts\run_work048.ps1
py -3.14 -m unittest tests.test_vehicle_load_cases -v
```
