# Importar bibliotecas
import requests
import re
import os
from pypdf import PdfReader

# definir función
def extraer_oposiciones(urls):
    for url in urls:
        print(f"Procesando URL: {url}")
        
        # Hacer la petición a la URL
        boe = requests.get(url)

        # Descargar y crear archivo pdf
        pdf_filename = 'BOE-Prueba.pdf'
        with open(pdf_filename, 'wb') as f:
            f.write(boe.content)

        # Abrir y leer el texto del PDF
        with open(pdf_filename, 'rb') as archivo:
            leer_pdf = PdfReader(archivo)
            contenido = ""

            # Iterar cada página y extraer la información en formato texto
            for pagina in leer_pdf.pages:
                contenido += pagina.extract_text()

        # Utilizar expresiones regulares para buscar una palabra en el texto
        oposiciones = [frase.strip() for frase in re.findall(r'[^.!?]*\boposiciones\b[^.!?]*[.!?]', contenido, re.IGNORECASE)]
        plaza = [frase.strip() for frase in re.findall(r'[^.!?]*\bplaza\b[^.!?]*[.!?]', contenido, re.IGNORECASE)]
        convocatoria = [frase.strip() for frase in re.findall(r'[^.!?]*\bconvocatoria\b[^.!?]*[.!?]', contenido, re.IGNORECASE)]

        # Imprimir resultados encontrados
        print("Frases con 'oposiciones':")
        for frase in oposiciones:
            print(f"  - {frase}")
        print("\nFrases con 'bases':")
        for frase in plaza:
            print(f"  - {frase}")
        print("\nFrases con 'convocatoria':")
        for frase in convocatoria:
            print(f"  - {frase}")

        # Borrar pdf
        os.remove(pdf_filename)

# Ejemplo de uso de la función
urls = [
    'https://www.boe.es/boe/dias/2025/03/28/pdfs/BOE-S-2025-75.pdf',
    'https://www.boe.es/boe/dias/2025/04/11/pdfs/BOE-S-2025-88.pdf'
]
extraer_oposiciones(urls)
