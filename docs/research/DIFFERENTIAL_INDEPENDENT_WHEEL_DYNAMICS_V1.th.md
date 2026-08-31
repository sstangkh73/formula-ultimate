# Differential และพลวัตล้อขับเคลื่อนอิสระ v1

เอกสารต้นฉบับภาษาอังกฤษ: `DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.md`

## ผลลัพธ์และขอบเขต

Work 070 แทน approximation ความเร็วล้อร่วมของ Work 068 ด้วย ideal open-differential specimen แบบ deterministic จุดสัมผัสขับเคลื่อนสองจุดของสถาปัตยกรรม v3 ที่เสถียรจาก Work 069 มีความเร็วเชิงมุมอิสระแล้ว โดยคง geometry, materials, support loads, powertrain, contact limits และแหล่งพลังงานชุดเดิม

งานนี้เป็น Level-0 lumped dynamics contract ภายใน component `torque_transmission` ที่มีอยู่ ตรวจ kinematics, inertia accounting, energy transfer, loss, limits, failure propagation และ replay ไม่ใช่ geometry เฟืองที่ resolve แล้ว ฮาร์ดแวร์ differential จากการวัด transient suspension หรือ physical validation ของรถทั้งคัน

## พิกัดและการคิด inertia

สำหรับความเร็ว carrier `omega_c` และความเร็ว differential mode `delta_omega`:

```text
omega_L = omega_c - delta_omega
omega_R = omega_c + delta_omega
omega_c = (omega_L + omega_R) / 2.
```

solid ขับเคลื่อนแต่ละข้างมี axial inertia จาก geometry `0.13034241725073026 kg m^2` output inertia ที่ตรึงจาก Work 067 ปิดดังนี้:

```text
J_other + J_L + J_R
= 2.2393151654985397 + 0.13034241725073026 + 0.13034241725073026
= 2.5 kg m^2.
```

ดังนั้น common wheel inertia อยู่ใน `J_output` แล้ว พลังงานที่เพิ่ม downstream มีเฉพาะ independent mode:

```text
J_delta = J_L + J_R = 0.2606848345014605 kg m^2
E_delta = 0.5 J_delta delta_omega^2.
```

วิธีนี้ป้องกันการนับ wheel inertia ซ้ำ

## Torque, efficiency และ modal energy

powered branch แต่ละข้างใช้ connection efficiency จากสถาปัตยกรรม `eta_i = 0.98` wheel load torque `tau_i = F_i r_i` ถูก reflect ไปยัง carrier เป็น:

```text
q_i = tau_i / eta_i.
```

เมื่อ modal damping `c_delta = 0.02 N m s/rad` independent mode เป็นไปตาม:

```text
J_delta d(delta_omega)/dt = q_L - q_R - c_delta delta_omega.
```

การอัปเดต damping แบบ implicit midpoint ทำให้ partition ต่อ step ชัดเจน:

```text
W_carrier
= W_reflected_left + W_reflected_right
  + Delta(E_delta) + Q_differential.
```

จากนั้น reflected branch work แต่ละข้างถูกแบ่งเป็น wheel input work กับ connection heat และ wheel input work ถูกแบ่งเป็น body work กับ longitudinal slip heat การสูญเสียติดลบเกิน tolerance ถูกปฏิเสธ

## ผล reference และ split grip

การรันที่อนุมัติทั้งหมดใช้ throttle `0.5`, duration `2 s`, step `0.0005 s` และ `4000` steps

| Metric | สมมาตร `mu=(1.2,1.2)` | Split `mu=(1.0,1.2)` | Mirrored `mu=(1.2,1.0)` |
| --- | ---: | ---: | ---: |
| ความเร็วรถสุดท้าย | `11.68448249437216 m/s` | `9.96057727044386 m/s` | `9.96057727044386 m/s` |
| ระยะสุดท้าย | `11.742989097609598 m` | `10.255133327646465 m` | `10.255133327646465 m` |
| carrier speed | `103.15502526901471 rad/s` | `107.65471518711871 rad/s` | `107.65471518711871 rad/s` |
| left speed | `103.15502526901471 rad/s` | `141.05601957062677 rad/s` | `74.25341080361065 rad/s` |
| right speed | `103.15502526901471 rad/s` | `74.25341080361065 rad/s` | `141.05601957062677 rad/s` |
| `delta_omega` สุดท้าย | `0 rad/s` | `-33.401304383508055 rad/s` | `33.401304383508055 rad/s` |
| modal energy สูงสุด | `0 J` | `324.1158550756573 J` | `324.1158550756573 J` |
| slip heat | `13922.812590781254 J` | `14984.833885342356 J` | `14984.833885342356 J` |
| branch-connection heat | `687.7218665085455 J` | `599.8816054535888 J` | `599.8816054535888 J` |
| differential heat | `0 J` | `60.115830964968396 J` | `60.115830964968396 J` |

grip สมมาตรคงความเร็วล้อเท่ากันตรง ๆ และ modal energy เป็นศูนย์ เมื่อ split grip แขนซ้ายที่ grip ต่ำกว่าหมุนเร็วขึ้น ส่วนแขนขวาที่รับโหลดสูงกว่าหมุนช้าลง การสลับ friction ทำให้สถานะสอง branch สลับกันตรง ๆ และคงความเร็วรวม ระยะ พลังงาน และ loss เท่าเดิม

## Residuals, controls และ replay

สำหรับ split-grip run:

- carrier-average residual สูงสุด: `1.4210854715202004e-14 rad/s`;
- modal-equation residual สูงสุด: `5.9534599472499394e-12 N m`;
- torque residual สูงสุด: `0 N m`;
- interface energy residual สูงสุด: `1.9071116214020023e-12 J`;
- global energy residual สูงสุด: `0.5030174478888512 J`;
- global relative residual สูงสุด: `1.0060348957777023e-8`;
- contact utilization สูงสุด: `1.0`

global residual ถูกแสดงและต่ำกว่าเพดาน `1e-3` ที่ตรึงไว้มาก เมื่อลด time step ครึ่งหนึ่ง metric ปลายทางที่เลือกเปลี่ยนสูงสุด `0.00023334677638767642` ต่ำกว่าขีด refinement `0.02`

พลังงาน onboard ศูนย์ให้ torque, force, speed, distance, slip heat, connection heat และ modal energy เป็นศูนย์ทั้งหมด การตั้ง operational branch-speed limit เป็น `25 rad/s` อย่างตั้งใจทำให้เกิด `differential_branch_overspeed` ที่ step `532`, รถไปได้ `0.2040023153031444 m` และจบ `DNF`; terminal state ทำงานต่ออีก step ไม่ได้

reference result SHA-256 คือ `c23eea2641b6863da2d63eb8a2ca3b7ae5ad94a53822c70bffd8fa1bffb1b92a` split result SHA-256 คือ `eee844e411d194c5d2205e5467ce42d3877867b013863fd4cd0772bda2be4879` exact replay ให้ทั้งสองค่าซ้ำ และให้ canonical experiment evidence SHA-256 `bc23719a3fbd0d343898488f263bf805d8aae8152acc6de4ef23ff2d410cd79a`

## หลักฐาน geometry และความมั่นใจ

materialized architecture SHA-256 ยังคงเป็น `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418` JSON bytes ตรงกับ geometry หลัง commit ของ Work 069 จึงยังใช้หลักฐาน STEP/FreeCAD `11` solids ที่ตรวจแล้วได้ และ Work 070 ไม่มี hidden geometry change

focused tests `9` รายการและ repository tests ทั้งหมด `421` รายการผ่าน ความมั่นใจสูงสำหรับสมการ lumped ที่ประกาศ branch symmetry แบบ deterministic การ reconcile identity/limits การทำบัญชีพลังงาน failure state และ numerical replay แต่ความมั่นใจต่อความทนทาน differential จริงหรือการทำนาย traction ยังต่ำ เพราะ coefficient และกลไกภายในเป็น synthetic

## หลักฐานที่ยังขาดและงานถัดไป

specimen ใช้ ideal `50:50` open torque split, lumped reflected branch inertia, แรงปกติสถิตคงที่ และไม่มี reverse rotation ยังไม่มี differential gear tooth contact, shaft torsion ต่อ branch, bearing friction maps, backlash, housing deformation, lubricant thermal state, limited-slip/torque-vectoring logic, wheel hop, tyre relaxation และ friction/slip curve จากการวัด

งานถัดไปควรเชื่อม independent wheel states เหล่านี้กับ planar yaw/contact dynamics จาก Work 069 พร้อม transient normal-load transfer ที่ derive จาก geometry หลังจากนั้นต้องเพิ่ม geometry ภายใน transmission และ structural/thermal verification ก่อนเรียก candidate ว่าเป็นรถทั้งคันที่ละเอียด
