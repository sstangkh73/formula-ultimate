# Structural Failure Coupling และ DNF

ไฟล์ต้นฉบับภาษาอังกฤษ: `STRUCTURAL_FAILURE_COUPLING_DNF.md`

## ขอบเขตการอ้างและผลลัพธ์

Work 046 validate deterministic structural connection-state/failure-coupling policy ภายใน narrow numerical domain ที่ Work 051 admit รองรับ typed transition `intact -> degraded -> failed`, localized failure event, post-failure wrench เป็นศูนย์, redundant redistribution, failure-energy accounting, critical-path `DNF`, race-event arbitration และ exact replay

ไม่ได้ validate real fracture dynamics, crack propagation, fatigue crack growth, contact separation, stress wave, impact, crash energy, occupant safety หรือ arbitrary joint

## Evidence identity ที่ admit

ทุก evaluation ต้องตรงทั้งหมดดังนี้:

- remediation protocol `gate_a_remediation_v1` พร้อม decision `narrowly_bounded`
- element route `C3D10_precritical_v1`
- support topology SHA-256 `7f4444a78af66157f04441b38e4d4bc3225a892b29f90ebf9840279694fb6258`
- boundary model `bonded_cylindrical_surface_zero_displacement_v1`
- yield protocol `yield_plasticity_acceptance_v1`
- fracture protocol `fracture_initiation_acceptance_v1`
- fatigue protocol `fatigue_damage_acceptance_v1`

Identity ใดไม่ตรงจะคืน `invalid` โดยไม่มี candidate connection state

## State และ load-path policy

Bounded fixture ของ Work 046 มี load-path group ที่ประกาศหนึ่งกลุ่ม Connection ที่ intact/degraded รับ applied six-component wrench ตามสัดส่วน positive share weight ที่ประกาศ Yield evidence เปลี่ยน `intact -> degraded` Fracture หรือ fatigue evidence เปลี่ยน connection เป็น `failed` และบังคับ transmitted wrench เป็นศูนย์ exact

หลัง failure connection ที่รอดรับ share ใหม่แบบ deterministic หากเหลือ survivor อย่างน้อยหนึ่งตัว จะ audit force/moment closure หากไม่เหลือ survivor ใน required path network outcome เป็น `DNF`; applied-load closure จะถือว่า unavailable แทนการสร้างผลสมดุลปลอม

## Failure-energy policy

สำหรับ connection ทุกตัวที่ fail ณ localized event:

```text
U_stored = U_dissipated + U_released + residual
U_dissipated = fraction * U_stored
U_released = (1 - fraction) * U_stored
```

Fixture ใช้ stored energy `12 J` และ dissipated fraction `0.7` ได้ dissipated `8.399999999999999 J`, released `3.6000000000000005 J` และ observable floating-point residual `8.881784197001252e-16 J` Residual ผ่าน frozen tolerance และไม่ถูกเขียนทับเป็นศูนย์

Ledger นี้ไม่ได้ model ว่า released energy ไหลไปที่ใด มีหน้าที่ป้องกัน energy erasure ที่ coupling boundary เท่านั้น

## การทดลองและผลลัพธ์

Applied wrench คือ:

```text
force  = (1000, 50, -20) N
moment = (10, 5, -3) N*m
```

`joint_a` yield ที่ `0.2 s` และ fracture ที่ `0.375 s` การรัน timestep `0.5`, `0.25` และ `0.125 s` localize fracture ที่ `0.375 s` exact ทุกกรณี Maximum relative event-time change เป็น `0` ต่ำกว่า `1e-6`

ใน redundant fixture หลัง failure `joint_a` ส่ง `(0,0,0,0,0,0)` และ `joint_b` รับ applied wrench ทั้งหมด Maximum raw wrench/energy residual magnitude เท่ากับ `8.881784197001252e-16` Outcome ยังคง `running`

ใน critical fixture `joint_a` เป็น path เดียว Failure ทำให้ wrench เป็นศูนย์ exact และได้ deterministic `DNF` ทุก timestep

Same-input replay ตรง exact Negative control ห้ากรณี reject out-of-domain Gate A identity, unknown connection identity, upstream protocol mismatch, event ที่เกิดก่อน current state และ invalid energy partition

## Race arbitration

`structural_failure` เป็น typed central event หลัง `reliability_failure` และก่อน `damage_failure` Exact-time finish/structural tie เก็บ candidate ทั้งคู่และ priority เดิมให้ `finished` ชนะ Structural event ที่เกิดก่อน finish จะชนะและ map shared race state ไป `failed`/structural `DNF` semantics

นี่คือ deterministic Level-0 policy ไม่ใช่ sporting/safety regulation

## การประเมินเพื่อหักล้าง

หลักฐานสนับสนุนคือ exact event-time refinement, failed-wrench zero exact, redundant force/moment closure, retained energy residual, critical `DNF`, same-input replay และ fail-closed control

หลักฐานขัดแย้งคือ redistribution เป็น instantaneous และ Gate A identity มีขอบเขตแคบ Joint จริงอาจ redistribute ผ่าน stress wave, slip, contact, plasticity หรือ progressive fracture หลักฐานที่ยังขาดคือ physical joint test, calibrated material record, contact/preload/friction, transient dynamics, post-critical behavior, impact และ crash response

ความมั่นใจสูงสำหรับ policy mechanics ที่ implement และต่ำสำหรับ real failure dynamics

## การทำซ้ำ

```powershell
.\scripts\run_work046.ps1
py -3.14 -m unittest tests.test_structural_failure_coupling tests.test_coupling_contracts tests.test_whole_race -q
py -3.14 -m unittest discover -s tests -q
```

Machine-readable evidence อยู่ใต้ `artifacts/work046/` และ Git จงใจ ignore ต้องทำ clean-tree replay หลัง commit
