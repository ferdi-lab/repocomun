import os
import re
import time
import requests
import threading
from uuid import uuid4
from datetime import datetime
import pandas as pd
from pypdf import PdfReader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------- Configuración de Excel --------
resultados = []  # Aquí guardamos resultados para luego exportar

fecha_actual = datetime.now().strftime("%Y-%m-%d")
archivo_excel = f"oposiciones_{fecha_actual}.xlsx"

# -------- Utilidades Comunes --------
def descargar_pdf(url, nombre_archivo):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        with open(nombre_archivo, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error al descargar PDF desde {url}: {e}")
        return False

def extraer_texto_pdf(ruta_pdf):
    contenido = ""
    try:
        with open(ruta_pdf, 'rb') as archivo:
            reader = PdfReader(archivo)
            for pagina in reader.pages:
                texto = pagina.extract_text()
                if texto:
                    contenido += texto
    except Exception as e:
        print(f"Error al leer el PDF {ruta_pdf}: {e}")
    return contenido

def buscar_oposiciones(contenido, origen):
    coincidencias = re.findall(r'Oposiciones+', contenido, re.IGNORECASE)
    print(f"[{origen}] Resultados: {coincidencias}")
    resultados.append({
        "Fuente": origen,
        "Coincidencias": len(coincidencias),
        "Palabras encontradas": ", ".join(coincidencias) if coincidencias else "-"
    })

# -------- Funciones Principales --------
def extraer_boletin(url):
    nombre_pdf = f"boletin_{uuid4().hex}.pdf"
    if descargar_pdf(url, nombre_pdf):
        texto = extraer_texto_pdf(nombre_pdf)
        buscar_oposiciones(texto, url)
        os.remove(nombre_pdf)

def procesar_comunidades(urls):
    for url in urls:
        extraer_boletin(url)

def procesar_selenium(chromedriver_path, download_path, urls_y_xpaths):
    service = Service(executable_path=chromedriver_path)
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    })
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=service, options=options)

    try:
        for url, xpath in urls_y_xpaths:
            try:
                driver.get(url)
                wait = WebDriverWait(driver, 10)
                boton = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                boton.click()
                time.sleep(5)
            except Exception as e:
                print(f"Error al interactuar con {url}: {e}")
    finally:
        driver.quit()

    for archivo in os.listdir(download_path):
        if archivo.endswith('.pdf'):
            ruta_pdf = os.path.join(download_path, archivo)
            texto = extraer_texto_pdf(ruta_pdf)
            buscar_oposiciones(texto, archivo)
            os.remove(ruta_pdf)

# --------- Datos ---------
url_boe = 'https://www.boe.es/boe/dias/2025/03/28/pdfs/BOE-S-2025-75.pdf'

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

chromedriver_path = 'C:\\Users\\alexd\\Desktop\\oposiciones programa\\chromedriver-win64\\chromedriver.exe'
download_path = 'C:\\Users\\alexd\\Descargas'

urls_y_xpaths = [
    ("https://www.caib.es/eboibfront/ES/2025/12077/?lang=es", "//img[@src='/eboibfront/img/ico/ico_pdf.gif']"),
    ("https://bon.navarra.es/es/inicio", "//a[@class='pdf-link-a']"),
    ("https://www.gobiernodecanarias.org/boc/archivo/2025/070/", "//a[@href='https://sede.gobiernodecanarias.org/boc/boc-s-2025-070.pdf']"),
    ("https://bomemelilla.es/ultimo", "//a[@title='Descargar BOME-B-2025-6267']")
]

# --------- Ejecutar en Paralelo ---------
hilo_boe = threading.Thread(target=extraer_boletin, args=(url_boe,))
hilo_comunidades = threading.Thread(target=procesar_comunidades, args=(urls_comunidades,))
hilo_selenium = threading.Thread(target=procesar_selenium, args=(chromedriver_path, download_path, urls_y_xpaths))

hilo_boe.start()
hilo_comunidades.start()
hilo_selenium.start()

hilo_boe.join()
hilo_comunidades.join()
hilo_selenium.join()

# -------- Guardar en Excel --------
df = pd.DataFrame(resultados)
df.to_excel(archivo_excel, index=False)
print(f"\n✅ Resultados guardados en {archivo_excel}")
