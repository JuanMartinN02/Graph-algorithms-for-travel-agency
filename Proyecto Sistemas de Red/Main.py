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


visasprueba = load_visas("visas.csv")
grafo_prueba = cargar_grafo("destinos.csv", visasprueba)

print(visasprueba)
pos = nx.spring_layout(grafo_prueba, seed=225)
nx.draw(grafo_prueba, pos)
mp.show()

#visa?
#origen
#destino
#viaje mas corto o mas barato?



