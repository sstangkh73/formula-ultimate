# แผน Work 070: Differential และพลวัตล้อขับเคลื่อนอิสระ

สถานะ: เสร็จสมบูรณ์ (Completed)

เอกสารต้นฉบับภาษาอังกฤษ: `2026-08-31_070_differential-independent-wheel-dynamics-plan.md`

## วัตถุประสงค์และขอบเขต

แทนสมมติฐานความเร็วล้อร่วมของ Work 068 ด้วย differential/carrier contract ที่อนุรักษ์พลังงานอย่างชัดเจนสำหรับจุดสัมผัสขับเคลื่อนสองจุดของแบบอ้างอิง v3 ที่มีฐานรองรับเสถียรจาก Work 069 แบบจำลองต้องยอมให้ความเร็วเชิงมุมซ้าย/ขวาต่างกันเมื่อโหลดสัมผัสต่างกัน คง radius/inertia จาก geometry และแรงปกติสถิต เคารพขีดจำกัด port/connection ของสถาปัตยกรรม แสดง loss/residual ทุกส่วน และส่งต่อ differential/branch failure เป็น `DNF`

งานนี้เปลี่ยนเฉพาะ dynamic model และ experiment declaration โดยใช้สถาปัตยกรรม 3D ที่ materialize และหลักฐาน STEP/FreeCAD ชุดเดิมจาก Work 069 เพราะไม่มี solid ภายนอกเปลี่ยน Differential ยังเป็นกฎ lumped ภายใน component `torque_transmission`; การแยก gear/bearing เป็น solid อิสระถูกเลื่อนไว้อย่างชัดเจน

## แบบจำลองฟิสิกส์และกฎห้ามนับซ้ำ

สำหรับความเร็ว carrier `omega_c` และความเร็วโหมด differential `delta_omega`:

```text
omega_L = omega_c - delta_omega
omega_R = omega_c + delta_omega
omega_c = (omega_L + omega_R) / 2.
```

output inertia ของ Work 067 `J_output = 2.5 kg m^2` รวม common-mode contribution ของ inertia ล้อทั้งสองที่ derive จาก geometry แล้ว:

```text
J_output = J_other + J_L + J_R.
```

ดังนั้นพลังงานโหมดอิสระเพิ่มเพียง

```text
E_delta = 0.5 (J_L + J_R) delta_omega^2,
```

และจะไม่เพิ่ม wheel common-mode inertia ซ้ำ สำหรับ reflected branch load torque `q_L`, `q_R`, modal inertia `J_delta = J_L + J_R` และ differential damping `c_delta`:

```text
J_delta d(delta_omega)/dt = q_L - q_R - c_delta delta_omega.
```

การอัปเดต damping แบบ implicit midpoint ต้องปิด identity ต่อ step:

```text
W_carrier = W_reflected_branches + Delta(E_delta) + Q_differential.
```

connection แต่ละ branch ในสถาปัตยกรรมประกาศ efficiency `eta = 0.98` torque ที่ล้อ `tau_i` ถูก reflect ต้นทางเป็น `q_i = tau_i / eta`; ผลต่าง `q_i omega_i - tau_i omega_i` เป็น connection heat ที่สังเกตได้ จากนั้น wheel input work แบ่งเป็น body workและ slip heat การสูญเสียติดลบเกิน tolerance ถือว่า invalid แทนการ clip เงียบ ๆ

## การออกแบบการทดลอง

- ตัวแปรอิสระ: friction coefficient ซ้าย/ขวา, แรงปกติสถิตจาก geometry v3, throttle, พลังงานเริ่มต้น, step size, branch connection efficiency, differential damping และ branch speed limit
- ตัวแปรตาม: carrier/left/right speed, differential-mode speed/energy, drive/load torque ต่อ branch, force/slip/utilization, connection heat, differential heat, ความเร็ว/ระยะรถ, interface/global energy residual, failure state/time และ replay hash
- controls: grip สมมาตร, พลังงานศูนย์, split grip แบบ mirrored, branch-speed limit ที่ลดอย่างตั้งใจแต่ยัง admissible, half-step refinement, geometry Work 069 ที่ไม่แก้, powertrain declaration คงที่ และ ordering deterministic
- สมมติฐานที่ต้องการ: grip สมมาตรคง `delta_omega = 0`; split grip ทำให้ branch speed ต่างกันแบบจำกัดโดยไม่ละเมิดค่าเฉลี่ย carrier หรือ energy identity; mirrored grip สลับสถานะ branch; การรันที่อนุมัติทั้งหมดเคารพขีดจำกัดและ replay ตรงกัน
- การหักล้าง: ยังได้ common speed เมื่อโหลดไม่เท่ากัน, carrier average ไม่ปิด, wheel inertia ถูกนับสองครั้ง, branch connection loss หาย, มี hidden energy creation, branch เกิน port speed/torque โดยไม่ `DNF`, พลังงานศูนย์สร้างการเคลื่อนที่, mirrored cases ไม่สมมาตร หรือ half-step/replay ไม่ผ่าน

## ไฟล์ที่วางแผน

- `config/vehicle/functional_differential_drive_v1.json`
- `src/formula_ultimate/simulation/differential_drive_coupling.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_differential_drive.py`
- `tests/test_differential_drive_coupling.py`
- `docs/research/DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.md`
- `docs/research/DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.th.md`
- บันทึกผล Work 070 สองภาษาที่ตรงกัน
- หลักฐาน deterministic ที่ git ignore ใต้ `artifacts/work070/`

## Validation และเกณฑ์สำเร็จ

1. loader materialize และ validate สถาปัตยกรรม v3 ของ Work 069 ระบุ powered branches สองแขนพอดี และ reconcile identity ของ component/contact/port/connection
2. radius และ axial inertia ตรงกับ geometry component ภายใน relative tolerance `<= 1e-9`; `J_other + J_L + J_R = 2.5 kg m^2` ภายใน tolerance เดียวกัน
3. แรงที่ driven contact สถิตตรงกับคำตอบสมดุล Work 069; passive rear contact ไม่ถูกใช้เป็นแหล่ง propulsion
4. ทุก step ที่อนุมัติปิด `(omega_L + omega_R)/2 = omega_c`, branch speed ไม่ติดลบและไม่เกินขีดจำกัดสถาปัตยกรรม และ torque ที่ส่งไม่เกิน port limit
5. grip สมมาตรคง independent-mode speed/energy เป็นศูนย์ภายใน numerical tolerance
6. grip ไม่เท่ากันสร้าง independent speed และ modal energy ที่ไม่เป็นศูนย์ ขณะ carrier/interface/global energy residual ต่ำกว่าเพดานที่ประกาศ
7. mirrored unequal-grip controls สลับสถานะซ้าย/ขวาและคง aggregate vehicle metrics เท่ากันภายใน tolerance
8. พลังงาน onboard ศูนย์ให้ drive torque, force, vehicle motion และ differential-mode energy เป็นศูนย์
9. การลด branch-speed limit ที่ admissible อย่างตั้งใจทำให้เกิด terminal branch-overspeed `DNF` ที่สังเกตได้; ระบบปฏิเสธการทำงานต่อหลัง terminal failure
10. exact replay, half-step refinement `<= 2%`, focused/full tests, compilation, หลักฐานสองภาษา, scoped commit และ post-commit clean-tree replay ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

แบบจำลองนี้เป็น ideal open-differential kinematic/energy specimen พร้อม lumped damping ไม่ได้ resolve tooth contact, backlash, bearing compliance, housing stress, lubricant flow, torque-vectoring control, limited-slip clutch friction, brake intervention, reverse rotation, wheel hop, transient suspension, tyre thermal/wear state หรือ coefficient จากการวัด ยังคงใช้แรงปกติสถิตจาก Work 069; transient load transfer อยู่นอก specimen ตามยาวนี้

Work 070 ไม่กล่าวอ้าง handling จริง ความทนทาน ความพร้อมผลิต การจบการแข่งขัน หรือ physical validation และไม่เปลี่ยน 3D solids ต้องมี geometry ภายใน differential และ structural/thermal verification แยกก่อนกล่าวอ้างรถทั้งคันแบบละเอียด
