import os
import numpy as np

filename = 'input_4.txt'

with open(filename) as fp:
    lines = fp.readlines()
lines = [line[:-1] if line[-1:] == '\n' else line for line in lines]

C1s = []; C2s = [];
for line in lines:
    ix = np.where(np.array([_ for _ in line])==',')[0][0]
    lineONE = line[:ix]; lineTWO = line[ix+1:]
    ixONE = np.where(np.array([_ for _ in lineONE])=='-')[0][0]
    ixTWO = np.where(np.array([_ for _ in lineTWO])=='-')[0][0]
    C1s.append(np.arange(int(lineONE[:ixONE]), int(lineONE[ixONE+1:])+1))
    C2s.append(np.arange(int(lineTWO[:ixTWO]), int(lineTWO[ixTWO+1:])+1))

n_nested_pairs=0
for c1,c2 in zip(C1s,C2s):
    if set(c1).intersection(set(c2)) == set(c1) or set(c1).intersection(set(c2)) == set(c2):
        n_nested_pairs=n_nested_pairs+1
n_nested_pairs

n_intersecting_pairs=0
for c1,c2 in zip(C1s,C2s):
    if len(set(c1).intersection(set(c2)))>0:
        n_intersecting_pairs=n_intersecting_pairs+1
n_intersecting_pairs
