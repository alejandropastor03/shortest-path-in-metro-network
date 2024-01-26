"""
Interfaz gráfica
"""
from algoritmo.grafo import genera_grafos_con_nodos
from algoritmo.a_estrella import A_estrella

import PySimpleGUI as sg
import math
import os

# Path de la imagen del metro usada y de los nodos del grafo
script_dir = os.path.dirname(__file__)
imagen_rel_path = "recursos/map3.png"
imagen_abs_path = os.path.join(script_dir, imagen_rel_path)
nodos_grafo_rel_path = "recursos/nodos_grafo.xlsx"
nodos_grafo_abs_path = os.path.join(script_dir, nodos_grafo_rel_path)

# Diccionario con los nombres de las estaciones y sus coordenadas en la representación gráfica
estaciones = {
    'Kifissia': (533, 651),
    'Kat': (515, 624),
    'Maroussi': (515, 598),
    'Neratziotissa': (482, 559),
    'Irini': (458, 547),
    'Iraklio': (411, 548),
    'Nea Ionia': (381, 544),
    'Pefkakia': (367, 529),
    'Perissos': (351, 513),
    'Ano Patissia': (326, 489),
    'Aghia Eleftherios': (311, 473),
    'Kato Patissia': (295, 446),
    'Aghia Nikolaos': (291, 423),
    'Attiki': (291, 398),
    'Victoria': (309, 372),
    'Omonia': (309, 345),
    'Monastiraki': (292, 317),
    'Thissio': (267, 313),
    'Petralona': (244, 285),
    'Tavros': (228, 273),
    'Kalithea': (210, 251),
    'Moschato': (163, 244),
    'Faliro': (120, 210),
    'Piraeus': (69, 220),
    'Anthoupoli': (197, 456),
    'Peristeri': (212, 441),
    'Aghia Antonios': (236, 416),
    'Sepolia': (265, 406),
    'Larissa Station': (287, 372),
    'Metaxourghio': (287, 351),
    'Panepistimio': (321, 330),
    'Syntagma': (321, 316),
    'Akropolis': (310, 292),
    'Syngrou': (292, 277),
    'Neos Kosmos': (291, 255),
    'Aghia Ioannis': (310, 247),
    'Dafni': (330, 231),
    'Aghia Dimitrios': (334, 192),
    'Ilioupoli': (344, 149),
    'Alimos': (343, 103),
    'Argyroupoli': (344, 64),
    'Elliniko': (366, 19),
    'Teatro Dimotiko': (76, 197),
    'Maniatika': (67, 262),
    'Nikea': (85, 286),
    'Korydallos': (98, 312),
    'Aghia Varvara': (111, 338),
    'Aghia Marina': (136, 364),
    'Egaleo': (170, 368),
    'Eleonas': (205, 369),
    'Kerameikos': (263, 331),
    'Evangelismos': (356, 316),
    'Megaro Moussikis': (377, 333),
    'Ambelokipi': (385, 352),
    'Panormou': (399, 372),
    'Katehaki': (437, 373),
    'Ethniki Amyna': (465, 396),
    'Holargos': (495, 412),
    'Nomismatokopio': (533, 437),
    'Aghia Paraskevi': (558, 464),
    'Halandri': (588, 480),
    'Doukissis Plakentias': (614, 479),
    'Pallini': (660, 365),
    'Peania-Kantza': (661, 277),
    'Koropi': (661, 170),
    'Aeropuerto Eleftherios Venizelos': (757, 114)

}

# ---------------------------------------
# Funciones auxiliares
# ---------------------------------------
def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# ---------------------------------------
# Estructura de la interfaz gráfica
# ---------------------------------------
# Estructura del lado derecho 
columna_der = [
    [sg.Text('METRO')],
    [sg.Text('Origen'),sg.Combo(k='origen',values=tuple(estaciones.keys()), readonly=True, enable_events=True), sg.Button('Seleccionar en mapa',k='origen_mapa')],
    [sg.Text('Destino'),sg.Combo(k='destino',values=tuple(estaciones.keys()), readonly=True, enable_events=True), sg.Button('Seleccionar en mapa',k='destino_mapa')],
    [sg.Text('',k='-modo_seleccion-')],
    [sg.Button('Iniciar'), sg.Button('Reiniciar')],
    [sg.Text('Ruta a seguir:')],
    [sg.Multiline(k='route', size= (50,27),disabled=True)],
    [sg.Button('Cerrar', pad=(400,5))]
   ]

# Estructura del lado izquierdo
columna_izq = [
    [sg.Graph(enable_events=True,k='-graph-', canvas_size=(777,660),graph_bottom_left=(0,0),graph_top_right=(777,660))]
]

# Estructura general
layout = [
    [sg.Column(columna_izq,size=(777,660)),sg.Column(columna_der, size=(460,660))]
]

# Inicialización de la ventana para la herramienta gráfica
window = sg.Window('Metro Atenas - Algoritmo A*', layout, finalize=True)
window['-graph-'].draw_image(imagen_abs_path,location = (0,660))    # Carga la imagen del mapa del metro

# ---------------------------------------
# Bucle principal, manejo de eventos
# ---------------------------------------
modo_seleccion_mapa = None
origen_ids = None
destino_ids = None
lineas_ids = []
graph = window['-graph-']
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cerrar'):
        break

    # limpiar el mapa, las elecciones de origen y destino y la ruta resultado 
    if event == 'Reiniciar':
        if origen_ids is not None:
            graph.delete_figure(origen_ids[0])
            graph.delete_figure(origen_ids[1])     

        if destino_ids is not None:
            graph.delete_figure(destino_ids[0])
            graph.delete_figure(destino_ids[1])

        for linea_id in lineas_ids:
            graph.delete_figure(linea_id)

        window['route']('')
        window['origen']('')
        window['destino']('')
        window['-modo_seleccion-']('')
        modo_seleccion_mapa = None
    
    if event == 'Iniciar':

        # borrar las líneas pintadas de posibles aplicaciones anteriores
        if lineas_ids != []:
            for linea_id in lineas_ids:
                graph.delete_figure(linea_id)

        # aplicar el algoritmo A* al grafo generado
        if values['origen'] != '' and values['destino'] != '':
            nuevo_grafo = genera_grafos_con_nodos(nodos_grafo_abs_path)

            origen = values['origen']
            destino = values['destino']
            ruta_estaciones = A_estrella(nuevo_grafo, origen, destino)
            path = ruta_estaciones.busqueda()
            window['route']('')
            
            resultado = ''
            # Marcar en el mapa el camino recorrido
            for i in range(1, len(path)):
                lineas_ids.append(window['-graph-'].draw_line(estaciones[path[i-1]],estaciones[path[i]], width= 2))

            if len(path) == 2:
                resultado += str(path[0])+ ' -> '+str(path[1]+'\n')

            if len(path) >= 3:
                # Marcar los transbordos y resultado de aplicar el algoritmo al grafo
                path_aux = path
                for i in range(1,len(path)-1):
                    if path[i] == 'Piraeus':
                        if (path[i-1] == 'Dimotiko Theatro' or path[i-1] == 'Maniatika') and path[i+1] == 'Faliro':
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 3 -> Línea 1)\n'
                        elif path[i-1] == 'Faliro' and (path[i+1] == 'Dimotiko Theatro' or path[i+1] == 'Maniatika'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 1 -> Línea 3)\n'

                    elif path[i] == 'Monastiraki':
                        if (path[i-1] == 'Kerameikos' or path[i-1] == 'Syntagma') and (path[i+1] == 'Thissio' or path[i+1] == 'Omonia'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 3 -> Línea 1)\n'
                        elif (path[i-1] == 'Thissio' or path[i-1] == 'Omonia') and (path[i+1] == 'Kerameikos' or path[i+1] == 'Syntagma'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 1 -> Línea 3)\n'

                    elif path[i] == 'Syntagma':
                        if (path[i-1] == 'Akropolis' or path[i-1] == 'Panepistimio') and (path[i+1] == 'Monastiraki' or path[i+1] == 'Evangelismos'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 2 -> Línea 3)\n'
                        elif (path[i-1] == 'Monastiraki' or path[i-1] == 'Evangelismos') and (path[i+1] == 'Akropolis' or path[i+1] == 'Panepistimio'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 3 -> Línea 2)\n'
                    
                    elif path[i] == 'Omonia':
                        if (path[i-1] == 'Metaxourghio' or path[i-1] == 'Panepistimio') and (path[i+1] == 'Monastiraki' or path[i+1] == 'Victoria'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 2 -> Línea 1)\n'
                        elif (path[i-1] == 'Monastiraki' or path[i-1] == 'Victoria') and (path[i+1] == 'Metaxourghio' or path[i+1] == 'Panepistimio'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 1 -> Línea 2)\n'

                    elif path[i] == 'Attiki':
                        if (path[i-1] == 'Larissa Station' or path[i-1] == 'Sepolia') and (path[i+1] == 'Aghia Nikolaos' or path[i+1] == 'Victoria'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 2 -> Línea 1)\n'
                        elif (path[i-1] == 'Aghia Nikolaos' or path[i-1] == 'Victoria') and (path[i+1] == 'Sepolia' or path[i+1] == 'Larissa Station'):
                            if str(path_aux[0]) != str(path[i]):
                                resultado += str(path_aux[0])+ ' -> '+str(path[i]+'\n')
                            path_aux = path[i+1:]
                            resultado += str(path[i])+ ' -> '+str(path[i+1])+' (Transbordo: Línea 1 -> Línea 2)\n'
            resultado += str(path_aux[0])+ ' -> '+str(path[-1])
            window['route'](resultado)

    # dibujar en el grafo las marcas de origen y destino si el usuario hace click en el mapa
    if event == '-graph-':
        for estacion in estaciones.keys():
            if distance(values['-graph-'],estaciones[estacion]) < 10:
                if modo_seleccion_mapa == 'origen':
                    window['origen'](estacion)
                    values['origen'] = estacion
                    if origen_ids is not None:
                        graph.delete_figure(origen_ids[0])
                        graph.delete_figure(origen_ids[1])
                    origen_ids = (
                        graph.draw_circle(estaciones[values['origen']],5, fill_color='black'),
                        graph.draw_text('ORIGEN', (estaciones[values['origen']][0], estaciones[values['origen']][1] - 10))
                    )
                elif modo_seleccion_mapa == 'destino':
                    window['destino'](estacion)
                    values['destino'] = estacion
                    if destino_ids is not None:
                        graph.delete_figure(destino_ids[0])
                        graph.delete_figure(destino_ids[1])
                    destino_ids = (
                        graph.draw_circle(estaciones[values['destino']],5, fill_color='black'),
                        graph.draw_text('DESTINO', (estaciones[values['destino']][0], estaciones[values['destino']][1] - 10))
                    )
                break

    # elección de estación origen en el desplegable
    if event == 'origen':
        if origen_ids is not None:
            graph.delete_figure(origen_ids[0])
            graph.delete_figure(origen_ids[1])
        origen_ids = (
            graph.draw_circle(estaciones[values['origen']],5, fill_color='black'),
            graph.draw_text('ORIGEN', (estaciones[values['origen']][0], estaciones[values['origen']][1] - 10))
        )

    # elección de estación destino en el desplegable
    if event == 'destino':
        if destino_ids is not None:
            graph.delete_figure(destino_ids[0])
            graph.delete_figure(destino_ids[1])
        destino_ids = (
            graph.draw_circle(estaciones[values['destino']],5, fill_color='black'),
            graph.draw_text('DESTINO', (estaciones[values['destino']][0], estaciones[values['destino']][1] - 10))
        )
    
    # permite elegir el origen haciendo click en el mapa en el caso de que el botón para ello sea pulsado
    if event == 'origen_mapa': 
        modo_seleccion_mapa = 'origen'
        window['-modo_seleccion-']('Seleccione el origen en el mapa')

    # permite elegir el destino haciendo click en el mapa en el caso de que el botón para ello sea pulsado
    if event == 'destino_mapa': 
        modo_seleccion_mapa = 'destino'
        window['-modo_seleccion-']('Seleccione el destino en el mapa')

# Finalización
window.close()
exit(0)
