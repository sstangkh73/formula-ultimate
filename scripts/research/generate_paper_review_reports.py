from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "docs" / "research" / "paper_library" / "sources"
MANIFEST = ROOT / "docs" / "research" / "paper_reviews" / "reading_manifest.json"
OUTPUT = MANIFEST.parent
BY_PAPER = OUTPUT / "by_paper"
CORPUS = ROOT / "artifacts" / "paper_review_corpus"


CATEGORY_GUIDANCE = {
    "OE": {
        "theme_en": "Open-ended morphology/control co-design",
        "theme_th": "การออกแบบรูปร่างและการควบคุมร่วมแบบ open-ended",
        "findings_en": [
            "Body topology, controller learning, and environment difficulty interact; evaluating a new body with an under-trained controller systematically removes potentially useful morphology.",
            "Generative encodings, graph grammars, and differentiable refinement offer different search biases. No representation is neutral, so representation coverage must itself be audited.",
            "The strongest precedents close part of the sim-to-real loop through fabrication or physical trials; virtual novelty alone is not a technology-discovery claim.",
        ],
        "findings_th": [
            "topology ของร่างกาย การเรียนรู้ตัวควบคุม และความยากของสภาพแวดล้อมมีปฏิสัมพันธ์กัน การประเมินร่างใหม่ด้วยตัวควบคุมที่ยังฝึกไม่พอจะคัดทิ้ง morphology ที่อาจมีประโยชน์อย่างเป็นระบบ",
            "generative encoding, graph grammar และ differentiable refinement มี search bias ต่างกัน ไม่มี representation ใดเป็นกลาง จึงต้อง audit coverage ของ representation ด้วย",
            "งานตัวอย่างที่แข็งแรงที่สุดปิด sim-to-real loop บางส่วนด้วยการผลิตหรือทดสอบจริง ความใหม่ในโลกเสมือนอย่างเดียวไม่ใช่ claim การค้นพบเทคโนโลยี",
        ],
        "actions_en": [
            "Add controller-allocation fairness and morphology-age protection to the Work 124 search scheduler.",
            "Compare direct, generative, graph, and continuous-refinement representations at matched compute and evaluator access.",
            "Require physical-correlation gates from Works 131-133 before promoting unconventional morphology beyond simulation.",
        ],
        "actions_th": [
            "เพิ่มความยุติธรรมในการจัดสรรการฝึกตัวควบคุมและการปกป้อง morphology ใหม่ในตัวจัดตารางค้นหาของ Work 124",
            "เปรียบเทียบ representation แบบ direct, generative, graph และ continuous refinement ด้วยงบคำนวณและสิทธิ์เข้าถึง evaluator เท่ากัน",
            "บังคับใช้ physical-correlation gate จาก Works 131-133 ก่อนเลื่อน morphology ที่ไม่ธรรมดาออกจากระดับ simulation",
        ],
    },
    "AG": {
        "theme_en": "AI agents for engineering and scientific design",
        "theme_th": "AI agent สำหรับการออกแบบวิศวกรรมและวิทยาศาสตร์",
        "findings_en": [
            "LLM agents are most useful as proposal, code, and workflow generators when paired with executable verifiers; fluent output is not engineering evidence.",
            "CAD and CAE benchmarks repeatedly expose a gap between visual plausibility or tool completion and functional, geometric, or multiphysics correctness.",
            "Search benefits from archives, reflection, and test-time candidate generation, but evaluation leakage and self-judging can manufacture apparent progress.",
        ],
        "findings_th": [
            "LLM agent มีประโยชน์สูงสุดในฐานะตัวเสนอแบบ สร้างโค้ด และจัด workflow เมื่อจับคู่กับ verifier ที่รันได้ ภาษาที่ดูน่าเชื่อไม่ใช่หลักฐานวิศวกรรม",
            "benchmark CAD และ CAE พบซ้ำ ๆ ว่าความดูสมจริงหรือการใช้เครื่องมือสำเร็จไม่เท่ากับความถูกต้องเชิงหน้าที่ เรขาคณิต หรือ multiphysics",
            "archive, reflection และการสร้าง candidate เพิ่มตอนทดสอบช่วย search ได้ แต่ evaluation leakage และการตัดสินตัวเองอาจสร้างภาพความก้าวหน้าปลอม",
        ],
        "actions_en": [
            "Keep agents outside the authority boundary: they may propose artifacts, but deterministic geometry, physics, provenance, and test gates decide admission.",
            "Add CAD/CAE task suites with hidden negative controls, exact artifact checks, and failure localization rather than natural-language grading.",
            "Record prompts, tool versions, retries, token/compute cost, and verifier outcomes in the experiment ledger.",
        ],
        "actions_th": [
            "ไม่ให้ agent มีอำนาจตัดสิน admission: agent เสนอ artifact ได้ แต่ gate ด้าน geometry, physics, provenance และ test ที่ deterministic เป็นผู้ตัดสิน",
            "เพิ่มชุดงาน CAD/CAE ที่มี hidden negative control การตรวจ artifact จริง และการระบุตำแหน่งความล้มเหลว แทนการให้คะแนนด้วยภาษาธรรมชาติ",
            "บันทึก prompt, เวอร์ชันเครื่องมือ, retry, ค่า token/compute และผล verifier ใน experiment ledger",
        ],
    },
    "QD": {
        "theme_en": "Quality-diversity, novelty, surrogate, and multifidelity search",
        "theme_th": "quality-diversity, novelty, surrogate และการค้นหาแบบ multifidelity",
        "findings_en": [
            "QD methods separate finding one optimum from illuminating many high-quality niches; descriptor choice determines what diversity is visible.",
            "Surrogate and multifidelity methods save expensive evaluations only when uncertainty, fidelity discrepancy, and false-negative audits are explicit.",
            "Novelty can unlock stepping stones, but novelty without feasibility and external task holdouts does not establish useful discovery.",
        ],
        "findings_th": [
            "วิธี QD แยกการหาคำตอบดีที่สุดหนึ่งแบบออกจากการส่องให้เห็นหลาย niche ที่มีคุณภาพ ตัวเลือก descriptor เป็นตัวกำหนดว่าความหลากหลายแบบใดมองเห็นได้",
            "surrogate และ multifidelity ลดการประเมินราคาแพงได้ต่อเมื่อระบุ uncertainty, fidelity discrepancy และ false-negative audit ชัดเจน",
            "novelty ช่วยเปิด stepping stone ได้ แต่ novelty ที่ไม่มี feasibility และ external-task holdout ไม่ยืนยันการค้นพบที่มีประโยชน์",
        ],
        "actions_en": [
            "Implement descriptor-versioned archives and report archive coverage, QD score, feasible coverage, and descriptor occupancy separately.",
            "Use registered multifidelity promotion with stratified proxy audits and `not_estimable` outcomes for unresolved high-fidelity labels.",
            "Budget-match QD, objective optimization, random search, and fixed-topology baselines across seeds.",
        ],
        "actions_th": [
            "ใช้ archive ที่ version descriptor และรายงาน archive coverage, QD score, feasible coverage และ descriptor occupancy แยกกัน",
            "ใช้การเลื่อน fidelity ที่ลงทะเบียนล่วงหน้า พร้อม stratified proxy audit และผล `not_estimable` สำหรับ label fidelity สูงที่ยังไม่ทราบ",
            "จับคู่งบ QD, objective optimization, random search และ fixed-topology baseline ข้าม seed",
        ],
    },
    "CAD": {
        "theme_en": "CAD, B-rep, assemblies, and geometry generation",
        "theme_th": "CAD, B-rep, assembly และการสร้างเรขาคณิต",
        "findings_en": [
            "CAD generation must preserve construction semantics, topology, constraints, and editability; image similarity or point-cloud proximity misses functional defects.",
            "B-rep and assembly learning depend on explicit face-edge-loop and mating relationships, not unordered geometry alone.",
            "Execution-guided and verifier-guided generation improves validity, but does not replace tolerance, interference, material, or load-path evidence.",
        ],
        "findings_th": [
            "การสร้าง CAD ต้องรักษา construction semantics, topology, constraint และความแก้ไขได้ ความคล้ายของภาพหรือระยะ point cloud มองไม่เห็น defect เชิงหน้าที่",
            "การเรียนรู้ B-rep และ assembly ต้องใช้ความสัมพันธ์ face-edge-loop และ mating ที่ชัดเจน ไม่ใช่เรขาคณิตไร้ลำดับอย่างเดียว",
            "generation ที่มี execution/verifier ช่วยเพิ่ม validity แต่ไม่แทนหลักฐาน tolerance, interference, material หรือ load path",
        ],
        "actions_en": [
            "Extend the Work 138 geometry-general evaluator with semantic topology, constraint, editability, and assembly-mate checks.",
            "Maintain exact geometry-to-mesh-to-reduced-model revision identity and quantify every adapter discrepancy.",
            "Score generated CAD on physical and manufacturing tasks, not render similarity.",
        ],
        "actions_th": [
            "ขยาย geometry-general evaluator ของ Work 138 ด้วยการตรวจ semantic topology, constraint, editability และ assembly mate",
            "รักษา revision identity จาก geometry ไป mesh ไป reduced model และวัด discrepancy ของ adapter ทุกจุด",
            "ให้คะแนน CAD ที่สร้างจากงานฟิสิกส์และการผลิต ไม่ใช่ความคล้ายของภาพ render",
        ],
    },
    "ST": {
        "theme_en": "Structures, meshing, contact, and topology optimization",
        "theme_th": "โครงสร้าง meshing contact และ topology optimization",
        "findings_en": [
            "Structural credibility depends on equilibrium, discretization, constitutive assumptions, contact treatment, and convergence rather than a single stress scalar.",
            "Topology optimization can create useful material layouts, but filters, length scales, manufacturing constraints, and mesh dependence strongly shape the result.",
            "Robust contact methods treat penetration, friction, solver failure, and non-convergence as observable outcomes.",
        ],
        "findings_th": [
            "ความน่าเชื่อถือเชิงโครงสร้างขึ้นกับ equilibrium, discretization, constitutive assumption, contact treatment และ convergence ไม่ใช่ค่า stress เดี่ยว",
            "topology optimization สร้างการวางวัสดุที่มีประโยชน์ได้ แต่ filter, length scale, ข้อจำกัดการผลิต และ mesh dependence กำหนดผลอย่างมาก",
            "วิธี contact ที่น่าเชื่อถือถือ penetration, friction, solver failure และ non-convergence เป็นผลที่สังเกตได้",
        ],
        "actions_en": [
            "Promote only field solutions with independently recovered reactions, residual histories, failure locations, and at least three registered refinement levels.",
            "Add contact/mesh failure taxonomies and prevent geometry healing from silently changing candidate identity.",
            "Carry manufacturing length scales and uncertainty into structural search instead of applying them after optimization.",
        ],
        "actions_th": [
            "เลื่อนเฉพาะ field solution ที่มี reaction ที่กู้คืนอย่างอิสระ residual history ตำแหน่งพัง และ refinement อย่างน้อยสามระดับที่ลงทะเบียนไว้",
            "เพิ่ม taxonomy ของ contact/mesh failure และห้าม geometry healing เปลี่ยน candidate identity อย่างเงียบ ๆ",
            "นำ manufacturing length scale และ uncertainty เข้า structural search ไม่ใช่ใส่หลัง optimize",
        ],
    },
    "SI": {
        "theme_en": "Simulation infrastructure and differentiable physics",
        "theme_th": "โครงสร้างพื้นฐาน simulation และ differentiable physics",
        "findings_en": [
            "Fast differentiable and GPU simulators enable co-design scale, but gradient availability is not evidence of model applicability.",
            "Contact, deformables, rigid bodies, and multiphysics each impose different numerical failure modes and validation duties.",
            "Simulator benchmarks are meaningful only with disclosed hardware, tolerances, time-step sensitivity, and accuracy-cost trade-offs.",
        ],
        "findings_th": [
            "simulator แบบ differentiable และ GPU ที่เร็วทำให้ co-design ขนาดใหญ่เป็นไปได้ แต่การมี gradient ไม่ใช่หลักฐานว่า model ใช้ได้กับโจทย์",
            "contact, deformable, rigid body และ multiphysics มีรูปแบบความล้มเหลวเชิงตัวเลขและภาระ validation ต่างกัน",
            "benchmark simulator มีความหมายเมื่อเปิดเผย hardware, tolerance, time-step sensitivity และ trade-off ระหว่างความแม่นกับต้นทุน",
        ],
        "actions_en": [
            "Create evaluator applicability records per candidate class and treat solver/gradient failure as first-class ledger outcomes.",
            "Benchmark runtime together with solution error, conservation residuals, and stability across time-step and mesh refinement.",
            "Use differentiable solvers for local refinement only inside validated domains; retain discrete topology search outside them.",
        ],
        "actions_th": [
            "สร้าง evaluator applicability record ต่อ candidate class และบันทึก solver/gradient failure เป็นผลระดับแรกใน ledger",
            "benchmark runtime พร้อม solution error, conservation residual และ stability ข้าม time-step/mesh refinement",
            "ใช้ differentiable solver ปรับละเอียดเฉพาะในโดเมนที่ validate แล้ว และคง discrete topology search ภายนอกโดเมนนั้น",
        ],
    },
    "LT": {
        "theme_en": "Minimum-lap-time and vehicle design/control co-optimization",
        "theme_th": "เวลาต่อรอบต่ำสุดและการออกแบบรถ/การควบคุมร่วม",
        "findings_en": [
            "Minimum-lap-time optimization couples vehicle states, controls, path constraints, tyre limits, and power/energy constraints; isolated peak metrics are poor substitutes.",
            "Simultaneous design and control optimization changes the preferred hardware because the controller can exploit or expose component trade-offs.",
            "Numerical transcription, scaling, initialization, and constraint enforcement materially affect whether a computed lap is credible.",
        ],
        "findings_th": [
            "การ optimize เวลาต่อรอบต่ำสุดเชื่อม state ของรถ control path constraint ขีดจำกัดยาง และข้อจำกัด power/energy ค่าสูงสุดแยกส่วนใช้แทนได้ไม่ดี",
            "การปรับ design และ control พร้อมกันเปลี่ยน hardware ที่เหมาะ เพราะตัวควบคุมใช้ประโยชน์หรือเปิดเผย trade-off ของชิ้นส่วน",
            "numerical transcription, scaling, initialization และการบังคับ constraint มีผลโดยตรงต่อความน่าเชื่อถือของรอบที่คำนวณ",
        ],
        "actions_en": [
            "Replace disconnected subsystem scores with a coupled transient lap objective that preserves tyre, energy, thermal, brake, and stability constraints.",
            "Audit optimal-control feasibility by replaying controls in an independently configured forward simulation.",
            "Compare co-design against separately optimized fixed-topology baselines under the same track, energy profile, seeds, and compute.",
        ],
        "actions_th": [
            "แทนคะแนน subsystem ที่แยกกันด้วยวัตถุประสงค์ lap transient แบบ coupled ที่รักษาข้อจำกัดยาง พลังงาน ความร้อน เบรก และเสถียรภาพ",
            "audit feasibility ของ optimal control ด้วยการ replay control ใน forward simulation ที่ตั้งค่าอย่างอิสระ",
            "เทียบ co-design กับ fixed-topology baseline ที่ optimize แล้วภายใต้สนาม energy profile seed และ compute เดียวกัน",
        ],
    },
    "EN": {
        "theme_en": "Energy storage, powertrain, and race energy management",
        "theme_th": "แหล่งเก็บพลังงาน powertrain และการจัดการพลังงานในการแข่ง",
        "findings_en": [
            "Usable race energy is constrained by power limits, efficiency maps, temperature, state of charge, degradation, and containment mass, not nominal joules alone.",
            "Optimal energy management is trajectory-dependent and coupled to lap time, thermal state, and component sizing.",
            "Equivalent comparisons need complete carrier, conversion, cooling, and recovery accounting with observable losses.",
        ],
        "findings_th": [
            "พลังงานที่ใช้แข่งได้จริงถูกจำกัดด้วย power limit, efficiency map, อุณหภูมิ, state of charge, degradation และมวล containment ไม่ใช่ joule nominal อย่างเดียว",
            "การจัดการพลังงานที่เหมาะขึ้นกับ trajectory และเชื่อมกับเวลาต่อรอบ thermal state และขนาดชิ้นส่วน",
            "การเปรียบเทียบที่เท่าเทียมต้องรวม carrier, conversion, cooling และ recovery พร้อม loss ที่สังเกตได้",
        ],
        "actions_en": [
            "Implement stateful storage and converter maps with power, temperature, degradation, and failure bounds in the Work 120 energy realization.",
            "Make the race-energy profile include containment, auxiliaries, cooling, and recovery provenance.",
            "Optimize energy management jointly with trajectory and sizing, then replay the full balance independently.",
        ],
        "actions_th": [
            "เพิ่ม storage state และ converter map ที่มีขอบเขต power, temperature, degradation และ failure ใน Work 120",
            "ให้ race-energy profile รวม containment, auxiliary, cooling และ provenance ของ recovery",
            "optimize การจัดการพลังงานร่วมกับ trajectory และ sizing แล้ว replay สมดุลทั้งหมดอย่างอิสระ",
        ],
    },
    "TY": {
        "theme_en": "Tyres, friction, and road contact",
        "theme_th": "ยาง แรงเสียดทาน และการสัมผัสถนน",
        "findings_en": [
            "Tyre force depends on combined slip, normal load, camber, pressure, temperature, wear, speed, and road state; a fixed friction circle is only a bounded approximation.",
            "Transient relaxation and load transfer matter in racing manoeuvres, so steady-state maps alone can mis-rank a design.",
            "Model identification and uncertainty are central because tyre parameters are condition-specific and difficult to measure.",
        ],
        "findings_th": [
            "แรงยางขึ้นกับ combined slip, normal load, camber, pressure, temperature, wear, speed และสภาพถนน friction circle คงที่เป็นเพียง approximation ที่มีขอบเขต",
            "transient relaxation และ load transfer สำคัญในการขับแข่ง จึงอาจจัดอันดับแบบผิดหากใช้เฉพาะ steady-state map",
            "model identification และ uncertainty เป็นหัวใจ เพราะพารามิเตอร์ยางขึ้นกับสภาวะและวัดยาก",
        ],
        "actions_en": [
            "Upgrade the ground-interaction contract to combined-slip transient force with load, temperature, wear, and validity envelopes.",
            "Calibrate against declared data and propagate tyre uncertainty into lap-time and safety margins.",
            "Retain the present simple model only as a low-fidelity gate with audited promotion error.",
        ],
        "actions_th": [
            "ยกระดับ ground-interaction contract เป็นแรง combined-slip แบบ transient พร้อม load, temperature, wear และ validity envelope",
            "calibrate กับข้อมูลที่ประกาศและส่งต่อ uncertainty ของยางไปยังเวลาต่อรอบกับ safety margin",
            "คง model ง่ายปัจจุบันไว้เป็น low-fidelity gate เท่านั้นและ audit promotion error",
        ],
    },
    "AE": {
        "theme_en": "Aerodynamics and aerodynamic data",
        "theme_th": "อากาศพลศาสตร์และข้อมูล aerodynamic",
        "findings_en": [
            "Vehicle aerodynamics is geometry-, attitude-, wheel-, ground-, and flow-condition-dependent; isolated scalar coefficients hide spatial loads and balance shifts.",
            "Open CFD and experimental datasets can support surrogates and validation, but their geometry and Reynolds-number domains constrain transfer.",
            "Shape optimization needs drag, downforce, balance, cooling flow, sensitivity, and uncertainty together rather than one coefficient.",
        ],
        "findings_th": [
            "อากาศพลศาสตร์รถขึ้นกับ geometry, attitude, wheel, ground และสภาวะการไหล ค่าสัมประสิทธิ์เดี่ยวซ่อน spatial load และการเลื่อน balance",
            "ชุดข้อมูล CFD และการทดลองแบบเปิดช่วย surrogate และ validation ได้ แต่โดเมน geometry กับ Reynolds number จำกัดการถ่ายโอน",
            "shape optimization ต้องพิจารณา drag, downforce, balance, cooling flow, sensitivity และ uncertainty ร่วมกัน ไม่ใช่สัมประสิทธิ์เดียว",
        ],
        "actions_en": [
            "Add geometry-derived aero surfaces/fields with ride-height, yaw, wheel, and ground-effect sweeps to Work 121 and the coupled vehicle model.",
            "Use public datasets for pipeline validation and pretraining, then hold out project-specific geometries and conditions for independent tests.",
            "Promote aero surrogates only with uncertainty and periodic CFD/experimental audits.",
        ],
        "actions_th": [
            "เพิ่ม field/surface aero ที่มาจาก geometry พร้อม sweep ride height, yaw, wheel และ ground effect ใน Work 121 และ coupled vehicle model",
            "ใช้ public dataset ตรวจ pipeline และ pretrain แล้วกัน geometry/condition ของโครงการเป็น holdout อิสระ",
            "เลื่อน aero surrogate เมื่อมี uncertainty และ audit ด้วย CFD/การทดลองเป็นระยะเท่านั้น",
        ],
    },
    "TH": {
        "theme_en": "Thermal systems and cooling",
        "theme_th": "ระบบความร้อนและการระบายความร้อน",
        "findings_en": [
            "Thermal limits emerge from transient heat generation, storage, transfer, coolant/airflow, and control; a lumped steady temperature cannot establish race endurance.",
            "Cooling hardware costs mass, volume, pressure loss, parasitic power, and aerodynamic opportunity, so thermal design must be coupled to the vehicle objective.",
            "Reduced thermal models require calibrated envelopes and escalation when a candidate leaves them.",
        ],
        "findings_th": [
            "ขีดจำกัดความร้อนเกิดจาก heat generation, storage, transfer, coolant/airflow และ control แบบ transient อุณหภูมิ lumped คงที่ไม่ยืนยันความทนทานตลอดการแข่ง",
            "อุปกรณ์ระบายความร้อนมีต้นทุนมวล ปริมาตร pressure loss parasitic power และโอกาสทาง aero จึงต้องเชื่อม thermal design กับ objective ของรถ",
            "reduced thermal model ต้องมี envelope ที่ calibrate และเลื่อน fidelity เมื่อ candidate ออกจาก envelope",
        ],
        "actions_en": [
            "Couple Work 115/121 thermal-solid and flow-heat models to storage, converter, brakes, aero ducts, and the full-stint finish gate.",
            "Track heat-source provenance, stored energy, boundary flux, coolant pumping, and rejected heat as one balance.",
            "Add thermal soak, repeated-lap, hot-ambient, blockage, and pump/fan-failure cases.",
        ],
        "actions_th": [
            "เชื่อม thermal-solid และ flow-heat ของ Work 115/121 กับ storage, converter, brake, aero duct และ finish gate ตลอด stint",
            "ติดตาม provenance ของแหล่งความร้อน พลังงานสะสม boundary flux กำลังปั๊ม coolant และความร้อนที่ระบายเป็นสมดุลเดียว",
            "เพิ่มกรณี thermal soak, หลายรอบต่อเนื่อง, อากาศร้อน, ทางไหลอุดตัน และ pump/fan failure",
        ],
    },
    "MA": {
        "theme_en": "Materials, joints, fatigue, and manufacturing",
        "theme_th": "วัสดุ ข้อต่อ ความล้า และการผลิต",
        "findings_en": [
            "Material and joint performance is process-, orientation-, surface-, temperature-, tolerance-, and load-history-dependent; a handbook scalar is not a universal constitutive law.",
            "Fatigue and reliability require distributions, damage accumulation, and failure modes, not only static factor of safety.",
            "Manufacturing feasibility must be tied to a declared process and inspection plan.",
        ],
        "findings_th": [
            "สมรรถนะวัสดุและข้อต่อขึ้นกับ process, orientation, surface, temperature, tolerance และ load history ค่า scalar จาก handbook ไม่ใช่ constitutive law สากล",
            "fatigue และ reliability ต้องใช้ distribution, damage accumulation และ failure mode ไม่ใช่ static factor of safety อย่างเดียว",
            "manufacturing feasibility ต้องผูกกับกระบวนการและแผนตรวจที่ประกาศ",
        ],
        "actions_en": [
            "Apply the material-data policy at every constitutive lookup and keep unsupported conditions as explicit unknowns.",
            "Extend Works 113/114/116/130 with joint preload, contact, tolerance, thermal, fatigue, and process-specific failure envelopes.",
            "Add specimen and assembly correlation before transferring a material/joint model to a complete vehicle.",
        ],
        "actions_th": [
            "ใช้ material-data policy กับ constitutive lookup ทุกครั้ง และคงสภาวะที่ไม่มีข้อมูลเป็น unknown ชัดเจน",
            "ขยาย Works 113/114/116/130 ด้วย preload, contact, tolerance, thermal, fatigue และ failure envelope เฉพาะ process",
            "เพิ่ม specimen และ assembly correlation ก่อนถ่ายโอน model วัสดุ/ข้อต่อไปยังรถเต็มคัน",
        ],
    },
    "VV": {
        "theme_en": "Verification, validation, uncertainty, statistics, and claims",
        "theme_th": "verification, validation, uncertainty, สถิติ และ claim",
        "findings_en": [
            "Verification asks whether equations were solved correctly; validation asks whether the equations represent reality for the intended use. Neither is replaced by passing software tests.",
            "Uncertainty, sensitivity, convergence, calibration/validation separation, and multiplicity control determine how strong a claim can be.",
            "Adaptive search and benchmark reuse create selection bias; untouched holdouts and append-only evidence are necessary for credible discovery claims.",
        ],
        "findings_th": [
            "verification ถามว่าแก้สมการถูกหรือไม่ ส่วน validation ถามว่าสมการแทนโลกจริงสำหรับ intended use ได้หรือไม่ การผ่าน software test ไม่แทนทั้งสองอย่าง",
            "uncertainty, sensitivity, convergence, การแยก calibration/validation และการควบคุม multiplicity กำหนดความแข็งแรงของ claim",
            "adaptive search และการใช้ benchmark ซ้ำสร้าง selection bias จึงต้องมี untouched holdout และหลักฐานแบบ append-only",
        ],
        "actions_en": [
            "Turn the Validation Strategy into executable, domain-specific evidence gates with traceable intended-use statements.",
            "Require convergence, sensitivity/UQ, calibration/holdout separation, multiplicity-aware inference, and negative controls in every admitted study.",
            "Use claim templates that bind each conclusion to candidate, evaluator, dataset, fidelity, and uncertainty identities.",
        ],
        "actions_th": [
            "ทำ Validation Strategy ให้เป็น evidence gate เฉพาะโดเมนที่รันได้ พร้อม intended-use statement ที่ trace ได้",
            "บังคับ convergence, sensitivity/UQ, การแยก calibration/holdout, inference ที่คำนึง multiplicity และ negative control ในงาน admitted ทุกชิ้น",
            "ใช้ claim template ที่ผูกข้อสรุปกับ candidate, evaluator, dataset, fidelity และ uncertainty identity",
        ],
    },
    "AR": {
        "theme_en": "Autonomous racing control, data, and strategy",
        "theme_th": "การควบคุม ข้อมูล และกลยุทธ์การแข่งอัตโนมัติ",
        "findings_en": [
            "Racing performance requires perception, state estimation, prediction, planning, control, system identification, and safety to remain coupled at the limit.",
            "MPC and learning complement each other when learned components expose uncertainty and hard constraints remain enforceable.",
            "Real-track systems show that latency, localization faults, opponents, changing grip, and operational safety dominate beyond ideal simulation.",
        ],
        "findings_th": [
            "สมรรถนะการแข่งต้องเชื่อม perception, state estimation, prediction, planning, control, system identification และ safety ไว้ด้วยกันที่ขีดจำกัด",
            "MPC และ learning เสริมกันได้เมื่อส่วนที่เรียนรู้เปิดเผย uncertainty และยังบังคับ hard constraint ได้",
            "ระบบในสนามจริงแสดงว่า latency, localization fault, คู่แข่ง, grip ที่เปลี่ยน และ operational safety สำคัญกว่า simulation อุดมคติ",
        ],
        "actions_en": [
            "Use an optimized autonomous racing stack as a fair controller baseline before attributing gains to vehicle morphology.",
            "Add online identification, uncertainty-aware prediction, latency/fault injection, and opponent scenarios to held-out evaluation.",
            "Keep strategy decisions inside the same energy, tyre, thermal, and safety accounting as the vehicle design.",
        ],
        "actions_th": [
            "ใช้ autonomous racing stack ที่ optimize แล้วเป็น controller baseline ที่ยุติธรรมก่อนให้เครดิต morphology ของรถ",
            "เพิ่ม online identification, prediction ที่รู้ uncertainty, การฉีด latency/fault และสถานการณ์คู่แข่งใน held-out evaluation",
            "ให้การตัดสินใจเชิงกลยุทธ์อยู่ในบัญชีพลังงาน ยาง ความร้อน และ safety เดียวกับการออกแบบรถ",
        ],
    },
    "DS": {
        "theme_en": "Design synthesis, creativity, and novelty evidence",
        "theme_th": "การสังเคราะห์แบบ ความสร้างสรรค์ และหลักฐานความใหม่",
        "findings_en": [
            "Function-to-form mappings and generative models can expand concept production, but generated variety is not automatically useful or novel.",
            "Novelty has multiple meanings: visual, structural, functional, technological, and prior-art novelty require different evidence.",
            "Design metrics must separate quantity, quality, variety, and novelty and must be anchored to external references.",
        ],
        "findings_th": [
            "function-to-form mapping และ generative model เพิ่มจำนวน concept ได้ แต่ความหลากหลายที่สร้างไม่เท่ากับความมีประโยชน์หรือความใหม่โดยอัตโนมัติ",
            "novelty มีหลายความหมาย: ความใหม่ทางภาพ โครงสร้าง หน้าที่ เทคโนโลยี และ prior art ต้องใช้หลักฐานต่างกัน",
            "metric การออกแบบต้องแยก quantity, quality, variety และ novelty และยึดกับแหล่งอ้างอิงภายนอก",
        ],
        "actions_en": [
            "Split Formula Ultimate reporting into geometric novelty, causal functional difference, performance benefit, and external technology novelty.",
            "Add a prior-art search only after a candidate has causal function and fair performance evidence.",
            "Use function-flow and physical-interface descriptions as search aids, not as proof that hardware exists.",
        ],
        "actions_th": [
            "แยกรายงาน Formula Ultimate เป็น geometric novelty, causal functional difference, performance benefit และ external technology novelty",
            "ค้น prior art หลัง candidate มีหลักฐาน causal function และ performance ที่ยุติธรรมแล้ว",
            "ใช้คำอธิบาย function-flow และ physical interface ช่วยค้นหา ไม่ใช้เป็นหลักฐานว่า hardware มีอยู่จริง",
        ],
    },
}


PAPER_TRANSFER = {
    "OE": {
        "question_en": "How does {title} search, preserve, or evaluate coupled morphology and control, and what bias does that introduce?",
        "question_th": "งาน {title} ค้นหา รักษา หรือประเมิน morphology ร่วมกับ control อย่างไร และทำให้เกิด bias แบบใด?",
        "target_en": "Work 124 multiscale search scheduler and morphology/controller evidence ledger",
        "target_th": "ตัวจัดตาราง multiscale search และ morphology/controller evidence ledger ของ Work 124",
        "test_en": "Run the paper-derived operator or allocation rule against evolution/QD and an optimized fixed-topology control using matched seeds, total compute, controller-training budget, and held-out race environments.",
        "test_th": "รัน operator หรือกฎจัดสรรที่ได้จาก paper เทียบ evolution/QD และ fixed-topology control ที่ optimize แล้ว โดยจับคู่ seed, compute รวม, งบฝึก controller และสนาม held-out",
        "accept_en": "Accept only if feasible archive coverage or held-out race performance improves without increasing invalid designs, controller under-training, or evaluator disagreement; otherwise reject the transfer.",
        "accept_th": "ยอมรับเมื่อ feasible archive coverage หรือผลงานสนาม held-out ดีขึ้นโดยไม่เพิ่มแบบ invalid, controller under-training หรือ evaluator disagreement มิฉะนั้นปฏิเสธการถ่ายโอน",
        "boundary_en": "Morphology results are highly sensitive to encoding, controller-training allocation, task distribution, and simulator assumptions; virtual success does not transfer to a racing vehicle without physical correlation.",
        "boundary_th": "ผล morphology ไวต่อ encoding, การจัดงบฝึก controller, task distribution และสมมติฐาน simulator มาก ความสำเร็จเสมือนไม่ถ่ายโอนไปรถแข่งโดยไม่มี physical correlation",
    },
    "AG": {
        "question_en": "Can the agent or generative method in {title} produce engineering artifacts that pass executable geometric and physical verification?",
        "question_th": "agent หรือ generative method ใน {title} สร้าง artifact วิศวกรรมที่ผ่านการตรวจ geometry และ physics แบบรันได้หรือไม่?",
        "target_en": "agent proposal pipeline, CAD/CAE verifier suite, and experiment provenance ledger",
        "target_th": "agent proposal pipeline, ชุด verifier CAD/CAE และ experiment provenance ledger",
        "test_en": "Use hidden CAD/CAE tasks and negative controls; compare artifact execution, geometry validity, physics checks, repair cost, and verifier false positives against the current scripted baseline.",
        "test_th": "ใช้โจทย์ CAD/CAE และ negative control ที่ซ่อน เปรียบเทียบการรัน artifact, geometry validity, physics check, ค่า repair และ verifier false positive กับ scripted baseline ปัจจุบัน",
        "accept_en": "Accept only verified artifact-quality gains at a declared token/tool/compute budget; fluent text, self-grading, or render similarity cannot pass.",
        "accept_th": "ยอมรับเฉพาะคุณภาพ artifact ที่ verifier ยืนยันภายใต้งบ token/tool/compute ที่ประกาศ ข้อความลื่นไหล การให้คะแนนตนเอง หรือ render similarity ใช้ผ่านไม่ได้",
        "boundary_en": "Agent benchmarks often measure completion or appearance rather than functional correctness, and self-evaluation can leak task knowledge or reward superficial proxies.",
        "boundary_th": "benchmark agent มักวัดการทำงานจบหรือรูปลักษณ์แทน functional correctness และการประเมินตนเองอาจทำ task leakage หรือให้รางวัล proxy ผิวเผิน",
    },
    "QD": {
        "question_en": "How does {title} trade quality, diversity, evaluation cost, and fidelity error in an adaptive search?",
        "question_th": "งาน {title} แลกเปลี่ยน quality, diversity, evaluation cost และ fidelity error ใน adaptive search อย่างไร?",
        "target_en": "QD archive, descriptor schema, resource ledger, and multifidelity promotion policy",
        "target_th": "QD archive, descriptor schema, resource ledger และนโยบาย multifidelity promotion",
        "test_en": "Compare the paper-derived search rule with objective optimization, random search, and MAP-Elites under matched proposals, seeds, wall/CPU/GPU budgets, and stratified high-fidelity audits.",
        "test_th": "เทียบกฎค้นหาจาก paper กับ objective optimization, random search และ MAP-Elites โดยจับคู่ proposal, seed, งบ wall/CPU/GPU และ high-fidelity audit แบบ stratified",
        "accept_en": "Require improved feasible coverage or held-out quality with confidence intervals and no unacceptable proxy false-negative rate; unknown high-fidelity outcomes remain `not_estimable`.",
        "accept_th": "ต้องเพิ่ม feasible coverage หรือ held-out quality พร้อม confidence interval และไม่มี proxy false-negative rate ที่ยอมรับไม่ได้ ผล fidelity สูงที่ยังไม่ทราบคงเป็น `not_estimable`",
        "boundary_en": "QD conclusions depend on descriptor geometry, archive resolution, evaluation budget, and proxy fidelity; archive score alone is not vehicle value.",
        "boundary_th": "ข้อสรุป QD ขึ้นกับ descriptor geometry, archive resolution, งบประเมิน และ proxy fidelity คะแนน archive อย่างเดียวไม่ใช่คุณค่าของรถ",
    },
    "CAD": {
        "question_en": "Does {title} represent or generate CAD topology, geometry, constraints, and assembly semantics well enough for downstream engineering use?",
        "question_th": "งาน {title} แทนหรือสร้าง CAD topology, geometry, constraint และ assembly semantics ได้พอสำหรับใช้งานวิศวกรรมต่อหรือไม่?",
        "target_en": "Work 138 geometry-general evaluator, B-rep/STEP adapter, and Work 140 joint-system checks",
        "target_th": "geometry-general evaluator ของ Work 138, B-rep/STEP adapter และ joint-system check ของ Work 140",
        "test_en": "Evaluate paper-derived representations on hidden solids and assemblies with exact topology, watertightness, constraint/editability, mass-property, mate, interference, meshing, and load-path checks.",
        "test_th": "ประเมิน representation จาก paper บน solid/assembly ที่ซ่อนด้วยการตรวจ topology, watertightness, constraint/editability, mass property, mate, interference, meshing และ load path",
        "accept_en": "Require higher functional artifact pass rate at matched generation budget without worsening topology corruption, invalid mates, or geometry-to-mesh discrepancy.",
        "accept_th": "ต้องเพิ่มอัตรา artifact ผ่านเชิงหน้าที่ที่งบสร้างเท่ากัน โดยไม่เพิ่ม topology corruption, mate invalid หรือ geometry-to-mesh discrepancy",
        "boundary_en": "CAD reconstruction or generation metrics can reward visual or geometric similarity while missing invalid topology, lost design intent, impossible mates, and non-manufacturable detail.",
        "boundary_th": "metric CAD reconstruction/generation อาจให้รางวัลความคล้ายทางภาพหรือ geometry แต่พลาด topology invalid, design intent ที่หาย, mate ที่เป็นไปไม่ได้ และรายละเอียดผลิตไม่ได้",
    },
    "ST": {
        "question_en": "What structural, meshing, contact, or failure method does {title} validate, and over which numerical and physical regime?",
        "question_th": "งาน {title} validate วิธีด้าน structure, meshing, contact หรือ failure แบบใด และในช่วง numerical/physical ใด?",
        "target_en": "structural/contact evaluator, mesh-refinement evidence, and material-failure gate",
        "target_th": "structural/contact evaluator, หลักฐาน mesh refinement และ material-failure gate",
        "test_en": "Run analytical/manufactured-solution cases, at least three registered refinements, contact/failure negative controls, and an independent solver comparison on the same geometry and loads.",
        "test_th": "รันกรณี analytical/manufactured solution, refinement ที่ลงทะเบียนอย่างน้อยสามระดับ, negative control ของ contact/failure และ independent solver comparison บน geometry/load เดียวกัน",
        "accept_en": "Require converged fields, independently recovered reactions, bounded residuals and discrepancies, correct failure localization, and explicit non-convergence outcomes.",
        "accept_th": "ต้องได้ field ที่ converge, reaction ที่กู้คืนอิสระ, residual/discrepancy มีขอบเขต, ตำแหน่ง failure ถูก และบันทึก non-convergence ชัดเจน",
        "boundary_en": "Results can be mesh-, regularization-, constitutive-, and contact-formulation-dependent; a scalar stress or a solver completion flag is insufficient.",
        "boundary_th": "ผลอาจขึ้นกับ mesh, regularization, constitutive law และ contact formulation ค่า stress เดี่ยวหรือสถานะ solver จบไม่เพียงพอ",
    },
    "SI": {
        "question_en": "Which simulation, coupling, differentiation, or optimal-control capability in {title} is accurate and stable enough for a Formula Ultimate evaluator?",
        "question_th": "ความสามารถด้าน simulation, coupling, differentiation หรือ optimal control ใน {title} แม่นและเสถียรพอสำหรับ evaluator ของ Formula Ultimate หรือไม่?",
        "target_en": "simulation coupling contract, evaluator applicability registry, and solver-failure ledger",
        "target_th": "simulation coupling contract, evaluator applicability registry และ solver-failure ledger",
        "test_en": "Benchmark against analytical and independent-solver cases across time steps, meshes, stiffness/contact regimes, and hardware while measuring error, conservation, stability, and cost.",
        "test_th": "benchmark กับกรณี analytical และ independent solver ข้าม time step, mesh, ช่วง stiffness/contact และ hardware พร้อมวัด error, conservation, stability และ cost",
        "accept_en": "Admit only declared candidate classes whose error and stability stay inside a registered envelope; gradient or solver failure remains an observable result.",
        "accept_th": "admit เฉพาะ candidate class ที่ error/stability อยู่ใน envelope ที่ลงทะเบียน และคง gradient/solver failure เป็นผลที่สังเกตได้",
        "boundary_en": "Speed, differentiability, or API convenience does not establish model-form validity, conservation, contact correctness, or stable coupling.",
        "boundary_th": "ความเร็ว differentiability หรือ API ที่สะดวกไม่ยืนยัน model-form validity, conservation, contact correctness หรือ coupling stability",
    },
    "LT": {
        "question_en": "How does {title} formulate and solve minimum-lap-time or coupled vehicle design/control, and how is feasibility checked?",
        "question_th": "งาน {title} ตั้งและแก้ปัญหา minimum lap time หรือ vehicle design/control แบบ coupled อย่างไร และตรวจ feasibility อย่างไร?",
        "target_en": "integrated transient lap evaluator, optimal-control transcription, and independent forward replay",
        "target_th": "integrated transient lap evaluator, optimal-control transcription และ independent forward replay",
        "test_en": "Solve and replay matched track problems with identical tyre, aero, energy, thermal, actuator, and path constraints; compare transcription methods and optimized fixed-topology baselines.",
        "test_th": "แก้และ replay โจทย์สนามเดียวกันด้วยข้อจำกัด tyre, aero, energy, thermal, actuator และ path เดียวกัน พร้อมเทียบ transcription และ fixed-topology baseline ที่ optimize แล้ว",
        "accept_en": "Require forward-replay feasibility, small state/control defects, conserved energy, finish completion, and repeatable lap-time gains outside numerical tolerance.",
        "accept_th": "ต้องผ่าน forward-replay feasibility, state/control defect ต่ำ, สมดุลพลังงาน, finish completion และเวลาที่ดีขึ้นซ้ำได้เกิน numerical tolerance",
        "boundary_en": "Lap-time results depend on vehicle model, tyre/aero maps, track representation, constraints, initialization, scaling, and transcription; optimizer convergence alone is not feasibility.",
        "boundary_th": "ผลเวลาต่อรอบขึ้นกับ vehicle model, tyre/aero map, track, constraint, initialization, scaling และ transcription การที่ optimizer converge อย่างเดียวไม่ใช่ feasibility",
    },
    "EN": {
        "question_en": "How does {title} model energy storage, conversion, control, or architecture strongly enough to support a race-time comparison?",
        "question_th": "งาน {title} model การเก็บ/แปลง/ควบคุมพลังงานหรือ architecture แข็งแรงพอสำหรับเปรียบเทียบเวลาแข่งอย่างไร?",
        "target_en": "Work 120 onboard-energy realization, power/thermal state model, and race-energy ledger",
        "target_th": "onboard-energy realization ของ Work 120, power/thermal state model และ race-energy ledger",
        "test_en": "Compare the paper-derived model or strategy with the current lumped model over matched laps/stints, including carrier and containment mass, efficiency maps, auxiliaries, cooling, recovery, and degradation.",
        "test_th": "เทียบ model/strategy จาก paper กับ lumped model ปัจจุบันบน lap/stint เดียวกัน โดยรวมมวล carrier/containment, efficiency map, auxiliary, cooling, recovery และ degradation",
        "accept_en": "Require independently closed energy/heat balances, finish completion, bounded state and temperature error, and ranking stability under admitted model refinements.",
        "accept_th": "ต้องปิดสมดุล energy/heat อย่างอิสระ, แข่งจบ, state/temperature error มีขอบเขต และอันดับคงตัวภายใต้ model refinement ที่ admit",
        "boundary_en": "Energy results are conditional on cell/component parameterization, power and thermal limits, degradation, containment, auxiliaries, and race policy; nominal energy is not equivalence.",
        "boundary_th": "ผลพลังงานขึ้นกับ parameter ของ cell/component, power/thermal limit, degradation, containment, auxiliary และนโยบายแข่ง พลังงาน nominal ไม่ใช่ความเท่าเทียม",
    },
    "TY": {
        "question_en": "Which tyre/contact states and operating conditions does {title} identify, and can they support transient racing predictions?",
        "question_th": "งาน {title} ระบุ state และ operating condition ของ tyre/contact ใด และรองรับการทำนายการแข่งแบบ transient ได้หรือไม่?",
        "target_en": "ground-interaction contract, tyre-state estimator, and lap/safety uncertainty propagation",
        "target_th": "ground-interaction contract, tyre-state estimator และการส่งต่อ uncertainty ไปยัง lap/safety",
        "test_en": "Fit and validate against separate manoeuvres across combined slip, load, camber, pressure, temperature, wear, speed, and road state; compare with the present low-fidelity model.",
        "test_th": "fit และ validate กับ manoeuvre แยกข้าม combined slip, load, camber, pressure, temperature, wear, speed และสภาพถนน แล้วเทียบ low-fidelity model ปัจจุบัน",
        "accept_en": "Require bounded force/moment and temperature/wear errors on held-out manoeuvres and improved lap replay without hiding extrapolation outside the tyre envelope.",
        "accept_th": "ต้องมี force/moment และ temperature/wear error มีขอบเขตบน manoeuvre held-out และทำ lap replay ดีขึ้นโดยไม่ซ่อน extrapolation นอก tyre envelope",
        "boundary_en": "Tyre parameters and conclusions are condition-, construction-, and dataset-specific; a fitted curve outside its load/temperature/wear envelope is not validated.",
        "boundary_th": "พารามิเตอร์และข้อสรุปยางขึ้นกับ condition, construction และ dataset curve ที่ fit แล้วนอก envelope load/temperature/wear ยังไม่ validate",
    },
    "AE": {
        "question_en": "What aerodynamic mechanism, dataset, solver, or surrogate does {title} establish, and over what geometry and flow domain?",
        "question_th": "งาน {title} ยืนยันกลไก aerodynamic, dataset, solver หรือ surrogate ใด และในโดเมน geometry/flow ใด?",
        "target_en": "Work 121 geometry-flow-heat path, aero-field evaluator, and surrogate promotion audit",
        "target_th": "geometry-flow-heat path ของ Work 121, aero-field evaluator และ surrogate promotion audit",
        "test_en": "Evaluate matched geometries across ride height, yaw, wheel/ground treatment, Reynolds number, and cooling flow; compare surrogate or CFD outputs with independent CFD and available experiments.",
        "test_th": "ประเมิน geometry เดียวกันข้าม ride height, yaw, wheel/ground treatment, Reynolds number และ cooling flow แล้วเทียบ surrogate/CFD กับ independent CFD และการทดลองที่มี",
        "accept_en": "Require bounded force, moment, balance, surface-field, and uncertainty errors on held-out geometries, with no systematic rejection of unfamiliar forms.",
        "accept_th": "ต้องมี error ของ force, moment, balance, surface field และ uncertainty มีขอบเขตบน geometry held-out และไม่คัดทิ้งรูปทรงไม่คุ้นอย่างเป็นระบบ",
        "boundary_en": "Aero conclusions are tied to geometry family, Reynolds number, turbulence/ground/wheel treatment, mesh, and validation data; road-car or canonical-body transfer is limited.",
        "boundary_th": "ข้อสรุป aero ผูกกับตระกูล geometry, Reynolds number, turbulence/ground/wheel treatment, mesh และข้อมูล validation การถ่ายโอนจากรถถนนหรือทรงมาตรฐานมีขอบเขต",
    },
    "TH": {
        "question_en": "How does {title} represent transient heat generation, storage, transfer, and cooling cost for the relevant component or geometry?",
        "question_th": "งาน {title} แทน heat generation, storage, transfer และต้นทุน cooling แบบ transient ของ component/geometry ที่เกี่ยวข้องอย่างไร?",
        "target_en": "Works 115/121 coupled thermal-solid/flow model and full-stint thermal finish gate",
        "target_th": "coupled thermal-solid/flow model ของ Works 115/121 และ full-stint thermal finish gate",
        "test_en": "Compare reduced and spatial models over repeated laps, hot ambient, flow blockage, and cooling-actuator failures while closing heat and auxiliary-power balances.",
        "test_th": "เทียบ reduced/spatial model บนหลายรอบต่อเนื่อง อากาศร้อน flow blockage และ cooling-actuator failure พร้อมปิดสมดุล heat/auxiliary power",
        "accept_en": "Require bounded temperature and heat-flow discrepancy, correct derating/failure timing, full-stint completion, and escalation outside the reduced-model envelope.",
        "accept_th": "ต้องมี temperature/heat-flow discrepancy มีขอบเขต, เวลา derating/failure ถูก, จบเต็ม stint และยกระดับ fidelity เมื่อนอก reduced-model envelope",
        "boundary_en": "Thermal results depend on geometry, boundary conditions, material properties, flow regime, heat-source calibration, and time history; steady lumped agreement is limited.",
        "boundary_th": "ผล thermal ขึ้นกับ geometry, boundary condition, material property, flow regime, calibration แหล่งความร้อน และ time history การตรงกันของ steady lumped model มีขอบเขต",
    },
    "MA": {
        "question_en": "What material, joint, fatigue, tolerance, or manufacturing evidence does {title} provide for a declared process and load history?",
        "question_th": "งาน {title} ให้หลักฐานวัสดุ ข้อต่อ fatigue tolerance หรือ manufacturing ใดสำหรับ process/load history ที่ประกาศ?",
        "target_en": "material-data policy and Works 113/114/116/130 joint, failure, and tolerance evidence",
        "target_th": "material-data policy และหลักฐาน joint/failure/tolerance ของ Works 113/114/116/130",
        "test_en": "Validate paper-derived properties or mechanisms with held-out specimen and joint/assembly cases spanning process, orientation, temperature, tolerance, preload, surface, and cyclic loading.",
        "test_th": "validate property/mechanism จาก paper ด้วย specimen และ joint/assembly held-out ข้าม process, orientation, temperature, tolerance, preload, surface และ cyclic loading",
        "accept_en": "Require provenance-complete properties, calibrated uncertainty, correct failure mode/location, and bounded transfer from specimen to assembly; unsupported conditions remain unknown.",
        "accept_th": "ต้องมี property provenance ครบ, uncertainty ที่ calibrate, failure mode/location ถูก และการถ่ายโอน specimen-to-assembly มีขอบเขต สภาวะไม่มีข้อมูลคงเป็น unknown",
        "boundary_en": "Material and joint evidence is process-, orientation-, surface-, temperature-, tolerance-, and load-history-specific; database values cannot silently substitute for tests.",
        "boundary_th": "หลักฐานวัสดุ/ข้อต่อเฉพาะ process, orientation, surface, temperature, tolerance และ load history ค่าฐานข้อมูลแทนการทดสอบอย่างเงียบ ๆ ไม่ได้",
    },
    "VV": {
        "question_en": "Which verification, validation, uncertainty, statistical, or claim failure does {title} address, and what evidence discipline follows?",
        "question_th": "งาน {title} แก้ปัญหา verification, validation, uncertainty, สถิติ หรือ claim failure ใด และต้องใช้วินัยหลักฐานอะไร?",
        "target_en": "Validation Strategy, experiment registration schema, claim ledger, and independent evidence gates",
        "target_th": "Validation Strategy, experiment registration schema, claim ledger และ independent evidence gate",
        "test_en": "Apply the paper-derived check to a known-positive case, a falsifying negative control, repeated seeds/refinements, and a calibration-versus-holdout split; audit claim wording against outcomes.",
        "test_th": "ใช้ check จาก paper กับ known-positive, negative control ที่หักล้างได้, seed/refinement ซ้ำ และการแยก calibration/holdout แล้ว audit wording ของ claim กับผล",
        "accept_en": "Require predefined error/uncertainty bounds, correct rejection of invalid evidence, multiplicity-aware inference, deterministic provenance, and no retrospective repair.",
        "accept_th": "ต้องมี error/uncertainty bound ที่กำหนดล่วงหน้า, ปฏิเสธหลักฐาน invalid ถูก, inference คำนึง multiplicity, provenance deterministic และไม่มี retrospective repair",
        "boundary_en": "These methods improve claim discipline but do not supply missing physical data or model validity; statistical correctness cannot rescue an inapplicable evaluator.",
        "boundary_th": "วิธีเหล่านี้เพิ่มวินัย claim แต่ไม่สร้างข้อมูลกายภาพหรือ model validity ที่ขาด ความถูกต้องทางสถิติช่วย evaluator ที่ใช้ผิดโดเมนไม่ได้",
    },
    "AR": {
        "question_en": "How does {title} combine racing perception, estimation, planning, control, identification, or strategy at the performance limit?",
        "question_th": "งาน {title} รวม perception, estimation, planning, control, identification หรือ strategy ของการแข่งที่ขีดจำกัดอย่างไร?",
        "target_en": "optimized autonomous-driver baseline, held-out race scenarios, and controller/vehicle attribution protocol",
        "target_th": "optimized autonomous-driver baseline, สถานการณ์แข่ง held-out และ protocol แยกผล controller/vehicle",
        "test_en": "Compare against MPC, learning, and hybrid baselines on the same vehicle and tracks with latency, localization faults, grip shifts, opponents, energy/thermal limits, and safety constraints.",
        "test_th": "เทียบ MPC, learning และ hybrid baseline บนรถ/สนามเดียวกัน พร้อม latency, localization fault, grip shift, คู่แข่ง, energy/thermal limit และ safety constraint",
        "accept_en": "Require repeatable held-out race-time or completion gains without more safety violations, constraint breaches, or vehicle-model advantage; separate controller and morphology effects.",
        "accept_th": "ต้องได้เวลาหรือ completion บน held-out ดีขึ้นซ้ำได้โดยไม่เพิ่ม safety violation, constraint breach หรือความได้เปรียบจาก vehicle model และแยกผล controller/morphology",
        "boundary_en": "Controller results are stack-, vehicle-, sensor-, latency-, opponent-, track-, and safety-policy-specific; simulator dominance is not real-track or morphology evidence.",
        "boundary_th": "ผล controller เฉพาะ stack, vehicle, sensor, latency, opponent, track และ safety policy การชนะใน simulator ไม่ใช่หลักฐานสนามจริงหรือ morphology",
    },
    "DS": {
        "question_en": "How does {title} synthesize or measure form, function, architecture, creativity, or novelty, and what evidence distinguishes useful novelty?",
        "question_th": "งาน {title} สังเคราะห์หรือวัด form, function, architecture, creativity หรือ novelty อย่างไร และหลักฐานใดแยกความใหม่ที่มีประโยชน์?",
        "target_en": "design-language descriptors, causal-function record, and four-part novelty claim template",
        "target_th": "design-language descriptor, causal-function record และ template claim ความใหม่สี่ส่วน",
        "test_en": "Apply the paper-derived synthesis or novelty measure to known duplicates, geometric variants, functionally distinct candidates, and external prior-art controls while preserving evaluator blindness.",
        "test_th": "ใช้วิธี synthesis/novelty จาก paper กับ duplicate ที่รู้ผล, geometric variant, candidate ที่หน้าที่ต่าง และ external prior-art control โดยรักษา evaluator blindness",
        "accept_en": "Require correct separation of geometric variety, causal functional difference, fair performance benefit, and external technology novelty; reject appearance-only positives.",
        "accept_th": "ต้องแยก geometric variety, causal functional difference, performance benefit ที่ยุติธรรม และ external technology novelty ได้ถูก และปฏิเสธผลบวกจากรูปลักษณ์อย่างเดียว",
        "boundary_en": "Function and novelty taxonomies are observer- and corpus-dependent; a generative model's diversity or patent-distance score is not physical usefulness or novelty by itself.",
        "boundary_th": "taxonomy ของ function/novelty ขึ้นกับผู้สังเกตและ corpus คะแนน diversity หรือ patent distance ของ generative model ไม่ใช่ประโยชน์ทางกายภาพหรือความใหม่โดยตัวมันเอง",
    },
}


HIGHLIGHT_IDS = {
    "OE": ("OE-002", "OE-016", "OE-029"),
    "AG": ("AG-003", "AG-004", "AG-026"),
    "QD": ("QD-001", "QD-003", "QD-005"),
    "CAD": ("CAD-003", "CAD-013", "CAD-018"),
    "ST": ("ST-011", "ST-015", "ST-016"),
    "SI": ("SI-001", "SI-006", "SI-020"),
    "LT": ("LT-001", "LT-005", "LT-032"),
    "EN": ("EN-012", "EN-016", "EN-030"),
    "TY": ("TY-006", "TY-011", "TY-012"),
    "AE": ("AE-002", "AE-007", "AE-024"),
    "TH": ("TH-001", "TH-004"),
    "MA": ("MA-003", "MA-012"),
    "VV": ("VV-008", "VV-012", "VV-024"),
    "AR": ("AR-003", "AR-012", "AR-022"),
    "DS": ("DS-009", "DS-012", "DS-017"),
}


PAPER_OVERRIDES = {
    "OE-016": {
        "question_en": "Can a co-design search preserve a new morphology long enough for its controller to adapt, instead of discarding it on immediate fitness?",
        "question_th": "co-design search จะรักษา morphology ใหม่ไว้นานพอให้ controller ปรับตัวได้หรือไม่ แทนการคัดทิ้งจาก fitness ทันที?",
        "method_en": "The study evolves voxel-based virtual robots and adds morphology age as a second objective, comparing morphological-innovation protection with unprotected and alternative-protection treatments over 5,000 generations (pp. 4-6).",
        "method_th": "งานวิวัฒนาการหุ่นยนต์ voxel เสมือนและเพิ่มอายุ morphology เป็น objective ที่สอง เทียบ morphological-innovation protection กับแบบไม่ปกป้องและการปกป้องทางเลือกตลอด 5,000 generation (หน้า 4-6)",
        "findings_en": "With morphology protection, mean fitness rose from 18.715 at generation 0 to 22.916 at generation 5,000 (p < 0.001). An alternative protection treatment did not beat no protection (p = 0.240) and was significantly worse than morphology protection (p = 1.211e-4) (p. 4).",
        "findings_th": "เมื่อปกป้อง morphology ค่า fitness เฉลี่ยเพิ่มจาก 18.715 ที่ generation 0 เป็น 22.916 ที่ generation 5,000 (p < 0.001) ส่วนการปกป้องทางเลือกไม่ดีกว่าแบบไม่ปกป้อง (p = 0.240) และแย่กว่า morphology protection อย่างมีนัยสำคัญ (p = 1.211e-4) (หน้า 4)",
        "interesting_en": "The paper isolates controller-adaptation lag as a selection bias: a structurally promising child can look worse only because it inherits a controller specialized for its parent (p. 5).",
        "interesting_th": "paper แยก controller-adaptation lag เป็น selection bias: ลูกที่โครงสร้างมีศักยภาพอาจดูแย่เพียงเพราะรับ controller ที่เฉพาะกับ parent มา (หน้า 5)",
        "limitations_en": "The evidence is from virtual voxel locomotion, and the authors state that the fitness gain does not conclusively prove their proposed causal explanation (p. 4). It does not establish the same effect in racing vehicles or under equal controller-training cost.",
        "limitations_th": "หลักฐานมาจากการเคลื่อนที่ของ voxel เสมือน และผู้เขียนระบุว่า fitness ที่เพิ่มยังไม่พิสูจน์คำอธิบายเชิงสาเหตุอย่างเด็ดขาด (หน้า 4) จึงยังไม่ยืนยันผลเดียวกันในรถแข่งหรือเมื่อคิดต้นทุนฝึก controller เท่ากัน",
        "proposal_en": "Add morphology age and controller-training spend to each candidate ledger record; run protected versus unprotected co-design at matched total controller steps and require the held-out benefit to survive after every morphology receives equal adaptation opportunity.",
        "proposal_th": "เพิ่มอายุ morphology และจำนวน step ฝึก controller ใน ledger ของ candidate ทุกตัว แล้วเทียบ co-design แบบปกป้อง/ไม่ปกป้องด้วย controller step รวมเท่ากัน โดยผล held-out ต้องยังอยู่หลัง morphology ทุกแบบได้โอกาสปรับตัวเท่ากัน",
    },
    "AG-026": {
        "question_en": "Do text/code-capable models produce CAD that remains valid under parameter edits, engineering checks, matched FEA, and assembly-joint execution?",
        "question_th": "โมเดลที่สร้างข้อความ/โค้ดผลิต CAD ที่ยัง valid ภายใต้ parameter edit, engineering check, matched FEA และการรัน assembly joint ได้หรือไม่?",
        "method_en": "CADEngBench-P uses 300 parametric parts for 600 zero-to-CAD and functional-edit tasks, while CADEngBench-A uses 150 body pairs for joint retrieval, exact entity grounding, frame prediction, and kinematic verification; eight multimodal code-capable models are compared (p. 1).",
        "method_th": "CADEngBench-P ใช้ชิ้นส่วน parametric 300 ชิ้นในโจทย์ zero-to-CAD และ functional edit รวม 600 งาน ส่วน CADEngBench-A ใช้ body pair 150 คู่ตรวจ joint retrieval, entity grounding, frame prediction และ kinematic verification โดยเทียบโมเดล multimodal ที่เขียนโค้ดได้ 8 ตัว (หน้า 1)",
        "findings_en": "Editing supplied CAD is substantially easier than generating it; complex edits and matched linear-static FEA remain difficult. Assembly models often find the right region but not the recorded joint or mating entities, and no model leads every evaluation stage (pp. 1, 5, 22-23).",
        "findings_th": "การแก้ CAD ที่ให้มาง่ายกว่าการสร้างใหม่มาก แต่ complex edit และ matched linear-static FEA ยังยาก โมเดล assembly มักหาบริเวณถูกแต่หา joint/mating entity ที่บันทึกไว้ไม่ถูก และไม่มีโมเดลใดนำทุกขั้นประเมิน (หน้า 1, 5, 22-23)",
        "interesting_en": "A generated program can execute and match one nominal shape while encoding the wrong parameter dependency, causing its structural-response family to diverge (p. 5).",
        "interesting_th": "โปรแกรมที่สร้างอาจรันได้และตรงรูป nominal หนึ่งจุด แต่ encode ความสัมพันธ์พารามิเตอร์ผิด ทำให้ตระกูล structural response เบี่ยงออก (หน้า 5)",
        "limitations_en": "The benchmark uses declared DFM rules, CalculiX linear-static FEA, and recorded assembly relations; it does not cover nonlinear material/contact, fatigue, tolerance stacks, or complete vehicle function.",
        "limitations_th": "benchmark ใช้กฎ DFM ที่ประกาศ, CalculiX linear-static FEA และ assembly relation ที่บันทึกไว้ ยังไม่ครอบคลุม nonlinear material/contact, fatigue, tolerance stack หรือหน้าที่รถเต็มคัน",
        "proposal_en": "Adopt hidden parametric-family, matched-FEA, exact-mate, and motion-probe tests in the agent verifier; score end-to-end failure when any earlier geometry or joint-grounding stage fails.",
        "proposal_th": "เพิ่ม hidden test สำหรับ parametric family, matched FEA, exact mate และ motion probe ใน agent verifier และนับ end-to-end fail เมื่อขั้น geometry หรือ joint grounding ก่อนหน้าล้มเหลว",
    },
    "QD-003": {
        "question_en": "Can surrogate-assisted illumination map many high-performing design niches using far fewer expensive evaluations than MAP-Elites or single-optimum search?",
        "question_th": "surrogate-assisted illumination จะทำแผนที่ niche การออกแบบคุณภาพสูงหลายแบบด้วย expensive evaluation น้อยกว่า MAP-Elites หรือการหา optimum เดี่ยวได้หรือไม่?",
        "method_en": "SAIL combines a Gaussian-process surrogate, an upper-confidence-bound acquisition map, and MAP-Elites. It is tested first on 2-D airfoils and then on realistic 3-D aerodynamic design with expensive flow simulation (pp. 1-2, 8, 13).",
        "method_th": "SAIL รวม Gaussian-process surrogate, upper-confidence-bound acquisition map และ MAP-Elites ทดสอบกับ airfoil 2 มิติแล้วขยายไปงานออกแบบ aero 3 มิติที่ flow simulation มีราคาแพง (หน้า 1-2, 8, 13)",
        "findings_en": "The paper reports hundreds of diverse high-performing designs with orders-of-magnitude fewer evaluations than MAP-Elites or CMA-ES in the 2-D task, and demonstrates high-performing illumination maps in the 3-D task (p. 1). UCB sampling improves accuracy around high-fitness regions relative to uniform or variance-only sampling (p. 13).",
        "findings_th": "paper รายงานแบบที่หลากหลายและคุณภาพสูงหลายร้อยแบบด้วยจำนวน evaluation ต่ำกว่า MAP-Elites หรือ CMA-ES หลายลำดับขนาดในงาน 2 มิติ และสร้าง illumination map คุณภาพสูงในงาน 3 มิติ (หน้า 1) การสุ่มด้วย UCB เพิ่มความแม่นบริเวณ high-fitness เมื่อเทียบการสุ่มสม่ำเสมอหรือดู variance อย่างเดียว (หน้า 13)",
        "interesting_en": "Besides saving evaluations, SAIL exposes encoding bias: its maps show which regions an encoding can express and where the surrogate is easy or hard to learn (discussion, pp. 25-26).",
        "interesting_th": "นอกจากลด evaluation แล้ว SAIL เปิดเผย encoding bias โดยแผนที่แสดงบริเวณที่ encoding สร้างได้และบริเวณที่ surrogate เรียนง่ายหรือยาก (discussion หน้า 25-26)",
        "limitations_en": "The gain depends on chosen behavioral features, Gaussian-process adequacy, acquisition policy, and expensive-truth sampling. The 3-D study was costly enough that detailed learning curves available for the airfoil case were not reproduced (p. 19).",
        "limitations_th": "ประโยชน์ขึ้นกับ behavioral feature, ความเหมาะของ Gaussian process, acquisition policy และการสุ่ม expensive truth งาน 3 มิติมีต้นทุนสูงจนไม่ได้ทำ learning curve ละเอียดเท่ากรณี airfoil (หน้า 19)",
        "proposal_en": "Add a SAIL arm to the search benchmark with the same high-fidelity call budget as MAP-Elites; audit surrogate error by archive cell and require gains in held-out feasible coverage, not predicted QD score alone.",
        "proposal_th": "เพิ่มแขน SAIL ใน benchmark การค้นหาโดยให้งบ high-fidelity call เท่ากับ MAP-Elites audit surrogate error แยก archive cell และต้องเพิ่ม held-out feasible coverage ไม่ใช่ predicted QD score อย่างเดียว",
    },
    "CAD-013": {
        "question_en": "Can B-rep graph learning recover joint axes and poses from weak supervision in ordinary parametric CAD assemblies?",
        "question_th": "การเรียนรู้บนกราฟ B-rep จะกู้ joint axis และ pose จาก weak supervision ใน parametric CAD assembly ทั่วไปได้หรือไม่?",
        "method_en": "JoinABLe encodes B-rep faces and edges as graphs, predicts joint-axis entity pairs, and searches joint pose. It uses weak labels from the Fusion 360 Gallery assembly dataset and compares multiple geometric baselines (pp. 1, 22-28).",
        "method_th": "JoinABLe encode face/edge ของ B-rep เป็นกราฟ ทำนายคู่ entity ของ joint axis และค้น joint pose ใช้ weak label จาก Fusion 360 Gallery assembly dataset และเทียบ geometric baseline หลายแบบ (หน้า 1, 22-28)",
        "findings_en": "The reported joint-axis accuracy is 79.53%, close to the 80% human result and above the tested baselines (p. 1). Performance is higher for hole-based joints; edge length and entity type are important features, while face area can hurt (results appendix, pp. 22-25).",
        "findings_th": "ความแม่น joint-axis ที่รายงานคือ 79.53% ใกล้ผลมนุษย์ 80% และสูงกว่า baseline ที่ทดสอบ (หน้า 1) งาน joint ที่มีรูทำได้ดีกว่า โดย edge length และ entity type สำคัญ ส่วน face area อาจลดผล (ภาคผล หน้า 22-25)",
        "interesting_en": "Equivalent labels materially raise measured accuracy (p. 22), showing that assembly evaluation must distinguish genuine geometric equivalence from forgiving an incorrect mate.",
        "interesting_th": "equivalent label ทำให้ความแม่นที่วัดเพิ่มมาก (หน้า 22) แสดงว่า evaluation assembly ต้องแยก geometric equivalence จริงออกจากการยอม joint ผิด",
        "limitations_en": "The method predicts joints from dataset regularities and is easier on hole-like interfaces; it does not prove load transfer, tolerance, collision-free motion, fastening detail, or manufacturing feasibility.",
        "limitations_th": "วิธีทำนาย joint จาก regularity ของ dataset และทำงานง่ายกว่ากับ interface แบบรู ไม่พิสูจน์ load transfer, tolerance, motion ที่ไม่ชน, รายละเอียดตัวยึด หรือ manufacturing feasibility",
        "proposal_en": "Use JoinABLe as a proposal baseline in Work 140, but require exact face/edge grounding, declared DOF, motion probe, interference, and load-path checks before accepting a joint.",
        "proposal_th": "ใช้ JoinABLe เป็น proposal baseline ใน Work 140 แต่ต้องผ่าน exact face/edge grounding, DOF ที่ประกาศ, motion probe, interference และ load-path check ก่อนรับ joint",
    },
    "ST-015": {
        "question_en": "Can contact dynamics remain intersection- and element-inversion-free under large deformation while exposing separate physical and geometric accuracy tolerances?",
        "question_th": "contact dynamics จะคงสภาพไม่ทะลุและไม่ทำ element inversion ภายใต้ large deformation พร้อมแยก tolerance ทาง physics/geometry ได้หรือไม่?",
        "method_en": "IPC formulates contact as barrier potentials inside implicit nonlinear elastodynamics, uses continuous collision detection and a custom Newton-type solver, and benchmarks deformable/self-contact cases with declared material, time-step, and geometric tolerances (pp. 1, 7, 10, 16).",
        "method_th": "IPC สร้าง contact เป็น barrier potential ใน implicit nonlinear elastodynamics ใช้ continuous collision detection และ Newton-type solver เฉพาะ ทดสอบ deformable/self-contact ด้วย material, time step และ geometric tolerance ที่ประกาศ (หน้า 1, 7, 10, 16)",
        "findings_en": "The method produces intersection- and inversion-free trajectories across the reported examples and permits independent dynamics and surface-conformation tolerances (p. 1). Resolution raises contact count, iteration count, memory roughly linearly, and timing slightly superlinearly in the mat study (p. 16).",
        "findings_th": "วิธีให้ trajectory ที่ไม่ทะลุและไม่ inversion ในตัวอย่างที่รายงาน และแยก tolerance ของ dynamics กับ surface conformation ได้ (หน้า 1) ในกรณี mat เมื่อเพิ่ม resolution จำนวน contact/iteration/memory เพิ่มใกล้เชิงเส้น และเวลาสูงกว่าเชิงเส้นเล็กน้อย (หน้า 16)",
        "interesting_en": "The paper treats missed collision and infeasible linearized constraints as numerical failures rather than hiding them with non-physical fail-safes (pp. 5, 7).",
        "interesting_th": "paper ถือ missed collision และ linearized constraint ที่ infeasible เป็น numerical failure แทนการซ่อนด้วย non-physical fail-safe (หน้า 5, 7)",
        "limitations_en": "Cost rises with contact complexity and mesh resolution, and the authors give no general convergence guarantee for their lagged friction variables, except stiction (conclusion, p. 20). Geometric non-penetration is not constitutive validation.",
        "limitations_th": "ต้นทุนเพิ่มตามความซับซ้อน contact และ mesh resolution และผู้เขียนไม่ให้ convergence guarantee ทั่วไปแก่ lagged friction variable ยกเว้น stiction (สรุป หน้า 20) การไม่ทะลุทาง geometry ไม่ใช่ constitutive validation",
        "proposal_en": "Add IPC as an independent contact candidate for Work 114/123, with CCD failure, barrier tolerance, friction convergence, energy residual, reaction recovery, and mesh refinement all retained in the ledger.",
        "proposal_th": "เพิ่ม IPC เป็น independent contact candidate สำหรับ Work 114/123 โดยเก็บ CCD failure, barrier tolerance, friction convergence, energy residual, reaction recovery และ mesh refinement ใน ledger ทั้งหมด",
    },
    "SI-020": {
        "question_en": "Can exchanged power residuals provide a non-iterative error estimate and adaptive macro-step controller for co-simulation?",
        "question_th": "residual ของกำลังที่แลกเปลี่ยนจะใช้เป็น error estimate และตัวควบคุม macro step แบบไม่ iterate สำหรับ co-simulation ได้หรือไม่?",
        "method_en": "ECCO computes residual power/energy from power bonds at subsystem interfaces and adapts the macro step without rollback or subsystem-internal access. It is tested on linear and nonlinear quarter-car co-simulation variants (pp. 1, 5, 8-11).",
        "method_th": "ECCO คำนวณ residual power/energy จาก power bond ที่ interface ของ subsystem และปรับ macro step โดยไม่ rollback หรือเข้าถึงภายใน subsystem ทดสอบกับ quarter-car co-simulation แบบ linear/nonlinear (หน้า 1, 5, 8-11)",
        "findings_en": "In a reported linear benchmark, residual-energy-based adaptation reduces residual energy by about 90%; alternative system partitioning produces larger errors, showing that coupling topology itself matters (pp. 10-11).",
        "findings_th": "ใน linear benchmark ที่รายงาน adaptive step จาก residual energy ลด residual energy ประมาณ 90% และการแบ่ง subsystem อีกแบบให้ error สูงกว่า แสดงว่า coupling topology มีผล (หน้า 10-11)",
        "interesting_en": "The error signal is independently observable at the interface rather than constructed by negating a prescribed input, matching the project's need for transferred-energy evidence.",
        "interesting_th": "error signal สังเกตได้อย่างอิสระที่ interface ไม่ได้สร้างจากการใส่เครื่องหมายลบให้ input ที่กำหนด ตรงกับความต้องการหลักฐาน transferred energy ของโครงการ",
        "limitations_en": "The global-error argument assumes coupling without algebraic loops and the evidence is from quarter-car benchmarks; tolerance choice and subsystem partition remain application-specific.",
        "limitations_th": "ข้อผูก global error สมมติ coupling ที่ไม่มี algebraic loop และหลักฐานมาจาก quarter-car benchmark การเลือก tolerance กับการแบ่ง subsystem ยังเฉพาะ application",
        "proposal_en": "Instrument every Work 123 coupling bond with exchanged effort/flow and residual energy, compare constant and ECCO-adaptive macro steps, and fail promotion when residual-energy reduction does not correlate with independent state/output error.",
        "proposal_th": "ติดเครื่องมือที่ทุก coupling bond ของ Work 123 เพื่อวัด effort/flow และ residual energy เทียบ macro step คงที่กับ ECCO adaptive และไม่เลื่อนเมื่อ residual-energy reduction ไม่สัมพันธ์กับ state/output error อิสระ",
    },
    "LT-005": {
        "question_en": "How much do suspension kinematics and attitude-sensitive aerodynamics change the optimal lap when modeled together?",
        "question_th": "suspension kinematics และ aerodynamics ที่ไวต่อ attitude เปลี่ยน optimal lap มากเพียงใดเมื่อ model ร่วมกัน?",
        "method_en": "The paper embeds polynomial surrogates of a physical suspension-kinematics model and attitude-dependent aero into a Formula One optimal-control lap calculation, retaining high kinematic accuracy while reducing solve cost (pp. 4, 6, 11).",
        "method_th": "paper ฝัง polynomial surrogate ของ suspension-kinematics model เชิงกายภาพและ aero ที่ขึ้นกับ attitude ใน optimal-control lap ของ Formula One เพื่อรักษาความแม่น kinematic แต่ลดเวลาคำนวณ (หน้า 4, 6, 11)",
        "findings_en": "Reported surrogate errors are at most 0.147 mm in front ride height and 0.038 degrees in roll over the tested mesh. Including steer and sideslip aero sensitivities raises the reported lap time to 83.45 s, and lower high-speed ride height gains downforce while roll degrades it (pp. 6, 11).",
        "findings_th": "surrogate error สูงสุดที่รายงานคือ 0.147 mm สำหรับ front ride height และ 0.038° สำหรับ roll บน mesh ที่ทดสอบ เมื่อรวม sensitivity ของ aero ต่อ steer/sideslip เวลาต่อรอบเพิ่มเป็น 83.45 s และ ride height ต่ำที่ความเร็วสูงเพิ่ม downforce ขณะที่ roll ลดมัน (หน้า 6, 11)",
        "interesting_en": "Aero and suspension cannot be optimized as independent peak metrics: the controller changes ride and roll along the lap, moving the aero operating point.",
        "interesting_th": "aero กับ suspension optimize เป็น peak metric แยกกันไม่ได้ เพราะ controller เปลี่ยน ride/roll ตลอด lap และเลื่อน operating point ของ aero",
        "limitations_en": "The result is tied to the chosen F1 model, surrogate mesh, aero maps, track, and optimal-control transcription; polynomial fit accuracy does not validate the underlying aero or suspension data.",
        "limitations_th": "ผลผูกกับ F1 model, surrogate mesh, aero map, track และ optimal-control transcription ที่เลือก ความแม่น polynomial fit ไม่ validate ข้อมูล aero/suspension ต้นทาง",
        "proposal_en": "Add ride height, pitch, roll, steer, and sideslip as shared states between Work 121 aero and Work 123 vehicle dynamics; require independent forward replay and aero-map envelope checks.",
        "proposal_th": "เพิ่ม ride height, pitch, roll, steer และ sideslip เป็น state ร่วมระหว่าง aero Work 121 กับ vehicle dynamics Work 123 และบังคับ independent forward replay กับ aero-map envelope check",
    },
    "EN-012": {
        "question_en": "Which battery-model details are necessary for race-car sizing, and which are necessary for physically informative optimal control?",
        "question_th": "รายละเอียด battery model ใดจำเป็นต่อ sizing รถแข่ง และรายละเอียดใดจำเป็นต่อ optimal control ที่ให้ตัวแปรเชิงกายภาพน่าเชื่อถือ?",
        "method_en": "The paper places battery models of increasing detail inside a time-optimal electric-race-car co-design problem, comparing a simple datasheet model with models that include state-of-charge-dependent open-circuit voltage and more realistic electrical behavior; both convex and nonlinear formulations use 15 m spatial steps (pp. 5-9).",
        "method_th": "paper ใส่ battery model หลายระดับรายละเอียดใน time-optimal co-design ของรถแข่งไฟฟ้า เทียบ model ง่ายจาก datasheet กับ model ที่รวม open-circuit voltage ตาม state of charge และพฤติกรรมไฟฟ้าที่สมจริงกว่า โดย formulation แบบ convex/nonlinear ใช้ spatial step 15 m (หน้า 5-9)",
        "findings_en": "The simple model gives consistent battery-sizing results, while detailed models are needed to study credible control-variable evolution. For the detailed models, race-time difference between 24 and 25 parallel cells is negligible; convex relaxation can also yield non-physical energy-variable profiles (pp. 1-2, 9, 11).",
        "findings_th": "model ง่ายให้ผล battery sizing สอดคล้องกัน ส่วน model ละเอียดจำเป็นเมื่อต้องการศึกษาวิวัฒนาการตัวแปร control ที่น่าเชื่อถือ ใน model ละเอียด ความต่างเวลาแข่งระหว่าง 24 กับ 25 cell ขนานแทบไม่มี และ convex relaxation อาจให้ profile ตัวแปรพลังงานที่ไม่เป็นกายภาพ (หน้า 1-2, 9, 11)",
        "interesting_en": "The paper does not show a generic architecture-ranking reversal; it shows a narrower fidelity split: simple models may suffice for sizing, but not for interpreting optimal energy-control trajectories.",
        "interesting_th": "paper ไม่ได้แสดงการกลับอันดับ architecture แบบทั่วไป แต่แสดงเส้นแบ่ง fidelity ที่แคบกว่า: model ง่ายอาจพอสำหรับ sizing แต่ไม่พอสำหรับตีความ trajectory การควบคุมพลังงานที่ optimize",
        "limitations_en": "The result is specific to the studied electric race-car problem, battery parameterization, 15 m discretization, and convex/non-convex formulations. It does not include every storage chemistry, degradation pathway, containment, or full thermal architecture.",
        "limitations_th": "ผลเฉพาะโจทย์รถแข่งไฟฟ้า parameter battery, discretization 15 m และ formulation convex/non-convex ที่ศึกษา ยังไม่รวมทุก chemistry, degradation pathway, containment หรือ thermal architecture เต็ม",
        "proposal_en": "Use the simple model only for a sizing pre-screen; require the state-dependent model for control interpretation and compare both by forward replay, energy/heat closure, and ranking stability before Work 120 promotion.",
        "proposal_th": "ใช้ model ง่ายเฉพาะ sizing pre-screen และบังคับ model ที่ขึ้นกับ state สำหรับตีความ control เทียบทั้งสองด้วย forward replay, energy/heat closure และ ranking stability ก่อนเลื่อน Work 120",
    },
    "TY-011": {
        "question_en": "Can tyre parameters and their uncertainty be identified from real driving data, and how does manoeuvre excitation affect identifiability?",
        "question_th": "จะระบุพารามิเตอร์ยางและ uncertainty จากข้อมูลขับจริงได้หรือไม่ และ excitation ของ manoeuvre มีผลต่อ identifiability อย่างไร?",
        "method_en": "The study uses stochastic variational inference within a Bayesian-optimization workflow, evaluates excitation effects, and compares with a Nelder-Mead baseline on theoretical and real-world identification cases (pp. 2-3).",
        "method_th": "งานใช้ stochastic variational inference ใน workflow แบบ Bayesian optimization ประเมินผลของ excitation และเทียบ Nelder-Mead baseline ในกรณี identification เชิงทฤษฎีและข้อมูลจริง (หน้า 2-3)",
        "findings_en": "The method estimates parameter distributions rather than one best fit and shows that excitation affects parameter accuracy. The paper also reports that tire-only parameter identification can perform worse than identifying the fuller model, warning against treating other vehicle parameters as known (pp. 2-3).",
        "findings_th": "วิธีประมาณ distribution ของพารามิเตอร์แทน best fit จุดเดียวและแสดงว่า excitation มีผลต่อความแม่น งานยังพบว่าการ identify เฉพาะพารามิเตอร์ยางอาจแย่กว่าการ identify model เต็ม เตือนว่าห้ามถือพารามิเตอร์รถอื่นว่ารู้แน่ (หน้า 2-3)",
        "interesting_en": "The experiment links manoeuvre design to uncertainty: ordinary accessible driving may not excite the parameters that a racing controller needs.",
        "interesting_th": "การทดลองเชื่อมการออกแบบ manoeuvre กับ uncertainty เพราะการขับทั่วไปที่ทำได้ง่ายอาจไม่กระตุ้นพารามิเตอร์ที่ racing controller ต้องใช้",
        "limitations_en": "The result depends on the tyre/vehicle model, excitation range, sensors, and real-data quality; posterior uncertainty does not correct model-form error or extrapolation outside measured conditions.",
        "limitations_th": "ผลขึ้นกับ tyre/vehicle model, ช่วง excitation, sensor และคุณภาพข้อมูลจริง posterior uncertainty ไม่แก้ model-form error หรือ extrapolation นอกสภาวะที่วัด",
        "proposal_en": "Design a D-optimal-style tyre identification manoeuvre set, fit joint tyre/vehicle uncertainty, and propagate posterior samples through held-out lap replay before tightening the ground-contact envelope.",
        "proposal_th": "ออกแบบชุด manoeuvre ระบุยางแบบ D-optimal fit uncertainty ร่วม tyre/vehicle และส่ง posterior sample ผ่าน held-out lap replay ก่อนลดขอบเขต ground-contact envelope",
    },
    "AE-002": {
        "question_en": "What spatial and temporal resolution is required for high-fidelity CFD to reproduce measured ground-effect front-wing flow structures?",
        "question_th": "high-fidelity CFD ต้องใช้ spatial/temporal resolution เท่าใดจึงสร้างโครงสร้างการไหลที่วัดได้ของปีกหน้าใน ground effect?",
        "method_en": "The Imperial Front Wing supplies CAD and experimental oil-flow/PIV data. Under-resolved DNS/implicit LES with third-, fourth-, and fifth-order spectral/hp discretizations is compared against measured vortex locations, intensities, wall features, lift, and drag (pp. 1, 7-16).",
        "method_th": "Imperial Front Wing มี CAD และข้อมูลทดลอง oil-flow/PIV แล้วเทียบ under-resolved DNS/implicit LES ด้วย spectral/hp order 3, 4 และ 5 กับตำแหน่ง/ความเข้ม vortex, wall feature, lift และ drag ที่วัด (หน้า 1, 7-16)",
        "findings_en": "The third-order case is under-resolved. The fifth-order case best matches experimental reattachment and flow features; its downforce is 4.5% above the fourth-order case, and its lift stabilizes only late in the averaging window (pp. 8, 16).",
        "findings_th": "กรณี order 3 มี resolution ไม่พอ กรณี order 5 ตรงการทดลองด้าน reattachment/flow feature ดีที่สุด ให้ downforce สูงกว่า order 4 อยู่ 4.5% และ lift เสถียรเฉพาะช่วงท้ายของ averaging window (หน้า 8, 16)",
        "interesting_en": "A visually plausible lower-resolution field gives the wrong load trend, so aero validation must include resolution and averaging-time sensitivity, not only one coefficient snapshot.",
        "interesting_th": "field resolution ต่ำที่ดูสมจริงอาจให้แนวโน้ม load ผิด จึงต้องตรวจ resolution และ averaging-time sensitivity ไม่ใช่ coefficient ภาพเดียว",
        "limitations_en": "This is one front-wing geometry and high-fidelity setup, not a complete car or broad turbulence-model validation. The highest-order lift was still evolving for much of the run, so averaging convergence remains material.",
        "limitations_th": "เป็น geometry ปีกหน้าหนึ่งแบบและ high-fidelity setup หนึ่งชุด ไม่ใช่รถเต็มคันหรือ validation turbulence model ทั่วไป lift ของ order สูงสุดยังเปลี่ยนในช่วงรันมาก จึงต้องระวัง averaging convergence",
        "proposal_en": "Use the IFW CAD/PIV case as the first independent aero gate: reproduce vortex location and reattachment plus lift/drag under at least three resolution levels and a preregistered averaging-convergence rule.",
        "proposal_th": "ใช้ IFW CAD/PIV เป็น independent aero gate แรก โดยทำซ้ำตำแหน่ง vortex, reattachment, lift/drag ที่ resolution อย่างน้อยสามระดับและกฎ averaging convergence ที่ลงทะเบียนล่วงหน้า",
    },
    "TH-001": {
        "question_en": "What terms are required for a thermodynamically complete battery energy balance when multiple reactions, mixing, and phase change occur?",
        "question_th": "สมดุลพลังงานแบตเตอรี่ที่ครบทาง thermodynamics ต้องมี term ใดเมื่อเกิดหลาย reaction, mixing และ phase change?",
        "method_en": "The paper derives a general cell energy balance including electrochemical reactions, composition-dependent open-circuit potentials, mixing, phase change, and Joule heating, then applies it to two Li-Al/FeS reaction mechanisms (pp. 1-8).",
        "method_th": "paper derive สมดุลพลังงานเซลล์ทั่วไปที่รวม electrochemical reaction, open-circuit potential ตาม composition, mixing, phase change และ Joule heating แล้วใช้กับกลไก reaction Li-Al/FeS สองแบบ (หน้า 1-8)",
        "findings_en": "The two mechanisms can reach the same final adiabatic-reversible temperature yet follow different heat-generation histories and slope changes. The common single-reaction balance is justified only when phase-change, mixing, and simultaneous-reaction effects are negligible (results/conclusion, pp. 7-9).",
        "findings_th": "สองกลไกไปถึงอุณหภูมิ adiabatic-reversible สุดท้ายเท่ากันได้แต่มีประวัติ heat generation และจุดเปลี่ยน slope ต่างกัน สมดุลแบบ reaction เดียวที่ใช้ทั่วไปใช้ได้เมื่อ phase change, mixing และ simultaneous reaction ไม่มีนัยสำคัญเท่านั้น (ผล/สรุป หน้า 7-9)",
        "interesting_en": "Equal terminal temperature does not imply equal internal thermal mechanism, so a final-temperature check can hide incorrect heat-source provenance.",
        "interesting_th": "อุณหภูมิปลายเท่ากันไม่แปลว่ากลไกความร้อนภายในเท่ากัน การตรวจแค่อุณหภูมิสุดท้ายจึงซ่อน provenance ของแหล่งความร้อนที่ผิดได้",
        "limitations_en": "The rigorous balance needs instantaneous composition profiles and reaction-current fractions, which are hard to obtain without a detailed electrochemical model (p. 2); the example chemistry is not a modern racing cell.",
        "limitations_th": "สมดุลเต็มต้องใช้ composition profile และสัดส่วนกระแสของแต่ละ reaction แบบทันที ซึ่งหาได้ยากหากไม่มี electrochemical model ละเอียด (หน้า 2) และ chemistry ตัวอย่างไม่ใช่เซลล์แข่งสมัยใหม่",
        "proposal_en": "Extend Work 120/115 heat accounting with named irreversible, reversible, mixing, phase, and side-reaction terms; test when the lumped single-reaction model stays within a registered error envelope.",
        "proposal_th": "ขยายบัญชีความร้อน Work 120/115 ด้วย term irreversible, reversible, mixing, phase และ side reaction ที่ระบุชื่อ แล้วทดสอบว่า lumped single-reaction model อยู่ใน error envelope ที่ลงทะเบียนเมื่อใด",
    },
    "MA-003": {
        "question_en": "Can steel fatigue strength be predicted from composition and processing variables using open materials data, and which inputs matter most?",
        "question_th": "จะทำนาย fatigue strength ของเหล็กจาก composition และ processing variable ด้วยข้อมูลวัสดุเปิดได้หรือไม่ และ input ใดสำคัญที่สุด?",
        "method_en": "The study cleans NIMS steel records, ranks composition/process features, fits multiple regressors including neural networks, trees, and polynomial models, and evaluates with leave-one-out cross-validation for rotating-bending fatigue at 10^7 cycles (pp. 5-10).",
        "method_th": "งานทำความสะอาดข้อมูลเหล็ก NIMS จัดอันดับ feature ด้าน composition/process fit regressor หลายชนิดรวม neural network, tree และ polynomial และประเมินด้วย leave-one-out cross-validation สำหรับ rotating-bending fatigue ที่ 10^7 cycle (หน้า 5-10)",
        "findings_en": "Several models reach R2 around 0.98 with reported error below 4%, improving earlier efforts and ranking predictive composition/process variables (pp. 1, 13-15).",
        "findings_th": "หลาย model ได้ R2 ประมาณ 0.98 และ error ที่รายงานต่ำกว่า 4% ดีกว่างานก่อนและช่วยจัดอันดับ composition/process variable ที่ทำนายได้ (หน้า 1, 13-15)",
        "interesting_en": "The paper models process-structure-property linkage rather than composition alone, which matches the project's rule that material values depend on manufacturing history.",
        "interesting_th": "paper model ความเชื่อมโยง process-structure-property ไม่ใช่ composition อย่างเดียว ตรงกับกฎโครงการว่าค่าวัสดุขึ้นกับประวัติการผลิต",
        "limitations_en": "The authors call the dataset small for data mining and recommend more heterogeneous data (p. 16). LOOCV within one database does not prove cross-source, new-alloy, multiaxial, thermal, or variable-amplitude fatigue transfer, and prediction is not causation.",
        "limitations_th": "ผู้เขียนระบุว่าชุดข้อมูลเล็กสำหรับ data mining และควรเพิ่มข้อมูลหลายแหล่ง (หน้า 16) LOOCV ในฐานเดียวไม่พิสูจน์การถ่ายโอนข้ามแหล่ง/โลหะใหม่ หรือ fatigue แบบ multiaxial, thermal, variable amplitude และ prediction ไม่ใช่ causation",
        "proposal_en": "Register NIMS provenance and reproduce the model with alloy-family/source holdouts; use predictions only to prioritize tests, then validate candidate-specific S-N/failure data before Work 116 admission.",
        "proposal_th": "ลงทะเบียน provenance ของ NIMS และทำซ้ำ model ด้วย holdout แยก alloy family/source ใช้ prediction จัดลำดับการทดสอบเท่านั้น แล้ว validate S-N/failure data เฉพาะ candidate ก่อน Work 116 admission",
    },
    "VV-008": {
        "question_en": "How should confidence in a computational prediction be built by separating code/solution verification from validation against experiments?",
        "question_th": "ควรสร้างความเชื่อมั่นในการทำนายเชิงคำนวณอย่างไรโดยแยก code/solution verification ออกจาก validation กับการทดลอง?",
        "method_en": "This 92-page engineering viewpoint synthesizes V&V practice: PIRT prioritization, code and calculation verification, grid convergence, validation hierarchies, experimental uncertainty, quantitative comparison, and inference from a validation domain to prediction (pp. 14, 21, 34, 48).",
        "method_th": "บทความมุมมองวิศวกรรม 92 หน้าสังเคราะห์ V&V: PIRT, code/calculation verification, grid convergence, validation hierarchy, experimental uncertainty, quantitative comparison และ inference จาก validation domain ไป prediction (หน้า 14, 21, 34, 48)",
        "findings_en": "Verification assesses accuracy in solving the computational model; validation assesses agreement with experimental reality for intended use. Validation requires numerical error, experimental uncertainty, and model discrepancy to remain distinct, and prediction outside the validation database requires weaker inference (pp. 3-4, 14, 21).",
        "findings_th": "verification ประเมินความแม่นในการแก้ computational model ส่วน validation ประเมินความตรงกับโลกทดลองสำหรับ intended use ต้องแยก numerical error, experimental uncertainty และ model discrepancy และการทำนายนอก validation database ใช้ inference ที่อ่อนกว่า (หน้า 3-4, 14, 21)",
        "interesting_en": "A code can be verified while its model is invalid for the application; equally, experimental agreement at one tier does not automatically validate a complete-system prediction.",
        "interesting_th": "code อาจ verify แล้วแต่ model ใช้ไม่ได้กับ application และการตรงการทดลองหนึ่ง tier ไม่ได้ validate การทำนายระบบเต็มโดยอัตโนมัติ",
        "limitations_en": "This is a framework and viewpoint, not validation evidence for any Formula Ultimate solver. Its practices must be specialized into numerical thresholds, experiments, and intended-use domains for each physics evaluator.",
        "limitations_th": "เป็น framework/มุมมอง ไม่ใช่หลักฐาน validation ของ solver Formula Ultimate ต้องแปลงเป็น threshold, experiment และ intended-use domain เฉพาะ evaluator ฟิสิกส์แต่ละตัว",
        "proposal_en": "Add an intended-use/V&V block to every evaluator identity: governing model, code-verification cases, refinement evidence, validation tier/data, discrepancy and uncertainty, applicability domain, and prohibited claim language.",
        "proposal_th": "เพิ่ม block intended-use/V&V ใน evaluator identity ทุกตัว: governing model, code-verification case, refinement evidence, validation tier/data, discrepancy/uncertainty, applicability domain และภาษาที่ห้าม claim",
    },
    "AR-003": {
        "question_en": "Does a vehicle model that fits open-loop or aggregate data better necessarily evaluate a closed-loop autonomous motion controller more faithfully?",
        "question_th": "vehicle model ที่ fit ข้อมูล open-loop หรือ aggregate ดีกว่า จะประเมิน autonomous motion controller แบบ closed loop ได้ตรงขึ้นเสมอหรือไม่?",
        "method_en": "The study compares simulation models against real-track closed-loop trajectory-tracking data, using maximum lateral error and a distribution-sensitive lateral-error disparity, then repeats under a scaled velocity profile (pp. 4-6).",
        "method_th": "งานเทียบ simulation model กับข้อมูล trajectory tracking แบบ closed loop จากสนามจริง ใช้ทั้ง maximum lateral error และ lateral-error disparity ที่ไวต่อ distribution แล้วทำซ้ำเมื่อ scale velocity profile (หน้า 4-6)",
        "findings_en": "Maximum lateral error alone discards important error structure, and retuning the baseline model for better approximation can disproportionately worsen lateral-error disparity (pp. 5-6). Model fidelity and controller-evaluation fidelity are therefore not monotonically equivalent.",
        "findings_th": "maximum lateral error อย่างเดียวทิ้งโครงสร้าง error สำคัญ และการ retune baseline ให้ approximation ดีขึ้นอาจทำ lateral-error disparity แย่ลงมาก (หน้า 5-6) ดังนั้น model fidelity กับ fidelity ของการประเมิน controller ไม่ได้เพิ่มตามกันเสมอ",
        "interesting_en": "The paper directly challenges the assumption that a globally 'better' model preserves controller rankings or closed-loop error behavior.",
        "interesting_th": "paper ท้าทายสมมติฐานโดยตรงว่า model ที่ 'ดีกว่า' โดยรวมจะรักษาอันดับ controller หรือพฤติกรรม error แบบ closed loop",
        "limitations_en": "The evidence concerns the tested controller, model family, track, speed profile, sensors, and lateral-error metrics; it does not establish a universal best simulator or cover wheel-to-wheel racing.",
        "limitations_th": "หลักฐานเฉพาะ controller, model family, track, speed profile, sensor และ lateral-error metric ที่ทดสอบ ไม่สร้าง simulator ที่ดีที่สุดสากลหรือครอบคลุม wheel-to-wheel",
        "proposal_en": "Audit every fidelity promotion with closed-loop controller outcomes and ranking preservation, not open-loop fit alone; include full lateral-error distributions, constraint violations, and held-out speed/grip conditions.",
        "proposal_th": "audit fidelity promotion ทุกครั้งด้วยผล controller closed loop และการรักษาอันดับ ไม่ใช่ open-loop fit อย่างเดียว โดยรวม distribution ของ lateral error, constraint violation และ speed/grip held-out",
    },
    "DS-012": {
        "question_en": "Can ex-ante technological radicalness be separated into new functionality and new technological/scientific origins using patent data?",
        "question_th": "จะใช้ข้อมูลสิทธิบัตรแยก radicalness เชิงเทคโนโลยีล่วงหน้าเป็น new functionality กับ new technological/scientific origins ได้หรือไม่?",
        "method_en": "The study operationalizes novelty with patent classifications and citation information, then validates indicators on a large patent-application sample using breakthrough outcomes and controls (pp. 2, 11-12).",
        "method_th": "งาน operationalize novelty ด้วย patent classification/citation แล้ว validate indicator บนตัวอย่าง patent application ขนาดใหญ่ด้วย breakthrough outcome และ control (หน้า 2, 11-12)",
        "findings_en": "New functionality and new origins are correlated but convey distinct information; correlations among separate dimension indicators are generally no more than 0.3, and the IPC4-level indicators show positive significant relationships with breakthrough probability (pp. 2, 11-12).",
        "findings_th": "new functionality กับ new origins มีความสัมพันธ์แต่ให้ข้อมูลต่างกัน correlation ระหว่าง indicator คนละมิติโดยทั่วไปไม่เกิน 0.3 และ indicator ระดับ IPC4 มีความสัมพันธ์บวกอย่างมีนัยสำคัญกับโอกาสเป็น breakthrough (หน้า 2, 11-12)",
        "interesting_en": "The paper shows why one novelty score is inadequate: a design can use unfamiliar knowledge without adding function, or add function from familiar origins.",
        "interesting_th": "paper แสดงว่าคะแนน novelty เดียวไม่พอ แบบหนึ่งอาจใช้ความรู้ต้นทางแปลกใหม่แต่ไม่เพิ่มหน้าที่ หรือเพิ่มหน้าที่จากต้นทางคุ้นเคย",
        "limitations_en": "Patent indicators depend on classification/citation practice, corpus, time, and the absence of consensus on radical innovation (p. 3). They cannot establish physical function, performance, or freedom to operate.",
        "limitations_th": "indicator สิทธิบัตรขึ้นกับวิธี classify/cite, corpus, เวลา และยังไม่มี consensus เรื่อง radical innovation (หน้า 3) จึงไม่ยืนยัน physical function, performance หรือ freedom to operate",
        "proposal_en": "Keep external novelty downstream: after causal function and fair performance pass, score new functionality and new origins separately with a dated prior-art corpus and human review; never use patent distance as a physics gate.",
        "proposal_th": "วาง external novelty ไว้ปลายทาง หลัง causal function และ fair performance ผ่าน ให้คะแนน new functionality กับ new origins แยกกันด้วย prior-art corpus ที่ระบุวันที่และ human review ห้ามใช้ patent distance เป็น physics gate",
    },
}


def load_category_metadata() -> dict[str, dict]:
    metadata = {}
    for path in sorted(SOURCES.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        metadata[payload["category"]["key"]] = payload["category"]
    return metadata


def evidence_profile(item: dict) -> tuple[list[str], list[str]]:
    text = " ".join(
        [item["title"]]
        + list(item.get("sections", {}).values())
        + [entry["text"] for entry in item.get("evidence_sentences", [])]
    ).lower()
    profiles: list[tuple[str, str, str]] = [
        (r"\b(review|survey|systematic review)\b", "review/synthesis", "งานทบทวน/สังเคราะห์"),
        (r"\b(dataset|benchmark|corpus)\b", "dataset/benchmark", "ชุดข้อมูล/benchmark"),
        (r"\b(fabricat|manufactur|prototype|wind tunnel|physical test|test rig|real[- ]world|on[- ]track)\b", "physical-test evidence", "หลักฐานการทดสอบกายภาพ"),
        (r"\b(experiment(?:al)?|ablation|empirical|user study)\b", "empirical/experimental evidence", "หลักฐานเชิงประจักษ์/การทดลอง"),
        (r"\b(simulat|numerical|finite element|cfd|computational)\b", "simulation/numerical evidence", "หลักฐาน simulation/เชิงตัวเลข"),
        (r"\b(theorem|proof|formal|mathematical)\b", "mathematical/formal evidence", "หลักฐานคณิตศาสตร์/เชิงรูปนัย"),
        (r"\b(optim|search|evolution|gradient|bayesian)\b", "optimization/search study", "การศึกษา optimization/search"),
        (r"\b(control|trajectory|mpc|policy|reinforcement learning)\b", "control/learning study", "การศึกษา control/learning"),
    ]
    en, th = [], []
    for pattern, label_en, label_th in profiles:
        if re.search(pattern, text):
            en.append(label_en)
            th.append(label_th)
    if not en:
        en, th = ["technical/methodological study"], ["การศึกษาเชิงเทคนิค/วิธีวิทยา"]
    return en[:4], th[:4]


def top_terms(item: dict, count: int = 8) -> str:
    return ", ".join(entry["term"] for entry in item.get("keywords", [])[:count])


def evidence_pages(item: dict, count: int = 8) -> str:
    if item.get("evidence_sentences"):
        pages = sorted({entry["page"] for entry in item["evidence_sentences"]})[:count]
    else:
        pages = item.get("evidence_pages", [])[:count]
    return ", ".join(str(page) for page in pages) if pages else "none detected"


def authors(item: dict) -> str:
    values = item.get("authors") or []
    return ", ".join(values) if values else "Not recorded in the curated source"


def split_relevance(text: str) -> tuple[str, str]:
    for separator in ("; ", ". "):
        if separator in text:
            claim, connection = text.split(separator, 1)
            return claim.rstrip("."), connection.rstrip(".")
    return text.rstrip("."), ""


def paper_action(item: dict, thai: bool) -> str:
    claim, _ = split_relevance(item["prior_relevance_th" if thai else "prior_relevance_en"])
    relation = item["relation"]
    if thai:
        if relation == "data":
            return f"ลงทะเบียนชุดข้อมูล/benchmark ที่เกี่ยวกับ '{claim}' พร้อม licence, domain, split และ leakage control แล้วใช้เฉพาะ calibration, pretraining หรือ independent test ตามที่ลงทะเบียน"
        if relation == "direct":
            return f"สร้าง matched-control pilot เพื่อทดสอบกลไกโดยตรงจากข้อค้นพบ '{claim}' ใน target ที่ระบุด้านล่าง"
        return f"สร้าง diagnostic pilot แบบจำกัดขอบเขตจาก '{claim}' และห้ามเปลี่ยน admitted evaluator จนกว่าจะผ่าน applicability test"
    if relation == "data":
        return f"Register the dataset or benchmark behind '{claim}' with licence, domain, split, and leakage controls, then use it only for the preregistered calibration, pretraining, or independent-test role."
    if relation == "direct":
        return f"Build a matched-control pilot that directly tests the mechanism in '{claim}' against the target below."
    return f"Build a bounded diagnostic pilot from '{claim}' and do not change an admitted evaluator until applicability testing passes."


def bibliography_value(item: dict, key: str) -> str:
    value = item.get("bibliography", {}).get(key)
    return str(value) if value else "Not recorded"


def principal_takeaway(item: dict, thai: bool, highlight: bool = False) -> str:
    override = PAPER_OVERRIDES.get(item["id"])
    if override:
        key = ("interesting_" if highlight else "findings_") + ("th" if thai else "en")
        return override[key]
    return item["prior_relevance_th" if thai else "prior_relevance_en"]


def report_en(item: dict, category: dict) -> str:
    guide = CATEGORY_GUIDANCE[item["category"]]
    transfer = PAPER_TRANSFER[item["category"]]
    override = PAPER_OVERRIDES.get(item["id"])
    profile_en, _ = evidence_profile(item)
    sections = ", ".join(sorted(item.get("sections", {}))) or "no reliable heading match"
    claim, interpretation = split_relevance(item["prior_relevance_en"])
    interesting = interpretation or (
        f"it makes {claim[0].lower() + claim[1:] if claim else item['title']} testable inside a registered {guide['theme_en'].lower()} study"
    )
    biblio = item.get("bibliography", {})
    url = biblio.get("landing_url") or biblio.get("download_url")
    canonical = f"[{url}]({url})" if url else "Not recorded"
    limitations_heading = "present" if "limitations" in item.get("sections", {}) else "not detected as a standalone heading"
    question_text = override["question_en"] if override else transfer["question_en"].format(title=item["title"])
    method_text = override["method_en"] if override else (
        f"The complete PDF was processed page by page. Its heuristic evidence profile is **{', '.join(profile_en)}**; "
        f"this label is a navigation aid, not an evidence grade. Located sections were {sections}, and frequent technical "
        f"terms were {top_terms(item)}. The paper-specific method or result selected for transfer review is: **{claim}**."
    )
    finding_text = override["findings_en"] if override else claim
    interesting_text = override["interesting_en"] if override else interesting
    connection_claim = interesting_text if override else claim
    limitation_text = override["limitations_en"] if override else transfer["boundary_en"]
    proposal_text = override["proposal_en"] if override else paper_action(item, thai=False)
    return f"""# {item['id']}: {item['title']}

Thai companion: `{item['id']}_review.th.md`

## Bibliographic and reading record

| Field | Value |
|---|---|
| Authors | {authors(item)} |
| Year | {item.get('year') or 'Not recorded'} |
| Venue | {bibliography_value(item, 'venue')} |
| DOI | {bibliography_value(item, 'doi')} |
| arXiv | {bibliography_value(item, 'arxiv_id')} |
| Canonical record | {canonical} |
| Library topic | {guide['theme_en']} |
| Project relation | `{item['relation']}` |
| Review depth | {'Decision-critical deep review' if override else 'Full-text transfer record'} |
| Source | [local PDF](../../../../{item['source_pdf']}) |
| Source SHA-256 | `{item['sha256']}` |
| Full-text coverage | {item['pages_with_text']}/{item['page_count']} pages ({item['text_coverage']:.2%}); {item['words']:,} extracted words |

## Research question

{question_text}

## Method and evidence

{method_text}

## Principal findings

- **Paper finding (conservative paraphrase):** {finding_text}
- **Reviewer interpretation:** {interesting_text}
- **Confidence:** moderate for identifying the transferable idea; no independent replication was performed.

## What is especially interesting

**Standout:** {interesting_text} This is a `{item['relation']}` contribution: it supplies a mechanism, dataset, comparator, or warning that can become a falsifiable project test rather than an appearance-based analogy.

## Limitations and transfer boundary

{limitation_text} An explicit `Limitations` heading was **{limitations_heading}** by automatic section detection. Regardless of heading, the paper does not validate a complete Formula Ultimate vehicle, and its evidence class cannot be promoted without project-specific verification, uncertainty analysis, and physical correlation.

## Connection to Formula Ultimate

The causal transfer hypothesis is: if **{connection_claim}** remains valid under Formula Ultimate's geometry, loads, budgets, and held-out race conditions, it should measurably improve or de-risk the **{transfer['target_en']}**. That hypothesis is not yet established; it must obey the Whole-Vehicle Technology Discovery Protocol's fixed-task, fair-budget, provenance, and promotion rules.

## Recommended project changes

| Transfer field | Paper-derived proposal |
|---|---|
| Target artifact/module | {transfer['target_en']} |
| Proposed change | {proposal_text} |
| Experiment and control | {transfer['test_en']} |
| Acceptance and failure evidence | {transfer['accept_en']} |

This is a project proposal, not a finding of the paper. If it changes a physical law, solver, dataset split, or admission rule, assign a new identity and rerun fair controls.

## Reading evidence

- Complete-file extraction: {item['page_count']} pages, {item['characters']:,} characters, {item['words']:,} words.
- Pages with substantial extractable text: {item['pages_with_text']}/{item['page_count']}.
- High-information cue pages sampled from across the paper: {evidence_pages(item)}. These are navigation locators, not substitutes for a pinpoint citation audit.
- Located section headings: {sections}.
- Extraction errors: {len(item.get('extraction_errors', []))}; likely scanned: `{str(item.get('likely_scanned', False)).lower()}`.
- This report separates paper finding, reviewer interpretation, and project proposal; it does not reproduce the paper or claim an independent replication.
"""


def report_th(item: dict, category: dict) -> str:
    guide = CATEGORY_GUIDANCE[item["category"]]
    transfer = PAPER_TRANSFER[item["category"]]
    override = PAPER_OVERRIDES.get(item["id"])
    _, profile_th = evidence_profile(item)
    sections = ", ".join(sorted(item.get("sections", {}))) or "ไม่พบ heading ที่เชื่อถือได้"
    claim, interpretation = split_relevance(item["prior_relevance_th"])
    interesting = interpretation or f"ทำให้ข้อค้นพบ '{claim}' กลายเป็นสมมติฐานที่ทดสอบได้ในหัวข้อ{guide['theme_th']}"
    biblio = item.get("bibliography", {})
    url = biblio.get("landing_url") or biblio.get("download_url")
    canonical = f"[{url}]({url})" if url else "ไม่ได้บันทึก"
    limitations_heading = "พบ" if "limitations" in item.get("sections", {}) else "ไม่พบเป็น heading แยก"
    question_text = override["question_th"] if override else transfer["question_th"].format(title=item["title"])
    method_text = override["method_th"] if override else (
        f"ประมวลผล PDF ทั้งฉบับทีละหน้า heuristic evidence profile คือ **{', '.join(profile_th)}** ป้ายนี้ใช้ช่วยนำทาง "
        f"ไม่ใช่ evidence grade ส่วนที่หาได้จาก heading คือ {sections} และคำเทคนิคที่พบบ่อย ได้แก่ {top_terms(item)} "
        f"วิธีหรือผลเฉพาะ paper ที่เลือกมาประเมินการถ่ายโอนคือ **{claim}**"
    )
    finding_text = override["findings_th"] if override else claim
    interesting_text = override["interesting_th"] if override else interesting
    connection_claim = interesting_text if override else claim
    limitation_text = override["limitations_th"] if override else transfer["boundary_th"]
    proposal_text = override["proposal_th"] if override else paper_action(item, thai=True)
    return f"""# {item['id']}: {item['title']}

English source: `{item['id']}_review.md`

## ระเบียนบรรณานุกรมและการอ่าน

| รายการ | ค่า |
|---|---|
| ผู้เขียน | {authors(item)} |
| ปี | {item.get('year') or 'ไม่ได้บันทึก'} |
| แหล่งตีพิมพ์ | {bibliography_value(item, 'venue')} |
| DOI | {bibliography_value(item, 'doi')} |
| arXiv | {bibliography_value(item, 'arxiv_id')} |
| ระเบียน canonical | {canonical} |
| หัวข้อในคลัง | {guide['theme_th']} |
| ความสัมพันธ์กับโครงการ | `{item['relation']}` |
| ระดับการทบทวน | {'deep review สำหรับการตัดสินใจ' if override else 'full-text transfer record'} |
| ต้นฉบับ | [PDF ในเครื่อง](../../../../{item['source_pdf']}) |
| SHA-256 ของต้นฉบับ | `{item['sha256']}` |
| coverage ของ full text | {item['pages_with_text']}/{item['page_count']} หน้า ({item['text_coverage']:.2%}); สกัดได้ {item['words']:,} คำ |

## คำถามวิจัย

{question_text}

## วิธีและหลักฐาน

{method_text}

## ผลสำคัญ

- **ผลจาก paper (ถอดความแบบระมัดระวัง):** {finding_text}
- **การตีความของผู้ทบทวน:** {interesting_text}
- **ความมั่นใจ:** ปานกลางสำหรับการระบุแนวคิดที่ถ่ายโอนได้ ยังไม่ได้ replicate ผลอย่างอิสระ

## ประเด็นที่น่าสนใจ

**จุดเด่น:** {interesting_text} โดยเป็นความเชื่อมโยงชนิด `{item['relation']}` ซึ่งให้กลไก ชุดข้อมูล ตัวเปรียบเทียบ หรือคำเตือนที่แปลงเป็นการทดสอบหักล้างได้ แทนการเทียบจากรูปลักษณ์

## ข้อจำกัดและขอบเขตการถ่ายโอน

{limitation_text} การตรวจ heading แบบอัตโนมัติ **{limitations_heading}** `Limitations` section อย่างไรก็ตาม paper นี้ไม่ validate รถ Formula Ultimate ทั้งคัน และห้ามยกระดับชั้นหลักฐานโดยไม่มี verification, uncertainty analysis และ physical correlation เฉพาะโครงการ

## ความเชื่อมโยงกับ Formula Ultimate

สมมติฐานการถ่ายโอนเชิงสาเหตุคือ หาก **{connection_claim}** ยังเป็นจริงภายใต้ geometry, load, budget และสนาม held-out ของ Formula Ultimate ก็ควรเพิ่มผลหรือช่วยลดความเสี่ยงของ **{transfer['target_th']}** อย่างวัดได้ ขณะนี้สมมติฐานนี้ยังไม่ถูกยืนยัน และต้องทำตามกฎ fixed task, fair budget, provenance และ promotion ของ Whole-Vehicle Technology Discovery Protocol

## ข้อเสนอปรับปรุงโครงการ

| ช่องการถ่ายโอน | ข้อเสนอจาก paper |
|---|---|
| artifact/module เป้าหมาย | {transfer['target_th']} |
| การเปลี่ยนแปลงที่เสนอ | {proposal_text} |
| experiment และ control | {transfer['test_th']} |
| หลักฐานผ่านและล้มเหลว | {transfer['accept_th']} |

ส่วนนี้เป็นข้อเสนอโครงการ ไม่ใช่ผลจาก paper หากเปลี่ยนกฎฟิสิกส์ solver dataset split หรือ admission rule ต้องสร้าง identity ใหม่และรัน control ที่ยุติธรรมใหม่

## หลักฐานการอ่าน

- สกัดครบทั้งไฟล์: {item['page_count']} หน้า, {item['characters']:,} ตัวอักษร, {item['words']:,} คำ
- หน้าที่มีข้อความสกัดได้ในระดับสาระ: {item['pages_with_text']}/{item['page_count']}
- หน้าตัวอย่าง high-information cue ที่กระจายทั่ว paper: {evidence_pages(item)} เป็นตำแหน่งนำทาง ไม่แทน pinpoint citation audit
- heading ที่ระบุตำแหน่งได้: {sections}
- extraction error: {len(item.get('extraction_errors', []))}; มีแนวโน้มเป็นสแกน: `{str(item.get('likely_scanned', False)).lower()}`
- รายงานนี้แยกผลจาก paper การตีความของผู้ทบทวน และข้อเสนอโครงการ ไม่ได้ทำซ้ำเนื้อหา paper หรืออ้างว่า replicate ผลอย่างอิสระ
"""


def combined_report(items: list[dict], categories: dict[str, dict], thai: bool) -> str:
    by_category: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        by_category[item["category"]].append(item)
    total_pages = sum(item["page_count"] for item in items)
    total_words = sum(item["words"] for item in items)

    if thai:
        parts = [f"""# รายงานสังเคราะห์ paper ทั้งคลังสำหรับ Formula Ultimate

English source: `FULL_LIBRARY_SYNTHESIS_2026-09-28.md`

วันที่อ่าน: 2026-09-28 (Asia/Bangkok)

## ขอบเขตและวิธี

รายงานนี้ครอบคลุม PDF ทุกฉบับที่มีอยู่ใน `papers/` ณ เวลาสกัด: **{len(items)} ฉบับ, {total_pages:,} หน้า, ประมาณ {total_words:,} คำที่สกัดได้** อ่าน full text ทีละหน้าและสร้าง reading manifest ที่ผูก source path, SHA-256, page coverage, section cue และ evidence-cue page จากนั้นสังเคราะห์ผลตาม 15 หัวข้อของคลัง

ใช้ระดับความลึกสองชั้น: paper ที่มีผลต่อการตัดสินใจสูง {len(PAPER_OVERRIDES)} ฉบับได้รับ deep review ที่ระบุวิธี ตัวเลข ผล ข้อจำกัด เลขหน้า และ proposal เฉพาะ ส่วนอีก {len(items) - len(PAPER_OVERRIDES)} ฉบับได้รับ full-text transfer record ที่ผูกข้อค้นพบที่คัดสรรกับ target, experiment/control และเกณฑ์ผ่าน/ล้มเหลวเฉพาะหัวข้อ จึงไม่ควรอ่าน record ชั้นหลังว่าเทียบเท่า critical replication

ข้อจำกัดสำคัญ: การอ่าน paper ไม่ใช่การ replicate ผล การคำนวณหรือการทดลองของผู้เขียนยังไม่ได้รันซ้ำ และผลจาก simulation/benchmark/review ไม่ถูกยกระดับเป็น physical validation ของ Formula Ultimate

PDF 6 ฉบับมี text coverage ต่ำกว่า 95% จึง render และตรวจหน้าที่มีข้อความน้อย พบว่าเป็นหน้าภาพล้วน (field CFD, ตารางภาพ geometry, diagram หรือภาพชุดข้อมูล) หรือหน้าท้ายว่าง ไม่ใช่เนื้อความสแกนที่อ่านตกหล่น และไม่มี PDF ใดถูกจัดว่าเป็นสแกนที่อ่านไม่ได้

## ข้อสรุปรวม

1. งานทั้งหมดสนับสนุนให้ Formula Ultimate คงเป้าหมายแบบ open-ended แต่ **ต้องเปิดกว้างภายใน constraint และ evidence gate ที่ชัด** ไม่ใช่ปล่อย generator ไม่มีขอบเขต
2. ประเด็นร่วมที่แรงที่สุดคือ **representation, evaluator และ budget เป็นส่วนหนึ่งของผลการค้นพบ** ไม่ใช่รายละเอียด implementation ที่ละเลยได้
3. geometry ที่ดูใหม่ต้องผ่านลำดับ: สร้างได้จริง -> มี causal physical response -> ทำงานใน assembly/vehicle -> ดีกว่า baseline ที่ optimize อย่างยุติธรรม -> รอด higher fidelity/holdout -> จึงพิจารณาความใหม่ภายนอก
4. ช่องว่างเร่งด่วนที่สุดยังตรงกับ roadmap ปัจจุบัน: tyre/contact transient, aero field, energy/thermal endurance, independently recovered structural evidence, tolerance/fatigue และ coupled whole-vehicle replay
5. AI agent และ generative model ควรเพิ่มอัตราการเสนอและซ่อม artifact แต่ห้ามเป็นผู้ตัดสินความถูกต้องของ artifact ที่ตัวเองสร้าง
6. QD/multifidelity เหมาะกับโจทย์ แต่ต้องมี descriptor versioning, uncertainty, false-negative audit, resource ledger และ untouched holdout
7. ข้อมูลสาธารณะใช้ calibrate, pretrain และตรวจ pipeline ได้ แต่ต้องประกาศ domain shift และกันข้อมูลโครงการไว้ทดสอบอิสระ
8. งานแข่งอัตโนมัติชี้ว่าต้องมี controller baseline ที่แข็งแรง มิฉะนั้นอาจให้เครดิตรูปร่างรถกับความต่างของ controller

## ลำดับการปรับปรุงที่เสนอ

1. **ทำ evaluator ให้เชื่อถือได้ก่อนเพิ่ม search:** ปิดช่องว่าง field equilibrium/contact/tyre/aero/thermal-energy และบันทึก invalid/numerical failure เป็นผล
2. **เชื่อม transient ทั้งรถ:** รวม vehicle, tyre, aero, energy, brake, thermal และ controller ใน objective เวลารวมการแข่งขัน พร้อม finish gate
3. **ทำ search ให้ยุติธรรม:** matched seed/compute/evaluator access, controller-allocation fairness, fixed-topology optimized baselines และ resource accounting
4. **ทำ multifidelity promotion ให้ตรวจสอบได้:** uncertainty envelope, discrepancy model, stratified audit และ independent replay
5. **เพิ่ม evidence จากของจริงตามลำดับ:** specimen -> connection/subsystem -> assembly -> vehicle โดยห้ามข้ามระดับด้วย claim จาก simulation
6. **แยก claim สี่ชนิด:** geometric novelty, causal functional difference, performance superiority และ external technology novelty
"""]
    else:
        parts = [f"""# Full Paper-Library Synthesis for Formula Ultimate

Thai companion: `FULL_LIBRARY_SYNTHESIS_2026-09-28.th.md`

Reading date: 2026-09-28 (Asia/Bangkok)

## Scope and method

This report covers every PDF present under `papers/` at extraction time: **{len(items)} papers, {total_pages:,} pages, and approximately {total_words:,} extracted words**. Full text was processed page by page into a reading manifest binding source path, SHA-256, page coverage, section cues, and high-information cue pages. The evidence was then synthesized across the library's 15 topics.

Two review depths are explicit: {len(PAPER_OVERRIDES)} decision-critical papers receive deep reviews with methods, numbers, findings, limitations, page locators, and paper-specific proposals; the other {len(items) - len(PAPER_OVERRIDES)} receive full-text transfer records binding a curated takeaway to a topic-specific target, experiment/control, and pass/fail evidence. The latter should not be read as equivalent to a critical replication.

Important boundary: reading is not replication. The authors' computations and experiments were not independently rerun, and simulation, benchmark, or review evidence is not promoted to physical validation of Formula Ultimate.

Six PDFs had text coverage below 95%. Their low-text pages were rendered and inspected: they were figure-only plates (CFD fields, geometry grids, diagrams, or dataset visualizations) or a blank trailing page, not unread scanned prose. No PDF was classified as an unreadable scan.

## Cross-library conclusions

1. The literature supports an open-ended Formula Ultimate objective, but openness must operate inside explicit physical constraints and evidence gates.
2. Representation, evaluator, and compute allocation are part of the discovery result, not implementation details that can be ignored.
3. Novel-looking geometry must pass a ladder: constructible geometry -> causal physical response -> assembly/vehicle function -> fair superiority over optimized baselines -> higher-fidelity and holdout survival -> external novelty assessment.
4. The most urgent gaps still match the current roadmap: transient tyre/contact, aero fields, energy/thermal endurance, independently recovered structural evidence, tolerance/fatigue, and coupled whole-vehicle replay.
5. AI agents and generative models should increase proposal and repair throughput, but must not judge the correctness of their own artifacts.
6. QD and multifidelity search fit the problem only with descriptor versioning, uncertainty, false-negative audits, resource ledgers, and untouched holdouts.
7. Public data can calibrate, pretrain, and test pipelines, but domain shift must be declared and project-specific conditions must remain independently held out.
8. Autonomous-racing work shows the need for a strong optimized controller baseline before attributing gains to vehicle morphology.

## Prioritized project improvements

1. **Credible evaluators before more search:** close field-equilibrium, contact, tyre, aero, and thermal-energy gaps; retain invalid and numerical failures as outcomes.
2. **Coupled full-race transient:** combine vehicle, tyre, aero, energy, brake, thermal, and controller states under total race time and a finish gate.
3. **Fair search:** matched seeds, compute, evaluator access, controller allocation, optimized fixed-topology baselines, and resource accounting.
4. **Auditable multifidelity promotion:** uncertainty envelopes, discrepancy models, stratified audits, and independent replay.
5. **Progressive physical evidence:** specimen -> connection/subsystem -> assembly -> vehicle; never skip stages using simulation claims.
6. **Four separate claims:** geometric novelty, causal functional difference, performance superiority, and external technology novelty.
"""]

    for key in sorted(by_category, key=lambda value: categories[value]["folder"]):
        cat = categories[key]
        guide = CATEGORY_GUIDANCE[key]
        papers = sorted(by_category[key], key=lambda item: item["id"])
        paper_by_id = {item["id"]: item for item in papers}
        highlights = [paper_by_id[paper_id] for paper_id in HIGHLIGHT_IDS[key] if paper_id in paper_by_id]
        profiles = Counter(label for item in papers for label in evidence_profile(item)[1 if thai else 0])
        if thai:
            parts.append(f"\n## {key}: {cat['title_th']}\n\n**ขอบเขต:** {cat['scope_th']}\n\n**สิ่งที่พบข้าม paper**\n")
            parts.extend(f"- {finding}\n" for finding in guide["findings_th"])
            parts.append("\n**สิ่งที่น่าสนใจ**\n\n")
            for item in highlights:
                parts.append(f"- [{item['id']}](by_paper/{item['id']}_review.th.md): {principal_takeaway(item, thai=True, highlight=True)}\n")
            parts.append(f"\nชุด {len(papers)} ฉบับมี evidence profile หลักคือ " + ", ".join(f"{name} ({count})" for name, count in profiles.most_common()) + " ความตึงเครียดร่วมคือผลที่ดูดีมักขึ้นกับ representation, fidelity และ test condition จึงต้องทดสอบ transfer แทนการยืม claim โดยตรง\n\n")
            parts.append("**ควรปรับปรุงส่วนใดในงานเรา**\n")
            parts.extend(f"- {action}\n" for action in guide["actions_th"])
            parts.append("\n**รายงานรายฉบับและข้อค้นพบหลัก**\n")
            for item in papers:
                depth = "**deep review** — " if item["id"] in PAPER_OVERRIDES else ""
                parts.append(f"- [{item['id']}: {item['title']}](by_paper/{item['id']}_review.th.md) — {depth}{principal_takeaway(item, thai=True)}\n")
        else:
            parts.append(f"\n## {key}: {cat['title_en']}\n\n**Scope:** {cat['scope_en']}\n\n**Cross-paper findings**\n")
            parts.extend(f"- {finding}\n" for finding in guide["findings_en"])
            parts.append("\n**What is especially interesting**\n\n")
            for item in highlights:
                parts.append(f"- [{item['id']}](by_paper/{item['id']}_review.md): {principal_takeaway(item, thai=False, highlight=True)}\n")
            parts.append(f"\nAcross these {len(papers)} papers, the leading evidence profiles are " + ", ".join(f"{name} ({count})" for name, count in profiles.most_common()) + ". The shared tension is that apparent success is conditional on representation, fidelity, and test conditions, so transfer must be tested instead of borrowed.\n\n")
            parts.append("**Where Formula Ultimate should improve**\n")
            parts.extend(f"- {action}\n" for action in guide["actions_en"])
            parts.append("\n**Per-paper reports and principal takeaways**\n")
            for item in papers:
                depth = "**deep review** — " if item["id"] in PAPER_OVERRIDES else ""
                parts.append(f"- [{item['id']}: {item['title']}](by_paper/{item['id']}_review.md) — {depth}{principal_takeaway(item, thai=False)}\n")

    if thai:
        parts.append("\n## ข้อจำกัดของรายงาน\n\n- คลังนี้ครอบคลุมเฉพาะ PDF ที่อยู่ใน `papers/` ณ วันที่อ่าน ไม่ใช่ systematic review ที่ค้นครบทุกฐานข้อมูล\n- section detection เป็นตัวช่วยนำทางและพลาด heading ที่จัดรูปแบบไม่ปกติได้ แต่ coverage และคำรวมคำนวณจากทุกหน้า\n- รายงานรายฉบับเป็นการอ่านเชิงถ่ายโอนสู่โครงการ ไม่แทน critical replication หรือการประเมินคุณภาพทางสถิติเต็มรูปแบบ\n")
    else:
        parts.append("\n## Report limitations\n\n- This library covers PDFs present under `papers/` on the reading date; it is not an exhaustive database systematic review.\n- Section detection is a navigation aid and can miss unusually formatted headings, while page coverage and word totals are computed across every page.\n- Per-paper reports are project-transfer readings, not critical replications or complete statistical-quality appraisals.\n")
    return "".join(parts)


def main() -> int:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = []
    for public_item in payload["papers"]:
        digest_path = CORPUS / f"{public_item['id']}.json"
        digest = json.loads(digest_path.read_text(encoding="utf-8"))
        items.append({**public_item, **digest})
    categories = load_category_metadata()
    missing = sorted(set(item["category"] for item in items) - set(CATEGORY_GUIDANCE))
    if missing:
        raise ValueError(f"Missing category guidance: {missing}")
    BY_PAPER.mkdir(parents=True, exist_ok=True)
    for item in items:
        category = categories[item["category"]]
        (BY_PAPER / f"{item['id']}_review.md").write_text(report_en(item, category), encoding="utf-8")
        (BY_PAPER / f"{item['id']}_review.th.md").write_text(report_th(item, category), encoding="utf-8")
    (OUTPUT / "FULL_LIBRARY_SYNTHESIS_2026-09-28.md").write_text(
        combined_report(items, categories, thai=False), encoding="utf-8"
    )
    (OUTPUT / "FULL_LIBRARY_SYNTHESIS_2026-09-28.th.md").write_text(
        combined_report(items, categories, thai=True), encoding="utf-8"
    )
    print(f"Generated {len(items) * 2} per-paper reports and 2 synthesis reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
