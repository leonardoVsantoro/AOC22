import numpy as np
filename = 'input_6.txt'
with open(filename) as fp:
    data = fp.readlines()[0]

for i in np.arange(len(data)-4):
    if len(set(data[i:i+4])) == 4:
        print('Part 1: {}'.format(i+4))
        break
        
for i in np.arange(len(data)-14):
    if len(set(data[i:i+14])) == 14:
        print('Part 2: {}'.format(i+14))
        break
