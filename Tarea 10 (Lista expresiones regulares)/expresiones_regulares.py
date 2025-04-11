import re
from PyPDF2 import PdfReader

pdf_path = "D:\Escritorio\Repocomun\Tarea 10 (Lista expresiones regulares)\BOCM-20211203-12.pdf"
reader = PdfReader(pdf_path)

# Expresiones regulares a buscar
palabras_clave = ["convocatoria", "oposición", "requisitos", "conductor"]

# Extraer texto de todas las páginas y buscar las expresiones
resultados = {palabra: [] for palabra in palabras_clave}

for num_pagina, pagina in enumerate(reader.pages):
    text = pagina.extract_text()
    if text:
        for palabra in palabras_clave:
            if re.search(rf"\b{palabra}\b", text, re.IGNORECASE):
                resultados[palabra].append(num_pagina + 1)

print(resultados)