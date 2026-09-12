"""Offline whole-vehicle staged-program entry and telemetry audit."""
from __future__ import annotations
import hashlib,json
PROTOCOL_VERSION="physical_vehicle_validation_v1"
class PhysicalVehicleViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise PhysicalVehicleViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
def validate_protocol(raw):
    if set(raw)!={"protocol_version","units","dependencies","inputs","entry","registration","telemetry","coverage","experiment"} or raw.get("protocol_version")!=PROTOCOL_VERSION: raise PhysicalVehicleViolation("protocol schema or identity mismatch")
    if raw["units"]!="SI" or {x.get("work") for x in raw["dependencies"]}!={128,129,130,131,132}: raise PhysicalVehicleViolation("units or Work 128 through 132 dependency mismatch")
    return {"status":"passed","protocol_sha256":canonical_sha256(raw)}
def entry_gate(raw,prerequisites):
    validate_protocol(raw); blockers=[name for name,available in prerequisites.items() if not available]
    for key in ("qualified_vehicle_safety_review_ref","facility_authorization_ref","authorized_test_director_ref","configuration_sha256","measurement_plan_sha256","incident_plan_sha256"):
        if not raw["entry"].get(key): blockers.append(key)
    if not raw["telemetry"]: blockers.append("measured_vehicle_telemetry")
    return {"ready":not blockers,"blockers":blockers,"vehicle_operation_authorized":False}
def audit_telemetry(raw,records):
    if not records: raise PhysicalVehicleViolation("missing vehicle telemetry")
    approved=set(raw["registration"]["approved_stages"]); config=raw["entry"]["configuration_sha256"]
    for x in records:
        if x["stage"] not in approved: raise PhysicalVehicleViolation("unapproved stage expansion")
        if x["configuration_sha256"]!=config: raise PhysicalVehicleViolation("changed hardware or control configuration")
        if x.get("failed") and not x.get("incident_recorded"): raise PhysicalVehicleViolation("missing failure or incident")
        if x.get("energy_in_j") is None or x.get("energy_out_j") is None or x.get("loss_j") is None: raise PhysicalVehicleViolation("incomplete energy record")
        residual=x["energy_in_j"]-x["energy_out_j"]-x["loss_j"]
        if abs(residual)>raw["registration"]["energy_residual_tolerance_j"]: raise PhysicalVehicleViolation("energy residual exceeds tolerance")
        if x.get("claim_scope") not in ("tested_stage_only",None): raise PhysicalVehicleViolation("improper extrapolation")
    return {"records":len(records),"tested_stages":sorted({x["stage"] for x in records}),"scope":"tested stages only","safety_certification":False,"guaranteed_superiority":False}
