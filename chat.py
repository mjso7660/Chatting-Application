from mongoengine import *
import user
import chatroom

class Chats(Document):
	user = ReferenceField(user.Users, required=True)
	chatroom = ReferenceField(chatroom.Chatrooms,required=True)
	date = DateTimeField()#required=True)
	message = StringField(required=True)

def insertChat(user, chatroom, date, text):
	print('a')

def getChats(u, chatroom):
	result = []
	for x in user.mychats.find({'chatroom': chatroom['_id']}):
		if u['_id'] == x['user']:
			sender = 'me'
		else:
			sender = 'somebody else'
		result.append( (sender, x['date'], x['message']) )
	return result