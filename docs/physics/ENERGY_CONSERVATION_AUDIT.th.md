# Independent Energy-Conservation Audit

สถานะ: ดำเนินการแล้วสำหรับ Work 013

ต้นฉบับภาษาอังกฤษ: `ENERGY_CONSERVATION_AUDIT.md`

## ขอบเขตและ convention

Auditor ตรวจ energy ในช่วงเวลาที่ประกาศบน graph Work 012 ที่ compile แล้ว
พลังงานทั้งหมดใช้ joule ค่า input, output, transfer และ declared loss ไม่ติดลบ;
stored-energy change มีเครื่องหมาย (บวกคือเก็บ ลบคือปล่อย)

```text
component residual = E_in - E_out - E_loss - delta_E_stored
tolerance = absolute_j + relative * max(abs(all declared/observed terms))
```

ระบบตรวจ input/output ของ component เทียบผลรวม connection transfer แยกกัน
ต้องมีหลักฐาน component/connection ครบตรงทุกจุด Residual ถูกรายงานและไม่แก้ทิ้ง

## กฎสถานะ

`valid` ต้องให้ balance/interface residual ทุกค่าภายใน tolerance, endpoint ถูก,
หลักฐานไม่ซ้ำ และไม่มีหลักฐานขาด/เกิน มิฉะนั้นเป็น `invalid` พร้อม violation
ตามลำดับ Tolerance เริ่มต้นคือ absolute `1e-9 J` และ relative `1e-12`

Chain อ้างอิง `100 J` ปล่อย `100 J` จาก storage, เสีย `10 J` ใน motor และเก็บ
`90 J` ที่ road sink จึงปิดที่ `0 J` การเพิ่ม output motor เป็น `95 J` แต่คง
loss `10 J` ให้ `-5 J`; การประกาศ loss `20 J` ขณะ output `90 J` ให้ `-10 J`
ทั้งคู่ invalid

```powershell
python scripts/validate_energy_audit.py
python -m unittest tests.test_energy_audit -v
```

## ข้อจำกัด

Audit พีชคณิตนี้ไม่พิสูจน์สมการ source, power integration, efficiency map หรือ
ความจริงทางกายภาพ ตรวจเฉพาะหลักฐานที่ส่งเข้า Thermal state, uncertainty,
regenerative timing และ race integration เป็นงานขั้นถัดไป Audit valid เป็น
หลักฐานจำเป็น ไม่ใช่ physical validation
