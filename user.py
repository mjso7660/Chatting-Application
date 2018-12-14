import pymongo
from passlib.context import CryptContext

pwd_context = CryptContext(
	schemes=["pbkdf2_sha256"],
	default="pbkdf2_sha256",
	pbkdf2_sha256__default_rounds=30
)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
myusers = mydb["users"]
mychatrooms = mydb["chatrooms"]
mychats = mydb["chats"]
# db = mydatabase
# collection = users

''' Schema
class Users(Document):
	username = StringField(required=True, unique=True)
	pw = StringField(required=True)
'''

def getUser(id):
	return myusers.find_one({'username': id})

# Login / User Control
def encryptPassword(password):
    return pwd_context.encrypt(password)

def checkEncryptedPassword(password, hashed):
    return pwd_context.verify(password, hashed)

def checkPassword(id, password):
	print("Login attempt: {username:" + id + ",pw:" + password + "}")
	for x in myusers.find({'username':id}):
		return checkEncryptedPassword(password, x['pw'])

# not to be used
def removeAccount(id,password):
	myusers.remove({'username':id})
	print("removed id:" + id)

def insertAccount(id, password):
	result = []
	for x in myusers.find({'username': id}):
		result.append(x)
	if len(result) > 0:
		return False
	else:
		myusers.insert_one({'username': id,'pw': encryptPassword(password)})
		return True
