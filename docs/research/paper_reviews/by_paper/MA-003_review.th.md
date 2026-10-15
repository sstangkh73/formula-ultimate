# MA-003: Exploration of data science techniques to predict fatigue strength of steel from composition and processing parameters

English source: `MA-003_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Ankit Agrawal, Parijat D Deshpande, Ahmet Cecen, Gautham P Basavarsu, Alok N Choudhary, Surya R Kalidindi |
| ปี | 2014 |
| แหล่งตีพิมพ์ | Integrating Materials and Manufacturing Innovation |
| DOI | 10.1186/2193-9772-3-8 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.1186/2193-9772-3-8](https://doi.org/10.1186/2193-9772-3-8) |
| หัวข้อในคลัง | วัสดุ ข้อต่อ ความล้า และการผลิต |
| ความสัมพันธ์กับโครงการ | `data` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/12_materials_joints_manufacturing/MA-003_Agrawal2014_exploration-of-data-science-techniques-to-predict.pdf) |
| SHA-256 ของต้นฉบับ | `390cc476d0f097cfd8b1b216a72cff89c1e371b36fb40e385e802ca4d1bbf204` |
| coverage ของ full text | 19/19 หน้า (100.00%); สกัดได้ 8,896 คำ |

## คำถามวิจัย

จะทำนาย fatigue strength ของเหล็กจาก composition และ processing variable ด้วยข้อมูลวัสดุเปิดได้หรือไม่ และ input ใดสำคัญที่สุด?

## วิธีและหลักฐาน

งานทำความสะอาดข้อมูลเหล็ก NIMS จัดอันดับ feature ด้าน composition/process fit regressor หลายชนิดรวม neural network, tree และ polynomial และประเมินด้วย leave-one-out cross-validation สำหรับ rotating-bending fatigue ที่ 10^7 cycle (หน้า 5-10)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** หลาย model ได้ R2 ประมาณ 0.98 และ error ที่รายงานต่ำกว่า 4% ดีกว่างานก่อนและช่วยจัดอันดับ composition/process variable ที่ทำนายได้ (หน้า 1, 13-15)
- **การตีความของผู้ทบทวน:** paper model ความเชื่อมโยง process-structure-property ไม่ใช่ composition อย่างเดียว ตรงกับกฎโครงการว่าค่าวัสดุขึ้นกับประวัติการผลิต
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** paper model ความเชื่อมโยง process-structure-property ไม่ใช่ composition อย่างเดียว ตรงกับกฎโครงการว่าค่าวัสดุขึ้นกับประวัติการผลิต โดยเป็นความเชื่อมโยงชนิด `data` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

ผู้เขียนระบุว่าชุดข้อมูลเล็กสำหรับ data mining และควรเพิ่มข้อมูลหลายแหล่ง (หน้า 16) LOOCV ในฐานเดียวไม่พิสูจน์การถ่ายโอนข้ามแหล่ง/โลหะใหม่ หรือ fatigue แบบ multiaxial, thermal, variable amplitude และ prediction ไม่ใช่ causation การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **paper model ความเชื่อมโยง process-structure-property ไม่ใช่ composition อย่างเดียว ตรงกับกฎโครงการว่าค่าวัสดุขึ้นกับประวัติการผลิต** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **material-data policy และหลักฐาน joint/failure/tolerance ของ Works 113/114/116/130** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | material-data policy และหลักฐาน joint/failure/tolerance ของ Works 113/114/116/130 |
| การเปลี่ยนแปลงที่เสนอ | ลงทะเบียน provenance ของ NIMS และทำซ้ำ model ด้วย holdout แยก alloy family/source ใช้ prediction จัดลำดับการทดสอบเท่านั้น แล้ว validate S-N/failure data เฉพาะ candidate ก่อน Work 116 admission |
| experiment และ control | validate property/mechanism จาก paper ด้วย specimen และ joint/assembly held-out ข้าม process, orientation, temperature, tolerance, preload, surface และ cyclic loading |
| หลักฐานผ่านและล้มเหลว | ต้องมี property provenance ครบ, uncertainty ที่ calibrate, failure mode/location ถูก และการถ่ายโอน specimen-to-assembly มีขอบเขต สภาวะไม่มีข้อมูลคงเป็น unknown |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 19 หน้า, 55,665 ตัวอักษร, 8,896 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 19/19
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 7, 8, 9, 10, 11, 13 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract, conclusion, methods, results
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
