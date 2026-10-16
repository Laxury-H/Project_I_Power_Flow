"""Reproduce CSV tables, figures and the machine-readable result summary."""
from pathlib import Path
import json,platform
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.data_models import load_case
from src.newton_raphson import solve
from src.ybus import build_ybus
from src.branch_flows import output_tables
from src.power_equations import indices,mismatch
from src.jacobian import jacobian
ROOT=Path(__file__).resolve().parent

def main():
 out=ROOT/'results';fig=ROOT/'figures';out.mkdir(exist_ok=True);fig.mkdir(exist_ok=True)
 plt.rcParams.update({'font.size':11,'figure.dpi':160,'axes.spines.top':False,'axes.spines.right':False})
 summary=[];cases={}
 for name in ['3bus','5bus']:
  for scale in [.8,1,1.2]:
   b,l=load_case(name);b[['pd_pu','qd_pu']]*=scale
   s=solve(b,l)
   if not s.converged:raise RuntimeError(s.message)
   bt,lt=output_tables(b,l,s);hist=pd.DataFrame(s.history)
   key=f'{name}_{round(scale*100)}'
   for suffix,df in [('buses',bt),('branches',lt),('convergence',hist)]:df.to_csv(out/f'{key}_{suffix}.csv',index=False)
   summary.append({'case':name,'load_percent':round(scale*100),'iterations':s.iterations,
      'residual_pu':s.history[-1]['max_mismatch_pu'],'min_voltage_pu':s.vm.min(),
      'loss_MW':lt.p_loss_MW.sum(),'q_absorption_Mvar':lt.q_absorption_Mvar.sum(),
      'p_balance_error_MW':bt.p_net_MW.sum()-lt.p_loss_MW.sum(),
      'q_balance_error_Mvar':bt.q_net_Mvar.sum()-lt.q_absorption_Mvar.sum()})
   cases[key]={'bus':bt.to_dict('records'),'branch':lt.to_dict('records'),'history':s.history}
  b,l=load_case(name);y=build_ybus(b,l)
  np.savetxt(out/f'{name}_Ybus.txt',y,fmt='%.9f')
  for quantity,label in [('vm_pu','Voltage magnitude (pu)'),('va_deg','Voltage angle (degrees)')]:
   f,ax=plt.subplots(figsize=(7,3.8))
   for scale in [80,100,120]:
    bt=pd.DataFrame(cases[f'{name}_{scale}']['bus']);ax.plot(bt.bus,bt[quantity],'-o',label=f'{scale}% load')
   ax.set(xlabel='Bus',ylabel=label,xticks=b.bus);ax.legend();ax.grid(alpha=.2);f.tight_layout()
   f.savefig(fig/f'{name}_{quantity}.png');f.savefig(fig/f'{name}_{quantity}.svg');plt.close(f)
  f,ax=plt.subplots(figsize=(7,3.8))
  for scale in [80,100,120]:
   h=pd.DataFrame(cases[f'{name}_{scale}']['history']);ax.semilogy(h.iteration,h.max_mismatch_pu,'-o',label=f'{scale}% load')
  ax.axhline(1e-10,color='gray',ls='--',label='Tolerance');ax.set(xlabel='Newton updates',ylabel='Maximum mismatch (pu)')
  ax.legend();ax.grid(alpha=.2);f.tight_layout();f.savefig(fig/f'{name}_convergence.png');plt.close(f)
 df=pd.DataFrame(summary);df.to_csv(out/'scenario_summary.csv',index=False)
 f,ax=plt.subplots(figsize=(7,3.8))
 for name,part in df.groupby('case'):ax.plot(part.load_percent,part.loss_MW,'-o',label=name)
 ax.set(xlabel='Load (% of base)',ylabel='Active power loss (MW)',xticks=[80,100,120]);ax.legend();ax.grid(alpha=.2);f.tight_layout();f.savefig(fig/'loss_comparison.png');plt.close(f)
 # Save a real first update for teaching.
 b,l=load_case();y=build_ybus(b,l);ns,pq=indices(b);vm=b.vm_pu.to_numpy();va=np.deg2rad(b.va_deg.to_numpy())
 j=jacobian(y,vm,va,ns,pq);f=mismatch(b,y,vm,va);dx=np.linalg.solve(j,f)
 (out/'first_iteration.json').write_text(json.dumps({'state_order':['delta2_rad','delta3_rad','V3_pu'],'mismatch':f.tolist(),'jacobian':j.tolist(),'update':dx.tolist(),'next_state':(np.r_[va[ns],vm[pq]]+dx).tolist()},indent=2))
 (out/'results.json').write_text(json.dumps({'base_mva':100,'tolerance':1e-10,'max_iterations':30,'scenarios':summary,'cases':cases},indent=2))
 (out/'environment.txt').write_text(f'Python {platform.python_version()}\nNumPy {np.__version__}\npandas {pd.__version__}\nMatplotlib {matplotlib.__version__}\n')
 print(df.to_string(index=False))
if __name__=='__main__':main()
