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

def makeChatroom(self, users):
	# make chatroom for multiple users
	print('a')

def getChatroom(self, user):
	# query chatroom with speicified user using find in collection
	print('a')


def getChats(self):
	# query chats within chatroom and return tuple of chat list marked with (mine, chat) and (others, chat)
	print('a')


def searchChat(self, keyword):
	# return lists of chat that contain the keyword and few neighboring chats
	print('a')
