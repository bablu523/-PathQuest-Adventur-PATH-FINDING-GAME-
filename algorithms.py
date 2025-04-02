from heapq import heappop, heappush

def a_star(start, end, obstacles, grid_size):
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heappop(open_set)

        if current == end:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, grid_size, obstacles):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heappush(open_set, (f_score[neighbor], neighbor))

    return []

def dijkstra(start, end, obstacles, grid_size):
    # Similar to A*, without heuristic.
    return a_star(start, end, obstacles, grid_size)

def bfs(start, end, obstacles, grid_size):
    from collections import deque
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, grid_size, obstacles):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    return []

def get_neighbors(pos, grid_size, obstacles):
    neighbors = []
    row, col = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        neighbor = (row + dr, col + dc)
        if 0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and neighbor not in obstacles:
            neighbors.append(neighbor)

    return neighbors

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    path = []
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1]
