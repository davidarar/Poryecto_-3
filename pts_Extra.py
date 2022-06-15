from tkinter import  Tk, StringVar, Label, Button, ttk
import matplotlib.pyplot as plt
from tkinter.messagebox import showwarning

from actividades import obtener_lista_actividades,Actividades


def graficar_actividad(name_actividad):
    " Funcion para graficar una actividad "
    actividad=name_actividad.get()
    x=[]
    y=[]
    l1=Actividades.listar_actividades(Actividades)

    for i in l1:
        if i['descripcion']==actividad:
            try:
                if i['emociones registradas']!=None:
                    a=i['emociones registradas']
                    for b in a:
                        y.append(b['emocion'])
                        x.append(b['fecha'])

                    plt.plot(x, y)
                    plt.title('Grafico de emociones')
                    plt.xlabel('fecha')
                    plt.ylabel('emociones')
                    plt.show()
            except:
               showwarning("Error","No se pudo graficar")

def grafico():
    " Ventana para seleccionar una actividad y graficarla "

    ventana=Tk()
    ventana.title("Grafico")
    ventana.geometry("400x200")
    ventana.resizable(0,0)

    Label(ventana,text = "Actividades :",font = ("Cambria", 14)).place(x = 30, y = 40)

    sv_actividad = StringVar(ventana)
    c_box=ttk.Combobox(ventana,values=[],state="readonly",width = "20",font = ("Cambria", 10),textvariable=sv_actividad)
    c_box.place(x = 170, y = 45)
    l1=Actividades.listar_actividades(Actividades)
    list_act=[]

    for i in l1:
        list_act.append(i['descripcion'])
    c_box['values']=list_act 

    Button(ventana,  width = 10,  text ="Graficar",command=lambda: graficar_actividad(sv_actividad)).place(x = 100, y = 110)
    Button(ventana,  width = 10,  text ="Regresar",command=lambda: ventana.withdraw()).place(x = 230, y = 110)

    ventana.mainloop()

#grafico()




