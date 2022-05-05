import requests
import sqlite3
import traceback
import pafy
import matplotlib.pyplot as plt
import cv2
import os.path
from os import path
from datetime import datetime, timedelta
from dateutil import tz

DATABASE = 'data/historicData.db'

def getDataFromDataList(dataList, timestamp):
### DataList con el formato de la API de portus
    i=0
    datos = dataList.json()
    n_datos = len(datos)
    while i < n_datos and timestamp != datos[i]['fecha']:
        i = i + 1
    
    if(i >= len(datos)):
        raise Exception("Fecha no válida")    
    
    return dataList.json()[i]['datos']

def getItemFromData(paramName, data):
    return next((item for item in data if item["nombreParametro"] == paramName), False)

def getFrameFromYoutube(url):
    video = pafy.new(url)
    best  = video.getbest()
    capture = cv2.VideoCapture(best.url)
    capture.set(cv2.CAP_PROP_POS_MSEC, 0)
    check, frame = capture.read()
    return frame

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def createDataBase(filename):
    sql_file = open("data/create_db.sql")
    
    conn = sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    
    conn.close()
    sql_file.close()



def main():
    if(not path.exists(DATABASE)):
        print('No existe base de datos, se crea una nueva')
        createDataBase(DATABASE)
            
    #Obtener datos de PORTUS
    params = {'locale': 'es'}
    oleaje = requests.post('https://portus.puertos.es/portussvr/api/RTData/station/7256', params=params, json=[34,13,20,32])
    mareas = requests.post('https://portus.puertos.es/portussvr/api/RTData/station/3120', params=params, json=[27])
    viento = requests.post('https://portus.puertos.es/portussvr/api/RTData/station/4175', params=params, json=[42,40,43,41])
    temp = requests.post('https://portus.puertos.es/portussvr/api/RTData/station/2242', params=params, json=[2,38])

    #Quedarse con la última actualización
    timestamp = oleaje.json()[0]['fecha']
    datos_oleaje = getDataFromDataList(oleaje, timestamp)
    datos_mareas = getDataFromDataList(mareas, timestamp)
    datos_viento = getDataFromDataList(viento, timestamp)
    datos_temp = getDataFromDataList(temp, timestamp)
    
    #Inicializar carpeta temporal con immágenes de error por si falla leer webcam
    cv2.imwrite('tmp/foto1.jpg', cv2.imread('empty-img.jpg'))
    cv2.imwrite('tmp/foto2.jpg', cv2.imread('empty-img.jpg'))
    cv2.imwrite('tmp/foto3.jpg', cv2.imread('empty-img.jpg'))

    #Capturas de las webcams
    try:
        cv2.imwrite('tmp/foto1.jpg', getFrameFromYoutube("https://www.youtube.com/watch?v=doNsXrJHErU"))
        cv2.imwrite('tmp/foto2.jpg', getFrameFromYoutube("https://www.youtube.com/watch?v=UHxxrdrMQWU"))
        cv2.imwrite('tmp/foto3.jpg', getFrameFromYoutube("https://www.youtube.com/watch?v=yt1e_gATGcc"))
    except:
        print("Error leyendo webcam")

    #Actualizar base de datos
    conn = sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    try:
            nivel =  float(getItemFromData("Nivel del mar", datos_mareas)['valor']) / getItemFromData("Nivel del mar", datos_mareas)['factor']
            cursor.execute('''
                    INSERT INTO Marea (nivel)
                    VALUES (?);
                    ''', [nivel])
            id_marea = cursor.lastrowid


            periodo_pico =  float(getItemFromData("Periodo de Pico", datos_oleaje)['valor']) / getItemFromData("Periodo de Pico", datos_oleaje)['factor']
            direccion =  float(getItemFromData("Direcc. Media de Proced.", datos_oleaje)['valor']) / getItemFromData("Direcc. Media de Proced.", datos_oleaje)['factor']
            periodo_medio =  float(getItemFromData("Periodo Medio Tm02", datos_oleaje)['valor']) / getItemFromData("Periodo Medio Tm02", datos_oleaje)['factor']
            altura =  float(getItemFromData("Altura Signif. del Oleaje", datos_oleaje)['valor']) / getItemFromData("Altura Signif. del Oleaje", datos_oleaje)['factor']
            cursor.execute('''
                    INSERT INTO Oleaje (periodo_de_pico, periodo_medio, direccion_procedencia, altura)
                    VALUES (?,?,?,?);
                    ''', [periodo_pico, periodo_medio, direccion, altura])
            id_oleaje = cursor.lastrowid


            t_agua =  float(getItemFromData("Temperatura del Agua", datos_temp)['valor']) / getItemFromData("Temperatura del Agua", datos_temp)['factor']
            t_aire =  float(getItemFromData("Temperatura del Aire", datos_temp)['valor']) / getItemFromData("Temperatura del Aire", datos_temp)['factor']
            cursor.execute('''
                    INSERT INTO Temperatura (temp_agua, temp_aire)
                    VALUES (?,?);
                    ''', [t_agua, t_aire])
            id_temperatura = cursor.lastrowid


            v_viento =  float(getItemFromData("Velocidad del viento", datos_viento)['valor']) / getItemFromData("Velocidad del viento", datos_viento)['factor']
            d_viento =  float(getItemFromData("Direc. de proced. del Viento", datos_viento)['valor']) / getItemFromData("Direc. de proced. del Viento", datos_viento)['factor']
            cursor.execute('''
                    INSERT INTO Viento (velocidad_media, direccion_procedencia)
                    VALUES (?,?);
                    ''', [v_viento, d_viento])
            id_viento = cursor.lastrowid

            #Convertir hora a uso horario
            gmt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            gmt = gmt.replace(tzinfo=tz.tzutc())
            local = gmt.astimezone(tz.tzlocal())
            local = local+timedelta(hours = 1)
            local = local.strftime('%Y-%m-%d %H:%M:%S.%f')

            cursor.execute('''
                    INSERT INTO General (timestamp, id_oleaje, id_marea, id_viento, id_temperatura, foto1, foto2, foto3)
                    VALUES (?,?,?,?,?,?,?,?);
                    ''', [local,id_oleaje,id_marea,id_viento,id_temperatura,convertToBinaryData('tmp/foto1.jpg'),convertToBinaryData('tmp/foto2.jpg'),convertToBinaryData('tmp/foto3.jpg')])

            conn.commit()
            
    except:
            print("Error escribiendo en la base de datos: ")
            traceback.print_exc()
            
    conn.close()





if __name__ == "__main__":
    main()
    print("Terminado programa con éxito")