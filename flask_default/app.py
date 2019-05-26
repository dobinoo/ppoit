#importy na pouzivanie funkcii
from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import time
import os
import csv
import serial

#tieto veci nepotrebujeme
#import MySQLdb
#import random
#import math

#arduino(data)
ser = serial.Serial("/dev/ttyUSB0", 115200)

async_mode = None
app = Flask(__name__)

#serververove nastavenia
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

#Defaultne hodnoty
LED = 'OFF'
LED_mode = 'Manual'
state = 'Stop'
cruise_state = 'OFF'
lane_state = 'OFF'
speed_value = 0
steering_value = 50
control = "Remote"
udaje = ""

#Funkcia na vytvaranie suboru data.csv
def data(led, led_mode, status, tempomat, asistent, rychlost, zatocenie, control):

    with open('data.csv', mode='a') as data:
        data_writer = csv.writer(data, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([led,led_mode,status,tempomat,asistent,rychlost,zatocenie,control])



#Pridanie zaciatku a konca do suboru
def data_start_stop(number):

    with open('data.csv', mode='a') as data:
        data_writer = csv.writer(data, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if(number == "1"):
            data_writer.writerow([time.asctime()])
            data_writer.writerow(['LED','LED_mode','state','cruise_state','lane_state','speed_value','steering_value', 'control'])
            print("Start zapisovania dat")


        if(number == "0"):
            data_writer.writerow([])
            data_writer.writerow([])
            print("Ukoncenie zapisovania dat")


#Formatovanie hodnot do string na poslanie
def vypln_udaje(led, led_mode, status, tempomat, asistent, rychlost, zatocenie, control):
    global udaje

    if status=='Start':
        udaje = udaje + "1"
    else:
        udaje = udaje + "0"

    if led=="ON":
        udaje = udaje + "1"
    else:
        udaje = udaje + "0"

    if led_mode=="Auto":
        udaje = udaje + "1" #auto
    else:
        udaje = udaje + "0" #manual

    if asistent=="ON":
        udaje = udaje + "1"
    else:
        udaje = udaje + "0"

    if tempomat=="ON":
        udaje = udaje + "1"
    else:
        udaje = udaje + "0"

    if control=="Web":
        udaje = udaje + "1"
    else:
        udaje = udaje + "0"

    udaje = udaje + "{:03d}".format(int(rychlost))
    udaje = udaje + "{:03d}".format(int(zatocenie))
    udaje = udaje + "R"


def background_thread(args):
    count = 0
    #dataList = []
    while True:
        global udaje
        socketio.sleep(0.1)
        udaje = ""

        #posielanie udajov do serial portu
        if(state == "Start"):
            vypln_udaje(LED, LED_mode, state, cruise_state, lane_state, speed_value, steering_value, control)
            data(LED, LED_mode, state, cruise_state, lane_state, speed_value, steering_value, control)
            print (udaje)
            ser.write(udaje)

#Nacitanie default stranky pre cestu "/"
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['A'] = message['value']
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})

#Svetla on/off
@socketio.on('svetla', namespace='/test')
def test_message(message):
	global LED
	global state
	if state == 'Start':
            if LED == 'OFF':
                LED='ON'
                emit('ovladanie_LED',
                         {'data': 'OFF' })
            else:
                LED='OFF'
                emit('ovladanie_LED',
                         {'data': 'ON' })
            print LED

#Automaticke svetla(podla intenzity svetla) on/off
@socketio.on('svetla_auto', namespace='/test')
def test_message(message):
	global LED_mode
	global state
	if state == 'Start':
            if LED_mode == 'Auto':
                LED_mode='Manual'
                emit('auto_LED',
                         {'data': 'Auto' })
            else:
                LED_mode='Auto'
                emit('auto_LED',
                         {'data': 'Manual' })
            print LED_mode

#Ciarovy assistent
@socketio.on('lane_request', namespace='/test')
def test_message(message):
	global state
	global lane_state
	if state == 'Start':
            if lane_state == 'OFF':
                lane_state = 'ON'
                emit('lane_response',
                         {'data': 'OFF' })
            else:
                lane_state = 'OFF'
                emit('lane_response',
                         {'data': 'ON' })
            print lane_state

#Adaptivny tempomat
@socketio.on('cruise_request', namespace='/test')
def test_message(message):
	global state
	global cruise_state
	if state == 'Start':
            if cruise_state == 'OFF':
                cruise_state = 'ON'
                emit('cruise_response',
                         {'data': 'OFF' })
            else:
                cruise_state = 'OFF'
                emit('cruise_response',
                         {'data': 'ON' })
            print cruise_state

#Ovladanie ovladac/web
@socketio.on('control_state', namespace='/test')
def test_message(message):
	global state
	global control
	if state == 'Start':
            if control == 'Remote':
                control = 'Web'
                emit('control_response',
                         {'data': 'Remote' })
            else:
                control = 'Remote'
                emit('control_response',
                         {'data': 'Web' })
            print control

#Kontrolujeme stav START/STOP
@socketio.on('e_state', namespace='/test')
def test_message(message):
	global state

    #Inicializacia
	if state == 'Stop':
            state = 'Start'
            global thread
            global past
            with thread_lock:
                if thread is None:
                    thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
            emit('state_connected', {'data': 'Stop', 'count': 0})
            print 'Start (Inicializacia)'

            #Ziskanie aktualneho casu pri stlaceni start
            past=time.time()

            #Generovanie dat do hlavicky data.csv
            data_start_stop("1")


        else:
            state ='Stop'
            emit('state_connected',
                 {'data': 'Start', 'count': 0})
            print 'Koniec (Stop)'

            #Vynulovanie casu
            past=0

            #Generovanie dat do footer-u data.csv
            data_start_stop("0")

            #Poslanie posledneho retazca
            ser.write("000000000050R")
            print("Poslanie posledneho stringu do arduina (0 0 0 0 0 0 000 050 R)")

#Odpojenie zo servera
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    global state
    state='Stop'
    data_start_stop("0")

    ser.write("000000000050R")
    print("Poslanie posledneho stringu do arduina (0 0 0 0 0 0 000 050 R)")

    disconnect()
    print("\nDISCONNECTED\n\n")

#Rychlost
@socketio.on('speed_input', namespace='/test')
def test_message(message):
    global state
    global speed_value
    if state == 'Start':
        speed_value = message['value']
        now=time.time()-past
        #session['receive_count'] = session.get('receive_count', 0) + 1
        #session['A'] = message['value']
        emit('new_speed',
             {'data': message['value'], 'count': int(now)})
            #{'data': message['value'], 'count': session['receive_count']})

#Riadenie
@socketio.on('steering_input', namespace='/test')
def test_message(message):
    global steering_value
    global state
    if state == 'Start':
        steering_value = message['value']
        #session['receive_count'] = session.get('receive_count', 0) + 1
        #emit('my_response',
        #    {'data': message['value'], 'count': session['receive_count']})

#Main funkcia a spustenie serveru localhost, port 80
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
