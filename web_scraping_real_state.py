#Importamos las librerias necesarias. 
import requests
from bs4 import BeautifulSoup
from csv import writer 
import csv
import re

class WebScraper:
 #Recibe como parámetros: la url, la posición de la url a partir de la cual hay que agregar el número de página y el número de páginas. 
    def __init__(self, target_url,pos, max_page):
        self.target_url = str(target_url)
        self.pos = int(pos)
        self.max_page = int(max_page)

    def scrape_pages(self):
        # Recibe como parámetros: 
        # la url de la pagina web a scrapear
        # la posición de la url a partir de la cual hay que agregar el número de página
        # el número de páginas
        #Genera un archivo .csv con la información que obtiene de la url a través de web scraping
        try:
        #Guardamos los resultados en un fichero csv.
            with open('real_state_ecuador_dataset.csv', 'a+', newline='', encoding='UTF8') as f:
                thewriter = csv.writer(f)
                header = ["Titulo", "Precio","Provincia", "Lugar", "Num. dormitorios", "Num. banos", "Area", "Num. garages"]
                thewriter.writerow(header)

                #Recorremos las paginas existentes
                for pagina in range(1, self.max_page):
                    if pagina == 1:
                        url = self.target_url
                    else: 
                        url = self.target_url[0:self.pos]+'page/'+str(pagina)+'/'+self.target_url[(self.pos):]
                    
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
                    page = requests.get(url, headers=headers)

                    soup1 = BeautifulSoup(page.content, 'html.parser')
                    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

                    lists = soup2.find_all("div", class_ = "item-listing-wrap")

                    for list in lists:
                        try:
                            titulo = list.find("h2", class_ = "item-title").a.text.strip()
                        except:
                            titulo = "NaN"

                        try:
                            precio = re.sub("[^0-9]","",list.find("li", class_ = "item-price").text.strip())
                        except:
                            precio = "NaN"

                        try:
                            provincia = str(list.find("address", class_ = "item-address").text.strip().split(sep = ',')[0])
                        except:
                            provincia = "NaN"

                        try:
                            lugar = list.find("address", class_ = "item-address").text.strip()
                        except:
                            lugar = "NaN"

                        try:
                            dormitorios = list.find("li", class_ = "h-beds").span.text.strip()
                        except:
                            dormitorios = "NaN"

                        try:
                            banos = list.find("li", class_ = "h-baths").span.text.strip()
                        except:
                            banos = "NaN"

                        try:
                            area = list.find("li", class_ = "h-area").span.text.strip()
                        except:
                            area = "NaN"

                        try:
                            garage = list.find("li", class_ = "h-cars").span.text.strip()
                        except:
                            garage = "NaN"

                        info = [titulo, precio, provincia, lugar, dormitorios, banos, area, garage]

                        #Si todos los elementos de la lista info son iguales, borramos los elementos dejando la lista vacia
                        #Esto lo hacemos en el caso de que existan listas en las que todos sus elementos son "NaN"
                        result = False;
                        if len(info) > 0 :
                            result = info.count(info[0]) == len(info)
                            if result:
                                info.clear()

                        #Agregamos las listas info al fichero csv.
                        thewriter.writerow(info)
        
        except Exception as e: print('Error: Failed to execute'), print(e)

def main():
# Instaciamos la clase
    webscraper = WebScraper('https://arriendayvende.com/busqueda-avanzada/?keyword&states%5B0%5D&location%5B0%5D&bedrooms&bathrooms&min-area&max-area&property_id&min-price&max-price=10000',45,26)
    scrape_pages = webscraper.scrape_pages()

if __name__ == '__main__':
    main() 
