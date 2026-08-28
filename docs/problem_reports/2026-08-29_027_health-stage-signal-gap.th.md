# รายงานปัญหา: health stage merge energy และ motion ไม่ได้

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_027_health-stage-signal-gap.md`

## ปัญหา

architecture v2 ไม่ route `energy.residuals` หรือ `state.motion_candidate` ไป `health_event_solver`

## ผลกระทบ

health stage ไม่สามารถจัดสรร propulsion/recovery loss เป็น heat, ตรวจ depletion evidence หรือตัด motion ให้ตรง earliest event time เดียวกัน

## การแก้ไข

เก็บ v2 เดิมและเพิ่ม `coupled_level0_architecture_v3.json` โดย version 3 route สองสัญญาณนี้เข้า health และ pin energy/health adapter เป็น model version ของ Work 027

## ข้อจำกัด

การแก้ versioned dependency เพียงอย่างเดียวไม่ได้พิสูจน์ physical fidelity
