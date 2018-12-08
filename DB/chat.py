from mongoengine import *
import user
import chatroom

class Chats(Document):
	user = ReferenceField(user.Users, required=True)
	chatroom = ReferenceField(chatroom.Chatrooms,required=True)
	date = DateTimeField()#required=True)
	message = StringField(required=True)

class Chat:
	def __init__(self, user, chatroom, date, text):
		self.user = user
		# user should be foreign key referencing a user // it should insert user objectid
		self.chatroom = chatroom
		# chatroom should be foreign key referencing a chatroom // it should insert chatroom objectid
		self.date = date
		# make sure to set date as date format
		self.text = text
		# make sure to set text as a text
