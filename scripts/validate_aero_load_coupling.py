"""Generate deterministic Work 024 aerodynamic/load coupling evidence."""

from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))

from formula_ultimate.physics.aerodynamics import (AerodynamicCoefficientMap,
    AerodynamicCoefficientSample,AerodynamicEvidence,AerodynamicReference,AerodynamicStateGrid)  # noqa: E402
from formula_ultimate.physics.lateral import PlanarContact,PlanarVehicle,PlanarVehicleParameters  # noqa: E402
from formula_ultimate.physics.tyre import TyreContactParameters  # noqa: E402
from formula_ultimate.simulation import (AdapterReadView,AerodynamicChassisWrench,
    AerodynamicMapAdapter,AerodynamicReferenceOrigin,ComponentHealthState,
    ContactRuntimeState,EnvironmentStepInputs,RuntimeSignal,SharedVehicleState,
    TrafficStepEvidence,WeatherStepEvidence,couple_wrench_to_normal_loads)  # noqa: E402

TYRE=TyreContactParameters(1.2,1.1)
def contact(cid,x,y,n): return PlanarContact(cid,x,y,n,0,20000,0,TYRE)
def vehicle():
    mass=1000.; n=mass*9.81/4
    return PlanarVehicle("reference",PlanarVehicleParameters(mass,1500,.4),(
        contact("fl",1,.8,n),contact("fr",1,-.8,n),contact("rl",-1,.8,n),contact("rr",-1,-.8,n)))
def shared(v,speed=30.):
    return SharedVehicleState(0,0,(0,0,0),(speed,0,0),0,0,1e6,0,0,
        tuple(ContactRuntimeState(c.contact_id,c.baseline_normal_load_n,0,0,0,0) for c in v.contacts),
        (ComponentHealthState("store",350,0,0,False),))
def main():
    v=vehicle(); current=shared(v)
    coefficient_map=AerodynamicCoefficientMap("fixture",(30.,),(.05,),(0.,),
        (AerodynamicStateGrid("nominal",(AerodynamicCoefficientSample(.5,0,1,0,0,.2),)),),
        AerodynamicEvidence("fixture","synthetic_reference","analytical"))
    reference=AerodynamicReference(2,3,.1,1005,.5)
    weather=WeatherStepEvidence("fixture","observed","fixture",300,101325,.5,(0,0,0),"local_enu",0,310)
    environment=EnvironmentStepInputs(weather,TrafficStepEvidence("fixture","isolated_control","fixture",0))
    adapter=AerodynamicMapAdapter(coefficient_map,reference,AerodynamicReferenceOrigin((1,0,0)),.05,"nominal",350)
    output=adapter.execute(AdapterReadView("aerodynamic_map",current,(
        RuntimeSignal("environment.step_inputs",environment),RuntimeSignal("state.current",current))))
    if output.status != "ok": raise RuntimeError(output.reason)
    values={signal.signal_id:signal.value for signal in output.signals}; wrench=values["aero.force_moment"]
    loads=couple_wrench_to_normal_loads(vehicle=v,wrench=wrench)
    if loads.status != "ok" or not all(e.passed for e in loads.residuals.entries()): raise RuntimeError(loads.reason)
    outside=AerodynamicMapAdapter(coefficient_map,reference,AerodynamicReferenceOrigin((0,0,0)),.05,"nominal",350).execute(
        AdapterReadView("aerodynamic_map",shared(v,40),(
            RuntimeSignal("environment.step_inputs",environment),RuntimeSignal("state.current",shared(v,40)))))
    if outside.status != "invalid" or outside.signals: raise RuntimeError("outside map did not fail closed")
    evidence={"schema_version":"1.0","claim_boundary":"Work 024 Level-0 synthetic aero/load coupling; not physical validation",
        "aero":{"force_body_n":wrench.force_body_n,"moment_about_com_n_m":wrench.moment_about_com_n_m,
            "cooling_heat_rejection_w":values["aero.cooling_evidence"].heat_rejection_w},
        "loads":{"contact_loads_n":{x.contact_id:x.normal_load_n for x in loads.contact_loads},
            "residuals":[{"id":e.residual_id,"value":e.value,"unit":e.unit,"passed":e.passed} for e in loads.residuals.entries()]},
        "front_load_exceeds_rear":sum(x.normal_load_n for x in loads.contact_loads[:2])>sum(x.normal_load_n for x in loads.contact_loads[2:]),
        "outside_map":{"status":outside.status,"emitted_signal_count":len(outside.signals),"reason":outside.reason},
        "topology_prescription":None}
    print(json.dumps(evidence,indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
