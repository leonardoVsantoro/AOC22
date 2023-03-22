import numpy as np
from numpy.linalg import norm

filename = 'input_9.txt'
with open(filename) as fp:
    lines = fp.readlines()
    
lines = [line[:-1] if line[-1:] == '\n' else line for line in lines]

directions = [line[0] for line in lines]
steps = np.array([line[2:] for line in lines]).astype(int)

full_steps_H = []
for dir_,n_steps in zip(directions,steps):
    for _ in range(n_steps):
        full_steps_H.append(dir_)

where_is_H_has_been = []
where_is_T_has_been = []

where_is_H = 0; where_is_H_has_been = [where_is_H]
where_is_T = 0;  where_is_T_has_been = [where_is_T]

delta_dict_ = {'R': 1, 'L':-1, 'U': 1j, 'D': -1j}

for dir_ in (full_steps_H):
    where_is_H = where_is_H + delta_dict_[dir_]
    where_is_H_has_been.append(where_is_H)
    if norm(where_is_H - where_is_T) > 2**.5:
        where_is_T =  where_is_H_has_been[-2]
        where_is_T_has_been.append(where_is_T)
    else: 
        where_is_T_has_been.append(where_is_T)
        
print('Part 2: {}'.format(len(set(where_is_H_has_been))))
print('Part 2: {}'.format(len(set(where_is_T_has_been))))
        
