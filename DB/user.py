from mongoengine import *
import pymongo
from passlib.context import CryptContext

pwd_context = CryptContext(
	schemes=["pbkdf2_sha256"],
	default="pbkdf2_sha256",
	pbkdf2_sha256__default_rounds=30
)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["users"]
# db = mydatabase
# collection = users

class Users(Document):
	username = StringField(required=True)
	pw = StringField(required=True)

# get chatrooms
# get chats
# search chats

def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

def check_password(id, password):
	print("Login attempt: {id:" + id + ",pw:" + password + "}")
	for x in mycol.find({'id':id}):
		return check_encrypted_password(password, x['pw'])

# not to be used
def remove_account(id,password):
	mycol.remove({'id':id})
	print("removed id:" + id)

def insert_account(id, password):
	result = []
	for x in mycol.find({'id': id}):
		result.append(x)
	if len(result) > 0:
		return False
	else:
		mycol.insert_one({'id': id,'pw': encrypt_password(password)})
		return True
