import requests
from bs4 import BeautifulSoup
import sqlite3

url = "https://es.wikipedia.org/wiki/Andorra"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Función para extraer datos de la tabla de información
def obtener_dato(soup, titulo):
    for row in soup.find_all("tr"):
        if row.find("th") and titulo in row.find("th").get_text():
            siguiente_fila = row.find_next_sibling("tr")
            if siguiente_fila:
                return siguiente_fila.find("td").get_text(strip=True)
    return "No encontrado"

# Extraer los datos requeridos
superficie = obtener_dato(soup, "Superficie")
población = obtener_dato(soup, "Población total")
pib = obtener_dato(soup, "PIB")


print("Superficie:", superficie)
print("Población:", población)
print("PIB:", pib)




# Crear la base de datos, la tabla e insertar los datos
conn = sqlite3.connect('datospaises.db')

c = conn.cursor()

# c.execute("""CREATE TABLE datospaises (
#     Superficie INTEGER,
#     Población INTEGER,
#     PIB INTEGER
# )""")


todos_paises = [
    (superficie, población, pib),
]

c.executemany("INSERT INTO datospaises VALUES (?, ?, ?)", todos_paises)

conn.commit()
conn.close()