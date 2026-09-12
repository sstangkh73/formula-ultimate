# Material Failure Scope V1

ต้นฉบับภาษาอังกฤษ: `MATERIAL_FAILURE_SCOPE_V1.md`

Status: พัฒนาโดย Work 116 เป็น applicability และ reference-law gate

## ขอบเขตหลักฐาน

Contract นี้ตรึงหลักฐาน stress จาก Work 111, dynamic history จาก Work 114 และ temperature จาก Work 115 ทุก material record ประกาศ property units, source, evidence class, temperature/rate bounds, process, uncertainty และ allowed uses Synthetic หรือ analytic records ห้าม relabel เป็น measured survival evidence กรณี temperature/rate/process นอกช่วง, units หาย และ mixture ไม่ลงทะเบียนล้มเหลวแบบปิด

First-yield ใช้ lower uncertainty-adjusted yield stress Pinned-column buckling ใช้ `pi^2 E I / (K L)^2`; bounded imperfection fixture ลด capacity ด้วย `1 + imperfection/radius_of_gyration` ทั้งหมดเป็น mathematical verification fixtures ไม่ใช่ universal constitutive หรือ collapse laws

Candidate aluminium record เป็น synthetic จึงอนุญาตเฉพาะ diagnostic margins Fatigue, fracture และ wear คงสถานะ `unresolved_missing_tested_data` การขาด measured process-qualified properties, geometry-applicable member mapping, manufacturing variability และ physical correlation บล็อก physical-survival claims แม้ diagnostic margin เป็นบวก

Exact replay ต้องได้ result SHA-256 เดิม Contract นี้ไม่ยืนยัน fatigue life, fracture resistance, wear, manufacturing qualification, safety certification หรือ complete physical survival
