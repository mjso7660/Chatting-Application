import pymongo
import user

'''
# schema
class Chatrooms(Document):
	chatroomID = StringField(required=True)
	channel = StringField(required=True)
	users = ListField(ReferenceField(user.Users), required=True)
'''

def getall(user1):
	# query chatroom with speicified user1 using find in collection
	result = user.mychatrooms.find({'users':user1['_id']})
	return result

def get20(user1):
	result = user.mychatrooms.find({'users':user1['_id']}).limit(20)
	return result

# make sure N is less than length
def getN(user1, N = 20):
	result = user.mychatrooms.find({'users':user1['_id']}).limit(N)
	return result

# add try catch block
def createChatroom(chatroomID, channel, users):
	# make chatroom for multiple users
	uidlist = []
	for u in users:
		userq = user.myusers.find_one({'users': u})
		uidlist.append(userq['_id'])
	cr = {'chatroomID': chatroomID, 'channel': channel, '$addToSet':{'users': uidlist}}
	mychatrooms.insert_one(cr)

def getUsernames(chatroom):
	cr = user.mychatrooms.find_one({'chatroomID': chatroom['chatroomID'], 'channel': chatroom['channel']})
	names = []
	for u in cr['users']:
		us = user.myusers.find_one({'_id':u})
		names.append(us['username'])
	return names