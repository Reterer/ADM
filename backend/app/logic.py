import random


def generate_graph(node_count: int, edge_count: int):
    graph = [[] for i in range(node_count)]

    for _ in range(edge_count):
        q, v = random.randint(0, node_count - 1), random.randint(0, node_count - 1)
        while q == v or (v in graph[q]):
            q, v = random.randint(0, node_count - 1), random.randint(0, node_count - 1)

        graph[q].append(v)
    print(graph)
    nodes = {str(i): {} for i in range(node_count)}
    edges = []
    for q in range(node_count):
        for v in graph[q]:
            edges.append({"source": str(q), "target": str(v)})
    print(edges)
    edges = {str(i): edges[i] for i in range(len(edges))}
    return nodes, edges
