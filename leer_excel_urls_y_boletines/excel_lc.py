import pandas as pd
import re
from openpyxl import Workbook
from datetime import datetime
import os

#PREGUNTAR: que columna tomar para los enlaces


#ver que filas no tienen URL o boletín
def sheets(sheet_name, df):    
    #lista para almacenar las filas en las que faltan la URL o el boletín
    missing_data = []

    #iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        enlaces = row.get('Enlace si hay')
        url_missing = pd.isna(row.get('Enlace si hay')) or not re.match(r'^https?://', str(enlaces)) #isna := Detect missing values for an array-like object.
        boletin_missing = pd.isna(row.get('Boletín'))

        if url_missing or boletin_missing:
            #info que falta
            row_data = row.to_dict() #clave=nombre columna, valor= valor celda
            row_data['Falta la URL'] = "Sí" if url_missing else ""
            row_data['Falta el boletín'] = "Sí" if boletin_missing else ""
            missing_data.append(row_data)


    #filas faltantes en un DataFrame
    if missing_data:
        return pd.DataFrame(missing_data)
    return None


def main():
    excel_path = 'C:/Users/Erica/Documents/GitHub/Semanas-FCT/4_Cuarta-Semana/8_Tarea/Lista URLs de Oposiciones.xlsx'
    new_excel = f"Nuevo_Excel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    new_path = os.path.join(os.path.dirname(excel_path), new_excel)

    #cargar archivo excel
    excel_data = pd.ExcelFile(excel_path)

    #diccionario para almacenar los resultados por hoja
    results = {}

    sheet_names = excel_data.sheet_names

    for sheet_name in sheet_names:
        df = excel_data.parse(sheet_name)
       #procesar hojas para obtener las filas con datos faltantes
        read_data = sheets(sheet_name, df)
        if read_data is not None:
            results[sheet_name] = read_data

    #buena prática cerrar el excel después de procesarlo
    excel_data.close()


    #archivo excel nuevo para guardar los resultados
    with pd.ExcelWriter(new_path, engine='openpyxl') as writer:
        for sheet_name, df in results.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)             




if __name__ == '__main__':
    main()

"""
!= no es adecuado--> is not
"""