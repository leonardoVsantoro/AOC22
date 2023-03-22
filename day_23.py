import numpy as np
data = np.array(open('input_23.txt').read().split('\n'))

ps0 = set()
for j, row in enumerate(data):
    for i, el in enumerate(row): 
        if el == '#':
            ps0.add(i-j*1j)
        
moves = [ 1j, -1j, -1, 1 ]
_check = { 1j : np.array([0,1,2]),  -1j : np.array([4,5,6]) , 1  : np.array([2,3,4]), -1  : np.array([6,7,0])}

for _round in range(10):
    occupied = set(); abort = set(); ps1 = list()
    for p0 in ps0:
        conditions = np.array([ p0 + delta not in ps0 
                for delta in [-1+1j,  1j,  1j+1,  1,   1-1j,     -1j, -1j -1,  -1 ] ] ) 
        p1 = p0;
        if not all(conditions):
            for move in moves:
                if all(conditions[_check[move]]):
                    p1 = p0 + move
                    if p1 in occupied:
                        abort.add(p1)
                    else:
                        occupied.add(p1)
                    break 
        ps1.append(p1) 
    ps1 = set ( p0 if p1 in abort else p1 for p0,p1 in zip(ps0,ps1)); ps0 = ps1
    moves = np.roll(moves,-1)  

ps_final = np.array(list(ps0))
left = ps_final.real.min();right = ps_final.real.max();
lower = ps_final.imag.min(); upper = ps_final.imag.max() 

print('Part 1 : {}'.format( (abs(right - left) + 1 )*(abs(upper - lower) + 1) - len(ps0)))


ps0 = set()
for j, row in enumerate(data):
    for i, el in enumerate(row): 
        if el == '#':
            ps0.add(i-j*1j)
        
moves = [ 1j, -1j, -1, 1 ]
_check = { 1j : np.array([0,1,2]),  -1j : np.array([4,5,6]) , 1  : np.array([2,3,4]), -1  : np.array([6,7,0])} 

_round = 1
while True:
    occupied = set(); abort = set(); ps1 = list()
    for p0 in ps0:
        conditions = np.array([ p0 + delta not in ps0 
                for delta in [-1+1j,  1j,  1j+1,  1,   1-1j,     -1j, -1j -1,  -1 ] ] ) 
        p1 = p0;
        if not all(conditions):
            for move in moves:
                if all(conditions[_check[move]]):
                    p1 = p0 + move
                    if p1 in occupied:
                        abort.add(p1)
                    else:
                        occupied.add(p1)
                    break 
        ps1.append(p1) 
    ps1 = set ( p0 if p1 in abort else p1 for p0,p1 in zip(ps0,ps1));
    if ps0 == ps1:
        break
    ps0 = ps1
    moves = np.roll(moves,-1)  
    _round +=1

ps_final = np.array(list(ps0))

print('Part 2 : {}'.format( _round))
