class Lista:
    self = None

    def __init__(self) -> None:
        self.sig = None

    def imprimir(self):
        print(self)
        if self.sig != None:
            self.sig.imprimir()

    def insertar(self, nuevo):
        puntero = self
        while (puntero.sig != None):
            puntero = puntero.sig
        puntero.sig = nuevo

    def obtener(self, posi):
        if posi == 0:
            return self
        if self.sig == None:
            return None
        return self.sig.obtener(posi-1)

# Clase hija de clase Lista
class Actividades(Lista):

    def __init__(self, descripcion, fecha_inicio, fecha_finalizacion) -> None:
        super().__init__()
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_finalizacion = fecha_finalizacion

    def registrar_actividad(self):
        """Método que escribe los datos de la lista vinculada en el archivo 'actividades.txt'"""
        puntero = self
        try:
            with open("actividades.txt", "ta") as archivo:
                archivo.writelines({'descripcion': puntero.descripcion, 'inicio': puntero.fecha_inicio,
                                   'final': puntero.fecha_finalizacion}.__str__()+"\n")
                while puntero.sig != None:
                    puntero = puntero.sig
                    archivo.writelines({'descripcion': puntero.descripcion, 'inicio': puntero.fecha_inicio,
                                       'final': puntero.fecha_finalizacion}.__str__()+"\n")
        except FileNotFoundError as error:
            respuesta = input(
                "No encontramos el archivo de actividades. ¿Desea crear un nuevo archivo? (s/n)")
            if respuesta.lower() == "s":
                archivo = open("actividades.txt", "ta")
                archivo.writelines({'nombre': puntero.descripcion, 'inicio': puntero.fecha_inicio,
                                   'final': puntero.fecha_finalizacion}.__str__()+"\n")
                while puntero.sig != None:
                    puntero = puntero.sig
                    archivo.writelines({'nombre': puntero.descripcion, 'inicio': puntero.fecha_inicio,
                                       'final': puntero.fecha_finalizacion}.__str__()+"\n")
        finally:
            archivo.close()

    def obtener_lista_actividades(self):
        """Método que lee el contenido del archivo 'actividades.txt' y crea un
        lista vinculada de ella """
        lista_actividades = None
        try:
            with open("actividades.txt", "tr") as lector:
                a = lector.readline()
                p = eval(a)
                lista_actividades = Actividades(p['descripcion'], p['inicio'], p['final'])
                p = lector.readline()
                while (p != ""):
                    p = eval(p)
                    lista_actividades.insertar = Actividades(p['descripcion'], p['inicio'], p['final'])
                    p = lector.readline()
        except FileNotFoundError as error:
            print("No se logro leer el archivo de actividades")
        finally:
            lector.close() 
        return lista_actividades


# if __name__ == "__main__":
#     actividades = Actividades('Estudiar para laboratorio','31/5/2022','31/5/2022')
#     actividades.insertar(Actividades('Terminar proyecto taller','24/5/2022','12/6/2022'))
#     actividades.insertar(Actividades('Ver Jurassic world dominion','14/6/2022','14/6/2022'))
#     actividades.registrar_actividad()

