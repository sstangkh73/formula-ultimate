"""Offline subsystem-correlation readiness and record integrity checks."""
from __future__ import annotations
import hashlib,json
PROTOCOL_VERSION="physical_subsystem_correlation_v1"
class PhysicalSubsystemViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise PhysicalSubsystemViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
def validate_protocol(raw):
    if set(raw)!={"protocol_version","units","dependency","input","entry","registration","records","coverage","experiment"} or raw.get("protocol_version")!=PROTOCOL_VERSION: raise PhysicalSubsystemViolation("protocol schema or identity mismatch")
    if raw["units"]!="SI" or raw["dependency"].get("work")!=131: raise PhysicalSubsystemViolation("units or Work 131 dependency mismatch")
    return {"status":"passed","protocol_sha256":canonical_sha256(raw)}
def entry_gate(raw,upstream_status):
    validate_protocol(raw); blockers=[]
    if upstream_status!="measured_connection_correlation_available": blockers.append("valid_Work131_measured_applicability")
    for key in ("subsystem_safety_approval_ref","facility_ref","authorized_operator_ref","frozen_configuration_sha256","instrument_manifest_sha256"):
        if not raw["entry"].get(key): blockers.append(key)
    if not raw["records"]: blockers.append("measured_subsystem_records")
    return {"ready":not blockers,"blockers":blockers,"equipment_operation_authorized":False}
def analyze_records(raw,records):
    if not records: raise PhysicalSubsystemViolation("missing measured subsystem records")
    identities={x["configuration_id"] for x in records}
    if len(identities)!=1: raise PhysicalSubsystemViolation("undocumented replacement")
    calibration={x["run_id"] for x in records if x["partition"]=="calibration"}; validation={x["run_id"] for x in records if x["partition"]=="validation"}
    if calibration & validation or not calibration or not validation: raise PhysicalSubsystemViolation("calibration leakage")
    for x in records:
        if x.get("boundary_power_in_w") is None or x.get("boundary_power_out_w") is None: raise PhysicalSubsystemViolation("missing boundary power")
        if x.get("aborted") and not x.get("abort_reason"): raise PhysicalSubsystemViolation("censored abort")
        if abs(x["sensor_a"]-x["sensor_b"])>raw["registration"]["maximum_sensor_disagreement"]: raise PhysicalSubsystemViolation("sensor disagreement")
    valid=[x for x in records if x["partition"]=="validation"]
    losses=[x["boundary_power_in_w"]-x["boundary_power_out_w"] for x in valid]
    return {"validation_runs":len(valid),"mean_loss_w":sum(losses)/len(losses),"maximum_cycles_observed":max(x["cycles"] for x in valid),"lifetime_extrapolation_allowed":False}
