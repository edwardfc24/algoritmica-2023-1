import random

class Algorithms:

    def __init__(self):
        self.mst = []
        self.nodes = {}
        self.level = {}
        self._origin = 0
        self._destination = 1
        self._weight = 2

    def sort_edges(self, edges):
        return sorted(edges, key=lambda node: node[self._weight])

    def initialize_data(self, node):
        self.nodes[node] = node
        self.level[node] = 0

    def find_set_root(self, node):
        if node not in self.nodes:
            raise NameError('El nodo que busca no se encuentra en la lista')
        if self.nodes[node] != node:
            self.nodes[node] = self.find_set_root(self.nodes[node])
        return self.nodes[node]

    def check_union(self, origin, destination):
        origin_found = self.find_set_root(origin)
        destination_found = self.find_set_root(destination)
        if self.level[origin_found] > self.level[destination_found]:
            self.nodes[destination_found] = origin_found
        elif self.level[origin_found] < self.level[destination_found]:
            self.nodes[origin_found] = destination_found
        else:
            self.nodes[destination_found] = origin_found
            self.level[destination_found] += 1

    def edges_availables(self, sorted_edges, nodes):
        edges_availables = []
        for edge in sorted_edges:
            if edge[self._origin] in nodes or edge[self._destination] in nodes:
                edges_availables.append(edge)
        edges_availables = self.sort_edges(edges_availables)
        for edge in self.mst:
            if edge in edges_availables:
                edges_availables.remove(edge)
        return edges_availables

    def kruskal(self, nodes, edges):
        for node in nodes:
            self.initialize_data(node)
        sorted_edges = self.sort_edges(edges)
        iteration = 0
        while iteration < len(sorted_edges):
            edge = sorted_edges[iteration]
            origin, destination, weight = edge
            origin = self.find_set_root(origin)
            destination = self.find_set_root(destination)
            if origin != destination:
                self.check_union(origin, destination)
                self.mst.append(edge)
            else:
                iteration += 1
        return self.mst

    def prim(self, nodes, edges):
        for node in nodes:
            self.initialize_data(node)
        sorted_edges = self.sort_edges(edges)
        added_nodes = []
        first_random_node = random.choice(nodes)
        print(first_random_node)
        added_nodes.append(first_random_node)
        iteration = 0
        while len(added_nodes) < len(self.nodes):
            edges_availables = self.edges_availables(sorted_edges,added_nodes)
            origin, destination, weight = edges_availables[iteration]
            if self.find_set_root(origin) != self.find_set_root(destination):
                self.check_union(origin, destination)
                self.mst.append(edges_availables[iteration])
                if origin not in added_nodes:
                    added_nodes.append(origin)
                if destination not in added_nodes:
                    added_nodes.append(destination)
            else:
                iteration += 1
        return self.mst