from chatterbot import ChatBot

chatbot = ChatBot(
	'Terminal',
	trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
chatbot.train(
	"chatterbot.corpus.english",
	"chatterbot.corpus.english.greetings",
	"chatterbot.corpus.english.conversations"
)

