class Kruskal:

    def __init__(self):
        self.mst = []
        self.nodes = {}
        self.levels = {}
    
    def sort_edges(self, edges):
        return sorted(edges, key= lambda node: node[2])
    
    def init_nl(self, node):
        self.nodes[node] = node
        self.levels[node] = 0
    
    def find_root(self, node):
        if self.nodes[node] != node:
            self.nodes[node] = self.find_root(self.nodes[node])
        return self.nodes[node]
    
    def make_union(self, origin_root, destination_root):
        if self.levels[origin_root] > self.levels[destination_root]:
            self.nodes[destination_root] = origin_root
        else:
            self.nodes[origin_root] = destination_root
            if self.levels[origin_root] == self.levels[destination_root]:
                self.levels[destination_root] += 1

    def apply_kruskal(self, nodes, edges):
        for node in nodes:
            self.init_nl(node)
        orded_edges = self.sort_edges(edges)
        limit = len(nodes) - 1 
        i = 0
        while len(self.mst) != limit:
            origin, destination, weight = orded_edges[i]
            origin_root = self.find_root(origin)
            destination_root = self.find_root(destination)
            if origin_root != destination_root:
                self.make_union(origin_root, destination_root)
                self.mst.append(orded_edges[i])
            i += 1
        return self.mst
