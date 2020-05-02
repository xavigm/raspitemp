import datetime
import Adafruit_DHT
import sqlite3
import RPi.GPIO as GPIO
import time


def setConfig():
    # GPIO DEL RELE O LED
    led = 16
    # MODELO Y PIN SENSOR TEMPERATURA
    sensor = 11
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    # set gpio inicial
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led, GPIO.OUT)
    return temperature


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
    # comparar con dia y hora actual
    start_time = int(starth)*60 + int(startm)
    end_time = int(endh)*60 + int(endm)
    current_time = datetime.datetime.now().hour*60 + datetime.datetime.now().minute
    if start_time <= current_time and end_time >= current_time:
        estado_time = "on"
    else:
        estado_time = "off"

    return estado_time


def enciendeLed():
    led = 16
    GPIO.output(led, GPIO.HIGH)


def apagaLed():
    led = 16
    GPIO.output(led, GPIO.LOW)


def background():

    temperature = setConfig()
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
        temperature = setConfig()
        temperature_back = temperature_now
        temperature_now = temperature
        max = int(temperature_back) + 5
        min = int(temperature_back) - 5
        if int(temperature) > max:
            temperature_now = temperature_back
        if int(temperature) < min:
            temperature_now = temperature_back

        # debug
        #print("Temperatura actual:")
        # print(temperature_now)
        #print("Temperatura bbdd:")
        # print(temp)
        #print("Estado general:")
        # print(estado_general)
        #print("Estado programacion:")
        # print(estado_time)

        # comparamos temperaturas,si el boton general esta activado y si esta programado.
        if int(temperature_now) < int(temp):
            if estado_general == "on":
                if estado_time == "on":
                    enciendeLed()
                    print("enciendo rele")
                    calefaccion = "on"
                else:
                    apagaLed()
                    print("apago rele")
                    calefaccion = "off"
            else:
                apagaLed()
                print("apago rele")
                calefaccion = "off"
        else:
            apagaLed()
            print("apago rele")
            calefaccion = "off"

        # Set calefaccion value
        con_bd = sqlite3.connect('temp.db')
        cursor_temp = con_bd.cursor()
        cursor_temp.execute("UPDATE calefaccion SET actual=?", (calefaccion,))
        con_bd.commit()
        cursor_temp.close()

        time.sleep(20)
