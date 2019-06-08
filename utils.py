
import pandas as pd


class asignacion:
    def __init__(self, cargas, costos, capacidades, incompatibilidad=None):
        # costos de asignar demandas a ciertos vehículos
        self.costos = pd.read_csv(costos)
        self.carga = pd.read_csv(cargas)  # cantidad demandada por cada pedido
        self.capacidades = pd.read_csv(capacidades)  # capacidad de cada camion
        self.incompatibilidad = pd.read_csv(
            incompatibilidad) if incompatibilidad else None  # incomptaibilidad en caso de que exista

    def functionObjetivo(self, solucion):
        valor = 0
        for i, s in enumerate(solucion):
            valor = valor + self.costos[s][i]
        return valor

    def restriccionCapacidad(self, solucion):
        for j, c in enumerate(self.capacidades):
            conjuntoI = [i for i in range(solucion) if j == solucion[i]]
            if sum(conjuntoI) > c:
                return False
        return True

    def restriccionCompatibilidad(self, solucion):
        incompatibilidadTemp = self.incompatibilidad.copy()
        for i, incomp in enumerate(incompatibilidadTemp):
            if incomp > 0 and solucion[i] == solucion[incomp]:
                return False
            del incompatibilidadTemp[incomp]
        return True
