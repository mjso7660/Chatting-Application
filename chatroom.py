from mongoengine import *
import pymongo
import user
# hijb
# db = mydatabase
# collection = chatrooms

class Chatrooms(Document):
	chatroomID = StringField(required=True)
	channel = StringField(required=True)
	users = ListField(ReferenceField(user.Users), required=True)

def makeChatroom(chatroomID, channel, users):
	# make chatroom for multiple users
	userlist = user.myusers.find({'users': users})
	uidlist = []
	for user in userlist:
		uidlist.append(user['_id'])
	cr = {'chatroomID': chatroomID, 'channel': channel, '$addToSet':{'users': users}}
	mychatrooms.insert_one(cr)

def getChatroom(user1):
	# query chatroom with speicified user1 using find in collection
	result = user.mychatrooms.find({'users':user1['_id']})
	return result

def getChats(user, chatroom):
	# query chats within chatroom and return tuple of chat list marked with (mine, chat) and (others, chat)
	print('a')

def searchChat(chatroom, keyword):
	# return lists of chat that contain the keyword and few neighboring chats
	print('a')
