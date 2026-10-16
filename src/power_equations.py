import numpy as np

def power(ybus, vm, va):
    """Angles in radians. Positive P,Q are net injections into the network."""
    voltage=vm*np.exp(1j*va)
    s=voltage*np.conj(ybus@voltage)
    return s.real,s.imag

def indices(buses):
    return np.flatnonzero(buses.type.to_numpy()!='Slack'), np.flatnonzero(buses.type.to_numpy()=='PQ')

def mismatch(buses, ybus, vm, va):
    ns,pq=indices(buses)
    p,q=power(ybus,vm,va)
    ps=(buses.pg_pu-buses.pd_pu).to_numpy()
    qs=(buses.qg_pu-buses.qd_pu).to_numpy()
    return np.r_[ps[ns]-p[ns],qs[pq]-q[pq]]
