import pandas as pd

excel = pd.ExcelFile("D:\Escritorio\Repocomun\Tarea 7 (Leer excel)\Lista URLs de Oposiciones.xlsx")

# Leer las columnas y la primera fila de cada hoja
def print_sheet_summary():
    for sheet_name in excel.sheet_names: # Recorrer las hojas
        df = excel.parse(sheet_name, nrows=1)  # Leer solo la primera fila
        print(f"\nHoja: {sheet_name}")
        print("Columnas:", df.columns.tolist())
        if not df.empty:
            print("Primera fila:", df.iloc[0].tolist())

print_sheet_summary()