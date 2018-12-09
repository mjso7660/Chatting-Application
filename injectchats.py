from mongoengine import *
from time import time
from pymongo.errors import BulkWriteError
import user
import chat
import chatroom
import sys
from time import time
from pprint import pprint

def insert_records(l,total):
	records = []
	batchtime = time()
	begin = time()
	for i, c in enumerate(l):
		cr = user.mychatrooms.find_one({'chatroomID':c[0][0], 'channel':c[0][1]})
		us = user.myusers.find_one({'username': c[1]})
		records.append({'chatroom': cr['_id'], 'user': us['_id'], 'date': c[2], 'message': c[3]})
		if i % 10000 == 0:
			print('Finding record: %8.0f/%8.0f\t%.2f\t%.2f\t%.2f'%(i,len(l),time()-batchtime, time()-begin,time()-total))
			batchtime = time()

	try:
		user.mychats.insert_many(records, ordered=False)
		#user.myusers.insert_one({'username': us, 'pw': user.encryptPassword(us)})
	except BulkWriteError as bwe:
		pprint(bwe.details)
		pass

	print('Inserting record: %8.0f/%8.0f\t%.2f\t%.2f\t%.2f'%(i,len(l),time()-batchtime, time()-begin,time()-total))


file = open(sys.argv[1], 'rt', encoding='UTF-8')
file.readline()
total = time()
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
	if i % 100000 == 0:
		print('Reading line: %8.0f\t%.2f\t%.2f\t%.2f'%(i,time()-batchtime, time()-begin,time()-total))
		insert_records(chatToInsert,total)
		chatToInsert = []

print("Time elapsed in seconds: " + str(time()-total))


