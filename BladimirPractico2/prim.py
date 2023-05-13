import random
import copy
class Prim:
    def __init__(self):
        self.arbolExpancionMinima  = []
        self.conexionesDisponibles  = []
        self.posicionPeso = 2
        self.conexionesGenerales =[] 
        self.nodosVisitados = []

    
    def ordenarConexiones(self, conexiones):
        return sorted(conexiones, key=lambda node: node[self.posicionPeso])

    def adicionarNodosVisitados(self,nodoA, nodoB):
        if nodoA not in self.nodosVisitados:
            self.nodosVisitados.append(nodoA)
        if nodoB not in self.nodosVisitados:
            self.nodosVisitados.append(nodoB)

    def buscarConexionesDisponibles(self):
        for conexion in self.conexionesGenerales:
            if (conexion[0] in self.nodosVisitados) or (conexion[1] in self.nodosVisitados):
                self.conexionesDisponibles.append(conexion)

    def aplicarPrim(self, nodos, conexiones):
        limiteConexiones = len(nodos) - 1
        self.conexionesGenerales = copy.copy(conexiones)
        nodoElegido = self.obtenerNodoAleatorio(nodos, (len(nodos)-1))
        conexionMenor = self.obtenerConexionMinima(nodoElegido)
        self.arbolExpancionMinima.append(conexionMenor)
        self.adicionarNodosVisitados(conexionMenor[0],conexionMenor[1])
        self.removerConexion(conexionMenor)
        self.buscarConexionesDisponibles()
        conexionesHechas = 1
        while (limiteConexiones > conexionesHechas):
            self.conexionesDisponibles = self.ordenarConexiones(self.conexionesDisponibles)
            for conexionDisponible in self.conexionesDisponibles:
                if self.generaBucle(conexionDisponible) == False:
                    self.arbolExpancionMinima.append(conexionDisponible)
                    self.adicionarNodosVisitados(conexionDisponible[0], conexionDisponible[1])
                    self.removerConexion(conexionDisponible)
                    self.buscarConexionesDisponibles()
                    conexionesHechas = conexionesHechas +1
                    break
        return self.arbolExpancionMinima
    
    def generaBucle(self, conexion):
        if (conexion[0] in self.nodosVisitados) and (conexion[1] in self.nodosVisitados):
            return True
        else: 
            return False
        
    def removerConexion(self, conexionEliminar):
        for conexion in self.conexionesGenerales:
            if (conexion[0] == conexionEliminar[0]) and (conexion[1] == conexionEliminar[1]) and (conexion[2] == conexionEliminar[2]):
                self.conexionesGenerales.remove(conexion)

    def obtenerNodoAleatorio(self,nodos, cantidadNodos):
        indice = random.randint(0, cantidadNodos)
        return nodos[indice]
    
    def obtenerConexionMinima(self, nodo):
        listaConexionesValidas = []
        for conexion in self.conexionesGenerales:
            if (conexion[0] == nodo) or (conexion[1] == nodo):
                listaConexionesValidas.append(conexion)
        listaConexionesValidas = self.ordenarConexiones(listaConexionesValidas)
        return listaConexionesValidas[0]