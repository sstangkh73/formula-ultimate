"""Bounded onboard stored-energy realization for Work 120."""
from __future__ import annotations
import hashlib,json,math
from typing import Any,Mapping
PROTOCOL_VERSION="onboard_energy_realization_v1"
class OnboardEnergyViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise OnboardEnergyViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
def shell_volume(outer,thickness):
    x,y,z=outer
    if thickness<=0 or min(outer)<=2*thickness: raise OnboardEnergyViolation("containment geometry is invalid")
    return x*y*z-(x-2*thickness)*(y-2*thickness)*(z-2*thickness)
def assembly(raw):
    storage=raw["storage"]; hardware=raw["hardware"]; containment=hardware["containment"]
    active_mass=storage["active_volume_m3"]*storage["active_density_kg_m3"]
    enclosure_mass=shell_volume(containment["outer_dimensions_m"],containment["wall_thickness_m"])*containment["density_kg_m3"]
    insulation_mass=hardware["insulation_volume_m3"]*hardware["insulation_density_kg_m3"]
    connector_mass=hardware["connector_volume_m3"]*hardware["connector_density_kg_m3"]
    mount_mass=hardware["mount_count"]*hardware["mount_mass_each_kg"]
    converter_mass=hardware["converter_mass_kg"]
    masses={"active_storage_kg":active_mass,"enclosure_kg":enclosure_mass,"insulation_kg":insulation_mass,"connectors_kg":connector_mass,"mounts_kg":mount_mass,"converter_kg":converter_mass}
    heat_capacity=active_mass*storage["specific_heat_j_kg_k"]+enclosure_mass*containment["specific_heat_j_kg_k"]+insulation_mass*hardware["insulation_specific_heat_j_kg_k"]+connector_mass*hardware["connector_specific_heat_j_kg_k"]+(mount_mass+converter_mass)*hardware["balance_specific_heat_j_kg_k"]
    nominal=active_mass*storage["specific_energy_j_kg"]; usable=nominal*storage["usable_fraction"]
    return {"component_masses":masses,"complete_mass_kg":sum(masses.values()),"effective_heat_capacity_j_k":heat_capacity,"nominal_energy_j":nominal,"usable_capacity_j":usable,"internal_allocated_volume_m3":storage["active_volume_m3"]+hardware["insulation_volume_m3"]+hardware["connector_volume_m3"]}
def validate_protocol(raw:Mapping[str,Any]):
    required={"protocol_version","units","dependencies","inputs","energy_boundary","storage","hardware","conversion","operating_cases","tolerances","coverage","experiment"}
    if set(raw)!=required or raw.get("protocol_version")!=PROTOCOL_VERSION: raise OnboardEnergyViolation("protocol schema or identity mismatch")
    if raw.get("units")!="SI_m_kg_s_K_W_J_V_A_ohm": raise OnboardEnergyViolation("unit or energy-boundary inconsistency")
    if {x.get("work") for x in raw["dependencies"]}!={115,116,119}: raise OnboardEnergyViolation("Work 115, 116 and 119 dependencies are required")
    if raw["energy_boundary"]!={"external_replenishment":"prohibited","initial_state_included":True,"losses_inside_boundary":True}: raise OnboardEnergyViolation("unit or energy-boundary inconsistency")
    storage=raw["storage"]
    if any(storage[k]<=0 for k in ("active_volume_m3","active_density_kg_m3","specific_energy_j_kg","specific_heat_j_kg_k")) or not 0<storage["usable_fraction"]<=1 or not 0<=storage["initial_fraction"]<=1: raise OnboardEnergyViolation("storage record is invalid")
    hardware=raw["hardware"]
    required_hardware={"envelope_internal_volume_m3","containment","insulation_volume_m3","insulation_density_kg_m3","insulation_specific_heat_j_kg_k","connector_volume_m3","connector_density_kg_m3","connector_specific_heat_j_kg_k","mount_count","mount_mass_each_kg","converter_mass_kg","balance_specific_heat_j_kg_k"}
    if set(hardware)!=required_hardware: raise OnboardEnergyViolation("containment or hardware mass is omitted")
    data=assembly(raw)
    if data["internal_allocated_volume_m3"]>hardware["envelope_internal_volume_m3"]: raise OnboardEnergyViolation("internal geometry exceeds containment")
    conversion=raw["conversion"]
    if not 0<conversion["efficiency"]<=1 or conversion["maximum_output_power_w"]<=0 or conversion["nominal_voltage_v"]<=0 or conversion["connector_resistance_ohm"]<0: raise OnboardEnergyViolation("conversion law is invalid")
    if any(not values for values in raw["experiment"].values()): raise OnboardEnergyViolation("experiment registration is incomplete")
    if not all(str(value).startswith("unresolved") for key,value in raw["coverage"].items() if key!="stored_electric_dc_reference"): raise OnboardEnergyViolation("unsupported route was promoted")
    return {"status":"passed","assembly":data,"protocol_sha256":canonical_sha256(raw)}
def operate(raw:Mapping[str,Any],requested_output_power_w:float,duration_s:float,initial_temperature_k:float,*,initial_fraction=None,connected=True,external_replenishment_w=0.0):
    if external_replenishment_w!=0: raise OnboardEnergyViolation("hidden external replenishment is prohibited")
    if requested_output_power_w<0 or duration_s<=0 or not all(math.isfinite(x) for x in (requested_output_power_w,duration_s,initial_temperature_k)): raise OnboardEnergyViolation("operating request is invalid")
    validation=validate_protocol(raw); data=validation["assembly"]; storage=raw["storage"]; conversion=raw["conversion"]
    fraction=storage["initial_fraction"] if initial_fraction is None else initial_fraction
    if not 0<=fraction<=1: raise OnboardEnergyViolation("initial stored fraction is invalid")
    t_min,t_max=storage["temperature_range_k"]
    if not t_min<=initial_temperature_k<=t_max: raise OnboardEnergyViolation("temperature outside storage applicability")
    initial_energy=data["usable_capacity_j"]*fraction
    if not connected: return {"state":"disconnected","initial_stored_energy_j":initial_energy,"final_stored_energy_j":initial_energy,"delivered_power_w":0.0,"delivered_energy_j":0.0,"conversion_loss_j":0.0,"connector_loss_j":0.0,"total_loss_j":0.0,"final_temperature_k":initial_temperature_k,"energy_residual_j":0.0,"complete_mass_kg":data["complete_mass_kg"]}
    delivered_power=min(requested_output_power_w,conversion["maximum_output_power_w"])
    conversion_input=delivered_power/conversion["efficiency"] if delivered_power else 0.0
    current=conversion_input/conversion["nominal_voltage_v"]
    connector_loss_power=current*current*conversion["connector_resistance_ohm"]
    conversion_loss_power=conversion_input-delivered_power
    total_draw_power=conversion_input+connector_loss_power
    total_loss_power=conversion_loss_power+connector_loss_power
    served=duration_s
    state="rate_limited" if requested_output_power_w>conversion["maximum_output_power_w"] else "admitted"
    if initial_energy==0 or total_draw_power==0:
        served=0.0 if initial_energy==0 else duration_s
        if initial_energy==0 and requested_output_power_w>0: state="empty"
    elif total_draw_power*served>initial_energy:
        served=initial_energy/total_draw_power; state="depleted"
    thermal_time=math.inf if total_loss_power==0 else max(0.0,(t_max-initial_temperature_k)*data["effective_heat_capacity_j_k"])/total_loss_power
    if thermal_time<served:
        served=thermal_time; state="thermal_limited"
    delivered_energy=delivered_power*served; conversion_loss=conversion_loss_power*served; connector_loss=connector_loss_power*served; total_loss=conversion_loss+connector_loss; draw=delivered_energy+total_loss; final_energy=max(0.0,initial_energy-draw); final_temperature=initial_temperature_k+total_loss/data["effective_heat_capacity_j_k"]
    return {"state":state,"requested_output_power_w":requested_output_power_w,"delivered_power_w":delivered_power,"served_duration_s":served,"initial_stored_energy_j":initial_energy,"final_stored_energy_j":final_energy,"stored_energy_change_j":final_energy-initial_energy,"delivered_energy_j":delivered_energy,"conversion_loss_j":conversion_loss,"connector_loss_j":connector_loss,"total_loss_j":total_loss,"average_heat_rate_w":total_loss_power,"final_temperature_k":final_temperature,"energy_residual_j":initial_energy-final_energy-delivered_energy-total_loss,"complete_mass_kg":data["complete_mass_kg"],"assembly_sha256":canonical_sha256(data)}
