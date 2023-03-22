filename = 'input_11.txt'
with open(filename) as fp:
    lines = fp.readlines()    
lines = [line[:-1] if line[-1:] == '\n' else line for line in lines]


starting_items = {i : [int(s) for s in lines[1 + i*7][18:].split(',') ] for i in range(8) }
operations = {i : lines[2 + i*7][19:] for i in range(8)}
test_div = {i : int(lines[3 + i*7][21:]) for i in range(8)}
if_true = {i : int(lines[4 + i*7][-1]) for i in range(8)}
if_false = {i : int(lines[5 + i*7][-1]) for i in range(8)}


op = lambda operation , old: eval(f"({operation})")

counts = np.zeros(8)
for _ in range(20):
    for i in np.arange(8):
        start_ = starting_items[i]  
        starting_items.update({i:[]})
        for old_ in start_:
            counts[i] += 1
            new_ = op(operations[i], old_)//3
            toix = if_true[i] if new_ % test_div[i] == 0 else if_false[i]
            starting_items[toix].append(new_)
                        

print('Part 1: {}'.format(np.sort(counts)[-1]*np.sort(counts)[-2]))

filename = 'input_11.txt'
with open(filename) as fp:
    lines = fp.readlines()    
lines = [line[:-1] if line[-1:] == '\n' else line for line in lines]


starting_items = {i : [int(s) for s in lines[1 + i*7][18:].split(',') ] for i in range(8) }
operations = {i : lines[2 + i*7][19:] for i in range(8)}
test_div = {i : int(lines[3 + i*7][21:]) for i in range(8)}
if_true = {i : int(lines[4 + i*7][-1]) for i in range(8)}
if_false = {i : int(lines[5 + i*7][-1]) for i in range(8)}


op = lambda operation , old: eval(f"({operation})")

BigNumHandler = np.prod(list(test_div.values()))

counts = np.zeros(8)
for _ in np.arange(10000):
    for i in np.arange(8):
        start_ = starting_items[i]  
        starting_items.update({i:[]})
        for old_ in start_:
            counts[i] += 1
            new_ = op(operations[i], old_)% BigNumHandler
            toix = if_true[i] if new_ % test_div[i] == 0 else if_false[i]
            starting_items[toix].append(new_)
                        

print('Part 1: {}'.format(np.sort(counts)[-1]*np.sort(counts)[-2]))
