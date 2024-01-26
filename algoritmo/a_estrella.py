from __future__ import annotations
from typing import List
from algoritmo.tads import *

class A_estrella ():
    def __init__(self, grafo: Grafo, origen: str, destino: str) -> None:
        self.grafo = grafo
        self.origen = self.grafo.encontrar_nodo(origen) 
        self.destino = self.grafo.encontrar_nodo(destino)
        self.nodos_abiertos: List = [] #Lista de nodos a explorar en la iteración
        self.nodos_cerrados: List = [] #Lista de nodos ya explorados
        # Si no se tiene origen o destino en el árbol de nodos se devuelve una excepción
        if self.origen is None:
            raise ValueError("{} no es un nodo del grafo".format(origen))
        if self.destino is None:
            raise ValueError("{} no es un nodo del grafo".format(destino))
    
    def distancia_manhattan(self, nodo1: Nodo, nodo2: Nodo) -> float:
        return abs(nodo1.x - nodo2.x) + abs(nodo1.y - nodo2.y)

    def distancia(self, nodo_padre: Nodo, nodo_hijo: Nodo) -> float:
        for adyacente in self.grafo.encontrar_nodo(nodo_padre.etiqueta).mostrar_hijos():
            if adyacente.etiqueta == nodo_hijo.etiqueta:
                distancia: float = nodo_padre.distancia_origen + adyacente.distancia_origen
                if distancia < nodo_hijo.distancia_origen:
                    nodo_hijo.nodo_padre = nodo_padre
                    return distancia
                return nodo_hijo.distancia_origen

    def calcular_valor_heuristico(self, nodo_padre: Nodo, nodo_hijo: Nodo, etiqueta: str) -> float:
        return self.distancia(nodo_padre, nodo_hijo) + self.distancia_manhattan(nodo_hijo, etiqueta)

    def añadir_lista(self, nodo: Nodo, lista: str) -> None:
        if lista == "abierta":
            self.nodos_abiertos.append(nodo)
        else:
            self.nodos_cerrados.append(nodo)

    def eliminar_lista_nodos_abiertos(self) -> None:
        self.nodos_abiertos.sort()
        nodo: Nodo = self.nodos_abiertos.pop(0)
        self.nodos_cerrados.append(nodo)
        return nodo
    
    def nodos_abiertos_vacia(self) -> bool:
        return len(self.nodos_abiertos) == 0

    def nodo_misma_etiqueta(self, etiqueta: str) -> Nodo:
        for nodo in self.nodos_abiertos:
            if nodo.etiqueta == etiqueta:
                return nodo
        return None

    def calcular_ruta(self, nodo_destino: Nodo) -> List[str]:
        ruta: List[str] = [nodo_destino.etiqueta]
        nodo: Nodo = nodo_destino.nodo_padre
        while nodo.nodo_padre is not None:
            ruta.append(nodo.etiqueta)
            nodo = nodo.nodo_padre
        ruta.append(nodo.etiqueta)
        return ruta

    def busqueda(self) -> List[str]:
        self.origen.distancia_origen = 0
        self.origen.valor_heuristico = self.distancia_manhattan(self.origen, self.destino)
        self.nodos_abiertos.append(self.origen)

        while not self.nodos_abiertos_vacia():
            nodo_elegido: Nodo = self.eliminar_lista_nodos_abiertos()
            self.añadir_lista(nodo_elegido,"cerrado")  # se marca el nodo como ya visitado
            if nodo_elegido == self.destino:
                ruta: List[str] = self.calcular_ruta(nodo_elegido)
                ruta.reverse()
                return ruta

            # se obtienen los hijos usando los métodos de la clase grafo
            nuevos_nodos: List[Nodo] =self.grafo.encontrar_nodo(nodo_elegido.etiqueta).mostrar_hijos()
            if len(nuevos_nodos) > 0:
                for nuevo_nodo in nuevos_nodos:
                    nuevo_nodo.nodo_padre = nodo_elegido
                    if nuevo_nodo not in self.nodos_cerrados and nuevo_nodo not in self.nodos_abiertos:
                        nuevo_nodo.valor_heuristico = self.calcular_valor_heuristico(nodo_elegido, nuevo_nodo, self.destino)
                        self.añadir_lista(nuevo_nodo, "abierta")