# !/usr/bin/python3

import heapq
import math
import grafo as g
import vertice as v
import operator
import random

def obtener_parametros(linea):

    parametros = linea.split(" ")
    sep = " "
    aux1 = []
    parametros_final = []

    for i in range(1, len(parametros)):
        aux1.append(parametros[i])

    cadena = sep.join(aux1)
    aux2 = cadena.split(",")

    for i in range(0, len(aux2)):
        parametros_final.append(aux2[i])

    return parametros_final


def recorrido_dfs(grafo, v, visitados, padres, orden):
    visitados.add(v)
    for w in grafo.obtener_adyacentes(v):
        if w not in visitados:
            padres[w] = v
            orden[w] = orden[v] + 1
            recorrido_dfs(grafo, w, visitados, padres, orden)


def dfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    padres[origen] = None
    orden[origen] = 0
    recorrido_dfs(grafo, origen, visitados, padres, orden)
    return padres, orden


def bfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    cola = []
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    cola.append(origen)

    while len(cola) != 0:
        v = cola.pop(0)
        for w in grafo.obtener_adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                orden[w] = orden[v] + 1
                cola.append(w)

    return padres, orden

def camino_minimo(grafo, aeropuerto_origen, destino, modo):

    distancia = {}
    padres = {}
    visitados = set()
    heap = []
    peso_total = 0

    for key in grafo.obtener_todos_vertices():
        distancia[key] = float('inf')

    distancia[aeropuerto_origen] = 0
    padres[aeropuerto_origen] = None
    visitados.add(grafo.obtener_ciudad(aeropuerto_origen))
    heapq.heappush(heap, (distancia[aeropuerto_origen], aeropuerto_origen))

    while heap:

        vertice = heapq.heappop(heap)
        ciudad_actual = grafo.obtener_ciudad(vertice[1])
        visitados.add(ciudad_actual)

        if ciudad_actual == destino:
            return padres, distancia, peso_total, vertice[1]

        for adyacente in grafo.obtener_adyacentes(vertice[1]).keys():
            ciudad_adyacente = grafo.obtener_ciudad(adyacente)
            if ciudad_adyacente not in visitados:
                if modo == "barato":
                    peso = int(grafo.obtener_precio(vertice[1], adyacente))
                else:
                    peso = int(grafo.obtener_tiempo(vertice[1], adyacente))

                if vertice[0] + peso < distancia[adyacente]:
                    distancia[adyacente] = vertice[0] + peso
                    peso_total += peso
                    padres[adyacente] = vertice[1]
                    heapq.heappush(heap, (distancia[adyacente], adyacente))

    return padres, distancia, peso_total, vertice[1]

def prim(grafo, aeropuerto_origen, modo):

    visitados = []
    visitados.append(aeropuerto_origen)
    heap = []
    arbol = g.Grafo()
    vertice_actual = grafo.obtener_vertice(aeropuerto_origen)
    peso_total = 0

    for adyacente in vertice_actual.obtener_adyacentes().keys():
        if modo == "barato":
            peso_arista = grafo.obtener_precio(aeropuerto_origen, adyacente)
        else:
            peso_arista = grafo.obtener_tiempo(aeropuerto_origen, adyacente)
        heapq.heappush(heap, (peso_arista, adyacente, aeropuerto_origen))

    for v in grafo.obtener_todos_vertices().values():
        arbol.agregar_vertice(v.obtener_ciudad(), v.obtener_codigo(), 0, 0)

    while heap:
        v = heapq.heappop(heap)
        if grafo.obtener_ciudad(v[1]) in visitados:
            continue

        if modo == "barato":
            arbol.agregar_arista(v[1], v[2], 0, v[0], 0)
        else:
            arbol.agregar_arista(v[1], v[2], v[0], 0, 0)

        visitados.append(grafo.obtener_ciudad(v[1]))
        vertice_actual = grafo.obtener_vertice(v[1])

        for key in vertice_actual.obtener_adyacentes().keys():
            ciudad_adyacente = grafo.obtener_ciudad(key)

            if ciudad_adyacente not in visitados:

                if modo == "barato":
                    a_guardar = grafo.obtener_precio(v[1], key)
                else:
                    a_guardar = grafo.obtener_tiempo(v[1], key)
                peso_total += int(a_guardar)
                heapq.heappush(heap, (a_guardar, key, v[1]))
    return arbol, peso_total


def recorrido_vacaciones(grafo, origen, v, contador, n, visitados):

    visitados.append(v)

    if contador == n:
        return True

    for adyacente in grafo.obtener_adyacentes(v).keys():
        if adyacente not in visitados:
            if adyacente not in visitados:
                if contador == n-1:
                    if origen not in grafo.obtener_adyacentes(adyacente).keys():
                        break
                contador += 1
                if recorrido_vacaciones(grafo, origen, adyacente, contador, n, visitados):
                    return True
    visitados.remove(v)
    return False


def recorrer_lugares(grafo, lugares, actual, costo, visitados, claves):
    if len(lugares) == 0:
        return True

    codigo_random = random.choice(claves)
    ciudad_random = grafo.obtener_ciudad(codigo_random)
    padres, distancia, peso, aeropuerto_dest = camino_minimo(grafo, actual, ciudad_random, "rapido")

    costo += peso
    lugares.remove(ciudad_random)
    visitados.append(aeropuerto_dest)
    claves.remove(codigo_random)

    return recorrer_lugares(grafo, lugares, aeropuerto_dest, costo, visitados)


def centralidad(grafo):
    cent = {}

    for key in grafo.obtener_todos_vertices().keys():
        cent[key] = 0

    for key1 in grafo.obtener_todos_vertices().keys():
        padres, dist = bfs(grafo, key1)
        cent_aux = {}
        for key2 in grafo.obtener_todos_vertices().keys():
            cent_aux[key2] = 0

        # Filtra infinitos
        for a in dist:
            if type(dist) is float:
                if math.isinf(a):
                    dist.pop(a)

        vertices_ordenados = sorted(dist.items(), key=operator.itemgetter(1))

        for w in vertices_ordenados:
            if w[0] == key1:
                continue

            cent_aux[padres[w[0]]] += 1
            cent_aux[padres[w[0]]] += cent_aux[w[0]]

        for w in grafo.obtener_todos_vertices().keys():
            if w == key1:
                continue
            cent[w] += cent_aux[w]

    return cent
