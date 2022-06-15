from tkinter.messagebox import showerror, showwarning

class Lista: # Clase Lista
    self = None

    def __init__(self) -> None:
        self.sig = None
        self.p = self

    def imprimir(self):
        print(self)
        if self.sig != None:
            self.sig.imprimir()

    def insertar(self, nuevo):
        puntero = self
        while (puntero.sig != None):
            puntero = puntero.sig
        puntero.sig = nuevo

class Actividades(Lista): # Clase Actividades, hereda de Lista

    def __init__(self, descripcion, fecha_inicio, hora_inicio, fecha_final, hora_final, emociones_registradas):
        super().__init__()
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.hora_inicio = hora_inicio
        self.fecha_final = fecha_final
        self.hora_final = hora_final
        self.emociones_registradas = emociones_registradas

    def listar_actividades(self):
        l=obtener_lista_actividades()
        lista_de_actividades=[]
        return self.__listar_actividades(self,l,lista_de_actividades)

    def __listar_actividades(self,l,lista_de_actividades):
        """Método que lista las actividades registradas en el archivo 'actividades.txt'
        - args:
            -   l = lista de actividades 
            -   lista_de_actividades = lista donde se guardarán las actividades"""

        if l!=None:
            lista_de_actividades.append({'descripcion': l.descripcion,
                                        'fecha inicio': l.fecha_inicio,
                                        'hora inicio': l.hora_inicio,
                                        'fecha final': l.fecha_final,
                                        'hora final': l.hora_final,
                                        'emociones registradas': l.emociones_registradas})
            lista_de_actividades=self.__listar_actividades(self,l.sig,lista_de_actividades)

        return lista_de_actividades

    def obtener_actividad(self, descrip):
        """Método que busca una actividad en la lista vinculada para agregarle una emoción
        -   args: 
                -   descrip = descripcion de la actividad
        - return: 
            -   puntero = puntero a la actividad encontrada"""
        puntero = self 
        try:
            while puntero.descripcion != descrip:
                puntero = puntero.sig
            return (puntero)
        except:
            return None

    def agregar_emocion(self, act, emc, l_act):
        """Método que agrega una emoción a una actividad
        - args:
            -   act = actividad a la que se le agregará la emoción
            -   emc = emoción a agregar
            -   l_act = lista de actividades"""
        self = l_act
        descrip = act.descripcion
        actividad = Actividades.obtener_emocion(self, descrip=descrip)
        if actividad == None:
            showerror(title='Error',
                      message='Ocurrió un error al registrar la emoción')
        else:
            actividad.emociones_registradas.append(emc)
            Actividades.guardar_actividad_archivo(self)

    def añadir_actividad_archivo(self, n_actividad):
        """Método que agrega una actividad al archivo 'actividades.txt'
        - args:
            -   n_actividad = actividad a agregar"""
        try:
            with open("actividades.txt", "a") as file:
                file.writelines(str({'descripcion': n_actividad.descripcion,
                                    'fecha inicio': n_actividad.fecha_inicio,
                                     'hora inicio': n_actividad.hora_inicio,
                                     'fecha final': n_actividad.fecha_final,
                                     'hora final': n_actividad.hora_final,
                                     'emociones registradas': n_actividad.emociones_registradas})+"\n")
        except FileNotFoundError as error:
            showerror("No encontramos el archivo de actividades")
        finally:
            file.close()

    def guardar_actividad_archivo(self):
        """Método que escribe los datos de la lista vinculada en el archivo 'actividades.txt'"""
        # lis_act=obtener_lista_actividades()
        puntero = self 
        try:
            with open("actividades.txt", "w") as file: 
                self.añadir_actividad_archivo(str({'descripcion': puntero.descripcion,
                                                   'fecha inicio': puntero.fecha_inicio,
                                                   'hora inicio': puntero.hora_inicio,
                                                   'fecha final': puntero.fecha_final,
                                                   'hora final': puntero.hora_final,
                                                   'emociones registradas': puntero.emociones_registradas})+"\n")

                while puntero.sig != None: # Recorre la lista de actividades, guardando cada una en el archivo
                    puntero = puntero.sig
                    self.añadir_actividad_archivo(str({'descripcion': puntero.descripcion,
                                                       'fecha inicio': puntero.fecha_inicio,
                                                       'hora inicio': puntero.hora_inicio,
                                                       'fecha final': puntero.fecha_final,
                                                       'hora final': puntero.hora_final,
                                                       'emociones registradas': puntero.emociones_registradas})+"\n")

        except FileNotFoundError as error:
            showerror("No encontramos el archivo de actividades")
        finally:
            file.close()

def obtener_lista_actividades():
    """Método que obtiene la lista de actividades del archivo 'actividades.txt'
    - return:
        -   lista = lista de actividades"""
    lista = None 
    try:
        with open("actividades.txt", "r") as lector:
            a = lector.readline()
            p = eval(a)
            lista = Actividades(p['descripcion'], p['fecha inicio'], p['hora inicio'],
                                p['fecha final'], p['hora final'], p['emociones registradas'])
            p = lector.readline()
            while (p != ""):
                p = eval(p)
                lista.insertar(Actividades(p['descripcion'], p['fecha inicio'], p['hora inicio'],
                               p['fecha final'], p['hora final'], p['emociones registradas']))
                p = lector.readline()
    except FileNotFoundError as error:
        showwarning(title="Error",
                    message="No se pudo cargar la lista de actividades")
    finally:
        lector.close()
    return lista

