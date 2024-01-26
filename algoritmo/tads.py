from __future__ import annotations
from typing import List, Tuple
import math

class Nodo():
    def __init__(self, etiqueta: str, coordenadas: Tuple, adyacentes: List[Tuple[Nodo,int]] = None ) -> None:
        self.etiqueta: str = etiqueta
        self.x: float = coordenadas[0]
        self.y: float = coordenadas[1]
        self.valor_heuristico: float = -1
        self.distancia_origen: float = math.inf
        if adyacentes is None:
            self.adyacentes: List[Tuple[Nodo,int]] = []
        else:
            self.adyacentes = adyacentes
        self.nodo_padre = None

    def añadir_adyactente(self, adyacente: Tuple[Nodo, int]) -> None:
        self.adyacentes.append(adyacente)

    def mostrar_hijos(self) -> List[Nodo]:
        hijos: List[Nodo] = []
        for hijo in self.adyacentes:
            hijos.append(hijo[0]) 
        return hijos
    
    def __gt__(self, nodo: Nodo) -> bool:
        if isinstance(nodo, Nodo):
            if self.valor_heuristico > nodo.valor_heuristico:
                return True
            if self.valor_heuristico < nodo.valor_heuristico:
                return False
            return self.etiqueta > nodo.etiqueta

    def __eq__(self, nodo: Nodo) -> bool:
        if isinstance(nodo, Nodo):
            return self.etiqueta == nodo.etiqueta
        return self.etiqueta == nodo.etiqueta

class Grafo():
    def __init__(self, nodos: List[Nodo] = None) -> None:
        if nodos is None:
            self.nodos: List[Nodo] = []
        else:
            self.nodos = nodos

    def añadir_nodo(self, nodo: Nodo) -> None:
        self.nodos.append(nodo)

    def encontrar_nodo(self, etiqueta: str) -> Nodo:
        nodo_encontrado: Nodo = None
        for nodo in self.nodos:
            if nodo.etiqueta == etiqueta:
                nodo_encontrado = nodo
        return nodo_encontrado

    def añadir_arista(self, etiqueta1: str, etiqueta2: str, peso: int = 1) -> None:
        nodo1: Nodo = self.encontrar_nodo(etiqueta1)
        nodo2: Nodo = self.encontrar_nodo(etiqueta2)

        if nodo1 is not None and nodo2 is not None:
            nodo1.añadir_adyactente((nodo2, peso))
            nodo2.añadir_adyactente((nodo1, peso))

    def estan_conectados(self, etiqueta1: str, etiqueta2: str) -> bool:
        nodo1: Nodo = self.encontrar_nodo(etiqueta1)
        nodo2: Nodo = self.encontrar_nodo(etiqueta2)

        conectados: bool = False
        for adyacente in nodo1.adyacentes:
            if adyacente[0].etiqueta == nodo2.etiqueta:
                conectados = True
        return conectados
