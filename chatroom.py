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

def makeChatroom(chatroomID, channel, users):
	# make chatroom for multiple users
	userlist = user.myusers.find({'users': users})
	uidlist = []
	for user in userlist:
		uidlist.append(user['_id'])
	cr = {'chatroomID': chatroomID, 'channel': channel, '$addToSet':{'users': users}}
	mychatrooms.insert_one(cr)

