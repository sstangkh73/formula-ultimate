# แผนระบบฟิสิกส์

> ฉบับภาษาไทยของ `PHYSICS_SYSTEM_PLAN.md`

## 1. วัตถุประสงค์

ระบบฟิสิกส์คือ evidence engine แบบแบ่งขั้นสำหรับประเมิน candidate vehicle
graph หน้าที่แรกคือ reject และจัดอันดับ candidate powertrain หนึ่งมิติอย่าง
รวดเร็วและ deterministic ระบบนี้ไม่ใช้แทน detailed vehicle validation

## 2. หลักการสำคัญ

1. **Conservation มาก่อน performance:** หาก energy หรือ force balance fail
   run นั้นเป็น invalid ก่อนพิจารณา fitness
2. **สมมติฐานชัดเจน:** approximation ทุกตัวมี fidelity level และช่วงที่ใช้ได้
   ซึ่งจัดทำเป็นเอกสาร
3. **Typed interface:** connection ของ component ส่ง physical domain และค่า SI
   ไม่ใช่ตัวเลขที่ไม่มี type
4. **มองเห็น failure:** solver divergence, clipping, thermal violation และ
   energy depletion เป็น telemetry event
5. **Deterministic replay:** version, configuration และ seed เดียวกันต้องให้
   candidate evaluation เดิมภายใน tolerance ที่ประกาศ
6. **Promotion ไม่ใช่ proof:** Level 0 เลือก candidate ไปทดสอบที่แข็งแรงขึ้น
   ไม่รับรอง performance หรือความปลอดภัยในโลกจริง

## 3. ลำดับ Fidelity

### Level 0: Analytical / 1D

- Longitudinal point-mass vehicle dynamics
- Typed energy-flow component graph
- Quasi-static component map หรือ bounded analytical model
- Basic tyre traction envelope
- Drag, rolling resistance และ road gradient
- Lumped energy และ thermal state
- Deterministic failure และ race-completion logic

### Level 1: Reduced Order

- Longitudinal/lateral/yaw vehicle dynamics
- Load transfer และ combined tyre force
- Reduced-order aerodynamics และ cooling
- Component transient ที่ละเอียดขึ้น
- Control-system dynamics และ track-following

### Level 2: 3D Candidate

- Generated geometry และ packaging
- Collision และ clearance check
- Component placement, inertia และ centre of mass
- Mesh-ready geometry และ manufacturability heuristic

#### Geometry ของ component ที่ agent ออกแบบ

Level 2 ไม่ได้จำกัดแค่การจัดวาง component จาก catalog Agent สามารถ generate
geometry และ internal topology จริงของ component รวมถึง structure, cooling
path, housing, rotor, coupling, duct และชิ้นส่วนอื่นที่ versioned geometry
language สามารถแสดงออกได้

Agent ไม่มีสิทธิ์ประกาศเองว่า geometry ของตนเบา แข็งแรง เย็น หรือมีประสิทธิภาพ
การ promote ต้องผ่าน trusted evaluation boundary:

```text
Functional requirement and interface ports
  -> agent-generated parametric CAD / B-rep / implicit geometry
  -> geometry validity and interface checks
  -> assigned material and manufacturing process
  -> independent mass, volume, inertia, and surface extraction
  -> reduced thermal/flow/structural screening
  -> selected CFD / FEA / detailed electromagnetic or mechanical analysis
  -> uncertainty-aware reduced-order component model
  -> Level-0/Level-1 vehicle and race evaluation
  -> telemetry and failures returned to the next design generation
```

วิธีนี้รักษา geometric invention ที่แท้จริง พร้อมป้องกัน generator จากการรายงาน
property ที่เป็นไปไม่ได้ด้วยตัวเอง Generated component เป็น immutable,
content-addressed artifact ซึ่งบรรจุ source representation, generator version,
seed, material, interface, meshing setting, solver setting และผลลัพธ์

Geometry promotion gate ควรรวม watertightness หรือ valid solid topology,
minimum feature size, bounded envelope, interface alignment, collision,
material assignment, manufacturing assumption, mesh convergence, solver
convergence, safety factor และความไม่สอดคล้องระหว่าง surrogate กับ
authoritative analysis Geometry ที่ดูแปลกไม่ถือเป็นเทคโนโลยีใหม่ จนกว่า
functional advantage จะผ่าน gate เหล่านี้และการเปรียบเทียบกับ baseline ที่รู้จัก

### Level 3: High Fidelity

- CFD, FEA, detailed tyre, cooling และ structural analysis
- Independent solver cross-check
- Uncertainty bound และ model calibration

### Level 4: Digital Race

- การออกแบบ full race, strategy, reliability, traffic, weather และ control ร่วมกัน
- ความ robust หลาย event แทน fastest lap เพียงครั้งเดียว

## 4. ขอบเขตระบบ Level-0

### Input

- candidate component graph และ parameter
- vehicle envelope parameter ที่ experiment กำหนดให้คงที่
- track distance, gradient และ target event definition
- ambient state
- resource, safety-proxy และ race constraint
- deterministic driver/controller policy
- numerical configuration และ seed

### State Vector

State vector ระยะแรกควรมีอย่างน้อย:

- time และ longitudinal position
- vehicle speed และ acceleration
- stored energy หรือ fuel mass ต่อ source
- component temperature
- component availability/degradation state
- controller mode และ race status
- cumulative energy-conservation residual

State ต้อง immutable ข้าม evaluation step ยกเว้นผ่าน solver update ที่ประกาศ
ห้ามใช้ hidden module-level state

### Output

- completion/failure status และเหตุผล
- elapsed time และ distance
- energy use ต่อ source และ recovered energy
- force/power ที่ส่งไป tyre endpoint แต่ละตัว
- ประวัติ component operating point และ limit
- temperature และระยะเวลาที่เกิน thermal limit
- conservation residual
- การคิด cost, mass และ volume
- deterministic replay metadata

## 5. สมการและ Contract เริ่มต้น

สมการที่วางแผนไว้กำหนดเป้าหมาย implementation ไม่ใช่ validation ที่ทำเสร็จแล้ว

### Longitudinal balance

```text
m_eff * dv/dt = F_tractive - F_drag - F_roll - m*g*sin(grade)
dx/dt = v
```

`m_eff` ต้องประกาศชัดเจนว่า rotational inertia ถูกสะท้อนเข้า vehicle mass
หรือแก้แยกต่อ rotating component

### Aerodynamic drag

```text
F_drag = 0.5 * rho_air * CdA * v_rel^2 * sign(v_rel)
```

Level 0 ใช้ `CdA` คงที่ ส่วน downforce และ aero map เลื่อนไปภายหลัง

### Rolling resistance

```text
F_roll = Crr * m * g * cos(grade) * sign(v)
```

ต้องมี zero-speed regularization เพื่อป้องกัน launch resistance เทียมหรือ
numerical sign chatter

### Tyre traction gate

```text
abs(F_longitudinal) <= mu_longitudinal * F_normal
```

Model แรกเป็น bounded envelope ไม่ใช่ detailed tyre model ต้อง log ทั้ง
saturated force และ requested force เพื่อไม่ให้ search ซ่อน traction violation

### Mechanical power

```text
P_rotational = torque * angular_speed
P_translational = force * velocity
```

Component ทุกตัวประกาศ sign convention, efficiency direction, operating
envelope และปลายทางของ loss

### Lumped thermal state

```text
C_thermal * dT/dt = P_loss - Q_rejected(T, ambient, operating_state)
```

ห้าม clip temperature เมื่อถึง limit ให้เกิด derating หรือ failure ตาม policy
ที่ component ประกาศไว้

### Energy audit

สำหรับแต่ละ step และทั้ง run:

```text
energy_in - energy_out - stored_energy_change - declared_losses = residual
```

Residual tolerance ต้อง scale ตาม energy ที่ถ่ายโอนและ numerical precision
Run ที่เกิน tolerance เป็น invalid ไม่ใช่เพียงได้ fitness ต่ำลง

## 6. Component Contract

Level-0 component model ทุกตัวต้องประกาศ:

- stable component type และ model version
- typed port และ sign convention
- parameter พร้อมหน่วย SI และ valid range
- dynamic state และ initialization
- การคิด mass, cost และ volume
- operating envelope
- loss และ thermal model
- derating และ failure behavior
- deterministic step/evaluation interface
- invariant และ reference test
- ข้อจำกัดของ fidelity

Candidate parameter ห้าม override physical limit ที่เก็บใน catalog

## 7. Simulation Pipeline

```text
Candidate graph
  -> schema and graph validation
  -> static resource accounting
  -> graph compilation and solver ordering
  -> initial-state validation
  -> controller demand
  -> component-network solve
  -> tyre traction gate
  -> vehicle-state integration
  -> energy and thermal update
  -> invariant/failure checks
  -> telemetry append
  -> finish, fail, or next timestep
  -> independent post-run audit
```

คำนวณ fitness หลัง independent audit ยอมรับ run แล้วเท่านั้น

## 8. Numerical Strategy

- เริ่มด้วย deterministic fixed-step integration เพื่อ replay ได้โปร่งใส
- ซ่อน solver choice ไว้หลัง interface เพื่อใช้ reference integrator ได้
- ประกาศ absolute/relative tolerance ใน versioned configuration
- Reject NaN, infinity, negative mass/energy, time reversal และ non-monotonic
  race distance เว้นแต่ experiment รองรับ reverse motion อย่างชัดเจน
- ตรวจ algebraic-loop non-convergence ด้วย iteration ที่มีขอบเขตและบันทึก
  failure reason
- ทำ timestep-convergence test ก่อนเลือก production timestep
- ปฏิบัติต่อ forward-only zero-speed boundary เป็น unilateral constraint และ
  บันทึก impulse แยกจาก unconstrained road-load force ห้ามซ่อน step ที่ถูก
  ป้องกันไม่ให้ถอยหลังเป็น acceleration ปกติ

## 9. Failure Taxonomy

อย่างน้อยต้องมี:

- invalid topology
- invalid parameter หรือ initial state
- resource-budget violation
- solver non-convergence
- conservation violation
- energy depletion
- thermal limit/derating/failure
- traction saturation
- component envelope violation
- timeout หรือวิ่งไม่จบ
- numerical invalidity
- successful completion

Traction saturation อาจเป็น operating event ที่ valid แต่การเกิน model โดยไม่
ผ่าน saturation gate คือ physics violation ต้องรักษาความแตกต่างนี้ไว้

## 10. Package Boundary

- `components`: component physics และ catalog ที่นำกลับใช้ได้
- `topology`: graph representation, compilation, mutation และ validity
- `physics`: domain equation, unit, integrator และ invariant check
- `simulation`: race loop และ fidelity orchestration
- `telemetry`: schema, run record, audit และ replay metadata
- `experiments`: baseline, search comparison, seed และ analysis entrypoint

Search algorithm ห้าม import internal solver state หรือข้าม graph gate
Physics code ห้ามคำนวณ evolutionary fitness

## 11. Implementation Milestone

1. Units, quantity naming, schema และ failure type
2. Analytical point-mass coast-down และ constant-force reference model
3. Tyre traction gate และ road-load model
4. Minimal electrical source -> motor -> tyre baseline
5. Telemetry และ independent conservation audit
6. Fixed EV/ICE/hybrid reference topology
7. Typed graph validation และ compilation
8. Topology mutation/search พร้อม equal-budget experiment
9. Timestep convergence และ Level-0/Level-1 promotion study
10. Versioned geometry language และ trusted 3D property-extraction pipeline
11. Agent-generated component geometry พร้อม multi-fidelity promotion gate

แต่ละ milestone ต้องมี pre-work plan และ post-work result record ของตัวเอง
