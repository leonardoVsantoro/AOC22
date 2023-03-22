data = np.array(open('input_24.txt').read().split('\n'))
# data = np.array(open('test_24.txt').read().split('\n'))

mx = 0; Mx = len(data[0]) - 1
my = 0; My = len(data) - 1 

blz_symbs = ['>','<','v','^']

snowflakes_locs = []
snowflakes_symbs = []
for j,row in enumerate(data):
    for i, symb in enumerate(row):
        if j == 0 and symb == '.':
            start = i + ( My-j)*1j
        if j == len(data)-1 and symb == '.':
            end = i + ( My-j)*1j
        if symb in blz_symbs:
            snowflakes_locs.append(i +( My-j)*1j)
            snowflakes_symbs.append(symb)

            
init_snowflakes_locs = snowflakes_locs.copy()

dict_move = {'>' : 1 ,'<' : -1,'v' : -1j,'^':1j}

teleport = {'>' : mx+1, '<' : Mx -1 ,'v' :(My -1)*1j ,'^' : (my+1)*1j}

def invariant(loc):
    return {'>' : loc.imag*1j, '<' : loc.imag*1j ,'v' : loc.real ,'^' : loc.real}

def is_in_grid(loc):
    if loc == start or loc ==end:
        return True
    else:
        return all([loc.real> mx, loc.real< Mx, loc.imag> my, loc.imag< My])

def move(loc, symb):
    new_loc = loc + dict_move[symb]
    if is_in_grid(new_loc):
        return new_loc
    else:
        return invariant(loc)[symb] + teleport[symb] 

def manhattan(a, b):
    return abs(a.real-b.real) + abs(a.imag-b.imag) 

deltas = [1,-1,1j,-1j,0]
def possible_next_steps(loc, occupied):
    psb =  []
    for delta in deltas:
        if is_in_grid(loc + delta) and (loc + delta not in occupied):
            psb.append(loc + delta)
    return psb
    

paths = [[start]]

snowflakes_locs = init_snowflakes_locs.copy()
should_break = False


while len(paths)>0:
    snowflakes_locs = [move(loc, symb) for loc, symb in zip(snowflakes_locs, snowflakes_symbs)]
    occupied = set(snowflakes_locs)
    
    next_paths = []
    visited = set()
    for path in paths:
        for choice in possible_next_steps(path[-1], occupied):
            if choice not in visited:
                visited.add(choice)
                next_paths.append(path + [choice])
                if choice == end:
                    should_break = True; len_path = len(path); finalpath = path
                    break
    paths = next_paths.copy()

    if should_break:
        break


print('Part 1: {}'.format(len_path))

    

__start = start
__end = end

snowflakes_locs = init_snowflakes_locs.copy()


tot_steps = 0

for start_,end_ in  zip([__start, __end, __start], [__end,__start,__end]):

    paths = [[start_]]
    should_break = False

    MAXITER = 1000; counter = 0
    while len(paths)>0:
        snowflakes_locs = [move(loc, symb) for loc, symb in zip(snowflakes_locs, snowflakes_symbs)]
        occupied = set(snowflakes_locs)

        next_paths = []
        visited = set()
        for path in paths:
            for choice in possible_next_steps(path[-1], occupied):
                if choice not in visited:
                    visited.add(choice)
                    next_paths.append(path + [choice])
                    if choice == end_:
                        should_break = True; len_path = len(path); finalpath = path
                        break
        paths = next_paths.copy()



        if should_break:
            tot_steps += len_path
            break


print('Part 2: {}'.format(tot_steps))
