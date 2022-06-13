import os
import io
from time import sleep
from tkinter.messagebox import showerror, showwarning
import cv2 as cv
from datetime import datetime

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

    from google.cloud import vision
    # Se carga el archivo de credenciales
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'key.json'
    client = vision.ImageAnnotatorClient()  # Inicializa un cliente

    with io.open("niñoFeliz.png", 'rb') as imagen_file:  # Se abre la imagen capturada
        content = imagen_file.read()

    image = vision.Image(content=content)
    response = client.face_detection(image=image)  # Detecta la cara
    faces = response.face_annotations  # Obtiene las caras

    # probabilidad de emociones(desconocido=0,muy improbable=1,improbable=2,posible=3,probable=4,muy probable=5)
    likelihood_name = ('0', '1', '2', '3', '4', '5')

    faces_list = []

    if faces != []:  # Si 'faces' no esta vacio, entonces reconoce un rostro
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
    else:
        showwarning(title='Error', message='No se detectó ninguna cara!')
