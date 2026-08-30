"""Topology-neutral primitive assembly grammar for Work 047."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib,json,math
from typing import Any,Mapping

GRAMMAR_VERSION="vehicle_assembly_primitives_v1"
class VehicleAssemblyViolation(ValueError): pass
def vec(x,name):
    if len(x)!=3: raise VehicleAssemblyViolation(f"{name} must have three values")
    y=tuple(float(v) for v in x)
    if not all(math.isfinite(v) for v in y): raise VehicleAssemblyViolation(f"{name} must be finite")
    return y
@dataclass(frozen=True,slots=True)
class Component:
    component_id:str; tags:tuple[str,...]; material_id:str; kind:str; dims:tuple[float,...]; position:tuple[float,float,float]; density:float
    @property
    def volume(self): return math.prod(self.dims) if self.kind=="box" else math.pi*self.dims[0]**2*self.dims[1]
    @property
    def mass(self): return self.volume*self.density
    @property
    def bounds(self):
        h=tuple(v/2 for v in self.dims) if self.kind=="box" else (self.dims[0],self.dims[0],self.dims[1]/2)
        return tuple(tuple(self.position[i]+s*h[i] for i in range(3)) for s in (-1,1))
    @property
    def inertia(self):
        m=self.mass
        if self.kind=="box":
            x,y,z=self.dims; return (m*(y*y+z*z)/12,m*(x*x+z*z)/12,m*(x*x+y*y)/12,0.,0.,0.)
        r,h=self.dims; q=m*(3*r*r+h*h)/12; return (q,q,m*r*r/2,0.,0.,0.)
@dataclass(frozen=True,slots=True)
class Assembly:
    protocol_id:str; candidate_id:str; components:tuple[Component,...]; interfaces:tuple[dict,...]; connections:tuple[dict,...]; contacts:tuple[dict,...]; energy_edges:tuple[tuple[str,str],...]; loads:tuple[str,...]; envelope:tuple[tuple[float,float,float],tuple[float,float,float]]; keepouts:tuple[tuple[str,tuple[float,float,float],tuple[float,float,float]],...]; tolerances:dict[str,float]
def path(edges,start,goal):
    graph={}
    for a,b in edges: graph.setdefault(a,set()).add(b); graph.setdefault(b,set()).add(a)
    seen=set(); todo=[start]
    while todo:
        n=todo.pop()
        if n==goal:return True
        if n not in seen: seen.add(n); todo.extend(graph.get(n,set())-seen)
    return False
def from_mapping(raw:Mapping[str,Any])->Assembly:
    if raw.get("grammar_version")!=GRAMMAR_VERSION: raise VehicleAssemblyViolation("grammar version mismatch")
    mats=raw["materials"]; comps=[]
    for x in raw["components"]:
        p=x["primitive"]; k=p["type"]; d=vec(p["size_m"],"box size") if k=="box" else (float(p["radius_m"]),float(p["height_m"])) if k=="cylinder_z" else ()
        if not d or any(v<=0 or not math.isfinite(v) for v in d): raise VehicleAssemblyViolation("invalid primitive")
        rho=float(mats[x["material_id"]]["density_kg_per_m3"])
        if rho<=0: raise VehicleAssemblyViolation("massless material")
        comps.append(Component(x["component_id"],tuple(x["function_tags"]),x["material_id"],k,tuple(d),vec(x["translation_m"],"translation"),rho))
    ids=[x.component_id for x in comps]
    if len(ids)!=len(set(ids)): raise VehicleAssemblyViolation("duplicate component")
    interfaces=tuple(dict(x) for x in raw["interfaces"]); iids=[x["interface_id"] for x in interfaces]
    if len(iids)!=len(set(iids)): raise VehicleAssemblyViolation("duplicate interface")
    return Assembly(raw["protocol_id"],raw["candidate_id"],tuple(comps),interfaces,tuple(dict(x) for x in raw["connections"]),tuple(dict(x) for x in raw["contacts"]),tuple(tuple(x) for x in raw["energy_edges"]),tuple(raw["external_load_components"]),(vec(raw["envelope"]["minimum_m"],"envelope"),vec(raw["envelope"]["maximum_m"],"envelope")),tuple((x["keep_out_id"],vec(x["minimum_m"],"keepout"),vec(x["maximum_m"],"keepout")) for x in raw["keep_outs"]),{k:float(v) for k,v in raw["tolerances"].items()})
def mass_properties(a:Assembly):
    m=math.fsum(x.mass for x in a.components); c=tuple(math.fsum(x.mass*x.position[i] for x in a.components)/m for i in range(3)); I=[0.]*6
    for x in a.components:
        dx,dy,dz=(x.position[i]-c[i] for i in range(3)); q=(x.mass*(dy*dy+dz*dz),x.mass*(dx*dx+dz*dz),x.mass*(dx*dx+dy*dy),-x.mass*dx*dy,-x.mass*dx*dz,-x.mass*dy*dz)
        I=[I[i]+x.inertia[i]+q[i] for i in range(6)]
    return {"mass_kg":m,"centre_of_mass_m":c,"inertia_kg_m2":tuple(I)}
def validate(a:Assembly):
    by={x.component_id:x for x in a.components}; iface={x["interface_id"]:x for x in a.interfaces}; tol=a.tolerances["interface_position_m"]
    if any(x["component_id"] not in by for x in a.interfaces): raise VehicleAssemblyViolation("unknown interface component")
    world={k:tuple(by[v["component_id"]].position[i]+vec(v["local_position_m"],"interface")[i] for i in range(3)) for k,v in iface.items()}; edges=[]; maxr=0.
    for x in a.connections:
        if x["interface_a"] not in iface or x["interface_b"] not in iface: raise VehicleAssemblyViolation("unmatched interface")
        r=math.dist(world[x["interface_a"]],world[x["interface_b"]]); maxr=max(maxr,r)
        if r>tol: raise VehicleAssemblyViolation("interface mismatch")
        edges.append((iface[x["interface_a"]]["component_id"],iface[x["interface_b"]]["component_id"]))
    root=a.components[0].component_id
    if any(not path(edges,root,x.component_id) for x in a.components): raise VehicleAssemblyViolation("floating component")
    lo,hi=a.envelope
    for x in a.components:
        low,high=x.bounds
        if any(low[i]<lo[i]-tol or high[i]>hi[i]+tol for i in range(3)): raise VehicleAssemblyViolation("envelope violation")
        if any(all(min(high[i],kh[i])-max(low[i],kl[i])>tol for i in range(3)) for _,kl,kh in a.keepouts): raise VehicleAssemblyViolation("keepout overlap")
    for n,x in enumerate(a.components):
        for y in a.components[n+1:]:
            if all(min(x.bounds[1][i],y.bounds[1][i])-max(x.bounds[0][i],y.bounds[0][i])>tol for i in range(3)): raise VehicleAssemblyViolation("solid overlap")
    contact_components=[]
    for x in a.contacts:
        if x["interface_id"] not in iface or abs(world[x["interface_id"]][2])>a.tolerances["ground_position_m"]: raise VehicleAssemblyViolation("invalid ground contact")
        contact_components.append(iface[x["interface_id"]]["component_id"])
    sources=[x.component_id for x in a.components if "energy_source" in x.tags]; props=[x.component_id for x in a.components if "propulsion" in x.tags]
    if not sources or not props or any(not path(a.energy_edges,s,p) for s in sources for p in props): raise VehicleAssemblyViolation("disconnected energy path")
    if any(not path(edges,l,c) for l in a.loads for c in contact_components): raise VehicleAssemblyViolation("disconnected load path")
    return {"status":"passed","maximum_interface_residual_m":maxr,"mass_properties":mass_properties(a),"contact_components":tuple(contact_components)}
def declaration_sha256(raw): return hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
