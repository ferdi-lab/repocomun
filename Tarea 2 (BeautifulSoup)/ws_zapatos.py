import requests
from bs4 import BeautifulSoup

url = "https://listado.mercadolibre.com.ar/ropa-accesorios/calzado/zapatillas/zapatillas_NoIndex_True#D[A:zapatillas,on]"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    productos = soup.find_all('div', class_="andes-card poly-card poly-card--grid-card andes-card--flat andes-card--padding-0 andes-card--animated")
    print(len(productos))

    for producto in productos:
        titulo = producto.find('h3', class_="poly-component__title-wrapper")
        precio = producto.find('span', class_="andes-money-amount andes-money-amount--cents-superscript")
        if titulo:
            print(titulo.text.strip())
        if precio:
            print(precio.text.strip())
else:
    print ("Error al cargar la web, código:", response.status_code)