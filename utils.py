
import pandas as pd
class asignacion:
    def __init__(self, cargas, costos, capacidades, incompatibilidad = None):
        self.costos = pd.read_csv(costos) #costos de asignar demandas a ciertos vehículos
        self.carga = pd.read_csv(cargas)  #cantidad demandada por cada pedido
        self.capacidades = pd.read_csv(capacidades) #capacidad de cada camion
        self.incompatibilidad = pd.read_csv( 
            incompatibilidad) if incompatibilidad else None #incomptaibilidad en caso de que exista
        
    def functionObjetivo(self, solucion, costos):
        valor = 0
        for i,s in enumerate(solucion):
            valor = valor + costos[s][i]
        return valor

    def restriccionCapacidad(self, solucion, capacidades):
        for j, c in enumerate(capacidades):
            conjuntoI = [i for i in range(solucion) if j == solucion[i]]
            if sum(conjuntoI) > c:
                return False
        return True

    def restriccionCompatibilidad(self, solucion, incompatibilidad):
        incompatibilidadTemp = incompatibilidad.copy()
        for i,incomp in enumerate(incompatibilidadTemp):
            if incomp > 0 and solucion[i] == solucion[incomp]:
                    return False
            del incompatibilidadTemp[incomp]
        return True