import pandas as pd

excel = pd.ExcelFile("D:\Escritorio\Repocomun\Lista URLs de Oposiciones.xlsx")

# Obtener nombres de las hojas
sheet_names = excel.sheet_names

# Extraer la columna 'Enlace general sgto' de todas las hojas menos la última
enlace_data = {}

for sheet in sheet_names[:-1]:  # Excluir la última hoja
    df = excel.parse(sheet)
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