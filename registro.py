# ------------------------------------------------------------------------Registro de Actividades--------------------------------------------------------------------------------


print("Resgitro de Actividades\n\n1)-Nueva Actividad\n2)-Mostrar Actividades\n3)-Eliminar Registro")

opcion = int(input("Dijite su Opcion: "))

if opcion == 1:
    print(
        "***********************Nuevo Registro de Actividad******************************\n"
    )
    archivo = open("ejemplo.csv", "a")

    nombre = input("Dijite el Nombre del Estudiante: ")
    apellido1 = input("Dijite el primer apellidos : ")
    apellido2 = input("Dijite el segundo apellidos: ")
    actividad = input("Dijite la actividad: ")
    curso = input("Dijite el nombre del curso: ")
    carrera = input("Dijite la carrera: ")

    print(
        "Se han capturado: "
        + nombre
        + ", Primer Apellido: "
        + apellido1
        + ", Segundo Apellido: "
        + apellido2
        + ", Actividad: "
        + actividad
        + ", Curso: "
        + curso
        + ", Carrera: "
        + carrera
    )

    archivo.write(nombre)
    archivo.write(",")
    archivo.write(apellido1)
    archivo.write(",")
    archivo.write(apellido2)
    archivo.write(",")
    archivo.write(actividad)
    archivo.write(",")
    archivo.write(curso)
    archivo.write(",")
    archivo.write(carrera)
    archivo.write(".")
    archivo.write("\n")

    archivo.close()

elif opcion == 2:
    print("Mostrar Registros\n")
    archivo = open("ejemplo.csv")

    print(archivo.read())

    archivo.close()

elif opcion == 3:
    archivo = open("ejemplo.csv","a")
    archivo.truncate()
    
    print("Registros Eliminados")
    
    archivo.close()
else:
    print("Debes de Elegir una opcion anterior")
    
#falta hacer la parte restante