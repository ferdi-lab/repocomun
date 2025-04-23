# Importar bibliotecas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
import os
from pypdf import PdfReader

# Diseñar chromedriver y su ejecución
service = Service(executable_path='C:\\Users\\LAB Masas\\Desktop\\BOE\\chromedriver.exe')
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "C:\\Users\\LAB Masas\\Desktop\\Descargas\\",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Crear objeto de webdriver
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.caib.es/eboibfront/ES/2025/12077/?lang=es")
time.sleep(3)

# Encontrar y hacer clic en el botón de descarga
download_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div/div/div/nav/div/div[2]/ul/li/ul/li[1]/a")
time.sleep(3)
download_button.click()
time.sleep(5)

# Cerrar driver
driver.quit()

# Esperar a que el archivo se descargue
time.sleep(5)

# Leer todos los archivos PDF en la carpeta de descargas
descargas_path = 'C:\\Users\\LAB Masas\\Desktop\\Descargas\\'
for archivo in os.listdir(descargas_path):
    if archivo.endswith('.pdf'):
        with open(os.path.join(descargas_path, archivo), 'rb') as texto_BOE:
            leer_pdf = PdfReader(texto_BOE)
            # Iterar cada página y extraer la información en formato texto
            contenido = ""
            for pagina in leer_pdf.pages:
                contenido += pagina.extract_text() if pagina.extract_text() else ""

            # Utilizar expresiones regulares para buscar una palabra en el texto
            oposiciones = re.findall(r'Oposiciones+', contenido, re.IGNORECASE)

            # Imprimir resultados encontrados
            print(f"Resultados en {archivo}: {oposiciones}")

# Borrar pdf
os.remove(os.path.join(descargas_path, archivo))