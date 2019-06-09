import argparse
import utils
import estrategias as strg
import yaml

def main():
    # Obtención de parámetros línea de comando
    parser = argparse.ArgumentParser(
        description='Procesa los path de los archivos a los parámetros')
    parser.add_argument("nVehiculos", help="Numero de vehiculso a usar", type=int)
    parser.add_argument("nDemadas", help="Número de demandas por satisfacer", type=int)
    parser.add_argument(
        "Costos",  help="Directorio dónde está el archivo de costos")
    parser.add_argument(
        "Carga", help="Directorio dónde está el archivo de carga de cada demanda")
    parser.add_argument(
        "Capacidades", help="Directorio dónde está el archivo de capacidades de los vehículos")
    parser.add_argument("configuracion", help = "Archivo de configuración para parámetros de simulated annealing")
    parser.add_argument("-I", "--incompatibilidades",
                        help="Archivo opcional con las incompatibilidades entre las demas")
    
    args = parser.parse_args()
    with open(args.configuracion, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    alpha = cfg["alpha"]
    temperaturaMin = cfg["temperaturaMin"]
    temperaturaMax = cfg["temperaturaMax"]
    threshold = cfg["threshold"]
    iteraciones = cfg["iteraciones"]
    
    #Por ejemplo, un templado simulado, pero no es 100% seguro que lo use
    templadoSimulador = strg.SA(alpha, temperaturaMin, temperaturaMax, threshold, iteraciones)
    problema = utils.asignacion(args.Costos, args.Carga,
                                args.Capacidades, args.nVehiculos, args.nDemadas, templadoSimulador, args.incompatibilidades)
    problema.resolver()
if __name__ == "__main__":
    main()