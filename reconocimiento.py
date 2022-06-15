import os
import io
from time import sleep
from tkinter.messagebox import showerror, showwarning, askyesno
import cv2 as cv
from datetime import datetime
from actividades import Actividades
import matplotlib.pyplot as plt 
from google.cloud import vision
from pygame import mixer

def capturar_imagen():
    """Función que captura una imagen y la guarda en la carpeta de la aplicación.
    - Retorna la ruta de la imagen"""

    # Se abre la camara, 0 es la camara principal y 1 es la secundaria(webcam)
    camara = cv.VideoCapture(0)
    leido, imagen = camara.read()
    camara.release()

    if leido == True:
        cv.imwrite("foto.png", imagen)
    else:
        showerror(title='Error en la toma de imagen',
                  message='No fue posible capturar la imagen con esta dispositivo!')

    return imagen  # Retorna la imagen capturada

def reconocer_emocion():
    """Función que reconoce la emoción de una persona
    - Retorna la emoción de la imagen capturada"""

    capturar_imagen()  # Se captura la imagen

    # Se toma la fecha y hora actual
    fecha = str(datetime.now().strftime('%Y-%m-%d'))
    hora = str(datetime.now().strftime('%H:%M'))

    # Se carga el archivo de credenciales
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'key.json'
    client = vision.ImageAnnotatorClient()  # Inicializa un cliente

    with io.open("2caras.png", 'rb') as imagen_file:  # Se abre la imagen capturada
        content = imagen_file.read()

    image = vision.Image(content=content)
    response = client.face_detection(image=image)  # Detecta la cara
    faces = response.face_annotations  # Obtiene las caras

    # probabilidad de emociones(desconocido=0,muy improbable=1,improbable=2,posible=3,probable=4,muy probable=5)
    likelihood_name = ('0', '1', '2', '3', '4', '5')

    faces_list = []

    if faces != []:  # Si 'faces' no esta vacio, entonces reconoce un rostro
        if len(faces) == 1:  # Si hay un solo rostro
            for face in faces:
                # dicccionario con los angulos asociados a la detección de la cara
                face_angles = dict(roll_angle=face.roll_angle,
                                pan_angle=face.pan_angle, tilt_angle=face.tilt_angle)

                # confianza de detección (tipo float)
                detection_confidence = face.detection_confidence

                # Probabilidad de Expresiones
                # Emociones: Alegría, Tristeza, ira, sorpresa
                face_expressions = dict(Alegre=likelihood_name[face.joy_likelihood],
                                        Triste=likelihood_name[face.sorrow_likelihood],
                                        Enojado=likelihood_name[face.anger_likelihood],
                                        Sorprendido=likelihood_name[face.surprise_likelihood],)

                # Se obtiene la emoción predominante
                emocion_predominante = max(
                    face_expressions, key=face_expressions.get)

                emocion = {'emocion': emocion_predominante,
                        'fecha': fecha, 'hora': hora}

            return emocion  # Retorna un diccionario con la emocion, la fecha y hora

        else:  # Si hay mas de un rostro
            showwarning(title='Error', message='No se pudo reconocer la emocion, porque hay mas de un rostro')
    else:
        showwarning(title='Error', message='No se detectó ninguna cara!')


#----------------------------Codigo de control de concentracion-------------------------------

def concentracion():
    """Función que determina la concentración de una persona"""

    #tiempo=60
    conatencion = 0
    atencion = True
    cont = 0
    pend = None
    listsexpresion = []
    capturar_imagen()
    
    # Se carga el archivo de credenciales
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'key.json'
    client = vision.ImageAnnotatorClient()  # Inicializa un cliente

    with io.open('foto.png','rb') as image_file:
        content = image_file.read() # imgen en bytes

    image = vision.Image(content=content)
    response = client.face_detection(image=image) 

    image = vision.Image(content=content) 
    response = client.face_detection(image=image) # Detecta la cara
    faces = response.face_annotations # Obtiene las caras
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY') #probabilidad de emociones

    faces_list=[] 
    #si no entra, es por que detecta el rostro
    for face in faces: 
        #dicccionario con los angulos asociados a la detección de la cara
        face_angles=dict(roll_angle=face.roll_angle,pan_angle=face.pan_angle,tilt_angle=face.tilt_angle)

        #confianza de detección (tipo float)
        detection_confidence=face.detection_confidence
    
        face_expressions=dict(  joy_likelihood=likelihood_name[face.joy_likelihood],
                                sorrow_likelihood=likelihood_name[face.sorrow_likelihood],
                                anger_likelihood=likelihood_name[face.anger_likelihood],
                                surprise_likelihood=likelihood_name[face.surprise_likelihood],
                                under_exposed_likelihood=likelihood_name[face.under_exposed_likelihood],
                                blurred_likelihood=likelihood_name[face.blurred_likelihood],
                                headwear_likelihood=likelihood_name[face.headwear_likelihood])

        #polígono de marco de cara
        vertices=[]
        for vertex in face.bounding_poly.vertices:
            vertices.append (dict (x=vertex.x, y=vertex.y))

        face_dict=dict( face_angles=face_angles,
                        detection_confidence=detection_confidence,
                        face_expressions=face_expressions,
                        vertices=vertices)
        faces_list.append(face_dict)

    if len(faces_list) >1:
        showerror(
            title='Error al reconocer rostro',
            message='Se  detectado más de un rostro')
    elif faces_list == []:
        showerror(
            title='Error al reconocer rostro',
            message='No se ha podido reconocer ningun rostro')
    else:
        for i in face_dict['face_expressions']:
            if 'VERY_LIKELY' == face_dict['face_expressions'][i]:
                listsexpresion.append(i) #esto cambiar por el nombre de la lista de espresiones
            else:
                if 'LIKELY' == face_dict['face_expressions'][i]:
                    listsexpresion.append(i)
                else:
                    if 'POSSIBLE' == face_dict['face_expressions'][i]:
                        listsexpresion.append(i)
                    else:
                        if 'UNLIKELY' == face_dict['face_expressions'][i]:
                            listsexpresion.append(i)
    
    #print(face_dict['face_angles']['pan_angle'])

    #toma los abgulos para saber si esta desconcentrado 
    if face_dict['face_angles']['pan_angle'] < -15 or face_dict['face_angles']['pan_angle'] > 15:
        if conatencion == 1:   
            tiempo = 5
            atencion = False
        else:
            conatencion = conatencion+1
            tiempo = 30
            atencion = True
            cont = 0
    else:
        cont = 0
        atencion = True
        conatencion = 0
        tiempo = 60

    #toma los angulos para saber si esta desconcentrado 
    if face_dict['face_angles']['pan_angle'] < -12 or face_dict['face_angles']['pan_angle'] > 12:
        if conatencion == 1:
            tiempo = 5
            atencion = False
        else:
            conatencion = conatencion+1
            tiempo = 30
            atencion = True
            cont = 0 
    else:
        cont = 0 
        atencion = True
        conatencion = 0
        tiempo = 60
        #print(lists expresion)
        if(atencion==False):
            cont = cont+1
        if cont == 7:
            mixer.init()
            sonido = mixer.Sound("alerta.mp3") # parte de sonido de alerta 
            mixer.Sound.play(sonido)
            cont = 0
            atencion = True
            tiempo = 60
            conatencion = 0
            pend = askyesno(message="Por favor, concentrese")
        if pend == True:
            mixer.Sound.stop(sonido)

    return tiempo

