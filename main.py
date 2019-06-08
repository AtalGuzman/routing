import argparse
import utils


def main():
    # Obtención de parámetros línea de comando
    parser = argparse.ArgumentParser(
        description='Procesa los path de los archivos a los parámetros')
    parser.add_argument(
        "Costos",  help="Directorio dónde está el archivo de costos")
    parser.add_argument(
        "Carga", help="Directorio dónde está el archivo de carga de cada demanda")
    parser.add_argument(
        "Capacidades", help="Directorio dónde está el archivo de capacidades de los vehículos")
    parser.add_argument("-I", "--incompatibilidades",
                        help="Archivo opcional con las incompatibilidades entre las demas")
    args = parser.parse_args()

    problema = utils.asignacion(args.Costos, args.Carga,
                                args.Capacidades, args.incompatibilidades)


if __name__ == "__main__":
    main()
