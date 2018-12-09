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
u = set()

for line in file:
	l = line.strip().split(',',5)
	# inject users
	if l[3] != '':
		u.add(l[3])
	if l[4] != '':
		u.add(l[4])

	'''
	# inject chatrooms
	for us in u:
		if us is not None:
			c = chatroom.Chatrooms.objects(chatroomID=l[0], channel=l[1]).modify(chatroomID=l[0], channel=l[1], add_to_set__users=us.id,upsert=True)

	# inject chats
	if u[0] is not None and c is not None:
		chat.Chats.objects(user=u[0].id, chatroom=c.id, date=l[2],message=l[5]).modify(user=u[0].id, chatroom=c.id, date=l[2],message=l[5],upsert=True)
	'''
	i += 1
	if i % 1000000 == 0:
		print('Reading line: %8.0f\t%.2f\t%.2f'%(i,time()-batchtime, time()-begin))
		batchtime = time()


i = 0
begin=time()
for us in u:
	i += 1
	try:
		user.myusers.insert_one({'username': us, 'pw': user.encryptPassword(us)})
	except DuplicateKeyError:
		pass

	if i % 1000 == 0:
		print('Inserting record: %g/%g\t%.2f\t%.2f'%(i,len(u),time()-batchtime, time()-begin))
		batchtime = time()

print("Time elapsed in seconds: " + str(time()-begin))
