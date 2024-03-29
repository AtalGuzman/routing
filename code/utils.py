import pandas as pd


class asignacion:

    def __init__(self, costos, cargas, capacidades, nVehiculos, nDemanda, estrategiaDeSolucion, incompatibilidad=None):

        self._estrategia = estrategiaDeSolucion
        self.nVehiculos = int(nVehiculos)
        self.nDemanda = int(nDemanda)

        # Transformación de lo leído desde el archivo de texto plano a un matriz sencilla
        def preprocesamiento(vector): return [
            [vector["costo"][y+x*nVehiculos] for x in range(nDemanda)] for y in range(nVehiculos)]
        self.costos = preprocesamiento(pd.read_csv(costos, sep=";"))

        # Transformación de lo leído desde el archivo a un vector
        self.carga = pd.read_csv(cargas, sep=";").get_values()[:, 1]
        self.capacidades = pd.read_csv(capacidades, sep=";").get_values()[:, 1]

        # En esta implementación se está asumiendo incompatibilidad de a pares,
        # en base a lo observado en las instancias de prueba
        # Se crea el vector de incompatibilidad, con -1 significa el elemento en esa posición
        # no tiene conflictos
        self.incompatibilidad = [-1 for i in range(nDemanda)]

        # Se actualiza esta información con lo leído desde el archivo de entrada, de lo contrario queda todo negativo
        # y simplemente no se considera al evaluar la restricción de compatibilidad.
        if incompatibilidad:
            temp = pd.read_csv(incompatibilidad, sep=";").get_values()
            for i in range(temp.shape[0]):
                self.incompatibilidad[int(
                    temp[i][0][1]) - 1] = int(temp[i][1][1])-1
                self.incompatibilidad[int(
                    temp[i][1][1]) - 1] = int(temp[i][0][1])-1

        self.solucion = None

    def funcionObjetivo(self, solucion):
        # Sumatoria de los costos entre de la demanda y el vehículo que la va a suplir, considerando
        # que es posible que demandas queden sin satisfacer, en cuyo caso no son contabilizadas
        return sum([self.costos[vehiculo][demanda] for demanda, vehiculo in enumerate(solucion) if vehiculo >= 0])

    def restriccionCapacidad(self, solucion):
        # Determina si la solución actual es factible, respecto a la capacidad de los vehículos
        for vehiculo in range(self.nVehiculos):
            capacidad = self.capacidades[vehiculo]
            conjuntoI = [self.carga[i]
                         for i in range(len(solucion)) if vehiculo == solucion[i]]
            if sum(conjuntoI) > capacidad:
                return False
        return True

    def restriccionCompatibilidad(self, solucion):
        # Determina si la solución actual es facible, respecto a la compatibilidad de las soluciones
        for i, incomp in enumerate(self.incompatibilidad):
            if incomp > 0 and solucion[i] == solucion[incomp] and solucion[i] > 0 and solucion[incomp] > 0:
                return False
        return True

    def resolver(self):
        # Se resuelve el modelo aquí planteado, dependiendo de la estrategia que se utilice
        self._estrategia.solve(self)

    def graficar(self):
        # Se grafican los datos según la estrategia usada
        self._estrategia.plot()
