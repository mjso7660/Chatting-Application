import mongoengine
from time import time
from pymongo.errors import BulkWriteError
import user
import chat
import chatroom
import sys

mongoengine.connect('mydatabase')

file = open(sys.argv[1], 'rt', encoding='UTF-8')
file.readline()
start = time()

i = 0
batchno = 1
bulk = []
s = set()
for line in file:
	l = line.strip().split(',',5)
	
	if i < 1000:
		#u = []
		# inject users
		if l[3] != '':
			s.add(l[3])
			#u1 = user.Users.objects(username=l[3]).modify(set__username=l[3],set__pw=user.encrypt_password(l[3]),upsert=True)
			#u.append(u1)
		if l[4] != '':
			s.add(l[4])
			#u2 = user.Users.objects(username=l[4]).modify(set__username=l[4],set__pw=user.encrypt_password(l[4]),upsert=True)
			#u.append(u2)
		for u in s:
			bulk.append({'username': u, 'pw':user.encryptPassword(u)})
		i += 1
	else:
		try:
			user.myusers.insert_many(bulk)
			sys.stderr.write('writing batch ' + str(batchno) + '\n')

		except BulkWriteError as exc:
			#sys.stderr.write(str(exc.details) + '\n')
			sys.stderr.write('failed to write batch ' + str(batchno) + '\n')
			pass
		
		i = 0
		batchno+=1
		s = set()
		bulk = []
	'''
	# inject chatrooms
	for us in u:
		if us is not None:
			c = chatroom.Chatrooms.objects(chatroomID=l[0], channel=l[1]).modify(chatroomID=l[0], channel=l[1], add_to_set__users=us.id,upsert=True)

	# inject chats
	if u[0] is not None and c is not None:
		chat.Chats.objects(user=u[0].id, chatroom=c.id, date=l[2],message=l[5]).modify(user=u[0].id, chatroom=c.id, date=l[2],message=l[5],upsert=True)
	'''
print("Time elapsed in seconds: " + str(time()-start))
