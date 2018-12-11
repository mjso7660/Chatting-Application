from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_socketio import SocketIO
from login import check_password
import json as js
import login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

username = ''

@app.route('/')
def sess():
    '''
    Directing to main page
    1) If not logged in: return to register.html
    2) If logged in: display the main page
    '''
    if not session.get('logged_in'):
        return render_template('register.html')
    else:
        return render_template('chat.html')
 
@app.route('/login', methods=['GET', 'POST'])
def login():
	'''
	!Decaded
	Initial login page
    Only keep if statment that JB edited
	'''
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
    print('--------------------------{}------------------'.format(request.form))
    if request.method == 'POST':
        #TODO: If signing UP
        if request.form['email']:
            username = request.form['username']
            password = request.form['password']
            password2 = request.form['password2']
            if password != password2:
                flash('Passwords dont match')
                error = "Passwords don't match"
        #If signin IN
        else:
            if request.form['password'] != 'password' or request.form['username'] != 'admin':
                flash('Incorrect username/password')
                error = 'Incorrect username/password'
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

@socketio.on('get_message')
def get_message(json, methods=['GET', 'POST']):
    '''
    when changing chat tab
    '''
    #TODO: get message
    print(str(json))
    
@socketio.on('test')
def test(json, methods=['GET', 'POST']):
    #TODO: get message
    some_data = {0:'t1',1:'t2'}
    socketio.emit('message_history',some_data, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
