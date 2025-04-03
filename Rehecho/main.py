import threading
import re
from conseguir_pdfs import download_pdf, search_pdf
import os

#Descargar PDF, buscar patrón y borrar archivo PDF
def action(url, file_path, pattern):
    download_pdf(url, file_path)
    results = search_pdf(file_path, pattern)
    print(f"Resultado/s de {pattern} in {file_path}: {results}")
    
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Archivo eliminado.")


if __name__ == "__main__":
    url_boe = "https://www.boe.es/boe/dias/2025/03/11/pdfs/BOE-A-2025-4761.pdf"
    urls_comunidades = { 
        "Andalucia" : "https://www.juntadeandalucia.es/eboja/2025/47/BOJA25-047-00002-3332-01_00316938.pdf",
        "Madrid" : "https://www.bocm.es/boletin/CM_Boletin_BOCM/2025/03/11/05900.PDF"
    }

    search_pattern = r"(?i)(Anexo|Oposición|Oposiciones|Convocatoria|Plazas).*?(?=\n|\.)"

# RegExp info:
# r"" : raw string->no interpretar caracteres especiales (\n, \t) -> Aconsejable usarlo siempre para evitar errores
# (?i) : no distinguir entre mayus y minus (re.IGNORECASE)
# *? {. : cualquier caracter
#     * cero o más veces
#     ? convierte * en "lazy", búsqueda mínima, no máxima. Se detiene en el primer punto.
#     Sin ?, cogería hasta el último punto
#     }
# (?= tatata) : lookahead, asegura que lo que sigue esté presente pero no lo incluye
# \. : representa el fin de la oración con punto. Se tiene que expresar así para que no se confunda con el punto (.) de regexp, que es cualquier caracter)


#Hilos
#Comunidades
threads = []
for comunidad, url in urls_comunidades.items():
    file_name = f"{comunidad}.pdf"
    thread = threading.Thread(target=action, args=(url, file_name, search_pattern))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

#boe
thread_boe = threading.Thread(target=action, args=(url_boe, search_pattern))
thread_boe.start()
thread_boe.join()