class Kruskal:
    def __init__(self):
        self.met = []
        self.nodos = {}
        self.niveles = {}
        self.poscionPeso = 2

    
    def ordenarConexiones(self, conexiones):
        return sorted(conexiones, key=lambda nodo: nodo[self.poscionPeso])
    
    def inicializarDatos(self, nodo):
        self.nodos[nodo] = nodo
        self.niveles[nodo] = 0

    def encontrarRaiz(self, nodo):
        if self.nodos[nodo] != nodo:
            self.nodos[nodo] = self.encontrarRaiz(self.nodos[nodo])
        return self.nodos[nodo]
    
    def verificarUnion(self, origen, destino):
        origenRaiz = self.encontrarRaiz(origen)
        destinoRaiz = self.encontrarRaiz(destino)
        if origenRaiz != destinoRaiz:
            if self.niveles[origenRaiz] > self.niveles[origenRaiz]:
                self.nodos[destinoRaiz] = origenRaiz
            else:
                self.nodos[origenRaiz] = destinoRaiz
                if self.niveles[origenRaiz] == self.niveles[destinoRaiz]:
                    self.niveles[destinoRaiz] += 1


    def apply_kruskal(self, nodos, conexiones):
        for node in nodos:
            self.inicializarDatos(node)
        conexionesOrdenadas = self.ordenarConexiones(conexiones)
        limiteConexiones = len(nodos) - 1
        conexionesHechas = 0
        posicion = 0
        while (limiteConexiones > conexionesHechas):
            conexion =  conexionesOrdenadas[posicion]
            origen, destino, peso = conexion
            if self.encontrarRaiz(origen) != self.encontrarRaiz(destino):
                self.verificarUnion(origen, destino)
                self.met.append(conexion)
                conexionesHechas = conexionesHechas + 1
            posicion = posicion+1
        return self.met


        
    