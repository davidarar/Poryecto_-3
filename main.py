from tkinter import Tk
from tkinter import Button, Menu
from tkinter.messagebox import showwarning, showinfo, askyesno
import threading
from time import sleep
from reconocimiento import reconocer_emocion
from regisActividad import RegistroActividad
from regisEmocion import Emociones

class MainVentana:  # Clase principal de la aplicación

    def __init__(self) -> None:
        self.pausado = True  # Variable que indica si el reconocimiento esta pausado

        # Crea la ventana principal
        self.main_vtna = Tk()
        self.main_vtna.geometry("400x350")
        self.main_vtna.title("Administrador del Tiempo")
        self.main_vtna.resizable(False, False)
        self.main_vtna.protocol("WM_DELETE_WINDOW", self.salir)

        # Menú del sistema
        menu = Menu(self.main_vtna)
        self.main_vtna.config(menu=menu)

        # Primer opción del menú
        menu_reconoc = Menu(menu, tearoff=1)
        menu_reconoc.add_command(
            label="Habilitar", command=lambda: self.habilitar_reconocimiento())
        menu_reconoc.add_command(
            label="Desabilitar", command=lambda: self.deshabilitar_reconocimiento())

        # Segunda opción del menú
        menu_concentracion = Menu(menu, tearoff=0)
        menu_concentracion.add_command(label="Habilitar")
        menu_concentracion.add_command(label="Desabilitar")

        # Tercera opción del menú
        menu_info = Menu(menu, tearoff=0)
        menu_info.add_command(label=" Créditos", command=lambda: self.info())

        # Adicionar al menu pirncipal los tres submenus
        menu.add_cascade(label="Reconocimiento", menu=menu_reconoc)
        menu.add_cascade(label="Concentración", menu=menu_concentracion)
        menu.add_cascade(label="Info", menu=menu_info)

        # Botones de la ventana
        Button(self.main_vtna, text="Agregar actividad", font=(
            "Cambria", 12),  width="15", height="1", command=lambda: RegistroActividad()).place(x=100, y=30)
        Button(self.main_vtna, text="Mostrar actividad", font=(
            "Cambria", 12),  width="15", height="1").place(x=100, y=120)
        Button(self.main_vtna, text="Reporte semanal", font=(
            "Cambria", 12),  width="15", height="1").place(x=100, y=200)
        Button(self.main_vtna, text="Salir", font=("Cambria", 12),
               width="5", command=self.salir).place(x=300, y=270)

        self.main_vtna.mainloop()  # Inicia la ventana

    def salir(self):  # Cierra la ventana y termina el programa
        confirmacion = askyesno(
            title='Confirmación', message='¿Esta seguro de que desea cerrar esta ventana?')
        if (confirmacion):
            self.main_vtna.destroy()

    def info(self):  # Ventana emergente para mostrar los creditos del programa
        showinfo(title="Créditos", message="""Proyecto para Taller de Programación
                    Creado por: 
            Karina Urbina Alvarez 
        Jose David Arguedas Arias""")

    def tarea_reconocer(self):
        while True:
            if not self.pausado:
                emocion = reconocer_emocion()
                if emocion != None:
                    Emociones.insertar_emocion(self=Emociones, emocion=emocion)
                    print("Reconociendo emociones...")
                sleep(12)  # Temporizador para el reconocimiento de emociones

    # Crea un hilo para el reconocimiento de emociones
    def habilitar_reconocimiento(self):
        showinfo(title="Advertencia",
                 message="El reconocimiento de emociones esta habilitado")
        self.pausado = False
        # Crea un hilo para el reconocimiento de emociones
        t = threading.Thread(target=self.tarea_reconocer)
        t.start()

    # Pausa el reconocimiento de emociones
    def deshabilitar_reconocimiento(self):
        showwarning(title="Advertencia",
                    message="Se ha deshabilitado el reconocimiento de emociones")
        self.pausado = True

MainVentana()
