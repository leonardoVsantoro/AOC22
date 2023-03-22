import numpy as np 
data = open('input_14.txt').read().split("\n")
data = [_.split('->') for _ in data]

from collections import defaultdict
occupied = defaultdict(list)
rocks = occupied.copy()
            
for traj in data:
    for xyS,xyE in zip(traj[:-1],traj[1:]):
        (xS,yS) = eval(xyS.strip()); (xE,yE) = eval(xyE.strip());
        if xS == xE:
            for y in np.arange(min([yS,yE]), max([yS,yE])+1) :
                occupied[(xS,y)] = 'occupied'
        if yS == yE:
            for x in np.arange(min([xS,xE]), max([xS, xE])+1) :
                occupied[(x,yS)] = 'occupied'

rocks = occupied.copy()
max_y_height = max([y for (x,y) in rocks.keys()])

        
def whereIfall(loc,max_y_height):
    x,y = loc
    if y < max_y_height:
        if occupied[x,y+1] != 'occupied':
            return (x,y+1)
        if occupied[x-1,y+1] != 'occupied':
            return (x-1,y+1)
        if occupied[x+1,y+1] != 'occupied':
            return (x+1,y+1)
        else:
            return (x,y)
    else:    
        return (x,y)
    

def new_fall(loc,max_y_height):
    x,y = loc
    if whereIfall((x,y),max_y_height) == (x,y):
        return (x,y)
    else:
        return new_fall(whereIfall((x,y),max_y_height),max_y_height)

start_x = 500; start_y =0

i=0; y = 0
while y < max_y_height:
    (x,y) = new_fall((start_x,start_y),max_y_height)
    occupied[x,y] = 'occupied'
    i = i+1
print('Part 1: {}'.format(i-1))

occupied = rocks.copy()
max_y_height = max_y_height + 1
i=0; y = 0
while (x,y) != (start_x,start_y):
    (x,y) = new_fall((start_x,start_y),max_y_height)
    occupied[x,y] = 'occupied'
    i = i+1
print('Part 2: {}'.format(i))
    
