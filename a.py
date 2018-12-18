from mongoengine import *
from time import time
from pymongo.errors import DuplicateKeyError
import user
import chat
import chatroom
import sys
from time import time


#u = user.myusers.find_one({'username':'stuNNed'})

f1 = open('chatdata.txt','w')
f2 = open('searchdata.txt','w')
# query for users
u = user.getUser('stuNNed')
start = time()
numchats = 0
numsearch = 0
numchatrooms = 0
# query for chatrooms. specifying N will allow adjustment of the return size
for cr in chatroom.getall(u):
	# how to print username
	#print('user:', u['username'])
	# how to print chat rooms and channels
	#print('chatroom:',cr['chatroomID'], cr['channel'])
	#print('----------------------------------------')
	numchatrooms += 1
	
	# how to print chats in chatrooms
	for x in chat.getChats(u, cr, 10000):
		f1.write(str(x) + "\n")
		numchats += 1
	
	# how to search for chats
	for x in chat.searchChat(u,cr,"yes"):
		f2.write(str(x) + '\n')
		numsearch += 1
	
print("number of chatrooms: " + str(numchatrooms))
print("number of chats: " + str(numchats))
print("number of searched chats: " + str(numsearch))
print("time: " +str(time()-start))
	