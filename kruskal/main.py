from kruskal import Kruskal
from prim import Prim


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


# nodes = ['a','b','c','d']
# edges = [
#     ('a', 'b', 1),
#     ('a', 'd', 5),
#     ('b', 'd', 5),
#     ('b', 'c', 4),
#     ('c', 'd', 2)
# ]

if __name__ == '__main__':
    # kruskal = Kruskal()
    # met = kruskal.apply_kruskal(nodes, edges)


    prim = Prim()
    met2 = prim.apply_prim(nodes, edges)
    print(met2)

