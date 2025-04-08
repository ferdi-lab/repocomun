import pandas as pd

# Cargar el archivo
xlsx = pd.ExcelFile("D:\Escritorio\Repocomun\Tarea 9 (palabras clave)\Lista URLs de Oposiciones.xlsx")

# Hojas que tienen la columna "Puesto"
hojas_con_puesto = ['PSV', 'OPSO', 'BIT', 'OARC']

# Extraer las filas de la columna "Puesto"
puestos = {}

for hoja in hojas_con_puesto:
    df = xlsx.parse(hoja)
    puestos[hoja] = df["Puesto"].dropna().tolist()

# Ejemplo: imprimir los puestos de la hoja "PSV"
print("Puestos en hoja PSV:")
for puesto in puestos["PSV"]:
    print(puesto)