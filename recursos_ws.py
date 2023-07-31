import requests
from bs4 import BeautifulSoup

#usuario falso para evitar 403 Forbidden Error
HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

##########################  REQUEST PARA ACCEDER A LOS DATOS DE LA PÁGINA Y BÚSQUEDA CON BS ############################################
pagina = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm', headers=HEADERS).text
soup = BeautifulSoup(pagina,'lxml')
peliculas = soup.find_all('li', class_='ipc-metadata-list-summary-item sc-bca49391-0 eypSaE cli-parent')