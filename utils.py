import numpy as np

def fo(solucion, costos):
    valor = 0
    for i,s in enumerate(solucion):
        valor = valor + costos[s][i]
    return valor

def restriccionCapacidad(solucion, capacidades):
    for j, c in enumerate(capacidades):
        conjuntoI = [i for i in range(solucion) if j == solucion[i]]
        conjuntoI = np.array(conjuntoI)
        if conjuntoI.sum() > c:
            return False
    return True

def restriccionCompatibilidad(solucion, incompatibilidad):
    
    return True
