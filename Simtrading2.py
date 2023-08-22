import datetime
import os
from Scanner import Scanner
from Chart import Chart
from multiprocessing import Pool
import sys

 

def proceso_graficar(scanner, fecha_inicial):
    # Crear un objeto de gráfico
    chart = Chart(scanner)
    # Graficar velas japonesas
    chart.graficar_velas_japonesas(fecha_inicial)

 

def main():
    # sys.argv[0] es el nombre del script en sí mismo, los argumentos comienzan desde sys.argv[1]
    parsed_args = {"-p": None, "-f": None, "-m": None}    

 

    if len(sys.argv) > 3:
        for arg in sys.argv:
            if arg.startswith("-p="):
                parsed_args["-p"] = arg.split("=")[1]
            elif arg.startswith("-f="):
                parsed_args["-f"] = arg.split("=")[1]
            elif arg.startswith("-m="):
                parsed_args["-m"] = arg.split("=")[1]

 

    else:
        print("Se necesitan al menos 3 argumentos.")
        return(1)

 

    scanner = Scanner()
    nombre_archivo = f"{parsed_args['-m']}_{parsed_args['-p']}.{parsed_args['-f'].lower()}"

 

    if parsed_args["-f"] == "CSV":
        ruta = os.path.join('.\\MonedasCSV', nombre_archivo)
        scanner.leer_csv(ruta)
    elif parsed_args["-f"] == "JSON":
        ruta = os.path.join('.\\MonedasJSON', nombre_archivo)
        scanner.leer_json(ruta)
    else:
        print("Formato de archivo NO valido.")
        return(1)

 

    # Definir fecha inicial
    fecha_inicial = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")

    # Paralelizar el proceso de graficación
    with Pool() as pool:
        pool.apply(proceso_graficar, args=(scanner, fecha_inicial))

 

if __name__ == "__main__":
    main()