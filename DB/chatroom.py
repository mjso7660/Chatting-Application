from mongoengine import *
import pymongo
import user
# hijb
# db = mydatabase
# collection = chatrooms

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
myusers = mydb["users"]
mychatrooms = mydb["chatrooms"]

class Chatrooms(Document):
	chatroomID = StringField(required=True)
	channel = StringField(required=True)
	users = ListField(ReferenceField(user.Users), required=True)

def makeChatroom(self, chatroomID, channel, users):
	# make chatroom for multiple users
	userlist = myusers.find({'users': users})
	uidlist = []
	for user in userlist:
		uidlist.append(user['_id'])
	cr = {'chatroomID': chatroomID, 'channel': channel, '$addToSet':{'users': users}}
	mychatrooms.insert_one(cr)

def getChatroom(self, user):
	# query chatroom with speicified user using find in collection
	result = mychatrooms.find({'users':user})
	for x in result:
		print(x)
	return result

def getChats(self, user, chatroom):
	# query chats within chatroom and return tuple of chat list marked with (mine, chat) and (others, chat)
	


def searchChat(self, chatroom, keyword):
	# return lists of chat that contain the keyword and few neighboring chats
	print('a')

main():
	