from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_socketio import SocketIO
from chatterbot import ChatBot
import json as js

bot = ChatBot(
	'Terminal',
	storage_adapter="chatterbot.storage.SQLStorageAdapter",
	logic_adapters=[
		"chatterbot.logic.MathematicalEvaluation",
		"chatterbot.logic.BestMatch"
	],
	database="./db.sqlite3"
)

isQuiz = False
quizNumber = 1
quizScore = 0

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
        if request.form['password'] != 'password' and request.form['username'] != 'admin':
            flash('Invalid credentails')
            error = 'Invalid credentials'
        else:
            session['logged_in'] = True
            return redirect(url_for('sess'))
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
    
    

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	global isQuiz, quizNumber, quizScore
	print('received my event: ' + str(json))
	socketio.emit('my response', json, callback=messageReceived)

	if 'message' in json.keys():
		r = dict()
		input_string = json['message'].lower()

		# quiz demo
		if isQuiz:
			answer = input_string[0].upper()
			if quizNumber == 1:
				# answer question
				if answer == 'E':
					correctness = "You answered E."
					quizScore = quizScore + 1
				else:
					correctness = "You answered " + answer + "."
				r['message'] = correctness + "<b> E is the correct Answer.</b> Despite available therapies, the inability to manage the disease remains a significant challenge. Factors can include delayed prescribing of appropriate medications, inadequate dosage, nonadherence, intolerance, or inadequate response despite maximum doses that are otherwise tolerated. Despite the availability of therapies, there remains a subset of patients with gout who, despite aggressive therapy, have intractable disease (i.e., patients with refractory gout)."
				socketio.emit('your response', r, callback=messageReceived)
				# give next question
				r['message'] = "A 5-month old infant was recently treated for vomiting and dehydration and was found to have hyponatremia, hypokalemia and a severe metabolic acidosis. Growth was initially normal, but has fallen below the third percentile on the growth curve. Which evaluation measures should be considered now for this patient, in order to confirm a suspected diagnosis of nephropathic cystinosis? </br>"\
					"</br>A. Detection of elevated cystine levels in white blood cells"\
					"</br>B. Detection of corneal cystine crystals by slit lamp examination"\
					"</br>C. Molecular testing of the CTNS gene"\
					"</br>D. A and C"\
					"</br>E. All of the above"
				socketio.emit('your response', r, callback=messageReceived)
				quizNumber = 2	
			else:
				# answer question
				if  answer == 'D':
					correctness = "You answered D."
					quizScore = quizScore + 1
				else:
					correctness = "You answered " + answer + "."
				r['message'] = correctness + "<b> E is the correct Answer.</b> Detection of elevated cystine levels in white blood cells will confirm the presence of cystinosis. Molecular testing of the CTNS gene is considered important in genetic counseling and generally recommended to confirm an initial diagnosis. Detection of corneal cystine crystals by slit lamp examination can help confirm diagnosis, but cystine crystals may not appear with this method until the second year of life, so not seeing crystals does not eliminate nephropathic cystinosis in very young infants and children with the disease."
				socketio.emit('your response', r, callback=messageReceived)
				r['message'] = "You scored " + str(quizScore) + "/2."
				socketio.emit('your response', r, callback=messageReceived)
				isQuiz = False
		else:	
			if "quiz" in input_string:  #initiate quiz
				r['message'] = "Which of the following factors for this patient can lead to gout that is not properly managed over the long-term?</br>"\
					"</br>A. Delayed prescribing of appropriate medications"\
					"</br>B. Inadequate dosage of medications"\
					"</br>C. Patient nonadherence to dietary recommendations and medications"\
					"</br>D. The presence of intractable disease (i.e., refractory gout)"\
					"</br>E. All of the above"
				isQuiz = True
				quizNumber = 1
				quizScore = 0
			elif "turner" in input_string and "short" in input_string:
				r['message'] = "Oh, how tall is he now?"
			elif "3 " in input_string:
				r['message'] = "With turner's syndrome an average final adult height is about 4 feet and 7 inches. There are few treatment options if you contact local docs, like growth hormones though"
			elif "thank" in input_string:
				r['message'] = "No problem"
			else:
				r['message'] = str(bot.get_response(json['message']))
			print(r)

			socketio.emit('your response', r, callback=messageReceived)
'''
if __name__ == '__main__':
    socketio.run(app, debug=True)
