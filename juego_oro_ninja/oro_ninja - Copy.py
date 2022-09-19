from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from random import randint

app = Flask(__name__)
app.secret_key = 'secretninja'

#!/usr/bin/env python3

LIMIT_INTENTOS = 15
intentos = 0
status_jugador = ''
movimientos_oro = []



#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/')
def main_page():

  if 'oro' not in session: session['oro'] = 0
  if 'casino_ganas' not in session: session['casino_ganas'] = False
  if 'intentos' not in session: session['intentos'] = 0
  if 'status_jugador' not in session: session['status_jugador'] = ''

  session['movimientos_oro'] = movimientos_oro
  session['status_jugador']  = status_jugador
  #tambien se devuelve la lista de diccionarios como una variable renderizada GET como practica
  return render_template('main.html')

#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/procesar_money', methods=['POST'])
def procesar():

  global movimientos_oro
  global intentos
  global status_jugador

  if request.form['bform'] == 'granja':
    cantidad  = randint(10,20)
    session['oro'] += cantidad
    movimientos_oro.append({'cantidad':cantidad, 'opcion':'Gano', 'proveniente':'Granja', 'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
  if request.form['bform'] == 'cueva':
    cantidad  = randint(5,10)
    session['oro'] += cantidad
    movimientos_oro.append({'cantidad':cantidad, 'opcion':'Gano', 'proveniente':'Cueva', 'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
  if request.form['bform'] == 'casa':
    cantidad  = randint(2,5)
    session['oro'] += cantidad
    movimientos_oro.append({'cantidad':cantidad, 'opcion':'Gano', 'proveniente':'Casa', 'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
  if request.form['bform'] == 'casino':
    cantidad  = randint(0,50)
    session['casino_ganas'] = bool(randint(0,1))
    session['oro'] += cantidad if session['casino_ganas'] else (cantidad * -1)
    opcion = 'Gano'  if session['casino_ganas'] else 'Perdio'
    movimientos_oro.append({'cantidad':cantidad, 'opcion':opcion, 'proveniente':'Casino', 'fecha':datetime.now().strftime("%d/%m/%Y %H:%M:%S")})

  intentos+= 1
  session['intentos'] = intentos
  print("intentos",end='',flush=True)
  print(session['intentos'],flush=True)
  print("status jugador",end='',flush=True)
  print("el oro del jugador es",end='',flush=True)
  print(session['oro'],flush=True)
  if session['oro'] >= 250:
    status_jugador = 'Ganaste'
    session['status_jugador'] = status_jugador
    print("status del jugador : ",end='',flush=True)
    print(status_jugador,flush=True)
    return redirect("/resultado")
  else:
    if session['intentos'] == LIMIT_INTENTOS:
      status_jugador = 'Perdiste'
      session['status_jugador'] = status_jugador
      print("status del jugador : ",end='',flush=True)
      print(status_jugador,flush=True)
      return redirect("/resultado")
    else:
      print("status del jugador : ",end='')
      print(status_jugador,flush=True)
      return redirect("/")


#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/limpiar')
def limpiar():
  global movimientos_oro
  global intentos
  session.clear()
  movimientos_oro = []
  intentos = 0
  return redirect("/")

#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/resultado')
def resultado():
  return render_template("/resultado.html")


if __name__=="__main__":   # Asegúrate de que este archivo se esté ejecutando directamente y no desde un módulo diferente    
    app.run(debug=True)    # Ejecuta la aplicación en modo de depuración