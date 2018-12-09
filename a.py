from mongoengine import *
from time import time
from pymongo.errors import DuplicateKeyError
import user
import chat
import chatroom
import sys
from time import time


u = user.myusers.find_one({'username':'stuNNed'})
print('user')
print(u)
print('chatrooms')
print(user.mychatrooms.find_one({'users':u['_id']}))
print('chats')
for x in user.mychats.find({'user':u['_id']}):
	print(x)
