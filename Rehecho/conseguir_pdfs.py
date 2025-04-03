import requests
import re
from PyPDF2 import PdfReader
import os


# Descargar PDF desde URL
def download_pdf(url, file_path): 
    petition = requests.get(url)
    if petition.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(petition.content)
            print("Archivo descargado.")
    else:
        print(f"Error: {petition.status_code}")


# Leer el contenido del PDF
def search_pdf(file_path, pattern):
    if not os.path.exists(file_path):  # Verificar si el archivo existe
        print("Error")
        return False
    results = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            matches = re.findall(pattern, text, re.IGNORECASE)  
            if matches:
                results.extend(matches)
                print(results)
            else:
                print("No se ha encontrado nada.")
            return results


"""
Anotaciones:
Diferencias diccionarios de listas en python:
Diccionario:
   urls_comunidades = { 
    "Andalucia" : "a",
    "Madrid" : "b"
    }
    A los diccionarios se puede acceder directamente a la URL que necesito: urls_comunidades[Andalucia]
    No pueden tener valores duplicados, han de ser únicas.

Lista (de tuplas!)=
    urls_comunidades = `[ 
    ("Andalucia", "a"),
    ("Madrid", "b")
    ]
    Las listas mantienen el orden de inserción; es útil cuando hayy claves repetidas o se quiere almacenar
    más de un valor por clave.
"""