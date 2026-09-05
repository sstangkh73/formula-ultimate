# ผล Work 104: Protocol การค้นพบรถทั้งคันและเทคโนโลยี

ต้นฉบับภาษาอังกฤษ: `2026-09-06_104_whole-vehicle-discovery-protocol-result.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และไฟล์ที่เปลี่ยน

- เพิ่ม `docs/contracts/WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md` และคู่ภาษาไทย เป็น normative protocol ลงวันที่ใหม่ โดยระบุว่า implementation ยัง pending
- เพิ่มประกาศเปลี่ยนเอกสารอ้างอิงลงวันที่ใน `docs/reports/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` และคู่ภาษาไทย โดยเก็บเนื้อหาประวัติตรงทุก byte
- เพิ่มสำเนา roadmap ทั้งสองภาษาก่อนแก้ที่ตรงต้นฉบับภายใต้ `docs/reports/backups/2026-09-06_104/`
- เพิ่มผลนี้ แผน Work 104 และคู่ภาษาไทย ขอบเขต commit ที่ตั้งใจรวม 10 Markdown files

## ข้อตัดสินใจ

- ขอบเขตชิ้นส่วนภายใน บริเวณหลายหน้าที่ architecture และ controllers วิวัฒนาการร่วมกันได้ ขณะที่ external task ที่ลงทะเบียนยังตรึง
- Exploratory integration เริ่มด้วยหลักฐานเฉพาะส่วนที่ประกาศว่ายังไม่ครบได้ แต่ complete-vehicle claims ยังต้องมี promotion evidence ทุกด้านที่เกี่ยวข้องและแบบสามมิติที่คิดบัญชีครบ
- Evidence states แยกหลายมิติตาม domain/fidelity/process/use โดยแยก untested, unsupported, numerical failure, physical failure และ corrupted provenance
- การเรียนรู้หลังเห็นผลสร้าง descendant หรือ evaluation identity ใหม่ ไม่เขียนทับ parent เกณฑ์เดิม หรือต้นทุน
- Registration กำหนดกติกา budget, replay, audit, statistical และ holdout ชัด Numerical study thresholds ต้องใส่ก่อน admitted observations และไม่แต่งสำหรับ domains ที่ยังไม่ implement
- Geometry ใหม่ mechanism, vehicle utility และ external novelty ต้องใช้หลักฐานต่างกัน Graph non-isomorphism ไม่บังคับกับทุกการค้นพบ
- ปรับ deliverables ของ Works 098–101 โดย Work 104 ไม่ได้ implement หรือทำงานเหล่านั้นเสร็จ

## หลักฐาน backup

Source revision: `9889daf`

- English SHA-256: `686b81df2f98b566775010aabcf225ae32a8552f9ec1818d43b1457070dbc449`
- Thai SHA-256: `f86ee5472f5afe02f18ac14685dcf755de7a56bd82c5ade960cc2b51d71338c3`

คัดลอกและตรวจ hash ของ backup ทั้งคู่ก่อนเปลี่ยนต้นฉบับใด ๆ แล้วตรวจเทียบกับ Git source bytes และ staged backup blobs

## Validation

Environment: Windows / PowerShell; Python 3.14.3 รัน gates แยกกัน และไม่ดำเนิน commit หลัง gate ล้มเหลว

- ตรวจ backup/content/link: exit 0; backup ตรงต้นฉบับ 2 ฉบับ เนื้อหาประวัติตรงเดิม 2 ฉบับ หัวข้อหมายเลขตรงกัน 15 หัวข้อ fenced content และ technical token sets ตรงกัน และ local links ใช้ได้ 14 ลิงก์ ตรวจสองภาษาด้วยการอ่านให้ขอบเขต ข้อจำกัดการกล่าวอ้าง และ implementation boundaries เทียบเท่ากัน
- ตรวจ staged backup: exit 0; Git blobs ใน staging ทั้งคู่ตรง original blobs ที่ `9889daf`
- Repository contract tests: exit 0; ผ่าน 6 tests ไม่รัน physics suites ซ้ำเพราะไม่มี implementation เปลี่ยน
- `git diff --check`: exit 0
- ตรวจ staged scope: exit 0; ตรง 10 Markdown files ที่ตั้งใจ
- `git diff --cached --check` ครั้งแรก: exit 1 แจ้ง trailing whitespace 6 บรรทัดจาก Markdown hard breaks ใน metadata ของ protocol ใหม่ เปลี่ยนเป็นย่อหน้าแยกด้วยบรรทัดว่างทั้งสองภาษา แล้วรันซ้ำได้ exit 0 ไม่มี output การตรวจที่ล้มเหลวหยุดเส้นทาง commit จนแก้แล้ว
- Git แจ้ง LF/CRLF checkout advisories โดยตรวจ working bytes ของ backup และ staged blobs แยกกัน ไม่ใช้การ normalize backup แทน byte equality

คำสั่ง validation ที่รันจริง (ตรวจแต่ละ gate แยกกัน):

````powershell
@'
from pathlib import Path
import hashlib, re, subprocess
root = Path.cwd()
name = 'WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06'
protocols = [root / 'docs/contracts' / (name + ext) for ext in ('.md', '.th.md')]
texts = [p.read_text(encoding='utf-8') for p in protocols]
for text in texts:
    assert '2026-09-06' in text and 'FU-WHOLE-VEHICLE-DISCOVERY-V1-2026-09-06' in text
    assert 'Status: Normative design protocol; implementation pending' in text
    assert re.findall(r'^## (\d+)\.', text, re.M) == [str(i) for i in range(1, 16)]
    assert '\ufffd' not in text
assert re.findall(r'```[^\n]*\n(.*?)```', texts[0], re.S) == re.findall(r'```[^\n]*\n(.*?)```', texts[1], re.S)
tokens = [set(t for t in re.findall(r'(?<!`)`([^`\n]+)`(?!`)', text) if not t.endswith('.md')) for text in texts]
assert tokens[0] == tokens[1], tokens[0] ^ tokens[1]
link_sources = list(zip(protocols, texts))
for suffix in ('.md', '.th.md'):
    filename = 'GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1' + suffix
    original = subprocess.check_output(['git', 'show', '9889daf:docs/reports/' + filename])
    backup = root / 'docs/reports/backups/2026-09-06_104' / filename
    current = root / 'docs/reports' / filename
    assert backup.read_bytes() == original, filename
    value = current.read_bytes()
    assert value.endswith(original), filename
    notice = value[:-len(original)].decode('utf-8')
    assert notice.startswith('> ') and '2026-09-06' in notice
    digest = hashlib.sha256(original).hexdigest()
    assert all(digest in text for text in texts)
    link_sources.append((current, notice))
    print(filename, digest, 'backup and historical body exact')
links = 0
for path, text in link_sources:
    for target in re.findall(r'\]\(([^)]+)\)', text):
        assert (path.parent / target.split('#')[0]).is_file(), (path, target)
        links += 1
print('PASS: 2 exact backups; 2 exact historical bodies; 15 matched sections; identical fenced content and technical token sets;', links, 'valid local links')
'@ | python -
````

```powershell
@'
import subprocess
for suffix in ('.md','.th.md'):
    name = 'GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1' + suffix
    original = subprocess.check_output(['git','show','9889daf:docs/reports/' + name])
    backup = subprocess.check_output(['git','show',':docs/reports/backups/2026-09-06_104/' + name])
    assert backup == original, name
print('Both staged backup blobs exactly match original Git blobs.')
'@ | python -
```

```powershell
python -m unittest tests.test_repository_contract -q

git diff --check

git diff --cached --name-only

git diff --cached --check
```


## ข้อจำกัดและงานต่อ

เป็นงานเอกสารเท่านั้น ไม่ได้สร้าง CAD, physics solver, search, admitted experiment, survivor จริง ความเหนือกว่าของรถ หรือการค้นพบเทคโนโลยี ลิงก์ใน backup ที่เก็บไว้ยังอ้างบริบท `docs/reports/` เดิม ไม่มีการเขียนทับผลประวัติ ไม่เปลี่ยนโค้ด และไม่ได้รับคำขอ push

ถัดไป: implement Work 098 ตาม contract นี้ รวม acceptance cases ที่กำหนดและ registration/budget schemas ที่เป็นรูปธรรม Implementation ถัดไปต้องมีแผน validation และ commit แยก จะรายงาน final commit hash ใน handoff เพราะไม่สามารถฝัง hash ลงใน commit ของตัวเองได้

Plan deviations: none.
