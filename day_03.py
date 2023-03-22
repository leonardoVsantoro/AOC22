import os
import numpy as np
from string import ascii_lowercase,ascii_uppercase
_letters_to_num_ = {v:k+1 for k,v in enumerate(ascii_lowercase)}
_letters_to_num_.update( {v:k+27 for k,v in enumerate(ascii_uppercase)})

filename = 'input_3.txt'

C1s = []; C2s = []
intersection = []
with open(filename) as fp:
    lines = fp.readlines()
for line in lines:
    if line[-1:] == '\n':
        line =line[:-1]; 
    line = [_letters_to_num_[letter] for letter in line] 
    c1 = line[:len(line)//2]; c2 = line[len(line)//2:]
    C1s.append(c1); C2s.append(c2)
    intersection.append(list(set(c1).intersection(set(c2))))
intersection = np.array(intersection).ravel()
print('Part 1: {}'.format(intersection.sum()))


filename = 'input_3.txt'

C1s = []; C2s = []
intersection = []
with open(filename) as fp:
    lines = fp.readlines()
lines = np.array(lines)
Nlines = len(lines)
common_items = []
for i in range(Nlines//3):
    group = []
    for line in lines[3*i:(i+1)*3]:
        if line[-1:] == '\n':
            line =line[:-1]; 
        line = [_letters_to_num_[letter] for letter in line] 
        group.append(line)
    common_item = list(set(group[0]).intersection(set(group[1])).intersection(set(group[2])))
    common_items.append(common_item)
common_items = np.array(common_items).ravel()
print('Part 2: {}'.format(common_items.sum()))
