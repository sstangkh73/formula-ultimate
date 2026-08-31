# แผนงาน 066: Functional Vehicle Architecture v2

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_066_functional-vehicle-architecture-v2-plan.md`

## วัตถุประสงค์

แทนที่ four-placeholder Work 047 vehicle fixture ในฐานะ next-generation research input ด้วย technology-neutral multi-component functional vehicle architecture Candidate ที่ admit ต้องมี 3D solids ที่ derive ได้, materials, typed ports, compatible connections, explicit energy/torque/control/thermal/structural paths และ failure-relevant limits การติดป้าย propulsion โดยไม่มี conversion/transmission path ที่เชื่อมทางกายภาพห้ามสร้างแรง

งานนี้สร้างและ validate architecture grammar พร้อม fixed reference fixture หนึ่งชุด แต่ยังไม่แทน frozen Work 062 campaign และไม่อ้างว่า reference fixture ถูก optimize

## คำถามวิจัยและสมมติฐาน

คำถาม: architecture contract ชุดเดียวสามารถแทนรถที่มีชิ้นส่วนหลายชิ้นอย่างเห็นได้ชัด โดยยัง neutral ต่อ component count, layout, energy technology, conversion method, transmission type และ ground-interaction mechanism ได้หรือไม่

Preferred hypothesis: reference fixture และ CAD ที่ regenerate อย่างอิสระผ่าน typed graph, geometry, mass, packaging, energy, torque, thermal, control และ structural-path contracts ทั้งหมด ส่วน deliberate broken-path และ incompatible-port controls fail closed ด้วย deterministic codes

Falsification รวม accepted floating component, undeclared force source, domain-mismatched connection, ไม่มี storage-to-ground power path, ไม่มี load-to-ground structural path, ไม่มี heat-source-to-sink path, uncontrolled actuator, physical limit ไม่เป็นบวก/invalid, solids overlap, STEP invalid, mass/inertia mismatch, nondeterministic identity หรือ negative control ผ่าน

## Functional contract

Candidate ใช้ topology หรือ technology ใดก็ได้ แต่ต้อง instantiate capabilities ที่เทียบเท่ากับ:

1. energy storage
2. energy conversion
3. torque หรือ power transmission
4. ground interaction/propulsion
5. direction control
6. braking
7. load-bearing structure
8. thermal management
9. sensing/control

ไม่บังคับ conventional engine, motor, gearbox, wheel count, body form หรือ layout Capability ถูกระบุผ่าน function tags และ connected typed ports ไม่ใช่ชื่อ component

## Typed physical domains

- `structural`: six-component load path ผ่าน declared mount interfaces
- `electrical`: energy/power transfer พร้อม voltage, current, efficiency และ capacity limits ตามที่เกี่ยวข้อง
- `mechanical_rotary`: torque, angular speed, inertia, ratio และ efficiency limits
- `thermal`: heat flow, temperature limit และ heat-rejection capacity
- `control`: command/sensor connectivity; ไม่ขน mechanical energy
- `ground`: declared external contact ที่ส่ง bounded longitudinal/lateral/normal forceได้

Connections ต้องเชื่อม compatible domains และอ้าง exact component ports Energy/mechanical losses ต้องกลายเป็น heat ส่วน control edges ห้ามใช้แทน power edges

## Geometry และ CAD scope

Functional component ทุกชิ้นต้องมี declared primitive solid หนึ่งชิ้น, SI dimensions, pose, material density, ports ที่อยู่บนหรือภายใน solid และ explicit limits Work 066 จะสร้าง STEP ต่อ component และ multi-solid assembly STEP แล้วตรวจ assembly อย่างอิสระด้วย FreeCAD Geometry-derived mass, centre of mass, inertia, solid count, component identities และ hashes ต้อง replay

Reference fixture ใช้ simple boxes/cylinders ได้เพราะงานนี้ validate architecture/evidence plumbing ไม่ใช่ detailed manufacturing geometry แต่ solid แต่ละชิ้นยังเป็น distinct functional component ไม่ใช่ decorative body ก้อนเดียว

## ไฟล์ที่วางแผน

- `src/formula_ultimate/topology/functional_vehicle.py`
- exports ใน `src/formula_ultimate/topology/__init__.py`
- `config/vehicle/functional_vehicle_architecture_v2.json`
- `scripts/cad/generate_functional_vehicle_v2.py`
- `scripts/cad/inspect_functional_vehicle_v2_freecad.py`
- `tests/test_functional_vehicle_architecture.py`
- bilingual research/result documentation และ ignored evidence ใต้ `artifacts/work066/`

## Independent variables, controls และ metrics

- Independent variables: component count, function allocation, primitive geometry, material, pose, port domains/locations, connection topology, energy/conversion/transmission parameters, ground contacts และ thermal/control routing
- Dependent variables: admission status/codes, path completeness, port compatibility, power/torque/heat limits, component/assembly mass properties, overlap/containment, STEP validity, FreeCAD residuals และ replay fingerprints
- Controls: SI units, right-handed `x` forward/`y` left/`z` up frame, frozen material records, deterministic ordering/serialization, explicit external environment node, zero silent repair และ fixed numerical tolerances
- Metrics: required-capability coverage, path count, component/connection/contact count, declared เทียบ geometry-derived mass residual, centre/inertia residual, solid count, invalid-control rejection count และ SHA-256 replay

## Validation และเกณฑ์สำเร็จ

1. Reference architecture ผ่าน exact schema และ physics-path validation
2. Storage เชื่อมถึงทุก ground-propulsion capability ผ่าน compatible energy/conversion/transmission edges
3. ทุก non-ground component มี structural path ไป declared ground contact
4. ทุก heat-producing component มี thermal path ไป heat-rejection capability
5. Conversion, direction และ braking actuators มี control paths จาก controller
6. Declared limits ทุกค่าต้อง finite, positive ตามที่ต้องใช้ และ locally conservative; efficiency อยู่ใน `(0, 1]`
7. Deliberate broken-path, mismatched-domain, floating-component, overlap, invalid-limit และ force-from-nowhere controls ถูก reject
8. CAD generation และ FreeCAD inspection ผ่านด้วย exact component count/identity, valid solids, ไม่มี hidden repair และ relative mass/centre/inertia residuals `<= 1e-6`
9. Focused/full tests, compilation, bilingual evidence, scoped commit และ post-commit clean-tree replay ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Reference architecture แรกอาจ bias search ภายหลังหากถูกใช้เป็น preferred layout; มันเป็นเพียง fixed validation baseline Primitive geometry ยัง resolve gear teeth, bearings, windings, seals, fasteners, fluid passages, local joints, crash structures หรือ manufacturing tolerances ไม่ได้ Work 066 ยังไม่ implement transient drivetrain dynamics, efficiency maps, combustion/electromagnetic physics, tyre/suspension coupling, detailed cooling flow, structural FEA, contact, fatigue, fracture, controls optimization, race fitness, independent replication, physical validation, safety certification หรือ discovery claim งานเหล่านี้ต้องเป็น work item แยก
