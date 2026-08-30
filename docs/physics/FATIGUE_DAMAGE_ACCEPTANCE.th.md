# การยอมรับ Fatigue Damage และ Life

ไฟล์ต้นฉบับภาษาอังกฤษ: `FATIGUE_DAMAGE_ACCEPTANCE.md`

## ผลลัพธ์และขอบเขตข้ออ้าง

Work 044 ผ่าน deterministic rainflow counting, Goodman mean-stress correction, synthetic Basquin S-N life, append-only Miner damage, first-crossing localization, uncertainty emission, replay และ unsupported-domain rejection

งานนี้ validate เฉพาะ arithmetic/event contract ไม่ใช่ sourced material life, crack-growth validation, multiaxial/non-proportional fatigue, strain-life/plastic hysteresis, environment/process evidence หรือ real component service-life claim

## Model

Synthetic record ประกาศ `Sa_ref=200 MPa`, `N_ref=1000`, Basquin exponent `m=5`, corrected-stress domain `80..300 MPa`, ultimate stress `500 MPa`, Goodman correction และ life-scatter factor `2`:

```text
Sa_corrected = Sa / (1 - Sm/Su)
N = N_ref (Sa_corrected/Sa_ref)^(-m)
D = sum(n_i/N_i)
failure crossing: first D >= 1
```

NASA reference อธิบาย rainflow ว่าใช้ลด reversal history เป็น cycle range/mean event, Palmgren-Miner damage เป็นผลรวม life fraction และ modified Goodman correction สำหรับ combined alternating/mean stress ค่า curve ของ Work 044 ยังเป็น synthetic และห้ามใช้ใน design fitness

## ผลการทดลอง

- Constant fully reversed `Sa=200 MPa`: rainflow นับตรง `1200` cycles, cumulative `D=1.2` และ localize failure แรกที่ cycle `1000` Damage ไม่ถูก clip เป็น `1`
- High→low blocks: `300` cycles ที่ `Sa=240 MPa` แล้ว `1000` ที่ `160 MPa`; final `D=1.074176`, crossing แรกที่ cycle `1073.632813`
- Low→high blocks: bin เดิมแต่สลับลำดับ; final `D=1.074176`, crossing แรกที่ cycle `1270.190329`
- Positive mean case `50..250 MPa`: `Sa=100 MPa`, `Sm=150 MPa`, Goodman-corrected `Sa=142.857143 MPa`, predicted life `5378.24` cycles และ `100` cycles ให้ `D=0.01859344`
- Negative control หกแบบ reject overload, below-domain stress, mean stress ที่ ultimate, missing curve, missing provenance และ non-finite history

Final Miner sum ที่เท่ากันเมื่อสลับ block เป็นคุณสมบัติของ model ไม่ใช่หลักฐานว่า real material ไม่มี sequence effect ส่วน event-cycle chronology ที่ต่างกันยัง observable

## Falsification review

หลักฐานสนับสนุนมี exact constant cycle count/damage, unclipped first crossing, deterministic identical replay, chronological block event, Goodman correction, uncertainty interval ทุก ledger entry และ exact domain rejection ไม่มี admitted result ขัด preferred arithmetic hypothesis

คำอธิบายทางเลือกและข้อจำกัดหลักคือ Miner linear accumulation ตัด load interaction, overload retardation, residual stress evolution และ crack growth ออก หลักฐานที่ขาดคือ sourced S-N scatter, surface/notch/process/temperature/environment record, multiaxial/strain-life validation, physical spectrum test และ fracture-mechanics growth มีความมั่นใจสูงเฉพาะ deterministic accounting

## การรันซ้ำ

```powershell
.\scripts\run_work044.ps1
py -3.14 -m unittest tests.test_fatigue_damage -v
```

Machine-readable evidence อยู่ที่ ignored `artifacts/work044/experiment_summary.json`
