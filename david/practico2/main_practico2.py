import random
from kruskal.kruskal_algorithm import Kruskal
from prim.prim import Prim

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
    ('e', 'f', 8)
]

kruskal = Kruskal()
prim = Prim()

node = random.choice(nodes)
met = kruskal.apply_kruskal(nodes, edges)
mst = prim.apply_prim(nodes, edges, node)

print(met)
print(node)
#print(prim.sort_edges(mst))
print(mst)