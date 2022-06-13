import tkinter as tk
from tkinter import Button, Entry, Label, StringVar, ttk
from actividades import Actividades
from tkinter.messagebox import showinfo, showwarning

# Clase que muestra la ventana de registro de actividades
class RegistroActividad():

    # Contenedores de las entradas de texto
    sv_descripcion, sv_fechaInicio, sv_horaInicio, sv_fechaFinal, sv_horaFinal = [
        None, None, None, None, None]

    def __init__(self) -> None:

        # Ventana de registro de actividades
        self.v_registro_actividad = tk.Tk()
        self.v_registro_actividad.geometry("400x330")
        self.v_registro_actividad.title("Administrador del Tiempo")
        self.v_registro_actividad.resizable(False, False)

        # Texto y entradas  de datos
        Label(self.v_registro_actividad, text="Descripcion:",
              font=("Cambria", 12)).place(x=25, y=80)
        self.sv_descripcion = StringVar(self.v_registro_actividad)
        Entry(self.v_registro_actividad, textvariable=self.sv_descripcion,
              width="27").place(x=140, y=85)

        Label(self.v_registro_actividad, text="Fecha Inicio:",
              font=("Cambria", 12)).place(x=25, y=120)
        self.sv_fechaInicio = StringVar(self.v_registro_actividad)
        Entry(self.v_registro_actividad, textvariable=self.sv_fechaInicio,
              width="27").place(x=140, y=125)

        Label(self.v_registro_actividad, text="Hora Inicio:",
              font=("Cambria", 12)).place(x=25, y=150)
        self.sv_horaInicio = StringVar(self.v_registro_actividad)
        Entry(self.v_registro_actividad, textvariable=self.sv_horaInicio,
              width="27").place(x=140, y=155)

        Label(self.v_registro_actividad, text="Fecha Final:",
              font=("Cambria", 12)).place(x=25, y=190)
        self.sv_fechaFinal = StringVar(self.v_registro_actividad)
        Entry(self.v_registro_actividad, textvariable=self.sv_fechaFinal,
              width="27").place(x=140, y=195)

        Label(self.v_registro_actividad, text="Hora Final:",
              font=("Cambria", 12)).place(x=25, y=220)
        self.sv_horaFinal = StringVar(self.v_registro_actividad)
        Entry(self.v_registro_actividad, textvariable=self.sv_horaFinal,
              width="27").place(x=140, y=225)

        Label(self.v_registro_actividad, text="""NOTA: 
        El formato de fecha es 'aaaa-mm-dd'                     
         y el formato de hora es 'hh:mm'""", font=("Cambria", 11)).place(x=25, y=8)  # Nota para el formato de fecha y hora

        # Botones de registro
        Button(self.v_registro_actividad, text="Guardar", width="10",
               command=lambda:  self.guardar_actividad()).place(x=70, y=270)
        Button(self.v_registro_actividad, text="Cancelar", width="10",
               command=lambda: self.v_registro_actividad.destroy()).place(x=230, y=270)

        self.v_registro_actividad.mainloop()

    def guardar_actividad(self):
        """Metodo que guarda la actividad en el archivo de texto"""
        try:
            p_admin = Actividades(self.sv_descripcion.get(),
                                  self.sv_fechaInicio.get(),
                                  self.sv_horaInicio.get(),
                                  self.sv_fechaFinal.get(),
                                  self.sv_horaFinal.get(), [])

            p_admin.añadir_actividad_archivo(p_admin)

            # Actividades.añadir_actividad_archivo(self=Actividades,p_admin)

            # limpiar las entradas de datos
            self.sv_descripcion.set('')
            self.sv_fechaInicio.set('')
            self.sv_horaInicio.set('')
            self.sv_fechaFinal.set('')
            self.sv_horaFinal.set('')

            showinfo("Registro de Actividad", "Registro exitoso")
            self.v_registro_actividad.withdraw()

        except:
            showwarning(title="Alerta",
                        message="No se ha pudo agregar la actividad")
