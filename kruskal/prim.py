class Prim:
    def __init__(self):
        self.met = []
        self.visited = []
        self._weight = 2

    def get_weight(self, node):
        return node[2]

    def sort_graph(self, graph):
        return sorted(graph, key=lambda node: node[self._weight])
    
    def apply_prim(self, nodes, edges):
        sorted_edges = self.sort_graph(edges)

        first_edge = sorted_edges[0]

        self.visited.append(first_edge[0])
        
        while len(self.visited) < len(nodes):

            min_weight = float('inf')

            min_edge = None

            for node in self.visited:
                neighbors = [tup for tup in edges if any(i in tup for i in self.visited)]
                for node1, node2, weight in neighbors:

                    if node1==node and node2 not in self.visited:
                        if weight < min_weight:
                            min_weight = weight
                            min_edge = (node, node2, min_weight)

                    if node2==node and node1 not in self.visited:
                        if weight < min_weight:
                            min_weight = weight
                            min_edge = (node, node1, min_weight)

            self.met.append(min_edge)

            self.visited.append(min_edge[1])

        return self.met
        