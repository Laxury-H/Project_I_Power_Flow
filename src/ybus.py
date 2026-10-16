"""Series-only lines; parallel branches add naturally."""
import numpy as np

def build_ybus(buses, lines):
    ix={b:i for i,b in enumerate(buses.bus)}
    ybus=np.zeros((len(buses),len(buses)),complex)
    for row in lines.itertuples():
        i,j=ix[row.from_bus],ix[row.to_bus]
        y=1/complex(row.r_pu,row.x_pu)
        ybus[i,i]+=y;ybus[j,j]+=y
        ybus[i,j]-=y;ybus[j,i]-=y
    return ybus
