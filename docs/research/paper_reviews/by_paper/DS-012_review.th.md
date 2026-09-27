# DS-012: Measuring technological novelty with patent-based indicators

English source: `DS-012_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Dennis Verhoeven, Jurriën Bakker, Reinhilde Veugelers |
| ปี | 2016 |
| แหล่งตีพิมพ์ | Research Policy |
| DOI | 10.1016/j.respol.2015.11.010 |
| arXiv | Not recorded |
| ระเบียน canonical | [https://doi.org/10.1016/j.respol.2015.11.010](https://doi.org/10.1016/j.respol.2015.11.010) |
| หัวข้อในคลัง | การสังเคราะห์แบบ ความสร้างสรรค์ และหลักฐานความใหม่ |
| ความสัมพันธ์กับโครงการ | `indirect` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/15_design_synthesis_novelty/DS-012_Verhoeven2016_measuring-technological-novelty-with-patent-based.pdf) |
| SHA-256 ของต้นฉบับ | `88dbfa55cd7da6c541690f1f3bd2ebcbe72488f0b9374627a8b8abdc304ee09a` |
| coverage ของ full text | 25/25 หน้า (100.00%); สกัดได้ 9,567 คำ |

## คำถามวิจัย

จะใช้ข้อมูลสิทธิบัตรแยก radicalness เชิงเทคโนโลยีล่วงหน้าเป็น new functionality กับ new technological/scientific origins ได้หรือไม่?

## วิธีและหลักฐาน

งาน operationalize novelty ด้วย patent classification/citation แล้ว validate indicator บนตัวอย่าง patent application ขนาดใหญ่ด้วย breakthrough outcome และ control (หน้า 2, 11-12)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** new functionality กับ new origins มีความสัมพันธ์แต่ให้ข้อมูลต่างกัน correlation ระหว่าง indicator คนละมิติโดยทั่วไปไม่เกิน 0.3 และ indicator ระดับ IPC4 มีความสัมพันธ์บวกอย่างมีนัยสำคัญกับโอกาสเป็น breakthrough (หน้า 2, 11-12)
- **การตีความของผู้ทบทวน:** paper แสดงว่าคะแนน novelty เดียวไม่พอ แบบหนึ่งอาจใช้ความรู้ต้นทางแปลกใหม่แต่ไม่เพิ่มหน้าที่ หรือเพิ่มหน้าที่จากต้นทางคุ้นเคย
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** paper แสดงว่าคะแนน novelty เดียวไม่พอ แบบหนึ่งอาจใช้ความรู้ต้นทางแปลกใหม่แต่ไม่เพิ่มหน้าที่ หรือเพิ่มหน้าที่จากต้นทางคุ้นเคย โดยเป็นความเชื่อมโยงชนิด `indirect` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

indicator สิทธิบัตรขึ้นกับวิธี classify/cite, corpus, เวลา และยังไม่มี consensus เรื่อง radical innovation (หน้า 3) จึงไม่ยืนยัน physical function, performance หรือ freedom to operate การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **paper แสดงว่าคะแนน novelty เดียวไม่พอ แบบหนึ่งอาจใช้ความรู้ต้นทางแปลกใหม่แต่ไม่เพิ่มหน้าที่ หรือเพิ่มหน้าที่จากต้นทางคุ้นเคย** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **design-language descriptor, causal-function record และ template claim ความใหม่สี่ส่วน** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | design-language descriptor, causal-function record และ template claim ความใหม่สี่ส่วน |
| การเปลี่ยนแปลงที่เสนอ | วาง external novelty ไว้ปลายทาง หลัง causal function และ fair performance ผ่าน ให้คะแนน new functionality กับ new origins แยกกันด้วย prior-art corpus ที่ระบุวันที่และ human review ห้ามใช้ patent distance เป็น physics gate |
| experiment และ control | ใช้วิธี synthesis/novelty จาก paper กับ duplicate ที่รู้ผล, geometric variant, candidate ที่หน้าที่ต่าง และ external prior-art control โดยรักษา evaluator blindness |
| หลักฐานผ่านและล้มเหลว | ต้องแยก geometric variety, causal functional difference, performance benefit ที่ยุติธรรม และ external technology novelty ได้ถูก และปฏิเสธผลบวกจากรูปลักษณ์อย่างเดียว |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 25 หน้า, 62,157 ตัวอักษร, 9,567 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 25/25
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 2, 3, 4, 5, 6, 7, 8, 9 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: abstract
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
