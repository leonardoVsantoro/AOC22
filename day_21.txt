def _eval(string):
    try:
        _return = eval(string)
    except:
        _return = None
    return _return

def _getparents(string):
    if '+' in string:
        return string.split(' + ')[0],string.split(' + ')[1], '+'
    if '*' in string:
        return string.split(' * ')[0],string.split(' * ')[1], '*'
    if '-' in string:
        return string.split(' - ')[0],string.split(' - ')[1], '-'
    if '/' in string:
        return string.split(' / ')[0],string.split(' / ')[1], '/'
    else:
        return None
    
def fillvalue(monkey):
    op = monkey.op
    if op=='+':
        return monkeys[monkey.parents[0]].value + monkeys[monkey.parents[1]].value
    if op=='*':
        return monkeys[monkey.parents[0]].value * monkeys[monkey.parents[1]].value
    if op=='/':
        return monkeys[monkey.parents[0]].value / monkeys[monkey.parents[1]].value
    if op=='-':
        return monkeys[monkey.parents[0]].value - monkeys[monkey.parents[1]].value
    
class monkey_class (object):
    def __init__(self, monkey, val,parents):
            self.name = monkey
            self.parents = (parents[0], parents[1]) if parents != None else None; 
            self.op = parents[2]  if parents != None else None; 
            self.value = val
    def __repr__(self):
        return self.name

data = open('input_21.txt').read().split('\n')

all_vals = [_eval(_.split(': ')[1]) for _ in data]
all_monkeys = [_[:4] for _ in data]
all_parents = [_getparents(_[6:]) for _ in data] 

    
monkeys = {name: monkey_class(name,val,parents) for (name,val,parents) in zip(all_monkeys,all_vals,all_parents)}
uncovered_monkeys = set(monkey.name for monkey in monkeys.values() if monkey.value != None)
          

while 'root' not in uncovered_monkeys:
    for monkey in monkeys.values():
        if monkey.parents != None:
            if (monkey.parents[0] in uncovered_monkeys) and (monkey.parents[1] in uncovered_monkeys):
                monkey.value = fillvalue(monkey)
                uncovered_monkeys.add(monkey.name)
print('Part 1 : {}'.format(monkeys['root'].value))

import sympy

L,R  = monkeys['root'].parents
monkeys = {name: monkey_class(name,val,parents) for (name,val,parents) in zip(all_monkeys,all_vals,all_parents)
          if name != 'root'}
monkeys['humn'].value = sympy.Symbol('x')    
uncovered_monkeys = set(monkey.name for monkey in monkeys.values() if monkey.value != None)
          

while L not in uncovered_monkeys or R not in uncovered_monkeys:
    for monkey in monkeys.values():
        if monkey.parents != None:
            if (monkey.parents[0] in uncovered_monkeys) and (monkey.parents[1] in uncovered_monkeys):
                monkey.value = fillvalue(monkey)
                uncovered_monkeys.add(monkey.name)
print('Part 2 : {}'.format(sympy.solve( monkeys[L].value - monkeys[R].value)[0]))

print()