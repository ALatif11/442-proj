# All legal boatloads: (missionaries, cannibals), 1 to 2 people total
MOVES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]


def read_state(fname="input.txt"):
    with open(fname) as f:
        parts = [p.strip() for p in f.readline().split(",")]
    return (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), parts[4].upper())



#ml = missionaries left, cl = cannibals left, mr = missionaries right, cr = cannibals right, boat = 'L' or 'R'
def is_valid(state):
    ml, cl, mr, cr, _ = state
    if min(ml, cl, mr, cr) < 0:
        return False
    if ml > 0 and cl > ml:   # left bank, number of cannibals cannot exceed number of missionaries
        return False
    if mr > 0 and cr > mr:   # right bank, number of cannibals cannot exceed number of missionaries
        return False
    return True


def is_goal(state):
    return state[0] == 0 and state[1] == 0


def successors(state):
    ml, cl, mr, cr, boat = state
    for m, c in MOVES:
        if boat == 'L':
            nxt = (ml - m, cl - c, mr + m, cr + c, 'R')
        else:
            nxt = (ml + m, cl + c, mr - m, cr - c, 'L')
        if is_valid(nxt):
            yield nxt, (m, c)
            
start = read_state()
for nxt, move in successors(start):
    print(move, nxt)