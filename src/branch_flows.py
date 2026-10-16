import numpy as np
import pandas as pd
from .power_equations import power
from .ybus import build_ybus

def output_tables(buses,lines,solution,base_mva=100.):
    if not solution.converged: raise ValueError('Cannot publish an unconverged state as a solution')
    if not np.isfinite(base_mva) or base_mva<=0: raise ValueError('Invalid MVA base')
    v=solution.vm*np.exp(1j*solution.va)
    p,q=power(build_ybus(buses,lines),solution.vm,solution.va)
    bus=pd.DataFrame({'bus':buses.bus,'type':buses.type,'vm_pu':solution.vm,
        'va_deg':np.rad2deg(solution.va),'p_net_MW':p*base_mva,'q_net_Mvar':q*base_mva,
        'pg_MW':(p+buses.pd_pu)*base_mva,'qg_Mvar':(q+buses.qd_pu)*base_mva,
        'pd_MW':buses.pd_pu*base_mva,'qd_Mvar':buses.qd_pu*base_mva})
    ix={b:i for i,b in enumerate(buses.bus)};rows=[]
    for r in lines.itertuples():
        i,j=ix[r.from_bus],ix[r.to_bus];z=complex(r.r_pu,r.x_pu)
        current=(v[i]-v[j])/z
        sf=v[i]*np.conj(current)*base_mva;st=v[j]*np.conj(-current)*base_mva
        rows.append([r.from_bus,r.to_bus,sf.real,sf.imag,st.real,st.imag,
                     (sf+st).real,(sf+st).imag,abs(current)**2*r.r_pu*base_mva])
    branch=pd.DataFrame(rows,columns=['from_bus','to_bus','p_from_MW','q_from_Mvar',
        'p_to_MW','q_to_Mvar','p_loss_MW','q_absorption_Mvar','i2r_MW'])
    return bus,branch
