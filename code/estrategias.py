import abc
import random
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time


class SolucionStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def solve(self):
        pass

    @abc.abstractmethod
    def plot(self):
        pass


class SA(SolucionStrategyAbstract):

    def __init__(self, alpha, temperaturaMin, temperaturaMax, threshold, iteraciones, nBsize):
        # Parámetros para SA, especificados en el documento adjuntos
        self.alpha = alpha
        self.temperaturaMin = temperaturaMin
        self.temperaturaMax = temperaturaMax
        self.threshold = threshold
        self.iteraciones = iteraciones
        self.nBsize = nBsize
        # Historia de soluciones y temperatura para gráficos
        self.historySolution = []
        self.historyTemperature = []
        # Nombre y datos para reportar la ejecución
        self.timeStamp = datetime.datetime.now().timestamp()
        self.executionTime = 0

    def generarVecino(self, solucion, nDemanda, nVehiculo, restriccion1, restriccion2, incompatibilidades, pasos):
        solucion2 = solucion.copy()
        for _ in range(pasos):
            demanda = random.randrange(nDemanda)
            vehiculoNuevo = random.randrange(nVehiculo)
            solucion2[demanda] = vehiculoNuevo
        while(not(restriccion1(solucion2) and restriccion2(solucion2))):
            solucion2 = solucion.copy()
            for _ in range(pasos):
                demanda = random.randrange(nDemanda)
                vehiculoNuevo = random.randrange(nVehiculo)
                solucion2[demanda] = vehiculoNuevo
        return solucion2

    # Generación aleatoria, modificar por una generación golosa
    def generateInitialSolution(self, nDemanda, nVehiculo, restriccion1, incompatibilidades, costos):
        solucion = [-1 for _ in range(nDemanda)]  # Se genera una solución
        # Parte golosa
        for i in range(nVehiculo):
            demanda = random.randrange(nDemanda)
            # Se encuentran todos los costos de la demanda i
            costosDemanda_i = [costos[j][demanda] for j in range(nVehiculo)]
            # Aquel vehiculo que minimiza el costo de la demanda
            solucion[i] = np.argmin(costosDemanda_i)

        # Parte aleatoria
        noInicializados = [i for i in range(nDemanda) if solucion[i] < 0]
        if len(noInicializados) >= int(0.5*len(solucion)):
            for k in noInicializados:
                # Se elije aleatoriamente un vehículo que no esté asignado a
                # una demanda incompatible para la demanda k no inicializada
                posiblesVehiculos = [i for i in range(nVehiculo) if (
                    i != solucion[incompatibilidades[k]])]
                solucion[k] = random.choice(posiblesVehiculos)
                tol = 0
                # Se veririfca que se cumpla la restricción de capacidad,
                # en caso de encontrar no una asignación satisfactoria durante la tolerancia simplemente
                # se deja sin asignación
                while(not restriccion1(solucion) and tol < 20):
                    solucion[k] = random.choice(posiblesVehiculos)
                    tol += 1
                if tol == 20:
                    solucion[k] = -1
        return solucion

    def solve(self, problema, graph=False):
        print("Resolviendo ...")
        start = time.time()

        # Aplicación de SA, algoritmo especificado en la documentación
        temperaturaActual = self.temperaturaMax
        solucion = self.generateInitialSolution(
            problema.nDemanda, problema.nVehiculos, problema.restriccionCapacidad, problema.incompatibilidad, problema.costos)
        # Ciclo de enfriamiento
        while(temperaturaActual - self.temperaturaMin >= self.threshold):
            # Ciclo de estabilización a cierta temperatura
            for _ in range(self.iteraciones):
                # Historial de soluciones y temperatura
                self.historySolution.append(problema.funcionObjetivo(solucion))
                self.historyTemperature.append(temperaturaActual)
                # Generación de vecino
                solucion2 = self.generarVecino(
                    solucion, problema.nDemanda, problema.nVehiculos, problema.restriccionCapacidad, problema.restriccionCompatibilidad, problema.incompatibilidad, self.nBsize)
                # Calculo de delta de energía
                deltaEnergia = problema.funcionObjetivo(
                    solucion2) - problema.funcionObjetivo(solucion)
                # Aceptación de nueva solución si es mejor se acepta inmediatamente, si no con la probabilidad
                # de exp(-deltaEnergia/Tactual)
                if deltaEnergia <= 0:
                    solucion = solucion2
                else:
                    probabilidadDeAceptacion = np.exp(
                        -deltaEnergia/temperaturaActual)
                    # Se escoje aleatoriamente con las probabilidades mencionadas
                    eleccion = np.random.choice([False, True], p=[
                                                1-probabilidadDeAceptacion, probabilidadDeAceptacion])
                    solucion = solucion2 if eleccion else solucion
            # Actualización de la temperatura
            temperaturaActual = temperaturaActual*self.alpha

        self.executionTime = time.time() - start

        # Guardado de resultados
        results = open(
            "..\\dropzone\\out\\solucion {}.csv".format(self.timeStamp), "w")
        results.write("Demandas ; Vehiculos\n")
        for i, s in enumerate(solucion):
            if s >= 0:
                results.write("d{} ; v{}\n".format(i+1, s+1))
            else:
                results.write("d{} ; - \n".format(i+1))
        results.write("valor {}".format(problema.funcionObjetivo(solucion)))
        results.close()
        return

    def plot(self):
        # Gráfico de historial del valor de la función objetivo
        plt.rcParams["figure.figsize"] = [20, 10]
        fig, ax = plt.subplots()
        scat = ax.scatter(range(len(self.historySolution)), self.historySolution,
                          c=self.historyTemperature, cmap="hsv", vmin=self.temperaturaMin, vmax=self.temperaturaMax, s=0.1)
        ax.set_title("Mejor costo {} - Tiempo ejecución {:.2f} min".format(
            self.historySolution[-1], self.executionTime/60))
        ax.set_xlabel("N° Iteraciones")
        ax.set_ylabel("Costo total")
        bar = fig.colorbar(scat, ax=ax, orientation='vertical')
        bar.ax.set_ylabel("Temperatura")
        fig.savefig("..\\dropzone\\out\\{}.png".format(self.timeStamp))

        plt.close()
        return
