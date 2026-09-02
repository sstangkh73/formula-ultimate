# ผล Work 074: ตัวควบคุม Corridor แบบ Closed Loop

สถานะ: เสร็จสมบูรณ์ (Completed)

แปลจากไฟล์ภาษาอังกฤษ: `2026-09-02_074_closed-loop-corridor-controller-result.md`

## ผลลัพธ์และไฟล์

สร้าง centreline projection แบบ deterministic และ bounded feedback steering controller รอบ physical plant Work 073 ที่ไม่เปลี่ยน เพิ่ม fixture วงกลมซ้าย/ขวาและทางตรง, config, simulation module/exports, runner, tests, เอกสารวิจัยสองภาษา และผลนี้ รวมทั้งลงทะเบียนแผนสองภาษา Work 075/076 ก่อน implement หลักฐานถูก ignore ใต้ `artifacts/work074/`

## การตัดสินใจและหลักฐาน

Controller เก็บ feed-forward, feedback, raw/applied steer, saturation, signed tracking error, desired heading, progress, widths และ downstream physical evidence ต่อ sampled step Departure แสดงชัด Feedback ที่ถูกต้องลด final error จาก zero-feedback `0.3772375000371769 m` เหลือ `0.02307508195600006 m`; wrong-sign แย่ลงเป็น `0.46591408662822736 m` การ saturation `348/500` steps ถูกเก็บเป็นข้อจำกัด โหลดต่ำสุด `290.149480377666 N`; travel สูงสุด `0.011457919570257338 m`

Work 073 hash คงที่ `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973` Work 074 result/canonical evidence/file hashes คือ `a400e8a9c1c0768d11647aa6c2fde3855a5d12898b548edef0b2fd6911244374`, `9572a793e45713ee9768d3bca7ead9460ce3d1fe1824d6cee273b89e7737efea`, `B21A66201270C99CB0177CA6A4BF82755DDF734C6F1EACFF46ACB7A78C84FE5B`

## บันทึกการตรวจสอบ

```text
python -m unittest tests.test_closed_loop_corridor_controller -q
Exit: 0
Ran 9 tests — OK

python scripts/experiments/run_closed_loop_corridor_controller.py --config config/vehicle/closed_loop_corridor_controller_v1.json --vehicle-root config/vehicle --output artifacts/work074/experiment_evidence.json
Exit: 0; status=passed

คำสั่งเดียวกันแต่ใช้ --output artifacts/work074/replay/experiment_evidence.json
Exit: 0; byte-identical SHA-256 B21A66201270C99CB0177CA6A4BF82755DDF734C6F1EACFF46ACB7A78C84FE5B

python -m unittest discover -s tests -q
Exit: 0
Ran 463 tests in 197.111s — OK
```

Full regression, repository contract, compilation, scoped commit และ post-commit replay จะบันทึกใน final handoff หลังรัน

## ข้อจำกัดและงานถัดไป

Controller ระยะสั้นนี้ saturation มากและใช้ geometry สังเคราะห์แบบ sampled ไม่มี longitudinal control หรือหลักฐานสนามจริง Work 075 ถัดไปเพิ่ม motion ratio ของ linkage ที่ชัดเจน Work 076 ต้อง retune และหักล้าง integration หนึ่งรอบต่อเนื่อง ไม่ extrapolate ผลนี้
