import pandas as pd

xls = pd.ExcelFile("D:\Escritorio\Repocomun\Tarea 8 (Leer excel 2)\Lista URLs de Oposiciones.xlsx")

# Obtener nombres de las hojas
sheet_names = xls.sheet_names

# Extraer la columna 'Enlace general sgto' de todas las hojas menos la última
enlace_data = {}

for sheet in sheet_names[:-1]:  # Excluir la última hoja
    df = xls.parse(sheet)
    if 'Enlace general sgto' in df.columns:
        enlace_data[sheet] = df[['Enlace general sgto']]

# Combinar en un solo DataFrame
enlaces = pd.concat(enlace_data.values(), keys=enlace_data.keys())
enlaces.reset_index(level=0, inplace=True)
enlaces.rename(columns={'level_0': 'Hoja'}, inplace=True)

# Guardar en un nuevo archivo Excel
output_path = "enlaces_generales.xlsx"
enlaces.to_excel(output_path, index=False)

print(f"Archivo guardado en: {output_path}")