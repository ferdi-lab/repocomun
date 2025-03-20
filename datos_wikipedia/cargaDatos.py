from flask import Flask, render_template
import sys
import io

# Configurar salida estándar para usar UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ahora puedes imprimir texto con caracteres especiales sin problemas
print("Texto con caracteres especiales ′")
import requests
from bs4 import BeautifulSoup
import re  # Para manejar expresiones regulares

app = Flask(__name__)

# En estos comentarios vamos a realizar pruebas de distintas url con paises distintos a ver que datos coge el programa
    # https://es.wikipedia.org/wiki/Espa%C3%B1a
    # https://es.wikipedia.org/wiki/Portugal
    # https://es.wikipedia.org/wiki/Francia
    # https://es.wikipedia.org/wiki/Alemania

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
        # Imprimir el contenido completo de la tabla para depuración
        print("Contenido de la tabla:")
        for fila in tabla_info.find_all('tr'):
            print(fila.text.strip())  # Imprime el contenido de cada fila de la tabla

        # Buscar las filas y extraer los datos
        for fila in tabla_info.find_all('tr'):
            encabezado = fila.find('th')
            contenido = fila.find('td')

            if encabezado and contenido:
                encabezado_texto = encabezado.get_text(strip=True)
                contenido_texto = contenido.get_text(strip=True)

                # Mostrar en consola para ver qué encabezados y contenidos estamos extrayendo
                print(f"Encabezado: {encabezado_texto}")
                print(f"Contenido: {contenido_texto}")

                # Buscar la superficie utilizando expresiones regulares más flexibles
                if re.search(r'(Superficie|Área).*total', encabezado_texto, re.IGNORECASE):
                    datos["Superficie"] = contenido_texto
                elif re.search(r'Superficie.*total', encabezado_texto, re.IGNORECASE):
                    datos[".Total"] = contenido_texto
                elif re.search(r'Población.*total', encabezado_texto, re.IGNORECASE):
                    datos["Población"] = contenido_texto
                elif re.search(r'PIB.*PPA', encabezado_texto, re.IGNORECASE):
                    datos["PIB (PPA)"] = contenido_texto

    return datos

@app.route('/')
def home():
    datos = extraer_datos_wikipedia()
    return render_template('index.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
