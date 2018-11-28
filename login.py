import sys
import time
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

def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)

def check_password(id, password):
	print("Login attempt: {id:" + id + ",pw:" + password + "}")
	for x in mycol.find({'id':id}):
		print(x)
		return check_encrypted_password(password, x['pw'])