import requests
import re
import os
import time
from pypdf import PdfReader
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Definir función para extraer BOE
def extraer_BOE(url):
    # Hacer la petición a la URL
    boe = requests.get(url)

    # Descargar y crear archivo pdf
    with open('BOE-Prueba.pdf', 'wb') as f:
        f.write(boe.content)

    # Abrir y leer el texto del PDF
    with open('BOE-Prueba.pdf', 'rb') as archivo:
        leer_pdf = PdfReader(archivo)
        contenido = ""

        # Iterar cada página y extraer la información en formato texto
        for pagina in leer_pdf.pages:
            contenido += pagina.extract_text()

        # Utilizar expresiones regulares para buscar una palabra en el texto
        oposiciones = re.findall(r'Oposiciones+', contenido, re.IGNORECASE)

        # Imprimir resultados encontrados
        print(f'Resultados de {url}: {oposiciones}')

    # Borrar pdf
    if os.path.exists('BOE-Prueba.pdf'):
        os.remove('BOE-Prueba.pdf')

# Definir función para extraer oposiciones en comunidades
def oposiciones_comunidades(urls):
    for url in urls:
        respuesta = requests.get(url)

        # Guardar el contenido del PDF en un archivo
        with open('Comunidades-Prueba.pdf', 'wb') as f:
            f.write(respuesta.content)

        # Abrir y leer el texto del PDF
        with open('Comunidades-Prueba.pdf', 'rb') as texto_BOE:
            leer_pdf = PdfReader(texto_BOE)
            contenido = ""

            # Iterar cada página y extraer la información en formato texto
            for pagina in leer_pdf.pages:
                contenido += pagina.extract_text()

            # Utilizar expresiones regulares para buscar una palabra en el texto
            oposiciones = re.findall(r'Oposiciones+', contenido, re.IGNORECASE)

            # Imprimir resultados encontrados
            print(f'Resultados de {url}: {oposiciones}')

        # Borrar pdf
        if os.path.exists('Comunidades-Prueba.pdf'):
            os.remove('Comunidades-Prueba.pdf')

# Definir función para extraer oposiciones usando Selenium
def descargar_y_leer_pdfs(chromedriver_path, download_path, urls_y_xpaths):
    service = Service(executable_path=chromedriver_path)
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=service, options=chrome_options)

    for url, xpath in urls_y_xpaths:
        driver.get(url)
        time.sleep(3)

        download_button = driver.find_element(By.XPATH, xpath)
        time.sleep(3)
        download_button.click()
        time.sleep(5)  

    driver.quit()

    # Leer todos los archivos PDF en la carpeta de descargas
    for archivo in os.listdir(download_path):
        if archivo.endswith('.pdf'):
            with open(os.path.join(download_path, archivo), 'rb') as texto_BOE:
                leer_pdf = PdfReader(texto_BOE)
                contenido = ""

                for pagina in leer_pdf.pages:
                    contenido += pagina.extract_text() if pagina.extract_text() else ""

                oposiciones = re.findall(r'Oposiciones+', contenido, re.IGNORECASE)
                print(f"Resultados en {archivo}: {oposiciones}")

            os.remove(os.path.join(download_path, archivo))

# URL para el BOE, puede haber más de una
url_BOE ='https://www.boe.es/boe/dias/2025/03/28/pdfs/BOE-S-2025-75.pdf'


# Lista de URLs para oposiciones_comunidades 
urls_comunidades = [
    'https://www.xunta.gal/dog/Publicados/2025/20250409/Indice69_gl.pdf',
    'https://sede.asturias.es/bopa/2025/04/09/20250409.pdf',
    'https://boc.cantabria.es/boces/verPdfAction.do?idBlob=39943&tipoPdf=0',
    'https://www.euskadi.eus/web01-bopv/es/bopv2/datos/2025/04/s25_0069.pdf',
    'https://ias1.larioja.org/boletin/Bor_Boletin_visor_Servlet?referencia=34191265-2-X',
    'https://www.boa.aragon.es/cgi-bin/EBOA/BRSCGI?CMD=VEROBJ&MLKOB=1387843610202',
    'https://bocyl.jcyl.es/boletines/2025/04/09/pdf/BOCYL-S-09042025.pdf',
    'https://www.bocm.es/boletin/CM_Boletin_BOCM/2025/04/09/08400.PDF',
    'https://docm.jccm.es/docm/descargarArchivo.do?ruta=2025/04/04/pdf/docm_66.pdf&tipo=rutaDocm',
    'https://doe.juntaex.es/pdfs/doe/2025/690o/690o.pdf',
    'https://dogv.gva.es/datos/2025/04/09/pdf/dogv_2025_10084_es.pdf',
    'https://www.borm.es/services/boletin/ano/2025/numero/82/pdf',
    'https://www.juntadeandalucia.es/eboja/2025/68/BOJA25-068-00013_10000038.pdf',
    'https://www.ceuta.es/ceuta/component/jdownloads/finish/1954-abril/22784-bocce-extra14-08-04-2025?Itemid=534'
]

# Lista de URls usando Selenium
chromedriver_path = 'C:\\Users\\LAB Masas\\Desktop\\BOE\\chromedriver.exe'
download_path = 'C:\\Users\\LAB Masas\\Desktop\\Descargas\\'
urls_y_xpaths = [
    ("https://www.caib.es/eboibfront/ES/2025/12077/?lang=es", "//img[@src='/eboibfront/img/ico/ico_pdf.gif']"),
    ("https://bon.navarra.es/es/inicio", "//a[@class='pdf-link-a']"),
    ("https://www.gobiernodecanarias.org/boc/archivo/2025/070/", "//a[@href='https://sede.gobiernodecanarias.org/boc/boc-s-2025-070.pdf']"),
    ("https://bomemelilla.es/ultimo", "//a[@title='Descargar BOME-B-2025-6267']")
]

# Hilos para ejecutar las funciones
hilo_oposiciones = threading.Thread(target=extraer_BOE, args=(url_BOE,))
hilo_comunidades = threading.Thread(target=oposiciones_comunidades, args=(urls_comunidades,))
hilo_comunidades_selenium = threading.Thread(target=descargar_y_leer_pdfs, args=(chromedriver_path, download_path, urls_y_xpaths))

# Iniciar hilos
hilo_oposiciones.start()
hilo_comunidades.start()
hilo_comunidades_selenium.start()

# Esperar a que terminen
hilo_oposiciones.join()
hilo_comunidades.join()
hilo_comunidades_selenium.join()