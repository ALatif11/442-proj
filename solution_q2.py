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
    ml, cl, mr, cr, boat = state
    return (boat in ("L", "R") and all(n >= 0 for n in state[:4])
            and (ml == 0 or ml >= cl) and (mr == 0 or mr >= cr))


def successors(state):
    ml, cl, mr, cr, boat = state
    for missionaries, cannibals in MOVES:
        if boat == "L":
            if ml < missionaries or cl < cannibals:
                continue
            next_state = (ml - missionaries, cl - cannibals,
                          mr + missionaries, cr + cannibals, "R")
        else:
            if mr < missionaries or cr < cannibals:
                continue
            next_state = (ml + missionaries, cl + cannibals,
                          mr - missionaries, cr - cannibals, "L")
        if valid(next_state):
            yield next_state, missionaries, cannibals


def move_cost(state, missionaries_on_boat, cannibals_on_boat, model):
    if model == "A":
        return 2 * missionaries_on_boat + cannibals_on_boat
    if model == "B":
        return 2 if state[4] == "L" else 1
    raise ValueError("Choose cost model A or B")


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


def display_result(model, path, cost, expansions):
    print("The solution of Q2.1 (UCS, cost model " + model + ") is:")
    print("Solution Path: " + (" -> ".join(
        "(" + ", ".join(map(str, state)) + ")" for state in path)
                               if path else "No solution"))
    print("Total cost = " + (str(cost) if cost is not None else "N/A"))
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
