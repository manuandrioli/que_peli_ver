import requests
from bs4 import BeautifulSoup
import tkinter
from tkinter import ttk
import threading
from multiprocessing import Process
from threading import Event, Thread
import time
from recursos_ws import *
from ttkthemes import ThemedTk



######## TKINTER window, frame #######
window = ThemedTk(theme='clearlooks')
window.title('¿Qué película ver?')
window.iconbitmap('que_peli_ver/log.ico')
#window.geometry('518x580')

frame = tkinter.Frame(window, borderwidth=30)
frame.grid(row=0, column=0, sticky="nsew")

frame.grid_columnconfigure((0), weight=1)
frame.grid_rowconfigure((0), weight=1)


############### ESTILO  ##################
#estilo=ThemedTk(window)
#estilo.set_theme('yaru')


#########  TKINTER entry, labels, text output, radio button, option menu, traducir()  ##################################################

entrada = tkinter.Entry(frame)

l1=ttk.Label(frame, text="¿Querés buscar por género, director, o actor? : ", font=('Helvetica',11) )
l1.grid(row=0, column=1,padx=10,pady=5)
l2=ttk.Label(frame)

#text output
txt_output = tkinter.Text(frame, height=25, width=40, font=('Helvetica',10),bd=5,relief='groove')
txt_output.grid(column=1, row=6,sticky=tkinter.NSEW,padx=5,pady=5)
scr=ttk.Scrollbar(frame, orient=tkinter.VERTICAL, command=txt_output)
scr.grid(row=6, column=2, rowspan=15, columnspan=1, sticky=tkinter.NS)
txt_output.config(yscrollcommand=scr.set)

#radio button
rb_seleccionado=tkinter.StringVar()
rb_genero = ttk.Radiobutton(frame, text='Género',value='g',variable=rb_seleccionado)
rb_director = ttk.Radiobutton(frame, text='Director',value='d',variable=rb_seleccionado)
rb_actor = ttk.Radiobutton(frame, text='Actor',value='ac',variable=rb_seleccionado)
rb_genero.grid(row=1, column=0)
rb_director.grid(row=1, column=1)
rb_actor.grid(row=1, column=2,sticky=tkinter.W)

#option menu
om_seleccionado=tkinter.StringVar()
g_opciones=ttk.OptionMenu(frame,om_seleccionado, 'Acción','Comedia','Historia','Aventura', 'Terror', 'Crimen', 'Biografía', 'Animación')
om_seleccionado.set(' - ')

#traduce el género para poder buscarlo en base al código de la página
def traducir(gen):
    global l2 
    if gen == 'Acción':
        gen='Action'
    elif gen == 'Comedia':
        gen='Comedy'
    elif gen == 'Historia':
        gen='History'
    elif gen == 'Aventura':
        gen='Adventure'
    elif gen == 'Terror':
        gen='Horror'
    elif gen == 'Crimen':
        gen='Crime'
    elif gen == 'Biografía':
        gen='Biography'
    
    return gen

progressbar = ttk.Progressbar(frame, mode='indeterminate')

resultados=0 #para terminar el loop si no se encontraron coincidencias
running=True
condicion = Event()



#evalúa la entrada y con el boton2 llama al thread que comienza la función buscar_peliculas
def que_buscar(): 
    if rb_seleccionado.get() == 'g':
        g_opciones.grid(row=1,column=1,padx=5,pady=5)
        l1.config(text="¿Qué género de película querés ver? : ")
    elif rb_seleccionado.get() == 'd':    
        entrada.grid(row=1,column=1,padx=5,pady=5)
        l1.config(text="Ingresá el director que quieras ver : ")
    elif rb_seleccionado.get() == 'ac':        
        entrada.grid(row=1,column=1,padx=5,pady=5)
        l1.config(text="Ingresá un actor que quieras ver : ")
    else:
        l2.config(text='Valor incorrecto.')
    
    boton.grid_forget()
    rb_genero.grid_forget()
    rb_director.grid_forget()
    rb_actor.grid_forget()
    boton2.grid(row=2, column=1,padx=5,pady=5)
    

########## BUCLE PARA OBTENER LOS DATOS DE CADA PELÍCULA Y COMPARARLOS AL INPUT ##############################
def buscar_peliculas():
    global resultados
    global running
    global boton2
    
    running=True
    time.sleep(5)
    progressbar.grid(column=1, row=5,padx=5,pady=5)
    ingresado = lambda : 'el género '+om_seleccionado.get() if not om_seleccionado.get() == ' - ' else 'a '+entrada.get().title()
    l2.config(text=f'Buscando {ingresado()}...')
    l2.grid(row=3, column=1)
    boton2.grid_forget()
    boton3.grid(row=2,column=1,padx=5,pady=5)
    g_opciones.config(state='disabled')

    for pelicula in peliculas:
        if not running:
            break
        titulo = pelicula.h3.text
        anio = pelicula.find('span', class_='sc-14dd939d-6 kHVqMR cli-title-metadata-item').text
        link = 'https://www.imdb.com/'+pelicula.div.a['href']
        pagina2= requests.get(link, headers=HEADERS).text
        soup2 = BeautifulSoup(pagina2,'lxml')
        genero = soup2.find('a', class_='ipc-chip ipc-chip--on-baseAlt').span.text
        director = soup2.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text
        actor = soup2.find('li', class_='ipc-metadata-list__item ipc-metadata-list-item--link').li.a.text
        if ( genero == traducir(om_seleccionado.get()) ) or ( director == entrada.get().title() ) or ( actor == entrada.get().title() ): #si coincide cualquiera de las entradas se imprimen los datos de la película
            txt_output.insert(tkinter.END,f"Título: {titulo}\n")
            txt_output.insert(tkinter.END,f"Año: {anio}\n")
            txt_output.insert(tkinter.END,f"Género: {genero}\n")
            txt_output.insert(tkinter.END,f"Director: {director}\n")
            txt_output.insert(tkinter.END,f"Actor principal: {actor}\n")
            txt_output.insert(tkinter.END,"-----------------------------\n")
            resultados=+1

    if resultados==0:
        txt_output.insert(tkinter.END,f"No hay resultados para: {entrada.get()}\n")
    l2.config(text=f'{resultados} resultados.')

    boton3.grid_forget()


    """ genero == traducir(om_seleccionado.get()) or director == entrada.get().title() or """

""" if __name__ == '__main__':
    buscar_peliculas() """

#########################################  THREADING  ##########################################################
def empezar_thread(event):
    global submit_thread
    submit_thread = threading.Thread(target=lambda:buscar_peliculas())
    submit_thread.daemon = True
    progressbar.start()
    submit_thread.start()
    window.after(20, check_thread)
    

def check_thread():
    if submit_thread.is_alive() and running:
        window.after(20, check_thread)
    else:
        progressbar.stop()

def detener():
    global running
    running=False


#####################################  TKINTER: botones  #####################################################

boton=ttk.Button(frame, text="Aceptar", command=que_buscar)
boton.grid(row=2,column=1,padx=10,pady=10)
boton2=ttk.Button(frame, text='Buscar',command=lambda: empezar_thread(None))
boton3=ttk.Button(frame, text="Detener", command=detener)




window.mainloop()
        


    


    