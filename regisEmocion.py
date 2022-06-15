import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, messagebox
from time import sleep
from actividades import Actividades, obtener_lista_actividades


class Emociones(): # Arbol de emociones
    izq = None
    der = None
    emocion = None
    fecha = None
    hora = None


    def __init__(self, emocion, fecha, hora,) -> None:
        self.emocion = emocion
        self.fecha = fecha
        self.hora = hora

    def insertar_nuevo_nodo(self, emocion, fecha, hora): # Inserta un nuevo nodo emocion
        nn = Emociones(emocion, fecha, hora)
        self.__insertar_nuevo_nodo(self, nn)

    def __insertar_nuevo_nodo(self, raiz, nn):
        if raiz.fecha > nn.fecha:  # 2022-06-12 es mayor que 2020-06-10,
            if raiz.der == None:
                raiz.der = nn
            else:
                self.__insertar_nuevo_nodo(raiz.der, nn)
        elif raiz.fecha == nn.fecha:
            if raiz.hora < nn.hora:  # 13:00 es menor que 13:01
                if raiz.izq == None:
                    raiz.izq = nn
                else:
                    self.__insertar_nuevo_nodo(raiz.izq, nn)
            else:
                if raiz.der == None:
                    raiz.der = nn
                else:
                    self.__insertar_nuevo_nodo(raiz.der, nn)
        else:  # 2020-06-10 es menor que 2022-06-12
            if raiz.izq == None:
                raiz.izq = nn
            else:
                self.__insertar_nuevo_nodo(raiz.izq, nn)

    def insertar_emocion(self, emocion):
        " Inserta una nueva emocion en el arbol "
        l_actividad = obtener_lista_actividades()
        l2_actividad = l_actividad
        self._insertar_emocion(
            self, emocion=emocion, l_actividad=l_actividad, l2_actividad=l2_actividad)

    def _insertar_emocion(self, emocion, l_actividad, l2_actividad):
        " Funcion recursiva para insertar una nueva emocion en las actividades "

        if emocion['fecha'] == l_actividad.fecha_inicio: 
            if emocion['hora'] >= l_actividad.hora_inicio and emocion['hora'] <= l_actividad.hora_final:# Si la hora esta dentro del rango de la actividad
                if self == None:
                    Emociones(emocion['emocion'], emocion['fecha'], emocion['hora'])
                else:
                    self.insertar_nuevo_nodo(emocion['emocion'], emocion['fecha'], emocion['hora'])
                l_actividad.agregar_emocion(l_actividad, emocion, l2_actividad)
                print("Se agrego la emocion: "+emocion['emocion'])
            else:
                self._insertar_emocion(
                    self, emocion, l_actividad.sig, l2_actividad)
        else:
            self._insertar_emocion(
                self, emocion, l_actividad.sig, l2_actividad)

    def listar_ascendente(self):
        lista_emociones = []
        return self.__listar_ascendente(self,lista_emociones)

    def __listar_ascendente(self,raiz,list_emocion):  # mayor a menor
        if raiz != None:
            list_emocion.append({'emocion':raiz.emocion, 'fecha':raiz.fecha, 'hora':raiz.hora})
            self.__listar_ascendente(raiz.der,list_emocion)
            self.__listar_ascendente(raiz.izq,list_emocion)
        return list_emocion


if __name__ == "__main__":
    emociones=Emociones('feliz', '2020-06-12', '13:00')
    emociones.insertar_nuevo_nodo('triste', '2020-06-12', '13:01')
    emociones.insertar_nuevo_nodo('Enojado', '2020-06-13', '13:02')

    print(emociones.listar_ascendente())


# top=tk.Tk()
# c=tk.Canvas(top,height=500,width=700,bg='lightblue')

# coord=10,10,240,240
# c.create_line(0,0,500,500,fill='green',width=10)
# c.create_oval(50,50,180,150,fill='red')
# c.create_text(115,100,text='Grafico de emociones',font=('Arial',20),fill='blue',)


# Label(top,text="Emociones").pack()


# c.pack()
# top.mainloop()
