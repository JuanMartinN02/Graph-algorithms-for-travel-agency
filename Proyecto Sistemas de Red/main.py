import csv 
import networkx as nx
import matplotlib.pyplot as mp

# Cargar los requerimientos de visas como un diccionario
def load_visas(visasCSV):
    visas = {}
    with open(visasCSV) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            airport, requires_visa = row
            visas[airport] = requires_visa == "si"
    return visas

# Creación del grafo
def cargar_grafo(destinosCSV, visas):
    grafo = nx.Graph()

    # Agregar nodos con atributo de visa
    for nodo, necesita_visa in visas.items():
        grafo.add_node(nodo, requiere_visa=necesita_visa)

    # Agregar aristas
    with open(destinosCSV) as csvfile:
        reader = csv.reader(csvfile)
        for origen, destino, costo in reader:
            grafo.add_edge(origen, destino, costo=float(costo))

    return grafo

# Dijkstra modificado para considerar visas
def dijkstra(grafo, origen, destino, tiene_visa):
    # Verificación inicial de visas
    if not tiene_visa:
        if grafo.nodes[origen].get('requiere_visa', False):
            return None, float('inf')
        if grafo.nodes[destino].get('requiere_visa', False):
            return None, float('inf')

    # Inicialización
    distancias = {nodo: float('inf') for nodo in grafo.nodes}
    distancias[origen] = 0
    predecesores = {nodo: None for nodo in grafo.nodes}
    visitados = set()

    while len(visitados) < len(grafo.nodes):
        # Encuentra el nodo no visitado con la menor distancia
        nodos_no_visitados = [n for n in grafo.nodes if n not in visitados]
        if not nodos_no_visitados:
            break
            
        nodo_actual = min(nodos_no_visitados, key=lambda n: distancias[n])
        
        if distancias[nodo_actual] == float('inf'):
            break

        visitados.add(nodo_actual)

        # Actualiza las distancias de los vecinos
        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                # Verificar restricción de visa
                if not tiene_visa and grafo.nodes[vecino].get('requiere_visa', False):
                    continue  # Saltar este vecino
                
                peso = grafo[nodo_actual][vecino]['costo']
                nueva_distancia = distancias[nodo_actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual

    # Reconstruye el camino más corto
    if distancias[destino] == float('inf'):
        return None, float('inf')
    
    camino = []
    nodo = destino
    while nodo is not None:
        camino.insert(0, nodo)
        nodo = predecesores[nodo]

    return camino, distancias[destino]

# BFS modificado para considerar visas
def bfs_camino_mas_corto(grafo, origen, destino, tiene_visa):
    # Verificación inicial de visas
    if not tiene_visa:
        if grafo.nodes[origen].get('requiere_visa', False):
            return None
        if grafo.nodes[destino].get('requiere_visa', False):
            return None

    # Inicialización
    visitados = set()
    cola = [[origen]]
    
    if origen == destino:
        return [origen]

    while cola:
        camino = cola.pop(0)
        nodo_actual = camino[-1]

        if nodo_actual not in visitados:
            vecinos = grafo.neighbors(nodo_actual)
            
            for vecino in vecinos:
                # Verificar restricción de visa
                if not tiene_visa and grafo.nodes[vecino].get('requiere_visa', False):
                    continue  # Saltar este vecino
                
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
                
                if vecino == destino:
                    return nuevo_camino
            
            visitados.add(nodo_actual)
    
    return None

# Cargar datos
visasprueba = load_visas("visas.csv")
grafo_prueba = cargar_grafo("destinos.csv", visasprueba)

# Interfaz principal
while True:
    print("\n=====================")
    print("Sistema de Optimización de Viajes")
    
    origen = input("Ingrese aeropuerto de origen (Ej: CCS): ").strip().upper()
    destino = input("Ingrese aeropuerto de destino (Ej: AUA): ").strip().upper()
    
    # Validar códigos de aeropuerto
    if origen not in grafo_prueba.nodes:
        print(f"Error: Aeropuerto {origen} no existe")
        continue
    if destino not in grafo_prueba.nodes:
        print(f"Error: Aeropuerto {destino} no existe")
        continue
        
    tiene_visa_input = input("¿El pasajero tiene visa? (S/N): ").strip().upper()
    tiene_visa = tiene_visa_input == "S"
    
    tipo_optimizacion = input("¿Qué optimización desea? (1: Menor escalas, 2: Menor costo): ").strip()

    if tipo_optimizacion == '1':
        camino = bfs_camino_mas_corto(grafo_prueba, origen, destino, tiene_visa)
        if camino:
            # Calcular costo total
            costo_total = 0
            for i in range(len(camino) - 1):
                costo_total += grafo_prueba[camino[i]][camino[i + 1]]['costo']
            escalas = len(camino) - 2
            print(f"\nRuta con menos escalas: {' → '.join(camino)}")
            print(f"Costo total: ${costo_total:.2f}")
            print(f"Número de escalas: {escalas}")
        else:
            print("\nNo se encontró ruta válida con las restricciones de visa")
    
    elif tipo_optimizacion == '2':
        camino, costo = dijkstra(grafo_prueba, origen, destino, tiene_visa)
        if camino:
            escalas = len(camino) - 2
            print(f"\nRuta más económica: {' → '.join(camino)}")
            print(f"Costo total: ${costo:.2f}")
            print(f"Número de escalas: {escalas}")
        else:
            print("\nNo se encontró ruta válida con las restricciones de visa")
    
    else:
        print("Opción inválida. Intente nuevamente.")
        continue
    
    continuar = input("\n¿Desea otra consulta? (S/N): ").strip().upper()
    if continuar != "S":
        break

#Mostrar gráfico del grafo
pos = nx.spring_layout(grafo_prueba, seed=225)
nx.draw(grafo_prueba, pos, with_labels=True, node_color='lightblue', 
        edge_color='gray', node_size=1000, font_size=10)
edge_labels = nx.get_edge_attributes(grafo_prueba, 'costo')
nx.draw_networkx_edge_labels(grafo_prueba, pos, edge_labels=edge_labels)
mp.show()