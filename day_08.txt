import numpy as np

filename = 'input_8.txt'
with open(filename) as fp:
    lines = fp.readlines()
data = np.array([[int(lines[i][j]) for i in range(99)] for j in range(99)])

def is_visible(data, i,j):
    out = False
    if (data[i,j] > data[i,:j]).all():
        out = True
    
    if (data[i,j] > data[i,j+1:]).all():
        out = True

    if (data[i,j] > data[i+1:,j]).all():
        out = True
    
    if (data[i,j] > data[:i,j]).all():
        out = True

    return out
    

visibility_matrix = np.array([[is_visible(data,i,j) for i in np.arange(99)] for j in np.arange(99)])
visibility_matrix.sum()

print('Part 1: {}'.format(visibility_matrix.sum()))


def L_vis(data,i,j):
    ix = 0
    if j!=99:
        for ix in np.arange(1,j+1):
            if data[i,j] <= data[i,j-ix]:
                break
    return ix

def R_vis(data,i,j):
    ix = 0
    if j!=0:
        for ix in np.arange(1,99-j):
            if data[i,j] <= data[i,j+ix]:
                break
    return ix

def U_vis(data,i,j):
    ix = 0
    if j!=0:
        for ix in np.arange(1,i+1):
            if data[i,j] <= data[i-ix,j]:
                break
    return ix

def D_vis(data,i,j):
    ix = 0
    if i!=99:
        for ix in np.arange(1,99-i):
            if data[i,j] <= data[i+ix,j]:
                break
    return ix

def viewing_distance(data,i,j):
    return D_vis(data,i,j)*U_vis(data,i,j)*L_vis(data,i,j)*R_vis(data,i,j)

dist_visibility_matrix = np.array([[viewing_distance(data,i,j) for i in np.arange(99)]
                                          for j in (np.arange(99))])


print('Part 2: {}'.format(dist_visibility_matrix.max()))
