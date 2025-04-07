import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Crear un directorio para almacenar los PDFs descargados
output_dir = "boletines_melilla_2025"
os.makedirs(output_dir, exist_ok=True)

# Usar Service en lugar de executable_path
service = Service(ChromeDriverManager().install())  # Esto maneja la instalación automática de ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar sin abrir ventana del navegador (opcional)

# Inicia el WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL del Boletín Oficial de Melilla
url = "https://bomemelilla.es/bomes/2025"
driver.get(url)

# Aumentar el tiempo de espera para asegurarse de que todos los enlaces se carguen
wait = WebDriverWait(driver, 90)  # Aumentamos el tiempo de espera a 90 segundos

# Hacemos una pausa para asegurarnos de que los scripts hayan cargado los elementos
time.sleep(5)

# Verificar si existe un botón o enlace para cargar más boletines (simular clic si existe)
try:
    # Intentamos encontrar un botón de carga de boletines (si existe)
    load_more_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Cargar más")]')))
    print("Botón 'Cargar más' encontrado. Haciendo clic...")
    load_more_button.click()  # Hacer clic en el botón

    # Esperar a que los boletines se carguen (ajustar el tiempo según sea necesario)
    time.sleep(5)  # Espera a que carguen los boletines

except Exception as e:
    print("No se encontró el botón 'Cargar más'. Continuamos buscando los boletines existentes.")

# Imprimir el HTML de la página para depurar
page_source = driver.page_source
print("HTML de la página cargada después de hacer clic:")
print(page_source[:1000])  # Solo imprimir los primeros 1000 caracteres para evitar que se imprima toda la página

try:
    # Intentamos encontrar los enlaces de descarga de los PDF usando el evento onclick
    download_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@onclick, "window.open")]')))
    print(f"Se encontraron {len(download_buttons)} boletines.")

    # Descargar boletines
    for i, button in enumerate(download_buttons, start=1):
        try:
            # Extraer la URL del PDF del atributo onclick
            onclick_attribute = button.get_attribute("onclick")
            pdf_url = onclick_attribute.split("window.open('")[1].split("');")[0]  # Extrae la URL entre comillas

            # Completar la URL si es necesario (agregar el dominio base)
            pdf_url = "https://bomemelilla.es" + pdf_url

            # Imprimir la URL del PDF para verificar que es correcta
            print(f"🔗 URL del PDF {i}: {pdf_url}")

            # Descargar el PDF
            response = requests.get(pdf_url)
            if response.status_code == 200:
                # Guardar el PDF en el directorio de salida
                filename = os.path.join(output_dir, f"boletin_{i:03d}.pdf")
                with open(filename, "wb") as f:
                    f.write(response.content)

                # Verificar que el archivo se ha guardado
                if os.path.exists(filename):
                    print(f"✅ PDF {i} descargado correctamente: {filename}")
                else:
                    print(f"❌ Error al guardar el PDF {i}")
            else:
                print(f"⚠️ Error al descargar el PDF {i}: {response.status_code}")

        except Exception as e:
            print(f"⚠️ Error con el boletín {i}: {e}")

except Exception as e:
    print(f"❌ No se encontraron boletines. Error: {e}")

# Cerrar el navegador
driver.quit()

print(f"\n✅ Descarga completa. Todos los boletines han sido descargados.")

