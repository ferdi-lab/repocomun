import requests
from bs4 import BeautifulSoup   #importar biblioteca BeautifulSoup
from requests import get    #importar función get()

#indicar la URL para descargar el HTML en una lista
Greece = "https://es.wikipedia.org/wiki/Grecia"
Italy = "https://es.wikipedia.org/wiki/Italia"

#Scraping de cada web

print("Información sobre Grecia")

#petición para obtener el HTML del primer País
petition = requests.get(Greece)

#almacenamos la respuesta del servidor en una variable
if petition.status_code == 200: #200 si se encuentra
    html_Greece = petition.text
else:
    print("Error", petition.status_code) #error si se tiene problemas al acceder a la página

#creamos un objeto para "almacenar" el HTML
soup_Greece = BeautifulSoup(html_Greece, "html.parser")

#empezamos a sacar la información
#HISTORIA
history_Greece = soup_Greece.find("h2", {"id": "Historia"}) #buscamos el título para la historia
history_subtitle_Greece = soup_Greece.find("h3", {"id": "Primeros_asentamientos_y_Antigua_Grecia"}) #subtítulo que introduce el párrafo de historia
history_section_Greece = history_subtitle_Greece.find_next("p") #buscamos el primer elemente p después del subtítulo, así obtenemos el primer párrafo

#almaceno los elementos relacionados con la Historia en un array
all_history_Greece = [history_Greece.text, history_subtitle_Greece.text, history_section_Greece.text]

#recorremos los array para imprimir los elementos solicitados línea línea
for p in all_history_Greece:
    print (p)

#SUPERFICIE
#tomo un punto de referencia, en este caso un enlace, para encontrar el título de Superficie (que sería el padre del a)
a_Greece = soup_Greece.find("a",{"title": "Anexo:Países por superficie"})
surface_Greece = a_Greece.parent
b_Greece = soup_Greece.find("a", {"title": "Kilómetro cuadrado"})
total_surface_Greece = b_Greece.parent


#almaceno los elementos relacionados con la Superficie en un array
all_surface_Greece = [surface_Greece.text, total_surface_Greece.text]

#recorremos los array para imprimir los elementos solicitados línea línea
for q in all_surface_Greece:
    print (q)

#POBLACIÓN
#tomo un punto de referencia, en este caso un enlace, para encontrar el título de Superficie (que sería el padre del a)
c_Greece = soup_Greece.find("a",{"title": "Anexo:Países y territorios dependientes por población"})
population_Greece = c_Greece.parent
d_Greece = soup_Greece.find("sup", {"id": "cite_ref-4"})
total_population_Greece = d_Greece.parent

#almaceno los elementos relacionados con la Población en un array
all_population_Greece = [population_Greece.text, total_population_Greece.text]

#recorremos los array para imprimir los elementos solicitados línea línea
for r in all_population_Greece:
    print (r)

#PIB
#tomo un punto de referencia, en este caso un enlace, para encontrar el título de PIB (que sería el padre del a)
e_Greece = soup_Greece.find("a",{"title": "Anexo:Países por PIB (nominal)"})
ranking_Greece = e_Greece.parent
population_Greece = ranking_Greece.find_previous("th")
f_Greece = soup_Greece.find("span", {"title": "Crecimiento"})
total_population_Greece = f_Greece.parent

#almaceno los elementos relacionados con el PIB en un array
all_pib_Greece = [population_Greece.text, total_population_Greece.text]

#recorremos los array para imprimir los elementos solicitados línea línea
for s in all_pib_Greece:
    print (s)


#separación
separate = "-"
print(separate * 60)

print("Información sobre Italia")
#petición para obtener el HTML del segundo país
petition = requests.get(Italy)

#almacenamos la respuesta del servidor en una variable
if petition.status_code == 200: #200 si se encuentra
    html_Italy = petition.text
else:
    print("Error", petition.status_code) #error si se tiene problemas al acceder a la página

#creamos un objeto para "almacenar" el HTML
soup_Italy = BeautifulSoup(html_Italy, "html.parser")

#empezamos a sacar la información
#HISTORIA
history_Italy = soup_Italy.find("h2", {"id": "Historia"}) #buscamos el título para la historia
history_subtitle_Italy = soup_Italy.find("h3", {"id": "Primeras_culturas_y_Edad_del_Hierro"}) #subtítulo que introduce el párrafo de historia
history_section_Italy = history_subtitle_Italy.find_next("p") #buscamos el primer elemente p después del subtítulo, así obtenemos el primer párrafo

#almaceno los elementos relacionados con la Historia en un array
all_history_Italy = [history_Italy.text, history_subtitle_Italy.text, history_section_Italy.text]

#recorremos los array para imprimir los elementos solicitados línea línea
for p in all_history_Italy:
    print (p)

#SUPERFICIE
#tomo un punto de referencia, en este caso un enlace, para encontrar el título de Superficie (que sería el padre del a)
a_Italy = soup_Italy.find("a",{"title": "Anexo:Países por superficie"})
surface_Italy = a_Italy.parent
b_Italy = soup_Italy.find("a", {"title": "Kilómetro cuadrado"})
total_surface_Italy = b_Italy.parent


#almaceno los elementos relacionados con la Superficie en un array
all_surface_Italy = [surface_Italy.text, total_surface_Italy.text]

#recorremos los array para imprimir los elementos solicitados línea línea
for q in all_surface_Italy:
    print (q)

#POBLACIÓN
#tomo un punto de referencia, en este caso un enlace, para encontrar el título de Superficie (que sería el padre del a)
c_Italy = soup_Italy.find("a",{"title": "Anexo:Países y territorios dependientes por población"})
population_Italy = c_Italy.parent
d_Italy = soup_Italy.find("sup", {"id": "cite_ref-4"})
total_population_Italy = d_Italy.parent

#almaceno los elementos relacionados con la Población en un array
all_population_Italy = [population_Italy.text, total_population_Italy.text]

#recorremos los array para imprimir los elementos solicitados línea línea
for r in all_population_Italy:
    print (r)

#PIB
#tomo un punto de referencia, en este caso un enlace, para encontrar el título de PIB (que sería el padre del a)
e_Italy = soup_Italy.find("a",{"title": "Anexo:Países por PIB (nominal)"})
ranking_Italy = e_Italy.parent
population_Italy = ranking_Italy.find_previous("th")
f_Italy = soup_Italy.find("span", {"title": "Crecimiento"})
total_population_Italy = f_Italy.parent

#almaceno los elementos relacionados con el PIB en un array
all_pib_Italy = [population_Italy.text, total_population_Italy.text]

#recorremos los array para imprimir los elementos solicitados línea línea
for s in all_pib_Italy:
    print (s)