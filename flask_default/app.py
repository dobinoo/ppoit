from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import MySQLdb       
import time
import random
import math

async_mode = None

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock() 
#session['checkk'] = '1'
checkk = 1


def background_thread(args):
    count = 0
    dataList = []
    global checkk
    while True:
		socketio.sleep(0.1)
		if checkk==1:
			print checkk
			if args:
			  A = dict(args).get('A')
			  btnV = dict(args).get('btn_value')
			else:
			  A = 1
			  btnV = 'null' 
			#print A
			print args  
			socketio.sleep(1)
			count += 1
			prem = random.random()
			dataDict = {
			  "t": time.time(),
			  "x": count,
			  "y": float(A)*prem}
			dataList.append(dataDict)
			if len(dataList)>0:
			  print str(dataList)
			  print str(dataList).replace("'", "\"")      
			socketio.emit('my_response',
						  {'data': float(A)*math.sin(time.time()), 'count': count},
						  namespace='/test')  

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)
  
@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['A'] = message['value']    
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})
 
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('click_event', namespace='/test')
def db_message(message):   
    session['btn_value'] = message['value']    
	
@socketio.on('e_start', namespace='/test')
def test_message(message):
	#session['checkk']=='1'
	global checkk
	checkk=1
	print 'startujeeeeeeeeeeeeem'
	print checkk
	print 'startujeeeeeeeeeeeeem'
	
# def db_message(message):   
  #  session['estart'] = message['value']    
	
@socketio.on('e_stop', namespace='/test')
def test_message(message):
	#session['checkk']=='0'
	global checkk
	checkk=0
	print 'konieccccccccccccccccccccccccc'
	print checkk
	print 'konieccccccccccccccccccccccccc'


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)