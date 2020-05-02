# Code by Xavi Gonzalez (xavi.coupe@gmail.com)
#
# Vars
# temp_actual,temperature (temperatura del sensor)
# temp (temperatura guardada en sqlite)
#

from flask import Flask, render_template, request, redirect
import datetime
import sys
import Adafruit_DHT
import sqlite3
import RPi.GPIO as GPIO
import time
import threading
from waitress import serve


# GPIO DEL RELE O LED
led = 16

sensor = 11
pin = 4
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


# set gpio inicial
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)


def timeActivate():

   # obtener datos programacion diaria de la bbdd
   dia = datetime.datetime.today().weekday()
   con_bd = sqlite3.connect('temp.db')
   cursor_temp = con_bd.cursor()
   cursor_temp.execute("SELECT * FROM dias WHERE dia=?", str(dia))
   registro = cursor_temp.fetchone()
   starth = registro[1] 
   startm = registro[2] 
   endh = registro[3] 
   endm = registro[4] 
   cursor_temp.close()
   #comparar con dia y hora actual
   start_time = int(starth)*60 + int(startm)
   end_time = int(endh)*60 + int(endm)
   current_time =  datetime.datetime.now().hour*60 +datetime.datetime.now().minute
   if start_time <= current_time and end_time >= current_time:
      estado_time = "on"
   else:
      estado_time = "off"

   return estado_time

def background():

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature_now = temperature
    
    while True:

        estado_time = timeActivate()

        # obtenemos valor temperatura guardado
        con_bd = sqlite3.connect('temp.db')
        cursor_temp = con_bd.cursor()
        cursor_temp.execute("SELECT * FROM temp")
        registro = cursor_temp.fetchone()
        temp = (registro[0])
        cursor_temp.close()

        # obtenemos valor estado guardado
        con_bd = sqlite3.connect('temp.db')
        cursor_estado = con_bd.cursor()
        cursor_estado.execute("SELECT * FROM estado")
        registro = cursor_estado.fetchone()
        estado_general = (registro[0])
        cursor_temp.close()

        # obtenemos valor actual del sensor
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature_back = temperature_now
        temperature_now = temperature
        max = int(temperature_back) + 5
        min = int(temperature_back) - 5
        if int(temperature) > max:
            temperature_now = temperature_back
        if int(temperature) < min:
            temperature_now = temperature_back
        print("temperatura actual:")
        print(temperature_now)
        print("temperatura bbdd:")
        print(temp)
        print("Estado general:")
        print(estado_general)
        print("ESTADO PROGRAMACION:")
        print(estado_time)
        # comparamos temperaturas,si el boton general esta activado y si esta programado.
        if int(temperature_now) < int(temp):
            if estado_general == "on":
               if estado_time == "on":
                  GPIO.output(led, GPIO.HIGH)
                  print("enciendo rele")
                  calefaccion = "on"
               else:
                  GPIO.output(led, GPIO.LOW)
                  print("apago rele")
                  calefaccion = "off"   
            else:
                GPIO.output(led, GPIO.LOW)
                print("apago rele")
                calefaccion = "off"
        else:
            GPIO.output(led, GPIO.LOW)
            print("apago rele")
            calefaccion = "off"

        # Set calefaccion value
        con_bd = sqlite3.connect('temp.db')
        cursor_temp = con_bd.cursor()
        cursor_temp.execute("UPDATE calefaccion SET actual=?", (calefaccion,))
        con_bd.commit()
        cursor_temp.close()

        time.sleep(20)


# arrancamos el bucle
# thread.start_new_thread(background, ());
x = threading.Thread(target=background, args=())
x.start()


app = Flask(__name__, static_url_path='/static')
@app.route("/")
def hello():

    # obtener datos programacion diaria
    horario = {}
    con_bd = sqlite3.connect('temp.db')
    cursor_temp = con_bd.cursor()
    for i in range(7):
      cursor_temp.execute("SELECT * FROM dias WHERE dia=?",str(i))
      registro = cursor_temp.fetchone()
      horario["starth"+str(i)] = registro[1] 
      horario["startm"+str(i)] = registro[2] 
      horario["endh"+str(i)] = registro[3] 
      horario["endm"+str(i)] = registro[4] 
      horario["activo"+str(i)] = registro[5] 

    cursor_temp.close()


    # obtenemos valor calefaccion guardado
    con_bd = sqlite3.connect('temp.db')
    cursor_temp = con_bd.cursor()
    cursor_temp.execute("SELECT * FROM calefaccion")
    registro = cursor_temp.fetchone()
    calefaccion = (registro[0])
    cursor_temp.close()

    if calefaccion == "on":
        estado = "Encendido"
        color = "green"
    else:
        color = "red"
        estado = "Apagado"

    # Set initial estado value
    con_bd = sqlite3.connect('temp.db')
    cursor_temp = con_bd.cursor()
    cursor_temp.execute("SELECT * FROM estado")
    registro1 = cursor_temp.fetchone()
    estado_general = (registro1[0])
    cursor_temp.close()

    if estado_general == "on":
        checked = "checked"
    else:
        checked = ""

    # Set initial temp value
    con_bd = sqlite3.connect('temp.db')
    cursor_temp = con_bd.cursor()
    cursor_temp.execute("SELECT * FROM temp")
    # for registro in cursor_temp:
    registro = cursor_temp.fetchone()
    temp = (registro[0])
    cursor_temp.close()

    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    # ENVIAR DATOS A TEMPLATE
    templateData = {
        'title': 'Raspitemp',
        'time': timeString,
        'temp_actual': temperature,
        'temp': temp,
        'checked': checked,
        'color': color,
        'estado': estado,
        'lunes' : str(horario["starth0"])+':'+str(horario["startm0"])+"-"+str(horario["endh0"])+':'+str(horario["endm0"]),
        'martes' : str(horario["starth1"])+':'+str(horario["startm1"])+"-"+str(horario["endh1"])+':'+str(horario["endm1"]),
        'miercoles' : str(horario["starth2"])+':'+str(horario["startm2"])+"-"+str(horario["endh2"])+':'+str(horario["endm2"]),
        'jueves' : str(horario["starth3"])+':'+str(horario["startm3"])+"-"+str(horario["endh3"])+':'+str(horario["endm3"]),
        'viernes' : str(horario["starth4"])+':'+str(horario["startm4"])+"-"+str(horario["endh4"])+':'+str(horario["endm4"]),
        'sabado' : str(horario["starth5"])+':'+str(horario["startm5"])+"-"+str(horario["endh5"])+':'+str(horario["endm5"]),
        'domingo' : str(horario["starth6"])+':'+str(horario["startm6"])+"-"+str(horario["endh6"])+':'+str(horario["endm6"])
    }

    return render_template('index.html', **templateData)


@app.route('/input', methods=['POST'])
def input():

    inputtemp = request.form['inputtemp']
    print("AQUI INPUTTEMP")
    print(inputtemp)
    # Set temp value
    con_bd = sqlite3.connect('temp.db')
    cursor_temp = con_bd.cursor()
    cursor_temp.execute("UPDATE temp SET actual=?", (inputtemp,))
    con_bd.commit()
    cursor_temp.close()

    def setEstado():
        estado_general = request.form['estado']
        print("input estado:")
        print(estado_general)
        # Set estado value
        con_bd = sqlite3.connect('temp.db')
        cursor_temp = con_bd.cursor()
        cursor_temp.execute("UPDATE estado SET actual=?", (estado_general,))
        con_bd.commit()
        cursor_temp.close()

    def setEstadoOff():
        estado_general = "off"
        # Set estado value
        con_bd = sqlite3.connect('temp.db')
        cursor_temp = con_bd.cursor()
        cursor_temp.execute("UPDATE estado SET actual=?", (estado_general,))
        con_bd.commit()
        cursor_temp.close()

    try:
        request.form['estado']
    except NameError:
        setEstadoOff()
    else:
        setEstado()

    return redirect('/')

@app.route('/dias', methods=['POST'])
def diainput():


   con_bd = sqlite3.connect('temp.db')
   cursor_temp = con_bd.cursor()
   for i in range(7):  

      horario = request.form[str(i)]
      horario = horario.replace(':','-')
      horario = horario.split("-")
      sql_update_query = "UPDATE dias SET starth=?, endh=?, startm=?, endm=?, activo=? WHERE dia=?"
      data = (horario[0],horario[1],horario[2],horario[3],1,i)
      cursor_temp.execute(sql_update_query,data)

   con_bd.commit()
   cursor_temp.close()


   return redirect('/')





if __name__ == "__main__":
   # app.run() ##Replaced with below code to run it using waitress
   serve(app, host='0.0.0.0', port=80)
