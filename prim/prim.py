class Prim:

    def __init__(self):
        self.mst = []
        self.nodes = {}
        self.levels = {}
        self._available_edges = []
    
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

    def update_available_edges(self, node, edges):
        for edge in edges: 
            if edge not in self._available_edges and edge not in self.mst:
                if edge[0] == node or edge[1] == node:
                    self._available_edges.append(edge)
        self._available_edges = self.sort_edges(self._available_edges)

    def apply_prim(self, nodes, edges, actual_node):
        for node in nodes:
            self.init_nl(node) 
        self.update_available_edges(actual_node, edges)
        limit = len(nodes) - 1
        i = 0
        while len(self.mst) < limit:
            origin, destination, weight = self._available_edges[i]
            origin_root = self.find_root(origin)
            destination_root = self.find_root(destination)
            if origin_root != destination_root:
                self.make_union(origin_root, destination_root)
                self.mst.append(self._available_edges[i])
                self._available_edges.pop(i)
                self.update_available_edges(origin, edges)
                self.update_available_edges(destination, edges)
                i = 0
            else: 
                i += 1
        return self.mst

