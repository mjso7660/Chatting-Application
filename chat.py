import user
import chatroom
import pymongo
from time import time
import datetime
''' Schema
class Chats(Document):
	user = ReferenceField(user.Users, required=True)
	chatroom = ReferenceField(chatroom.Chatrooms,required=True)
	date = DateTimeField()#required=True)
	message = StringField(required=True)
'''

def insertChat(user, chatroom, date, text):
	#current date
	d = datetime.datetime.now().isoformat()

# returns 20 chats
def getChats(u, chatroom, N=50):
	result = []
	chats = user.mychats.find({'chatroom': chatroom['_id']}).limit(N)
	for x in chats:
		if x['user'] == u['_id']:
			result.append({'sender':'me', 'message':x['message'].replace('\"','')})
		else:
			result.append({'sender':'other', 'message':x['message'].replace('\"','')})
	return result

def searchChat(chatroom, keyword):
	# return lists of chat that contain the keyword and few neighboring chats
	result = []
	chats = user.mychats.find({'chatroom': chatroom['_id'], '$text': {'$search':keyword}})
	for x in chats:
		if x['user'] == u['_id']:
			result.append({'sender':'me', 'message':x['message'].replace('\"','')})
		else:
			result.append({'sender':'other', 'message':x['message'].replace('\"','')})
	return result

