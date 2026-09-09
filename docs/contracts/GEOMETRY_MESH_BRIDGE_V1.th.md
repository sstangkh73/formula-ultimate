# สะพาน Geometry สู่ Mesh V1

ต้นฉบับภาษาอังกฤษ: `GEOMETRY_MESH_BRIDGE_V1.md`

Status: พัฒนาโดย Work 110 สำหรับสองเส้นทางแบบมีขอบเขต

## ขอบเขตและแหล่งข้อมูล

Contract นี้สร้าง Gmsh 2.2 tetrahedral volume และ triangular semantic-surface meshes จาก labelled field ที่ตรงกันของ Work 109 และ hollow B-rep ที่ตรงกันของ Work 108 พิสูจน์ deterministic mesh construction, การส่งต่อ identity/label และ geometry approximation แบบมีขอบเขต ไม่พิสูจน์ solver accuracy, field convergence, strength, thermal/flow, manufacturing หรือ physical validity

ตรึงทั้ง upstream commit และ contract SHA-256 เส้นทาง Work 109 ใช้ implicit source field ที่ตรวจแล้ว เส้นทาง Work 108 สร้าง STEP corpus Work 092 ทั้งชุดใหม่ตามลำดับเดิมและบังคับ hollow source SHA-256 `12bcac345f9395ffc766d84a8385a488c75533d162c233e6989215f8829e636d7`

## การสร้าง mesh และ semantics

occupied Cartesian cell ที่ admitted แต่ละช่องถูกแบ่งเป็น tetrahedra หกก้อนรอบ body diagonal คงที่ มุม grid ที่ใช้ร่วมกลายเป็น shared nodes แก้ลำดับ orientation ลบก่อน admission; signed Jacobian สุดท้ายทุกค่าต้องเกิน `1e-12 m3` และ edge ratio ไม่เกิน `1.8` ไม่มี fallback เป็นกล่องหรือ geometry ที่ repair

Tetrahedra รักษา scalar material physical groups Exterior faces สร้าง `external_surface`, ผิว negative-X สร้าง `load_surface`, ผิว negative-Z สร้าง `contact_surface` และเพื่อนบ้าน label ต่างกันสร้าง `material_interface` หนึ่งชุดที่คงชื่อ แต่ละ route ประกาศ sets ที่ต้องมี; ชื่อหายหรือ node reference เก่าล้มเหลวแบบปิด

เส้นทาง B-rep sample solid ที่มีเนื้อจริงที่ cell centres นี่คือ voxel approximation ที่เปิดเผย ไม่ใช่ conforming curved mesh Volume error และ constant-density mass error เทียบ reference ต้องไม่เกิน `0.35` centerline กลวงจริงต้องยังเป็น void ทุกระดับ; outer-solid fill เป็น negative control ชัดเจน

## Refinement หลักฐาน และการส่งต่อ

ทั้งสองเส้นทางรัน `0.02`, `0.01` และ `0.008 m` เก็บ element quality, nodes, elements, deterministic visits, volume/mass errors, set coverage และ identities Error ที่ไม่ monotonic เป็นหลักฐาน aliasing ไม่ใช่ convergence Inverted elements, sets หาย, หน่วยผิด, cavity ถูกเติม, source เก่า, label หาย, เกินงบ และ substitution ล้มเหลวแบบมองเห็นได้

Work 111 ใช้ Gmsh artifacts และ semantic sets ที่ตรงกันเพื่อสร้าง vector solid fields ได้ แต่ต้องตรวจสมการ boundary conditions และ numerical behaviour สามระดับอย่างอิสระ Work 110 ส่งเฉพาะ mesh geometry
