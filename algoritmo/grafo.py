from algoritmo.distancia_coor import distancia_coor
import pandas as pd
from pandas import *
from algoritmo.tads import *
from algoritmo.a_estrella import *

def genera_grafos_con_nodos(ficheroDatos:str)->Grafo:
    dict_hojas = pd.read_excel(ficheroDatos, sheet_name=['nodos_grafo','adyacentes'], index_col=0)
    estaciones = dict_hojas.get('nodos_grafo') # se lee la pestaña de estaciones
    adyacentes = dict_hojas.get('adyacentes') # se lee la pestaña de estaciones adyacentes
    estaciones_grafo = adyacentes.index.intersection(estaciones.index)   #nos quedamos solo con las estaciones que aplican para el grafo. Sino el df.loc da problemas
    estaciones = estaciones.loc[estaciones_grafo] # no se cargan nodos de estaciones "huérfanas"
    
    grafo1 = Grafo()
    for index, registro in estaciones.iterrows():   # vamos a crear los nodos para cada una de las estaciones
        aristas=[]  #lista de nodos adyacentes List[Tuple[Nodo,int]]
        etiqueta = str(index)
        coordernadas_nodo = [registro['CoordenadaX'],registro['CoordenadaY']]
        
        # Se van a buscar las estaciones adyacentes.
        # en pandas el df.loc devuelve una variabe tipo str si sólo hay una coincidencia
        # cuando hay varias coincidencias devuelve un objeto pandas.core.series.Series
        if type(adyacentes.loc[etiqueta,'Adyacente'])==str:  # nos devueleve un string
            elem=adyacentes.loc[etiqueta,'Adyacente']
            coor_parada = [estaciones.loc[elem, "CoordenadaX"], estaciones.loc[elem, "CoordenadaY"]]
            nuevo_adyacente=Nodo(elem, (estaciones.loc[elem, "CoordenadaX"], estaciones.loc[elem, "CoordenadaY"]) )
            aristas.append([nuevo_adyacente,distancia_coor(coor_parada, coordernadas_nodo)])
        else:   # nos devuelve una serie
            for elem in adyacentes.loc[etiqueta,'Adyacente']:
                coor_parada = [estaciones.loc[elem, "CoordenadaX"], estaciones.loc[elem, "CoordenadaY"]]
                nuevo_adyacente=Nodo(elem, (estaciones.loc[elem, "CoordenadaX"], estaciones.loc[elem, "CoordenadaY"]) )
                aristas.append([nuevo_adyacente,distancia_coor(coor_parada, coordernadas_nodo)])           
        #ya tenemos generadas las aristas    

        nuevo = Nodo(etiqueta, coordernadas_nodo,aristas)
        grafo1.añadir_nodo(nuevo)
    return grafo1

def main():
    nuevo_grafo = genera_grafos_con_nodos("grafo/nodos_grafo.xlsx")

    origen= 'Attiki'
    destino= 'Kifissia'
    print("RUTA A BUSCAR: {} => {}".format(origen,destino))
    try:
        ruta_estaciones = A_estrella(nuevo_grafo, origen, destino)
    except ValueError as fallo:
        print(fallo)
        exit()
    path = ruta_estaciones.busqueda()
    print(path)
    
if __name__ == "__main__":
    main()