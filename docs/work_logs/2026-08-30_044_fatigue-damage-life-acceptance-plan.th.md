# แผนงาน 044: การยอมรับ Fatigue Damage และ Life

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_044_fatigue-damage-life-acceptance-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

แปลง explicit stress history เป็น deterministic counted cycle, mean-stress-corrected S-N life, append-only Miner damage ledger และ fatigue-failure crossing แรกที่ observable โดยไม่ clip, reset หรือ silently extrapolate damage

## ขอบเขตและข้ออ้าง

- ใช้ immutable synthetic Basquin S-N record พร้อม explicit alternating-stress domain, ultimate strength, Goodman mean-stress correction และ life-scatter factor
- Implement deterministic rainflow counting สำหรับ declared reversal history และ exact constant/variable-amplitude fixture
- เก็บทุก damage contribution และ localize crossing แรก `D>=1` รวม fractional cycle position เมื่อจำเป็น
- Reject below-domain, above-domain, invalid mean-stress, missing curve/provenance และ non-finite history แทนการกำหนด damage เป็นศูนย์หรือ extrapolate

งานนี้ validate เฉพาะ deterministic Miner/S-N accounting ไม่ใช่ crack-growth validation, multiaxial/non-proportional fatigue, spectrum/environment validation, real component service life หรือ physical material evidence

## การออกแบบการทดลอง

- ตัวแปรอิสระ: constant/variable amplitude history, mean stress, cycle count, block sequence และ curve declaration
- ตัวแปรตาม: rainflow range/mean/count, corrected amplitude, life ต่อ bin, incremental/cumulative damage, predicted crossing cycle, event identity และ uncertainty interval
- ตัวแปรควบคุม: turning-point convention, rainflow algorithm version, Goodman rule, temperature/process declaration, exact floating-point order และไม่มี damage clipping
- สมมติฐานที่ต้องการพิสูจน์: exact cycle fixture และ constant-amplitude damage ผ่าน `<=1%`, input เดิม replay exact, Miner arithmetic exact และ emit failure ที่ crossing แรก
- การพยายามหักล้าง: deliberate overload, under-domain history, invalid mean stress, malformed curve, permutation/replay และ sequence pair ที่ final Miner damage เท่ากันแต่ event position ต่างกัน

## Implementation และไฟล์ที่วางแผน

- `config/structural/fatigue_damage_acceptance_v1.json`
- immutable fatigue record, rainflow counter, Goodman correction, life evaluator, damage ledger, uncertainty และ event contract
- Work 044 runner/launcher และ ignored evidence ใต้ `artifacts/work044/`
- focused exact-cycle, arithmetic, replay, negative-domain และ event test
- bilingual report และ matching result records

## Validation และเกณฑ์สำเร็จ

- exact declared cycle-count fixture และ constant-amplitude damage error `<=1%`
- exact replay identity และ exact cumulative arithmeticสำหรับ record/order เดิม
- emit first crossing ที่ `D>=1` โดยไม่ clip/reset; unsupported curve-domain request fail closed
- รายงาน uncertainty ชัดเจนและ synthetic provenance ยังห้ามใช้ใน design fitness
- focused/full test, compile/static check, staged-diff check, explicit commit และ clean-tree replay ผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Rainflow endpoint half cycle และ block boundary ต้อง explicit; จะไม่ concatenate block แบบสร้าง transition cycle ที่ไม่มีจริง Miner sequence independence เป็นข้อจำกัดของ model แต่ยังเก็บ first-crossing chronology ไม่มี strain-life, plastic hysteresis, crack growth, multiaxial critical plane, physical coupon, vehicle fitness, push หรือ publication
