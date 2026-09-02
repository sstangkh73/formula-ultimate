# Roadmap รถทั้งคันที่ Geometry เป็นสาเหตุ V1: Work 077-086

ต้นฉบับภาษาอังกฤษ: `GEOMETRY_CAUSAL_WHOLE_VEHICLE_ROADMAP_V1.md`

## เป้าหมายปลายทางและขอบเขตคำกล่าวอ้าง

Candidate จะเป็น **รถเชิงกลทั้งคันที่พร้อมเริ่มวิจัยทั้งคัน** เมื่อมีชิ้นส่วนทางกายภาพแยกได้จริงแทนหนึ่งกล่องต่อหนึ่งหน้าที่; ทุก part มีหลักฐาน geometry, material, interface และ tolerance; joint/DOF ของ assembly ตรวจได้; force/power path เกิดจาก geometry; STEP/FreeCAD ให้ mass, centre of mass, inertia, thickness, section property และ moment arm; load เข้า mesh แล้วเกิด stress/deformation; yield, fracture, fatigue, torsion, buckling และ connection failure เกิดได้; damage ส่งกลับเข้าระบบรถและทำให้ `DNF` ได้; seed/config replay แบบ deterministic; และห้ามเปลี่ยน geometry หลังเห็น admitted result

เป้าหมายนี้คือความพร้อมเริ่มวิจัย ไม่ใช่ physical validation ต้องผ่าน higher-fidelity validation และการเทียบข้อมูลจริงก่อนอ้างที่แรงกว่า

```text
Functional requirement
  -> agent proposes topology and parts
  -> parametric 3D B-rep
  -> assembly joints and interfaces
  -> STEP hash
  -> independent FreeCAD inspection
  -> geometry-derived physics inputs
  -> FEA / kinematics / torque / thermal tests
  -> failure or survival
  -> mutation and deterministic replay
  -> whole-vehicle Level 0 admission
```

## จังหวะทำงานชุดละสาม Work

ดำเนินการเป็น batch จำกัดขอบเขต: `077-079`, `080-082`, `083-085` แล้วจบด้วย `086` คำว่า “ทีละ 3 work” จำกัด active scope แต่ไม่ตัด dependency หรือรวมหลักฐาน แต่ละ Work ต้องทำตามลำดับและ commit หลัง validation ของตัวเองผ่าน หากสมมติฐานถูกปฏิเสธหรือ dependency ติดขัด ให้สร้าง remedial work ใหม่แทนการลด gate และยังไม่อนุญาต push อัตโนมัติ

## Work 077 — Geometry-Causal Part Contract V1

กำหนด declaration ขั้นต่ำของ part: identity, function tags, feature provenance ตามลำดับ, material record identity, local frame, datum/reference axes, typed interfaces, load/application regions และ path, manufacturing process ที่อนุญาต, tolerance, minimum feature size, parameter provenance และ claim boundary Interface ขั้นต้นครอบคลุม fixed, revolute, prismatic, spherical, bearing, shaft/spline, bolted, welded, ground, thermal และ electrical/fluid intent

Control สลับ key และฉีด unknown field/unit, material/interface/load path ที่หาย, `NaN`, negative thickness, invalid tolerance/frame/provenance และ unsupported interface ผลสำเร็จต้องได้ canonical bytes/hash แบบ deterministic และปฏิเสธ fail-closed อย่าง exact การผ่านนิยามว่า declaration ของ part คืออะไร แต่ไม่พิสูจน์ geometry, material, manufacturing หรือ strength

## Work 078 — Parametric B-rep Feature Grammar V1

สร้างคำสั่ง CAD แบบ bounded SI สำหรับ sketch profile, extrude, revolve, pocket/cut, through hole, stepped bore, shaft shoulder, rib/web, shell/wall thickness, linear/circular pattern, bounded fillet/chamfer และ boolean union/subtract/intersect ทุก operator มี parameter bounds, provenance, solid-validity check และปฏิเสธ zero thickness/self-intersection

Corpus ที่ผ่านต้องมีอย่างน้อย shaft, bracket, hollow housing, ribbed plate และ hub-like rotating part Config/toolchain เดิม replay แล้วต้องได้ canonical STEP hash เดิม การผ่านทำให้ออกแบบ single part จริงภายใน grammar ที่รับได้ แต่ไม่ยืนยัน arbitrary CAD topology, structural capacity หรือ manufacturing feasibility

## Work 079 — Engineering Material and Manufacturing Contract

เชื่อม material record ที่มีหลักฐานเข้ากับ part ทางกายภาพ Record ต้องประกาศ density, Young's modulus, Poisson ratio, shear modulus, yield/ultimate strength, fracture toughness, fatigue/S-N evidence หรือระบุว่าไม่มี, thermal conductivity, heat capacity, thermal expansion, allowable temperature range, source, confidence และ domain Manufacturing record ต้องประกาศ minimum wall, hole, ligament/web, tool access, machining/bend radius, unsupported-feature policy, tolerance class, process และ evidence

ตัวแปรอิสระรวมการเลือก material/process และมิติ geometry ตัวแปรตามรวม admission, ความพร้อมของ mass/stiffness/strength/thermal property และ manufacturing violation Control ครอบคลุม elastic constant ไม่สอดคล้อง, strength ordering เป็นไปไม่ได้, unit/source/domain หาย, fatigue claim ไม่มีหลักฐาน, wall/hole/web เล็กเกิน, tool access fail และ invalid tolerance Agent ลดความหนาได้ต่อเมื่อรับผลต่อ mass, stiffness, stress, buckling, fatigue, thermal และ manufacturing โดยตรง การผ่านห้ามใช้ “maximum force” ลอย ๆ แทน material/geometry evidence

## Work 080 — Mechanical Assembly and Joint Kernel

Implement mate ด้วย datum/axis/surface; rigid, revolute, prismatic, spherical joint; limit; bearing alignment; axial/radial clearance; interference และ minimum gap; fastener preload declaration; connection stiffness/compliance; และ intended-DOF calculation

การหักล้างรวม shaft misalignment, bearing สองตัว overconstrained, collision ตลอด motion envelope, tolerance หลวมเกิน และ realized DOF ต่างจาก declaration การผ่านแยก fixed/sliding/rotating/colliding behavior ได้ แต่ไม่ยืนยัน bearing life, fastener/weld strength, friction, wear หรือ full multibody dynamics

## Work 081 — STEP to FreeCAD Geometry Witness V2

ตรวจ exact CadQuery STEP hash อย่างอิสระและดึง solid count, volume, mass, centre of mass, inertia tensor, bounding box, principal axes, hole/shaft diameter, local wall thickness, section property, interface position, joint axis, load/contact surface และ clearance/interference จำนวน part/solid และ mass property ต้องปิด residual ภายใน tolerance ที่ preregistered โดยไม่มี hidden geometry repair

Semantic interface ต้องรอดผ่าน exchange ด้วย geometry signature และ datum witness แทน face number เปราะบาง เช่น `Face17` การผ่านยกเลิกการพิมพ์ motion ratio, lever arm, shaft radius และ mass ด้วยมือเมื่อวัดจาก CAD ได้ แต่ OCCT-family cross-check ยังไม่ใช่ physics validation ที่อิสระเต็มรูปแบบ

## Work 082 — Geometry-to-Structural Physics Coupling

เลือก support/load surface จาก witness, mesh exact geometry, ทำ mesh-convergence study, ใช้ material จาก Work 079 และ declared load case, parse stress/strain/displacement/reaction, ประเมิน failure และส่ง state เข้า connection graph Mode ที่ observable ได้แก่ elastic deformation, yield/plasticity, ultimate overload, fracture-domain violation, fatigue, torsion, local/global buckling และ solver divergence/invalid state

Control บังคับว่า geometry หนาขึ้นต้องไม่อ่อนลงโดยไม่มีคำอธิบาย, load path ที่ถูกตัดส่งแรงไม่ได้, reaction ต้องสมดุล, mesh ต้อง converge, connection ที่ fail ไม่ส่ง forbidden load ต่อ และ numerical failure ห้ามถูกซ่อมเงียบ การผ่านทำให้ “บางเกินไปแล้วหัก” มีสาเหตุจาก geometry/material/load ใน case ที่ทดสอบ แต่ยังไม่ใช่ whole-vehicle หรือ real-world validation

## Work 083 — Ground-Interaction Module Candidate 001

สร้าง multi-part subsystem แรกโดยไม่บังคับ conventional suspension หรือ wheel architecture ต้องสัมผัสพื้น; รับ normal/longitudinal/lateral force; รับ/ส่ง torque; เปลี่ยนทิศแรง; ให้ vertical motion ที่ประกาศ; ส่งแรงสู่ structural mount; เบรก; และจำกัด DOF ที่ไม่ต้องการ

ตัวแปรอิสระคือ topology, part count, joint position, section geometry, thickness, material, support spacing, contact radius และ motion ratio ตัวแปรตามคือ mass, stiffness, stress/fatigue/buckling margin, steering response, travel, torque efficiency, unsprung-equivalent inertia และ failure mode ผลสำเร็จคือ FCStd assembly ที่ตรวจได้ ประกอบจาก part จริง มี joint motion ที่ยืนยันและ ground-to-structure load path ต่อเนื่อง

## Work 084 — Energy Conversion and Torque-Path Candidate 001

แทนกล่อง `energy_converter` และ ratio ตัวเลขด้วย energy-store interface, converter geometry/mounting, input/output shaft หรือกลไกเทียบเท่า, torque multiplication, bearing/support, output coupling, housing, lubrication/cooling interface, braking-energy path และ thermal-loss ledger เทคโนโลยียังคง neutral แต่ candidate ต้องระบุ technology และ evidence

ทดสอบ torque equilibrium, shaft torsion, bearing reaction, housing deformation, rotational-speed limit, energy conservation, efficiency/loss, heat rejection และฉีด seized/broken connection ผลสำเร็จต้องให้ torque วิ่งผ่าน part/interface จริงจาก converter ถึง ground-interaction module แต่ยังไม่ยืนยัน motor/engine/battery/fuel system ทางกายภาพ

## Work 085 — Load Structure, Packaging และ Thermal Integration

แทน `load_spine` ด้วย load structure ที่ agent ออกแบบและรองรับทุก subsystem ผ่าน mount จริง บังคับ placement ไม่มี interference, service/removal path, power/control/fluid routing, heat-source/rejection interface, ground clearance, motion envelope และการส่ง braking/cornering/bump/torque-reaction load ประเมิน bending, torsion, buckling, fatigue และ mount failure

ผลสำเร็จคือ structure ที่เกิดจาก load path และ packaging constraint ไม่ใช่กล่องที่ดูเหมือนรถ แต่ไม่พิสูจน์ crashworthiness, occupant safety, production assembly, cooling correlation หรือ regulatory compliance

## Work 086 — Whole Mechanical Vehicle Candidate 001

รวม subsystem ทุกตัว Artifact ขั้นต่ำคือ individual STEP, complete assembly STEP, FCStd, assembly tree, joint/DOF manifest, material manifest, mass/COM/inertia report, interference report, structural load-case report, torque/power/energy ledger, failure-propagation report, deterministic replay manifest และ Level 0 result

Admission case รวม static support, acceleration, braking, steady cornering, combined braking/cornering, bump/vertical event, torque reaction, thermal duration, one-connection failure, refinement/replay และ mirrored/control candidate ผลสำเร็จคือรถเชิงกลมี part จริงพร้อมเริ่มวิจัยทั้งคัน และยังไม่ validated จนกว่า higher-fidelity/real-data evidence จะผ่าน

## Contract การทดลองร่วม

ตัวแปรควบคุมคงที่คือ SI units, toolchain version, material-library version, random seed, solver tolerances, mesh policy, load cases, component library, compute budget และ baseline candidate ทุก Work ต้องบันทึก independent/dependent variables, controls, metrics, success/failure criteria, supporting evidence, contradicting evidence, alternative explanations, missing evidence, residuals, solver failures และ confidence

Work ที่ Completed ทุกตัวต้องมี plan/result EN/TH, unit/acceptance tests, exact commands/exit codes, staged-scope inspection, `git diff --cached --check` และ scoped commit ทันที ต้อง freeze geometry/config ก่อน admitted result และห้ามแก้ geometry ลับหลังตามผล
