import argparse
import utils as problemaDe
import estrategias as strg
import yaml


def main():
    # Ubicación de directorio con los parámetros del problema y los parámetros del SA
    confDir = "conf_files\\"
    parser = argparse.ArgumentParser(
        description='Procesa los path de los archivos a los parámetros')
    parser.add_argument(
        "confInput", help="Archivo de configuración para parámetros de simulated annealing")
    parser.add_argument(
        "confSA", help="Archivo de configuración para parámetros de simulated annealing")
    args = parser.parse_args()

    # Carga de datos del problema y ejecución del programa
    with open(confDir+args.confInput, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    nVehiculos = cfg["nVehiculos"]
    nDemandas = cfg["nDemandas"]
    costos = cfg["costos"]
    carga = cfg["carga"]
    capacidades = cfg["capacidad"]
    incompatibilidades = cfg.get("incompatibilidad", None)
    graph = cfg["graph"]

    # Carga de parámetros de para SA
    with open(confDir+args.confSA, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    alpha = cfg["alpha"]
    temperaturaMin = cfg["temperaturaMin"]
    temperaturaMax = cfg["temperaturaMax"]
    threshold = cfg["threshold"]
    iteraciones = cfg["iteraciones"]
    nBsize = cfg["nBsize"]

    # Instancia del solver a utilizar
    templadoSimulador = strg.SA(
        alpha, temperaturaMin, temperaturaMax, threshold, iteraciones, nBsize)
    # Instancia del problema a resolver
    problema = problemaDe.asignacion(costos, carga,
                                     capacidades, nVehiculos, nDemandas, templadoSimulador, incompatibilidades)
    # Resolución del problema
    problema.resolver()
    if graph:
        problema.graficar()


if __name__ == "__main__":
    main()
