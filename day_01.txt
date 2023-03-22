import os
import numpy as np

filename = 'input_1.txt'
data = []
with open(filename) as fp:
    lines = fp.readlines()
_single_data = []
for line in lines:
    if line != '\n':
        _single_data.append(line[:-1]) 
    else:
        _single_data = np.array(_single_data).astype(int).sum()
        data.append(_single_data)
        _single_data = []
data = np.array(data)

print('Part 1: {}'.format(np.max(data)))

print('Part 2: {}'.format(np.sort(data)[-3:].sum()))

