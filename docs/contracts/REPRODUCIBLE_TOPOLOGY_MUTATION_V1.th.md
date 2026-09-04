# การกลายพันธุ์โทโพโลยีที่ทำซ้ำได้ V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `REPRODUCIBLE_TOPOLOGY_MUTATION_V1.md`

## ขอบเขต

สัญญานี้สร้างข้อเสนอแบบมีชนิด กำหนดได้แน่นอน และทำก่อนการประเมินจาก corpus ของ Work 093 การยอมรับพิสูจน์เพียงว่า child เป็น genotype แบบมีขอบเขตที่สืบย้อนเส้นทางได้ภายใต้ grammar และ policy ที่ประกาศไว้ ไม่ได้พิสูจน์ว่า CAD สร้างได้ ผลิตได้ เป็นไปได้ทางฟิสิกส์ ปลอดภัย มีสมรรถนะ หรือผ่านการตรวจสอบเชิงวิทยาศาสตร์

## โอกาสคงที่และสายที่มา

initializer ทั้ง 6 strata ได้รับ operator 8 slot ตามลำดับเท่ากัน slot ที่ถูกปฏิเสธต้องคงเป็น rejected และห้ามโยกงบไปให้ slot อื่น แต่ละ ledger entry บันทึก parent genotype/topology identity, seed ของ stratum, slot, operator และ probability ที่ประกาศ, RNG checkpoint, retry trace, child genotype/topology identity เมื่อยอมรับ และ lineage SHA-256 จำนวน retry ถูกจำกัดด้วย protocol ที่ตรึงไว้

operator ที่เปลี่ยนโทโพโลยี 5 แบบคือ `grow_branch`, `prune_branch`, `split_part`, `add_crosslink` และ `reroute_path` ส่วน control 3 แบบคือ `replace_solid_family`, `insert_feature` และ `mutate_material_process` ซึ่งอาจเปลี่ยน canonical genotype signature แต่จะไม่ถูกระบุว่าเป็น topology operator ส่วน crossover ถูกปิดไว้อย่างชัดเจนเพราะ V1 ยังไม่มีสัญญา typed cut-boundary ที่เข้ากันได้

## กฎปิดเมื่อผิด

child ทุกตัวต้องถูกตรวจซ้ำภายใน corpus Work 093 ทั้งชุด containment cycle ที่ผิด, part/terminal/domain ที่สืบเส้นทางไม่ได้, path ที่ขาด, interface domain/DOF ที่เป็นไปไม่ได้, คู่ material/process ที่เข้ากันไม่ได้, topology signature ที่ไม่เปลี่ยน, retry ที่หมดงบ หรือข้อเสนอใด ๆ หลังมีหลักฐานจากการประเมินแล้ว ต้องล้มเหลวแบบมองเห็นได้ ห้าม result-conditioned mutation และ hidden retry

## การทำซ้ำ

canonical JSON hashing ไม่ขึ้นกับลำดับ mapping key แต่ยังรักษาลำดับ array และค่าทั้งหมด อินพุตที่ตรึงเหมือนกันต้องสร้าง ordered ledger และ `result_sha256` เหมือนเดิมทุกประการ reference ที่ถูกเปลี่ยนต้องทำให้ replay ล้มเหลว ไม่ใช่ถูกยอมรับเงียบ ๆ
