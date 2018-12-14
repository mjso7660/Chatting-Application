from mongoengine import *
from time import time
from pymongo.errors import DuplicateKeyError
import user
import chat
import chatroom
import sys
from time import time


#u = user.myusers.find_one({'username':'stuNNed'})

# query for users
u = user.getUser('stuNNed')

# query for chatrooms. specifying N will allow adjustment of the return size
for cr in chatroom.getN(u):
	print()
	# how to print username
	print('user:', u['username'])
	# how to print chat rooms and channels
	print('chatroom:',cr['chatroomID'], cr['channel'])
	print('----------------------------------------')
	start = time()

	# how to print chats in chatrooms
	for x in chat.getChats(u, cr):
		print(x)


	# how to search for chats
	for x in chat.searchChat(cr,"yes"):
		print(x)
	print(time()-start)
	print('----------------------------------------')
