# Functional Powertrain Dynamics v1

ไฟล์ต้นฉบับภาษาอังกฤษ: `FUNCTIONAL_POWERTRAIN_DYNAMICS_V1.md`

## ผลลัพธ์และขอบเขต claim

Work 067 สร้าง transient component-law specimen รุ่นแรกหลังเส้นทาง Work 066 `energy_storage -> energy_converter -> power_transmission -> ground_propulsion` Model สร้าง torque ได้เมื่อถอน declared onboard energy เท่านั้น Electrical, conversion, viscous, shaft-damping, connection และ transmission losses กลายเป็น explicit heat Compliant connection สามารถ fail แบบ irreversible และหลังจากนั้น transmitted/output drive torque เป็นศูนย์

ผลนี้ validate equations, state transitions, accounting, deterministic replay และ deliberate failures สำหรับ synthetic reference แต่ไม่ได้เลือก motor, engine, energy store, transmission หรือ vehicle topology ที่ควรใช้ และไม่ใช่ measured หรือ physically validated hardware

## Dynamic model

Transmission ratio convention คือ

```text
n = omega_input / omega_output
```

Shaft twist และ torque คือ

```text
delta = theta_converter - n theta_output
T_shaft = k delta + c (omega_converter - n omega_output).
```

ก่อน failure rotational states สองฝั่งทำตาม implemented forward-only lumped equations

```text
J_converter domega_converter/dt = T_converter - T_shaft - b_converter omega_converter
J_output domega_output/dt = eta_shaft eta_transmission n T_shaft
                                  - T_load - b_output omega_output.
```

`T_converter` ถูกจำกัดด้วย throttle, interpolated torque-speed curve, converter output-power limit, converter input-power limit, connected storage-power limit, conversion efficiency และ stored energy ที่เหลือ External load เป็น unilateral/resistive: ลด forward rotation ได้แต่ inject undeclared reverse work ไม่ได้ Reverse rotation และ regeneration อยู่นอก v1 และจะ fail validation แทนการอนุมาน

Energy residual แสดงออกเป็น

```text
R = E_initial - (E_storage + E_kinetic + E_elastic + E_thermal
                 + W_useful + Q_rejected).
```

Residual ไม่ถูกใช้แก้ state Reference admission ceiling คือ `|R| / E_scale <= 1e-3`

## Frozen synthetic reference

Fixed fixture ใช้ storage capacity `50 MJ`, source power `120 kW`, electrical connection efficiency `0.99`, converter torque envelope `450 N m` ถึง `200 rad/s` แล้วลดเป็นศูนย์ที่ `400 rad/s`, converter inertia `0.2 kg m^2`, shaft stiffness `2000 N m/rad`, damping `35 N m s/rad`, shaft efficiency `0.99`, shaft torque limit `450 N m`, twist limit `0.3 rad`, transmission ratio `3.0`, transmission efficiency `0.95`, output inertia `2.5 kg m^2` และ synthetic lumped thermal parameters

ตัวเลขเหล่านี้ตรงหรือ locally restrictive กว่า Work 066 architecture fixture แต่ไม่ใช่ค่าที่วัดหรือ certified allowables

## Analytical power partition

ที่ throttle `0.5` และ converter speed `200 rad/s` independent algebraic check ให้:

- converter torque: `225 N m`
- storage power: `47,846.88995215311 W`
- converter mechanical power: `45,000 W`
- output speed: `66.66666666666667 rad/s`
- output torque: `634.8375 N m`
- electrical connection heat: `478.4688995215329 W`
- converter heat: `2,368.42105263158 W`
- shaft-efficiency heat: `450 W`
- transmission heat: `2,227.5 W`
- power residual: `0 W`

ดังนั้น output power ที่ต่ำลงอธิบายได้ด้วย declared losses ไม่ใช่พลังงานหายไป

## Transient experiment

Reference command ใช้ throttle `0.5`, output-load torque `200 N m`, duration `2 s` และ step `0.0005 s` รวม `4,000` steps และจบโดยไม่มี limit failure

| Metric | Result | Limit/status |
| --- | ---: | --- |
| final converter speed | `322.205241054604 rad/s` | `< 400 rad/s` |
| final output speed | `107.403266469072 rad/s` | `< 150 rad/s` |
| source energy used | `65,729.4197853313 J` | finite/decreasing store |
| useful external work | `30,286.8669266214 J` | positive |
| maximum connection demand | `182.066064231239 N m` | `< 450 N m` |
| maximum shaft twist | `0.0812613938084503 rad` | `< 0.3 rad` |
| maximum output drive torque | `513.699400228442 N m` | `< 1,200 N m` |
| final converter temperature | `300.317298442075 K` | `< 450 K` |
| final transmission temperature | `300.2848072388 K` | `< 450 K` |
| maximum absolute energy residual | `0.500342398881912 J` | observable |
| maximum relative energy residual | `1.00068479776382e-8` | `< 1e-3` |

Reference result SHA-256 คือ `3248fe721f8fdc39aca182cb81ced64ee7163fdabfa6874778636bd3df2b3543` การรันซ้ำให้ค่าเดียวกัน การลด step เป็น `0.00025 s` เปลี่ยน selected terminal metrics สูงสุด `1.79900311164274e-5` ต่ำกว่า frozen ceiling `0.02`

## Falsification controls

- Zero-energy control: source energy used และ useful work คงเป็น `0 J` พอดี; converter/output speeds เป็นศูนย์
- Shaft-overload control: ลด torque limit เป็น `50 N m` ทำให้ demand `56.331665505 N m`, terminal `shaft_connection_failure` ที่ `0.002 s` และ transmitted torque หลัง failure เป็น `0 N m`
- Thermal control: จงใจลด converter heat capacity และ maximum temperature ทำให้เกิด `converter_overtemperature` ที่ `0.016 s`
- Invalid declarations: unordered curves, efficiency มากกว่าหนึ่ง, undeclared power/torque creation, maximum temperature ต่ำกว่า ambient, numerical tolerance สูงเกิน, non-finite runtime state และ duration/step ที่ incompatible จะ fail closed

Frozen experiment checks ทั้ง 8 และ focused unit tests ทั้ง 8 ผ่าน Full repository regression ผ่าน 396 tests

## หลักฐานที่ยังขาดและการ coupling ถัดไป

Model ยังเป็น two-inertia, forward-only, lumped และ fixed-step ยังไม่มี electrochemistry, combustion, electromagnetic fields, detailed gear/shaft geometry, bearing/contact friction, backlash, lubrication, differential action, regeneration, tyre slip, suspension และ vehicle translation Connection torque ยังไม่ได้ derive จาก shaft stress, yield, fatigue หรือ fracture geometry Temperature เป็น lumped states ไม่ใช่ conjugate heat-transfer results

งานถัดไปควรเชื่อม output branches สองฝั่งเข้ากับ ground-force/slip และ wheel inertia โดยรักษา energy ledger เดิม จากนั้น compliant connection ต้องรับ geometry/material evidence จาก verified torsion/failure modules เพื่อให้ shaft ที่ fail ทางกายภาพทำให้เกิด whole-vehicle subsystem failure หรือ `DNF`
