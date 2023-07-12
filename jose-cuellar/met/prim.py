from graph import Graph


class Prim:

    def __init__(self):
        self.graph = Graph()
        self.edges_available = []

    def apply_prim(self, nodes, edges):
        # Preparamos la informacion
        for node in nodes:
            self.graph.initialize_data(node)
        # Agregamos las aristas del primer nodo
        self.add_node_edges(nodes[0], edges)
        while len(self.graph.met) < len(nodes) - 1:
            minimum_edge = self.get_minimum_edge(
                self.edges_available)
            # Obtenemos los valores del nodo para hacer el analisis del grafo
            origin, destination, weight = minimum_edge
            # Verificamos que el nodo no este en la lista de visitados
            if self.graph.find_set_root(origin) != self.graph.find_set_root(destination):
                self.graph.check_union(origin, destination)
                self.graph.met.append(minimum_edge)
                self.edges_available.remove(minimum_edge)
                self.add_node_edges(destination, edges)
            else:
                self.edges_available.remove(minimum_edge)
        return self.graph.met

    def get_minimum_edge(self, edges):
        return min(edges, key=self.graph.get_weight)

    def add_node_edges(self, node, edges):
        for edge in edges:
            origin, destination, weight = edge
            # Se obtienen las aristas que estan conectadas al nodo
            if origin == node or destination == node:
                # Se verifica que la arista no este en la lista de aristas disponibles
                if edge not in self.graph.met:
                    self.edges_available.append(edge)
