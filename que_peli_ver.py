import requests
from bs4 import BeautifulSoup

HEADERS = { #usuario falso para evitar 403 Forbidden Error
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
#titulos = soup.find_all('h3', class_='ipc-title__text')

###################################  INPUT PARA LA BÚSQUEDA  #######################################################
busqueda = input("¿Querés buscar por género (g), director (d), o actor (ac)? : ")
if busqueda == 'g':
    entrada = input("¿Qué género de película querés ver? (Action, Comedy, History, Adventure, Horror, Crime, Biography, Animation): ").capitalize()
elif busqueda == 'd':    
    entrada = input("Ingresá el director que quieras ver : ").split(' ')
    entrada = entrada[0].capitalize()+' '+ entrada[1].capitalize()
elif busqueda == 'ac':        
    entrada =input("Ingresá un actor que quieras ver : ").split(' ')
    entrada = entrada[0].capitalize()+' '+ entrada[1].capitalize()
else:
    print('Valor incorrecto.')


resultados=0
print(f'Buscando {entrada}...\n')

########## BUCLE PARA OBTENER LOS DATOS DE CADA PELÍCULA Y COMPARARLOS AL INPUT ##############################
def buscar_peliculas():
    for pelicula in peliculas:
        titulo = pelicula.h3.text
        anio = pelicula.find('span', class_='sc-14dd939d-6 kHVqMR cli-title-metadata-item').text
        link = 'https://www.imdb.com/'+pelicula.div.a['href']
        pagina2= requests.get(link, headers=HEADERS).text
        soup2 = BeautifulSoup(pagina2,'lxml')
        genero = soup2.find('a', class_='ipc-chip ipc-chip--on-baseAlt').span.text
        director = soup2.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text
        actor = soup2.find('li', class_='ipc-metadata-list__item ipc-metadata-list-item--link').li.a.text


        if genero == entrada or director == entrada or actor == entrada: #si coincide cualquiera de las entradas se imprimen los datos de la película
            print("Título: ",titulo)
            print("Año: ",anio)
            print("Género: ",genero)
            print("Director: ",director)
            print("Actor principal: ",actor)
            print("-----------------------------")
            resultados=+1
    

print(resultados,' resultados.')



if __name__ == '__main__':
    buscar_peliculas()
        


    


    