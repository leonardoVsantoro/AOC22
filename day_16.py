import numpy as np
import gurobipy
import pyomo.environ as pyo
from time import perf_counter

def getConnection(line2):
    try:
        connections =  line2.split('tunnels lead to valves ')[1].split(', ')
    except:
        connections = line2.split('tunnel leads to valve ')[1]
    return connections

data = np.array([_.split('; ') for _ in open('input_16.txt').read().split("\n")])
nodes = [line[6:8]  for line in data[:,0] ]
flow_rates = { line[6:8] : eval(line.split('=')[-1]) for line in data[:,0] }
graph = {  line1[6:8]  : getConnection(line2) for line1, line2 in data} 
edges = [(key, value) for (key,values) in graph.items() for value in values]; 


edges.append(('AA','AA'))

def max_pressure(nodes,edges,flow_rates):             
    model = pyo.ConcreteModel('Max pressure release')

    model.time_shift = pyo.Set(initialize=list(range(1,31)))
    model.shift_time_shift = pyo.Set(initialize=list(range(0,31)))

    model.nodes = pyo.Set(initialize=nodes)
    model.edges = pyo.Set(initialize=edges)

    model.flow_rates = pyo.Param(model.nodes, initialize=flow_rates)

    model.open_node = pyo.Var(model.nodes, model.shift_time_shift, domain=pyo.Binary)
    model.on_edge = pyo.Var(model.edges, model.shift_time_shift, domain=pyo.Binary)


    @model.Objective(sense = pyo.maximize)
    def total_pressure(m):
        return sum(m.open_node[i,t]*m.flow_rates[i]*(30-t) for t in m.time_shift for i in m.nodes)

    @model.Constraint(model.edges)
    def start_at_AA(m,i,j):
        if i==j:
            return m.on_edge[i,j,0]==1
        else:
            return m.on_edge[i,j,0]==0

    @model.Constraint(model.shift_time_shift)
    def either_open_or_move(m, t):
        return sum(m.open_node[i,t] for i in m.nodes) +  sum(m.on_edge[j,k,t] for j,k in m.edges) <=1

    @model.Constraint(model.nodes)
    def open_only_once(m,i):
        return sum(m.open_node[i, t] for t in m.shift_time_shift) <= 1
    
    @model.Constraint(model.nodes, model.time_shift)
    def consecutive_actions(m,i,t):
        return sum(m.on_edge[j,k,t] for j,k in edges if j ==i) + m.open_node[i,t] <= \
               sum(m.on_edge[k,l,t-1] for k,l in edges if l == i)  + m.open_node[i,t-1]
        

    result = pyo.SolverFactory('gurobi').solve(model)
    print(f'Solver status: {result.solver.status}, {result.solver.termination_condition}')

    print(f'\n Part 1 : Max pressure that can be released is {int(pyo.value(model.total_pressure()))}')
    
    return model

tstart = perf_counter()
m = max_pressure(nodes,edges,flow_rates)
tend = perf_counter()
print(f'\nElapsed time: {tend-tstart:.4f} seconds\n')


# ----

def max_pressure_with_elephant(nodes,edges,flow_rates):             
    model = pyo.ConcreteModel('Max pressure release')

    model.time = pyo.Set(initialize=list(range(0,26)))
    model.time_shift = pyo.Set(initialize=list(range(1,27)))
    model.shift_time_shift = pyo.Set(initialize=list(range(0,27)))

    model.nodes = pyo.Set(initialize=nodes)
    model.edges = pyo.Set(initialize=edges)

    model.flow_rates = pyo.Param(model.nodes, initialize=flow_rates)

    model.open_node = pyo.Var(model.nodes, model.shift_time_shift, domain=pyo.Binary)
    model.e_open_node = pyo.Var(model.nodes, model.shift_time_shift, domain=pyo.Binary)
    model.on_edge = pyo.Var(model.edges, model.shift_time_shift, domain=pyo.Binary)
    model.e_on_edge = pyo.Var(model.edges, model.shift_time_shift, domain=pyo.Binary)


    @model.Objective(sense = pyo.maximize)
    def total_pressure(m):
        return sum(m.open_node[i,t]*m.flow_rates[i]*(26-t) for t in m.time_shift for i in m.nodes) + \
               sum(m.e_open_node[i,t]*m.flow_rates[i]*(26-t) for t in m.time_shift for i in m.nodes)

    @model.Constraint(model.edges)
    def start_at_AA(m,i,j):
        if i==j:
            return m.on_edge[i,j,0] + m.e_on_edge[i,j,0] == 2
        else:
            return m.on_edge[i,j,0] + m.e_on_edge[i,j,0] == 0
        

    @model.Constraint(model.shift_time_shift)    
    def either_open_or_move(m, t):
        return sum(m.open_node[i,t] for i in m.nodes) +  sum(m.on_edge[j,k,t] for j,k in m.edges) <=1
   
    @model.Constraint(model.shift_time_shift)    
    def e_either_open_or_move(m, t):
        return sum(m.e_open_node[i,t] for i in m.nodes) +  sum(m.e_on_edge[j,k,t] for j,k in m.edges) <=1

    @model.Constraint(model.nodes)
    def open_only_once(m,i):
        return sum(m.open_node[i, t] for t in m.shift_time_shift) +\
                  sum(m.e_open_node[i, t] for t in m.shift_time_shift) <= 1
    
    @model.Constraint(model.nodes, model.time_shift)
    def consecutive_actions(m,i,t):
        return sum(m.on_edge[j,k,t] for j,k in edges if j ==i) + m.open_node[i,t] <= \
               sum(m.on_edge[k,l,t-1] for k,l in edges if l == i)  + m.open_node[i,t-1]
        
    @model.Constraint(model.nodes, model.time_shift)
    def e_consecutive_actions(m,i,t):
        return sum(m.e_on_edge[j,k,t] for j,k in edges if j ==i) + m.e_open_node[i,t] <= \
               sum(m.e_on_edge[k,l,t-1] for k,l in edges if l == i)  + m.e_open_node[i,t-1]
        


    result = pyo.SolverFactory('gurobi').solve(model)
    print(f'Solver status: {result.solver.status}, {result.solver.termination_condition}')

    print(f'\n Part 2: Max pressure that can be released is {int(pyo.value(model.total_pressure()))}')
    
    return model

tstart = perf_counter()
m = max_pressure_with_elephant(nodes,edges,flow_rates)
tend = perf_counter()
print(f'\nElapsed time: {tend-tstart:.4f} seconds\n')
