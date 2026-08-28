"""Work 028 deterministic whole-race coupled transaction orchestration."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass, replace
from datetime import date
import hashlib
import json
import math
from typing import Callable

from .aero_load_coupling import AeroLoadBalanceResiduals
from .coupling import (
    CompiledCouplingArchitecture,
    ComponentHealthState,
    EventCandidate,
    EventDecision,
    ResidualEntry,
    SharedVehicleState,
    arbitrate_event_candidates,
)
from .energy_health_coupling import (
    CentralEnergyEvidence,
    CentralHealthEvidence,
)
from .motion_coupling import MotionIntegrationEvidence
from .step_inputs import (
    CircuitInputScenario,
    SpatialStepEvidence,
    StrategyStepCommand,
    resolve_step_inputs,
)
from .transaction import (
    AdapterOutput,
    AdapterReadView,
    AdapterTrace,
    CoupledAdapter,
    RuntimeSignal,
    TransactionFailure,
    execute_coupled_step,
)


RACE_PROGRESS_ADAPTER_VERSION = "work028-race-progress-v1"


class WholeRaceError(ValueError):
    """Raised when Work 028 orchestration configuration is invalid."""


def _finite(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise WholeRaceError(f"{name} must be finite")


def _positive(name: str, value: float) -> None:
    _finite(name, value)
    if value <= 0.0:
        raise WholeRaceError(f"{name} must be positive")


def _json_ready(value):
    if isinstance(value, date): return value.isoformat()
    if is_dataclass(value): return _json_ready(asdict(value))
    if isinstance(value, dict): return {str(k):_json_ready(v) for k,v in value.items()}
    if isinstance(value, (tuple,list)): return [_json_ready(x) for x in value]
    return value


def _fingerprint(value) -> str:
    return hashlib.sha256(json.dumps(_json_ready(value),sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class RaceProgressConfiguration:
    target_distance_m: float
    lap_length_m: float
    timeout_s: float
    event_time_tolerance_s: float = 1.0e-12

    def __post_init__(self) -> None:
        for name in ("target_distance_m","lap_length_m","timeout_s"):
            _positive(name,getattr(self,name))
        _finite("event_time_tolerance_s",self.event_time_tolerance_s)
        if self.event_time_tolerance_s < 0: raise WholeRaceError("event_time_tolerance_s must be non-negative")


@dataclass(frozen=True, slots=True)
class RaceProgressEvidence:
    decision: EventDecision
    event_candidates: tuple[EventCandidate,...]
    requested_end_time_s: float
    executed_end_time_s: float
    start_distance_m: float
    candidate_distance_m: float
    committed_distance_m: float
    finish_distance_residual_m: float
    residuals: tuple[ResidualEntry,...]


@dataclass(frozen=True, slots=True)
class RaceProgressStepResult:
    status: str
    reason: str
    next_state: SharedVehicleState|None
    evidence: RaceProgressEvidence|None
    residuals: tuple[ResidualEntry,...]
    race_events: tuple[EventCandidate,...]


def _localize_state(start:SharedVehicleState,end:SharedVehicleState,time_s:float)->SharedVehicleState:
    full=end.time_s-start.time_s
    if full <= 0: raise WholeRaceError("candidate state must advance time")
    fraction=(time_s-start.time_s)/full
    if not -1e-12<=fraction<=1+1e-12: raise WholeRaceError("event lies outside candidate interval")
    fraction=min(1.0,max(0.0,fraction)); duration=time_s-start.time_s
    acceleration=tuple((b-a)/full for a,b in zip(start.velocity_mps,end.velocity_mps))
    velocity=tuple(a+(b-a)*fraction for a,b in zip(start.velocity_mps,end.velocity_mps))
    position=tuple(p+v*duration+.5*a*duration**2 for p,v,a in zip(start.position_m,start.velocity_mps,acceleration))
    yaw_alpha=(end.yaw_rate_rad_per_s-start.yaw_rate_rad_per_s)/full
    yaw_rate=start.yaw_rate_rad_per_s+yaw_alpha*duration
    yaw=start.yaw_rad+start.yaw_rate_rad_per_s*duration+.5*yaw_alpha*duration**2
    components=tuple(ComponentHealthState(a.component_id,
        a.temperature_k+(b.temperature_k-a.temperature_k)*fraction,
        a.degradation+(b.degradation-a.degradation)*fraction,
        a.damage+(b.damage-a.damage)*fraction,
        b.failed if fraction>=1-1e-12 else a.failed)
        for a,b in zip(start.components,end.components))
    return replace(start,time_s=time_s,
        race_distance_m=start.race_distance_m+(end.race_distance_m-start.race_distance_m)*fraction,
        position_m=position,velocity_mps=velocity,yaw_rad=yaw,yaw_rate_rad_per_s=yaw_rate,
        primary_energy_j=start.primary_energy_j+(end.primary_energy_j-start.primary_energy_j)*fraction,
        recovered_energy_j=start.recovered_energy_j+(end.recovered_energy_j-start.recovered_energy_j)*fraction,
        contacts=end.contacts if fraction>=1-1e-12 else start.contacts,
        components=components)


def merge_race_progress(*,config:RaceProgressConfiguration,current:SharedVehicleState,
        motion_candidate:SharedVehicleState,energy_candidate:SharedVehicleState,
        health_candidate:SharedVehicleState,health:CentralHealthEvidence)->RaceProgressStepResult:
    if current.status!="running": raise WholeRaceError("race progress requires running start state")
    if health_candidate.time_s<=current.time_s: raise WholeRaceError("health candidate must advance time")
    if motion_candidate.time_s<health_candidate.time_s-1e-12 or energy_candidate.time_s<health_candidate.time_s-1e-12:
        raise WholeRaceError("motion/energy candidates end before health candidate")
    candidates=list(health.event_candidates)
    race_events=[]
    distance_delta=health_candidate.race_distance_m-current.race_distance_m
    if current.race_distance_m < config.target_distance_m <= health_candidate.race_distance_m and distance_delta>0:
        fraction=(config.target_distance_m-current.race_distance_m)/distance_delta
        finish=EventCandidate("race.finish","finished",current.time_s+fraction*(health_candidate.time_s-current.time_s),"race_progress_solver")
        candidates.append(finish); race_events.append(finish)
    if current.time_s < config.timeout_s <= health_candidate.time_s:
        timeout=EventCandidate("race.timeout","timeout",config.timeout_s,"race_progress_solver")
        candidates.append(timeout); race_events.append(timeout)
    complete=EventCandidate("race.step-complete","step_complete",health_candidate.time_s,"race_progress_solver")
    candidates.append(complete); race_events.append(complete)
    decision=arbitrate_event_candidates(tuple(candidates),time_tolerance_s=config.event_time_tolerance_s)
    next_state=_localize_state(current,health_candidate,decision.earliest_time_s)
    event_type=decision.winner.event_type
    if event_type=="finished":
        next_state=replace(next_state,race_distance_m=config.target_distance_m,status="finished")
    elif event_type=="energy_depletion": next_state=replace(next_state,status="depleted")
    elif event_type in {"thermal_failure","reliability_failure","damage_failure","degradation_failure"}: next_state=replace(next_state,status="failed")
    elif event_type=="timeout": next_state=replace(next_state,status="timeout")
    else: next_state=replace(next_state,status="running")
    laps=min(int(next_state.race_distance_m/config.lap_length_m),int(config.target_distance_m/config.lap_length_m))
    next_state=replace(next_state,completed_laps=laps)
    finish_residual=next_state.race_distance_m-config.target_distance_m if next_state.status=="finished" else 0.0
    residuals=(
        ResidualEntry("race.event-time","time",next_state.time_s-decision.earliest_time_s,"s",1e-12,1e-12,max(1,next_state.time_s)),
        ResidualEntry("race.finish-distance","distance",finish_residual,"m",1e-9,1e-12,max(1,config.target_distance_m)),
        ResidualEntry("race.energy-nonnegative","energy",min(0.0,next_state.primary_energy_j,next_state.recovered_energy_j),"J",0,0,max(1,next_state.primary_energy_j+next_state.recovered_energy_j)),
    )
    evidence=RaceProgressEvidence(decision,tuple(sorted(candidates,key=lambda x:(x.time_s,x.event_id))),
        health_candidate.time_s,next_state.time_s,current.race_distance_m,health_candidate.race_distance_m,
        next_state.race_distance_m,finish_residual,residuals)
    if any(not x.passed for x in residuals): return RaceProgressStepResult("invalid","race residual failed",None,evidence,residuals,tuple(race_events))
    return RaceProgressStepResult("ok","race candidate merged",next_state,evidence,residuals,tuple(race_events))


@dataclass(frozen=True, slots=True)
class RaceProgressAdapter:
    config:RaceProgressConfiguration
    module_id:str=field(default="race_progress_solver",init=False)
    model_version:str=field(default=RACE_PROGRESS_ADAPTER_VERSION,init=False)
    def execute(self,view:AdapterReadView)->AdapterOutput:
        balance=view.read("chassis.balance_residuals"); spatial=view.read("circuit.segment_inputs")
        energy=view.read("energy.residuals"); health=view.read("health.event_candidates")
        health_residuals=view.read("health.residuals"); motion=view.read("motion.residuals")
        current=view.read("state.current"); energy_state=view.read("state.energy_candidate")
        health_state=view.read("state.health_candidate"); motion_state=view.read("state.motion_candidate")
        if not isinstance(balance,AeroLoadBalanceResiduals) or not isinstance(spatial,SpatialStepEvidence) or not isinstance(energy,CentralEnergyEvidence) or not isinstance(health,CentralHealthEvidence) or health_residuals!=health or not isinstance(motion,MotionIntegrationEvidence) or not all(isinstance(x,SharedVehicleState) for x in (current,energy_state,health_state,motion_state)):
            return AdapterOutput(self.module_id,"invalid",(),reason="race progress payload types are invalid")
        try: result=merge_race_progress(config=self.config,current=current,motion_candidate=motion_state,
            energy_candidate=energy_state,health_candidate=health_state,health=health)
        except (ArithmeticError,ValueError) as exc: return AdapterOutput(self.module_id,"invalid",(),reason=str(exc))
        if result.status!="ok": return AdapterOutput(self.module_id,"invalid",(),residuals=result.residuals,reason=result.reason)
        own_event=(result.evidence.decision.winner,) if result.evidence.decision.winner.source_module_id==self.module_id else ()
        return AdapterOutput(self.module_id,"ok",(
            RuntimeSignal("race.event_candidates",result.evidence),RuntimeSignal("race.residuals",result.evidence),
            RuntimeSignal("state.next",result.next_state)),residuals=result.residuals,events=own_event)


@dataclass(frozen=True, slots=True)
class CoupledRaceStepTelemetry:
    step_index:int
    transaction_status:str
    requested_duration_s:float
    scenario_fingerprint_sha256:str
    start_state_sha256:str
    end_state_sha256:str|None
    start_time_s:float
    end_time_s:float|None
    start_distance_m:float
    end_distance_m:float|None
    start_primary_energy_j:float
    end_primary_energy_j:float|None
    published_signal_ids:tuple[str,...]
    traces:tuple[AdapterTrace,...]
    residuals:tuple[ResidualEntry,...]
    events:tuple[EventCandidate,...]
    failure:TransactionFailure|None


@dataclass(frozen=True, slots=True)
class CoupledRaceReplayMetadata:
    schema_version:str
    architecture_id:str
    architecture_fingerprint_sha256:str
    model_versions:tuple[tuple[str,str],...]
    random_seed:int
    evaluation_budget:int
    time_step_s:float
    initial_state_sha256:str
    final_state_sha256:str
    scenario_fingerprints:tuple[str,...]
    attempted_step_count:int
    committed_step_count:int


@dataclass(frozen=True, slots=True)
class WholeRaceResult:
    outcome:str
    reason:str
    target_distance_m:float
    final_state:SharedVehicleState
    finish_distance_residual_m:float
    telemetry:tuple[CoupledRaceStepTelemetry,...]
    replay:CoupledRaceReplayMetadata
    replay_fingerprint_sha256:str


ScenarioFactory=Callable[[int,SharedVehicleState],CircuitInputScenario]
StrategyFactory=Callable[[int,SharedVehicleState],StrategyStepCommand]
AdapterFactory=Callable[[int,SharedVehicleState,float],tuple[CoupledAdapter,...]]


@dataclass(frozen=True, slots=True)
class WholeRaceConfiguration:
    architecture:CompiledCouplingArchitecture
    initial_state:SharedVehicleState
    time_step_s:float
    target_distance_m:float
    timeout_s:float
    evaluation_budget:int
    random_seed:int
    scenario_factory:ScenarioFactory=field(compare=False,repr=False)
    strategy_factory:StrategyFactory=field(compare=False,repr=False)
    adapter_factory:AdapterFactory=field(compare=False,repr=False)
    def __post_init__(self):
        for name in ("time_step_s","target_distance_m","timeout_s"): _positive(name,getattr(self,name))
        if not isinstance(self.evaluation_budget,int) or isinstance(self.evaluation_budget,bool) or self.evaluation_budget<=0: raise WholeRaceError("evaluation_budget must be positive integer")
        if not isinstance(self.random_seed,int) or isinstance(self.random_seed,bool): raise WholeRaceError("random_seed must be integer")
        if self.initial_state.status!="running": raise WholeRaceError("initial state must be running")


def _finish_result(config,state,outcome,reason,telemetry):
    replay=CoupledRaceReplayMetadata("1.0",config.architecture.architecture_id,
        config.architecture.fingerprint_sha256,
        tuple((x.module_id,x.model_version) for x in config.architecture.ordered_modules),
        config.random_seed,config.evaluation_budget,config.time_step_s,
        _fingerprint(config.initial_state),_fingerprint(state),
        tuple(x.scenario_fingerprint_sha256 for x in telemetry),len(telemetry),
        sum(x.transaction_status=="committed" for x in telemetry))
    fingerprint=_fingerprint({"outcome":outcome,"reason":reason,"target":config.target_distance_m,
        "final":state,"telemetry":telemetry,"replay":replay})
    return WholeRaceResult(outcome,reason,config.target_distance_m,state,
        state.race_distance_m-config.target_distance_m if outcome=="finished" else 0.0,
        tuple(telemetry),replay,fingerprint)


def run_whole_race(config:WholeRaceConfiguration)->WholeRaceResult:
    state=config.initial_state; telemetry=[]
    for step_index in range(config.evaluation_budget):
        if state.status!="running": return _finish_result(config,state,state.status,"terminal state committed",telemetry)
        remaining_timeout=config.timeout_s-state.time_s
        if remaining_timeout<=0:
            state=replace(state,status="timeout")
            return _finish_result(config,state,"timeout","timeout reached before next step",telemetry)
        duration=min(config.time_step_s,remaining_timeout)
        scenario=config.scenario_factory(step_index,state); strategy=config.strategy_factory(step_index,state)
        resolution=resolve_step_inputs(scenario,strategy)
        adapters=config.adapter_factory(step_index,state,duration)
        result=execute_coupled_step(architecture=config.architecture,start_state=state,
            initial_signals=(RuntimeSignal("manifest.circuit_profile",scenario),
                RuntimeSignal("manifest.current_state",state),RuntimeSignal("manifest.strategy_command",strategy)),
            adapters=adapters)
        end=result.committed_state
        telemetry.append(CoupledRaceStepTelemetry(step_index,result.status,duration,
            resolution.fingerprint_sha256,_fingerprint(state),_fingerprint(end) if end else None,
            state.time_s,end.time_s if end else None,state.race_distance_m,
            end.race_distance_m if end else None,state.primary_energy_j,
            end.primary_energy_j if end else None,tuple(x.signal_id for x in result.published_signals),
            result.traces,result.residuals,result.events,result.failure))
        if result.status!="committed":
            reason=f"{result.failure.code}: {result.failure.reason}" if result.failure else "invalid transaction"
            return _finish_result(config,state,"invalid",reason,telemetry)
        state=end
        if state.status!="running": return _finish_result(config,state,state.status,"terminal state committed",telemetry)
    state=replace(state,status="timeout")
    return _finish_result(config,state,"timeout","evaluation budget exhausted",telemetry)
