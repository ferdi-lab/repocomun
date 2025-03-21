import requests
from bs4 import BeautifulSoup

url = "https://es.wikipedia.org/wiki/Andorra"

resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

parrafos = soup.find_all('p')
primer_parrafo = parrafos[1]

tds = soup.find_all('td')
datopoblacion = tds[21]

print(primer_parrafo.text)
print(datopoblacion.text)