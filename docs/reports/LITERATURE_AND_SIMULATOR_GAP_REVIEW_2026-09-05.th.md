# Formula Ultimate: ทบทวนงานวิจัยและช่องว่างของซิม

ต้นฉบับภาษาอังกฤษ: `LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.md`

วันที่ประเมิน: 2026-09-05 ตรวจจาก revision เริ่มต้น `251ede5` Work 102 เป็นการทบทวนเอกสาร/งานวิจัย ไม่ใช่การทดลองใหม่

## ผลประเมิน

**Formula Ultimate มีโครงระบบวิจัยสำหรับค้นหาแบบภายใต้ฟิสิกส์ที่มีเนื้อหาและทดสอบได้แล้ว แต่ยังไม่ใช่ซิมแข่งขันของรถทั้งคันที่ยืนยันกับโลกจริงแล้ว** สิ่งที่มีหลักฐานเด่นคือการตามที่มาผล การบันทึกเหตุคัดทิ้ง การ replay และการตรวจเชิงคำนวณภายในขอบเขต ช่องว่างใหญ่ที่สุดคือหลักฐานฟิสิกส์อิสระ การนำ geometry จริงไปแก้สนามแรง/การเสียรูป การทำนายรถแบบ transient ที่เชื่อมระบบครบ และการหากลไกกับตัวควบคุมร่วมกัน

โค้ดก้าวหน้ากว่าคำอธิบาย longitudinal ระยะแรกใน README: มี planar, vertical, drivetrain, control, aero-map, thermal และงานกลไก/CAD แล้ว แต่การมีโมดูลเหล่านี้ไม่ได้แปลว่าทุกส่วนทำงานร่วมกันในซิมการแข่งขันที่ตรวจความตรงแล้ว

[แค็ตตาล็อก](../research/RELATED_WORK_CATALOG_2026-09-05.th.md) รวม 62 งานวิชาการและ 8 แหล่งอุตสาหกรรม/เครื่องมือทางการ พร้อมประโยชน์ ข้อจำกัด และระดับที่อ่าน การประเมินนี้คงเป้าหมาย geometry อิสระและพลังงานที่เป็นกลางต่อเทคโนโลยีของโครงการ รถ F1 แบบปกติใช้เป็น baseline เปรียบเทียบ ไม่ใช่รูปแบบที่ทุกคำตอบต้องเป็น

## หลักฐานปัจจุบัน: สิ่งที่ผ่านจริง

| หลักฐาน | ผลที่พบ | สิ่งที่ยืนยันได้ / ยังยืนยันไม่ได้ |
| --- | --- | --- |
| ชุดทดสอบปัจจุบัน | `python -m unittest discover -s tests -q`: 689 tests ใน 285.212 s, exit 0, ข้าม 7 tests | เป็นหลักฐาน regression ของซอฟต์แวร์ การข้าม tests และการผ่านชุดนี้ไม่ได้ยืนยันฟิสิกส์โลกจริง |
| [FU-BMC-003 / Work 062](../research/BOUNDED_MAIN_CAMPAIGN_V3_RESULT.th.md) | 2,880 attempts, 36 streams, 12 paired seeds, 960 attempts ต่อ treatment; feasible 2,107 และ structural failures 773 | มีแคมเปญค้นหาที่ควบคุมโอกาสประเมินจริง แต่ยังไม่ใช่การค้นพบรถทั้งคันแบบปลายเปิด |
| แบบที่เลื่อนด่านในแคมเปญเดียวกัน | ผ่าน holdout 72 แบบ; ผ่าน refinement 51; ไม่ผ่าน 21 เป็น `refined_disagreement`; 51 แบบมี STEP สี่ solids ที่ผ่าน FreeCAD | 21/72 = **29.17%** ของแบบที่รอด Level-0 และเลื่อนด่าน ตกเมื่อ refine อัตรานี้มีเงื่อนไข ไม่ใช่ false-positive rate ของข้อเสนอทั้ง 2,880 แบบ |
| ผลเทียบวิธีค้นหา | EVOLUTION กับ RANDOM ต่างด้าน supported-finisher rate +0.1667; exact McNemar p = 0.5 ส่วน 9 seeds ที่ทั้งคู่สำเร็จ median best-time difference -2.232959 s; sign-flip p = 0.0625 | ทิศทางผลที่พบเป็นบวก แต่ยังพิสูจน์ความเหนือกว่าที่ 0.05 ไม่ได้ grammar ห้าตัวแปรและการเลือกเฉพาะ seed ที่ทั้งคู่สำเร็จจำกัดการขยายข้อสรุป |
| [Work 076 integrated lap](../research/INTEGRATED_LEVEL0_LAP_GATE_V1.th.md) | วงกลมสังเคราะห์รัศมี 50 m; เวลารอบ 22.14108931044568 s; throttle คงที่ 0.3; dt = 0.005 s | สาธิตการเลี้ยวแบบ closed-loop และพลศาสตร์ที่เชื่อมกันบนวงกลมเชิงวิเคราะห์ ยังไม่ใช่เวลารอบต่ำสุดของสนามจริงหรือการแข่งขันเต็มรูปแบบ |
| [Work 088 admission audit](../work_logs/2026-09-04_088_whole-mechanical-vehicle-candidate-001-result.th.md) | `audit_status=passed`, `candidate_verdict=not_ready`; มี artifact classes 13/13; ประเมิน cases 11/11; ready 0/11 | ระบบ audit ทำงานและปฏิเสธแบบอย่างถูกต้อง งาน audit เสร็จไม่เท่ากับรถเสร็จ |
| [Work 097 benchmarks](../work_logs/2026-09-05_097_generalized-meshing-contact-failure-evaluation-result.th.md) | adapters แบบจำกัดขอบเขต 7 แบบ; fine relative error สูงสุด 0.0014270788520555852; last-two change สูงสุด 0.0042775693130952114 | แสดงการเห็นตรงกัน/การ refine ของโมเดลลดรูป ไม่ใช่ nonlinear finite-element 3D ที่สร้างจาก STEP อิสระทั่วไป |

ตรวจ `artifacts/work088/run_a/result.json` และ `artifacts/work097/run_a/result.json` ที่เก็บไว้เทียบกับโค้ดและบันทึกแล้ว ไม่ได้สร้างผลใหม่ Work 088 ระบุ `not_run_pre_admission_blocked` ส่วน Work 097 ระบุ `design_use_allowed=false` และ `arbitrary_3d_nonlinear_contact_solved=false`

สิ่งที่ขวางกลไก Work 088 เป็นรูปธรรม: มีคู่ชิ้นส่วนทับกันเป็นปริมาตร 8 คู่ และระยะห่างเป็นศูนย์อีก 1 คู่; การเคลื่อนช่วงล่างทำให้คลาดแนว 0.007 m เทียบ tolerance ของ rigid interface ที่ 0.000001 m; โครงรับแรงใหม่ยังไม่มีหลักฐาน mesh convergence; ข้อมูลวัสดุ/กระบวนการยังเป็น synthetic ต้องจัดการสิ่งเหล่านี้ก่อนอ้างว่าแบบนี้แข่งจบได้

## จุดที่พบในโค้ดและมีผลต่อความน่าเชื่อถือมากที่สุด

ใน [generalized_geometry_benchmarks.py](../../src/formula_ultimate/structural/generalized_geometry_benchmarks.py) บรรทัด 144–194 ทั้ง reference และ discrete path ลด geometry เหลือค่าสเกลาร์จากหน้าตัดที่สุ่มตรวจ แล้วใช้คำตอบเชิงวิเคราะห์หรือ quadrature บรรทัด 193–194 สร้างค่าแบบนี้:

```text
force residual = abs(load + (-load)) / scale
moment residual = abs(torque + (-torque)) / scale
stiffness = generalized_load / response
external = 0.5 * generalized_load * response
internal = 0.5 * stiffness * response**2
solver_converged = True
```

แรงและโมเมนต์หักล้างกันเองตั้งแต่ตั้งสูตร ส่วนพลังงานเท่ากันตามนิยาม stiffness ที่เพิ่งสร้าง จึงไม่ได้วัดปฏิกิริยารองรับที่กู้คืนอย่างอิสระ หรือสนาม stress/displacement 3D ที่แก้ได้จริง การ refine ค่า response ยังมีประโยชน์เป็นการตรวจเชิงตัวเลขเฉพาะขอบเขต แต่ residual เหล่านี้และธง convergence ที่ให้ True เสมอใช้เติมหลักฐานสมดุลอิสระที่ขาดไม่ได้ การมี negative controls ที่ถูกปฏิเสธไม่ได้ลบข้อจำกัดนี้

ข้อสังเกตนี้จำกัดเฉพาะ adapter ดังกล่าว แคมเปญเก่าเรียก CalculiX จริงผ่าน [campaign_physics.py](../../src/formula_ultimate/experiments/campaign_physics.py) จึงไม่ควรลบคุณค่าหรือบอกว่าไม่มี solver เลย ต้องแยกหลักฐาน solver จริงของโจทย์คานแบบจำกัด ออกจาก evaluator ทั่วไปสำหรับ geometry solid ใหม่

ก่อน Work 100 เลื่อนกลไกแปลกใหม่ขึ้นเป็นผลค้นพบ ควรมีเส้นทาง mesh/solver จริงสำหรับชนิด geometry ที่อนุญาต ดึง reactions, residual histories, stress/displacement fields และ failure states อย่างอิสระ โดยเก็บการตรวจลดรูปเดิมเป็นด่าน fidelity ต่ำไว้ได้ [P28](https://orbi.uliege.be/handle/2268/22742?locale=en), [P29](https://github.com/ipc-sim/IPC), [P59](https://www.sciencedirect.com/science/article/pii/S0376042102000052)

## ตามหลังซิม F1 แค่ไหน?

**ยังไม่มีหลักฐานให้ตอบเป็นเปอร์เซ็นต์ จำนวนปี หรืออัตราส่วนความผิดพลาดเวลารอบที่เทียบตรงกันได้** เราไม่ได้รันรถ สนาม อินพุต และเกณฑ์วัดเดียวกับทีม F1 อีกทั้งทีมไม่ได้เปิด error budget เชิงตัวเลขครบระบบ จำนวนฟีเจอร์ tests หรือรอบจำลองใช้สร้างตัวเลขเทียบนี้ไม่ได้

ข้อมูล F1 สาธารณะแสดงกระบวนการที่รวม computer models, driver-in-loop และการเทียบกับข้อมูลรถ/สนามจริง สมรรถนะ motion ของซิมคนขับเป็นคนละคุณสมบัติกับความแม่นของโมเดลรถ [Mercedes I01](https://www.mercedesamgf1.com/news/how-does-f1-simulation-work), [McLaren I02](https://www.mclaren.com/racing/latest-news/mclarenracing/article/secrets-formula-1-simulator/), [Formula 1 I05](https://www.formula1.com/en/latest/article/smedley-what-is-correlation.3gcOwCLuQ7rxk4bNeBKf1p), [Dynisma I03](https://www.dynisma.com/news/dynisma-completes-scuderia-ferrari-mission-winnows-new-simulator)

ระยะห่างที่อธิบายได้อย่างมีประโยชน์คือ **ยังขาดการผ่านหลักฐานอีกหลายขั้น**: โมเดลที่เชื่อมกันและรันได้ → benchmark เชิงตัวเลขอิสระที่ converge → โมดูลที่สอบเทียบและทดสอบกับเงื่อนไขจริงที่ไม่เคยใช้ fit → โมเดลรถทั้งคัน/การแข่งขันที่เทียบกับของจริงแล้ว บางโมดูลของเรามีบางส่วนของสองขั้นแรก แต่ candidate รถทั้งคันที่ตรวจยังไม่ผ่าน admission ข้อมูล F1 แสดงว่ามีกระบวนการ correlation กับรถจริง โดยยังใช้ให้คะแนนทุกทีมด้วยมาตรวัดสากลเดียวกันไม่ได้

เป้าหมายกลางที่เข้าถึงและทำซ้ำได้ง่ายกว่าคือซิมแข่งในงานวิชาการเปิด งาน GP2 เชื่อม transient 14-DOF, nonlinear tyres, แอโรตาม ride height และการเทียบ telemetry แล้ว ส่วนงาน fidelity ablation ทดสอบการลดรูปกับข้อมูลรถแข่งอัตโนมัติจริง ทั้งคู่แสดงความสามารถที่หลักฐาน integrated ปัจจุบันของเรายังไม่มี แต่ปีตีพิมพ์ไม่ได้แปลว่าโครงการเราล่าช้าเป็นจำนวนปีเท่านั้น [P34](https://eprints.soton.ac.uk/417133/), [P42](https://arxiv.org/abs/2602.07984)

## ตารางช่องว่างและลำดับความสำคัญ

A = ขวางการอ้างผลค้นพบ/การแข่งขันที่น่าเชื่อถือในตอนนี้; B = เพิ่ม fidelity หลัง baseline ผ่าน admission; C = ระยะหลังหรือตามความจำเป็น

| ด้าน | สิ่งที่พบว่ามีแล้ว | ความสามารถ/หลักฐานที่ขาดและผลกระทบ | ลำดับ / แหล่ง |
| --- | --- | --- | --- |
| Geometry สู่กลศาสตร์ | กราฟ CAD, witnesses, ตรวจ STEP, คาน CalculiX แบบจำกัด และ adapters ลดรูป 7 แบบ | mesh geometry อิสระที่ยอมรับจริง ส่ง boundary conditions อย่างถูกต้อง ตรวจ field convergence, reactions และ local failure อิสระ มิฉะนั้นการค้นหาอาจชนะช่องโหว่ proxy | A — P26–P30, P59 |
| ประกอบกลไก | บันทึก admission ของ Work 088 ครบ | แก้ชิ้นส่วนทับกัน interface ที่เคลื่อนได้ หลักฐาน mesh โครงรับแรง และสมบัติวัสดุ/กระบวนการจริง ปัจจุบัน `not_ready` | A — Work 088 |
| ยาง/contact | [Friction envelope](../../src/formula_ultimate/physics/tyre.py) และ [positive longitudinal slip/tanh](../../src/formula_ultimate/simulation/drive_ground_coupling.py) บรรทัด 300–303 | combined slip, load sensitivity, camber, relaxation และขอบเขตแรงดัน/อุณหภูมิที่สอบเทียบ ค่า friction คงที่ไม่พอยืนยันอันดับเวลารอบใกล้ขีดจำกัด แต่กล่าวว่าไม่มี slip model เลยก็ไม่ถูก | A — P43–P46, P61, I07–I08 |
| แอโร | [Maps](../../src/formula_ultimate/physics/aerodynamics.py) ตาม speed, ride height, yaw, active state และ metadata แรง/โมเมนต์/cooling | ในเส้นทางที่ตรวจยังไม่สาธิต pipeline geometry ใหม่ → CFD → map ที่ตรวจแล้ว ต้องมีหลักฐาน geometry, aero balance และ cooling; enum `cfd` หรือ `measured` ไม่ได้สร้างหลักฐานให้เอง | A/B — P35, P47–P53 |
| เชื่อมพลศาสตร์รถ | [Work 076](../../src/formula_ultimate/simulation/integrated_lap_gate.py) เชื่อม steering, planar/drivetrain/vertical | ผล tyre/aero/suspension/power/brake/thermal พร้อมกันที่ตรวจแล้ว การเคลื่อน transient สมดุลแรง/โมเมนต์และความไวต่อ time step การผ่านแต่ละโมดูลแยกไม่พิสูจน์ทั้งระบบ | A — P34–P35, P42, P55 |
| สนาม | วงกลมเชิงวิเคราะห์และ[คำอธิบายสนามมีแหล่งอ้างอิง](../research/REAL_CIRCUIT_SOURCE_REPORT.th.md) | สนามตามตำแหน่งที่มีความกว้าง ความสูง การเอียง ผิวทางและความไม่แน่นอน พร้อม lap solver ที่รู้ขอบเขต ความยาว/ระดับความต้องการสนามไม่ใช่ผิวถนน 3D | A — P32–P33, I04 |
| หาวิธีขับที่เหมาะสม | ควบคุม heading/cross-track และรอบ throttle คงที่ | หา speed, braking, steering และ energy policy ที่ดีให้แต่ละแบบอย่างเท่าเทียม พร้อมงบฝึก/solve ตัวควบคุม คนขับจำลองที่อ่อนอาจทำให้กลไกดีดูแย่ | A — P03, P31, P39, P41, P62 |
| พลังงานและความทนทาน | บัญชี powertrain, [lumped thermal model](../../src/formula_ultimate/physics/thermal.py), derating/failure | เชื่อมขีดจำกัดความร้อน/พลังงานตลอดช่วงแข่ง cooling และเกณฑ์แข่งจบที่ทำซ้ำได้ ต่อไปจึงเพิ่มยางสึก fatigue และ robustness รอบเดียวเร็วอาจแข่งไม่จบ | A สำหรับ finish gate; B สำหรับโมเดลละเอียดขึ้น — P36–P38, P46 |
| การค้นหาและความใหม่ | แคมเปญแบบจำกัด เครื่องมือ geometry/topology และแผน QD | ความหลากหลายที่มีความหมายทางกล การค้นหา topology/controller ร่วมกัน baseline ที่ optimize แล้ว และบัญชี compute ครบ ผลห้าสเกลาร์ยังไม่ใช่หลักฐานค้นพบแบบปลายเปิด | A — P03, P09, P11–P16 |
| ข้อมูลและความไม่แน่นอน | Replay, provenance, เหตุปฏิเสธแบบ | ข้อมูลโมดูลที่วัดจริง การระบุพารามิเตอร์ ความไม่แน่นอนการวัด เงื่อนไข holdout, model discrepancy และความคงที่ของอันดับ เป็นช่องว่างใหญ่ที่สุดต่อการใช้ทำนายทางวิศวกรรม | A — P17, P42, P58–P60 |
| Real time / คนขับจริง | time step เชิงตัวเลขและซิม deterministic | วัด deadline, latency/jitter, controls/force feedback, motion และ human correlation หากต้องการ driver-in-loop มีคุณค่าทันทีต่ำกว่าสำหรับ autonomous discovery | C — I01–I04 |
| สภาพการแข่งขัน | โจทย์/holdout แบบจำกัด | ต่อไปอาจเพิ่ม traffic/wake, weather, ผิวทางเปลี่ยน และกลยุทธ์หลาย stint ตามคำถามวิจัย ควรเพิ่มหลังโจทย์แข่งควบคุมผ่าน validation | B/C — P18–P19, P38, P40 |

time step ของ Work 076 เทียบเท่า **การสุ่มเวลาเชิงตัวเลข 200 Hz** ไม่ใช่ throughput แบบ real-time ที่วัดแล้ว ส่วน **สูงสุด 5 kHz** และรายละเอียดผิวทางแนวราบ/แนวดิ่ง **1 cm / 1 mm** ของ rFpro เป็นสเปกโมดูลผู้ขาย การนำ 5,000 หาร 200 จึงบอกว่าเราตามหลัง 25 เท่าไม่ได้ [I04](https://rfpro.com/simulation-software/terrain-server/)

## งานวิจัยที่ใกล้เป้าหมายจริงของเรา

ต้องเชื่อมงานสามกลุ่ม:

1. **ค้นหากลไกพร้อมตัวควบคุม:** RoboGrammar, multi-objective graph search, Neural Graph Evolution, DERL และ Evolution Gym ใกล้สิ่งที่เราต้องการให้ระบบทำมากกว่าซิมเวลารอบของรถรูปแบบตายตัว แต่แต่ละงานยังจำกัดร่างกาย ชิ้นส่วน หรือสภาพแวดล้อม P01–P10
2. **ใช้ compute กับแบบที่น่าเชื่อถือและหลากหลาย:** MAP-Elites, surrogate-assisted illumination, multifidelity optimization และ transferability ตรงกับ Works 098–100 และช่วยป้องกันการ optimize ชนะ proxy ที่ไม่ตรง P11–P17
3. **ทำนายและตรวจพฤติกรรมการแข่งขัน:** โมเดล optimal-control GP2/F1, aero-suspension, ยาง/transient/thermal, การทดลอง CFD และ uncertainty calibration กลุ่มนี้เติม evaluator ไม่ใช่ตัวแทนแบบสำหรับค้นหา P31–P59

ตัวอย่างยานพาหนะนอกกรอบที่ใกล้มากคืองานปี 2026 ที่แข่งหุ่นยนต์สี่ขาติดล้อ ผู้วิจัยรายงานการทดลอง active roll จริงว่าลด mean load-transfer ratio สูงสุด 44% และปรับปรุง fastest lap time 8.7% ตัวเลขเป็นของหุ่นยนต์และ baseline นั้น สนับสนุนการศึกษากลไก active แปลกใหม่ แต่ขยายเป็นสมรรถนะ F1 หรือบอกว่าบทความค้นพบรูปร่างเองไม่ได้ [P10](https://arxiv.org/abs/2606.26313)

ยังไม่มีบทความที่ตรวจในรอบนี้ยืนยันเป้าหมาย Formula Ultimate ครบต้นทางถึงปลายทาง ข้อนี้เป็นผลจากขอบเขตการค้น ไม่ใช่หลักฐานว่าทั่วโลกไม่มีใครทำ ความก้าวหน้าใหม่ที่ควรมุ่งพิสูจน์คือ **กระบวนการค้นพบจาก geometry สู่หลักฐาน ซึ่งค้นพบกลไกที่มีหน้าที่ต่างกัน รอดการตรวจ fidelity สูงอย่างอิสระ และปรับปรุงเป้าหมายการแข่งขันที่กำหนด ภายใต้งบออกแบบ/ควบคุมเท่าเทียมกัน** หลักฐานปัจจุบันสนับสนุนให้สร้างการศึกษานี้ต่อ ยังไม่ใช่หลักฐานว่าทำสำเร็จแล้ว

## ลำดับพัฒนาและการทดลองที่หักล้างได้

ทั้งหมดเป็นข้อเสนอ ยังไม่ได้ทดลองใน Work 102 ใช้ขยายรายละเอียด [roadmap Works 098–101](GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1.th.md) โดยไม่แก้ roadmap และไม่ถือว่า Work 097 เสร็จแปลว่า mesh แบบอิสระทุกชนิดได้แล้ว

| ลำดับ / การทดลอง | ตัวแปรต้นและตัวควบคุม | ตัวแปรตาม / ตัวชี้วัด | เกณฑ์สำเร็จและล้มเหลว |
| --- | --- | --- | --- |
| 1. Geometry evaluator อิสระ | geometry ที่ยอมรับจริง ความละเอียด mesh และวิธี solver; ตรึง SI units วัสดุ แรง boundary conditions และ identity geometry | displacement/stress, recovered reactions, residual history, contact penetration, runtime, invalid states | กำหนดกรณีเชิงวิเคราะห์/ทดลองและ tolerance ตาม uncertainty ล่วงหน้า ใช้ refinement อย่างน้อย 3 ระดับและตัวเทียบอิสระ ล้มเหลวเมื่อไม่ converge สมดุลผิดโดยอธิบายไม่ได้ ไม่มี field evidence หรือ failure/ranking เปลี่ยนเกิน error budget |
| 2. Baseline แข่งที่เชื่อมระบบ | fidelity และ time step; รถ input trace สนาม data split และ numerical tolerances เดียวกัน | traces ของ speed/yaw/load, ระยะเบรก พลังงาน อุณหภูมิ error ของ lap/sector และ runtime | สร้าง baseline เทียบโมเดลเปิดและทดสอบโมดูลกับข้อมูลจริง holdout ตรึง tolerance ก่อนเห็นผล ล้มเหลวหากเวลารอบดีแต่ traces ผิด ต้อง retune ทุก holdout หรือเปลี่ยน time step แล้วข้อสรุปกลับด้าน |
| 3. ความเป็นธรรมของแบบ/ตัวควบคุม | GRID, RANDOM, EVOLUTION แล้ว QD; baseline topology คงที่ที่ optimize แล้วเทียบ free-topology; paired seeds library ข้อจำกัด และงบรวมเดียวกัน | supported finishers, คะแนนแข่งดีที่สุดที่มีหลักฐาน diversity สัดส่วน invalid และต้นทุน controller | รายงานทุก failure และ paired uncertainty เลือกงบ seed จาก pilot variance/power planning ไม่ใช่รันที่ดีที่สุด อ้างเหนือกว่าไม่ได้หาก exact tests/intervals ไม่รองรับ หรือความได้เปรียบหายเมื่อฝึก controller เท่าเทียม |
| 4. Audit การเลื่อน fidelity | promotion policy และ fidelity; ตรึง candidate pool หรืองบ proposal ที่จับคู่ พร้อม stratified audit sampling | false positives, false negatives, rank agreement และคุณภาพ elite ที่ตรวจแล้วต่อ compute | สุ่มตรวจแบบที่คัดทิ้งด้วย ไม่ดูเฉพาะผู้รอด นับ CAD calls, solver seconds, mesh/iteration effort และ controller training ล้มเหลวหากการพลาดแบบดีหรือ fidelity bias อธิบายผลที่ดูดีได้ |
| 5. ค้นพบกลไกเฉพาะส่วนก่อนรวม | topology family และทางเลือก active/passive/control; interfaces วัสดุ/กระบวนการ พลังงาน และเป้าหมายแข่งเดียวกัน | ประโยชน์ด้านหน้าที่ การผลิตได้ การตรวจอิสระ และการถ่ายทอดข้าม loads/tracks holdout | เลื่อนเฉพาะ subsystem ที่ทำซ้ำได้และผ่าน causal ablation จากนั้นต้องผ่านการตรวจ interference/kinematics/load แบบ Work 088 ล้มเหลวหากประโยชน์มีแต่หน้าตา อยู่เฉพาะ proxy ขึ้นกับช่องโหว่บัญชีพลังงาน หรือหายเมื่อรวมระบบ |

**ลำดับอ่านก่อน:** P59/P15 เรื่องหลักฐานและ fidelity; P28 คู่กับเอกสาร solver จริงเรื่อง mesh; P34/P42 สำหรับ benchmark เชื่อมระบบ; P43/P44 เรื่องยาง; P03/P09 เรื่องค้นหาแบบ/ตัวควบคุม; P11/P13 เรื่องความหลากหลายและต้นทุน พิจารณา [Fastest-lap I06](https://github.com/juanmanzanero/fastest-lap) และ [Chrono::Vehicle P55](https://www.inderscience.com/info/inarticle.php?artid=97096) สำหรับ baseline แบบเปิดที่ทำซ้ำ ก่อนตัดสินใจเขียนโครงตัวคำนวณที่มีอยู่แล้วใหม่ทั้งหมด ควรทดสอบว่าเชื่อมเป็น adapter ได้หรือไม่

สิ่งที่ให้ประโยชน์ทันทีสูงสุดคือทำให้หลักฐาน solver อิสระมีความหมายตรง ได้ subsystem ที่ทำหน้าที่และผ่าน admission อย่างน้อยหนึ่งตัว และ baseline แข่งที่เทียบของจริงได้หนึ่งชุด แล้วจึงให้ระบบค้นหาใช้ evaluator นั้น รายละเอียดภาพ แท่น motion หรือ generator ที่อิสระขึ้นใช้แทนด่านเหล่านี้ไม่ได้

## ความมั่นใจ หลักฐานโต้แย้ง และข้อจำกัด

- **มั่นใจสูง:** สถานะ not-ready ของ Work 088, ขอบเขตวงกลม Work 076, สูตร residual ของ Work 097, ตัวเลข/สถิติแคมเปญ และผล tests มีไฟล์และโค้ดที่ตรวจรองรับ
- **มั่นใจปานกลาง:** ลำดับความสำคัญและวิธีที่ถ่ายทอดมาใช้ เป็นวิจารณญาณวิศวกรรมจากหลักฐาน ยังไม่ได้วัดผลตอบแทนต่อแรงพัฒนาเฉพาะโครงการ
- **ยังไม่ทราบ:** ความแม่นของซิม F1 ที่เป็นกรรมสิทธิ์ สถาปัตยกรรมปัจจุบันครบทุกทีม เวลา/ต้นทุนสู่ความเทียบเท่า physical lap error ของเรา และงานที่ยังค้นไม่พบครอบคลุมข้อเสนอแล้วหรือไม่
- **หลักฐานสนับสนุน:** การเก็บ failures, deterministic replay, แคมเปญ solver/CAD แบบจำกัด และธงไม่อนุญาตเลื่อนผล เป็นฐานที่มีคุณค่า
- **หลักฐานโต้แย้ง:** แบบที่เลื่อนด่านแล้ว 29.17% เห็นต่างเมื่อ refine ผลค้นหายังไม่มีนัยสำคัญ Work 088 ไม่มี case ready สมบัติ synthetic และ residual ที่สร้างให้หักล้างกันเอง จำกัดข้ออ้างที่แรงกว่านี้
- **คำอธิบายทางเลือก:** ผลดีของ evolution อาจมาจาก grammar/การจัดงบ controller หรือ bias ของ fidelity ต่ำ; solver เห็นตรงกันอาจเพราะสมมติฐานร่วม; CAD ถูกต้องยังประกอบทางกลให้ทำงานไม่ได้
- **หลักฐานที่ขาด:** ข้อมูลจริงอิสระพร้อม uncertainty, lap ที่เชื่อมระบบและสอบเทียบ, การแก้ field ของ geometry ที่ยอมรับทั่วไป และการเหนือกว่าของ free-topology ที่ทนต่อการเปลี่ยนเงื่อนไข

รันชุดทดสอบเต็มใหม่แล้ว แต่ไม่ได้รันแคมเปญย้อนหลังหรือทำซ้ำ papers/software ภายนอก การทบทวนนี้ไม่ได้แก้โค้ดฟิสิกส์ configuration ติดตั้ง solver หรือเปลี่ยนข้อผูกมัดใน roadmap
