"""Independent 3D frame finite-element evaluator and CalculiX B31 adapter."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence

import numpy as np

from formula_ultimate.topology.vehicle_assembly import from_mapping, validate


FRAME_EVALUATOR_IDENTITY = "project_frame6dof_plus_calculix_b31_section_force_v2"


class VehicleFrameError(ValueError):
    """Raised when frame evidence is invalid, singular, or incomplete."""


@dataclass(frozen=True, slots=True)
class FrameSection:
    section_id: str
    width_m: float
    height_m: float


@dataclass(frozen=True, slots=True)
class FrameElement:
    element_id: int
    node_a: int
    node_b: int
    section_id: str


@dataclass(frozen=True, slots=True)
class FrameModel:
    nodes: tuple[tuple[int, tuple[float, float, float]], ...]
    elements: tuple[FrameElement, ...]
    sections: tuple[FrameSection, ...]
    fixed_node_id: int
    component_node_ids: tuple[tuple[str, int], ...]


@dataclass(frozen=True, slots=True)
class FrameSolveResult:
    maximum_displacement_m: float
    maximum_von_mises_pa: float
    support_reaction: tuple[float, float, float, float, float, float]
    equilibrium_residual: tuple[float, float, float, float, float, float]
    node_displacements: tuple[tuple[int, tuple[float, float, float, float, float, float]], ...]
    element_von_mises_pa: tuple[tuple[int, float], ...]
    result_sha256: str


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def _norm(vector: Sequence[float]) -> float:
    return math.sqrt(math.fsum(float(item) ** 2 for item in vector))


def _cross(a: Sequence[float], b: Sequence[float]) -> tuple[float, float, float]:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def _basis(a: Sequence[float], b: Sequence[float]) -> np.ndarray:
    ex = np.asarray(b, dtype=float) - np.asarray(a, dtype=float)
    length = np.linalg.norm(ex)
    if not math.isfinite(float(length)) or length <= 0.0:
        raise VehicleFrameError("frame element length must be positive")
    ex /= length
    reference = np.array((0.0, 0.0, 1.0)) if abs(float(ex[2])) < 0.9 else np.array((1.0, 0.0, 0.0))
    ey = reference - np.dot(reference, ex) * ex
    ey /= np.linalg.norm(ey)
    ez = np.cross(ex, ey)
    return np.vstack((ex, ey, ez))


def _torsion_constant(width: float, height: float) -> float:
    long_side, short_side = max(width, height), min(width, height)
    ratio = short_side / long_side
    return long_side * short_side**3 * (1.0/3.0 - 0.21*ratio*(1.0-ratio**4/12.0))


def _local_stiffness(length: float, section: FrameSection, young: float, poisson: float) -> np.ndarray:
    if young <= 0.0 or not -1.0 < poisson < 0.5:
        raise VehicleFrameError("material stiffness is invalid")
    width, height = section.width_m, section.height_m
    if width <= 0.0 or height <= 0.0:
        raise VehicleFrameError("frame section dimensions must be positive")
    area = width * height
    iy = width * height**3 / 12.0
    iz = height * width**3 / 12.0
    shear = young / (2.0 * (1.0 + poisson))
    torsion = _torsion_constant(width, height)
    matrix = np.zeros((12, 12), dtype=float)
    axial = young * area / length
    matrix[0,0]=matrix[6,6]=axial; matrix[0,6]=matrix[6,0]=-axial
    twist = shear * torsion / length
    matrix[3,3]=matrix[9,9]=twist; matrix[3,9]=matrix[9,3]=-twist
    def bending(indices, inertia, sign):
        v1,r1,v2,r2=indices
        a=12*young*inertia/length**3; b=sign*6*young*inertia/length**2
        c=4*young*inertia/length; d=2*young*inertia/length
        values=((v1,v1,a),(v1,r1,b),(v1,v2,-a),(v1,r2,b),
                (r1,v1,b),(r1,r1,c),(r1,v2,-b),(r1,r2,d),
                (v2,v1,-a),(v2,r1,-b),(v2,v2,a),(v2,r2,-b),
                (r2,v1,b),(r2,r1,d),(r2,v2,-b),(r2,r2,c))
        for i,j,value in values: matrix[i,j]=value
    bending((1,5,7,11), iz, 1.0)
    bending((2,4,8,10), iy, -1.0)
    return matrix


def _element_matrices(a, b, section, young, poisson):
    length = _norm(tuple(float(b[i])-float(a[i]) for i in range(3)))
    local = _local_stiffness(length, section, young, poisson)
    rotation = _basis(a, b)
    transform = np.zeros((12,12), dtype=float)
    for start in (0,3,6,9): transform[start:start+3,start:start+3] = rotation
    return local, transform, transform.T @ local @ transform


def build_vehicle_frame(assembly_raw: Mapping[str, Any], subdivisions: int) -> FrameModel:
    if not isinstance(subdivisions, int) or isinstance(subdivisions, bool) or subdivisions <= 0:
        raise VehicleFrameError("subdivisions must be a positive integer")
    assembly = from_mapping(assembly_raw); validate(assembly)
    components = {item.component_id:item for item in assembly.components}
    interfaces = {item["interface_id"]:item for item in assembly.interfaces}
    ground_interface = interfaces[assembly.contacts[0]["interface_id"]]
    ground_component = components[ground_interface["component_id"]]
    ground = tuple(ground_component.position[i] + float(ground_interface["local_position_m"][i]) for i in range(3))
    endpoints = {"ground":ground,"core":components["core"].position,"source":components["source"].position,"propulsor":components["propulsor"].position}
    source_dims=components["source"].dims; prop_dims=components["propulsor"].dims; radius=components["contact_alpha"].dims[0]
    sections=(FrameSection("support",2*radius,2*radius),FrameSection("source",source_dims[1],source_dims[2]),FrameSection("propulsor",prop_dims[1],prop_dims[2]))
    nodes=[]; node_by_key={}; next_node=1
    def node(key,position):
        nonlocal next_node
        if key not in node_by_key:
            node_by_key[key]=next_node; nodes.append((next_node,tuple(float(x) for x in position))); next_node+=1
        return node_by_key[key]
    root=node("ground",endpoints["ground"]); core=node("core",endpoints["core"])
    elements=[]; next_element=1
    for start_name,end_name,section_id in (("ground","core","support"),("core","source","source"),("core","propulsor","propulsor")):
        start_pos,end_pos=endpoints[start_name],endpoints[end_name]; prior=node(start_name,start_pos)
        for index in range(1,subdivisions+1):
            fraction=index/subdivisions; position=tuple(start_pos[j]+fraction*(end_pos[j]-start_pos[j]) for j in range(3))
            key=end_name if index==subdivisions else f"{start_name}-{end_name}-{index}/{subdivisions}"; current=node(key,position)
            elements.append(FrameElement(next_element,prior,current,section_id));next_element+=1;prior=current
    return FrameModel(tuple(nodes),tuple(elements),sections,root,(("core",core),("source",node_by_key["source"]),("propulsor",node_by_key["propulsor"])))


def loads_from_work048(model: FrameModel, case: Mapping[str, Any], mass_ratio: float, centre_of_mass_m: Sequence[float]) -> dict[int, tuple[float,...]]:
    if not math.isfinite(mass_ratio) or mass_ratio <= 0.0: raise VehicleFrameError("mass ratio must be positive")
    connections={item["connection_id"]:tuple(float(x) for x in item["force_n"]+item["moment_nm"]) for item in case["connection_loads"]}
    for required in ("energy_core","core_propulsor","core_contact"):
        if required not in connections: raise VehicleFrameError("Work 048 connection load is incomplete")
    source=tuple(-x for x in connections["energy_core"]); propulsor=tuple(-x for x in connections["core_propulsor"])
    core=tuple(-connections["core_contact"][i]+connections["energy_core"][i]+connections["core_propulsor"][i] for i in range(6))
    nodes=dict(model.nodes); component_nodes=dict(model.component_node_ids); loads={}
    for name,wrench in (("core",core),("source",source),("propulsor",propulsor)):
        force=tuple(mass_ratio*x for x in wrench[:3]); moment_com=tuple(mass_ratio*x for x in wrench[3:])
        position=nodes[component_nodes[name]]; arm=tuple(position[i]-float(centre_of_mass_m[i]) for i in range(3)); arm_cross=_cross(arm,force)
        moment=tuple(moment_com[i]-arm_cross[i] for i in range(3)); loads[component_nodes[name]]=force+moment
    return loads


def solve_frame(model: FrameModel, loads: Mapping[int, Sequence[float]], young: float, poisson: float) -> FrameSolveResult:
    nodes=dict(model.nodes); sections={item.section_id:item for item in model.sections}; index={node_id:i for i,node_id in enumerate(nodes)}
    dof=6*len(nodes); stiffness=np.zeros((dof,dof),dtype=float); force=np.zeros(dof,dtype=float); element_cache={}
    for element in model.elements:
        local,transform,global_matrix=_element_matrices(nodes[element.node_a],nodes[element.node_b],sections[element.section_id],young,poisson)
        ids=list(range(6*index[element.node_a],6*index[element.node_a]+6))+list(range(6*index[element.node_b],6*index[element.node_b]+6))
        stiffness[np.ix_(ids,ids)] += global_matrix; element_cache[element.element_id]=(local,transform,ids,sections[element.section_id])
    for node_id,wrench in loads.items():
        if node_id not in index or len(wrench)!=6: raise VehicleFrameError("nodal load identity or size is invalid")
        force[6*index[node_id]:6*index[node_id]+6] += np.asarray(wrench,dtype=float)
    fixed=np.arange(6*index[model.fixed_node_id],6*index[model.fixed_node_id]+6); free=np.setdiff1d(np.arange(dof),fixed)
    try: displacement=np.zeros(dof); displacement[free]=np.linalg.solve(stiffness[np.ix_(free,free)],force[free])
    except np.linalg.LinAlgError as exc: raise VehicleFrameError("frame stiffness matrix is singular") from exc
    if not np.all(np.isfinite(displacement)): raise VehicleFrameError("frame displacement is non-finite")
    reaction=stiffness@displacement-force; support=tuple(float(reaction[item]) for item in fixed)
    total_force=np.zeros(3); total_moment=np.zeros(3); root=np.asarray(nodes[model.fixed_node_id])
    for node_id,wrench in loads.items():
        applied=np.asarray(wrench,dtype=float); total_force+=applied[:3]; total_moment+=applied[3:]+np.cross(np.asarray(nodes[node_id])-root,applied[:3])
    residual=tuple(float(support[i]+total_force[i]) for i in range(3))+tuple(float(support[i+3]+total_moment[i]) for i in range(3))
    stresses=[]
    for element in model.elements:
        local,transform,ids,section=element_cache[element.element_id]; end_forces=local@(transform@displacement[ids])
        area=section.width_m*section.height_m; iy=section.width_m*section.height_m**3/12; iz=section.height_m*section.width_m**3/12; torsion=_torsion_constant(section.width_m,section.height_m); values=[]
        for offset in (0,6):
            axial=abs(end_forces[offset])/area
            normal=axial+abs(end_forces[offset+4])*section.height_m/(2*iy)+abs(end_forces[offset+5])*section.width_m/(2*iz)
            shear=1.5*math.hypot(end_forces[offset+1],end_forces[offset+2])/area+abs(end_forces[offset+3])*max(section.width_m,section.height_m)/(2*torsion)
            values.append(math.sqrt(normal*normal+3*shear*shear))
        stresses.append((element.element_id,max(values)))
    node_displacements=tuple((node_id,tuple(float(x) for x in displacement[6*i:6*i+6])) for node_id,i in sorted(index.items()))
    maximum_displacement=max(_norm(values[:3]) for _,values in node_displacements); maximum_stress=max(value for _,value in stresses)
    draft={"maximum_displacement_m":maximum_displacement,"maximum_von_mises_pa":maximum_stress,"support_reaction":support,"equilibrium_residual":residual,"node_displacements":node_displacements,"element_von_mises_pa":stresses}
    return FrameSolveResult(maximum_displacement,maximum_stress,support,residual,node_displacements,tuple(stresses),canonical_sha256(draft))


def build_calculix_b31_deck(
    model: FrameModel,
    loads: Mapping[int, Sequence[float]],
    young: float,
    poisson: float,
    output_section_id: str | None = None,
    *,
    geometric_nonlinear: bool = False,
) -> str:
    nodes=dict(model.nodes); lines=["*HEADING","Work 052 independent vehicle frame","*NODE,NSET=NALL"]
    lines += [f"{node},{position[0]:.12E},{position[1]:.12E},{position[2]:.12E}" for node,position in model.nodes]
    for section in model.sections:
        chosen=[item for item in model.elements if item.section_id==section.section_id]; lines.append(f"*ELEMENT,TYPE=B31,ELSET=E_{section.section_id.upper()}"); lines += [f"{item.element_id},{item.node_a},{item.node_b}" for item in chosen]
    lines += ["*NSET,NSET=FIXED",str(model.fixed_node_id),"*MATERIAL,NAME=MAT","*ELASTIC",f"{young:.12E},{poisson:.12E}"]
    for section in model.sections:
        first=next(item for item in model.elements if item.section_id==section.section_id); reference=_basis(nodes[first.node_a],nodes[first.node_b])[1]
        lines += [f"*BEAM SECTION,ELSET=E_{section.section_id.upper()},MATERIAL=MAT,SECTION=RECT",f"{section.width_m:.12E},{section.height_m:.12E}",f"{reference[0]:.12E},{reference[1]:.12E},{reference[2]:.12E}"]
    if geometric_nonlinear:
        lines += ["*STEP,NLGEOM", "*STATIC", "1.000000E-01,1.000000E+00,1.000000E-05,1.000000E-01"]
    else:
        lines += ["*STEP", "*STATIC"]
    lines += ["*BOUNDARY","FIXED,1,6,0","*CLOAD"]
    for node_id in sorted(loads):
        for component,value in enumerate(loads[node_id],1):
            if value: lines.append(f"{node_id},{component},{float(value):.12E}")
    if output_section_id is None:
        if len(model.sections) != 1:
            raise VehicleFrameError("CalculiX section output must identify one section")
        output_section_id = model.sections[0].section_id
    if output_section_id not in {section.section_id for section in model.sections}:
        raise VehicleFrameError(f"unknown CalculiX output section {output_section_id}")
    output_set = f"E_{output_section_id.upper()}"
    lines += ["*NODE FILE,OUTPUT=2D","U",f"*EL FILE,ELSET={output_set},SECTION FORCES","S,NOE","*NODE PRINT,NSET=NALL","U"]
    for section in model.sections: lines += [f"*EL PRINT,ELSET=E_{section.section_id.upper()}","S"]
    lines += ["*END STEP",""]; return "\n".join(lines)


def parse_calculix_b31_dat(text: str) -> dict[str, Any]:
    displacement_rows=[]; stress_rows=[]; mode=None
    for line in text.splitlines():
        lower=line.lower()
        if "displacements (vx,vy,vz)" in lower: mode="u"; continue
        if "stresses (elem, integ.pnt." in lower: mode="s"; continue
        fields=line.split()
        if mode=="u" and len(fields)==4 and fields[0].isdigit(): displacement_rows.append((int(fields[0]),tuple(float(x) for x in fields[1:4])))
        elif mode=="s" and len(fields)==8 and fields[0].isdigit() and fields[1].isdigit():
            tensor=tuple(float(x) for x in fields[2:8]); sx,sy,sz,txy,txz,tyz=tensor
            von=math.sqrt(0.5*((sx-sy)**2+(sy-sz)**2+(sz-sx)**2)+3*(txy*txy+txz*txz+tyz*tyz)); stress_rows.append((int(fields[0]),int(fields[1]),tensor,von))
    if not displacement_rows: raise VehicleFrameError("CalculiX displacement table is missing")
    if not stress_rows: raise VehicleFrameError("CalculiX stress table is missing")
    if not all(math.isfinite(x) for _,row in displacement_rows for x in row) or not all(math.isfinite(row[3]) for row in stress_rows): raise VehicleFrameError("CalculiX evidence is non-finite")
    return {"node_displacements":displacement_rows,"stress_rows":stress_rows,"maximum_displacement_m":max(_norm(row) for _,row in displacement_rows),"maximum_von_mises_pa":max(row[3] for row in stress_rows)}


def parse_calculix_section_forces_frd(text: str) -> list[tuple[int, tuple[float, ...]]]:
    """Parse one OUTPUT=2D, SECTION FORCES result block from CalculiX FRD."""
    rows: list[tuple[int, tuple[float, ...]]] = []
    in_section_forces = False
    for line in text.splitlines():
        if line.startswith(" -4"):
            in_section_forces = line[4:16].strip() == "STRESS"
            continue
        if in_section_forces and line.startswith(" -3"):
            in_section_forces = False
            continue
        if not in_section_forces or not line.startswith(" -1"):
            continue
        fields = re.findall(r"[-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?", line)
        if len(fields) != 8 or fields[0] != "-1" or not fields[1].isdigit():
            raise VehicleFrameError("CalculiX section-force FRD row is malformed")
        values = tuple(float(value) for value in fields[2:8])
        if not all(math.isfinite(value) for value in values):
            raise VehicleFrameError("CalculiX section-force evidence is non-finite")
        rows.append((int(fields[1]), values))
    if not rows:
        raise VehicleFrameError("CalculiX section-force FRD block is missing")
    return rows


def section_force_extreme_von_mises(
    rows: Sequence[tuple[int, Sequence[float]]], section: FrameSection
) -> float:
    """Convert B31 section resultants to conservative rectangular surface stress."""
    area = section.width_m * section.height_m
    iy = section.width_m * section.height_m**3 / 12
    iz = section.height_m * section.width_m**3 / 12
    torsion = _torsion_constant(section.width_m, section.height_m)
    maximum = 0.0
    for _, values in rows:
        if len(values) != 6:
            raise VehicleFrameError("CalculiX section-force row must contain six resultants")
        shear_1, shear_2, normal_force, torque, moment_1, moment_2 = (float(value) for value in values)
        normal = (
            abs(normal_force) / area
            + abs(moment_1) * section.height_m / (2 * iy)
            + abs(moment_2) * section.width_m / (2 * iz)
        )
        shear = (
            1.5 * math.hypot(shear_1, shear_2) / area
            + abs(torque) * max(section.width_m, section.height_m) / (2 * torsion)
        )
        maximum = max(maximum, math.sqrt(normal * normal + 3 * shear * shear))
    return maximum


def analytical_cantilever(length: float, side: float, force: float, young: float) -> dict[str,float]:
    if min(length,side,force,young)<=0: raise VehicleFrameError("cantilever inputs must be positive")
    inertia=side**4/12; return {"tip_displacement_m":force*length**3/(3*young*inertia),"maximum_bending_stress_pa":6*force*length/side**3}


def benchmark_model(length: float, side: float, subdivisions: int) -> tuple[FrameModel,dict[int,tuple[float,...]]]:
    nodes=tuple((index+1,(length*index/subdivisions,0.0,0.0)) for index in range(subdivisions+1)); elements=tuple(FrameElement(index,index,index+1,"beam") for index in range(1,subdivisions+1)); model=FrameModel(nodes,elements,(FrameSection("beam",side,side),),1,(("tip",subdivisions+1),)); return model,{subdivisions+1:(0.0,-1.0,0.0,0.0,0.0,0.0)}
