from flask import Flask, render_template, request, send_from_directory
import sqlite3
import traceback
import numpy as np
import cv2
import os
import json

def getTimestampsDesc(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT timestamp FROM General ORDER BY id DESC")
        rows = cur.fetchall()
        # return rows
        return [row[0].replace("(\'", "").replace("\',)","") for row in rows]
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        
def getTimestamps(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT timestamp FROM General ORDER by id")
        rows = cur.fetchall()
        # return rows
        return [row[0].replace("(\'", "").replace("\',)","") for row in rows]
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        

def getData(conn):
    cur = conn.cursor()  
    try:
        cur.execute(""" SELECT General.timestamp, Marea.nivel, Temperatura.temp_agua, Temperatura.temp_aire, Oleaje.altura, Oleaje.direccion_procedencia, Oleaje.periodo_medio, Viento.direccion_procedencia, Viento.velocidad_media
                        FROM General
                        INNER JOIN Marea ON General.id_marea=Marea.id
                        INNER JOIN Temperatura ON General.id_temperatura=Temperatura.id
                        INNER JOIN Oleaje ON General.id_oleaje=Oleaje.id
                        INNER JOIN Viento ON General.id_viento=Viento.id
                        ORDER BY General.id DESC""")
        rows = cur.fetchall()
        return rows
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        
def getDataByTimestamp(conn, timestamp):
    cur = conn.cursor()  
    try:
        cur.execute(""" SELECT General.timestamp, Marea.nivel, Temperatura.temp_agua, Temperatura.temp_aire, Oleaje.altura, Oleaje.direccion_procedencia, Oleaje.periodo_medio, Viento.direccion_procedencia, Viento.velocidad_media FROM General
                        INNER JOIN Marea ON General.id_marea=Marea.id
                        INNER JOIN Temperatura ON General.id_temperatura=Temperatura.id
                        INNER JOIN Oleaje ON General.id_oleaje=Oleaje.id
                        INNER JOIN Viento ON General.id_viento=Viento.id
                        WHERE General.timestamp=? 
                        ORDER BY timestamp DESC""", [timestamp])
        rows = cur.fetchall()
        return rows
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        
def getImagesByTimestamp(conn, timestamp):
    cur = conn.cursor()  
    try:
        cur.execute(""" SELECT General.foto1, General.foto2, General.foto3 FROM General
                        WHERE General.timestamp=? """, [timestamp])
        record = cur.fetchall()

        imgs = []     
        for i in range(3):
            nparr = np.fromstring(record[0][i], np.uint8)
            img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
            imgs.append(img) 
        return imgs

        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
    
def getOleaje(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT altura FROM Oleaje")
        rows = cur.fetchall()
        # return rows
        return [row[0] for row in rows]
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        
def getPeriodo(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT periodo_medio FROM Oleaje")
        rows = cur.fetchall()
        # return rows
        return [row[0] for row in rows]
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        
def getViento(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT velocidad_media FROM Viento")
        rows = cur.fetchall()
        # return rows
        return [row[0] for row in rows]
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        
        
def getMareas(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT nivel FROM Marea")
        rows = cur.fetchall()
        # return rows
        return [row[0] for row in rows]
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        
def getTempAire(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT temp_aire FROM Temperatura")
        rows = cur.fetchall()
        # return rows
        return [row[0] for row in rows]
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()
        
def getTempAgua(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT temp_agua FROM Temperatura")
        rows = cur.fetchall()
        # return rows
        return [row[0] for row in rows]
        
    except:
        print("Error leyendo de la base de datos: ")
        traceback.print_exc()




app = Flask(__name__)


@app.route('/')
def main():
    conn  = sqlite3.connect('../surfData/data/historicData.db')
    times = getTimestampsDesc(conn)
    conn.close()
        
    return render_template('index.html', times=times)


@app.route('/alldata', methods=['GET'])
def alldata():
    conn  = sqlite3.connect('../surfData/data/historicData.db')
    data = getData(conn)
    conn.close()
    return render_template('datos-total.html', x=data)


@app.route('/data')
def data():
    timestamp = request.args.get('hora')
    
    conn  = sqlite3.connect('../surfData/data/historicData.db')
    data = getDataByTimestamp(conn, timestamp)
    imgs = getImagesByTimestamp(conn, timestamp)
    conn.close()
    
    cv2.imwrite("static/foto1.jpg", imgs[0])
    cv2.imwrite("static/foto2.jpg", imgs[1])
    cv2.imwrite("static/foto3.jpg", imgs[2])


    return render_template('datos-hora.html', x=data)


@app.route("/historicData.db")
def historicData():
    dir = os.path.join(app.root_path, "../surfData/data")
    return send_from_directory(directory=dir, path="historicData.db")


@app.route('/graphs')
def graphs():
    conn  = sqlite3.connect('../surfData/data/historicData.db')
    oleaje = getOleaje(conn)
    periodo = getPeriodo(conn)
    viento = getViento(conn)
    mareas = getMareas(conn)
    temp_aire = getTempAire(conn)
    temp_mar = getTempAgua(conn)
    timestamp = getTimestamps(conn)
    
    conn.close()
    return render_template('graficos.html', oleaje=oleaje, periodo=periodo, viento=viento, mareas=mareas, temp_aire=temp_aire, temp_mar=temp_mar, timestamp=json.dumps(timestamp))