import numpy as np
from tqdm import tqdm

def get_xy(_string_):
    _string_x, _string_y = _string_.split(', ')
    return  eval(_string_x[2:]) + eval(_string_y[2:])*1j

def manhattan(a, b):
    return abs(a.real-b.real) + abs(a.imag-b.imag) 

def get_intersection_of_manhattan_ball_on_hline(center, radius, yline):
    if yline in np.arange(center.imag - radius, center.imag + radius +1):
        dist = radius - np.abs(center.imag - yline)
        return set( yline*1j + center.real + delta_x  for delta_x in np.arange( - dist, dist+1))  
    else:
        return set()

def get_manhattan_sphere(center, radius):
    s = set( center + (radius - split) + split*1j  for split in range(0, radius+1))
    s  = s.union(set( center - (radius - split) + split*1j  for split in range(0, radius+1)))
    s  = s.union(set( center + (radius - split) - split*1j  for split in range(0, radius+1)))
    s  = s.union(set( center - (radius - split) - split*1j  for split in range(0, radius+1)))
    return  s

data = np.array([_[10:].split(': closest beacon is at ') for _ in open('input_15.txt').read().split("\n")])
sensors  = np.array([get_xy(line) for line in data[:,0]])
beacons  = np.array([get_xy(line) for line in data[:,1]])
distances = np.array([manhattan(s,b) for s,b in zip(sensors,beacons)]).astype(int)

no_beacon_here = set()
yline = 2000000
for center, radius in zip(sensors, distances):
    covered_ = get_intersection_of_manhattan_ball_on_hline(center, radius, yline)
    no_beacon_here = no_beacon_here.union(covered_)
print('Part 1 : {}'.format(len(no_beacon_here)-1))

spheres = []
for center, radius in tqdm( zip(sensors, distances), total = sensors.size):
    s = get_manhattan_sphere(center, radius+1); 
    spheres.append(s)

candidates = set()
for i, c1, s1, r1 in zip(np.arange(len(sensors)), sensors, spheres, distances):
    for c2,s2,r2 in zip(sensors[i+1:], spheres[i+1:], distances[i+1:]):
        if manhattan(c1,c2) == r1+r2+2:
            candidates = candidates.union(s1.intersection(s2))

real_candidates = candidates.copy()
for element in tqdm(candidates):
    for center, radius in zip(sensors,distances):
        if manhattan(element,center) <= radius:
            real_candidates.remove(element)
            break
            
print('Part 2 : {}'.format(list(real_candidates)[0].real *4000000 + list(real_candidates)[0].imag))