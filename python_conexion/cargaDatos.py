from flask import Flask, render_template
import sys
import io
import requests
from bs4 import BeautifulSoup
import re  # Para manejar expresiones regulares
import sqlite3

# Configurar salida estándar para usar UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ahora puedes imprimir texto con caracteres especiales sin problemas
print("Texto con caracteres especiales ′")

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect('wikipediaDB.sql')
cursor = conn.cursor()

# Crear la tabla "paises"
cursor.execute('''
CREATE TABLE IF NOT EXISTS paises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);
''')
conn.commit()  # Confirmamos la creación de la tabla

# Crear la tabla "contenido_extraido"
cursor.execute('''
CREATE TABLE IF NOT EXISTS contenido_extraido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pais_id INTEGER NOT NULL,
    superficie TEXT,
    poblacion TEXT,
    pib_ppa TEXT,
    FOREIGN KEY (pais_id) REFERENCES paises(id) ON DELETE CASCADE
);
''')
conn.commit()  # Confirmamos la creación de la tabla

def extraer_datos_wikipedia():
    url = 'https://es.wikipedia.org/wiki/Alemania'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraer el título de la página
    titulo = soup.find('h1', {'id': 'firstHeading'}).text.strip()

    # Buscar la tabla con información
    tabla_info = soup.find('table', {'class': 'infobox'})

    # Diccionario para almacenar los datos
    datos = {
        "Nombre del país": titulo,
        "Superficie": "No disponible",
        "Población": "No disponible",
        "PIB (PPA)": "No disponible"
    }

    if tabla_info:
        print("Tabla encontrada.")  # Confirmar que se encontró la tabla
        for fila in tabla_info.find_all('tr'):
            encabezado = fila.find('th')
            contenido = fila.find('td')

            if encabezado and contenido:
                encabezado_texto = encabezado.get_text(strip=True)
                contenido_texto = contenido.get_text(strip=True)

                # Imprimir encabezado y contenido para depuración
                print(f"Encabezado: {encabezado_texto}")  # Ver encabezado
                print(f"Contenido: {contenido_texto}")  # Ver contenido

                # Buscar la superficie utilizando expresiones regulares
                if re.search(r'(Superficie|Área)', encabezado_texto, re.IGNORECASE):
                    datos["Superficie"] = contenido_texto
                elif re.search(r'Población', encabezado_texto, re.IGNORECASE):
                    datos["Población"] = contenido_texto
                elif re.search(r'PIB', encabezado_texto, re.IGNORECASE):
                    datos["PIB (PPA)"] = contenido_texto

    # Imprimir los datos para verificar
    #print(datos)

    return datos

# Función para guardar los datos extraídos en la base de datos
def guardar_en_bd(datos):
    # Insertar país y obtener su ID
    cursor.execute("INSERT OR IGNORE INTO paises (nombre) VALUES (?)", (datos["Nombre del país"],))
    conn.commit()

    # Obtener el ID del país insertado
    cursor.execute("SELECT id FROM paises WHERE nombre = ?", (datos["Nombre del país"],))
    pais_id = cursor.fetchone()[0]

    # Insertar los datos extraídos en la tabla contenido_extraido
    cursor.execute('''
    INSERT INTO contenido_extraido (pais_id, superficie, poblacion, pib_ppa) 
    VALUES (?, ?, ?, ?)
    ''', (pais_id, datos["Superficie"], datos["Población"], datos["PIB (PPA)"]))
    conn.commit()

    print("Datos guardados correctamente en la base de datos.")

# Ejecutar la extracción de datos y guardarlos en la base de datos
datos = extraer_datos_wikipedia()
guardar_en_bd(datos)

#query = cursor.execute("select * from paises")
#print(query.description)
#cols = [column[0] for column in query.description]
#print(cols)

# Cerrar la conexión
conn.close()



#------------------------------------Flask app------------------------------------

app = Flask(__name__)

@app.route('/')
def home():
    # Extraer datos de Wikipedia
    datos = extraer_datos_wikipedia()
    return render_template('index.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
