# ผลงาน 044: การยอมรับ Fatigue Damage และ Life

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_044_fatigue-damage-life-acceptance-result.md`

สถานะ: เสร็จสมบูรณ์

## ผลลัพธ์

Synthetic fatigue accounting route ผ่าน Rainflow cycle count, constant/variable amplitude damage, Goodman correction, first crossing, uncertainty, exact replay และ invalid-domain control ทั้งหมด observable ไม่มี fatigue value ใดถูก admit เป็น real design data

## ไฟล์ที่เปลี่ยน

- `config/structural/fatigue_damage_acceptance_v1.json`
- `src/formula_ultimate/structural/fatigue.py` และ structural exports
- `scripts/structural/run_fatigue_damage_acceptance.py`
- `scripts/run_work044.ps1`
- `tests/test_fatigue_damage.py`
- `docs/physics/FATIGUE_DAMAGE_ACCEPTANCE.md` และ `.th.md`
- matching Work 044 plan/result pair

Ignored evidence อยู่ใต้ `artifacts/work044/`

## การตัดสินใจและผล

- Implement deterministic stack rainflow version และเก็บ endpoint half-cycle accounting
- Process independent block แยกกันเพื่อไม่ให้ concatenation สร้าง transition cycle ที่ไม่มีจริง
- ใช้ decimal damage accumulation และ serialize ทุก increment/cumulative value; damage คงเป็น `1.2` หลัง crossing ไม่ clip
- Constant history นับตรง `1200` cycles และ crossing ที่ `1000`
- High→low และ low→high จบที่ `D=1.074176` เท่ากัน แต่ first crossing ต่างที่ `1073.632813` และ `1270.190329` cycles
- Unsupported/malformed input หกแบบ fail closed

## การตรวจสอบ

```powershell
py -3.14 -m unittest tests.test_fatigue_damage -v
# exit 0; Ran 4 tests; OK

.\scripts\run_work044.ps1
# exit 0; status=passed; negative_controls=6

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 307 tests in 19.738s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

## ข้อจำกัดและงานต่อ

Miner/S-N arithmetic ไม่ใช่ crack growth หรือ physical service life Record ไม่มี sourced curve scatter, notch/surface/process/environment factor, plastic hysteresis, residual-stress evolution, multiaxiality และ load interaction Work 046 อาจใช้ typed crossing event หลัง Work 045 เท่านั้นและต้องเก็บ evidence limitation เหล่านี้ไว้
