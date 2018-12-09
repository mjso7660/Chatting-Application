from mongoengine import *
from time import time
from pymongo.errors import DuplicateKeyError
import user
import chat
import chatroom
import sys
from time import time


file = open(sys.argv[1], 'rt', encoding='UTF-8')
file.readline()
begin = time()

i = 0
batchtime = time()
chatToInsert=[]
for line in file:
	l = line.strip().split(',',5)
	# inject users
	# (chatroomID, channel), from, date, message
	chatToInsert.append([(l[0],l[1]),l[3],l[2],l[5]])
	i += 1
	if i % 1000000 == 0:
		print('Reading line: %8.0f\t%.2f\t%.2f'%(i,time()-batchtime, time()-begin))
		batchtime = time()

begin = time()

for c, i in enumerate(chatToInsert):
	cr = user.mychatrooms.find_one({'chatroomID':c[0][0], 'channel':c[0][1]})
	us = user.myusers.find_one({'username': c[1]})
	chatToInsert[i][0] = cr['_id']
	chatToInsert[i][1] = us['_id']
	if i % 1000 == 0:
		print('Finding record: %8.0f/%8.0f\t%.2f\t%.2f'%(i,len(cr),time()-batchtime, time()-begin))
		batchtime = time()

begin=time()
for c, i in enumerate(chatToInsert):
	try:
		user.mychats.insert_one({'chatroom': c[0], 'user': c[1], 'date': c[2], 'message': c[3]})
		#user.myusers.insert_one({'username': us, 'pw': user.encryptPassword(us)})
	except DuplicateKeyError:
		print(DuplicateKeyError.error_document)
		pass

	if i % 1000 == 0:
		print('Inserting record: %8.0f/%8.0f\t%.2f\t%.2f'%(i,len(toinsert),time()-batchtime, time()-begin))
		batchtime = time()

print("Time elapsed in seconds: " + str(time()-begin))
