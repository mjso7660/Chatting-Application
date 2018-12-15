from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_socketio import SocketIO
from login import check_password
import json as js
import login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

username = ''

@app.route('/', methods=['Get','POST'])
def sess():
    '''
    Directing to main page
    1) If not logged in: return to register.html
    2) If logged in: display the main page
    '''
    print('-----------------')
    if 'username' not in session:
        print('> Running sess(): username not in')
        return render_template('register.html')
    else:
        print('> Running sess(): username in')
        return render_template('chat.html')
 
@app.route('/register', methods=['Get','POST'])
def register():
    if 'username' in session:
        print(session)
        print('> Running register(): username in')
        return sess()
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
        #If signin IN
        else:
            if request.form['password'] != 'password' or request.form['username'] != 'admin':
                flash('Incorrect username/password')
                error = 'Incorrect username/password'
            else:
                session['username'] = username
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
    
@socketio.on('log_out')
def log_out(json,method=['GET','POST']):
    print(session)
    session.pop('username',None)
    print(session)
    return render_template('register.html')
    return sess()

if __name__ == '__main__':
    socketio.run(app, debug=True)
