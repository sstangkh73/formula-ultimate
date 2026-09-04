# Semantic Geometry Witness V3

ไฟล์ต้นฉบับภาษาอังกฤษ: `SEMANTIC_GEOMETRY_WITNESS_V3.md`

## ขอบเขต

V3 import STEP 10 ไฟล์ exact ของ Work 092 อย่างอิสระด้วย FreeCAD/OCCT และสร้าง semantic evidence ที่ไม่ขึ้นกับลำดับ การผ่านพิสูจน์การ inspect frozen corpus นี้ ไม่ได้พิสูจน์ structural validity, global minimum thickness, assembly clearance, manufacturability, safety หรือ physical validity

## หลักฐาน geometry

record แต่ละตัวมี body/solid/shell count, validity, volume, area, mass จาก density ที่ประกาศ, centre of mass, full inertia, deterministic principal axes, degeneracy, axis-aligned และ principal-oriented bounds, face signature, curvature sample/spectrum, material-span thickness sample, section evolution, datum ที่ประกาศ, semantic region, path evidence, clearance/interference ภายใน candidate และ static swept envelope

ค่า thickness เป็น exact B-rep line-intersection span ที่ frozen grid และ probe ผ่าน centre ของแต่ละ solid จึงเป็น sampled value ไม่ใช่ guaranteed wall minimum Section area คือ volume ของ thin-slab intersection หาร slab thickness ส่วน second moment ระบุชัดว่าเป็น bounding proxy Curvature radius มาจาก finite `Face.curvatureAt` sample ที่ fixed parameter

## Semantic correspondence

support และ load region ใช้ extreme face-centroid rule ตาม declared longest path Contact ใช้ boundary set ที่ area ใหญ่สุด, thermal ใช้ทุก face และ fluid ใช้ curved faces หรือทุก face เมื่อไม่มี curved face แต่ละ region hash ชุด face signature ที่ sort แล้วพร้อม area การ recover datum และ region ไม่ใช้ face ordinal Semantic ที่หาย ambiguous ถูกแก้ หรือ stale ต้อง fail closed

## Replay

เก็บ exact STEP, manifest, sampling, toolchain และ configuration identity Clean rerun ต้องสร้าง report และ comparison ซ้ำได้ การสลับ candidate, face, datum หรือ region record อาจเปลี่ยน raw report hash แต่ normalized semantic comparison identity ต้องคงเดิม
