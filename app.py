from flask import Flask, render_template , request 
import os
from markupsafe import escape
from engine import *
#from flask_cores import CORS

from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

async_mode = None
app = Flask(__name__, template_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)


@socket_.on('my_event', namespace='/naked')
def handle_myevent(message):
    print(message)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('keyword', namespace='/naked')
def searchKeyWord(msg):
    word = msg["data"]
    emit('search_response', {'data': searchByKeyWord(word)})

@socket_.on('episodetitle', namespace='/naked')
def searchEpisodeWord(msg):
    word = msg["data"]
    emit('search_response', {'data': searchByTitle(word)})

@socket_.on('episodeid', namespace='/naked')
def searchEpisodeid(msg):
    id = int(msg["data"])
    emit('search_response', {'data': searchByEpisodNumb(id)})

@socket_.on('image_event', namespace='/naked')
def handle_imageevent(msg):
    id = int(msg["data"])
    #pix = getPageImage(id)
    pix = getPageSVG(id)
    emit('image_response', pix)

@socket_.on('my_broadcast_event', namespace='/naked')
def handle_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socket_.on('disconnect_request', namespace='/naked')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


if __name__ == '__main__':
    #socket_.run(app,host="0.0.0.0", port=5005, debug=True)
    socket_.run(app,port=5005, debug=True)

