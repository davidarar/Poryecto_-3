"""Librería para crear interfaz grafica(tkinter)"""
from cProfile import label
import tkinter as tk
from tkinter import Button, Entry, Label, StringVar,ttk,Text
from tkinter.messagebox import askyesno, showerror, showwarning,showinfo
from actividades import Actividades, obtener_lista_actividades
from datetime import datetime
from regisEmocion import Emociones


class Ventana_reportes(): #Clase para la ventana de reportes
    sv_actividad=None
    l=obtener_lista_actividades()
    tree,tree2=None,None

    def __init__(self):

        self.ventana=tk.Tk()
        self.ventana.title("Reportes")
        self.ventana.geometry("850x700")
        self.ventana.resizable(0,0)

        #Boton de la ventana
        Button(self.ventana,text='Regresar',font=(3),command=lambda:self.ventana.withdraw()).place(x=730,y=610)

#-------------------------------Tabla de Estados Actividad---------------------------------------

        Label(self.ventana,text='Estado de las Actividades',font=("Cambria", 14)).place(x=30,y=20)

        columns = ('#1', '#2', '#3','#4') # Columnas de la tabla

        self.tree = ttk.Treeview(self.ventana, columns=columns, show='headings',height=10)

        # Nombre de las columnas
        self.tree.heading('#1', text='Actividad Concluida')
        self.tree.heading('#2', text='Estado general')
        self.tree.heading('#3', text='Primeros 5 minutos')
        self.tree.heading('#4', text='Ultimos 5 minutos')

        # self.tree.bind('<<TreeviewSelect>>', self.selec_item) # Seleccionar un item de la tabla
        self.tree.place(x=25,y=60)
        
        scrollbar = ttk.Scrollbar(self.ventana, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

#-------------------------------Tabla de Reporte Semanal de Actividades---------------------------------------

        Label(self.ventana, text='Estado Semanal de Emociones ',font=("Cambria", 14)).place(x=30,y=330)
        columnas = ('#1', '#2', '#3','#4') # Columnas de la tabla

        self.tree2 = ttk.Treeview(self.ventana, columns=columnas, show='headings',height=10)

        # Nombre de las columnas
        self.tree2.heading('#1', text='Fecha')
        self.tree2.heading('#2', text="Mañana(6:00-12:59)")
        self.tree2.heading('#3', text='Tarde(13:00-18:59)')
        self.tree2.heading('#4', text='Noche (19:00-23:59)')
  
        # self.tree2.bind('<<TreeviewSelect>>', self.selec_item) # Seleccionar un item de la tabla
        self.tree2.place(x=25,y=370)
        
        scrollbar2 = ttk.Scrollbar(self.ventana, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree2.configure(yscroll=scrollbar2.set)
        scrollbar2.grid(row=0, column=1, sticky='ns') 

        actividad=Actividades.listar_actividades(Actividades)
        fechaActual = str(datetime.now().strftime('%Y-%m-%d'))
        horaActual = str(datetime.now().strftime('%H:%M'))
        
        #Llenar la tabla de estados de las actividades 
        for i in actividad:
            if i['fecha final'] == fechaActual:
                if i['hora final'] <= horaActual:
                    emc_general=calcular_emocion_predominante(i['emociones registradas'])
                    primeros_minutos=calcular_emocion_predominante(i['emociones registradas'][0:6])
                    ultimos_minutos=obtener_ultimos_5min(i['emociones registradas'],i['fecha final'])
                    self.tree.insert("", "end", values=(i['descripcion'],emc_general,primeros_minutos,ultimos_minutos))
                    
            elif i['fecha final'] < fechaActual:
                emc_general=calcular_emocion_predominante(i['emociones registradas'])
                primeros_minutos=calcular_emocion_predominante(i['emociones registradas'][0:6])
                ultimos_minutos=obtener_ultimos_5min(i['emociones registradas'],i['fecha final'])
                self.tree.insert("", "end", values=(i['descripcion'],emc_general,primeros_minutos,ultimos_minutos))

        #Llenar la tabla de reporte semanal de actividades
        
        lista_de_emociones=Emociones.listar_ascendente(Emociones)

        l_mañana=[]
        l_tarde=[]
        l_noche=[]
        cont=1
        
        for i in lista_de_emociones:
            if not cont>len(lista_de_emociones):
                if i['fecha'] in lista_de_emociones[cont-1]['fecha']:
                    if i['hora'] >= '06:00' and i['hora'] <= '12:59':
                        l_mañana.append(i)
                    elif i['hora'] >= '13:00' and i['hora'] <= '18:59':
                        l_tarde.append(i)
                    elif i['hora'] >= '19:00' and i['hora'] <= '23:59':
                        l_noche.append(i)
                else:
                    l_mañana.clear()
                    l_noche.clear()
                    l_tarde.clear()
                    if i['hora'] >= '06:00' and i['hora'] <= '12:59':
                        l_mañana.append(i)
                    elif i['hora'] >= '13:00' and i['hora'] <= '18:59':
                        l_tarde.append(i)
                    elif i['hora'] >= '19:00' and i['hora'] <= '23:59':
                        l_noche.append(i)
            cont+=1    
        emc_mañana=calcular_emocion_predominante(l_mañana)
        emc_tarde=calcular_emocion_predominante(l_tarde)
        emc_noche=calcular_emocion_predominante(l_noche)

        self.tree2.insert("", "end", values=(i['fecha'],emc_mañana,emc_tarde,emc_noche))

        def regresar_menu(ventana):
            self.ventana.withdraw()
            

def obtener_ultimos_5min(item,fechaFinal):
    """Obtiene los ultimos 5 minutos de la actividad
    - args:
        item: lista de emociones registradas en la actividad """

    resultado=[]
    cont=0

    if item==[]:
        return None
    else:
        for a in item[::-1]:
            if  cont < 6:
                if a['hora'] <= fechaFinal: #12:00 a 13:00      12:00,12:01,12:02,12:03,12:04,12:05
                        resultado.append(a)
                        cont+=1
        return calcular_emocion_predominante(resultado)

            

def calcular_emocion_predominante(l):
    """ Calcula la emocion predominante de una lista de emociones de una actividad
    - args:
        - l: lista con registro de emociones de una actividad
    """
    happy,sad,surprise,angry=0,0,0,0
    emc,resp=None,None
    #emocion={'emocion': 'triste', 'fecha': '2022-06-13', 'hora': '01:30'}
    if len(l)==0:
        return None
    else:
        for a in l:
            # for a in item['emociones registradas']:
            if a['emocion'] == 'Feliz':
                happy+=1
            elif a['emocion'] == 'Triste':
                sad+=1
            elif a['emocion'] == 'Enojado':
                angry+=1
            elif a['emocion'] == 'Sorprendido':
                surprise+=1
       
    resultado=[]
    l_emc=[happy,sad,surprise,angry]
    emc_predominante=max(l_emc)

    cont=l_emc.count(emc_predominante)

    if emc_predominante == 0:
        return None
    elif cont > 1:
        l_emc=[('Alegre',happy),('Triste',sad),('Enojado',angry),('Sorprendido',surprise)]
        for t in l_emc:
            if t[1] == emc_predominante:
                resultado.append(t[0])
        return resultado
    else:
        emc=[('Alegre',happy),('Triste',sad),('Enojado',angry),('Sorprendido',surprise)]
        resp=max(emc, key=lambda x: x[1])
        return resp[0]












    




