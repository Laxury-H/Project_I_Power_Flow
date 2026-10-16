"""Independent package comparison; never used by the project solver."""
from pathlib import Path
import numpy as np
import pandas as pd
from pypower.api import runpf, ppoption
from src.data_models import load_case
from src.newton_raphson import solve
from src.branch_flows import output_tables

def main():
 rows=[]
 for name in ['3bus','5bus']:
  for scale in [.8,1.,1.2]:
   b,l=load_case(name);b[['pd_pu','qd_pu']]*=scale;n=len(b)
   bus=np.zeros((n,13));bus[:,0]=b.bus;bus[:,1]=b.type.map({'Slack':3,'PV':2,'PQ':1})
   bus[:,2]=100*b.pd_pu;bus[:,3]=100*b.qd_pu;bus[:,6]=1;bus[:,7]=b.vm_pu;bus[:,8]=b.va_deg
   bus[:,9]=110;bus[:,10]=1;bus[:,11]=1.1;bus[:,12]=.9
   genrows=[]
   for r in b[b.type!='PQ'].itertuples():
    genrows.append([r.bus,100*r.pg_pu,100*r.qg_pu,999,-999,r.vm_pu,100,1,999,-999]+[0]*11)
   br=np.zeros((len(l),13));br[:,0]=l.from_bus;br[:,1]=l.to_bus;br[:,2]=l.r_pu;br[:,3]=l.x_pu
   br[:,10]=1;br[:,11]=-360;br[:,12]=360
   result,ok=runpf({'version':'2','baseMVA':100.,'bus':bus,'gen':np.array(genrows,float),'branch':br},
                   ppoption(VERBOSE=0,OUT_ALL=0,PF_TOL=1e-10,ENFORCE_Q_LIMS=0))
   s=solve(b,l);_,flows=output_tables(b,l,s)
   vmerr=float(np.max(abs(s.vm-result['bus'][:,7])))
   vaerr=float(np.max(abs(np.rad2deg(s.va)-result['bus'][:,8])))
   losserr=float(abs(flows.p_loss_MW.sum()-(result['branch'][:,13]+result['branch'][:,15]).sum()))
   assert ok and vmerr<1e-8 and vaerr<1e-6 and losserr<1e-6
   rows.append([name,scale,vmerr,vaerr,losserr,'Pass'])
 out=pd.DataFrame(rows,columns=['case','load_scale','max_voltage_error_pu','max_angle_error_deg','loss_error_MW','status'])
 out.to_csv(Path(__file__).parent/'results/pypower_comparison.csv',index=False)
 print(out.to_string(index=False))
if __name__=='__main__':main()
