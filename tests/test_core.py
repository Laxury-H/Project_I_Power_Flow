import numpy as np
import pytest
from src.data_models import load_case
from src.ybus import build_ybus
from src.power_equations import indices,mismatch,power
from src.jacobian import jacobian
from src.newton_raphson import solve
from src.branch_flows import output_tables
from src.validation import validate

@pytest.mark.parametrize('name',['3bus','5bus'])
def test_ybus_structure(name):
 b,l=load_case(name);y=build_ybus(b,l)
 assert np.allclose(y,y.T)
 assert np.allclose(y.sum(axis=1),0)

def test_ybus_values():
 b,l=load_case();y=build_ybus(b,l)
 expected=np.array([[6.25,-5,-1.25],[-5,20/3,-5/3],[-1.25,-5/3,35/12]])*(1-3j)
 assert np.allclose(y,expected)

@pytest.mark.parametrize('name',['3bus','5bus'])
def test_jacobian_finite_difference(name):
 b,l=load_case(name);y=build_ybus(b,l);ns,pq=indices(b)
 vm=b.vm_pu.to_numpy().copy();vm[pq]=np.linspace(.97,1.01,len(pq))
 va=np.linspace(0,.04,len(b));h=1e-6
 analytic=jacobian(y,vm,va,ns,pq)
 numeric=np.zeros_like(analytic)
 for k in range(len(ns)+len(pq)):
  vp,vmn=vm.copy(),vm.copy();ap,am=va.copy(),va.copy()
  if k<len(ns):ap[ns[k]]+=h;am[ns[k]]-=h
  else:vp[pq[k-len(ns)]]+=h;vmn[pq[k-len(ns)]]-=h
  numeric[:,k]=-(mismatch(b,y,vp,ap)-mismatch(b,y,vmn,am))/(2*h)
 assert analytic.shape==(len(ns)+len(pq),)*2
 assert np.max(np.abs(analytic-numeric))<1e-7

@pytest.mark.parametrize('name,states',[('3bus',3),('5bus',7)])
def test_state_count(name,states):
 b,_=load_case(name);ns,pq=indices(b);assert len(ns)+len(pq)==states

@pytest.mark.parametrize('name',['3bus','5bus'])
@pytest.mark.parametrize('scale',[.8,1.,1.2])
def test_convergence_balance_and_losses(name,scale):
 b,l=load_case(name);b[['pd_pu','qd_pu']]*=scale;s=solve(b,l)
 assert s.converged
 assert np.max(np.abs(mismatch(b,build_ybus(b,l),s.vm,s.va)))<1e-10
 bus,branch=output_tables(b,l,s)
 assert abs(bus.p_net_MW.sum()-branch.p_loss_MW.sum())<1e-9
 assert abs(bus.q_net_Mvar.sum()-branch.q_absorption_Mvar.sum())<1e-9
 assert np.allclose(branch.p_loss_MW,branch.i2r_MW,atol=1e-10,rtol=0)
 assert (branch.p_loss_MW>=-1e-10).all()
 assert np.allclose(s.vm[b.type!='PQ'],b.vm_pu[b.type!='PQ'])

def test_reference_values():
 b,l=load_case();s=solve(b,l);_,br=output_tables(b,l,s)
 assert abs(s.vm[2]-.984385)<1e-6
 assert np.max(abs(np.rad2deg(s.va[1:])-[1.024098,-2.418330]))<1e-6
 assert abs(br.p_loss_MW.sum()-2.204693)<1e-6

@pytest.mark.parametrize('defect',['duplicate','slack','type','nan','endpoint','zero_x','negative_r','island','voltage','extra_column','demand'])
def test_invalid_input(defect):
 b,l=load_case()
 if defect=='duplicate':b.loc[2,'bus']=1
 elif defect=='slack':b.loc[1,'type']='Slack'
 elif defect=='type':b.loc[1,'type']='BAD'
 elif defect=='nan':b.loc[1,'pg_pu']=np.nan
 elif defect=='endpoint':l.loc[0,'to_bus']=99
 elif defect=='zero_x':l.loc[0,'x_pu']=0
 elif defect=='negative_r':l.loc[0,'r_pu']=-1
 elif defect=='island':l=l.iloc[:1]
 elif defect=='voltage':b.loc[2,'vm_pu']=0
 elif defect=='extra_column':l['tap']=1
 elif defect=='demand':b.loc[2,'pd_pu']=-1
 with pytest.raises(ValueError):validate(b,l)

def test_iteration_limit():
 b,l=load_case();s=solve(b,l,max_iterations=0)
 assert not s.converged and s.message=='Maximum iterations reached'
 with pytest.raises(ValueError):output_tables(b,l,s)

def test_singular_jacobian_handling(monkeypatch):
 import src.newton_raphson as nr
 b,l=load_case()
 monkeypatch.setattr(nr,'jacobian',lambda y,v,a,ns,pq:np.zeros((len(ns)+len(pq),)*2))
 s=nr.solve(b,l)
 assert not s.converged and s.message=='Singular Jacobian'

def test_noncontiguous_ids():
 b,l=load_case();mapping={1:10,2:40,3:80}
 b.bus=b.bus.map(mapping)
 for c in ['from_bus','to_bus']:l[c]=l[c].map(mapping)
 assert solve(b,l).converged

def test_no_pq():
 b,l=load_case();b.loc[2,'type']='PV'
 assert solve(b,l).converged

@pytest.mark.parametrize('kwargs',[{'tolerance':0},{'tolerance':np.nan},{'max_iterations':-1},{'max_iterations':1.5}])
def test_invalid_controls(kwargs):
 b,l=load_case()
 with pytest.raises(ValueError):solve(b,l,**kwargs)
