# ผล Work 107: แผนละเอียดแยกรายงาน

ต้นฉบับภาษาอังกฤษ: `2026-09-07_107_detailed-work-package-plans-result.md`

เริ่ม: 2026-09-07 ดำเนินการต่อ/วันที่ผล: 2026-09-09 (Asia/Bangkok)

Status: Completed

## ผลและขอบเขตที่แน่นอน

ขยาย Work 106 เป็น [แผนละเอียดแยก 26 งาน](../plans/detailed_part_to_vehicle_v1/README.th.md) แต่ละงานมีคู่ภาษาอังกฤษ Work 107 จริงเป็นงานเอกสารนี้ จึงเทียบ packages ที่เคยเสนอเป็น 107–132 ไปเป็น Works 108–133 สำหรับพัฒนาอย่างชัดเจน ไม่เขียน roadmap หรือ work logs ประวัติใหม่

เปลี่ยนเฉพาะ Markdown 58 ไฟล์: แผนรายงาน 52 ไฟล์ ดัชนีสองไฟล์ และ plan/result ของ Work 107 สี่ไฟล์ ไม่เปลี่ยน runtime source, tests, configurations, dependencies, ผลทดลองที่สร้าง หรือฮาร์ดแวร์จริง paths โมดูลและ CLI ที่พิมพ์เป็นจุดแบ่ง implementation ที่เสนอ ไม่ใช่ความสามารถที่มีและรันได้แล้ว

## เนื้อหาและการตัดสินใจ

ทุก package มีเก้าหัวข้อเลขกำกับ: ผล/ข้อมูลเข้า ไฟล์ที่เสนอ ขั้นพัฒนาตามลำดับสี่ขั้น IV/DV/controls tests/การหักล้างเฉพาะเรื่อง numerical registration/เกณฑ์รับ artifacts/งานรับต่อ ความเสี่ยง/สิ่งที่ไม่ทำ และคำสั่ง validation/replay ที่เสนอ

ดัชนีมีข้อกำหนด execution/evidence ร่วม prerequisites ช่องตัวเลขที่ต้องเติมก่อน admitted execution และตารางเทียบเลขเดิม–ใหม่ dependency ตามความสามารถเปิดให้เริ่ม B-rep meshing, interfaces และ co-design ย่อยตั้งแต่ต้น โดยไม่อ้างว่าส่วนที่ขาดครบแล้ว โปรแกรม solver หรือทดสอบของจริงที่ใหญ่ต้องแยกเป็น execution works ขอบเขตจำกัดเมื่อจำเป็น

หลักที่รักษา: shape/topology อิสระ fields ที่มาจาก geometry, hardware ภายในละเอียด ไม่มีทรัพยากรอุดมคติฟรี การนับเนื้อวัสดุจริง ผลมีประโยชน์แม้ topology เดิม early exploratory integration, แบบลดรูปตามขอบเขต ต้นทุนครบ fair controls และหลักฐาน unresolved ชัดเจน งานจริง Works 131–133 ต้องอนุญาตและ qualified review แยก runners ที่เสนอวิเคราะห์ข้อมูลบันทึกแบบ offline เท่านั้น

## คำสั่งตรวจสอบ

Repository contract gate:

```powershell
python -m unittest tests.test_repository_contract -v
```

Plan integrity gate แบบอ่านอย่างเดียว:

```powershell
$workPlanCheck = @'
import re
from pathlib import Path
root = Path.cwd()
directory = root / 'docs/plans/detailed_part_to_vehicle_v1'
english = sorted(p for p in directory.glob('work*.md') if not p.name.endswith('.th.md'))
assert len(english) == 26
ids = [int(re.match(r'work(\d+)-', p.name).group(1)) for p in english]
assert ids == list(range(108, 134)), ids
graph = {}
for p in english:
    pair = [p, p.with_name(p.stem + '.th.md')]
    texts = [q.read_text(encoding='utf-8') for q in pair]
    number = int(re.match(r'work(\d+)-', p.name).group(1))
    assert f'Original Work 106 package: {number - 1}' in texts[0]
    assert f'`{p.name}`' in texts[1]
    for text in texts:
        assert 'Status: Planned' in text
        assert re.findall(r'^## (\d+)\.', text, re.M) == list(map(str, range(1, 10)))
        assert len(re.findall(r'^\d+\. ', text, re.M)) == 4
        for label in ('IV:', 'DV:', 'Controls:'):
            assert label in text
    literals = [set(re.findall(r'(?<!`)`([^`\n]+)`(?!`)', t)) - {q.name for q in pair} for t in texts]
    assert literals[0] == literals[1], (p.name, literals[0] ^ literals[1])
    commands = [re.findall(r'```powershell\n(.*?)```', t, re.S) for t in texts]
    assert commands[0] == commands[1] and len(commands[0]) == 1, p.name
    dep_line = re.search(r'^Dependencies: (.*)$', texts[0], re.M).group(1)
    graph[number] = [int(v) for v in re.findall(r'Work (\d+)', dep_line)]
    th_dep_line = re.search(r'^พึ่งพา: (.*)$', texts[1], re.M).group(1)
    assert graph[number] == [int(v) for v in re.findall(r'Work (\d+)', th_dep_line)]
    assert all(d in ids and d != number for d in graph[number])
visited, active = set(), set()
def visit(node):
    assert node not in active, f'dependency cycle: {node}'
    if node in visited:
        return
    active.add(node)
    for dep in graph[node]:
        visit(dep)
    active.remove(node)
    visited.add(node)
for node in ids:
    visit(node)
for index in (directory / 'README.md', directory / 'README.th.md'):
    rows = re.findall(r'^\| (\d+) \| (\d+) \|', index.read_text(encoding='utf-8'), re.M)
    assert rows == [(str(n), str(n-1)) for n in ids]
for p in directory.glob('*.md'):
    text = p.read_text(encoding='utf-8')
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        if not target.startswith('https://'):
            assert (p.parent / target.split('#')[0]).resolve().is_file(), (p.name, target)
print('PASS: 26 paired plans; 9 sections and 4 steps each; matching literals/CLI/dependencies; valid numbering, DAG and local links')
'@
python -c $workPlanCheck
```

ผล validation: ทั้งสองคำสั่ง exit `0` Repository output: `Ran 6 tests`; `OK` Integrity output: `PASS: 26 paired plans; 9 sections and 4 steps each; matching literals/CLI/dependencies; valid numbering, DAG and local links` รันทั้งสองซ้ำหลังแก้ formatting ไม่รัน full physics suite ซ้ำเพราะงานนี้เปลี่ยนเฉพาะเอกสาร

`git diff --cached --check` ครั้งแรก exit `1` รายงาน `new blank line at EOF` ในเอกสารที่สร้าง 56 ไฟล์ จึงหยุด commit ลบเฉพาะบรรทัดว่างท้ายไฟล์ด้วย patches, restage ไฟล์เดิมที่ระบุชัด และรัน gate ซ้ำ: exit `0` ไม่มี output คำเตือน LF-to-CRLF ของ working copy จาก Git ไม่ได้เปลี่ยนเนื้อหาที่ตั้งใจหรือทำให้ผ่อน whitespace gate

## การอ่านทบทวนและข้อจำกัด

อ่านแต่ละ package เทียบ roadmap ต้นทาง functional dependencies เงื่อนไขเริ่ม และเจตนาการหักล้าง ไม่ยืนยันว่างานอนาคตใดสำเร็จทางวิทยาศาสตร์ การตรวจแผนยืนยัน implementation CAD, meshing, contact, material, energy, flow หรือรถในอนาคตไม่ได้

ค่า tolerances, sample sizes, compute allocations, backend และ safe operating bounds ของจริงต้องใช้ pilots ที่เปิดเผย ข้อมูลที่รับได้ และ execution registrations ที่ล็อก ไม่สัญญาการรองรับรูปทรงทั้งหมด วันเสร็จ ชนะสมรรถนะ ความพร้อมผลิต หรือ physical validation

## Commit และงานต่อ

stage paths งานนี้ที่ระบุชัดทั้ง 58 ไฟล์ เทียบ `git diff --cached --name-only` กับรายการที่คาด: ตรงทั้งหมด ไม่มีไฟล์อื่น `git diff --check` และ `git diff --cached --check` หลังแก้ exit `0`; `git diff --cached --shortstat` ยืนยันเพิ่ม Markdown 58 ไฟล์ การแก้สถานะสุดท้ายจะ restage และตรวจซ้ำทันทีก่อน commit

คำสั่ง commit: `git commit -m "docs: expand detailed part-to-vehicle work plans"` ตรวจด้วย `git log -1 --oneline`, `git show --shortstat --oneline HEAD` และ `git status --short`; รายงาน hash ที่ตรวจแล้วในข้อความส่งมอบหลังสำเร็จ ไม่ push หรือเขียนประวัติใหม่

งานพัฒนาถัดไป: Work 108 ที่เสนอ การนับเนื้อวัสดุ/ช่องว่างและหลักฐาน mass properties จาก CAD จริง ทุก execution อนาคตต้องมีแผน/ผลสองภาษาลงวันที่ของตน physical-law tests เมื่อเกี่ยวข้อง และ validated commit
