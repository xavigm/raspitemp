# Code by Xavi Gonzalez (xavi.coupe@gmail.com)
#
#

from flask import Flask, render_template, request, redirect, session
import datetime
import sys
import Adafruit_DHT
import sqlite3
import RPi.GPIO as GPIO
import time
import threading
from waitress import serve
import functions

temperature = functions.setConfig()

app = Flask(__name__, static_url_path='/static')
app.secret_key = '4534654756345'

@app.route('/login', methods=['GET','POST'])
def login():

    if "username" in request.form:
        user = request.form['username']
        password = request.form['password']
        result = functions.login(user, password)
        empty = False
    else:
        result = False
        empty = True    

    if result == True:
        session['loginFlag'] = True
        return redirect('/')

    else:
        if empty == 1:
            message = ""
        else:
            message = "Login incorrect"    
        templateData = {
            'error': message,
        }
        session['loginFlag'] = False
        return render_template('login.html', **templateData)

@app.route('/logout', methods=['GET'])
def logout():
    session['loginFlag'] = False
    return redirect('/')

@app.route("/")
def hello():
 
    try:
        session['loginFlag']
    except:
        return render_template('login.html')


    if session['loginFlag'] == False:
        return redirect('/login')
    else:

        # obtener datos programacion diaria
        horario = {}
        con_bd = sqlite3.connect('temp.db')
        cursor_temp = con_bd.cursor()
        for i in range(7):
            cursor_temp.execute("SELECT * FROM dias WHERE dia=?", str(i))
            registro = cursor_temp.fetchone()
            horario["starth"+str(i)] = registro[1]
            horario["startm"+str(i)] = registro[2]
            horario["endh"+str(i)] = registro[3]
            horario["endm"+str(i)] = registro[4]
            horario["activo"+str(i)] = registro[5]
        cursor_temp.close()

        # obtenemos historico
        history = functions.getHistory()

        # obtenemos valor calefaccion guardado
        calefaccion = functions.querySQL("SELECT * FROM calefaccion")

        if calefaccion == "on":
            estado = "Encendido"
            color = "green"
        else:
            color = "red"
            estado = "Apagado"

        # Set initial estado value
        estado_general = functions.querySQL("SELECT * FROM estado")

        if estado_general == "on":
            checked = "checked"
        else:
            checked = ""

        # Set initial temp value
        temp = functions.querySQL("SELECT * FROM temp")

        temperature = functions.setConfig()


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
            'lunes': str(horario["starth0"])+':'+str(horario["startm0"])+"-"+str(horario["endh0"])+':'+str(horario["endm0"]),
            'martes': str(horario["starth1"])+':'+str(horario["startm1"])+"-"+str(horario["endh1"])+':'+str(horario["endm1"]),
            'miercoles': str(horario["starth2"])+':'+str(horario["startm2"])+"-"+str(horario["endh2"])+':'+str(horario["endm2"]),
            'jueves': str(horario["starth3"])+':'+str(horario["startm3"])+"-"+str(horario["endh3"])+':'+str(horario["endm3"]),
            'viernes': str(horario["starth4"])+':'+str(horario["startm4"])+"-"+str(horario["endh4"])+':'+str(horario["endm4"]),
            'sabado': str(horario["starth5"])+':'+str(horario["startm5"])+"-"+str(horario["endh5"])+':'+str(horario["endm5"]),
            'domingo': str(horario["starth6"])+':'+str(horario["startm6"])+"-"+str(horario["endh6"])+':'+str(horario["endm6"]),
            'history': history,
            'user' : functions.getUser()
        }

        return render_template('index.html', **templateData)

@app.route('/input', methods=['POST'])
def input():

    inputtemp = request.form['inputtemp']
    # Set temp value
    con_bd = sqlite3.connect('temp.db')
    cursor_temp = con_bd.cursor()
    cursor_temp.execute("UPDATE temp SET actual=?", (inputtemp,))
    con_bd.commit()
    cursor_temp.close()

    def setEstado():
        estado_general = request.form['estado']
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
        horario = horario.replace(':', '-')
        horario = horario.split("-")
        sql_update_query = "UPDATE dias SET starth=?, endh=?, startm=?, endm=?, activo=? WHERE dia=?"
        data = (horario[0], horario[1], horario[2], horario[3], 1, i)
        cursor_temp.execute(sql_update_query, data)

    con_bd.commit()
    cursor_temp.close()

    return redirect('/')

# arrancamos el bucle
# thread.start_new_thread(background, ());
x = threading.Thread(target=functions.background, args=())
x.start()

if __name__ == "__main__":
    # app.run() ##Replaced with below code to run it using waitress
    serve(app, host='0.0.0.0', port=80)
