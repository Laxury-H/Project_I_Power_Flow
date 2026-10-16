"""Derivative of CALCULATED injections, not of specified-minus-calculated mismatch."""
import numpy as np
from .power_equations import power

def jacobian(ybus, vm, va, ns, pq):
    p,q=power(ybus,vm,va);g,b=ybus.real,ybus.imag
    n=len(vm);H=np.zeros((n,n));N=H.copy();M=H.copy();L=H.copy()
    for i in range(n):
        for j in range(n):
            if i==j:
                H[i,i]=-q[i]-b[i,i]*vm[i]**2
                N[i,i]=p[i]/vm[i]+g[i,i]*vm[i]
                M[i,i]=p[i]-g[i,i]*vm[i]**2
                L[i,i]=q[i]/vm[i]-b[i,i]*vm[i]
            else:
                d=va[i]-va[j];c,s=np.cos(d),np.sin(d)
                H[i,j]=vm[i]*vm[j]*(g[i,j]*s-b[i,j]*c)
                N[i,j]=vm[i]*(g[i,j]*c+b[i,j]*s)
                M[i,j]=-vm[i]*vm[j]*(g[i,j]*c+b[i,j]*s)
                L[i,j]=vm[i]*(g[i,j]*s-b[i,j]*c)
    return np.block([[H[np.ix_(ns,ns)],N[np.ix_(ns,pq)]],
                     [M[np.ix_(pq,ns)],L[np.ix_(pq,pq)]]])
