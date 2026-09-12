# ผล Work 132: Physical Subsystem Correlation

แหล่งภาษาอังกฤษ: `2026-09-12_132_physical-subsystem-correlation-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Stopped

Offline integrity pipeline ปฏิเสธ missing boundary power, undocumented replacement, calibration leakage, censored abort และ sensor disagreement Unit fixtures เป็นเพียง software tests งาน subsystem จริงหยุดด้วย blockers 7 รายการ: ขาด measured applicability ที่ valid จาก Work 131, subsystem safety/facility/operator references, frozen configuration, instrument manifest และ measured subsystem records ไม่มีการควบคุมอุปกรณ์และไม่อ้าง endurance/lifetime

Result SHA-256 คือ `0393b2cf2c3fe295496bbaa357ad928ad8f716b8cb580a48b46f447a68047797`; exact stopped-decision replay ผ่าน ไม่พบบั๊ก implementation

```powershell
python -m unittest tests.test_physical_subsystem_correlation -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/experiments/physical_subsystem_correlation.py scripts/development/run_physical_subsystem_correlation.py tests/test_physical_subsystem_correlation.py
# exit 0
python scripts/development/run_physical_subsystem_correlation.py --config config/development/physical_subsystem_correlation_v1.json --output-root artifacts/work132/run_a
# exit 0; stopped; 7 blockers
python scripts/development/run_physical_subsystem_correlation.py --config config/development/physical_subsystem_correlation_v1.json --output-root artifacts/work132/run_b --replay-reference artifacts/work132/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_physical_connection_correlation tests.test_physical_subsystem_correlation tests.test_repository_contract -v
# exit 0; ผ่าน 18 tests
```

การทำต่อจริงต้องเป็น authorized measured program ใหม่หลัง Work 131 ผ่าน
