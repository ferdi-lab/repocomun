import fitz
import re
import threading


boletin_estatal = fitz.open(r"D:\Escritorio\Repocomun\Lector pdf BOE\oposiciones.pdf")
boletin_autonomico = fitz.open(r"D:\Escritorio\Repocomun\Lector pdf BOE\oposiciones.pdf")


def buscar_en_documento(boletin, nombre):
    pattern = re.compile(r'\bjurista\b', re.IGNORECASE)
    
    for page_num in range(len(boletin)):
        page = boletin[page_num]
        text = page.get_text("text")
        
        matches = pattern.findall(text)
        if matches:
            print(f"{nombre}: Encontrado en la página {page_num + 1}: {len(matches)} veces")


# Crear hilos
hilo1 = threading.Thread(target=buscar_en_documento, args=(boletin_estatal, "Boletín Estatal"))
hilo2 = threading.Thread(target=buscar_en_documento, args=(boletin_autonomico, "Boletín Autonómico"))


hilo1.start()
hilo1.join()

hilo2.start()
hilo2.join()