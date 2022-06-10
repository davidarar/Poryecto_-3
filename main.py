from pickle import FALSE
from tkinter import Tk
from tkinter import ttk,Label,Button,Entry,StringVar,IntVar,Checkbutton,Menu
from tkinter.messagebox import showwarning,showinfo,askyesno
from reconocimiento import habilitar

def info(): #Ventana emergente para mostrar los creditos del programa
    showinfo(title="Créditos", message= """Proyecto para Taller de Programación
                Creado por: 
        Karina Urbina Alvarez 
      Jose David Arguedas Arias""")

class MainVentana: #Clase principal de la aplicación

    def __init__(self) -> None:
        
        self.main_vtna=Tk()
        self.main_vtna.geometry("400x350")
        self.main_vtna.title("Administrador del Tiempo")
        self.main_vtna.resizable(False,False)
        self.main_vtna.protocol("WM_DELETE_WINDOW", self.salir)
        
        # Menú del sistema
        menu = Menu(self.main_vtna)
        self.main_vtna.config(menu=menu)

        # primer opción del menú
        menu_reconoc =Menu(menu, tearoff=1)
        menu_reconoc.add_command(label="Habilitar",command=lambda:habilitar(True))
        menu_reconoc.add_command(label="Desabilitar",command=lambda:habilitar(False))

        # Segunda opción del menú
        menu_concentracion = Menu(menu, tearoff=0)
        menu_concentracion.add_command(label="Habilitar")
        menu_concentracion.add_command(label="Desabilitar")

        # Tercera opción del menú
        menu_info= Menu(menu, tearoff=0)
        menu_info.add_command(label=" Créditos", command=lambda: info())

        # Adicionar al menu pirncipal los tres submenus
        menu.add_cascade(label="Reconocimiento", menu=menu_reconoc)
        menu.add_cascade(label="Concentración", menu=menu_concentracion)
        menu.add_cascade(label="Info", menu=menu_info)

        Button(self.main_vtna,text="Agregar actividad",font = ("Cambria", 12),  width = "15", height = "1").place(x=100,y=30)
        Button(self.main_vtna,text="Mostrar actividad",font = ("Cambria", 12),  width = "15", height = "1").place(x=100,y=120)
        Button(self.main_vtna,text="Reporte semanal",font = ("Cambria", 12),  width = "15", height = "1").place(x=100,y=200)
        Button(self.main_vtna,text="Salir",font = ("Cambria", 12),  width = "5",command=self.salir).place(x=300,y=270)
        self.main_vtna.mainloop()

    def salir (self): #Cierra la ventana
        confirmacion = askyesno(title='Confirmación', message='¿Esta seguro de que desae cerrar esta ventana?')
        if (confirmacion):
            self.main_vtna.destroy()


if __name__ == "__main__":
     MainVentana=MainVentana()
    