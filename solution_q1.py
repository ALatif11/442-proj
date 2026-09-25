from collections import deque


MOVES = ((1, 0), (0, 1), (2, 0), (0, 2), (1, 1))


def read_initial_state(filename="input.txt"):
    with open(filename, encoding="utf-8") as input_file:
        parts = [part.strip() for part in input_file.read().strip().split(",")]
    if len(parts) != 5 or parts[4].upper() not in ("L", "R"):
        raise ValueError("Input must look like 3, 3, 0, 0, L")
    state = tuple(int(part) for part in parts[:4]) + (parts[4].upper(),)
    if not valid(state):
        raise ValueError("Initial state violates the puzzle rules")
    return state


def valid(state):
    m_left, c_left, m_right, c_right, boat = state
    return (boat in ("L", "R") and all(n >= 0 for n in state[:4])
            and (m_left == 0 or m_left >= c_left) and (m_right == 0 or m_right >= c_right))


def successors(state):
    m_left, c_left, m_right, c_right, boat = state
    for missionaries, cannibals in MOVES:
        if boat == "L":
            if m_left < missionaries or c_left < cannibals:
                continue
            next_state = (m_left - missionaries, c_left - cannibals,
                          m_right + missionaries, c_right + cannibals, "R")
        else:
            if m_right < missionaries or c_right < cannibals:
                continue
            next_state = (m_left + missionaries, c_left + cannibals,
                          m_right - missionaries, c_right - cannibals, "L")
        if valid(next_state):
            yield next_state


def goal(state, total_m, total_c):
    return state == (0, 0, total_m, total_c, "R")


def reconstruct(parents, state):
    path = []
    while state is not None:
        path.append(state)
        state = parents[state]
    return path[::-1]


def bfs(start):
    total_m, total_c = start[0] + start[2], start[1] + start[3]
    frontier = deque([start])
    parents = {start: None}
    expansions = 0  # Add one each time we explore a state’s possible moves.
    while frontier:
        state = frontier.popleft()
        if goal(state, total_m, total_c):
            return reconstruct(parents, state), expansions
        expansions += 1
        for next_state in successors(state):
            if next_state not in parents:
                parents[next_state] = state
                frontier.append(next_state)
    return None, expansions


def dfs(start):
    total_m, total_c = start[0] + start[2], start[1] + start[3]
    stack = [start]
    parents = {start: None}
    expansions = 0
    while stack:
        state = stack.pop()
        if goal(state, total_m, total_c):
            return reconstruct(parents, state), expansions
        expansions += 1
        for next_state in reversed(tuple(successors(state))):
            if next_state not in parents:
                parents[next_state] = state
                stack.append(next_state)
    return None, expansions


def display_state(state):
    return "(" + ", ".join(map(str, state)) + ")"


def display_result(label, path, expansions):
    print("The solution of " + label + " is:")
    print("Solution Path: " + (" -> ".join(map(display_state, path))
                               if path else "No solution"))
    print("Total cost = " + (str(len(path) - 1) if path else "N/A"))
    print("Number of node expansions = " + str(expansions))


if __name__ == "__main__":
    initial = read_initial_state()
    display_result("Q1.1.a (DFS)", *dfs(initial))
    print()
    display_result("Q1.1.b (BFS)", *bfs(initial))
