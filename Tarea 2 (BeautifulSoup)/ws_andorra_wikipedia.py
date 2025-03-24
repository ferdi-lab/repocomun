import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://es.wikipedia.org/wiki/Andorra"
table_class = 'infobox geography vcard'

respuesta = requests.get(url)
soup = BeautifulSoup(respuesta.text, "html.parser")

parrafos = soup.find_all('p')
primer_parrafo = parrafos[1]

tds = soup.find_all(text=re.compile(".*km²"), limit=4)

print(primer_parrafo.text)

for td in tds:
    print(td.strip())