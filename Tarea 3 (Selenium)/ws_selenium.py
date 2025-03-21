from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import time

usuario = "standard_user"
contraseña = "secret_sauce"

def main():
    service = Service(ChromeDriverManager().install()) #crear servicio e instalar Chrome si no lo tenemos

    option = webdriver.ChromeOptions() #para pasarle algunos parámetros al navegador
    option.add_argument("--window-size=1920,1080") #decir el tamaño que va a tener la pantalla

    driver = Chrome(service=service, options=option) #crear driver
    driver.get("https://www.saucedemo.com/") #enlace de la página que va a navegar

#LOGIN
    input_usuario = driver.find_element(By.ID, "user-name") #busca el elemento que tenga el ID: user-name
    input_usuario.send_keys(usuario) #escribe en el elemento el usuario almacenado en la variable: usuario

    input_contraseña = driver.find_element(By.ID, "password") #busca el elemento que tenga el ID: password
    input_contraseña.send_keys(contraseña) #escribe en el elemento la contraseña almacenada en la variable: contraseña

    boton = driver.find_element(By.ID, "login-button")
    boton.click()

#COMPRA
    boton1 = driver.find_element(By.NAME, "add-to-cart-sauce-labs-bolt-t-shirt")
    boton1.click()

    boton2 = driver.find_element(By.NAME, "add-to-cart-test.allthethings()-t-shirt-(red)")
    boton2.click()

    boton3 = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    boton3.click()

    boton4 = driver.find_element(By.ID, "checkout")
    boton4.click()

    input_nombre = driver.find_element(By.ID, "first-name")
    input_nombre.send_keys("Doramas")

    input_apellido = driver.find_element(By.ID, "last-name")
    input_apellido.send_keys("Rodríguez Torreira")

    input_codigopostal = driver.find_element(By.ID, "postal-code")
    input_codigopostal.send_keys("15821")

    boton5 = driver.find_element(By.ID, "continue")
    boton5.click()

    boton6 = driver.find_element(By.ID, "finish")
    boton6.click()

    time.sleep(10)
    driver.quit() #cerrar

if __name__ == "__main__":
    main()