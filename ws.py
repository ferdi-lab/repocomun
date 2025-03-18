from bs4 import BeautifulSoup
# abrimos el html
with open ("prueba.html","r", encoding="utf8") as file:
    contenido= file.read()

#creamos el objeto con BeautifulSoup
soup=BeautifulSoup(contenido,"html.parser")

#Buscamos todos los elementos del div
divs= soup.find_all("div")

#Recorremos los divs y mostrams el contenido
for i, div in enumerate(divs, 1):
    print(div.text)