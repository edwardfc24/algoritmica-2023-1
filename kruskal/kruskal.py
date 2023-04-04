class Kruskal:

    def __init__(self):
        self.met = []
        self.nodes = {}
        self.level = {}
        self._origin = 0
        self._destination = 1
        self._weight = 2

    def get_weight(self, node):
        return node[2]

    def sort_graph(self, graph):
        # Estructura del grafo (origen, destino, peso) --> ('A', 'D',  5)
        return sorted(graph, key=lambda node: node[self._weight])
    
    def initialize_data(self, node):
        self.nodes[node] = node
        self.level[node] = 0
        # En el caso de los visitados, almacenamos el nivel y en los nodos los conjuntos

    def find_set_root(self, node):
        # Buscamos el nodo raiz del conjunto, si el valor no es el mismo: buscamos sobre el padre
        if self.nodes[node] != node:
            # Aca el metodo se hace recursivo para llegar hasta el nivel 0
            self.nodes[node] = self.find_set_root(self.nodes[node])
        return self.nodes[node]
    
    def check_union(self, origin, destination):
        # Lo primero que vamos a hacer es encontrar los nodos raiz de ambos nodos
        origin_found = self.find_set_root(origin)
        destination_found = self.find_set_root(destination)
        # Solo seguiremos adelante si los nodos raiz son diferentes
        if origin_found != destination_found:
            if self.level[origin_found] > self.level[origin_found]:
                self.nodes[destination_found] = origin_found
            else:
                self.nodes[origin_found] = destination_found
                if self.level[origin_found] == self.level[destination_found]:
                    self.level[destination_found] += 1


    def apply_kruskal(self, nodes, edges):
        # Preparamos la informacion
        for node in nodes:
            self.initialize_data(node)
        # Ordeno el grafo
        sorted_edges = self.sort_graph(self.sort_graph(edges))
        for edge in sorted_edges:
            # Obtenemos los valores del nodo para hacer el analisis del grafo
            origin, destination, weight = edge
            if self.find_set_root(origin) != self.find_set_root(destination):
                self.check_union(origin, destination)
                self.met.append(edge)
        return self.met
        
    def apply_prim(self, nodes, edges):
        # Inicializar variables
        visited = set()
        met = []
        start_node = nodes[0]
        visited.add(start_node)
        edges_list = []
        for edge in edges:
            if edge[0] == start_node or edge[1] == start_node:
                edges_list.append(edge)
        while edges_list:
            # Arista de menor costo
            edge = min(edges_list, key=lambda x: x[2])
            edges_list.remove(edge)
            if edge[0] in visited and edge[1] in visited:
                continue
            met.append(edge)
            if edge[0] not in visited:
                visited.add(edge[0])
                for ne in edges:
                    if ne[0] == edge[0] or ne[1] == edge[0]:
                        edges_list.append(ne)
            if edge[1] not in visited:
                visited.add(edge[1])
                for ne in edges:
                    if ne[0] == edge[1] or ne[1] == edge[1]:
                        edges_list.append(ne)
        return met