# แผนงาน 069: Stable Support Topology and Planar Gate

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_069_stable-support-topology-planar-gate-plan.md`

## วัตถุประสงค์และ prerequisite ที่ค้นพบ

Falsify ground-support topology ของ Work 066/068 ก่อนเพิ่ม independent wheel speeds และ steering dynamics ปัจจุบัน contacts สองจุดอยู่ที่ `x = 0.45 m` ทั้งคู่ แต่ geometry-derived centre of mass อยู่ที่ `x = -0.024952088769517506 m` ดังนั้น line segment ของ contacts ไม่ครอบ centre-of-mass projection และปิด static pitch moment ไม่ได้ การทำ dynamic load transfer ต่อบน topology นี้จะเป็นการจำลองรถที่ไม่ stable ตั้งแต่หยุดนิ่ง

Work 069 จะรักษา frozen v2 fixture เป็น evidence, สร้าง technology-neutral v3 reference แยกต่างหากโดยเพิ่ม passive rear support contact, regenerate STEP/FreeCAD evidence และสร้าง support/load-transfer/planar steering admission gate Reference สาม contact หลีกเลี่ยงการบังคับ conventional four-wheel layout พร้อมสร้าง support polygon ที่ครอบ centre of mass ได้

Independent left/right wheel-speed และ differential dynamics ย้ายไป Work 070 เพราะ Work 067 ยังมี common output speed หนึ่งค่า การแยกโดยไม่มี explicit differential/carrier energy contract จะ duplicate inertia หรือสร้างพลังงาน

## คำถามวิจัยและสมมติฐาน

คำถาม: minimally remediated free-topology architecture สามารถสร้าง geometry-derived support polygon ที่ครอบ centre of mass, ปิด vertical/pitch/roll equilibrium ภายใต้ declared acceleration cases, รักษา Work 066 functional paths และให้ bounded nonzero steering/yaw response ได้หรือไม่

Preferred hypothesis: v3 three-contact reference ผ่าน architecture, overlap, STEP, FreeCAD, support-polygon, static load, bounded longitudinal/lateral transfer, combined-force, steering-sign, exact-replay และ refinement checks ส่วน frozen v2 topology ต้อง fail support-polygon gate

Falsification รวม v2 ผ่านผิดพลาด, v3 contact อยู่นอก solid หรือไม่มี support connection, centre of mass อยู่นอก/บน support boundary, negative normal load ใน admitted case, force/moment residual เกิน tolerance, contact capacity เกิน, steering/yaw sign ผิด, mass/inertia mismatch หลัง CAD import, nondeterministic evidence หรือ stable result ที่พึ่ง silent contact-force clipping

## Architecture remediation

v3 fixture จะ copy v2 และเพิ่ม passive ground-support component หนึ่งชิ้นด้านหลัง centre of mass โดยมี geometry, material, structural mount, ground port, bounded normal/longitudinal/lateral limits และ declared contact ของตนเอง Powered/direction-controlled ground units สองชิ้นเดิมไม่เปลี่ยน Component ใหม่เป็น support capability ไม่ใช่ undeclared propulsion source

Support polygon และ contact lever arms ทั้งหมด derive จาก component/port world positions Static normal forcesต้อง satisfy

```text
sum(N_i) = m g
sum(x_i N_i) = 0
sum(y_i N_i) = 0.
```

สำหรับ quasi-static planar accelerations ที่ centre-of-mass height `h`, v1 ใช้

```text
sum(x_i N_i) = -m a_x h
sum(y_i N_i) = -m a_y h.
```

Normal forces สามค่าถูก solve โดยตรง; negative force เป็น observable contact-lift failure ไม่ถูก clip เป็นศูนย์

## การออกแบบการทดลอง

- Independent variables: support component geometry/pose, contact positions/limits, material density, centre of mass, centre-of-mass height, longitudinal/lateral accelerations, steering command, cornering stiffness, friction coefficients, initial planar speed และ time step
- Dependent variables: polygon containment/margin, barycentric/static load fractions, per-contact normal loads, vertical/pitch/roll residuals, contact lift, combined tyre utilization, body forces, yaw moment/rate/heading, STEP solid count, mass/centre/inertia residuals และ replay hashes
- Controls: immutable v2 negative control, SI right-handed frame, unchanged powered paths, exact architecture identities, geometry-derived locations/mass/inertia, no hidden CAD repair, deterministic ordering และ frozen tolerances
- Metrics: signed support margin, minimum normal load, maximum contact utilization, equilibrium residuals, yaw-response sign/magnitude, CAD residuals, exact replay และ half-step refinement

Load cases จะมี static, bounded acceleration, bounded braking, bounded left/right lateral acceleration และ deliberate excessive lateral acceleration ที่ทำให้ contact lift Steering controls มี zero steer และ equal-magnitude positive/negative steer

## ไฟล์ที่วางแผน

- `config/vehicle/functional_vehicle_architecture_v3_planar.json`
- `src/formula_ultimate/simulation/planar_support_gate.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/planar_support_gate_v1.json`
- `scripts/experiments/run_planar_support_gate.py`
- `tests/test_planar_support_gate.py`
- `docs/research/STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.md`
- `docs/research/STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.th.md`
- matching bilingual Work 069 plan/result records
- ignored CAD/FreeCAD/experiment evidence ใต้ `artifacts/work069/`

จะ reuse generic CAD generation และ FreeCAD inspection scripts เดิมแทนการ copy

## Validation และเกณฑ์สำเร็จ

1. Frozen v2 fail โดยเฉพาะเพราะ centre-of-mass projection อยู่นอก degenerate two-contact support segment
2. v3 ผ่าน complete functional architecture contract โดยไม่มี overlap หรือ disconnected component
3. v3 support polygon nondegenerate และครอบ geometry-derived centre-of-mass projectionด้วย positive margin
4. Static loads positive และปิด vertical, pitch, roll equilibrium ภายใน relative residual `<= 1e-9`
5. Frozen bounded acceleration/braking และ left/right lateral cases มี positive normal loads และไม่เกิน contact normal-force limits
6. Deliberate excessive lateral acceleration รายงาน contact liftและถูก rejectโดยไม่ clipping
7. Zero steer มี zero symmetric yaw response; positive/negative steeringให้ opposite bounded yaw signsภายใต้ existing combined-force tyre law
8. STEP generationและ independent FreeCAD inspectionผ่านด้วย exact component identity/solid count และ mass/centre/inertia relative residuals `<= 1e-6`
9. Canonical experiment replay และ STEP/component hashes reproduce ตรงกัน; planar half-step refinement เปลี่ยน selected metrics `<= 2%`
10. Focused/full tests, compilation, bilingual evidence, scoped commit และ post-commit clean-tree replayผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Passive support และ material/contact values ทั้งหมดยังเป็น synthetic Three-point layout เป็น validation fixture ไม่ใช่ preferred/mandatory discovered topology Quasi-static load transfer ไม่มี suspension transients, heave, pitch/roll inertia, compliance, wheel lift duration และ road roughness Existing combined-force model ยังเป็น Level-0 friction boundary ไม่ใช่ measured tyre

Work 069 ไม่ implement independent wheel speeds, differential, torque vectoring, wheel rotational integration, transient suspension, tyre thermal/wear state, full aerodynamic load maps, race trajectory control, lap fitness, physical validation หรือ safety certification Work 070 ต้องสร้าง explicit differential/carrier energy contract ก่อน independent driven-wheel dynamics
