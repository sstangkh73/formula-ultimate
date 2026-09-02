# Engineering Material and Manufacturing Contract V1

ต้นฉบับภาษาอังกฤษ: `ENGINEERING_MATERIAL_MANUFACTURING_CONTRACT_V1.md`

## จุดประสงค์และขอบเขตหลักฐาน

Work 079 แทน component force limit ที่ลอย ๆ ด้วย material property แบบ hash-addressed, evidence domain และ manufacturing constraint ที่วัดจาก geometry Executable authority คือ `src/formula_ultimate/components/engineering_contracts.py`; canonical binding คือ `config/materials/engineering_material_manufacturing_v1.json`; และ runner คือ `scripts/components/validate_engineering_contracts.py`

Canonical material/process record เป็น **synthetic verification fixture** ใช้ exercise equation และ fail-closed behavior และคืน `design_use_allowed=false` ไม่ใช่ coupon result, handbook allowable, supplier capability หรือ input ออกแบบรถ ในอนาคตต้องแทนด้วย sourced record โดยไม่ลด gate ใด

## Engineering material record

`engineering_material_v1` บังคับ identity, display name, evidence status `synthetic` หรือ `sourced`, property แบบ exact, fatigue evidence state, evidence record, source mapping หนึ่งรายการต่อ property, validation tolerance และ claim boundary

Property SI ที่บังคับคือ:

- `density_kg_per_m3`
- `youngs_modulus_pa`, `poisson_ratio` และ `shear_modulus_pa`
- `yield_strength_pa` และ `ultimate_strength_pa`
- `fracture_toughness_pa_sqrt_m`
- `thermal_conductivity_w_per_m_k`, `specific_heat_capacity_j_per_kg_k` และ `thermal_expansion_per_k`
- `allowable_temperature_min_k` และ `allowable_temperature_max_k`

Property ทุกตัวต้อง finite และ magnitude ที่ทางกายภาพบังคับให้เป็นบวกต้องเป็นบวก Poisson ratio ต้องอยู่ใน `(-1, 0.5)`, yield ต้องไม่เกิน ultimate strength และ temperature interval ต้องเพิ่ม ตรวจ elastic consistency ด้วย:

```text
G_expected = E / (2 * (1 + nu))
relative residual = abs(G_declared - G_expected) / G_expected
```

Residual ต้องไม่เกิน tolerance ที่ประกาศ และ tolerance นี้ถูก cap ที่ `0.05`

## กติกา source, domain และ fatigue

Evidence record แต่ละตัวมี source ID คงที่, citation, source SHA-256, evidence class, confidence ใน `[0, 1]` และ temperature/material/process domain `property_sources` ต้อง map property ที่บังคับทุกตัวไปยัง record ที่มีอยู่ Material ที่ระบุ `sourced` ใช้ synthetic evidence ไม่ได้

Fatigue ต้องระบุ `missing` โดยไม่มี model, curve หรือ source หรือ `available` เป็น `sn_curve` ที่มีหลักฐานและอย่างน้อยสองจุด Cycle ต้องเพิ่มแบบ strict และ alternating stress ต้องไม่เพิ่ม Missing fatigue evidence เป็น output ที่สังเกตได้และห้าม fatigue-life claim ระบบไม่เติม neutral curve

Record ต้องห้าม `maximum_force_without_geometry` และ `physical_validation` Unknown field เช่น `maximum_force_n` ต้อง fail เฉพาะ fully sourced record จึงประกาศ `design_use_allowed=true` ได้; synthetic fixture ของ Work 079 ต้องและได้ประกาศ `false`

## Manufacturing process record

`manufacturing_process_v1` บังคับ typed process, evidence status, dimensional limit, tool-access envelope, tolerance class, policy `reject` สำหรับ unsupported feature, source mapping แบบ exact และ claim boundary

Dimensional gate V1 คือ minimum wall thickness, hole diameter, ligament, web thickness, internal radius และ bend radius ทั้งหมดเป็น metre Tool evidence ประกาศ required clearance, maximum depth-to-diameter ratio และ allowed approach direction Tolerance class ประกาศ minimum achievable tolerance; requested value ที่เล็กกว่าหลักฐานนั้นแน่นเกินและ fail

Process ที่ระบุ `sourced` ใช้ synthetic limit evidence ไม่ได้ เฉพาะ sourced process จึงประกาศ `production_use_allowed=true` ได้ แม้ sourced envelope ผ่านก็ยังต้องห้าม `manufacturability_proof` เพราะ dimensional screening ไม่พิสูจน์ supplier, tooling, quality, inspection, cost หรือ production capability

## Geometry witness และ causal margin

`manufacturing_geometry_witness_v1` ผูก part ID หนึ่งตัวกับ exact geometry SHA-256 และให้ measurement-evidence status/method/report SHA-256 พร้อม array ของ wall, hole, ligament, web, internal radius, bend radius, tool-access check, unsupported feature และ requested tolerance Measurement array ว่างต้อง fail แทนการเติม default Fixture ของ Work 079 ระบุ array เหล่านี้เป็น `synthetic` เพราะยังไม่ได้ดึงจาก STEP อย่างอิสระ Design use ต้องมีหลักฐาน `independently_measured` เพิ่ม และ route นั้นเป็นขอบเขต Work 081

สำหรับ dimensional family ทุกตัว:

```text
margin = minimum(measured geometry values) - declared process minimum
```

Margin ติดลบ fail ด้วย causal code คงที่: `wall_too_thin`, `hole_too_small`, `ligament_too_small`, `web_too_thin`, `internal_radius_too_small` หรือ `bend_radius_too_small` Tool direction, clearance, depth ratio, tolerance และ unsupported feature fail ด้วย code แยก ระบบไม่ clip มิติและไม่ repair geometry

## Hash binding และ replay

Material, process, assignment, witness report และ final result ใช้ identity SHA-256 จาก canonical sorted compact JSON Assignment ต้องตรง exact กับ part ID, geometry hash, material ID/hash และ process ID/hash Identity ที่ stale ต้อง fail ด้วย `assignment_identity_mismatch`

รันและ replay ด้วย:

```powershell
python scripts/components/validate_engineering_contracts.py `
  --config config/materials/engineering_material_manufacturing_v1.json `
  --output artifacts/work079/run_a/evidence.json
```

ทำซ้ำไปยัง output อื่นแล้วเทียบ file SHA-256 แบบ exact Canonical fixture ยังคง synthetic แม้ replay exact

## ข้อจำกัดและหลักฐานถัดไป

Internal equation consistency ไม่ใช่ real material validation V1 ไม่ model anisotropy, plastic hardening law, strain rate, environment/corrosion, heat-treatment/weld state, property scatter/statistical allowable, multiaxial fatigue, crack growth, creep, wear, surface finish, residual stress หรือ process simulation Work 082 ต้องใช้ sourced admitted record กับ geometry-derived mesh/load case ก่อน structural claim และยังต้องมี higher-fidelity comparison กับ real evidence
