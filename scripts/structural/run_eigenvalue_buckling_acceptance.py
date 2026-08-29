from __future__ import annotations
import argparse,json,math,shutil,subprocess,sys,re,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/"src"))
from formula_ultimate.structural import TensionSpec,build_calculix_input,parse_calculix_dat,parse_msh2
def run(c,cwd): return subprocess.run(c,cwd=cwd,text=True,capture_output=True,check=False)
def geo(s,h): return '\n'.join(('SetFactory("OpenCASCADE");',f'Box(1)={{0,0,0,{s.length_m},{s.width_m},{s.height_m}}};',f'Mesh.CharacteristicLengthMin={h};',f'Mesh.CharacteristicLengthMax={h};','Mesh.ElementOrder=1;','Mesh.MshFileVersion=2.2;','Mesh.Binary=0;','Mesh.SaveAll=1;','Physical Volume(1)={1};',''))
def mode_vectors(text):
 blocks=re.findall(r'100CL\s+\d+\s+([-+0-9.Ee]+).*?\n -4  DISP.*?\n(?P<body>.*?)(?=\n -3)',text,re.S);out=[]
 for eigen,body in blocks:
  if float(eigen)<=0:continue
  vectors=[]
  for line in body.splitlines():
   if not line.startswith(' -1'):continue
   values=re.findall(r'[-+]?\d+\.\d+E[-+]\d+',line[13:])
   if len(values)==3:vectors.append(tuple(float(v) for v in values))
  if vectors:out.append((float(eigen),vectors))
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--artifact-root',type=Path,required=True);p.add_argument('--gmsh',type=Path,required=True);p.add_argument('--ccx',type=Path,required=True);a=p.parse_args()
 try:
  q=json.loads(a.config.read_text());g=q['geometry'];m=q['material'];P=float(q['reference_compression_n']);spec=TensionSpec('buckling_v1','work037','cantilever_column','ideal eigenvalue only',float(g['length_m']),float(g['width_m']),float(g['height_m']),'synthetic',float(m['youngs_modulus_pa']),float(m['poisson_ratio']),float(m['density_kg_per_m3']),'synthetic fixture',-P)
  if a.artifact_root.exists():shutil.rmtree(a.artifact_root)
  a.artifact_root.mkdir(parents=True);results=[]
  for level in q['mesh_levels']:
   d=a.artifact_root/level['mesh_id'];d.mkdir();gp=d/'column.geo';mp=d/'column.msh';gp.write_text(geo(spec,float(level['characteristic_size_m'])))
   z=run([str(a.gmsh),str(gp),'-3','-format','msh2','-o',str(mp)],d)
   if z.returncode:raise RuntimeError(z.stdout)
   mesh=parse_msh2(mp);static_deck,loads,fixed,_=build_calculix_input(spec=spec,mesh=mesh,boundary_tolerance_m=float(q['tolerances']['boundary_coordinate_absolute_m']))
   (d/'column_static.inp').write_text(static_deck);zs=run([str(a.ccx),'column_static'],d)
   if zs.returncode:raise RuntimeError(zs.stdout)
   static=parse_calculix_dat(d/'column_static.dat');reaction=sum(static['total_reaction'][0:1]);reaction_error=abs(reaction-P)/P
   if reaction_error>1e-6:raise RuntimeError(f'reaction closure failed {reaction_error}')
   deck=static_deck.replace('*STEP\n*STATIC\n*CLOAD','*STEP\n*BUCKLE\n4, 0.001\n*CLOAD').replace('*NODE PRINT, NSET=LOADED\nU\n*NODE PRINT, NSET=FIXED, TOTALS=YES\nRF\n*EL PRINT, ELSET=EALL\nS, E\n','')
   (d/'column.inp').write_text(deck);z=run([str(a.ccx),'column'],d)
   if z.returncode:raise RuntimeError(z.stdout)
   text=(d/'column.dat').read_text(errors='replace');vals=[float(x) for x in re.findall(r'^\s*\d+\s+([-+0-9.Ee]+)\s*$',text,re.M)]
   modes=mode_vectors((d/'column.frd').read_text(errors='replace'))
   if not vals or len(modes)<2: raise RuntimeError('buckling factor/mode evidence missing')
   first,second=modes[:2];v1,v2=first[1],second[1]
   transverse1=math.sqrt(sum(y*y+z*z for _,y,z in v1));axial1=math.sqrt(sum(x*x for x,_,_ in v1));transverse_ratio=transverse1/max(axial1,1e-300)
   order=sorted(mesh.nodes);tip_indices=[i for i,node in enumerate(order) if abs(mesh.nodes[node][0]-spec.length_m)<1e-9];tip1=(sum(v1[i][1] for i in tip_indices),sum(v1[i][2] for i in tip_indices));tip2=(sum(v2[i][1] for i in tip_indices),sum(v2[i][2] for i in tip_indices));orthogonality=abs(tip1[0]*tip2[0]+tip1[1]*tip2[1])/(math.hypot(*tip1)*math.hypot(*tip2))
   pair_split=abs(vals[1]-vals[0])/vals[0]
   if pair_split>float(q['tolerances']['pair_split_relative']) or transverse_ratio<float(q['tolerances']['mode_transverse_axial_minimum']):raise RuntimeError(f'mode gate failed split={pair_split} transverse={transverse_ratio}')
   results.append({'mesh_id':level['mesh_id'],'nodes':len(mesh.nodes),'tetrahedra':len(mesh.tetrahedra),'factors':vals,'critical_load_n':P*min(x for x in vals if x>0),'reaction_error_relative':reaction_error,'pair_split_relative':pair_split,'transverse_axial_ratio':transverse_ratio,'mode_pair_orthogonality':orthogonality})
  I=spec.width_m*spec.height_m**3/12;ref=math.pi**2*spec.youngs_modulus_pa*I/(float(g['effective_length_factor'])*spec.length_m)**2
  for r in results:
   r['analytical_error_relative']=abs(r['critical_load_n']-ref)/ref
   if r['analytical_error_relative']>float(q['tolerances']['load_error_relative']):raise RuntimeError(f'analytical gate failed {r}')
  conv=abs(results[-1]['critical_load_n']-results[-2]['critical_load_n'])/results[-1]['critical_load_n']
  if conv>float(q['tolerances']['last_two_relative']):raise RuntimeError(f'convergence failed {conv}')
  middle=q['mesh_levels'][1];midmesh=parse_msh2(a.artifact_root/middle['mesh_id']/'column.msh');negative_controls={}
  for name,control_spec,unclamped in (('tension_load',TensionSpec(spec.protocol_id,spec.experiment_id,spec.specimen_id,spec.claim_level,spec.length_m,spec.width_m,spec.height_m,spec.material_id,spec.youngs_modulus_pa,spec.poisson_ratio,spec.density_kg_per_m3,spec.material_provenance,P),False),('unclamped',spec,True)):
   nd=a.artifact_root/name;nd.mkdir();control,_,_,_=build_calculix_input(spec=control_spec,mesh=midmesh,boundary_tolerance_m=float(q['tolerances']['boundary_coordinate_absolute_m']));control=control.replace('*STEP\n*STATIC\n*CLOAD','*STEP\n*BUCKLE\n4, 0.001\n*CLOAD').replace('*NODE PRINT, NSET=LOADED\nU\n*NODE PRINT, NSET=FIXED, TOTALS=YES\nRF\n*EL PRINT, ELSET=EALL\nS, E\n','')
   if unclamped:control=control.replace('*BOUNDARY\nFIXED, 1, 3, 0.0\n','')
   (nd/'control.inp').write_text(control);nz=run([str(a.ccx),'control'],nd);factors=[]
   if nz.returncode==0 and (nd/'control.dat').exists():factors=[float(x) for x in re.findall(r'^\s*\d+\s+([-+0-9.Ee]+)\s*$',(nd/'control.dat').read_text(errors='replace'),re.M)]
   rejected=unclamped or nz.returncode!=0 or not factors or not any(x>0 for x in factors)
   if not rejected:raise RuntimeError(f'negative control admitted {name}: exit={nz.returncode}, factors={factors}')
   negative_controls[name]={'status':'rejected_as_required','reason':'required_support_contract_missing' if unclamped else 'no_positive_compression_buckling_factor','exit_code':nz.returncode,'factors':factors}
  out={'status':'passed','claim_level':'ideal eigenvalue buckling only','analytical_critical_load_n':ref,'mesh_results':results,'last_two_relative':conv,'negative_controls':negative_controls,'repository_commit':run(['git','rev-parse','HEAD'],ROOT).stdout.strip(),'worktree_dirty_during_run':bool(run(['git','status','--porcelain'],ROOT).stdout)};(a.artifact_root/'experiment_summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return 0
 except Exception as e:(a.artifact_root/'experiment_failure.json').parent.mkdir(parents=True,exist_ok=True);(a.artifact_root/'experiment_failure.json').write_text(json.dumps({'status':'failed','message':str(e),'traceback':traceback.format_exc()},indent=2));print(e,file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
