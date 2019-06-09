import argparse
import utils as problemaAsignacion
import estrategias as strg
import yaml


def main():
    parser = argparse.ArgumentParser(
        description='Procesa los path de los archivos a los parámetros')
    parser.add_argument(
        "confInput", help="Archivo de configuración para parámetros de simulated annealing")
    parser.add_argument(
        "confSA", help="Archivo de configuración para parámetros de simulated annealing")
    args = parser.parse_args()

    with open(args.confInput, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    nVehiculos = cfg["nVehiculos"]
    nDemandas = cfg["nDemandas"]
    costos = cfg["costos"]
    carga = cfg["carga"]
    capacidades = cfg["capacidad"]
    incompatibilidades = cfg.get("incompatibilidad", None)
    graph = cfg["graph"]

    with open(args.confSA, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    alpha = cfg["alpha"]
    temperaturaMin = cfg["temperaturaMin"]
    temperaturaMax = cfg["temperaturaMax"]
    threshold = cfg["threshold"]
    iteraciones = cfg["iteraciones"]
    nBsize = cfg["nBsize"]

    templadoSimulador = strg.SA(
        alpha, temperaturaMin, temperaturaMax, threshold, iteraciones, nBsize)
    problema = problemaAsignacion.asignacion(costos, carga,
                                             capacidades, nVehiculos, nDemandas, templadoSimulador, incompatibilidades)
    problema.resolver()
    if graph: problema.graficar()


if __name__ == "__main__":
    main()
