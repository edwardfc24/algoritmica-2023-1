class Graph:

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
