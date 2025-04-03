#Importar bibliotecas requests, BeautifulSoup y base de datos SQLITE
from openpyxl import workbook
from openpyxl import load_workbook
import sqlite3


#Abrir el archivo Excel
wb= load_workbook('Lista URLs de Oposiciones.xlsx')
ws = wb.active
ws = wb['ListaURLS']

#Interacion de las columnas
iteracion = ws.iter_rows(min_row=1, max_row=20, min_col=1, max_col=2)

#Declarar variables para almacenar datos
comunidad_autonoma= []
url_BOE= []

#Recorrer la iteración y almacenar datos en la variables
for a,b in iteracion:
    comunidad_autonoma.append(a.value)
    url_BOE.append (b.value)
    
#Impirmir resultados
print (comunidad_autonoma)
print (url_BOE)


