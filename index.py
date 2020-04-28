#Code by Xavi Gonzalez (xavi.coupe@gmail.com)
#
#Vars
#temp_actual,temperature (temperatura del sensor)
#temp (temperatura guardada en sqlite)
#

from flask import Flask, render_template, request, redirect
import datetime
import sys
import Adafruit_DHT
import sqlite3

sensor = 11
pin = 4
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


app = Flask(__name__)
@app.route("/")
def hello():

   #Set initial temp value
   con_bd = sqlite3.connect('temp.db')
   cursor_temp = con_bd.cursor()
   cursor_temp.execute("SELECT * FROM temp")
   #for registro in cursor_temp:
   registro = cursor_temp.fetchone()
   temp = (registro[0])
   cursor_temp.close()

   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'Raspitemp',
      'time': timeString,
      'temp_actual': temperature,
      'temp' : temp,
      }
   return render_template('index.html', **templateData)

@app.route('/input', methods = ['POST'])
def input():
        inputtemp = request.form['inputtemp']
        #Set temp value
        con_bd = sqlite3.connect('temp.db')
        cursor_temp = con_bd.cursor()
        cursor_temp.execute("UPDATE temp SET actual=?", (inputtemp,))
        con_bd.commit()
        cursor_temp.close()
        #

        return redirect('/')


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
