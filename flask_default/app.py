from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import time
import os

#tieto veci nepotrebujeme
#import MySQLdb
#import random
#import math

import serial

#ser = serial.Serial("/dev/ttyACM0", 115200)

async_mode = None

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

LED = 'OFF'
LED_mode = 'Manual'
state = 'Stop'
cruise_state = 'OFF'
lane_state = 'OFF'
speed_value = 0
steering_value = 0

udaje = ""

def vypln_udaje(led, led_mode, status, tempomat, asistent, rychlost, zatocenie):
    global udaje
    if status=='Start':
        udaje = udaje + "1"
    else:
        udaje = udaje + "0"
    if tempomat=="ON":
        udaje = udaje + "1"
    else:
        udaje = udaje + "0"
    if asistent=="ON":
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
    udaje = udaje + str(rychlost)
    udaje = udaje + str(zatocenie)
    

def background_thread(args):
    count = 0
    #dataList = []
    while True:
        global udaje
        socketio.sleep(0.1)
        udaje = ""
        vypln_udaje(LED, LED_mode, state, cruise_state, lane_state, speed_value, steering_value)
        print (udaje)
        #if state=='Start':
            #ser.write(udaje)
            


#            socketio.emit('new_speed',
#              {'data': read_ser, 'count': count},
#              namespace='/test')

#			if args:
#			  A = dict(args).get('A')
#			  btnV = dict(args).get('btn_value')
#			else:
#			  A = 1
#			  btnV = 'null'
#			print A
#			print args
#			socketio.sleep(1)
#			count += 1
#			prem = random.random()
#			dataDict = {
#			  "t": time.time(),
#			  "x": count,
#			  "y": float(A)*prem}
#			dataList.append(dataDict)
#			if len(dataList)>0:
#			  print str(dataList)
#			  print str(dataList).replace("'", "\"")
#                          socketio.emit('my_response',
#						  {'data': float(A)*math.sin(time.time()), 'count': count},
#						  namespace='/test')

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['A'] = message['value']
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})

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

@socketio.on('e_state', namespace='/test')
def test_message(message):
	global state
	if state == 'Stop':
            state = 'Start'
            global thread
            with thread_lock:
                if thread is None:
                    thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
            emit('state_connected', {'data': 'Stop', 'count': 0})
            print 'Start (Inicializacia)'
        else:
            state ='Stop'
            emit('state_connected',
                 {'data': 'Start', 'count': 0})
            print 'Koniec (Stop)'

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    #session['receive_count'] = session.get('receive_count', 0) + 1
    #emit('my_response',
    #     {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('speed_input', namespace='/test')
def test_message(message):
    global state
    global speed_value
    if state == 'Start':
        speed_value = message['value']
        session['receive_count'] = session.get('receive_count', 0) + 1
        #session['A'] = message['value']
        emit('new_speed',
            {'data': message['value'], 'count': session['receive_count']})

@socketio.on('steering_input', namespace='/test')
def test_message(message):
    global steering_value
    global state
    if state == 'Start':
        steering_value = message['value']
        #session['receive_count'] = session.get('receive_count', 0) + 1
        #emit('my_response',
        #    {'data': message['value'], 'count': session['receive_count']})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
