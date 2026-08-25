# Typed Energy Component Graph

สถานะ: ดำเนินการแล้วสำหรับ Work 012

ต้นฉบับภาษาอังกฤษ: `ENERGY_COMPONENT_GRAPH.md`

## จุดประสงค์และขอบเขตของข้ออ้าง

Work 012 กำหนดและ compile interface ที่มีทิศทางของ topology พลังงาน/powertrain
ก่อนอนุญาตให้ simulation ใช้งาน Chain อ้างอิงที่ถูกต้องคือ:

```text
battery -> motor -> gearbox -> rear_tyre -> road
```

การ compile พิสูจน์เพียงว่า role ของ component, ทิศ port, carrier, connectivity
และลำดับ directed acyclic ตรงตาม interface contract นี้ ไม่ได้คำนวณ operating
power, joule, efficiency, depletion, heat หรือ conservation และไม่ใช่ physical
validation

## Contract ของ SI และชนิด

ทุก port ประกาศ:

- `port_id` ที่ไม่ซ้ำภายใน component
- ทิศ `input` หรือ `output`
- carrier หนึ่งชนิด: `chemical`, `electrical`, `mechanical_rotational`,
  `mechanical_translational` หรือ `thermal`
- `maximum_power_w` หน่วยวัตต์ที่ finite และเป็นบวก

Connection ส่ง power บวกตามทิศจาก output หนึ่งไป input หนึ่ง Carrier ที่ปลาย
ทั้งสองต้องตรงกัน Capacity ของ connection ที่ compile แล้วคือ:

```text
maximum_connection_power_w = min(source_port_capacity, target_port_capacity)
```

ค่านี้เป็นเพดาน interface ไม่ใช่ operating point

## Role ของ Component

| Role | ความหมาย port ที่ต้องมี |
|---|---|
| `source` | มีเฉพาะ output port |
| `converter` | มี input และ output อย่างน้อยอย่างละหนึ่ง; เปลี่ยน carrier ได้ |
| `transmission` | มี input/output และทุก port เป็น `mechanical_rotational` |
| `tyre` | input `mechanical_rotational` และ output `mechanical_translational` |
| `sink` | มีเฉพาะ input port |

Factory สร้าง role source, converter, transmission, tyre และ sink baseline
ส่วน generic component ยังต้องผ่าน role validation เดียวกัน

## กฎ Graph แบบ Fail-Closed

Work 012 ปฏิเสธ:

- carrier ที่ไม่รองรับหรือเข้ากันไม่ได้
- ใช้ input เป็น source หรือ output เป็น target
- endpoint หาย, identity ว่าง/ซ้ำ และ self-loop
- source connection มากกว่าหนึ่งเข้า input เดียว
- output fan-out โดยนัย
- required port ใด ๆ ที่ไม่เชื่อม
- directed cycle
- capacity invalid หรือ non-finite

Port ทุกจุด required และ one-to-one Output fan-out ไม่ถูกมองเป็นการทำซ้ำ power
แบบเงียบ Splitter ในอนาคตต้องจัดสรรหนึ่ง input ไปหลาย output อย่างชัดเจน และ
ผ่าน conservation audit

## การ Compile ที่ทำซ้ำได้

Compiler ใช้ lexical tie-breaking ใน Kahn topological sorting ส่วน connection
ที่ compile ใช้ลำดับ endpoint แบบ lexical ดังนั้นการสลับ tuple component และ
connection input ให้ผล compiled metadata เท่ากันทุกประการ

Chain อ้างอิงมีเพดาน connection ต่อไปนี้:

| Connection | Carrier | Maximum power |
|---|---|---:|
| `c1` battery → motor | electrical | `480000 W` |
| `c2` motor → gearbox | mechanical rotational | `440000 W` |
| `c3` gearbox → rear tyre | mechanical rotational | `410000 W` |
| `c4` rear tyre → road | mechanical translational | `390000 W` |

ใช้คำสั่ง:

```powershell
python scripts/validate_energy_graph.py
python -m unittest tests.test_energy_graph -v
```

## ข้อจำกัดและงานถัดไป

- ความเข้ากันของ capacity ไม่ได้กำหนด power ที่ใช้จริง
- Work 012 ยังไม่มี efficiency, loss port, storage state, energy integration
  หรือ residual
- Graph เป็น acyclic และ one-to-one; regenerative loop, splitter, merger และ
  หลาย shaft ต้องมี semantics ชัดเจนในงานหลังจากนี้
- Work 013 จะ audit energy transfer ที่ประกาศต่อ step อย่างอิสระ และต้องทำให้
  hidden/double-counted energy invalid แทนการสมมติว่า topology ที่ compile แล้ว
  อนุรักษ์พลังงาน
