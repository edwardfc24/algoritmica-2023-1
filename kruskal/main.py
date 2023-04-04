from kruskal import Kruskal

nodes = ['a','b','c','d','e','f', 'g']
edges = [
    ('a', 'b', 7),
    ('b', 'c', 8),
    ('c', 'e', 5),
    ('e', 'g', 9),
    ('g', 'f', 11),
    ('d', 'f', 6),
    ('a', 'd', 5),
    ('d', 'b', 9),
    ('d', 'e', 15),
    ('b', 'e', 7),
    ('e', 'f', 4)
]
graph = {
        'A': {'B': 2, 'C': 3},
        'B': {'A': 2, 'C': 5, 'D': 1},
        'C': {'A': 3, 'B': 5, 'D': 4, 'E': 6},
        'D': {'B': 1, 'C': 4, 'E': 2},
        'E': {'C': 6, 'D': 2}
    }
def prim(graph, start):
        visited = set()
        mst = []
        # heap es una cola de prioridad
        heap = [(0, start, None)]
        while heap:
            # se agarra el elemento de menor peso
            weight, node, parent = heapq.heappop(heap)
            if node not in visited:
                visited.add(node)
                if parent is not None:
                    mst.append((parent, node, weight))
                # identificador de los vecinos
                # weight es el peso de la arista que une a node con su vecino
                for neighbor, weight in graph[node].items():#devuelve el key y el value
                    heapq.heappush(heap, (weight, neighbor, node))
        return mst

if __name__ == '__main__':
    kruskal = Kruskal()
    met = kruskal.apply_kruskal(nodes, edges)
    print(met)

