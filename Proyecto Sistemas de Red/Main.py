import csv 
import networkx as nx
import matplotlib.pyplot as mp

#Cargar los requerimientos de visas como un diccionario
def load_visas(visasCSV):
    visas = {}
    with open(visasCSV) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            airport, requires_visa = row
            visas[airport] = requires_visa == "si"
    return visas

#creacion del grafo
def cargar_grafo(destinosCSV, visas):
    grafo = nx.Graph()

    #agregar nodos
    for nodo, necesita_visa in visas.items():
        grafo.add_node(nodo, requiere_visa = necesita_visa)

    #agregar aristas
    with open(destinosCSV) as csvfile:
        reader = csv.reader(csvfile)
        for origen, destino, costo in reader:
            grafo.add_edge(origen, destino, costo=float(costo))

    return grafo

#dijkstra
def dijkstra(grafo, origen, destino):
    # Inicialización
    distancias = {nodo: float('inf') for nodo in grafo.nodes}
    distancias[origen] = 0
    predecesores = {nodo: None for nodo in grafo.nodes}
    visitados = set()

    while len(visitados) < len(grafo.nodes):
        # Encuentra el nodo no visitado con la menor distancia
        nodo_actual = min((nodo for nodo in grafo.nodes if nodo not in visitados), key=lambda nodo: distancias[nodo], default=None)
        
        if nodo_actual is None or distancias[nodo_actual] == float('inf'):
            break  # No hay más nodos alcanzables

        visitados.add(nodo_actual)

        # Actualiza las distancias de los vecinos
        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                peso = grafo[nodo_actual][vecino]['costo']
                nueva_distancia = distancias[nodo_actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual

    # Reconstruye el camino más corto
    camino = []
    nodo = destino
    while nodo is not None:
        camino.insert(0, nodo)
        nodo = predecesores[nodo]

    if distancias[destino] == float('inf'):
        return None, float('inf')  # No hay camino entre origen y destino

    return camino, distancias[destino]

#BFS
def bfs_camino_mas_corto(grafo, origen, destino):

    # Inicialización
    visitados = set()
    cola = [[origen]]  # Cola para almacenar caminos
    if origen == destino:
        return [origen]  # Si origen y destino son iguales, el camino es el nodo mismo

    while cola:
        # Obtiene el primer camino de la cola
        camino = cola.pop(0)
        nodo_actual = camino[-1]

        # Si el nodo actual ya fue visitado, lo ignoramos
        if nodo_actual not in visitados:
            vecinos = grafo.neighbors(nodo_actual)

            # Recorre los vecinos del nodo actual
            for vecino in vecinos:
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)

                # Si encontramos el destino, retornamos el camino
                if vecino == destino:
                    return nuevo_camino

            # Marca el nodo actual como visitado
            visitados.add(nodo_actual)

    return None  # Si no se encuentra un camino, retorna None

# Main
visasprueba = load_visas("visas.csv")
grafo_prueba = cargar_grafo("destinos.csv", visasprueba)

print(visasprueba)
pos = nx.spring_layout(grafo_prueba, seed=225)

#dibuja el grafo
nx.draw(grafo_prueba, pos, label=True, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=10, font_color='black')

#dibuja las aristas 
edge_labels = nx.get_edge_attributes(grafo_prueba, 'costo')
nx.draw_networkx_edge_labels(grafo_prueba, pos, edge_labels=edge_labels)

#app
while True:
    print("\n=====================")
    print("Sistema de Optimización de Viajes")
    print("Bienvenido al sistema de optimización de viajes.")
    print("Por favor, ingrese los códigos de los aeropuertos de origen y destino.")
    origen = input("Ingrese el aeropuerto de origen (Ejemplo: CCS): ").strip().upper()
    destino = input("Ingrese el aeropuerto de destino (Ejemplo: CCS)): ").strip().upper()
    
    #verifica si los códigos de aeropuerto son válidos!!!! FALTA HACERLO!!!
    #!!!!!!!!!!!!
    #!!!!!!!!!!!

    tipo_optimizacion = input("¿Qué tipo de optimización desea realizar? (1: Camino más corto, 2: Camino más barato): ").strip()
    if tipo_optimizacion not in ['1', '2']:
        print("Opción no válida. Por favor, ingrese 1 o 2.")
        continue
    if tipo_optimizacion == '1':
        camino, costo = dijkstra(grafo_prueba, origen, destino)
        if camino:
            print(f"El camino más corto entre {origen} y {destino} es: {' -> '.join(camino)} con un costo total de {costo}")
            break
        else:
            print(f"No hay un camino entre {origen} y {destino}.")
    
    elif tipo_optimizacion == '2':  
        camino = bfs_camino_mas_corto(grafo_prueba, origen, destino)
        costo = sum(grafo_prueba[camino[i]][camino[i + 1]]['costo'] for i in range(len(camino) - 1)) if camino else float('inf')
        if camino:
            print(f"El camino más corto entre {origen} y {destino} es: {' -> '.join(camino)} con un costo total de {costo}")
            break
        else:
            print(f"No hay un camino entre {origen} y {destino}.")
        
    else:
        print("Uno o ambos códigos de aeropuerto no son válidos. Intente nuevamente.")

False

#muestra el grafo
mp.show()

#visa?
#origen
#destino
#viaje mas corto o mas barato?

