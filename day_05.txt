filename = 'input_5.txt'

with open(filename) as fp:
    lines = fp.readlines()
lines = [line[:-1] if line[-1:] == '\n' else line for line in lines]

# part 1
initial = { i+1:[] for i in range(9)}
for line in lines[:8][::-1]:
    for i in range(9):
        if line[1+i*4]!= ' ':
            initial[1+i].append(line[1+i*4])

for line in lines[10:]:
    how_many = int(line[5:-12])
    from_ = int(line[-6])
    to_ = int(line[-1])
    for i in range(how_many):
        which_moves = initial[from_][-1]
        which_stays =initial[from_][:-1]
        initial.update({from_: which_stays})
        initial[to_].append(which_moves)
        
ans = [values[-1][0] for values in initial.values()]
print('Part 1: ' +''.join(i[0].upper() for i in ans))

# part 2 
initial = { i+1:[] for i in range(9)}
for line in lines[:8][::-1]:
    for i in range(9):
        if line[1+i*4]!= ' ':
            initial[1+i].append(line[1+i*4])


for line in lines[10:]:
    how_many = int(line[5:-12])
    from_ = int(line[-6])
    to_ = int(line[-1])
    
    how_to_was = initial[to_]
    how_from_was = initial[from_]
    
    which_move = initial[from_][-how_many:]
    which_stay =initial[from_][:-how_many]
    
    initial.update({from_: which_stay})
    initial.update({to_: how_to_was + which_move})
    
ans = [values[-1][0] for values in initial.values()]

print('Part 2: ' +''.join(i[0].upper() for i in ans))
