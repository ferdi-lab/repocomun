import requests
import re
import os
from pypdf import PdfReader
import threading

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

# URL para el BOE, puede haber más de una
url_BOE ='https://www.boe.es/boe/dias/2025/03/28/pdfs/BOE-S-2025-75.pdf'


# Lista de URLs para oposiciones_comunidades 
urls_comunidades = [
    'https://www.xunta.gal/dog/Publicados/2025/20250331/AnuncioG0767-250325-0006_gl.pdf',
    'https://www.juntadeandalucia.es/eboja/2025/47/BOJA25-047-00213-3298-01_00316903.pdf',
    'https://www.borm.es/services/boletin/ano/2025/numero/74/pdf',
    'https://doe.juntaex.es/pdfs/doe/2025/620o/620o.pdf',
    'https://dogv.gva.es/datos/2025/03/31/pdf/sumario_2025_10077_es.pdf',
    'https://www.bocm.es/boletin/CM_Boletin_BOCM/2025/03/31/BOCM-20250331076.PDF',
    'https://bocyl.jcyl.es/boletines/2025/03/31/pdf/BOCYL-S-31032025.pdf',
    'https://www.boa.aragon.es/cgi-bin/EBOA/BRSCGI?CMD=VEROBJ&MLKOB=1386037320303',
    'https://boc.cantabria.es/boces/verPdfAction.do?idBlob=39803&tipoPdf=0'
]

# Hilos para ejecutar las funciones
hilo_oposiciones = threading.Thread(target=extraer_BOE, args=(url_BOE,))
hilo_comunidades = threading.Thread(target=oposiciones_comunidades, args=(urls_comunidades,))

# Iniciar hilos
hilo_oposiciones.start()
hilo_comunidades.start()

# Esperar a que terminen
hilo_oposiciones.join()
hilo_comunidades.join()