# การยอมรับ Fracture Initiation

ไฟล์ต้นฉบับภาษาอังกฤษ: `FRACTURE_INITIATION_ACCEPTANCE.md`

## ผลลัพธ์และขอบเขตข้ออ้าง

Work 043 ผ่าน narrow independently verified LEFM initiation evaluator ซึ่งเก็บ explicit crack identity, toughness provenance, thickness/material-state domain check, deterministic first-crossing event และ invalid case แบบ fail closed ไม่อ้าง CalculiX crack-tip field เพราะ route ปัจจุบันยังไม่มี independently validated contour-integral parser

นี่คือ ideal center-crack initiation arithmetic เท่านั้น ไม่ใช่ real toughness, crack propagation/path, fracture-energy dissipation, element deletion, fatigue crack growth, component strength หรือ crashworthiness

## Model และ Domain

สำหรับ infinite plate ที่มี center crack ความยาวรวม `2a` ภายใต้ uniform remote tension

```text
K_I = sigma sqrt(pi a)
sigma_initiation = K_IC / sqrt(pi a)
```

Synthetic record ใช้ `K_IC=15 MPa sqrt(m)`, `sigma_y=250 MPa`, `E=70 GPa`, ความกว้าง `0.2 m` และความหนา `0.012 m` การ admit ยังบังคับ full crack/width `<=0.1`, `B>=2.5(K_IC/sigma_y)^2`, plane-strain plastic-zone ratio `r_p/a<=0.1` และ initiation ต้องเกิดก่อน yield Toughness record ถูกห้ามใช้ใน design fitness อย่างชัดเจน

สูตรอิง NASA fracture-mechanics reference สำหรับ ideal infinite plate ส่วน thickness rule เป็น screening criterion ไม่ได้ทำให้ synthetic record กลายเป็น measured `K_IC` ที่ valid

## ผลการทดลอง

| Half-crack `a` (m) | Initiation stress (MPa) | Initiation force (N) | `r_p/a` | Localized load error |
|---:|---:|---:|---:|---:|
| 0.003 | 154.5097 | 370,823.23 | 0.06366 | 0 |
| 0.005 | 119.6827 | 287,238.44 | 0.03820 | 0 |
| 0.008 | 94.6175 | 227,081.93 | 0.02387 | 0 |

ทุก case ใช้ load factor `0.8`, `1.0`, `1.2` ของ analytical initiation force First crossing ที่ localize ตรง exact สำหรับ linear evaluator นี้ Representation level `8`, `16`, `32` segments ต่อ half crack รักษา exact tagged tip coordinates ดังนั้น last-two `K_I` change เป็นศูนย์ Reaction และ gross elastic work-ledger residual เป็นศูนย์

Negative control หกแบบถูก reject ด้วยเหตุผลที่ตั้งใจ: insufficient thickness, excessive finite-width ratio, missing flaw, missing toughness, missing provenance และ material yield เกิดก่อน LEFM initiation

## Falsification review

หลักฐานสนับสนุนคือ exact closed-form reproduction สำหรับ crack สามขนาด, deterministic event identity, representation-invariant crack tip, explicit material/domain gate และ negative-control rejection ครบ ไม่มี admitted evidence ที่ขัด preferred evaluator hypothesis

คำอธิบายทางเลือกหลักคือข้อจำกัดสำคัญด้วย: `Y=1` ตัด finite-geometry complexity ออก และ work ledger เป็น gross linear-elastic accounting control ไม่ใช่ fracture-energy evidence หลักฐานที่ขาดคือ finite-body geometry factor, crack-tip FEA/J-integral agreement, measured toughness uncertainty, physical coupon, propagation, path และ dissipated fracture energy มีความมั่นใจสูงด้าน arithmetic/rejection behavior และต่ำเมื่อนอก ideal initiation

## การรันซ้ำ

```powershell
.\scripts\run_work043.ps1
py -3.14 -m unittest tests.test_fracture_initiation -v
```

Machine-readable evidence อยู่ที่ ignored `artifacts/work043/experiment_summary.json`
