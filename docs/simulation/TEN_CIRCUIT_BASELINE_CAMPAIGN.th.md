# Ten-Circuit Fixed-Topology Baseline Campaign

สถานะ: Level-0 analytical proxy baseline ของ Work 029

ไฟล์ต้นฉบับภาษาอังกฤษ: `TEN_CIRCUIT_BASELINE_CAMPAIGN.md`

## จุดประสงค์และขอบเขต

Work 029 รัน immutable fixed-topology reference family หนึ่งชุดผ่าน whole-race orchestrator แปด stage จาก Work 028 สำหรับ circuit profile และ seed ทุกชุด เพื่อสร้าง reproducible integration baseline และ fair opportunity control ก่อนเปรียบเทียบ free-topology candidate

campaign ใช้ official profile identity, lap length, race distance, width evidence, source metadata และ design-pressure metadata แต่ยังไม่มี surveyed local centreline/corridor geometry หรือ event-time weather โดย local path กับ weather เป็น analytical control ที่ประกาศชัด ดังนั้นทุก run มี evidence grade `profile-distance-analytical-proxy` และ `real_circuit_admitted = false`

## Protocol ที่ตรึง

`config/simulation/fixed_topology_baseline_protocol_v1.json` ตรึง:

- campaign: `work029-ten-circuit-fixed-topology-v1`
- architecture: `coupled-level0-reference-v4`
- family: `fixed-four-steady-drag-v1`
- fixed contact สี่จุดและ component library จาก Work 025-027
- mass `1000 kg`, width `1.8 m`, speed `10 m/s`
- reference area `1.5 m^2` และ analytical drag coefficient `0.5`
- primary energy `50,000,000 J`, drive efficiency `0.9` และ recovered capacity `5,000,000 J`
- maximum drive force `1000 N` และ strategy `steady-drag-balance-v1`
- synthetic dry-track control ที่ `300 K`, `101325 Pa`, wind/precipitation ศูนย์ และ proxy half corridor `50 m`
- timestep `1000 s`, timeout `40000 s` และสูงสุด `64` step ต่อ run
- design-evaluation budget `1`
- seed `(17, 29, 43)`
- calibration เจ็ด profile / holdout สาม profile ที่ตรึง

unknown protocol field และ implicit integer coercion ถูกปฏิเสธ Protocol, control, component opportunity, architecture, run แต่ละชุด และ campaign result ทั้งหมดมี identity SHA-256

## ฟิสิกส์ Reference

analytical aerodynamic map มี drag ไม่เป็นศูนย์และ side force/downforce เป็นศูนย์ ในทุก step strategy ที่ตรึง request drive force เท่ากับ aerodynamic drag ที่คำนวณปัจจุบัน ทำให้ contact force, aerodynamic drag, motion, drive-wheel work, drive efficiency loss, central energy state, component heat, health และ race progress ผ่าน coupled adapter จริง

ระบบนี้แข็งแรงกว่า frictionless zero-energy coast แต่ยังไม่ครบ: ไม่มี rolling resistance, real cornering, gradient, braking zone, traffic, weather ที่เปลี่ยน, measured aero, tyre degradation และ circuit-local geometry

## กฎ Fairness และ Holdout

- ทุก circuit/seed run ได้ architecture, vehicle/component opportunity, initial energy, strategy law, timestep, timeout และ maximum step budget เดียวกัน
- race ที่สั้นกว่าอาจใช้ step น้อยกว่า แต่ maximum opportunity เท่ากันและไม่มี run ได้ extension
- calibration/holdout ID ไม่ overlap, ครบ และถูก fingerprint ก่อน execute
- รายงานผล holdout ได้แต่เปลี่ยน family หรือ control ไม่ได้
- seed identity ยังอยู่ใน replay metadata แม้การปิด stochastic hazard ทำให้ performance metric เหมือนกัน
- เก็บ static published-width screening โดย `indeterminate` หมายถึง width evidence ยังไม่รู้ ไม่ใช่ผ่าน

## ผลที่ Validate แล้ว

run ทั้ง `30/30` (`10 profiles × 3 seeds`) finish พร้อม residual ผ่านทั้งหมดและไม่มี run เกิน `31/64` step แต่ละ seed ให้ controlled performance metric ราย circuit เหมือนกันพร้อม replay identity แยก

| Circuit | Partition | Distance (m) | Time (s) | Primary energy used (MJ) | Steps | Static width |
|---|---|---:|---:|---:|---:|---|
| Bahrain 2025 | holdout | 308238 | 30823.8 | 15.012090 | 31 | indeterminate |
| Hungaroring 2026 | calibration | 306630 | 30663.0 | 14.933776 | 31 | indeterminate |
| Mexico City 2025 | holdout | 305354 | 30535.4 | 14.871631 | 31 | indeterminate |
| Monaco 2026 | calibration | 260286 | 26028.6 | 12.676688 | 27 | screen_passed |
| Monza 2026 | calibration | 306720 | 30672.0 | 14.938159 | 31 | screen_passed |
| Sao Paulo 2025 | holdout | 305879 | 30587.9 | 14.897200 | 31 | screen_passed |
| Silverstone 2026 | calibration | 306198 | 30619.8 | 14.912736 | 31 | indeterminate |
| Singapore 2025 | calibration | 306143 | 30614.3 | 14.910058 | 31 | indeterminate |
| Spa 2026 | calibration | 308052 | 30805.2 | 15.003032 | 31 | indeterminate |
| Suzuka 2026 | calibration | 307471 | 30747.1 | 14.974735 | 31 | screen_passed |

หลักฐาน campaign ณ เวลาจบ Work 029:

- architecture fingerprint: `abf3148cfba2063f8fdba23951239b2b0a4a899c391503d3e46db69fd203618d`
- protocol fingerprint: `4c1c93a21c8ada5d8859eebbce1adb11f750787b2f522ba671f30be08ea6f2a6`
- controls fingerprint: `9c6a168a90a1e8d7cf33f72f3410e8d193cfd4edffddf7a136c84a1bed0371c9`
- result fingerprint: `44dc7f85fac097b8ecbb38c04ff14a595702e8e4a0b9134ba70403fc451bfa98`

หลังจากนั้น Work 030 เพิ่มความเข้มงวดของ fingerprint field coverage และ bump
evidence model ปัจจุบันเป็น `work029-baseline-campaign-v2` โดย numerical table
ข้างบนไม่เปลี่ยน ส่วน current result fingerprint ที่ครอบ field ครบคือ
`79a03587e6bbeb17101c89a59c7fe61053571f493a29fbe356322418726d2a9b` ค่า hash v1
ยังเป็น historical evidence ของ commit Work 029 ไม่ใช่โมเดลปัจจุบัน

## การพยายามหักล้าง

test ปฏิเสธ partition ที่ overlap/ไม่ครบ, hidden protocol field, ค่า float ใน integer budget, real-circuit admission บน proxy evidence, evidence grade ที่ไม่รองรับ และ component opportunity ที่ถูกเปลี่ยน Budget หนึ่ง step ที่ไม่พอให้ timeout ที่สังเกตได้แทนการขยายเงียบ การ permute ลำดับ catalog replay exact ภายใต้ reduced controlled campaign

## การตีความ

ผลนี้พิสูจน์ว่า central Level-0 software execute fixed-topology reference ที่ใช้ energy หนึ่งชุดบนระยะ profile ทั้งสิบอย่างสอดคล้องภายใต้ pinned opportunity ไม่ได้พิสูจน์ว่า reference ขับสนามจริงเหล่านั้นได้, เวลาเป็นไปได้จริง หรือถูก optimize แล้ว นี่คือ comparison-control artifact ไม่ใช่ discovery

Work 030 ยังต้องทำ deliberate integrated defect, numerical refinement, uncertainty/claim review และ cross-model promotion gate โดย free-topology candidate ยังถูกบล็อกจาก discovery หรือ real-race claim จนมี higher-fidelity independent evidence
