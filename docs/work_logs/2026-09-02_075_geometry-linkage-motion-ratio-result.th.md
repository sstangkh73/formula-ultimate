# ผล Work 075: Motion Ratio ของ Linkage ที่คำนวณจาก Geometry

สถานะ: เสร็จสมบูรณ์ (Completed)

แปลจากไฟล์ภาษาอังกฤษ: `2026-09-02_075_geometry-linkage-motion-ratio-result.md`

## ผลลัพธ์และไฟล์

สร้างการคำนวณ motion ratio จาก projected lever 3D และ virtual-work transform ของ stiffness, damping, travel ช่วงล่าง Work 073 เพิ่ม config, simulation module/exports, runner, focused tests 8 ข้อ, เอกสารวิจัยสองภาษา และผลนี้ หลักฐาน deterministic ถูก ignore ใต้ `artifacts/work075/`

## หลักฐาน

Powered contacts ได้ ratio `0.7999999999999999`; rear ได้ `1.0` Coupled run ที่เลือกวิ่งจบด้วย heave สูงสุด `0.0008656698982980348 m`, travel `0.019278824606844512 m`, โหลดต่ำสุด `266.8789268655951 N`, energy residual `5.0778645277023315e-9` Unit ratio รักษา Work 073 พอดี Mutation เปลี่ยน identity และ normalization/mirror/permutation/degeneracy controls ผ่าน

Application/result/canonical evidence/file hashes คือ `51b6255347e4a6a59428ee309f4f78c8e981baa437386bdcf3505df9d8403487`, `7fd4af71e95dc49be5330762efe284a20a0ac86bc73b19df6a17c41d0e0b552a`, `69d4ad48f82026fdca4134a0c00519f9dc4df837cb43c2ad0608b7eafe16c939`, `37864D0AE558AFBEB4E2E90B63DE1A48D84C17D4C6B8EC6EB106414E02A2DE64`

## บันทึกการตรวจสอบ

```text
python -m unittest tests.test_linkage_motion_ratio -v
Exit: 0
Ran 8 tests in 9.323s — OK

python scripts/experiments/run_linkage_motion_ratio.py --config config/vehicle/geometry_linkage_motion_ratio_v1.json --vehicle-root config/vehicle --output artifacts/work075/experiment_evidence.json
Exit: 0; status=passed

คำสั่งเดียวกันแต่ใช้ --output artifacts/work075/replay/experiment_evidence.json
Exit: 0; byte-identical SHA-256 37864D0AE558AFBEB4E2E90B63DE1A48D84C17D4C6B8EC6EB106414E02A2DE64

python -m unittest discover -s tests -q
Exit: 0
Ran 471 tests in 206.598s — OK
```

Full regression, repository contract, compilation, commit และ post-commit replay จะทำก่อน handoff

## ข้อจำกัดและงานถัดไป

Geometry เป็นค่ากำหนดสังเคราะห์และ small-angle ไม่ได้ดึงจาก CAD Work 076 จะรวม transform ที่เลือกกับการเคลื่อนที่ closed-loop ต่อเนื่อง แต่ไม่สามารถยกระดับจุดเหล่านี้เป็น physical validation
