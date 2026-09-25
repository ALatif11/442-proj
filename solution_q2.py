import heapq
import sys
from itertools import count


MOVES = ((1, 0), (0, 1), (2, 0), (0, 2), (1, 1))


def read_initial_state(filename="input.txt"):
    with open(filename, encoding="utf-8") as input_file:
        parts = [part.strip() for part in input_file.read().strip().split(",")]
    if len(parts) != 5 or parts[4].upper() not in ("L", "R"):
        raise ValueError("Expected M_left,C_left,M_right,C_right,L_or_R")
    state = tuple(int(part) for part in parts[:4]) + (parts[4].upper(),)
    if not valid(state):
        raise ValueError("Initial state violates the puzzle rules")
    return state


def valid(state):
    m_left, c_left, m_right, c_right = state[:4]
    return (all(n >= 0 for n in state[:4])
            and (m_left == 0 or m_left >= c_left) and (m_right == 0 or m_right >= c_right))


def successors(state):
    m_left, c_left, m_right, c_right, boat = state
    for missionaries, cannibals in MOVES:
        if boat == "L":
            next_state = (m_left - missionaries, c_left - cannibals,
                          m_right + missionaries, c_right + cannibals, "R")
        else:
            next_state = (m_left + missionaries, c_left + cannibals,
                          m_right - missionaries, c_right - cannibals, "L")
        if valid(next_state):
            yield next_state, missionaries, cannibals


def move_cost(state, missionaries_on_boat, cannibals_on_boat, model):
    if model == "A":
        return 2 * missionaries_on_boat + cannibals_on_boat
    return 2 if state[4] == "L" else 1


def reconstruct(parents, state):
    path = []
    while state is not None:
        path.append(state)
        state = parents[state]
    return path[::-1]


def ucs(start, model):
    total_m, total_c = start[0] + start[2], start[1] + start[3]
    goal = (0, 0, total_m, total_c, "R")
    sequence = count()
    frontier = [(0, next(sequence), start)]
    best_cost = {start: 0}
    parents = {start: None}
    expansions = 0

    while frontier:
        cost, _, state = heapq.heappop(frontier)
        # Skip an old queue entry if a cheaper path to this state was found
        if cost != best_cost[state]:
            continue
        if state == goal:
            return reconstruct(parents, state), cost, expansions
        expansions += 1
        for next_state, missionaries, cannibals in successors(state):
            new_cost = cost + move_cost(state, missionaries, cannibals, model)
            if new_cost < best_cost.get(next_state, float("inf")):
                best_cost[next_state] = new_cost
                parents[next_state] = state
                heapq.heappush(frontier, (new_cost, next(sequence), next_state))
    return None, None, expansions


def display_state(state):
    return "(" + ", ".join(map(str, state)) + ")"


def display_result(model, path, cost, expansions):
    print("The solution of Q2.1 (UCS, cost model " + model + ") is:")
    if path:
        print("Solution Path: " + " -> ".join(map(display_state, path)))
        print("Total cost = " + str(cost))
    else:
        print("Solution Path: No solution")
        print("Total cost = N/A")
    print("Number of node expansions = " + str(expansions))


if __name__ == "__main__":
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1].upper() not in ("A", "B")):
        raise ValueError("Run with python solution_q2.py [A or B]")
    initial = read_initial_state()
    models = (sys.argv[1].upper(),) if len(sys.argv) == 2 else ("A", "B")
    for model in models:
        display_result(model, *ucs(initial, model))
        if model != models[-1]:
            print()