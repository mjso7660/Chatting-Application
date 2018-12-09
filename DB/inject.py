from mongoengine import *
from time import time
import user
import chat
import chatroom
import sys

connect('mydatabase')

file = open(sys.argv[1], 'rt', encoding='UTF-8')
file.readline()
start = time()

for line in file:
	l = line.strip().split(',',5)

	u = []
	# inject users
	if l[3] != '':
		u1 = user.Users.objects(username=l[3]).modify(set__username=l[3],set__pw=user.encrypt_password(l[3]),upsert=True)
		u.append(u1)
	if l[4] != '':
		u2 = user.Users.objects(username=l[4]).modify(set__username=l[4],set__pw=user.encrypt_password(l[4]),upsert=True)
		u.append(u2)

	# inject chatrooms
	for us in u:
		if us is not None:
			c = chatroom.Chatrooms.objects(chatroomID=l[0], channel=l[1]).modify(chatroomID=l[0], channel=l[1], add_to_set__users=us.id,upsert=True)

	# inject chats
	if u[0] is not None and c is not None:
		chat.Chats.objects(user=u[0].id, chatroom=c.id, date=l[2],message=l[5]).modify(user=u[0].id, chatroom=c.id, date=l[2],message=l[5],upsert=True)

print("Time elapsed in seconds: " + str(time()-start))
