import PyPDF2
import threading

def extraer_pagina(lector, num_pagina, resultados):
    """Extrae texto de una página específica y lo guarda en una lista de resultados."""
    texto = lector.pages[num_pagina].extract_text()
    resultados[num_pagina] = texto

def extraer_texto_multihilo(pdf_path):
    """Extrae el texto de un archivo PDF utilizando múltiples hilos."""
    with open(pdf_path, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        num_paginas = len(lector.pages)
        resultados = ["" for _ in range(num_paginas)]
        hilos = []
        
        for i in range(num_paginas):
            hilo = threading.Thread(target=extraer_pagina, args=(lector, i, resultados))
            hilos.append(hilo)
            hilo.start()
        
        for hilo in hilos:
            hilo.join()
        
    return "\n".join(resultados)

def main():
    pdf_path = "oposiciones.pdf"  # Se usa directamente el archivo
    texto = extraer_texto_multihilo(pdf_path)
    print("\nTexto extraído:\n", texto)

if __name__ == "__main__":
    main()