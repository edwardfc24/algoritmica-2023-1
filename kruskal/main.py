from kruskal import Kruskal

nodes = ['a','b','c','d','e']
edges = [
    ('a', 'b', 4),
    ('b', 'e', 5),
    ('a', 'd', 3),
    ('d', 'c', 1),
    ('c', 'b', 2)
]


if __name__ == '__main__':
    kruskal = Kruskal()
    met = kruskal.apply_prim(nodes, edges)
    print(met)

