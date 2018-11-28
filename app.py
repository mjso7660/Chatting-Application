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
'''
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash('wrong pss')
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
#            return redirect(url_for('sessions'))
    return sessions()

@app.route('/')
def sessions():
    if not session.get('logged_in'):
        print('1')
        return render_template('chat.html')
    else:
        print('2')
        return render_template('login.html')

@app.route('/demo2')
def sessions2():
    return render_template('chat2.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')
 '''
if __name__ == '__main__':
    socketio.run(app, debug=True)
