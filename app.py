from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_socketio import SocketIO
from login import check_password
import json as js
import login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sess():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('chat.html')
 
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		check = check_password(username, password)
		if check:
			session['logged_in'] = True
			return redirect(url_for('sess'))
		else:
			flash('Invalid credentails')
			error = 'Invalid credentials'
	return render_template('login.html', error=error)

@app.route('/register', methods=['Get','POST'])
def register():
    error = None
    print('--------------------------{}------------------'.format(error))
    if request.method == 'POST':
        if request.form['password'] != 'password' or request.form['username'] != 'admin':
            flash('Invalid credentails')
            error = 'Invalid credentials'
        else:
            session['logged_in'] = True
            return redirect(url_for('sess'))
    return render_template('register.html', error=error)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')
    
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
#    //socketio.emit('my response', json, callback=messageReceived)
    socketio.emit('your response', json, callback=messageReceived)
    
@socketio.on('search')
def handle_search(json, methods=['GET', 'POST']):
    print('received search: ' + str(json))

if __name__ == '__main__':
    socketio.run(app, debug=True)
