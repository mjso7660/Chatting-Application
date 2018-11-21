from chatterbot import ChatBot


#bot as in a raw version

#bot = ChatBot('Norman')


#Importing trained version of the bot
bot = ChatBot(
	'Terminal',
	storage_adapter="chatterbot.storage.SQLStorageAdapter",
	logic_adapters=[
		"chatterbot.logic.MathematicalEvaluation",
		"chatterbot.logic.TimeLogicAdapter",
		"chatterbot.logic.BestMatch"
	],
	database="./db.sqlite3"
)


while True:
	try:
		s = input("User: ")
		
		
		if len(s) == 0: #if there is no input, skip
			continue
		
		if s == "How old are you?":
			print("I am 25")
			continue

		bot_input = bot.get_response(s)
		print("Bot:", bot_input)
	except(KeyboardInterrupt, EOFError, SystemExit):
		break
