from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_socketio import SocketIO
import user
import chatroom
import chat
import json as js
import login
from random import randint
from PIL import Image
from bson import Binary

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
username = ''
myimage = user.mydb['images']

@app.route('/')
def init():
	#print(session)
	if 'username' in session:
		return redirect(url_for('usermain',username=session['username']))
	else:
		return redirect(url_for('login'))

#TODO change name of login to register b/c login imported
@app.route('/login', methods=['Get','POST'])
def login():
	print('test')
	# < --------------------  ADDED CODE ----------------------->
	#if 'username' in session:
	#	redirect(url_for('usermain',username=session['username']))
	# < --------------------  ADDED CODE ----------------------->        
	error = None
	#print('--------------------------{}------------------'.format(request.form))
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
			#print(username,password)
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
	#cr = chatroom.getN(u,20)
	# for x in cr:
		# #print(x)
		# cs = chat.getChats(u, x, 20)
		# for c in cs:
			# #print(c)
	#print('hello world')
	return render_template('chat.html')


def messageReceived(methods=['GET', 'POST']):
	print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	if json['message'][:10] == 'data:image':
		bin = json['message']
		u = session['username']
	
		#Put into db (chatroom) with 'sender' and 'message' info
		
		time = 123
		socketio.emit('img',{'data':bin})
	else:
		u = user.getUser(session['username'])
		cr = chatroom.getN(u,20)
		l = []
		for x in cr:
			l.append(x)
		if json['message'].strip() is not "":
			chat.insertChat(u,l[session['index']],json['message'])
		socketio.emit('my response', json, callback=messageReceived)

@socketio.on('search')
def search(json, methods=['GET', 'POST']):
	u = user.getUser(session['username'])
	cr = chatroom.getN(u,20)
	l = []
	for x in cr:
		l.append(x)
	#print(json['message'])

	chat_dat = chat.searchChat(u,l[session['index']],json['message'])
	socketio.emit('message_history',chat_dat)

@socketio.on('boot')
def boot(json, methods=['GET', 'POST']):
	print(11111111111111)
	u = user.getUser(session['username'])
	cr = chatroom.getN(u,20)
	l = []
	for x in cr:
		l.append(chatroom.getInfo(x))
	#print(l) 
	msg = {'data':l,'user':session['username']}
	socketio.emit('update_list',process_json(l),callback=messageReceived)

@socketio.on('test')
def test(json, methods=['GET', 'POST']):
	session['index'] = json['data']
	print(session['index'])
	u = user.getUser(session['username'])
	cr = chatroom.getN(u,20)
	l = []
	for x in cr:
		l.append(x)
	try:
		chat_data = chat.getChats(u,l[session['index']],20)
		socketio.emit('message_history',process_json(chat_data), callback=messageReceived)
	except:
		return
'''
@socketio.on('pic')
def pic(json, methods=['GET', 'POST']):
	bin = json['data']
	u = session['username']
	
	image = myimage.insert_one({'data':bin})
	img = myimage.find_one({'_id':image['_id']})
	print(img['_id'])
	time = 123
	#TODO: save binary (ex: save 'bin' under 'u' with time.now())
	socketio.emit('img',{'data':bin})
'''
	
@socketio.on('add')
def add(json,methods=['GET','POST']):
	user_to_add = json['message'].split(',')
	
	# impossible if username not in chat
	if session['username'] not in user_to_add:
		return

	users = []
	#TODO: no user found
	for each in user_to_add:
		result = user.myusers.find_one({'username':each})
		if result is None:
			break
		#user found
		else:
			users.append(result['_id'])
			#create new chat room
			
	if result is None:
		socketio.emit('no_user',{'name':each})
		return
	else:
		a = str(randint(1,100000))
		b = str(randint(1,100000))
		chatroom.createChatroom(a, b, users)


@app.route('/logout',methods=['GET','POST'])
def logout():
	session.clear()
	return redirect(url_for('login'))

def process_json(data):
	return_val = {'user':session['username'],'data':data}
	return return_val

if __name__ == '__main__':
	socketio.run(app, debug=True)

