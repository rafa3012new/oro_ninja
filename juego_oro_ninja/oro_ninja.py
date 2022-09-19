from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from random import randint

app = Flask(__name__)
app.secret_key = 'secretninja'

#!/usr/bin/env python3

#CONTANTES DEL PROGRAMA
LIMIT_INTENTOS = 15
GANAS_CON = 250



#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/')
def main_page():

  if 'oro' not in session: session['oro'] = 0
  if 'casino_ganas' not in session: session['casino_ganas'] = False
  if 'intentos' not in session: session['intentos'] = 0
  if 'status_jugador' not in session: session['status_jugador'] = ''
  if 'movimientos_oro' not in session: session['movimientos_oro'] = []
  if 'ganascon' not in session: session['ganascon'] = GANAS_CON

  return render_template('main.html')

#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/procesar_money', methods=['POST'])
def procesar():

  if request.form['bform'] == 'granja':
    cantidad = randint(10,20)
    session['oro'] += cantidad
    session['movimientos_oro'].append({'cantidad':cantidad, 'opcion':'Gano', 'proveniente':'Granja', 'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
  if request.form['bform'] == 'cueva':
    cantidad = randint(5,10)
    session['oro'] += cantidad
    session['movimientos_oro'].append({'cantidad':cantidad, 'opcion':'Gano', 'proveniente':'Cueva', 'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
  if request.form['bform'] == 'casa':
    cantidad = randint(2,5)
    session['oro'] += cantidad
    session['movimientos_oro'].append({'cantidad':cantidad, 'opcion':'Gano', 'proveniente':'Casa', 'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
  if request.form['bform'] == 'casino':
    cantidad  = randint(0,50)
    session['casino_ganas'] = bool(randint(0,1))
    opcion = 'Gano'  if session['casino_ganas'] else 'Perdio'
    session['oro'] += cantidad if session['casino_ganas'] else (cantidad * -1)
    session['movimientos_oro'].append({'cantidad':cantidad, 'opcion':opcion, 'proveniente':'Casino', 'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S")})

  session['intentos'] += 1
  if session['oro'] >= GANAS_CON:
    session['status_jugador'] = 'Ganaste'
    return redirect("/resultado")
  else:
    if session['intentos'] == LIMIT_INTENTOS:
      session['status_jugador'] = 'Perdiste'
      return redirect("/resultado")
    else:
      return redirect("/")


#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/limpiar')
def limpiar():
  session.clear()
  return redirect("/")

#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/resultado')
def resultado():
  return render_template("/resultado.html")


if __name__=="__main__":   # Asegúrate de que este archivo se esté ejecutando directamente y no desde un módulo diferente    
    app.run(debug=True)    # Ejecuta la aplicación en modo de depuración