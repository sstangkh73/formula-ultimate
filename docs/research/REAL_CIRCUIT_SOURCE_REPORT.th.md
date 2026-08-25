# รายงานแหล่งข้อมูลสนามจริง — แค็ตตาล็อก v1

ไฟล์ต้นฉบับภาษาอังกฤษ: `REAL_CIRCUIT_SOURCE_REPORT.md`

สถานะ: บันทึก baseline หลักฐานเมื่อ 2026-08-25

## เหตุผลการเลือกสนาม

ชุดนี้ตั้งใจครอบคลุมสนามถนนแคบ สนามความเร็วสูงสุด สนามยาวและไวต่อความสูง
สนามถนนกลางคืนที่ร้อนและมีกำแพง สนามเปลี่ยนทิศทางความเร็วสูง สนามสั้นที่ต้องการ
downforce สูง สนามที่สูงจากระดับน้ำทะเลมาก สนามทะเลทรายที่เน้นเบรก/traction
และสนามทวนเข็มที่มีความสูงเปลี่ยน จุดประสงค์ไม่ใช่จำลองทั้ง championship แต่คือ
ให้เอเจนต์พบข้อเรียกร้องจากโลกจริงที่ขัดกันก่อนสร้าง geometry

## ข้อเท็จจริงที่บันทึก

| Profile | ความยาว (m) | รอบ | ระยะเรซ (m) | โค้ง | ความกว้างเผยแพร่ (m) | ความแตกต่างหลักต่อดีไซน์ |
|---|---:|---:|---:|---:|---:|---|
| Monaco 2026 | 3,337 | 78 | 260,286 | 19 | ต่ำสุด 7 | พื้นที่จำกัดและความคล่องตัว |
| Monza ปัจจุบัน | 5,793 | 53 | 306,720 | 11 | 10–12 | ความเร็วสูงสุดและการเบรก |
| Spa 2026 | 7,004 | 44 | 308,052 | 19 | ยังไม่ทราบ | รอบยาว ความสูง และโค้งเร็ว |
| Singapore 2025 | 4,940 | 62 | 306,143 | 19 | ยังไม่ทราบ | ความร้อน ผิวขรุขระ กำแพง traction |
| Suzuka 2026 | 5,807 | 53 | 307,471 | 18 | 10–16 | เปลี่ยนทิศทางด้วยความเร็วสูง |
| Silverstone 2026 | 5,891 | 52 | 306,198 | 18 | ยังไม่ทราบ | โหลด aero ต่อเนื่องในโค้งเร็ว |
| Hungaroring 2026 | 4,381 | 70 | 306,630 | 14 | ยังไม่ทราบ | โค้งต่อเนื่องและ downforce สูง |
| Mexico City ปัจจุบัน | 4,304 | 71 | 305,354 | 17 | ยังไม่ทราบ | อากาศที่ `2,285 m` และ cooling |
| Bahrain ปัจจุบัน | 5,412 | 57 | 308,238 | 15 | ยังไม่ทราบ | เบรก traction และอุณหภูมิ |
| Sao Paulo ปัจจุบัน | 4,309 | 71 | 305,879 | 15 | 12–15 | banking, camber, ทางขึ้น และอากาศ |

## ลำดับความน่าเชื่อถือของแหล่งข้อมูล

รับข้อเท็จจริงจาก FIA/Formula 1 ผู้ดำเนินการสนาม หรือผู้จัดงาน ไม่ใช้บล็อกผลค้นหา
หรือฐานข้อมูลสนามที่ไม่มีแหล่งอ้างอิงเป็นหลักฐานมิติแบบ hard constraint คำอธิบาย
เชิงคุณภาพใช้สนับสนุนสมมติฐานคะแนนแบบ ordinal ได้ แต่คำว่า “แคบ” หรือ “tight”
จะไม่ถูกแปลงเป็นเมตร

แหล่งข้อมูลสถิติสนามทางการจาก Formula 1:

- [คู่มือ Monaco 2026](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-the-circuit-de-monaco.vFsmfGHr6RWyLFtxi58wi)
- [หน้าสนาม Monza](https://www.formula1.com/en/information/italy-autodromo-nazionalemonza.FiJN1jnQlRLeHqOxIt13m)
- [คู่มือ Spa 2026](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-the-circuit-de-spa-francorchamps.pC5N3J3W9LEj8REFvU6FX)
- [ตัวอย่าง Singapore 2025](https://www.formula1.com/en/latest/article/need-to-know-the-most-important-facts-stats-and-trivia-ahead-of-the-2025-singapore.468A8YSelm8nsKywLuGTf) และ [FIA media kit 2025](https://www.fia.com/sites/default/files/spg2025_0062_f1_mediakit_2025_eng_a4_250623_view.pdf)
- [คู่มือ Suzuka 2026](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-the-suzuka-circuit.2BbgsRdkeux78UBGbmYiZV)
- [คู่มือ Silverstone 2026](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-silverstone-2026.5Sl0O8g393enBWVIkjRzOr)
- [คู่มือ Hungaroring 2026](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-the-hungaroring.4ddtLbzLWLRjli7Y793jqh)
- [หน้าสนาม Mexico City](https://www.formula1.com/en/information/mexico-autodromo-hermanos-rodriguez-mexico-city.1K2WPfBcI8kTXjcTHcbsBM) และ [หลักฐานระดับความสูงจาก Formula 1](https://ticketing.formula1.com/tickets/en/mexico/general-admission-f1-ciudad-de-mexico-waitlist)
- [หน้าสนาม Bahrain](https://www.formula1.com/en/information/bahrain-international-circuit.2CaIdaOTCgQ3Yfnb37NmSS)
- [หน้าสนาม Sao Paulo](https://www.formula1.com/en/information/brazil-autodromo-jose-carlos-pace-sao-paulo.5z2RfrmiTTfEP6Wnxv1yIW)

หลักฐานความกว้างทางการ:

- Monaco: บทความเชิงวิศวกรรมของผู้จัด Mexico GP ระบุว่าถนน Monaco กว้างเพียง
  `7 m` และอธิบายว่ารถที่ใหญ่ขึ้นทำให้การแข่งขันแย่ลง:
  [บทความขนาดรถ](https://www.mexicogp.mx/noticia/asi-afecta-el-tamano-de-los-autos-a-la-formula-1/?IDM=LANG_EN)
- Monza: ผู้ดำเนินการสนามเผยแพร่ `ต่ำสุด 10 m – สูงสุด 12 m`:
  [layout Monza](https://www.monzanet.it/en/circuit/)
- Suzuka: ผู้ดำเนินการสนามเผยแพร่ `10–16 m`:
  [คู่มือสนาม Suzuka](https://www.suzukacircuit.jp/eng/course_s/)
- Sao Paulo: ผู้ดำเนินการสนามของเทศบาลเผยแพร่ `12–15 m`:
  [หน้าสนาม Interlagos](https://autodromodeinterlagos.prefeitura.sp.gov.br/circuito)

[หน้าผู้ดำเนินการ Bahrain](https://www.bahraingp.com/corporate-sales/track-hire/)
เผยแพร่ `14–15 m` ใต้หัวข้อ **Inner Track** ไม่ใช่ **Grand Prix Track** จึงใช้กับ
width gate ของ Formula 1 ไม่ได้ และ Bahrain ยังคงเป็น `indeterminate`

## ความขัดแย้งของหลักฐานที่เก็บไว้

layout ชั่วคราวของ Singapore มีการเปลี่ยนแปลง FIA media kit ปี 2025 ระบุ layout
19 โค้ง ยาว `4.94 km` จำนวน 62 รอบ และระยะเรซ `306.143 km` ขณะเดียวกันผู้จัด
โฆษณาค่าในอนาคต `4.927 km` และหน้าเก่าปี 2008 เคยระบุความกว้าง `10–15 m`
สำหรับ layout เก่า 5.067 km ดังนั้นแค็ตตาล็อก v1 จึงตรึง Singapore กับ layout FIA
ปี 2025 และไม่ย้ายค่าความกว้างเก่ามาเป็น hard gate ปัจจุบัน การเป็น
`indeterminate` ตรงนี้เป็นสิ่งที่ตั้งใจ ไม่ใช่ค่าเริ่มต้นแทนข้อมูลที่หายไป

## วินัยการทบทวน

ตัวแปรอิสระคือ profile สนามและความกว้างรถที่เสนอ ตัวแปรตามคือสถานะ static width,
ความหนาแน่น ISA เมื่อทราบระดับความสูง ค่าขนาดเรซ และเวกเตอร์แรงกดดัน 8 แกน
ตัวควบคุมคือนโยบายระยะเผื่อและเวอร์ชันแค็ตตาล็อกเดียวกันสำหรับรถทุกแบบ

สมมติฐานที่ต้องการทดสอบคือ การให้สนามจริงที่หลากหลายก่อนออกแบบจะป้องกันไม่ให้
รถขนาดใหญ่แบบไร้ข้อจำกัดหนึ่งแบบครองทุกสนาม การทดสอบรถกว้าง `7.0 m` พยายาม
หักล้างคุณสมบัติ “แข่งได้ทุกสนาม” และ Monaco ปฏิเสธเมื่อกำหนดระยะเผื่อข้างละ
`0.25 m` หลักฐานที่ขัดแย้งคือการผ่าน static width ยังไม่พิสูจน์ว่ารถเลี้ยวได้ และ
6 profile ยังไม่มีหลักฐานความกว้างปัจจุบัน คำอธิบายทางเลือกของผลลัพธ์ในอนาคตคือ
การเลือกคะแนนแรงกดดัน ข้อมูลผิวสนาม/อากาศที่ยังขาด และคุณภาพการควบคุมรถแทนที่
จะเป็น topology เอง ระดับความมั่นใจสูงสำหรับข้อเท็จจริงขนาดเรซ ปานกลางสำหรับ
width screen 4 สนาม และต่ำถึงปานกลางสำหรับสมมติฐานคะแนน ordinal จนกว่าจะทำ
sensitivity analysis
