from graph import Graph


class Kruskal:

    def __init__(self):
        self.graph = Graph()

    def apply_kruskal(self, nodes, edges):
        # Preparamos la informacion
        for node in nodes:
            self.graph.initialize_data(node)
        # Ordeno el grafo
        sorted_edges = self.graph.sort_graph(edges)
        for edge in sorted_edges:
            # Obtenemos los valores del nodo para hacer el analisis del grafo
            origin, destination, weight = edge
            if self.graph.find_set_root(origin) != self.graph.find_set_root(destination):
                self.graph.check_union(origin, destination)
                self.graph.met.append(edge)
        return self.graph.met
