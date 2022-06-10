from cProfile import run
from itertools import count
import os, io
from time import sleep
from tkinter.messagebox import showerror, showwarning
from tracemalloc import start, stop
import cv2 as cv
import threading, time
import uuid
import sys

class rostro ():
    
    ruta_fotos= "C:/Users/Karina/Documents/Poryecto_-3/fotos"
    cant_fotos=len(os.listdir(ruta_fotos)) # Cantidad de fotos en la carpeta
    count=cant_fotos 

    def __init__(self) -> None: 
        pass

    def capturar_imagen(self):
        camara = cv.VideoCapture(0)
        leido, imagen = camara.read()
        camara.release()
        if leido == True:
            if self.cant_fotos >0:
                self.count +=1
                # nombre_foto = str(uuid.uuid4()) + ".png" # Genera un nombre de foto aleatorio
                cv.imwrite(self.ruta_fotos + "/foto" + str(self.count) + ".png", imagen)    
        else:
            showerror(title='Error en la toma de imagen', 
                message='No fue posible capturar la imagen con esta dispositivo!')
        return imagen
    
def reconocer_emocion():
    # mi_rostro=rostro()
    # imagen=mi_rostro.capturar_imagen()

    from google.cloud import vision
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
    client=vision.ImageAnnotatorClient() # Inicializa un cliente 

    
    with io.open('fotos/niñoFeliz.png', 'rb') as imagen_file:
        content = imagen_file.read() # imgen en bytes

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

        #Probabilidad de Expresiones
        #Emociones: Alegría, pena, ira, sorpresa
        face_expressions=dict(  joy_likelihood=likelihood_name[face.joy_likelihood],
                                sorrow_likelihood=likelihood_name[face.sorrow_likelihood],
                                anger_likelihood=likelihood_name[face.anger_likelihood],
                                surprise_likelihood=likelihood_name[face.surprise_likelihood],
                                under_exposed_likelihood=likelihood_name[face.under_exposed_likelihood],
                                blurred_likelihood=likelihood_name[face.blurred_likelihood],
                                headwear_likelihood=likelihood_name[face.headwear_likelihood])

        # #polígono de marco de cara
        # vertices=[]
        # for vertex in face.bounding_poly.vertices:
        #     vertices.append (dict (x=vertex.x, y=vertex.y))

        # face_dict=dict( face_angles=face_angles,
        #                 detection_confidence=detection_confidence,
        #                 face_expressions=face_expressions,
        #                 vertices=vertices)
        # faces_list.append(face_dict)

        # x1=faces_list[0]['vertices'][0]['x']
        # y1=faces_list[0]['vertices'][0]['y']
        # x2=faces_list[0]['vertices'][2]['x']
        # y2=faces_list[0]['vertices'][2]['y']

        # cv.rectangle(image,(x1,y1),(x2,y2),(0,255,0),3)

    
# if __name__ == '__main__':
#     reconocer_emocion()

def tarea_paralela(estado):
    mi_rostro=rostro()
    while :
        mi_rostro.capturar_imagen()
        sleep(5)

def habilitar(estado):
    if estado == [True]:
        showwarning('Advertencia','Se ha habilidado la captura de imagen')
        parametros=[estado]
        proceso=threading.Thread(target=tarea_paralela,args=parametros)
        proceso.start()
    else:
        showwarning('Advertencia','La captura de imagen se ha deshabilitado')
        exit()





