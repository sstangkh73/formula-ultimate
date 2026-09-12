"""Separate bounded internal-flow/heat and external-flow references for Work 121."""
from __future__ import annotations
import hashlib,json,math
from typing import Any,Mapping,Sequence
PROTOCOL_VERSION="geometry_flow_heat_exchange_v1"
class GeometryFlowViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise GeometryFlowViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
def validate_protocol(raw:Mapping[str,Any]):
    required={"protocol_version","units","dependencies","inputs","mesh_source","boundaries","internal","external","refinement","tolerances","coverage","experiment"}
    if set(raw)!=required or raw.get("protocol_version")!=PROTOCOL_VERSION: raise GeometryFlowViolation("protocol schema or identity mismatch")
    if raw.get("units")!="SI_m_kg_s_K_Pa_W_J_N": raise GeometryFlowViolation("protocol units mismatch")
    if {x.get("work") for x in raw["dependencies"]}!={110,115,116}: raise GeometryFlowViolation("Work 110, 115 and 116 dependencies are required")
    if set(raw["boundaries"]["internal"])!={"inlet","outlet","wall"} or set(raw["boundaries"]["external"])!={"body_wall","far_field","symmetry"}: raise GeometryFlowViolation("fluid boundary topology is incomplete")
    internal=raw["internal"]; fluid=internal["fluid"]
    if internal["diameter_m"]<=0 or internal["length_m"]<=0 or internal["volume_flow_m3_s"]<0 or any(fluid[k]<=0 for k in ("density_kg_m3","dynamic_viscosity_pa_s","specific_heat_j_kg_k","conductivity_w_m_k")): raise GeometryFlowViolation("internal-flow geometry or properties are invalid")
    external=raw["external"]
    if external["density_kg_m3"]<=0 or external["drag_coefficient"]<0 or external["speed_m_s"]<0 or not 0<=external["pressure_fraction"]<=1: raise GeometryFlowViolation("external-flow record is invalid")
    if sorted(raw["refinement"]["internal_segments"])!=raw["refinement"]["internal_segments"] or sorted(raw["refinement"]["far_field_widths_m"])!=raw["refinement"]["far_field_widths_m"]: raise GeometryFlowViolation("refinement registration is invalid")
    if any(not values for values in raw["experiment"].values()): raise GeometryFlowViolation("experiment registration is incomplete")
    return {"status":"passed","protocol_sha256":canonical_sha256(raw),"scopes":["internal_laminar_passage","external_incompressible_quadratic_drag"]}
def mesh_bounds(vertices:Sequence[Sequence[float]]):
    if not vertices or any(len(vertex)!=3 for vertex in vertices): raise GeometryFlowViolation("mesh vertices are missing")
    axes=list(zip(*vertices)); mins=[min(axis) for axis in axes]; maxs=[max(axis) for axis in axes]
    if any(high<=low for low,high in zip(mins,maxs)): raise GeometryFlowViolation("mesh bounds are degenerate")
    return {"minimum_m":mins,"maximum_m":maxs,"extents_m":[high-low for low,high in zip(mins,maxs)]}
def internal_passage(raw:Mapping[str,Any],segments:int,*,diameter_m=None,volume_flow_m3_s=None,source_heat_w=None,blocked=False):
    case=raw["internal"]; fluid=case["fluid"]; diameter=case["diameter_m"] if diameter_m is None else diameter_m; flow=case["volume_flow_m3_s"] if volume_flow_m3_s is None else volume_flow_m3_s; source=case["source_heat_w"] if source_heat_w is None else source_heat_w
    if diameter<=0 or flow<0 or source<0 or segments<1: raise GeometryFlowViolation("internal-flow request is invalid")
    if blocked or flow==0:
        return {"state":"blocked" if blocked else "zero_flow","segments":segments,"diameter_m":diameter,"volume_flow_m3_s":0.0,"reynolds":0.0,"pressure_drop_pa":0.0,"pumping_power_w":0.0,"unlimited_heat_capacity_w":0.0,"heat_rejected_w":0.0,"outlet_temperature_k":case["inlet_temperature_k"],"heat_residual_w":0.0,"profile":[]}
    area=math.pi*diameter**2/4; velocity=flow/area; reynolds=fluid["density_kg_m3"]*velocity*diameter/fluid["dynamic_viscosity_pa_s"]
    if reynolds>case["maximum_reynolds"]: raise GeometryFlowViolation("internal flow outside registered laminar regime")
    pressure_drop=128*fluid["dynamic_viscosity_pa_s"]*case["length_m"]*flow/(math.pi*diameter**4); nusselt=case["nusselt_constant_wall_temperature"]; coefficient=nusselt*fluid["conductivity_w_m_k"]/diameter; mass_heat_capacity=fluid["density_kg_m3"]*flow*fluid["specific_heat_j_kg_k"]; dx=case["length_m"]/segments; temperature=case["inlet_temperature_k"]; profile=[]
    for index in range(segments):
        temperature+=coefficient*math.pi*diameter*dx*(case["wall_temperature_k"]-temperature)/mass_heat_capacity; profile.append({"x_m":(index+1)*dx,"capacity_temperature_k":temperature})
    unlimited=mass_heat_capacity*(temperature-case["inlet_temperature_k"]); rejected=min(source,unlimited); outlet=case["inlet_temperature_k"]+rejected/mass_heat_capacity; residual=rejected-mass_heat_capacity*(outlet-case["inlet_temperature_k"])
    analytic_capacity=mass_heat_capacity*(case["wall_temperature_k"]-case["inlet_temperature_k"])*(1-math.exp(-coefficient*math.pi*diameter*case["length_m"]/mass_heat_capacity))
    return {"state":"admitted","segments":segments,"diameter_m":diameter,"volume_flow_m3_s":flow,"velocity_m_s":velocity,"reynolds":reynolds,"pressure_drop_pa":pressure_drop,"pumping_power_w":pressure_drop*flow,"heat_transfer_coefficient_w_m2_k":coefficient,"unlimited_heat_capacity_w":unlimited,"analytic_heat_capacity_w":analytic_capacity,"heat_capacity_relative_error":abs(unlimited-analytic_capacity)/analytic_capacity,"heat_rejected_w":rejected,"outlet_temperature_k":outlet,"heat_residual_w":residual,"wall_pressure_force_n":pressure_drop*area,"profile":profile}
def external_flow(raw:Mapping[str,Any],projected_area_m2:float,far_field_width_m:float,*,speed_m_s=None,area_scale=1.0):
    case=raw["external"]; speed=case["speed_m_s"] if speed_m_s is None else speed_m_s
    if projected_area_m2<=0 or far_field_width_m<=0 or speed<0 or area_scale<=0: raise GeometryFlowViolation("external-flow geometry or request is invalid")
    blockage=case["body_width_m"]/far_field_width_m
    if blockage>=case["maximum_blockage_ratio"]: raise GeometryFlowViolation("external far-field domain is too small")
    area=projected_area_m2*area_scale; unbounded=.5*case["density_kg_m3"]*speed**2*case["drag_coefficient"]*area; correction=1+blockage**2; drag=unbounded*correction; pressure=drag*case["pressure_fraction"]; shear=drag-pressure
    return {"state":"admitted","projected_area_m2":area,"speed_m_s":speed,"far_field_width_m":far_field_width_m,"blockage_ratio":blockage,"unbounded_reference_drag_n":unbounded,"drag_force_n":drag,"pressure_force_n":pressure,"shear_force_n":shear,"yaw_moment_n_m":drag*case["centre_of_pressure_offset_m"],"force_residual_n":drag-pressure-shear,"domain_relative_error":abs(drag-unbounded)/max(unbounded,1e-30)}
