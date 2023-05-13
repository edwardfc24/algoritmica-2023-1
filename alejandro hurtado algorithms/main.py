from algorithms import Algorithms

kruskal = Algorithms()
prim = Algorithms()

nodes = ['a','b','c','d','e','f','g']
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
    ('e', 'f', 8)
]

mst_k = kruskal.kruskal(nodes, edges)
print(mst_k)

mst_p = prim.prim(nodes, edges)
print(mst_p)


