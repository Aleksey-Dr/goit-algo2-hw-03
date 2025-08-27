from collections import deque

def bfs(graph, s, t, parent):
    visited = [False] * len(graph)
    queue = deque()
    queue.append(s)
    visited[s] = True
    parent[s] = -1

    while queue:
        u = queue.popleft()
        for v, capacity in enumerate(graph[u]):
            if not visited[v] and capacity > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return visited[t]

def edmonds_karp(graph, s, t):
    parent = [-1] * len(graph)
    max_flow = 0
    # Make a copy of the graph to represent the residual graph
    residual_graph = [row[:] for row in graph]
    
    while bfs(residual_graph, s, t, parent):
        path_flow = float('Inf')
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, residual_graph[u][v])
            v = u

        max_flow += path_flow
        v = t
        while v != s:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = u
    
    # Calculate the flow on each edge from the original graph and the residual graph
    final_flow = [[0] * len(graph) for _ in range(len(graph))]
    for u in range(len(graph)):
        for v in range(len(graph)):
            if graph[u][v] > 0:
                final_flow[u][v] = graph[u][v] - residual_graph[u][v]

    return max_flow, final_flow

# Вершини:
# 0: S, 1: Термінал 1, 2: Термінал 2
# 3: Склад 1, 4: Склад 2, 5: Склад 3, 6: Склад 4
# 7: Магазин 1, 8: Магазин 2, ..., 20: Магазин 14
# 21: T

num_vertices = 22
graph_capacities = [[0] * num_vertices for _ in range(num_vertices)]

# Додавання ребер та пропускних здатностей
graph_capacities[0][1] = 60
graph_capacities[0][2] = 55

graph_capacities[1][3] = 25
graph_capacities[1][4] = 20
graph_capacities[1][5] = 15

graph_capacities[2][4] = 10
graph_capacities[2][5] = 15
graph_capacities[2][6] = 30

graph_capacities[3][7] = 15
graph_capacities[3][8] = 10
graph_capacities[3][9] = 20

graph_capacities[4][10] = 15
graph_capacities[4][11] = 10
graph_capacities[4][12] = 25

graph_capacities[5][13] = 20
graph_capacities[5][14] = 15
graph_capacities[5][15] = 10

graph_capacities[6][16] = 20
graph_capacities[6][17] = 10
graph_capacities[6][18] = 15
graph_capacities[6][19] = 5
graph_capacities[6][20] = 10

# Ребра від магазинів до стоку
for i in range(7, 21):
    graph_capacities[i][21] = float('Inf')

source = 0
sink = 21

max_flow, final_flow = edmonds_karp(graph_capacities, source, sink)

print(f"Максимальний потік: {max_flow} одиниць")

# Вивід детального розподілу потоків
print("\nДетальний розподіл потоків:")

# Маппинг для удобства вывода
vertex_names = {
    1: 'Термінал 1', 2: 'Термінал 2',
    3: 'Склад 1', 4: 'Склад 2', 5: 'Склад 3', 6: 'Склад 4',
    7: 'Магазин 1', 8: 'Магазин 2', 9: 'Магазин 3', 10: 'Магазин 4',
    11: 'Магазин 5', 12: 'Магазин 6', 13: 'Магазин 7', 14: 'Магазин 8',
    15: 'Магазин 9', 16: 'Магазин 10', 17: 'Магазин 11', 18: 'Магазин 12',
    19: 'Магазин 13', 20: 'Магазин 14'
}

# Створення таблиці
print("-" * 50)
print(f"{'Термінал':<15}{'Магазин':<15}{'Фактичний Потік':<20}")
print("-" * 50)

# Розрахунок потоків від терміналів до магазинів
for terminal_node in [1, 2]:
    for warehouse_node in range(3, 7):
        if final_flow[terminal_node][warehouse_node] > 0:
            for store_node in range(7, 21):
                # We need to consider cases where flow might be zero
                flow = final_flow[warehouse_node][store_node]
                if flow > 0:
                    print(f"{vertex_names[terminal_node]:<15}{vertex_names[store_node]:<15}{flow:<20}")