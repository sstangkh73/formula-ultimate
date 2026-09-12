"""Offline-only physical connection correlation entry and integrity gates."""
from __future__ import annotations
import hashlib,json
PROTOCOL_VERSION="physical_connection_correlation_v1"
class PhysicalConnectionCorrelationViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise PhysicalConnectionCorrelationViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
def validate_protocol(raw):
    required={"protocol_version","units","dependencies","inputs","entry_permissions","registration","measurement_manifest","raw_observations","coverage","experiment"}
    if set(raw)!=required or raw.get("protocol_version")!=PROTOCOL_VERSION: raise PhysicalConnectionCorrelationViolation("protocol schema or identity mismatch")
    if raw.get("units")!="SI": raise PhysicalConnectionCorrelationViolation("SI units are required")
    if {x.get("work") for x in raw["dependencies"]}!={113,116,130}: raise PhysicalConnectionCorrelationViolation("Work 113, 116 and 130 dependencies are required")
    return {"status":"passed","protocol_sha256":canonical_sha256(raw)}
def entry_gate(raw):
    validate_protocol(raw); blockers=[]
    for key in ("qualified_safety_approval_ref","facility_authorization_ref","authorized_operator_ref"):
        if not raw["entry_permissions"].get(key): blockers.append(key)
    for key in ("specimens_inspected","instruments_calibrated","hazard_review_complete"):
        if not raw["entry_permissions"].get(key): blockers.append(key)
    manifest=raw["measurement_manifest"]
    if not manifest["specimens"]: blockers.append("inspected_specimen_manifest")
    if not manifest["instruments"]: blockers.append("calibrated_instrument_manifest")
    if not raw["raw_observations"]["records"]: blockers.append("measured_raw_observations")
    if not raw["raw_observations"].get("sha256"): blockers.append("raw_observation_sha256")
    return {"ready":not blockers,"blockers":blockers,"equipment_operation_authorized":False}
def offline_stop(sample,limits):
    reasons=[]
    if sample.get("load_n",0)>limits["maximum_load_n"]: reasons.append("load_limit")
    if sample.get("temperature_k",0)>limits["maximum_temperature_k"]: reasons.append("temperature_limit")
    if sample.get("sensor_saturated",False): reasons.append("sensor_saturation")
    return {"stop":bool(reasons),"reasons":reasons}
def analyze_records(raw,records):
    gate=entry_gate(raw)
    if not gate["ready"]: raise PhysicalConnectionCorrelationViolation("physical entry gate incomplete")
    manifest=raw["measurement_manifest"]; specimen_ids={x["id"] for x in manifest["specimens"]}; instrument_ids={x["id"] for x in manifest["instruments"] if x["calibration_valid"]}
    if canonical_sha256(records)!=raw["raw_observations"]["sha256"]: raise PhysicalConnectionCorrelationViolation("edited raw data")
    for record in records:
        if record["specimen_id"] not in specimen_ids: raise PhysicalConnectionCorrelationViolation("swapped specimen ID")
        if record["instrument_id"] not in instrument_ids: raise PhysicalConnectionCorrelationViolation("missing calibration")
        if record["sensor_saturated"]: raise PhysicalConnectionCorrelationViolation("sensor saturation")
    calibration={x["specimen_id"] for x in records if x["partition"]=="calibration"}; validation={x["specimen_id"] for x in records if x["partition"]=="validation"}
    if calibration & validation or not calibration or not validation: raise PhysicalConnectionCorrelationViolation("calibration and validation partitions are invalid")
    errors=[x["measured_displacement_m"]-x["predicted_displacement_m"] for x in records if x["partition"]=="validation"]
    return {"validation_count":len(errors),"mean_discrepancy_m":sum(errors)/len(errors),"physical_scope":"tested records only"}
