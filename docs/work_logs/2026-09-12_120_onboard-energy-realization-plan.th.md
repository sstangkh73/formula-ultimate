# แผน Work 120: การทำระบบพลังงานบนรถให้เกิดจริงอย่างละเอียด

แหล่งภาษาอังกฤษ: `2026-09-12_120_onboard-energy-realization-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

ปิด reference route ของ stored-electric/DC conversion แบบ synthetic ที่เปิดเผยหนึ่งเส้นทาง โดยตรึงกับหลักฐาน thermal จาก Work 115, material scope จาก Work 116 และ realized actuation port จาก Work 119 แทน active storage volume, enclosure, insulation, connector และ mount พร้อมหามวลครบชุดและ usable initial energy จาก geometry/property ที่ลงทะเบียน

ติดตาม stored-energy decrease, output ที่ส่ง, conversion/conductor loss และ temperature rise โดยไม่มี external replenishment บังคับ capacity, power-rate และ temperature applicability พร้อมเปิดเส้นทาง chemistry/field/conversion อื่นด้วย extension slot ที่ blocked ชัดเจน

## ตัวแปร control และไฟล์

- IV: active volume/allocation, initial state fraction, rate/duration ที่สั่ง ambient/initial temperature, การเชื่อม converter และ containment coverage
- DV: usable energy, delivered power/energy, stored-energy change, loss/heat, final temperature, mass ครบชุด และ limiting state
- Controls: โอกาสพลังงานเดียวกัน; storage ว่าง demand เกินขีด converter ถูกตัด ไม่มี containment, hidden replenishment และ unit/boundary ขัดกัน
- Success: energy residual ปิด, mass รวม hardware class ที่ลงทะเบียนทุกชนิด, limit เป็นเชิงเหตุ, physics ที่ไม่รองรับยัง blocked และ exact replay ผ่าน

ไฟล์ที่วางแผน: `src/formula_ultimate/subsystems/onboard_energy_realization.py`, `config/development/onboard_energy_realization_v1.json`, `scripts/development/run_onboard_energy_realization.py`, `tests/test_onboard_energy_realization.py`, contract `docs/contracts/ONBOARD_ENERGY_REALIZATION_V1*` สองภาษา, plan/result สองภาษาชุดนี้ และ `artifacts/work120/run_a|run_b` ที่ไม่ติดตามใน Git

## การตรวจสอบ

```powershell
python -m unittest tests.test_onboard_energy_realization tests.test_repository_contract -v
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_a
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_b --replay-reference artifacts/work120/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 115/116/119 และตรวจ staged/cached diff แบบระบุไฟล์ จะ commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Property ด้าน storage/conversion ทั้งหมดเป็น synthetic สิ่งที่ไม่ทำ: อ้าง chemistry safety, อนุญาตให้สร้าง/จ่ายพลังงาน, validated capacity/rate/life, fault propagation, ความเหนือกว่า/neutrality ของเทคโนโลยีเกิน controlled opportunity นี้, physical validation, push หรือแก้ประวัติ
