# OE-016: Scalable Co-Optimization of Morphology and Control in Embodied Machines

English source: `OE-016_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | Nick Cheney, J. Bongard, Vytas SunSpiral, Hod Lipson |
| ปี | 2018 |
| แหล่งตีพิมพ์ | Journal of the Royal Society Interface |
| DOI | Not recorded |
| arXiv | 1706.06133 |
| ระเบียน canonical | [https://arxiv.org/abs/1706.06133](https://arxiv.org/abs/1706.06133) |
| หัวข้อในคลัง | การออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended |
| ความสัมพันธ์กับโครงการ | `direct` |
| ระดับการทบทวน | deep review สำหรับการตัดสินใจ |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../papers/01_open_ended_codesign/OE-016_Cheney2018_scalable-co-optimization-of-morphology-and-control.pdf) |
| SHA-256 ของต้นฉบับ | `ec75ed5670641b271a45297862b1ada057c6d96b983ca525809d86e1bee40f98` |
| coverage ของ full text | 10/10 หน้า (100.00%); สกัดได้ 8,135 คำ |

## คำถามวิจัย

co-design search จะรักษา morphology ใหม่ไว้นานพอให้ controller ปรับตัวได้หรือไม่ แทนการคัดทิ้งจาก fitness ทันที?

## วิธีและหลักฐาน

งานวิวัฒนาการหุ่นยนต์ voxel เสมือนและเพิ่มอายุ morphology เป็น objective ที่สอง เทียบ morphological-innovation protection กับแบบไม่ปกป้องและการปกป้องทางเลือกตลอด 5,000 generation (หน้า 4-6)

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** เมื่อปกป้อง morphology ค่า fitness เฉลี่ยเพิ่มจาก 18.715 ที่ generation 0 เป็น 22.916 ที่ generation 5,000 (p < 0.001) ส่วนการปกป้องทางเลือกไม่ดีกว่าแบบไม่ปกป้อง (p = 0.240) และแย่กว่า morphology protection อย่างมีนัยสำคัญ (p = 1.211e-4) (หน้า 4)
- **การตีความของผู้ทบทวน:** paper แยก controller-adaptation lag เป็น selection bias: ลูกที่โครงสร้างมีศักยภาพอาจดูแย่เพียงเพราะรับ controller ที่เฉพาะกับ parent มา (หน้า 5)
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** paper แยก controller-adaptation lag เป็น selection bias: ลูกที่โครงสร้างมีศักยภาพอาจดูแย่เพียงเพราะรับ controller ที่เฉพาะกับ parent มา (หน้า 5) โดยเป็นความเชื่อมโยงชนิด `direct` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

หลักฐานมาจากการเคลื่อนที่ของ voxel เสมือน และผู้เขียนระบุว่า fitness ที่เพิ่มยังไม่พิสูจน์คำอธิบายเชิงสาเหตุอย่างเด็ดขาด (หน้า 4) จึงยังไม่ยืนยันผลเดียวกันในรถแข่งหรือเมื่อคิดต้นทุนฝึก controller เท่ากัน การตรวจ heading แบบอัตโนมัติ **ไม่พบเป็น heading แยก** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **paper แยก controller-adaptation lag เป็น selection bias: ลูกที่โครงสร้างมีศักยภาพอาจดูแย่เพียงเพราะรับ controller ที่เฉพาะกับ parent มา (หน้า 5)** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124 |
| การเปลี่ยนแปลงที่เสนอ | เพิ่มอายุ morphology และจำนวน step ฝึก controller ใน ledger ของ candidate ทุกตัว แล้วเทียบ co-design แบบปกป้อง/ไม่ปกป้องด้วย controller step รวมเท่ากัน โดยผล held-out ต้องยังอยู่หลัง morphology ทุกแบบได้โอกาสปรับตัวเท่ากัน |
| experiment และ control | รัน operator หรือกฎจัดสรรที่ได้จาก paper เทียบ evolution/QD และ fixed-topology control ที่ optimize แล้ว โดยจับคู่ seed, compute รวม, งบฝึก controller และสนาม held-out |
| หลักฐานผ่านและล้มเหลว | ยอมรับเมื่อ feasible archive coverage หรือผลงานสนาม held-out ดีขึ้นโดยไม่เพิ่มแบบ invalid, controller under-training หรือ evaluator disagreement มิฉะนั้นปฏิเสธการถ่ายโอน |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: 10 หน้า, 52,154 ตัวอักษร, 8,135 คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: 10/10
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: 1, 2, 4, 5, 6, 8, 9 เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: ไม่พบ heading ที่เชื่อถือได้
- extraction error: 0; มีแนวโน้มเป็นสแกน: `false`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
