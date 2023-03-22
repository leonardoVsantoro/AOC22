import os
import numpy as np

# A,X : rock
# B,Y : paper
# C,Z : scizzords 
choicescore = {'X':1,'Y':2,'Z':3}
XYZ_to_ABC = {'X':'A','Y':'B','Z':'C'}


def didwin(ABC, XYZ):
    win = None
    if ABC == 'A':
        if XYZ == 'Y':
            win = True
        if XYZ == 'Z':
            win = False
    
    if ABC == 'B':
        if XYZ == 'X':
            win = False
        if XYZ == 'Z':
            win = True 
        
    if ABC == 'C':
        if XYZ == 'X':
            win = True
        if XYZ == 'Y':
            win = False 
    return win
    
    
def getscore(ABC,XYZ):
    win = didwin(ABC, XYZ)
    if ABC == XYZ_to_ABC[XYZ]:
        score = choicescore[XYZ]+3
    if win is False:
        score = choicescore[XYZ]
    if win is True:
        score = choicescore[XYZ]+6
    return score

filename = 'input_2.txt'

data = []

with open(filename) as fp:
    lines = fp.readlines()
opponent = []; you = []
for line in lines:
        opponent.append(line[0])
        you.append(line[2])
opponent = np.array(opponent)
you = np.array(you)

scores = []
for ABC,XYZ in zip(opponent,you):
    scores.append(getscore(ABC,XYZ))
totscore = np.array(scores).sum()
print('Part 1: {}'.format(totscore))


XYZ_to_ABC = {'X':'A','Y':'B','Z':'C'}
ABC_to_XYZ = {'A':'X','B':'Y','C':'Z'}
playtowin = {'A': 'Y', 'B': 'Z', 'C' : 'X' }
playtolose = {'A': 'Z', 'B': 'X', 'C' : 'Y' }

def get_whatyouplay(ABC,XYZ):
    if XYZ == 'X': # need to lose
        whatyouplay = playtolose[ABC]
    if XYZ == 'Z': # need to win
        whatyouplay = playtowin[ABC]
    if XYZ == 'Y': # need to draw
        whatyouplay = ABC_to_XYZ[ABC]
    return whatyouplay


data = []

with open(filename) as fp:
    lines = fp.readlines()
opponent = []; order = []
for line in lines:
        opponent.append(line[0])
        order.append(line[2])
opponent = np.array(opponent)
order = np.array(order)

you = []
for ABC,XYZ in zip(opponent,order):
    you.append(get_whatyouplay(ABC,XYZ))
you = np.array(you)

scores = []
for ABC,XYZ in zip(opponent,you):
    scores.append(getscore(ABC,XYZ))
totscore2 = np.array(scores).sum()
print('Part 2: {}'.format(totscore2))
