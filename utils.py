import numpy as np

def fo(solucion, costos):
    valor = 0
    for i,s in enumerate(solucion):
        valor = valor + costos[s][i]
    return valor

def restriccionCapacidad(solucion, capacidades):
    for j, c in enumerate(capacidades):
        conjuntoI = [i for i in range(solucion) if j == solucion[i]]
        if sum(conjuntoI) > c:
            return False
    return True

def restriccionCompatibilidad(solucion, incompatibilidad):
    incompatibilidadTemp = incompatibilidad.copy()
    for i,incomp in enumerate(incompatibilidadTemp):
        if solucion[i] == solucion[incomp]:
            return False
        del incompatibilidad[incomp]
    return True
