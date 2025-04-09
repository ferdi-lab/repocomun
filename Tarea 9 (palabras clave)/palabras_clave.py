import pandas as pd
import threading

# Ruta del archivo
ruta_archivo = "D:/Escritorio/Repocomun/Tarea 9 (palabras clave)/Lista URLs de Oposiciones.xlsx"

# Hojas que tienen la columna "Puesto"
hojas_con_puesto = ['PSV', 'OPSO', 'BIT', 'OARC']

# Cargar el archivo Excel una sola vez
xlsx = pd.ExcelFile(ruta_archivo)

# Función para procesar una hoja
def procesar_hoja(hoja):
    df = xlsx.parse(hoja)
    puestos = df["Puesto"].dropna().tolist()

    print(f"Hilo (thread) para la hoja: {hoja}")
    for puesto in puestos:
        print(f"[{hoja}] {puesto}")

# Crear y lanzar un hilo por cada hoja
hilos = []

for hoja in hojas_con_puesto:
    hilo = threading.Thread(target=procesar_hoja, args=(hoja,))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos los hilos terminen
for hilo in hilos:
    hilo.join()