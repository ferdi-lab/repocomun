import pandas as pd #para leer excel
import os 
from datetime import datetime
import re
from tkinter import Tk #interfaz gráfica
from tkinter.filedialog import askopenfilename, askdirectory

#Excel a uasr
excel_path = "C:/Users/Erica/Documents/GitHub/Semanas-FCT/4_Cuarta-Semana/7_Tarea/Lista URLs de Oposiciones.xlsx"
# excel = pd.ExcelFile("Lista URLs de Oposiciones.xlsx") 
#palabras clave
keywords = [
    r"\bbomberos\b"
]

#leer el archivo excel hoja por hoja
pages = pd.read_excel(excel_path, sheet_name=None) #con pandas, sheet_name=None hace que devuelva un diccionario con todas las hojas, en caso de querer leer una hoja específica, sheet_name="Tatata"

#para guardar los resultados
results = []

for sheets, info in pages.items(): #lee hoja por hoja
    if not isinstance(info, pd.DataFrame): #isinstance(): toma dos argumentos: un objeto y una clase o tipo. Devuelve True si el objeto es una instancia de la clase o de una subclase de ella, sino False. Es decir, que sea válida nuestra tabla o no
        continue #continua si no es una hoja válida
# no sé si realmente es lo que se quiere usar aquí
#iteramos sobre cada fila de un DataFrame; para cada celda intenta convertir un valor a texto y verifica si alguna coincide con las palabras clave. 
    for index, row in info.iterrows(): #iterrows: método que se llama en DataFrame; devuelve un iterador que produce pares de índice-fila. En cada interacción devuelve una tupla donde el primer elemento es el índice de la fila y el segundo elemento es la fila como un objeto. Es decir, recorre las filas una por una
        for column in info.columns: #cada columna
            try:
                value = str(row[column]) #valor de la celda en texto para poder aplicarle las regexp, se guarda en value
                for regexp in keywords: #
                      if re.search(regexp, value, flags=re.IGNORECASE):
                          results.append({
                              "Hoja": sheets,
                              "Fila": index + 1,
                              "Columna": column,
                              "Valor": value
                              })
            except: #por si algo salió mal, lo ignora
                continue #pasa al siguiente


#crea un DataFrame con los resultados encontrados 
results_pd = pd.DataFrame(results)

#creación de nuevo excel
new_excel = f"Nuevo_Excel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx" #creación del nuevo excel, con la fecha y hora en el título
new_path = os.path.join(os.path.dirname(excel_path), new_excel) #se guarda automáticamente en la misma carpeta que el excel original


#No me da tiempo
#guardar el nuevo excel con los resultados de la búsqueda
with pd.ExcelWriter(new_path, engine="openpyxl") as writer: #escribe los resultados en una hoja vacía por cada hoja original --> ChatGPT, buscar más
    for sheets, info in pages.items():
        new_info = pd.DataFrame(columns=info.columns) #la misma hoja pero vacía(?)
        new_info.to_excel(writer, sheet_name=sheets, index=False)

    if not results_pd.empty:
        results_pd.to_excel(writer, sheet_name="Resultados", index=False)

"""
Falta:
- La aparición de la info requerida en el nuevo excel ->lector PDF(?)
- Tema de guardar y crear un nuevo excel, aprender y entenderlo
- Crear interfaz: al iniciarla que pida introducir las palabras clave, y que todo aparezca dentro de la propia interfaz(?).
"""