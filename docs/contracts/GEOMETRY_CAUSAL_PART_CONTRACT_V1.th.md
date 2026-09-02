# Geometry-Causal Part Contract V1

ต้นฉบับภาษาอังกฤษ: `GEOMETRY_CAUSAL_PART_CONTRACT_V1.md`

## จุดประสงค์

`geometry_causal_part_v1` คือ declaration ขั้นต่ำแบบ fail-closed สำหรับสิ่งที่ repository นี้จะเรียกว่า “ชิ้นส่วนทางกายภาพ” โดยยกเลิกสมมติฐานแฝงว่ากล่องหนึ่งกล่องต่อหนึ่งฟังก์ชันเป็น component model ที่เพียงพอ Contract นี้ยังไม่ยืนยันว่า geometry ที่ประกาศสร้างได้จริง ผลิตได้ รับแรงได้ หรือผ่าน physical validation

Executable authority คือ `src/formula_ultimate/components/part_contract.py` และตัวอย่าง canonical ที่ผ่านคือ `config/components/geometry_causal_part_contract_v1.json`

## Declaration ที่บังคับ

ทุก top-level field เป็นข้อมูลบังคับและ unknown field จะถูกปฏิเสธ

| Field | หลักฐานที่บังคับ |
|---|---|
| `contract_version` | ค่า exact `geometry_causal_part_v1` |
| `part_id` | identity ตัวพิมพ์เล็กที่คงที่ |
| `function_tags` | functional claim ที่ไม่ว่างและไม่ซ้ำ |
| `feature_history` | feature ID ตามลำดับ, ชื่อ operator, parameter SI และการอ้าง parent ที่มาก่อน |
| `material` | `material_id`, SHA-256 ของ record แบบ exact และ evidence status |
| `local_frame` | origin และแกน `x/y/z` แบบ orthonormal right-handed |
| `datums` | witness ชนิด point, axis หรือ plane ที่ไม่ซ้ำ พร้อม frame ครบ |
| `interfaces` | interface มีชนิด ไม่ซ้ำ ผูกกับ datum และ geometry signature |
| `load_regions` | region ที่มี geometry signature ชนิด application, support, contact, thermal, electrical หรือ fluid |
| `load_path` | region ที่ประกาศต่างกันอย่างน้อยสองรายการตามลำดับการส่งผ่านที่ตั้งใจ |
| `manufacturing` | process และ evidence identity; defer feasibility ไป Work 079 |
| `tolerances` | general length/angular tolerance เป็นบวกในหน่วย SI |
| `minimum_feature_size_m` | ขนาด geometry ต่ำสุดที่ประกาศเป็นบวก |
| `parameter_provenance` | evidence record แบบหนึ่งต่อหนึ่งที่ exact สำหรับ feature parameter และ tolerance ทุกตัว |
| `claim_boundary` | admitted claim ที่ไม่ว่างและห้าม `physical_validation` โดยชัดแจ้ง |

## Vocabulary ของ interface

V1 รับเฉพาะ `fixed_mount`, `revolute`, `prismatic`, `spherical`, `bearing_seat`, `shaft_coupling`, `spline_key`, `bolted`, `welded`, `ground_contact`, `thermal` และ `electrical_fluid` แต่ละ interface ต้องประกาศ datum, SHA-256 geometry signature, mating role, `tolerance_m` เป็นบวก และ allowed DOF ไม่ซ้ำจาก `tx`, `ty`, `tz`, `rx`, `ry`, `rz` โดย `fixed_mount` ต้องไม่มี allowed DOF

Vocabulary นี้จำแนกเจตนาเท่านั้น Work 080 ต้องพิสูจน์ assembly constraint behavior, alignment, clearance, interference และ DOF ที่เกิดขึ้นจริง

## หน่วย ค่า และ provenance

Feature parameter รับเฉพาะ suffix `_m`, `_m2`, `_m3`, `_rad`, `_ratio` หรือ `_count` ค่าแต่ละตัวต้อง finite, count ต้องเป็น integer อย่างน้อยหนึ่ง และ parameter ที่มีคำว่า `thickness` ต้องเป็นบวก General tolerance ต้องเล็กกว่า minimum feature size และ interface tolerance แต่ละตัวต้องไม่เกิน minimum feature size

Numeric design parameter ที่ประกาศทุกตัวมี provenance record หนึ่งรายการ ประกอบด้วย source text, SHA-256 ตัวพิมพ์เล็กของ source identity และ confidence ในช่วง `[0, 1]` ทั้ง provenance target ที่ขาดและที่เกินจะ fail Traceability นี้ยังไม่พิสูจน์ว่า source เหมาะสม Work 079 จะเพิ่มการตรวจ source และ domain ของ engineering property

## กติกา frame และ identity

ตรวจ frame ด้วย absolute tolerance `1e-9`: ทุกแกนยาวหนึ่งหน่วย แกนตั้งฉากกัน และ `x cross y = z` Feature parent ต้องมีอยู่ก่อนใน history ส่วน identity ของ part, feature, datum, interface, load region, function tag, DOF และ claim ต้องไม่ซ้ำ ระบบไม่เติม default frame, material, interface หรือ load path

## Canonical replay

Mapping ที่ผ่านจะ serialize เป็น UTF-8 JSON โดยเรียง object key, ใช้ compact separator, ASCII escape และ `allow_nan=False` Identity ของ declaration คือ SHA-256 ของ byte เหล่านั้นแบบ exact ดังนั้นการสลับ object key รักษา identity แต่การเปลี่ยนลำดับ array เป็น causal change และทำให้ identity เปลี่ยน

รัน reference witness ด้วย:

```powershell
python scripts/components/validate_part_contract.py `
  --config config/components/geometry_causal_part_contract_v1.json `
  --output artifacts/work077/part_contract_evidence.json
```

## ขอบเขต fail-closed

Parser ปฏิเสธ unknown/missing field, suffix หน่วย parameter ที่ไม่รู้จัก, non-finite value, thickness/minimum feature/tolerance ที่ไม่เป็นบวก, tolerance มากเกิน, frame ผิดหรือ left-handed, interface/datum/region type ที่ไม่รองรับ, identity ซ้ำ, forward feature reference, provenance ไม่ครบ และ load path ที่ไม่มี known region ต่างกันอย่างน้อยสองรายการ

การผ่านยอมรับเฉพาะ `contract_complete` และ `deterministic_declaration` สำหรับตัวอย่างอ้างอิง ไม่ยอมรับ CAD validity, STEP identity, material adequacy, manufacturing feasibility, assembly behavior, structural capacity, fatigue/fracture life, thermal behavior หรือ physical validation
