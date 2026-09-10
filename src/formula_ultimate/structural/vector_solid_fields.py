"""Sparse linear tetrahedral vector solid mechanics for Work 111."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping

import numpy as np


PROTOCOL_VERSION = "vector_solid_fields_v1"


class VectorSolidViolation(ValueError):
    pass


def canonical_sha256(value: Any) -> str:
    try: data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()
    except (TypeError, ValueError) as exc: raise VectorSolidViolation("field evidence must be finite canonical JSON") from exc
    return hashlib.sha256(data).hexdigest()


def validate_protocol(raw: Mapping[str, Any]) -> dict[str, Any]:
    if set(raw) != {"protocol_version", "units", "dependency", "material", "load", "reference", "unfamiliar", "tolerances", "experiment"} or raw.get("protocol_version") != PROTOCOL_VERSION or raw.get("units") != "SI_m_kg_s_N_Pa":
        raise VectorSolidViolation("protocol schema, identity, or units mismatch")
    dependency = raw["dependency"]
    if set(dependency) != {"work110_commit", "contract_path", "contract_sha256"} or len(dependency["work110_commit"]) != 40 or len(dependency["contract_sha256"]) != 64:
        raise VectorSolidViolation("Work 110 dependency identity is invalid")
    material = raw["material"]
    if set(material) != {"material_id", "youngs_modulus_pa", "poisson_ratio", "density_kg_m3", "evidence_class"} or material["evidence_class"] != "synthetic_fixture":
        raise VectorSolidViolation("material schema or evidence class is invalid")
    for key in ("youngs_modulus_pa", "density_kg_m3"):
        if isinstance(material[key], bool) or not isinstance(material[key], (int, float)) or not math.isfinite(material[key]) or material[key] <= 0: raise VectorSolidViolation("material property must be positive finite")
    if not -1 < material["poisson_ratio"] < .5: raise VectorSolidViolation("Poisson ratio is outside elastic bounds")
    load = raw["load"]
    if set(load) != {"resultant_force_n", "body_acceleration_m_s2", "load_surface", "support_surface"} or load["load_surface"] == load["support_surface"]:
        raise VectorSolidViolation("load/support schema is invalid")
    for key in ("resultant_force_n", "body_acceleration_m_s2"):
        if not isinstance(load[key], list) or len(load[key]) != 3 or any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in load[key]): raise VectorSolidViolation("load vector must be finite 3D")
    if math.sqrt(sum(x*x for x in load["resultant_force_n"])) == 0: raise VectorSolidViolation("resultant force must be nonzero")
    reference = raw["reference"]
    if set(reference) != {"length_m", "width_m", "height_m", "force_n", "analytic_displacement_relative_tolerance", "patch_strain_absolute_tolerance"}: raise VectorSolidViolation("reference schema mismatch")
    unfamiliar = raw["unfamiliar"]
    if set(unfamiliar) != {"source_config", "resolutions_m", "last_two_relative_change_limit"} or len(unfamiliar["resolutions_m"]) != 3: raise VectorSolidViolation("unfamiliar refinement registration invalid")
    tolerances = raw["tolerances"]
    if set(tolerances) != {"force_residual_relative", "moment_residual_relative", "energy_residual_relative", "minimum_diagonal_condition_proxy"}: raise VectorSolidViolation("tolerance schema mismatch")
    experiment = raw["experiment"]
    if set(experiment) != {"independent_variables", "dependent_variables", "controls", "success_criteria", "failure_criteria"} or any(not v for v in experiment.values()): raise VectorSolidViolation("experiment registration incomplete")
    return {"status": "passed", "protocol_sha256": canonical_sha256(raw)}


def elasticity_matrix(youngs_modulus_pa: float, poisson_ratio: float) -> np.ndarray:
    if youngs_modulus_pa <= 0 or not -1 < poisson_ratio < .5: raise VectorSolidViolation("corrupted stiffness")
    factor = youngs_modulus_pa / ((1 + poisson_ratio) * (1 - 2 * poisson_ratio))
    return factor * np.array([[1-poisson_ratio,poisson_ratio,poisson_ratio,0,0,0],[poisson_ratio,1-poisson_ratio,poisson_ratio,0,0,0],[poisson_ratio,poisson_ratio,1-poisson_ratio,0,0,0],[0,0,0,(1-2*poisson_ratio)/2,0,0],[0,0,0,0,(1-2*poisson_ratio)/2,0],[0,0,0,0,0,(1-2*poisson_ratio)/2]], dtype=float)


def element_kinematics(points: np.ndarray) -> tuple[float, np.ndarray]:
    matrix = np.column_stack((np.ones(4), points))
    determinant = np.linalg.det(matrix)
    volume = abs(determinant) / 6
    if not math.isfinite(volume) or volume <= 0: raise VectorSolidViolation("inverted or zero-volume element")
    gradients = np.linalg.inv(matrix)[1:, :].T
    b = np.zeros((6, 12))
    for node, (dx, dy, dz) in enumerate(gradients):
        col = 3 * node
        b[:, col:col+3] = [[dx,0,0],[0,dy,0],[0,0,dz],[dy,dx,0],[0,dz,dy],[dz,0,dx]]
    return volume, b


def patch_strain(mesh: Mapping[str, Any], gradient: np.ndarray) -> float:
    expected = np.array([gradient[0,0],gradient[1,1],gradient[2,2],gradient[0,1]+gradient[1,0],gradient[1,2]+gradient[2,1],gradient[0,2]+gradient[2,0]])
    maximum = 0.0
    nodes = np.asarray(mesh["nodes"], dtype=float)
    for tet in mesh["tetrahedra"]:
        indices = np.array(tet["nodes"], dtype=int) - 1; _, b = element_kinematics(nodes[indices]); displacement = (nodes[indices] @ gradient.T).reshape(12); maximum = max(maximum, float(np.max(np.abs(b @ displacement - expected))))
    return maximum


def _triangle_area(a, b, c): return np.linalg.norm(np.cross(b-a, c-a)) / 2


def solve(mesh: Mapping[str, Any], material: Mapping[str, Any], load: Mapping[str, Any]) -> dict[str, Any]:
    import warnings
    try:
        from scipy.sparse import coo_matrix
        from scipy.sparse.linalg import MatrixRankWarning, spsolve
        sparse_available = True
    except ModuleNotFoundError:
        MatrixRankWarning = RuntimeWarning
        sparse_available = False
    nodes = np.asarray(mesh["nodes"], dtype=float); node_count = len(nodes); dofs = 3 * node_count; d = elasticity_matrix(material["youngs_modulus_pa"], material["poisson_ratio"])
    rows=[]; cols=[]; data=[]; element_data=[]; graph=[set() for _ in range(node_count)]
    for tet in mesh["tetrahedra"]:
        ids=np.array(tet["nodes"],dtype=int)-1; volume,b=element_kinematics(nodes[ids]); ke=volume*(b.T@d@b); edofs=np.array([[3*i,3*i+1,3*i+2] for i in ids]).reshape(12)
        rr,cc=np.meshgrid(edofs,edofs,indexing="ij"); rows.extend(rr.ravel()); cols.extend(cc.ravel()); data.extend(ke.ravel()); element_data.append((ids,volume,b))
        for i in ids:
            graph[i].update(int(j) for j in ids if j != i)
    if sparse_available:
        k = coo_matrix((data, (rows, cols)), shape=(dofs, dofs)).tocsr()
    else:
        if dofs > 3000:
            raise VectorSolidViolation("SciPy sparse solver is required above 3000 degrees of freedom")
        k = np.zeros((dofs, dofs))
        np.add.at(k, (rows, cols), data)
    surface_force=np.zeros(dofs); load_nodes=set(); support_nodes=set(); total_area=0.0
    for tri in mesh["triangles"]:
        ids=np.array(tri["nodes"],dtype=int)-1
        if tri["set"]==load["load_surface"]:
            area=_triangle_area(*nodes[ids]); total_area+=area; load_nodes.update(ids.tolist())
            for node in ids: surface_force[3*node:3*node+3]+=np.asarray(load["resultant_force_n"])*area/3
        if tri["set"]==load["support_surface"]: support_nodes.update(ids.tolist())
    if not load_nodes or len(support_nodes) < 3 or total_area <= 0: raise VectorSolidViolation("unsupported rigid modes or missing load/support surface")
    surface_force *= np.linalg.norm(load["resultant_force_n"]) / max(np.linalg.norm(surface_force.reshape(-1,3).sum(axis=0)),1e-30)
    force = surface_force.copy()
    body_acceleration = np.asarray(load["body_acceleration_m_s2"], dtype=float)
    for ids, volume, _ in element_data:
        nodal_body_force = material["density_kg_m3"] * volume * body_acceleration / 4
        for node in ids:
            force[3*node:3*node+3] += nodal_body_force
    # Require a topological path from one loaded node to one supported node.
    seen=set(support_nodes); stack=list(support_nodes)
    while stack:
        for neighbor in graph[stack.pop()]:
            if neighbor not in seen: seen.add(neighbor); stack.append(neighbor)
    if not load_nodes & seen: raise VectorSolidViolation("severed load path")
    fixed=np.array(sorted(3*n+a for n in support_nodes for a in range(3)),dtype=int); all_dofs=np.arange(dofs); free=np.setdiff1d(all_dofs,fixed); u=np.zeros(dofs)
    with warnings.catch_warnings():
        warnings.simplefilter("error", MatrixRankWarning)
        try:
            if sparse_available:
                u[free] = spsolve(k[free][:, free], force[free])
            else:
                u[free] = np.linalg.solve(k[np.ix_(free, free)], force[free])
        except (MatrixRankWarning, RuntimeError, np.linalg.LinAlgError) as exc:
            raise VectorSolidViolation("singular or non-converged solve") from exc
    if not np.all(np.isfinite(u)): raise VectorSolidViolation("singular or non-finite displacement")
    residual=k@u-force; reaction=residual.reshape(-1,3)[sorted(support_nodes)].sum(axis=0); applied=force.reshape(-1,3).sum(axis=0); force_res=np.linalg.norm(reaction+applied)/np.linalg.norm(applied)
    nodal_forces=force.reshape(-1,3); reaction_field=np.zeros((node_count,3)); reaction_field[sorted(support_nodes)]=residual.reshape(-1,3)[sorted(support_nodes)]
    moment=np.sum(np.cross(nodes,nodal_forces+reaction_field),axis=0); moment_scale=max(np.linalg.norm(applied)*max(np.linalg.norm(nodes-nodes.mean(axis=0),axis=1)),1e-30); moment_res=np.linalg.norm(moment)/moment_scale
    strain_energy=.5*float(u@(k@u)); work=.5*float(u@force); energy_res=abs(strain_energy-work)/max(abs(strain_energy),abs(work),1e-30)
    stresses=[]; volumes=[]; stress_rows=[]
    for index,(ids,volume,b) in enumerate(element_data):
        stress=d@(b@u[np.array([[3*i,3*i+1,3*i+2] for i in ids]).reshape(12)]); sx,sy,sz,txy,tyz,txz=stress; vm=math.sqrt(.5*((sx-sy)**2+(sy-sz)**2+(sz-sx)**2)+3*(txy*txy+tyz*tyz+txz*txz)); stresses.append(vm); volumes.append(volume); stress_rows.append({"element":index+1,"stress_pa":stress.tolist(),"von_mises_pa":vm})
    order=np.argsort(stresses); cumulative=0; target=.9*sum(volumes); p90=0.0
    for idx in order:
        cumulative += volumes[idx]
        p90 = stresses[idx]
        if cumulative >= target:
            break
    displacements=u.reshape(-1,3); diag=k.diagonal()[free]; condition_proxy=float(diag.min()/diag.max())
    loaded_displacement = displacements[sorted(load_nodes)].mean(axis=0)
    return {"status":"passed","node_count":node_count,"element_count":len(element_data),"loaded_node_count":len(load_nodes),"support_node_count":len(support_nodes),"applied_force_n":applied.tolist(),"recovered_reaction_n":reaction.tolist(),"force_residual_relative":float(force_res),"moment_residual_relative":float(moment_res),"strain_energy_j":strain_energy,"external_work_j":work,"energy_residual_relative":energy_res,"maximum_displacement_m":float(np.linalg.norm(displacements,axis=1).max()),"load_average_displacement_m":loaded_displacement.tolist(),"compliance_m_per_n":float((u@force)/(np.linalg.norm(applied)**2)),"p90_von_mises_stress_pa":float(p90),"minimum_diagonal_condition_proxy":condition_proxy,"displacement_sha256":canonical_sha256(displacements.tolist()),"stress_sha256":canonical_sha256(stress_rows),"reaction_field_sha256":canonical_sha256(reaction_field.tolist()),"displacements_m":displacements.tolist(),"element_stresses":stress_rows}
