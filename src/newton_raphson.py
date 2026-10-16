from dataclasses import dataclass
import numpy as np
from .validation import validate
from .ybus import build_ybus
from .power_equations import indices, mismatch
from .jacobian import jacobian

@dataclass
class Solution:
    converged: bool
    message: str
    vm: np.ndarray
    va: np.ndarray
    history: list
    iterations: int

def solve(buses, lines, tolerance=1e-10, max_iterations=30):
    validate(buses,lines)
    if not np.isfinite(tolerance) or tolerance<=0: raise ValueError('Invalid tolerance')
    if isinstance(max_iterations,bool) or not isinstance(max_iterations,(int,np.integer)) or max_iterations<0:
        raise ValueError('Maximum iterations must be a nonnegative integer')
    ybus=build_ybus(buses,lines);ns,pq=indices(buses)
    vm=buses.vm_pu.to_numpy(float).copy();va=np.deg2rad(buses.va_deg.to_numpy(float))
    history=[]
    for k in range(max_iterations+1):
        f=mismatch(buses,ybus,vm,va)
        err=float(np.max(np.abs(f),initial=0))
        history.append({'iteration':k,'max_mismatch_pu':err})
        if np.isfinite(err) and err<tolerance: return Solution(True,'Converged',vm,va,history,k)
        if not np.isfinite(err): return Solution(False,'Non-finite mismatch',vm,va,history,k)
        if k==max_iterations: break
        try: dx=np.linalg.solve(jacobian(ybus,vm,va,ns,pq),f)
        except np.linalg.LinAlgError: return Solution(False,'Singular Jacobian',vm,va,history,k)
        vm_new=vm.copy();va_new=va.copy()
        va_new[ns]+=dx[:len(ns)];vm_new[pq]+=dx[len(ns):]
        if not np.isfinite(dx).all() or (vm_new<=0).any():
            return Solution(False,'Invalid Newton step',vm,va,history,k)
        vm,va=vm_new,va_new
    return Solution(False,'Maximum iterations reached',vm,va,history,max_iterations)
