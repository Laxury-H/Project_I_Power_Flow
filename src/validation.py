"""Reject unsupported models and disconnected networks before solving."""
import numpy as np
BUS_COLUMNS = ['bus','type','pg_pu','qg_pu','pd_pu','qd_pu','vm_pu','va_deg']
LINE_COLUMNS = ['from_bus','to_bus','r_pu','x_pu']

def validate(buses, lines):
    for frame, columns in [(buses, BUS_COLUMNS),(lines, LINE_COLUMNS)]:
        if set(frame.columns) != set(columns):
            raise ValueError(f'Expected exactly these columns: {columns}')
        if frame.empty: raise ValueError('Empty input table')
    for frame, columns in [(buses,[c for c in BUS_COLUMNS if c!='type']),(lines,LINE_COLUMNS)]:
        try: a=frame[columns].to_numpy(dtype=float)
        except (TypeError,ValueError) as exc: raise ValueError('Non-numeric input') from exc
        if not np.isfinite(a).all(): raise ValueError('Non-finite input')
    ids=buses.bus.to_numpy()
    if not np.equal(ids, np.floor(ids)).all() or len(set(ids))!=len(ids):
        raise ValueError('Bus IDs must be unique integers')
    if not buses.type.isin(['Slack','PV','PQ']).all(): raise ValueError('Unknown bus type')
    if (buses.type=='Slack').sum()!=1: raise ValueError('Exactly one Slack bus required')
    if (buses.vm_pu<=0).any(): raise ValueError('Voltage magnitude must be positive')
    if (buses[['pd_pu','qd_pu']]<0).any().any(): raise ValueError('Demand must be nonnegative')
    if (lines.r_pu<0).any() or (lines.x_pu<=0).any():
        raise ValueError('This series inductive line model requires R >= 0 and X > 0')
    graph={i:set() for i in ids}
    for row in lines.itertuples():
        a,b=row.from_bus,row.to_bus
        if a not in graph or b not in graph or a==b: raise ValueError('Invalid line endpoint')
        graph[a].add(b);graph[b].add(a)
    visited=set(); todo=[ids[0]]
    while todo:
        a=todo.pop()
        if a not in visited: visited.add(a);todo.extend(graph[a]-visited)
    if len(visited)!=len(ids): raise ValueError('Disconnected network')
