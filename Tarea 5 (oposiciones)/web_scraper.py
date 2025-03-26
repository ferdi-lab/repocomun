import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd


# Leer el excel
archivo = 'D:\Escritorio\Repositorio1\Tarea 5 (oposiciones)\TablaAyuntamientosOposiciones.xlsx'
df = pd.read_excel(archivo, sheet_name='Hoja 1')
print(df)

# Crear la base de datos
conn = sqlite3.connect('ayuntamientos.db')
cursor = conn.cursor()

# Crear la tabla de los ayuntamientos
cursor.execute("""
CREATE TABLE IF NOT EXISTS Ayuntamientos (
    nombre TEXT,
    url TEXT,
    coordenadas TEXT PRIMARY KEY
);
""")

# Insertar los datos en la tabla
df.to_sql("Ayuntamientos", conn, if_exists="replace", index=False)

conn.commit()
conn.close()




# Scraper

url = "https://www.malaga.eu/el-ayuntamiento/ofertas-de-empleo-publico/ayuntamiento-de-malaga/"

resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

# Encontrar todas las secciones de oposiciones
oposiciones = []
año = None

# Buscar las convocatorias por año y sus respectivas oposiciones
for element in soup.find_all(["div", "h3"], class_=["brand-color", "item-title"]):
    if element.name == "div" and "brand-color" in element.get("class", []):
        año = element.text.strip().replace("OEP ", "")
    elif element.name == "h3" and "item-title" in element.get("class", []):
        oposicion = element.text.strip()
        if año:
            oposiciones.append((oposicion, año)) #crear lista con los datos de cada oposición



# Crear la base de datos
conn = sqlite3.connect('oposiciones.db')

c = conn.cursor()

# Crear la tabla de las oposiciones
c.execute("""
CREATE TABLE IF NOT EXISTS oposiciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Oposición TEXT NOT NULL,
    Año TEXT NOT NULL
)
""")

# Insertar los datos
c.executemany("INSERT INTO oposiciones (Oposición, año) VALUES (?, ?)", oposiciones)

conn.commit()
conn.close()