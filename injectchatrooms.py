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
cr = dict()
for line in file:
	l = line.strip().split(',',5)
	# inject users

	key = (l[0], l[1])
	if key not in cr:
		cr[key] = set()

	if l[3] != '':
		cr[key].add(l[3])
	if l[4] != '':
		cr[key].add(l[4])

	'''
	# inject chats
	if u[0] is not None and c is not None:
		chat.Chats.objects(user=u[0].id, chatroom=c.id, date=l[2],message=l[5]).modify(user=u[0].id, chatroom=c.id, date=l[2],message=l[5],upsert=True)
	'''
	i += 1
	if i % 1000000 == 0:
		print('Reading line: %8.0f\t%.2f\t%.2f'%(i,time()-batchtime, time()-begin))
		batchtime = time()

begin = time()
toinsert = dict()
i = 0
for key in cr:
	i += 1
	toinsert[key] = []
	for u in cr[key]:
		toinsert[key].append(user.myusers.find_one({'username': u})['_id'])

	if i % 1000 == 0:
		print('Finding record: %8.0f/%8.0f\t%.2f\t%.2f'%(i,len(cr),time()-batchtime, time()-begin))
		batchtime = time()

i = 0
begin=time()
for key in toinsert:
	i += 1
	try:
		user.mychatrooms.update_one({'chatroomID':key[0], 'channel':key[1]},{'$addToSet': {'users': { '$each': toinsert[key]}}},True)
		#user.myusers.insert_one({'username': us, 'pw': user.encryptPassword(us)})
	except DuplicateKeyError:
		print(DuplicateKeyError.error_document)
		pass

	if i % 1000 == 0:
		print('Inserting record: %8.0f/%8.0f\t%.2f\t%.2f'%(i,len(toinsert),time()-batchtime, time()-begin))
		batchtime = time()

print("Time elapsed in seconds: " + str(time()-begin))
