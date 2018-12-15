from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_socketio import SocketIO
import user
import chatroom
import chat
import json as js
import login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
username = ''

@app.route('/')
def init():
	print(session)
	if 'username' in session:
		return redirect(url_for('usermain',username=session['username']))
	else:
		return redirect(url_for('login'))

#TODO change name of login to register b/c login imported
@app.route('/login', methods=['Get','POST'])
def login():
    # < --------------------  ADDED CODE ----------------------->
	#if 'username' in session:
	#	redirect(url_for('usermain',username=session['username']))
    # < --------------------  ADDED CODE ----------------------->        
	error = None
	print('--------------------------{}------------------'.format(request.form))
	if request.method == 'POST':
		#TODO: If signing UP
		username = request.form['username']
		password = request.form['password']
		if request.form['email']:
			password2 = request.form['password2']
			if password != password2:
				flash('Passwords dont match')
				error = "Passwords don't match"
			else:
				if user.insertAccount(username, password) is 'DuplicateKeyError':
					error = 'Username exists'
		#If signin IN
		else:
			print(username,password)
			check = user.checkPassword(username, password)
			if not check:
				error = 'Incorrect username/password'
			else:
				session['username'] = username
				return redirect(url_for('usermain',username=session['username']))
	return render_template('register.html', error=error)

@app.route('/index/<username>')
def usermain(username, methods=['GET', 'POST']):
	u = user.getUser(session['username'])
	session['user'] = str(u['_id'])
	cr = chatroom.getN(u,20)
	# for x in cr:
		# print(x)
		# cs = chat.getChats(u, x, 20)
		# for c in cs:
			# print(c)
	print('hello world')
	return render_template('chat.html')


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
	u = user.getUser(session['username'])
	session['user'] = str(u['_id'])
	cr = chatroom.getN(u,1)
	for x in cr:
		print(x)
		some_data = chat.getChats(u, x, 20)
		
	#some_data = [{'sender': 'me', 'message': 't1'},{'sender': 'oth', 'message': 't2'}]
	socketio.emit('message_history',some_data, callback=messageReceived)
@app.route('/logout')
def logout(methods=['GET', 'POST']):
	print(111111111111111)
	session.clear()
	return redirect(url_for('login'))

if __name__ == '__main__':
	socketio.run(app, debug=True)

