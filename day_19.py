import numpy as np
import gurobipy
import pyomo.environ as pyo
from time import perf_counter

def _get_blueprint_dict(i):
    idata = data[i]
    _dict_ = {}
    _dict_.update({ 'ore' :{'ore' : eval(idata[0].split(' Each ore robot costs ')[1].split(' ore')[0]),
        'clay': 0, 'obsidian': 0, 'geode':0}})
    _dict_.update({ 'clay' :{'ore' :  eval(idata[1].split(' Each clay robot costs ')[1].split(' ore')[0]),
        'clay': 0, 'obsidian': 0, 'geode':0}})
    _dict_.update({ 'obsidian' :{'ore':eval(idata[2].split(' Each obsidian robot costs ')[1].split(' ore')[0]),
     'clay':eval(idata[2].split(' Each obsidian robot costs ')[1].split(' clay')[0].split('ore and ')[1])
   , 'obsidian': 0,'geode':0}})
    _dict_.update({ 'geode' :{'ore' :  eval(idata[3].split(' Each geode robot costs ')[1].split(' ore')[0]),
  'clay': 0, 
  'obsidian': eval(idata[3].split(' Each geode robot costs ')[1].split(' obsidian' )[0].split('ore and ')[1]),
  'geode':0}})
    return _dict_                  
data = [ _.split('.') for _ in open('input_19.txt').read().split('\n') ] 
blueprints = [_get_blueprint_dict(i) for i in np.arange(len(data))]



def max_geodes_open(blueprint,n_minutes):    
    
    types = ['ore', 'clay', 'obsidian', 'geode']    
    
    
    model = pyo.ConcreteModel('Max geodes open')
    

    model.time_shift = pyo.Set(initialize=list(range(1,n_minutes +1)))
    model.shift_time_shift = pyo.Set(initialize=list(range(0,n_minutes+1)))
    model.types = pyo.Set(initialize = types)

    model.create_robot = pyo.Var(model.shift_time_shift, model.types, domain=pyo.Binary)
    
    model.resources = pyo.Var(model.shift_time_shift,  model.types, domain=pyo.NonNegativeIntegers)
    

    @model.Objective(sense = pyo.maximize)
    def total_opened_geodes(m):
        return m.resources[n_minutes,'geode']

    @model.Constraint(model.types)
    def one_ore_at_start(m, i):
        if i == 'ore':
            return m.create_robot[0, i] == 1
        else:
            return m.create_robot[0, i] == 0
            
    
    @model.Constraint()
    def no_resources_at_start(m):
        return sum(m.resources[0, i] for i in types) ==0
    
    @model.Constraint(model.shift_time_shift)
    def create_one_robot_at_the_time(m,t):
        return sum(m.create_robot[t, i] for i in types) <= 1
    
    @model.Constraint(model.time_shift, model.types)
    def resources_dont_magically_appear(m,t,i):
        return model.resources[t,i] == model.resources[t-1,i] \
                                + sum(m.create_robot[s,i] for s in m.shift_time_shift if s<t) \
                                - sum(m.create_robot[t,j]*blueprint[j][i] for j in m.types)
  
    @model.Constraint(model.time_shift, model.types)
    def cant_buy_in_advance(m,t,i):
        return sum(m.create_robot[t,j]*blueprint[j][i] for j in m.types) <= model.resources[t-1,i]
        
    
    @model.Constraint(model.shift_time_shift, model.types)
    def no_loans(m,t,i):
        return model.resources[t,i] >= 0
   
    return model

res = 0
for i, blueprint in enumerate(blueprints):
#     print(f'\nBlueprint {i+1}')
    tstart = perf_counter()
    m = max_geodes_open(blueprint,24)

    result = pyo.SolverFactory('gurobi').solve(m)
#     print(f'Solver status: {result.solver.status}, {result.solver.termination_condition}')
    tot_opened_geodes = int(pyo.value(m.total_opened_geodes()))
#     print(f'Max number of geodes that can be opened: {tot_opened_geodes}')
    tend = perf_counter()
#     print(f'Elapsed time: {tend-tstart:.4f} seconds\n')
    res += tot_opened_geodes*(i+1)
print(f'\n Part 1 : {res}')

res = 1
for i, blueprint in enumerate(blueprints[:3]):
#     print(f'\nBlueprint {i+1}')
    tstart = perf_counter()
    m = max_geodes_open(blueprint,32)

    result = pyo.SolverFactory('gurobi').solve(m)
#     print(f'Solver status: {result.solver.status}, {result.solver.termination_condition}')
    tot_opened_geodes = int(pyo.value(m.total_opened_geodes()))
#     print(f'Max number of geodes that can be opened: {tot_opened_geodes}')
    tend = perf_counter()
#     print(f'Elapsed time: {tend-tstart:.4f} seconds\n')
    res = res* tot_opened_geodes
print(f'\n Part 2 : {res}')
