# Optimized Vehicle Controls V1

แหล่งภาษาอังกฤษ: `OPTIMIZED_VEHICLE_CONTROLS_V1.md`

สถานะ: Work 127 นำไปใช้เป็นด่าน fairness และ substitution ที่ลงทะเบียนล่วงหน้า

## ขอบเขตหลักฐาน

แขน fixed-topology, reference, random-control และ open-candidate ได้รับ external task, component-library opportunity, source energy, safety boundary, paired conditions และ budget แยกของ vehicle-search/controller-tuning เหมือนกัน ทุกแขนถูก optimize fixed topology เป็นเพียง control และไม่จำกัด layout ของ open arm

ประเมิน common-controller substitution ก่อน matched-budget retuning system estimand คือ open candidate ที่ retune ลบด้วย non-open control ที่ retune แล้วและดีที่สุด base, cooling, containment และ support mass ที่ติดตั้ง, source/use energy และ manufacturing penalty ถูกถ่ายเข้าในทุก score baseline ที่ไม่ tune, controller adaptation ที่ไม่คิดต้นทุน, burden ledger ไม่ครบ หรือ source energy ไม่เท่ากันทำให้ fairness เป็น invalid

การอ้าง system benefit ต้องให้ขอบล่างของ registered paired interval ถึง meaningful-effect threshold โดยไม่มี failure หรือ hidden burden exact replay ต้องได้ result SHA-256 เดิม response fixture เป็นข้อมูลสังเคราะห์ และ Work 126 ยังเป็น exploratory; สัญญานี้ไม่ยืนยัน held-out race performance, external novelty, promotion หรือ physical validation
