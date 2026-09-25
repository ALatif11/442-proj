import heapq
from itertools import count
from solution_q2 import read_initial_state, successors, move_cost


def heuristic(state, number):
    m_left, c_left, _, _, boat = state
    remaining_weight = 2 * m_left + c_left
    if number == 1:
        return remaining_weight
    if number == 2:
        return (remaining_weight + 2) // 3  
    if number == 3:
        remaining_people = m_left + c_left
        if remaining_people == 0:
            return 0
        minimum_returns = (max(0, remaining_people - 2) if boat == "L"
                           else remaining_people)
        return remaining_weight + 2 * minimum_returns
    raise ValueError("Heuristic has to be 1, 2, or 3")


def reconstruct(parents, state):
    path = []
    while state is not None:
        path.append(state)
        state = parents[state]
    return path[::-1]


def astar(start, number):
    total_m, total_c = start[0] + start[2], start[1] + start[3]
    goal = (0, 0, total_m, total_c, "R")
    sequence = count()
    frontier = [(heuristic(start, number), next(sequence), 0, start)]
    best_cost = {start: 0}
    parents = {start: None}
    expansions = 0

    while frontier:
        _, _, cost, state = heapq.heappop(frontier)
        if cost != best_cost[state]:
            continue
        if state == goal:
            return reconstruct(parents, state), cost, expansions
        expansions += 1
        for next_state, missionaries, cannibals in successors(state):
            new_cost = cost + move_cost(state, missionaries, cannibals, "A")
            if new_cost < best_cost.get(next_state, float("inf")):
                best_cost[next_state] = new_cost
                parents[next_state] = state
                priority = new_cost + heuristic(next_state, number)
                heapq.heappush(frontier, (priority, next(sequence), new_cost, next_state))
    return None, None, expansions


def display_result(number, path, cost, expansions):
    print("The solution of Q3.1 (Heuristic " + str(number) + ") is:")
    print("Solution Path: " + (" -> ".join(
        "(" + ", ".join(map(str, state)) + ")" for state in path)
                               if path else "No solution"))
    print("Total cost = " + (str(cost) if cost is not None else "N/A"))
    print("Number of node expansions = " + str(expansions))


if __name__ == "__main__":
    initial = read_initial_state()
    for number in (1, 2, 3):
        display_result(number, *astar(initial, number))
        if number != 3:
            print()
