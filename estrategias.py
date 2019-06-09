import abc
import random
import numpy as np


class SolucionStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def solve(self):
        pass


class SA(SolucionStrategyAbstract):

    def __init__(self, alpha, temperaturaMin, temperaturaMax, threshold, iteraciones):
        self.alpha = alpha
        self.temperaturaMin = temperaturaMin
        self.temperaturaMax = temperaturaMax
        self.threshold = threshold
        self.iteraciones = iteraciones

    def generarVecino(self, solucion, nDemanda, nVehiculo, restriccion1, restriccion2, pasos):
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
        for i in range(nVehiculo):
            demanda = random.randrange(nDemanda)
            # Se encuentran todos los costos de la demanda i
            costosDemanda_i = [costos[j][demanda] for j in range(nVehiculo)]
            # Aquel vehiculo que minimiza el costo de la demanda
            solucion[i] = np.argmin(costosDemanda_i)
        noInicializados = [i for i in range(nDemanda) if solucion[i] < 0]
        for k in noInicializados:
            posiblesVehiculos = [i for i in range(nVehiculo) if (
                i != solucion[incompatibilidades[k]])]
            solucion[k] = random.choice(posiblesVehiculos)
            tol = 0
            while(not restriccion1(solucion) and tol < 50):
                solucion[k] = random.choice(posiblesVehiculos)
                tol += 1
            if tol == 50:
                solucion[k] = -1
        return solucion

    def solve(self, problema):
        print("Resolviendo ...")
        temperaturaActual = self.temperaturaMax
        solucion = self.generateInitialSolution(
            problema.nDemanda, problema.nVehiculos, problema.restriccionCapacidad, problema.incompatibilidad, problema.costos)
        while(temperaturaActual - self.temperaturaMin >= self.threshold):
            #print("Temperatura {}".format(temperaturaActual))
            #print("\t\tSolucion actual valor =  {}".format(
            #    problema.funcionObjetivo(solucion)))
            for _ in range(self.iteraciones):
                solucion2 = self.generarVecino(
                    solucion, problema.nDemanda, problema.nVehiculos, problema.restriccionCapacidad, problema.restriccionCompatibilidad, 2)
                deltaEnergia = problema.funcionObjetivo(
                    solucion2) - problema.funcionObjetivo(solucion)
                if deltaEnergia <= 0:
                    solucion = solucion2
                else:
                    probabilidadDeAceptacion = np.exp(
                        -deltaEnergia/temperaturaActual)
                    eleccion = np.random.choice([False, True], p=[
                                                1-probabilidadDeAceptacion, probabilidadDeAceptacion])
                    solucion = solucion2 if eleccion else solucion
            temperaturaActual = temperaturaActual*self.alpha
        for i, s in enumerate(solucion):
            if s >= 0:
                print("d{} | v{}".format(i+1, s+1))
            else:
                print("d{} | - ".format(i+1))
        print(problema.funcionObjetivo(solucion))
