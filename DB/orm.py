from mongoengine import *

import user
import chat
import chatroom
import pymongo

connect('mydatabase')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
myusers = mydb["users"]
mychatrooms = mydb["chatrooms"]

u = user.getUser('stuNNed')
for cr in chatroom.getChatroom(u):
	print(cr)
	for x in chat.getChats(u, cr):
		print(x)

