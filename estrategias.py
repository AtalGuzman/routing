import abc
import random
import numpy as np
import math

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

        # restriccion de capacidad
        while(not(restriccion1(solucion2) and restriccion2(solucion2))):
            for _ in range(pasos):
                demanda = random.randrange(nDemanda)
                vehiculoNuevo = random.randrange(nVehiculo)
                solucion2[demanda] = vehiculoNuevo
        return solucion2

    def generateInitialSolution(self, nDemanda, nVehiculo, restriccion1, restriccion2):
        solucion = [random.randrange(nVehiculo) for _ in range(nDemanda)]
        vehiculo = random.randrange(nVehiculo)
        while(not(restriccion1(solucion) and restriccion2(solucion))):
            dep = random.randrange(nDemanda)
            vehiculo = random.randrange(nVehiculo)
            solucion[dep] = vehiculo
        return solucion

    def solve(self, problema):
        print("Resolviendo ...")
        temperaturaActual = self.temperaturaMax
        solucion = self.generateInitialSolution(
            problema.nDemanda, problema.nVehiculos, problema.restriccionCapacidad, problema.restriccionCompatibilidad)
        print("\tSolucion actual {} =  {}".format(
                    solucion, problema.funcionObjetivo(solucion)))
        while(temperaturaActual - self.temperaturaMin >= self.threshold):
            print("Temperatura {}".format(temperaturaActual))
            for k in range(self.iteraciones):
                print("\tIteracion {}".format(k))
                print("\t\tSolucion actual {} =  {}".format(
                    solucion, problema.funcionObjetivo(solucion)))
                solucion2 = self.generarVecino(
                    solucion, problema.nDemanda, problema.nVehiculos, problema.restriccionCapacidad, problema.restriccionCompatibilidad, math.ceil(problema.nDemanda))
                print("\t\tSOlucion cantidata {} = {}".format(solucion2, problema.funcionObjetivo(
                    solucion2)))
                
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
            print("d{} | v{}".format(i+1, s+1))
        print(problema.funcionObjetivo(solucion))
